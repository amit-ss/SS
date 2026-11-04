@echo off
echo ===================================================
echo Starting CampusGPT Django REST Backend Server...
echo ===================================================
cd /d "%~dp0backend"
C:\Python313\python.exe manage.py runserver 0.0.0.0:8000
pause
