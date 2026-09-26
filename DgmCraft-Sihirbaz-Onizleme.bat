@echo off
REM Kurulum sihirbazini ONIZLEME modunda acar: tum 7 adim gezilebilir,
REM Syncthing/Tailscale kontrolu yapilmaz, hicbir ayar kaydedilmez.
REM Kapatmak icin Esc veya pencereyi kapat. Geri almak icin bu dosyayi sil.
setlocal
cd /d "%~dp0launcher"
set DGM_SIHIRBAZ_GEC=1
start "" pythonw "qt.py"
exit
