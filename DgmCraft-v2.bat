@echo off
REM DGM Craft v2 onizleme (yeni kabuk). Konsol birakmaz.
cd /d "%~dp0launcher"
where pythonw >nul 2>nul
if %errorlevel%==0 (
  start "" pythonw v2.py
) else (
  start "" python v2.py
)
exit
