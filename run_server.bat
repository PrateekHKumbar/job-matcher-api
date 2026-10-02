@echo off
title JobTrack AI - Application Tracker & ATS Matcher API
echo ==========================================================
echo Starting JobTrack AI Server on http://127.0.0.1:8080
echo ==========================================================
cd /d "%~dp0"
call .venv\Scripts\activate.bat
.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8080 --reload
pause
