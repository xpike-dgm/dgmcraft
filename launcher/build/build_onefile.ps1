# Tek klasor / tek EXE derleme. Python 3.12 64-bit gerektirir. UAC istemez.
$ErrorActionPreference = "Stop"
$kok = $PSScriptRoot
$proje = Join-Path $kok ".."
Set-Location $proje
python -m pip install --upgrade pyinstaller
# Tek klasor (onerilen, hizli acilis):
python -m PyInstaller --noconfirm --windowed --name DgmCraft --paths launcher launcher/app.py
# Tek EXE (istersen):
# python -m PyInstaller --noconfirm --windowed --onefile --name DgmCraft-TekExe --paths launcher launcher/app.py
Write-Host "Cikti: dist/DgmCraft/ altinda. purpur.jar yanina kopyala."
