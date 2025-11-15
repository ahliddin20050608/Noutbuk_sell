@echo off
echo ====================================
echo   BOT TO'XTATILMOQDA...
echo ====================================
echo.

REM Python processlarini to'xtatish
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *main.py*" 2>nul
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq *main.py*" 2>nul

REM Barcha python processlarini to'xtatish (ehtiyotkorlik bilan)
echo Python processlarini to'xtatish...
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "python.exe"') do (
    echo Process %%a to'xtatilmoqda...
    taskkill /F /PID %%a 2>nul
)

echo.
echo ====================================
echo   BOT TO'XTATILDI!
echo ====================================
timeout /t 3 /nobreak >nul

