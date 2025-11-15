@echo off
:start
cd /d "%~dp0"
echo ====================================
echo   TELEGRAM BOT ISHGA TUSHMOGDA...
echo   Vaqt: %date% %time%
echo ====================================
echo.

REM Virtual environment aktivlashtirish
call env\Scripts\activate.bat

REM Botni ishga tushirish
python main.py

REM Agar bot to'xtasa, qayta ishga tushirish
if errorlevel 1 (
    echo.
    echo ====================================
    echo   BOT XATOLIK BILAN TO'XTADI!
    echo   10 soniyadan keyin qayta ishga tushiriladi...
    echo   Vaqt: %date% %time%
    echo ====================================
    timeout /t 10 /nobreak >nul
    goto :start
) else (
    echo.
    echo ====================================
    echo   BOT TO'XTATILDI!
    echo   Vaqt: %date% %time%
    echo ====================================
    timeout /t 5 /nobreak >nul
    goto :start
)

