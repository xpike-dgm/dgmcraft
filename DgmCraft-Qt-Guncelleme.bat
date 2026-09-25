@echo off
setlocal
cd /d "%~dp0launcher"
if /i "%~1"=="guncelleme" (
  start "" pythonw "qt.py" --guncelleme
) else (
  start "" pythonw "qt.py"
)
exit
