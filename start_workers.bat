@echo off

echo Starting Worker 2 on port 5001...
start "Worker2" python worker.py 2 5001
timeout /t 3 /nobreak > nul

echo worker started!
