@echo off
REM DgmCraft Başlatıcı - tek tıkla çalıştır (kurulum gerekmez)
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
  python app.py
) else (
  py app.py
)
if %errorlevel% neq 0 (
  echo.
  echo Python bulunamadi. Python 3.12+ kurman gerekiyor.
  pause
)
