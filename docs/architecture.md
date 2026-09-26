# Architecture — DGM Craft

## 1. Çekirdek

- Purpur **26.1.2 build 2592** (MC 26.1.2) — 2026-09-26'da düşürüldü, 31 eklenti + 750 görev ile doğrulandı
- Önceki sürüm: Purpur 26.2 build 2633 → geri dönüş için `purpur-26.2-2633.jar` olarak kökte saklanıyor
- WorldGuard: 7.0.19 (`api-version: 26.2`, 26.1'de yüklenmiyor) → **7.0.18**; yedek jar `geri-donus/worldguard-bukkit-7.0.19.jar`
- Jar: `purpur.jar`
- Çalışma modu: `--nogui`
- EULA: `eula.txt`

Purpur tercihi teknik gerekçesi: Paper tabanlı drop-in replacement, ek `purpur.yml` configurability içerir, vanilla mekanikleri korur. 2026-09-26'da kullanıcı kararıyla 26.2 → **26.1.2** hattına düşürüldü: BeautyQuests 2.1.0 ve 750 görev bu hatta doğrulandı, tüm eklentiler 0 hata ile yüklendi. Geri dönüş jar'ları kökte (`purpur-26.2-2633.jar`, `geri-donus/`) tutulur.

## 2. Klasör Yapısı

```
C:\Users\Xpike\Desktop\DgmCraftt\
  scripts\start.bat | stop.bat | backup.ps1 | restore.bat
  purpur.jar
  server.properties
  eula.txt
  bukkit.yml | spigot.yml | commands.yml
  config\paper-global.yml (+ paper-world-defaults)
  purpur.yml
  whitelist.json | ops.json | usercache.json | banned-*.json
  runtime\jdk-25.0.4.1+1\bin\java.exe   (portable, sisteme kurulmaz)
  world\                                 (tek dünya: overworld + dimensions)
    level.dat | players\ | dimensions\
  plugins\                               (10 jar + veri klasörleri)
  backups\dgmcraft_*.zip                 (7 günlük rotasyon)
  logs\ | docs\ | cache\ | libraries\
```

Not: `world_nether/` ve `world_the_end/` yoktur (26.1+ yeni dünya düzeni). Yedek ve restore işlemleri `world*` desenini kullanır.

## 3. Java

- Dağıtım: Eclipse Temurin 25.0.4.1 LTS, portable
- Yol: `runtime/jdk-25.0.4.1+1` (sistem Java'sı kullanılmaz, PATH değişikliği yok)
- Heap: `-Xms3G -Xmx3G` (16GB sistemde sabit 3GB, 3 oyuncu + 10 plugin için yeterli)
- GC: G1GC, `MaxGCPauseMillis=200` (agresif Aikar listesi kullanılmadı)
- Zorunlu flagler: `-Dfile.encoding=UTF-8 -Duser.language=en -Duser.country=US`
  (Türkçe Windows'ta BeautyQuests locale bug için — detayı AI_MANAGER.md §2)

## 4. RAM ve Performans

- Heap 3GB sabittir. 3 oyuncu için artırma gerekmez.
- `view-distance=10`, `simulation-distance=10` (vanilla varsayılan, ellemeyin).
- Mob AI, redstone, hopper, villager, farm kısıtlaması YOK.
- spark gömülüdür (`spark tps`, `spark health`, `spark profiler --timeout 120`).

## 5. Portlar ve RCON

- Oyun portu: 25565 (`server.properties: server-port`)
- RCON: 25575, `enable-rcon=true`, şifre `server.properties` içinde (`rcon.password`, repoya yazılmaz)
- `scripts/stop.bat` RCON üzerinden `stop` gönderir (mcrcon varsa, yoksa manuel)
- `online-mode=false` (crack uyumluluğu, sahip kararı), `white-list=false`
