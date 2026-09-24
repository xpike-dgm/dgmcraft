@echo off
REM DGM Craft - tek tikla baslatma (sunucu + site uygulamasi birlikte)
REM Konsol penceresi birakmaz, yanlislikla X'e basma riski yoktur.
cd /d "%~dp0launcher"
where pythonw >nul 2>nul
if %errorlevel%==0 (
  start "" pythonw app.py
) else (
  start "" python app.py
)
exit
