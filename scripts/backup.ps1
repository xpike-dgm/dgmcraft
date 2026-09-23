# DGM Craft yedekleme scripti — PowerShell 5.1 uyumlu
# Kullanim: powershell -ExecutionPolicy Bypass -File scripts\backup.ps1
# Oneri: calistirmadan once konsolda save-all flush yazin.

$ServerRoot = 'C:\Users\Xpike\Desktop\DgmCraftt'
$BackupDir = Join-Path $ServerRoot 'backups'
$DateStamp = Get-Date -Format 'yyyy-MM-dd_HH-mm'
$ZipPath = Join-Path $BackupDir ("dgmcraft_" + $DateStamp + ".zip")

if (-not (Test-Path -LiteralPath $ServerRoot)) {
    Write-Host "HATA: ServerRoot bulunamadi: $ServerRoot"
    exit 1
}

if (-not (Test-Path -LiteralPath $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

Write-Host "DGM Craft yedekleniyor..."
Write-Host "Kaynak: $ServerRoot"
Write-Host "Hedef: $ZipPath"

$ItemsToZip = @()

# world* (26.2 tek klasor + dimensions altinda nether/end)
$WorldPaths = Get-ChildItem -LiteralPath $ServerRoot -Filter 'world*' | ForEach-Object { $_.FullName }
foreach ($p in $WorldPaths) { $ItemsToZip += $p }

# plugins (config + SQLite/H2 veritabanlari)
$PluginsPath = Join-Path $ServerRoot 'plugins'
if (Test-Path -LiteralPath $PluginsPath) { $ItemsToZip += $PluginsPath }

# Paper config klasoru varsa
$ConfigPath = Join-Path $ServerRoot 'config'
if (Test-Path -LiteralPath $ConfigPath) { $ItemsToZip += $ConfigPath }

# kokteki json / yml / properties dosyalari
$RootFiles = Get-ChildItem -LiteralPath $ServerRoot -File | Where-Object {
    $_.Extension -eq '.json' -or $_.Extension -eq '.yml' -or $_.Extension -eq '.properties'
} | ForEach-Object { $_.FullName }
foreach ($f in $RootFiles) { $ItemsToZip += $f }

if ($ItemsToZip.Count -eq 0) {
    Write-Host "HATA: yedeklenecek dosya bulunamadi."
    exit 1
}

Compress-Archive -Path $ItemsToZip -DestinationPath $ZipPath -CompressionLevel Optimal -Force

Write-Host "Yedek tamamlandi: $ZipPath"

# 7 gunluk rotasyon
$Limit = (Get-Date).AddDays(-7)
$OldBackups = Get-ChildItem -LiteralPath $BackupDir -Filter 'dgmcraft_*.zip' | Where-Object { $_.LastWriteTime -lt $Limit }
foreach ($old in $OldBackups) {
    Write-Host ("Siliniyor (7 gunden eski): " + $old.FullName)
    Remove-Item -LiteralPath $old.FullName -Force
}

Write-Host "Rotasyon tamamlandi."
