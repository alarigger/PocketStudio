@echo off

cd /d %~dp0

echo Starting backend...

start cmd /k "cd backend && uvicorn app:app --host 127.0.0.1 --port 8000"

timeout /t 3 > nul

echo Starting frontend...

start cmd /k "cd frontend && python main.py"