@echo off
setlocal
cd /d "%~dp0"

set PORT=8504

if not exist "venv\Scripts\python.exe" (
    py -m venv venv
    if errorlevel 1 goto fail
)

venv\Scripts\python -c "import streamlit" >nul 2>nul
if errorlevel 1 (
    venv\Scripts\python -m pip install --force-reinstall -r requirements.txt
    if errorlevel 1 goto fail
)

netstat -ano | findstr ":%PORT%" | findstr "LISTENING" >nul 2>nul
if not errorlevel 1 (
    echo.
    echo [INFO] Hangeul Design is already running or port %PORT% is already in use.
    echo Open this address in your browser:
    echo http://localhost:%PORT%
    echo.
    pause
    endlocal
    exit /b 0
)

echo.
echo Starting Hangeul Design...
echo Open this address in your browser:
echo http://localhost:%PORT%
echo.
venv\Scripts\python -m streamlit run app.py --server.address localhost --server.port %PORT%
if errorlevel 1 goto fail
endlocal
exit /b 0

:fail
echo.
echo [ERROR] Hangeul Design failed to start.
echo Please check the error message above.
pause
endlocal
exit /b 1
