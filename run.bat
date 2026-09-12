@echo off
title Fruit Angle Detector - Web App
echo ========================================================
echo         Fruit Angle Detector - Server Launcher
echo ========================================================
echo.

cd /d "%~dp0"

REM 1. Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else (
    echo [!] Virtual environment not ready yet. Please wait.
    pause
    exit /b 1
)

REM 2. Check if packages are installed
python -c "import fastapi, cv2" >nul 2>nul
if errorlevel 1 (
    echo [*] Initial setup in progress: installing required computer vision packages...
    echo [*] Please wait a moment while packages finish installing...
    echo.
    if exist "%LOCALAPPDATA%\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe" (
        "%LOCALAPPDATA%\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe" pip install --python "%~dp0.venv\Scripts\python.exe" -r "%~dp0requirements.txt"
    ) else (
        pip install -r requirements.txt
    )
)

REM 3. Launch the web server
echo.
echo [*] Starting Fruit Angle Detector Server...
echo [*] Opening browser at http://localhost:8000
echo [*] Press Ctrl+C in this window to stop the server.
echo.

start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8000"

python main.py

if errorlevel 1 (
    echo.
    echo [!] Server stopped.
    pause
)
