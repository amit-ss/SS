"""
Provider-agnostic LLM layer for CampusGPT.

Supported providers
-------------------
ollama_local  : Ollama running on the same machine as Django (default http://localhost:11434)
ollama_cloud  : Ollama's hosted API (https://ollama.com) - needs OLLAMA_API_KEY
gemini        : Google Gemini - needs GEMINI_API_KEY

Selection
---------
AI_PROVIDER=auto (default) tries local -> cloud -> gemini and uses the first that answers.
AI_PROVIDER=ollama_local | ollama_cloud | gemini puts that provider first; the others
remain as automatic fallbacks. A single request can override this with `provider=`.
If every provider fails the caller falls back to the built-in verified-answer engine.
"""
import json
import logging
import re
from dataclasses import dataclass
from typing import List, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

PROVIDER_ORDER = ['ollama_local', 'ollama_cloud', 'gemini']
PROVIDER_LABELS = {
    'ollama_local': 'Ollama (Local)',
    'ollama_cloud': 'Ollama (Cloud)',
    'gemini': 'Google Gemini',
}


class LLMError(Exception):
    pass


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str


def _cfg(name: str, default=''):
    return getattr(settings, name, default) or default


def extract_json(text: str, expect: str = 'list'):
    """Pull JSON out of an LLM reply (handles ```json fences and chatty preambles)."""
    cleaned = (text or '').replace('```json', '```').strip()
    if '```' in cleaned:
        parts = cleaned.split('```')
        # the fenced block is normally the second chunk
        cleaned = max(parts, key=lambda p: ('[' in p or '{' in p) and len(p)).strip()

    opener, closer = ('[', ']') if expect == 'list' else ('{', '}')
    start, end = cleaned.find(opener), cleaned.rfind(closer)
    candidate = cleaned[start:end + 1] if start != -1 and end > start else cleaned

    try:
        data = json.loads(candidate)
    except json.JSONDecodeError:
        # last resort: a lenient scan for the first decodable value
        decoder = json.JSONDecoder()
        data = None
        for m in re.finditer(r'[\[{]', cleaned):
            try:
                data, _ = decoder.raw_decode(cleaned[m.start():])
                break
            except json.JSONDecodeError:
                continue
        if data is None:
            raise

    if expect == 'list' and isinstance(data, dict):
        # models often wrap the array: {"questions": [...]}
        for value in data.values():
            if isinstance(value, list):
                return value
    return data


