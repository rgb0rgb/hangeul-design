@echo off
setlocal
set PORT=8504

echo Stopping Hangeul Design on port %PORT%...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$pids = Get-NetTCPConnection -LocalPort %PORT% -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; if (-not $pids) { exit 2 }; foreach ($pid in $pids) { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue }; exit 0"

if errorlevel 2 goto notrunning
if errorlevel 1 goto fail

echo Hangeul Design stopped.
endlocal
exit /b 0

:notrunning
echo Hangeul Design is not running on port %PORT%.
endlocal
exit /b 0

:fail
echo [ERROR] Failed to stop Hangeul Design.
pause
endlocal
exit /b 1
