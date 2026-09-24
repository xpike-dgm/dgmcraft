@echo off
setlocal
cd /d "%~dp0launcher"
start "" pythonw "qt.py"
exit