class LLMRouter:
    # ------------------------------------------------------------------ config
    @property
    def local_host(self) -> str:
        return _cfg('OLLAMA_HOST', 'http://localhost:11434').rstrip('/')

    @property
    def local_model(self) -> str:
        return _cfg('OLLAMA_MODEL', 'llama3.2')

    @property
    def cloud_host(self) -> str:
        return _cfg('OLLAMA_CLOUD_HOST', 'https://ollama.com').rstrip('/')

    @property
    def cloud_model(self) -> str:
        return _cfg('OLLAMA_CLOUD_MODEL', 'gpt-oss:120b')

    @property
    def cloud_key(self) -> str:
        return _cfg('OLLAMA_API_KEY', '')

    @property
    def gemini_key(self) -> str:
        return _cfg('GEMINI_API_KEY', '')

    @property
    def gemini_model(self) -> str:
        return _cfg('GEMINI_MODEL', 'gemini-1.5-flash')

    @property
    def timeout(self) -> int:
        try:
            return int(_cfg('OLLAMA_TIMEOUT', 120))
        except (TypeError, ValueError):
            return 120

    def default_provider(self) -> str:
        value = str(_cfg('AI_PROVIDER', 'auto')).strip().lower()
        return value if value in PROVIDER_ORDER else 'auto'

    @property
    def enabled(self) -> bool:
        """True when at least one provider could plausibly answer."""
        return True  # local Ollama is always worth trying; failures fall through quickly

    # --------------------------------------------------------------- ordering
    def provider_chain(self, requested: Optional[str] = None) -> List[str]:
        first = (requested or self.default_provider() or 'auto').lower()
        chain = list(PROVIDER_ORDER)
        if first in PROVIDER_ORDER:
            chain.remove(first)
            chain.insert(0, first)
        # skip providers that clearly cannot work (no key configured)
        out = []
        for p in chain:
            if p == 'ollama_cloud' and not self.cloud_key:
                continue
            if p == 'gemini' and not self.gemini_key:
                continue
            out.append(p)
        return out

    # ---------------------------------------------------------------- status
    def status(self) -> list:
        default = self.default_provider()
        items = []

        local_ok, local_models, local_err = False, [], ''
        try:
            r = requests.get(f'{self.local_host}/api/tags', timeout=(2, 4))
            r.raise_for_status()
            local_models = [m.get('name') for m in r.json().get('models', [])]
            local_ok = True
        except Exception as e:
            local_err = 'Ollama is not running on this machine (start it with `ollama serve`).' \
                if isinstance(e, requests.ConnectionError) else str(e)
        model_missing = local_ok and not any(
            m == self.local_model or (m or '').split(':')[0] == self.local_model.split(':')[0]
            for m in local_models
        )
        items.append({
            'id': 'ollama_local', 'label': PROVIDER_LABELS['ollama_local'],
            'model': self.local_model, 'available': local_ok and not model_missing,
            'detail': local_err or (f'Model "{self.local_model}" not pulled. Run: ollama pull {self.local_model}'
                                    if model_missing else 'Ready'),
            'installed_models': local_models,
        })
        items.append({
            'id': 'ollama_cloud', 'label': PROVIDER_LABELS['ollama_cloud'],
            'model': self.cloud_model, 'available': bool(self.cloud_key),
            'detail': 'Ready' if self.cloud_key else 'Set OLLAMA_API_KEY in backend/.env',
        })
        items.append({
            'id': 'gemini', 'label': PROVIDER_LABELS['gemini'],
            'model': self.gemini_model, 'available': bool(self.gemini_key),
            'detail': 'Ready' if self.gemini_key else 'Set GEMINI_API_KEY in backend/.env',
        })
        for item in items:
            item['is_default'] = (item['id'] == default)
        return items

    # ------------------------------------------------------------- generation
    def generate(self, prompt: str, system: str = '', history: Optional[list] = None,
                 provider: Optional[str] = None) -> LLMResponse:
        errors = []
        for name in self.provider_chain(provider):
            try:
                if name == 'ollama_local':
                    return self._ollama(name, self.local_host, self.local_model, None, prompt, system, history)
                if name == 'ollama_cloud':
                    return self._ollama(name, self.cloud_host, self.cloud_model, self.cloud_key, prompt, system, history)
                if name == 'gemini':
                    return self._gemini(prompt, system, history)
            except Exception as e:
                logger.warning('LLM provider %s failed: %s', name, e)
                errors.append(f'{name}: {e}')
        raise LLMError('; '.join(errors) or 'No AI provider configured')

    def _ollama(self, name, host, model, api_key, prompt, system, history) -> LLMResponse:
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        for item in (history or []):
            role = 'user' if item.get('role') == 'user' else 'assistant'
            messages.append({'role': role, 'content': item.get('content', '')})
        messages.append({'role': 'user', 'content': prompt})

        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'

        resp = requests.post(
            f'{host}/api/chat',
            headers=headers,
            json={'model': model, 'messages': messages, 'stream': False},
            timeout=(3, self.timeout),  # fail fast if Ollama is not running, wait longer for generation
        )
        if resp.status_code == 404:
            raise LLMError(f'model "{model}" not found on {host}')
        if resp.status_code in (401, 403):
            raise LLMError('authentication failed - check OLLAMA_API_KEY')
        resp.raise_for_status()

        text = (resp.json().get('message') or {}).get('content', '').strip()
        if not text:
            raise LLMError('empty response')
        return LLMResponse(text=text, provider=name, model=model)

    def _gemini(self, prompt, system, history) -> LLMResponse:
        import google.generativeai as genai
        genai.configure(api_key=self.gemini_key)
        model = genai.GenerativeModel(model_name=self.gemini_model, system_instruction=system or None)

        contents = []
        for item in (history or []):
            role = 'user' if item.get('role') == 'user' else 'model'
            contents.append({'role': role, 'parts': [item.get('content', '')]})
        contents.append({'role': 'user', 'parts': [prompt]})

        response = model.generate_content(contents)
        text = (response.text or '').strip()
        if not text:
            raise LLMError('empty response')
        return LLMResponse(text=text, provider='gemini', model=self.gemini_model)


llm_router = LLMRouter()
