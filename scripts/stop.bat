@echo off
REM DGM Craft guvenli durdurma
REM Oncelik: RCON ile stop. mcrcon yoksa manuel talimat.

set RCON_HOST=127.0.0.1
set RCON_PORT=25575
REM RCON sifresi server.properties icindeki rcon.password degeridir.
REM Guvenlik icin buraya yazilmadi, calistirirken sorulur.
set /p RCON_PASS=RCON sifresini girin (server.properties rcon.password):

where mcrcon >nul 2>nul
if %errorlevel%==0 (
  echo Once save-all flush gonderiliyor (veri guvenligi icin)...
  mcrcon -H %RCON_HOST% -P %RCON_PORT% -p "%RCON_PASS%" "save-all flush"
  timeout /t 10 /nobreak >nul
  echo RCON ile stop gonderiliyor...
  mcrcon -H %RCON_HOST% -P %RCON_PORT% -p "%RCON_PASS%" "stop"
  echo Komut gonderildi. Konsolda Stopping the server gorunmeli.
  echo NOT: EliteMobs 10.9.5 kapanista nadiren takilabilir (yukaridaki yaris kosulu).
  echo 90 sn icinde konsol kapanmazsa gorev yoneticisinden java islemini sonlandirin.
  echo Dunya save-all ile yazildigi icin veri kaybi olmaz.
  exit /b 0
)

echo mcrcon bulunamadi. Yontem:
echo 1. Sunucu konsol penceresine gecin.
echo 2. Komut satirina stop yazip Enter basin.
echo 3. 30 saniye bekleyin, pencere kapanmadan gucu kesmeyin.
echo.
echo mcrcon kurmak isterseniz (zorunlu degil, sadece uzaktan guvenli kapatma icin):
echo - Kaynak: https://github.com/Tiiffi/mcrcon
echo - mcrcon.exe dosyasini PATH uzerinde bir klasore koyun, sonra bu scripti tekrar calistirin.
echo.
pause
