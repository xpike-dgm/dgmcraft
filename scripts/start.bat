@echo off
REM DGM Craft - Baslatma scripti (Windows)
REM Java 25 portable, Purpur 26.2, 3GB heap (16GB sistem icin guvenli)
REM KRITIK: -Duser.language=en -Duser.country=US sarti.
REM Sebep: Windows sistem dili tr-TR iken bazi pluginler (or. BeautyQuests)
REM String.toLowerCase() cagrilarinda Turkce "I->ı" donusumu yuzunden
REM config anahtarlarini bulamaz (kok neden: 2026-09-22 arastirmasi).
REM Oyuncu gorunur metinler yine Turkce (plugin dil dosyalariyla).
setlocal
REM Once sunucu kokune gec (yoksa dunya/config yanlis klasore acilir)
cd /d "%~dp0.."
set JAVA_EXE=%~dp0..\runtime\jdk-25.0.4.1+1\bin\java.exe
if not exist "%JAVA_EXE%" set JAVA_EXE=java
"%JAVA_EXE%" "-Dfile.encoding=UTF-8" "-Duser.language=en" "-Duser.country=US" -Xms3G -Xmx3G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:InitiatingHeapOccupancyPercent=15 -jar "%~dp0..\purpur.jar" --nogui
echo.
echo Sunucu durdu. Cikmak icin bir tusa basin.
pause >nul
endlocal
