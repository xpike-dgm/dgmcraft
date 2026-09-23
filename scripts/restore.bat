@echo off
REM DGM Craft geri yukleme
REM Kullanim: scripts\restore.bat backups\dgmcraft_YYYY-MM-DD_HH-mm.zip

set SERVERROOT=C:\Users\Xpike\Desktop\DgmCraftt

if "%~1"=="" (
  echo Kullanim: scripts\restore.bat backups\dgmcraft_YYYY-MM-DD_HH-mm.zip
  echo Ornek: scripts\restore.bat backups\dgmcraft_2026-09-22_20-30.zip
  exit /b 1
)

if not exist "%~1" (
  echo HATA: yedek bulunamadi: %~1
  exit /b 1
)

echo 1. Sunucuyu durdurun. Henuz durdurmadiysaniz ayri pencerede scripts\stop.bat calistirin
echo    veya konsola stop yazin. Devam etmeden once konsolun kapandigini dogrulayin.
pause

echo 2. Guvenlik yedegi aliniyor (mevcut durumun uzerine yazilmadan once)...
powershell -ExecutionPolicy Bypass -File "%SERVERROOT%\scripts\backup.ps1"
if errorlevel 1 (
  echo UYARI: guvenlik yedegi alinamadi. Devam etmek risklidir.
  pause
)

echo 3. Yedekten geri yukleniyor: %~1
powershell -Command "Expand-Archive -LiteralPath '%~1' -DestinationPath '%SERVERROOT%' -Force"
if errorlevel 1 (
  echo HATA: geri yukleme basarisiz.
  exit /b 1
)

echo 4. Tamamlandi. Simdi baslatip kontrol edin:
echo    scripts\start.bat
echo    Ardindan docs\recovery.md dogrulama listesini uygulayin.
pause
