@echo off
setlocal
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    py -m venv venv
    venv\Scripts\python -m pip install -r requirements.txt
)

venv\Scripts\python -m pip install --upgrade --force-reinstall pyinstaller
if errorlevel 1 goto fail

venv\Scripts\python -m PyInstaller.__main__ -F -n HangeulDesign_Streamlit_Launcher launcher.py --noconfirm
if errorlevel 1 goto fail

echo.
echo [OK] dist\HangeulDesign_Streamlit_Launcher.exe created.
pause
endlocal
exit /b 0

:fail
echo.
echo [ERROR] Build failed.
pause
endlocal
exit /b 1
