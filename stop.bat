@echo off
setlocal
set PORT=8504

echo Stopping Hangeul Design on port %PORT%...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$owners = Get-NetTCPConnection -LocalPort %PORT% -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; if (-not $owners) { exit 2 }; foreach ($processId in $owners) { Stop-Process -Id $processId -Force -ErrorAction Stop }; Start-Sleep -Milliseconds 500; $still = Get-NetTCPConnection -LocalPort %PORT% -State Listen -ErrorAction SilentlyContinue; if ($still) { exit 1 } else { exit 0 }"

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
