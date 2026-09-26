# DGM Craft — Survival+ Sunucu

Türkçe, 3 oyunculu özel Survival+ sunucusu.
Purpur 26.1.2 üzerine kurulu, düşük bakım yükü ve uzun ömürlü progression hedefler.

## Sistem Özeti

- Çekirdek: Purpur 26.1.2 build 2592 (MC 26.1.2)
- Java: Temurin 25.0.4.1 LTS, portable — `runtime/jdk-25.0.4.1+1`
- Klasör: `C:\Users\Xpike\Desktop\DgmCraftt`
- RAM: 16GB sistem / 3GB heap (`-Xms3G -Xmx3G`)
- Port: 25565 (oyun), RCON: 25575 (yerel kullanım)
- Dünya: Tek klasör `world/` (nether ve end `world/dimensions/` altında)
- Yedek: `backups/dgmcraft_*.zip`, 7 günlük rotasyon

## Kurulum (temiz makineden)

1. Klasörü yerleştirin:
   `C:\Users\Xpike\Desktop\DgmCraftt`

2. Java kontrolü (kurulum gerekmez, portable):
   ```
   runtime\jdk-25.0.4.1+1\bin\java.exe -version
   ```
   Çıktı `25.0.4.1` olmalıdır.

3. Başlatma: `scripts\start.bat` (değiştirmeyin).
   Kritik: `-Duser.language=en -Duser.country=US` zorunludur.
   tr-TR Windows sistemde BeautyQuests `toLowerCase` hatası ile çöker. Bu flagleri kaldırmayın.

4. İlk çalıştırma:
   - `scripts\start.bat` çalıştırın, `server.properties` ve `eula.txt` oluşur.
   - `eula.txt` içinde `eula=true` yapın.
   - `server.properties` değerlerini kontrol edin: `server-port=25565`, `rcon.port=25575`.
   - Tekrar `scripts\start.bat` ile başlatın.

## Günlük Kullanım

Başlatma:
```
scripts\start.bat
```

Durdurma (sırayla deneyin):
```
scripts\stop.bat
```
1. RCON ile güvenli `stop` gönderir (mcrcon varsa).
2. mcrcon yoksa konsola `stop` yazın, 30 saniye bekleyin.
3. Son çare: görev yöneticisinden kapatma (veri kaybı riski).

Yedek alma (manuel):
```
powershell -ExecutionPolicy Bypass -File scripts\backup.ps1
```

Geri yükleme:
```
scripts\restore.bat backups\dgmcraft_YYYY-MM-DD_HH-mm.zip
```
Detay: `docs/recovery.md`

## Plugin Listesi (kısa, toplam 30)

- LuckPerms, VaultUnlocked, EssentialsX + Spawn — komut/ekonomi/izin
- AuraSkills, BeautyQuests, EliteMobs — skill, görev, boss
- GriefPrevention — claim
- PlaceholderAPI, TAB — bilgi ekranı
- KaMenu (`/menu`), GUIShop (`/shop`) — menü + market
- AxGraves, Beacon/Monument Waypoints, GSit — kolaylık + eğlence
- FancyHolograms, UltraCosmetics, PetCore — tasarım
- Plan, ajLeaderboards — istatistik + sıralama
- SkinsRestorer — skinler
- WorldEdit + WorldGuard — admin inşa/koruma
- PerformanceAnalyzer, LagPeek, spark — izleme
- Chunky — harita ön-üretimi
- PlugManX — admin plugin yönetimi
- packetEvents — kütüphane
- DgmGecmis — `/gecmis` + denetim (yerli yapım)

Tam sürüm ve kaynak bilgisi: `plugins.lock.md`
Jobs Reborn yok (AuraSkills jobs kullanılıyor). MythicMobs, Citizens, Towny, anti-cheat yok.

## Ekonomi Özeti

- Başlangıç bakiyesi: 150₺
- `/sell` worth.yml minimal (cobblestone 0.25, demir 8, elmas 50, netherite hurda 200 vb.)
- Jobs geliri: ~0.05₺ / XP
- Quest: 50-250₺, Boss: 500-1500₺
- `max-money: 1000000`
- Gruplar: `oyuncu` (default), `admin` (miras + yönetim)
- Ev: 2, teleport delay 3sn / cooldown 10sn, `/back` cooldown 30sn

Detay: `docs/economy.md`

## Kurallar Özeti (oyuncu)

1. Grief ve hırsızlık yasaktır. Claim dışı alanlarda izinsiz blok kırmayın.
2. PvP sadece karşılıklı rıza ile. Spawn ve claim içinde PvP yok.
3. Hile, macro, autoclicker, X-ray yasaktır.
4. Küfür, hakaret, spam yasaktır.
5. Boss ve dungeon ödülleri ihtiyaca göre paylaşılır.
6. Ölümde eşya iadesi yok. Önemli eşyayı `/sethome` yakınında taşıyın.
7. Hafif bounty sistemi: ödül sadece `/pay` ile elden verilir, hardcore kayıp yok.

Tam liste: `docs/gameplay.md`

## Dökümanlar

- `AI_MANAGER.md` — AI ve bakım kuralları
- `CHANGELOG.md` — değişiklik geçmişi
- `docs/architecture.md` — teknik mimari
- `docs/gameplay.md` — komutlar ve claim kılavuzu
- `docs/progression.md` — 4 aşamalı progression
- `docs/economy.md` — ekonomi dengesi
- `docs/bosses.md` — boss tier listesi
- `docs/recovery.md` — yedekleme ve kurtarma
- `plugins.lock.md` — kilitli sürüm listesi
