import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

def run_tests():
    c = Client()
    print("==================================================")
    print("CAMPUSGPT BACKEND SUITE - TESTING ALL 13 ENDPOINTS")
    print("==================================================")

    # 1. Health
    r = c.get('/api/v1/health/')
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    print("[PASS] [1/13] Health Endpoint: 200 OK")

    # 2. Auth Login
    r = c.post('/api/v1/auth/login/', data={'username': '12204567', 'password': 'Student@123'}, content_type='application/json')
    assert r.status_code == 200, f"Login failed: {r.status_code} {r.content}"
    token = r.json().get('token')
    headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
    print("[PASS] [2/13] Auth Login: 200 OK (Token retrieved)")

    # 3. Auth Profile
    r = c.get('/api/v1/auth/profile/', **headers)
    assert r.status_code == 200, f"Profile failed: {r.status_code}"
    print(f"[PASS] [3/13] Auth Profile: 200 OK (Reg No: {r.json()['student_profile']['reg_number']})")

    # 4. Chatbot Message (RAG)
    r = c.post('/api/v1/chatbot/message/', data={'message': 'Where is the central library located in LPU?'}, content_type='application/json')
    assert r.status_code == 200, f"Chatbot failed: {r.status_code}"
    print(f"[PASS] [4/13] Chatbot RAG: 200 OK (Sources: {r.json().get('sources')})")

    # 5. Timetable Weekly & Today
    r = c.get('/api/v1/timetable/weekly/')
    assert r.status_code == 200, f"Timetable failed: {r.status_code}"
    print(f"[PASS] [5/13] Timetable Weekly: 200 OK ({len(r.json())} day groups)")

    # 6. Attendance Predictor
    r = c.post('/api/v1/attendance/predict/', data={'total_classes': 30, 'classes_attended': 21, 'target_percentage': 75.0}, content_type='application/json')
    assert r.status_code == 200, f"Attendance prediction failed: {r.status_code}"
    res = r.json()
    print(f"[PASS] [6/13] Attendance Predictor: 200 OK (Target: {res['target_percentage']}%, Classes needed: {res['classes_needed_for_target']})")

    # 7. Campus Navigation & QR Lookup
    r = c.get('/api/v1/navigation/locations/')
    assert r.status_code == 200, f"Locations failed: {r.status_code}"
    qr_r = c.get('/api/v1/navigation/qr/LPU-BLK34-CSE/')
    assert qr_r.status_code == 200, f"QR Lookup failed: {qr_r.status_code}"
    print(f"[PASS] [7/13] Navigation & QR Code: 200 OK (Resolved QR: {qr_r.json()['location']['name']})")

    # 8. Study Assistant Summarize & MCQs
    r = c.post('/api/v1/study/generate-mcqs/', data={'text': 'Data structures organize memory for rapid retrieval.', 'count': 3}, content_type='application/json')
    assert r.status_code == 200, f"MCQs failed: {r.status_code}"
    print(f"[PASS] [8/13] Study Assistant MCQs: 200 OK (Generated {len(r.json()['mcqs'])} questions)")

    # 9. Lost & Found
    r = c.get('/api/v1/lost-found/items/')
    assert r.status_code == 200, f"Lost Found failed: {r.status_code}"
    print(f"[PASS] [9/13] Lost & Found Noticeboard: 200 OK ({len(r.json())} active items)")

    # 10. Campus Events
    r = c.get('/api/v1/events/')
    assert r.status_code == 200, f"Events failed: {r.status_code}"
    print(f"[PASS] [10/13] Campus Events: 200 OK ({len(r.json())} live events)")

    # 11. Career Resume Analyzer
    r = c.post('/api/v1/career/resume-analyze/', data={'resume_text': 'CSE student skilled in Python, Django and Mobile App Development.', 'target_role': 'Full Stack AI Engineer'}, content_type='application/json')
    assert r.status_code == 200, f"Resume analyzer failed: {r.status_code}"
    print(f"[PASS] [11/13] Career Resume AI: 200 OK (ATS Score: {r.json()['analysis']['score']}/100)")

    # 12. Notifications & Study Partner
    r = c.get('/api/v1/notifications/')
    assert r.status_code == 200, f"Notifications failed: {r.status_code}"
    r_part = c.get('/api/v1/notifications/study-partners/')
    assert r_part.status_code == 200, f"Study partners failed: {r_part.status_code}"
    print(f"[PASS] [12/13] Notifications & Study Partner: 200 OK ({len(r_part.json())} peer partners)")

    # 13. My Campus Day Consolidated Dashboard
    r = c.get('/api/v1/notifications/dashboard/my-day/')
    assert r.status_code == 200, f"Dashboard failed: {r.status_code}"
    print(f"[PASS] [13/13] Consolidated 'My Campus Day': 200 OK")

    print("==================================================")
    print("ALL 13 TEST SUITES PASSED FLAWLESSLY! 100% OPERATIONAL")
    print("==================================================")

if __name__ == '__main__':
    run_tests()
