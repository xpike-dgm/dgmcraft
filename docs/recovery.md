# Recovery — Yedekleme ve Kurtarma

## 1. Yedekleme

Komut (sunucu çalışırken önce konsolda `save-all flush` yazın):
```
powershell -ExecutionPolicy Bypass -File scripts\backup.ps1
```

İçerik: `world*` (26.1.2 tek klasör + dimensions), `plugins/` (config + SQLite/H2 veritabanları), `config/`, kökteki `*.json + *.yml + server.properties`.
Hedef: `backups/dgmcraft_YYYY-MM-DD_HH-mm.zip`
Rotasyon: 7 günden eski `dgmcraft_*.zip` dosyaları silinir.

Öneri: her oyun günü sonunda ve update öncesi yedek alın. Plugin/Minecraft güncellemesi öncesi snapshot zorunludur.

## 2. Restore Adımları

1. Sunucuyu durdurun (`scripts\stop.bat` veya konsola `stop`). Konsol kapanmadan devam etmeyin.
2. Mevcut durumu koruyun:
   ```
   powershell -ExecutionPolicy Bypass -File scripts\backup.ps1
   ```
3. Geri yükleyin:
   ```
   scripts\restore.bat backups\dgmcraft_YYYY-MM-DD_HH-mm.zip
   ```
4. `scripts\start.bat` ile başlatın ve aşağıdaki listeyi uygulayın.

## 3. Test Restore Prosedürü (ayda bir)

1. `backups/` içinden son zip seçin.
2. Geçici klasöre açın (`C:\Temp\dgm-restore-test\`).
3. İçinde `world/level.dat` ve `plugins/Essentials/` olduğunu doğrulayın.
4. Zip boyutu önceki yedekle +-20% içinde olmalıdır, ani küçülme bozulma işaretidir.
5. Sonucu CHANGELOG'a işleyin.

## 4. Doğrulama Kontrol Listesi

Başlatma sonrası:
- [ ] Konsolda ERROR/SEVERE yok, `Done` görünür.
- [ ] `plugins` komutunda 10 plugin enabled (kırmızı yok).
- [ ] Oyuna giriş yapılır, `/spawn` çalışır.
- [ ] `/home`, `/money`, `/quests`, `/skills` her biri 1 kez denenir.
- [ ] `world/players/` tarihi günceldir.
- [ ] RCON port 25575 dinlemede.
