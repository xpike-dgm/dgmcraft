# DGM Craft web kurulumu. Tekrar çalıştırılabilir (kaldığı yerden devam eder).
# Kullanım (paylaşılacak tek satır TEK-SATIR.txt içinde):
#   powershell -NoProfile -ExecutionPolicy Bypass -Command "irm <HAM-URL>/Kur.ps1 | iex"
param(
    [string]$Repo = "xpike-dgm/dgmcraft",
    [string]$Hedef = "$HOME\Desktop\DgmCraftt"
)

$ErrorActionPreference = "Stop"
function Yaz([string]$m) { Write-Host "[DgmCraft] $m" }

Yaz("Hedef: $Hedef")
if (-not (Test-Path -LiteralPath $Hedef)) {
    New-Item -ItemType Directory -Path $Hedef | Out-Null
}

# 1) Python kontrolü (kaynak koddan çalışmak için gerekli)
$python = (Get-Command python -ErrorAction SilentlyContinue) -or (Get-Command py -ErrorAction SilentlyContinue)
if (-not $python) {
    Yaz("Python bulunamadı. https://www.python.org/downloads/ adresinden Python 3.12+ kur,")
    Yaz("kurulumda 'Add python.exe to PATH' kutusunu işaretle, sonra bu scripti tekrar çalıştır.")
    exit 1
}
Yaz("Python tamam.")

# 2) Repo güncel mi? .git varsa çek, yoksa zip indir.
if (Test-Path -LiteralPath (Join-Path $Hedef ".git")) {
    Yaz("Repo mevcut, güncelleniyor...")
    & git -C $Hedef pull --ff-only 2>&1 | Select-Object -First 3
} else {
    $zipUrl = "https://github.com/$Repo/archive/refs/heads/main.zip"
    $tmp = Join-Path $env:TEMP "dgmcraft-repo.zip"
    Yaz("Repo indiriliyor...")
    Invoke-WebRequest -Uri $zipUrl -OutFile $tmp
    Yaz("Çıkarılıyor...")
    $tmpAc = Join-Path $env:TEMP "dgmcraft-ac"
    if (Test-Path -LiteralPath $tmpAc) { Remove-Item -Recurse -Force -LiteralPath $tmpAc }
    Expand-Archive -LiteralPath $tmp -DestinationPath $tmpAc -Force
    $ic = Get-ChildItem -LiteralPath $tmpAc -Directory | Select-Object -First 1
    Get-ChildItem -LiteralPath $ic.FullName | ForEach-Object {
        $h = Join-Path $Hedef $_.Name
        if (Test-Path -LiteralPath $h) { Remove-Item -Recurse -Force -LiteralPath $h }
        Move-Item -LiteralPath $_.FullName -Destination $h
    }
    Remove-Item -Recurse -Force -LiteralPath $tmpAc
    Remove-Item -Force -LiteralPath $tmp
}

# 3) Başlatıcıyı aç (geri kalanı sihirbaz halleder: eşleşme + kontroller).
Yaz("Hazır. Başlatıcı açılıyor — sihirbazı takip et.")
$baslat = Join-Path $Hedef "DgmCraft-Baslat.bat"
if (Test-Path -LiteralPath $baslat) {
    Start-Process -FilePath $baslat
} else {
    Start-Process -FilePath "python" -ArgumentList "`"$Hedef\launcher\app.py`"" -WorkingDirectory "$Hedef\launcher"
}
