@echo off
title AI Recruitment Copilot - Launcher
color 0A

echo =====================================================================
echo              STARTING AI RECRUITMENT COPILOT PLATFORM
echo =====================================================================
echo.

cd /d "c:\Users\kvija\Downloads\Project"

echo [1/3] Launching FastAPI Backend Server (Port 8000)...
start "AI Copilot - Backend Server (Port 8000)" cmd /k "python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/3] Launching Web Frontend Server (Port 3000)...
start "AI Copilot - Frontend Server (Port 3000)" cmd /k "python -m http.server 3000"

echo [3/3] Launching Streamlit Recruitment Dashboard (Port 8501)...
start "AI Copilot - Streamlit Dashboard (Port 8501)" cmd /k "streamlit run streamlit_app.py --server.port=8501"

echo.
echo Waiting for servers to initialize...
timeout /t 4 /nobreak >nul

echo.
echo =====================================================================
echo                        ALL SERVICES ONLINE!
echo =====================================================================
echo  Main Landing Portal:    http://127.0.0.1:3000
echo  Candidate Portal:       http://127.0.0.1:3000/candidate_portal/index.html
echo  Recruiter Portal:       http://127.0.0.1:3000/recruiter_portal/index.html
echo  Streamlit Dashboard:    http://127.0.0.1:8501
echo  API Swagger Docs:       http://127.0.0.1:8000/docs
echo =====================================================================
echo.

start http://127.0.0.1:3000

pause
