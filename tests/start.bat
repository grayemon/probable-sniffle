@echo off
REM ============================================
REM Run Python server and ngrok tunnel
REM ============================================

REM Check if Python and ngrok are available
where python >nul 2>&1 || (echo Python not found! & pause & exit /b)
where ngrok >nul 2>&1 || (echo ngrok not found! & pause & exit /b)

REM Start the Python server
start "Python Server" python server.py

REM Wait a moment to ensure the server is up
timeout /t 5 /nobreak >nul

REM Start ngrok on port 3000 with reserved URL for chatwoot
start "ngrok Tunnel" ngrok http 3000 --url lemur-unbiased-usefully.ngrok-free.app

pause
