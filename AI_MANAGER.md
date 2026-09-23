# AI_MANAGER — DGM Craft Bakım Kuralları

Bu dosya gelecekteki AI asistanlar ve yöneticiler içindir. Önce bunu okumadan işlem yapma.

## 1. YASAKLAR (kesin)

1. Yedeksiz update yok. `plugins/`, `world/`, `*.yml`, `*.json`, `server.properties` dosyalarına dokunmadan önce `scripts/backup.ps1` ile tam yedek al.
2. Silmek yasak: `world/`, `world/players/`, `plugins/Essentials/userdata/`, ekonomi verisi, permission verisi (`plugins/LuckPerms/`).
3. `plugins.lock.md` güncellemeden plugin ekleme / kaldırma / sürüm değiştirme yasak.
4. `CHANGELOG.md` girdisi olmadan config veya plugin değişikliği yasak.
5. Test edilmemiş config yok. Her değişikliği önce konsol hatasız başlatma + ilgili komut testi ile doğrula.
6. Çalışan sistemi modernize etme. Sadece güncel diye Purpur build, Java major sürüm veya plugin major sürüm değiştirme.
7. Türkçe çeviri yasağı: Komut, permission node, placeholder, config key ve teknik adları Türkçeye çevirme.
8. 50 kişilik public varsayımı yasak. Bu sunucu 3 kişilik özel sunucudur. Rate limit, slot, queue, anti-bot önerisi getirme.

## 2. KRİTİK LOCALE BUG — JVM DİL FLAGİ

- Sorun: Windows tr-TR locale sistemde BeautyQuests-2.1.0 `toLowerCase()` çağrısında `I -> ı` dönüşümü yapar, `tabs.finished` anahtarı `tabs.fınıshed` diye aranır, config bulunamaz, plugin fatal error ile disable olur.
- Kanıt: decompile + `javap -l` ile `QuestsMenuConfig.init:714` → `loadItem(catConfig...)` içinde `catConfig=null` doğrulandı. Dosya ve jar varsayılanı sağlamdı.
- Çözüm: `scripts/start.bat` içinde JVM flagleri zorunludur:
  ```
  -Duser.language=en -Duser.country=US
  ```
- KURAL: Bu flagleri KALDIRMA. Java portable yolu `runtime/jdk-25.0.4.1+1` sabittir.
- Oyuncu görünen metinler yine Türkçe kalır (plugin dil dosyaları ayrıca ayarlanır).

## 3. BEAUTYQUESTS NOTU

- Sürüm 2.1.0 release, MC 26.2 uyumlu. 2.2.0+build.156 alpha denendi, aynı NPE (locale) verdi, kaldırıldı.
- Locale flag olmadan çalıştırma. Hata görülürse önce `logs/latest.log` içinde `BeautyQuests` ara.
- Quest dosyalarını elle düzenlersen UTF-8 BOM olmadan kaydet.

## 4. ZORUNLU İŞ AKIŞI

1. `plugins.lock.md` ve `CHANGELOG.md` oku.
2. `scripts/backup.ps1` ile yedek al, zip adını not et.
3. Değişikliği yap (tek seferde tek konu).
4. Sunucuyu başlat, `logs/latest.log` içinde ERROR/WARN tara.
5. İlgili komutu konsoldan test et.
6. `plugins.lock.md` + `CHANGELOG.md` güncelle.
7. `docs/recovery.md` kontrol listesi ile doğrulama yap.

## 5. EKONOMİ VE PERMISSION KORUMA

- `starting-balance`, `max-money`, `worth.yml`, jobs gelir katsayısı gerekçesiz değiştirilemez. Değişiklik istenirse önce `docs/economy.md` gerekçesi yazılır.
- `oyuncu` grubu default parent kalır. `admin` grubu `oyuncu` grubunu miras alır.
- `sethome` 2, teleport delay 3sn/cooldown 10sn, `/back` cooldown 30sn değerleri sabittir.

## 6. DÜNYA YAPISI NOTU

- MC 26.2 Purpur: tek klasör `world/`, nether ve end `world/dimensions/` altında.
- `world_nether/` ve `world_the_end/` yoktur, oluşturma. Yedek scripti `world*` desenini kullanır.

## 7. BİLİNEN OPERASYONEL NOTLAR

- EliteMobs 10.9.5 kapanış yarışı: `stop` sonrası nadiren `CacheRegenerationLifecycle.cancel` kilidinde takılır (jstack kanıtlı). `stop.bat` önce `save-all flush` gönderir, 90sn eşik + taskkill talimatı vardır. EM'yi bu yüzden kaldırma; boss sistemi çalışıyor.
- RCON komutları (özellikle LuckPerms async komutları) art arda gönderilmez; aralara 2-3sn bekleme koy. `papi reload`, ecloud indirmeleri bitmeden çalıştırılmaz.
- `scripts/tools/mcrcon.exe` (0.7.2) konsol otomasyonu içindir, silme.
- RCON şifresi yalnızca `server.properties` içindedir, scriptlere gömme (`stop.bat` sorar).
