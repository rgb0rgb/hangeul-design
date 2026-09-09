@echo off
setlocal
cd /d "%~dp0"
set PORT=8504

if not exist "venv\Scripts\python.exe" (
    py -m venv venv
    if errorlevel 1 goto fail
)

venv\Scripts\python -c "import streamlit,sys; sys.exit(0 if tuple(map(int,streamlit.__version__.split('.')[:2])) >= (1,55) else 1)" >nul 2>nul
if errorlevel 1 (
    echo [SETUP] Installing supported dependencies...
    venv\Scripts\python -m pip install --upgrade -r requirements.txt
    if errorlevel 1 goto fail
)

netstat -ano | findstr ":%PORT%" | findstr "LISTENING" >nul 2>nul
if not errorlevel 1 (
    echo [ERROR] Port %PORT% is already in use. Run stop.bat first.
    pause
    exit /b 1
)

start "Hangeul Design Server" /MIN "%CD%\venv\Scripts\python.exe" -m streamlit run "%CD%\app_reference.py" --server.address localhost --server.port %PORT% --server.headless false
if errorlevel 1 goto fail

echo Hangeul Design starting on http://localhost:%PORT%
endlocal
exit /b 0

:fail
echo [ERROR] Hangeul Design failed to start.
pause
endlocal
exit /b 1
