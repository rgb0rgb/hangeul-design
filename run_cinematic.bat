@echo off
setlocal
cd /d "%~dp0"
set PORT=8505

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
    echo [ERROR] Cinematic port %PORT% is already in use. Stop the existing cinematic app first.
    pause
    exit /b 1
)

start "Hangeul Design Cinematic Server" /B venv\Scripts\python -m streamlit run app_cinematic.py --server.address localhost --server.port %PORT% --server.headless true
for /L %%I in (1,1,30) do (
    powershell -NoProfile -Command "try { $r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 http://localhost:%PORT%/_stcore/health; if($r.StatusCode -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>nul
    if not errorlevel 1 goto ready
    timeout /t 1 /nobreak >nul
)
goto fail

:ready
start "" "http://localhost:%PORT%"
echo Cinematic ready: http://localhost:%PORT%
endlocal
exit /b 0

:fail
echo [ERROR] Hangeul Design Cinematic failed to start.
pause
endlocal
exit /b 1
