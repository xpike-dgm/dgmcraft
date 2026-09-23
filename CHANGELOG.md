# Changelog — DGM Craft

Format: `Added / Changed / Fixed` başlıkları altında kısa maddeler.

## [0.1.0] — 2026-09-22


İlk kurulum ve kilitli konfigürasyon.

### Added
- Purpur 26.2 build 2633 kurulumu, MC 26.2.
- Portable Java Temurin 25.0.4.1 LTS (`runtime/jdk-25.0.4.1+1`), heap 3G.
- Plugin seti (10 plugin + spark gömülü): LuckPerms 5.5.71, VaultUnlocked 2.20.3, EssentialsX + Spawn 2.22.1-dev+24-49a2f10, AuraSkills 2.4.0, BeautyQuests 2.1.0, EliteMobs 10.9.5, GriefPrevention 16.18.7, PlaceholderAPI 2.12.3, TAB 6.2.0.
- Ekonomi: starting-balance 150₺, max-money 1M₺, minimal worth.yml, AuraSkills jobs ~0.05₺/XP, quest 50-250₺, boss 500-1500₺.
- Gruplar: `oyuncu` (default), `admin` (miras + yönetim). Ev 2, teleport delay 3sn/cooldown 10sn, `/back` 30sn.
- Yedekleme: `scripts/backup.ps1` (7 günlük rotasyon, `backups/dgmcraft_*.zip`), `scripts/restore.bat`, `scripts/stop.bat`.
- Döküman seti: README, AI_MANAGER, architecture, gameplay, progression, economy, bosses, recovery, plugins.lock.

### Changed
- `scripts/start.bat` JVM flagleri standart hale getirildi: `-Dfile.encoding=UTF-8 -Duser.language=en -Duser.country=US`.
- Dünya yapısı 26.2 standardına sabitlendi: tek `world/`, `world_nether` / `world_the_end` yok.

### Fixed
- BeautyQuests tr-TR locale çökmesi çözüldü. Neden: `PlayerListCategory.name().toLowerCase()` içinde sistem locale tr-TR iken `I -> ı` dönüşümü (`tabs.finished` → `tabs.fınıshed`), `getConfigurationSection` null döndü, `loadItem` içinde NPE. Kanıt: decompile + javap satır eşleşmesi + dosya/jar varsayılanı sağlamlık kontrolü. Çözüm: JVM dil flagi ile EN locale zorlama. Flag kaldırılmayacak.

## [0.1.1] — 2026-09-22


Operasyonel sertleştirme.

### Added
- `scripts/tools/mcrcon.exe` (0.7.2, resmi Tiiffi release): RCON ile konsol otomasyonu + güvenli kapatma.
- LuckPerms grupları kuruldu: `oyuncu` (29 izin) + `admin` (miras + 14 yönetim izni), `default` → `oyuncu` parent. Doğrulama: H2 veritabanında binary kanıt.
- PlaceholderAPI eCloud expansionları: Vault 1.8.3, Player 2.0.9, Server 2.7.3, Statistic 2.0.2, GriefPrevention 1.7.0. Toplam 10 hook aktif.
- İlk yedek alındı: `backups/dgmcraft_2026-09-22_00-59.zip` (60.5MB). Restore testi 14/14 geçti.
- `docs/quests.md`: 11 görevlik içerik spesifikasyonu (GUI ile kurulacak).

### Fixed
- PAPI ecloud indirme yarışı: `papi reload` devam eden indirmeleri iptal ediyordu. Sıralı indirme + bekleme ile çözüldü.
- `scripts/start.bat` çalışma klasörü hatası: `cd /d` yoktu, çift tıklayınca sunucu `scripts/` içinde açılmaya çalışıp EULA bulamadan anında kapanıyordu. Düzeltildi + sona `pause` eklendi. `scripts/` içine yanlışlıkla oluşan kopya klasörler temizlendi.
- RCON komut yarışı: art arda komutlarda LuckPerms kuyruğu. Komut aralarına bekleme eklendi.

### Known issues
- EliteMobs 10.9.5 kapanış yarışı: `stop` sonrası nadiren (4 kapanışta 1) `CacheRegenerationLifecycle.cancel` kilidinde takılma (jstack kanıtlı, upstream race). Zarar: yok (önce `save-all flush` çalışır). `stop.bat` 90sn eşiği + taskkill talimatı içerir.

## [0.2.0] — 2026-09-22


Crack uyumluluğu (sahip isteği).

### Changed
- `online-mode: true → false`, `white-list: true → false`, `enforce-secure-profile: true → false`.
- Sonuç: premium hesabı olmayan launcher'lar kendi nickleriyle girebilir.

### Uyarılar (sahibe)
- Offline modda UUID'ler nick'ten türetilir: oyuncu nick değiştirirse parası/envanteri/claim'i SIFIRLANIR. Nickler sabit tutulmalı.
- Whitelist kapalıyken IP'yi bilen herkes HERHANGİ bir isimle (admin ismi dahil) girebilir. Sunucu internete açıksa whitelist'i tekrar açıp crack nickleri eklemek (`whitelist add <nick>`) önemle önerilir.
- Skinler görünmez (Mojang skin sistemi offline'da çalışmaz).

## [0.3.0] — 2026-09-22


Temalı kitler + renkli nick (sahip isteği).

### Added
- 3 günlük ücretli kit: madenci 200₺, savasci 250₺, kasif 150₺ (`kits.yml` + `command-costs`).
- 6 Türkçe nick komutu (`commands.yml` alias): nickyesil/nickkirmizi/nickmavi/nickaltin/nickmor/nicksari. Örn. `/nickyesil Kral`.
- İzinler: essentials.kits.madenci/savasci/kasif + essentials.nick/nick.color (oyuncu grubu, H2'de doğrulandı).

## [0.4.0] — 2026-09-22


Dialog menü + market (sahip isteği).

### Added
- KaMenu 2.0.7: `/menu` dialog hub (Kitler, Market, Nick Rengi, Görevler, Yetenekler, Bilgi) + 3 alt menü. 4/4 menü yüklendi (reload kanıtlı). F+Shift ile de açılır.
- GUIShop 9.4.4: `/shop` + `/satis` market (Bloklar, Yemek, Savas, Aletler). Spawner marketi silindi.
- packetEvents 2.13.0+spigot: GUIShop bağımlılığı (kapanış hatası çözüldü).
- İzinler: guishop.use, guishop.shop.*, guishop.sell (oyuncu grubu, H2'de doğrulandı).

### Changed
- Market fiyatları DGM dengesine çekildi: satışlar worth.yml ile birebir, alışlar ~5x kolaylık vergisi. Elmas/netherite ekipman, totem, büyülü elma, spawner, ender gözü SATILMIYOR.
- GUIShop dahili ekonomisi kapatıldı (EssentialsX kullanılıyor). `/sell` çakışması için satış komutu `satis` yapıldı.
- TAB scoreboard'a Menü/Market satırı eklendi.

### Fixed
- GUIShop PLAYER_BALANCE slotlarında eksik `id` alanı (4 shop, Shop Config Error veriyordu).

## [0.5.0] — 2026-09-22


Tam ekonomi denetimi + 15 kit (sahip isteği).

### Added
- 11 yeni kit: ciftci/balikci/insaatci/okcu/gececi/kiziltasci/dalgici 100-200₺ günlük; nether 400₺ 3 günlük; tamirci 300₺, piknik 150₺, acil 500₺ haftalık.
- İzinler: 11 yeni essentials.kits.* (oyuncu grubu, H2'de doğrulandı).
- KaMenu kit menüsü 15 butona çıktı.

### Changed
- worth.yml'e cobbled_deepslate 0.3 + netherrack 0.25 eklendi (marketle hizalama).
- Denetim: tüm kit içeriklerinde satılabilir-item ≤ kit fiyatı kontrolü yapıldı. Tamirci'deki demir+zümrüt (368₺ kar) çıkarıldı; iksirler Essentials syntax riskiyle kitlerden çıkarıldı.

### Known issues (izleme)
- Bakır 3₺: drowned farmı izlenecek, şişme olursa düşürülecek.

## [0.6.0] — 2026-09-22


Chunky harita ön-üretimi.

### Added
- Chunky 1.5.3 (Bukkit, 26.2 release): `chunky spawn + radius + start` ile harita ön-üretimi. 14/14 plugin, 0 hata.
- Karar kaydı: Jobs Reborn kurulmadı (AuraSkills jobs yeterli), MythicMobs kurulmadı (ücretli, EliteMobs ücretsiz alternatif), Citizens/Towny/anti-cheat kurulmadı (3 oyuncu için gereksiz yük).
## [0.7.0] — 2026-09-22


Chunky + özel /gecmis eklentisi (sahip istekleri).

### Added
- Chunky 1.5.3 (Bukkit, 26.2 release): harita ön-üretimi (`chunky spawn/radius/start`).
- DgmGecmis 1.0.0 (yerinde derlendi, paper-api 26.2): `/gecmis` son 100 log satırını SADECE yazana gösterir.

## [0.7.1] — 2026-09-22


Gamemode denetimi (sahip isteği).

### Changed
- DgmGecmis 1.0.0 → 1.0.1: oyuncu creative/survival (tüm modlar) değiştirdiğinde konsola `[DENETIM] <isim>: survival -> creative` işlenir. `/gecmis` ile geriye dönük görülür. İzin `dgm.gecmis` (varsayılan herkeste, LP kaydı gerekmez). IP adresleri ve gizli kelimeler filtrelenir, Türkçe karakterler korunur.

### Removed
- DiscordSRV 1.30.5 kaldırıldı (sahip Discord istemedi; token yokken her açılışta ERROR veriyordu). İstenirse jar + config yeniden kurulur.

## [0.8.0] — 2026-09-22


16 yeni plugin + Türkçe komutlar + liderlik (sahip isteği).

### Added
- Kolaylık: AxGraves (mezar), Beacon/Monument Waypoints, SmartTrading YOK (Bukkit sürümü yok).
- Harita: iki waypoint sistemi (yukarıda).
- Tasarım: FancyHolograms (tek hologram seçimi), UltraCosmetics, PetCore.
- Performans: PerformanceAnalyzer + LagPeek (ikisi de izleme, müdahale yok).
- Plan 5.8 (istatistik), ajLeaderboards 2.11.0 (5 pano: zengin/avci/süre/güç/ölüm, `/ajlb add` ile kuruldu), PlugManX, SkinsRestorer (forceDefaultPermissions), WorldEdit+WorldGuard, GSit.
- KaMenu `dgm/liderlik` dialogu + `/liderlik` + ana menüde Liderlik butonu.
- 22 Türkçe takma ad (ev, para, ode, sat, kitler, gorevler, tamir...) + `docs/komutlar.md` (tüm komutlar, Türkçe açıklamalı).
- İzinler: 29 yeni node (oyuncu grubu, H2'de doğrulandı). `/repair` ücreti 50₺.

### Removed
- SetHome_GUI kaldırıldı: Essentials /home ile komut çakışması (plugin.yml kanıtlı).
- TradeSystem kurulmadı (doğrulanabilir 26.2 kaynağı yok) + Maintenance plugini gerekmedi (whitelist yöntemi).
- SmartTrading+ kurulmadı (Modrinth'te Bukkit sürümü yok).


## [0.9.0] - 2026-09-22

Tam komut referansi.

### Added
- docs/komutlar-tam.md: 582 komutun tamami, Turkce, Oyuncu/Admin ayrimi.
- 14 sosyal izin acildi (H2 dogrulamali).

## [0.10.0] - 2026-09-22

Skript + Turkce komutlar.

### Added
- Skript 2.16.2 (26.2 release). dgm-turkce.sk: /odul (min 50, Vault fatural�), /cevrimici, /zar, /yazitura. 4 yapi hatasiz yuklendi.
- Plan jeolokasyon kapatildi (EULA istenmeyen ERROR veriyordu).

## [0.11.0] - 2026-09-22

Eksiksiz kilavuz.

### Added
- docs/kilavuz.md: 582 komutun tamami amac+ornek ile (oyuncu + admin, 2 altajanla paralel yazildi).
- 5 ek izin (tpaall/warpinfo/axgraves x2/guishop.value). H2 dogrulamali.

## [0.12.0] - 2026-09-23

Turkce komut paketi (sahip istegi).

### Added
- dgm-turkce2.sk: 57 Turkce komut (/ev /guven /pazar /otur /mezar ...) Skript ile gercek komutlara baglandi. 61 yapi hatasiz.
- Bukkit takma adlari kaldirildi (cakisma onleme); nick renkleri + market orada kaldi.

## [0.13.0] - 2026-09-23

Kalan gunluk komutlarin Turkcesi.

### Added
- dgm-turkce3.sk: 31 komut (/bakiye /zenginler /guvenlistesi /otokabul ...). 92 yapi hatasiz.
- 11 izin (afk/info/ping/helpop/tpauto/tptoggle/trustlist/stats/rank/BellyFlop/LegsUp). H2 dogrulamali.
- kilavuz.md: 30 yeni giris.

## [0.14.0] - 2026-09-23

Plugin kategorilerine gore detayli kilavuz.

### Changed
- `docs/kilavuz.md` alfabetik bolumlerden plugin/sistem kategorilerine tasindi.
- `1-) DGM Craft Turkce Aliaslari (Skript)` bolumunde 90 benzersiz Turkce komutun tamami yer aliyor.
- Plugin bolumlerinde her komut icin amac, kullanim ornegi ve `Orjinal Komutu` alani korunuyor.

## [0.15.0] - 2026-09-23

Tek dil standarti: oyuncuya gorunen tum metinler Turkce.

### Added
- `docs/dil-standardi.md`: terim sozlugu, karakter kurali (komut ASCII / metin tam Turkce), renk kurali.

### Changed
- `plugins/Essentials/motd.txt` Turkce oldu (`/yardim`, `/liste` oncelikli).
- `plugins/TAB/config.yml` baslik/alt bilgi/skor tablosu tam Turkce (`Hoş geldin`, `Çevrimiçi`, `Görev`, `Menü`, `/pazar`).
- `plugins/TAB/messages.yml` oyuncuya giden tum mesajlar Turkce.
- `plugins/KaMenu/menus/dgm/*.yml` menuler tam Turkce; bilgi menusunde komut listesi Turkce-oncelikli.
- `plugins/Skript/scripts/dgm-turkce.sk` sohbet mesajlari tam Turkce.

### Notlar
- Komut adlari ASCII kaldi (Minecraft zorunlulugu): `/odul`, `/cevrimici` vb.
- `server.properties` motd ASCII kaldi (dosya kodlama riski).
- `server-icon.png` (64x64) ve spawn hologramlari elle yapilacak, komutlar `dil-standardi.md` bolum 5'te.

## [0.16.0] - 2026-09-23

Tek dosya baslatma: DgmCraft masaustu uygulamasi (genel yonetici devraldi).

### Added
- `launcher/` uygulamasi: penceresiz konsol, tek tikla Baslat / Guvenli Kapat / Siteyi Ac / Yedek Al.
- Kurulum sihirbazı (4 ekran): ad girisi, sessiz kurulum, arkadas eslestirme, esitleme yuzdesi.
- Gomulu calisma klasoru (goz onunde olmayan konum), surum damgasi ile guncelleme kilidi.
- `host.lock.json` kilidi: ayni anda tek host, kalp atisi 60 sn, olu kilit 10 dk.
- Site yayini (VPN ici) + `/api/log`, `/api/durum`, `/api/oyuncular`, `/api/yetenekler`, `/api/komutlar`, `/api/olaylar`, `/api/cmd` (tehlikeliler onayli).
- Oyuncu ici `/site` komutu (`plugins/Skript/scripts/dgm-site.sk`, launcher gunceller, skript-io gerektirmez).
- `DgmCraft-Baslat.bat`: sunucu + site tek dosyadan.

### Fixed
- `app.py` sihirbaz akisi sadelestirildi (cift mainloop kaldirildi).
- Pencere kapatma: sunucu oldurulmuyor, simge durumuna aliniyor veya guvenli kapatiliyor.
- `store.py` tek veri dizini (LOCALAPPDATA/DgmCraft), `sunucu_kokunu_bul` gomulu klasoru tercih ediyor.
- `dgm-site.sk` dosya okuma kaldirildi (skript-io yoktu, boot hatasi verirdi).

## [0.16.1] - 2026-09-23

Thread/UI kilitlenmesi duzeltmesi (sihirbaz Kur hatasi).

### Fixed
- `ui/wizard.py`: worker thread artik arayuze dogrudan dokunmuyor. Tum `StringVar`/`Progressbar`/`messagebox` guncellemeleri `after(0)` ile ana thread'e yonlendirildi. Entry degerleri thread baslamadan once ana thread'de okunuyor. Kur ve Eslestir dugmeleri is surerken kilitleniyor (cift tiklama Thread-1/2/3 uretmiyor).
- `ui/main.py`: `_yaz` thread-guvenli yapildi, periyodik durum (`_durum_guncelle`), guvenli kapatma ve komut gonderimi (`_komut_thread`) artik widget'a dogrudan dokunmuyor.

## [0.16.2] - 2026-09-23

Uygulama kurulum yapmiyor: rehber + dogrulama modu.

### Changed
- Sihirbaz 2. ekran artik indirme/kurulum yapmiyor. Syncthing ve Tailscale kurulum adimlarini anlatiyor, Kontrol Et ile sadece dogruluyor (kurulu mu, calisiyor mu, bagli mi, Java hazir mi).
- VPN anahtari 1. ekranda saklaniyor, baglanti Ayarlar > VPN Baglan ile yapiliyor.
- UAC ile sessiz kurulum kaldirildi; `zip_indir`/`msi_indir`/`sessiz_kur` artik sihirbazdan cagrilmiyor.

## [0.16.3] - 2026-09-23

Thread/UI kilitlenmesi kokten duzeltme (Kontrol Et basiyor, sonuc gelmiyordu).

### Fixed
- Kok neden: `after()` dahil tum Tcl cagrilari worker thread'den yasak (Python 3.14). `_ui` yardimcisi kuyruk + pompa desenine cevrildi (`ui/wizard.py` ve `ui/main.py`).
- Kontrol Et artik aninda "kontrol ediliyor..." yaziyor, bitince dugme yeniden aciliyor.
- Eslestir on kontrolundeki ag istegi kaldirildi (ana thread donmuyordu); kayitli kimlik yoksa kullanici Kontrol Et adimina yonlendiriliyor.
- `_log_pompa` ayni dongude UI kuyrugunu da tuketiyor.

## [0.16.4] - 2026-09-23

Sihirbaz tekrar acilabilsin.

### Added
- Ayarlar'a "Kurulum Sihirbazını Aç" dugmesi (X ile kapatilabilir, bir sey kaydetmez).
- `kurulumTamam` bayragi sifirlandi; uygulama bir sonraki acilista sihirbazi gosterir.

## [0.16.5] - 2026-09-23

Sihirbaz bos gecilemesin.

### Fixed
- Bitir artik dogruluyor: ad bos ise ve Kontrol Et calismamissa ilgili ekrana donduruyor.
- Arkadas kodlari eksik/hatali ise sonuc acikca yaziliyor ("bu arkadaslarla esitlenmezsin") ve onay isteniyor.
- Eslestir en az 1 kod istiyor.

## [0.17.0] - 2026-09-23

SaaS koyu tema (siteyle ayni dil).

### Added
- `launcher/ui/theme.py`: warm-dark + amber palet, kart/rozet/giris/konsol yardimcilari.
- Ana pencere: logo baslik, renkli durum hapi (kapali/acik/misafir/bakim), konsol karti + Temizle, surum altbilgisi.
- Sihirbaz: temali ekranlar, renkli durum satirlari (yesil/kirmizi/amber), temali Ayarlar.

## [0.18.0] - 2026-09-23

Sihirbaz bastan yazildi: 7 tek-konulu adim, kapili ilerleme.

### Changed
- Sekmeler kaldirildi; ince ilerleme cubugu + "ADIM X/7" + buyuk fontlar.
- Her adim tek konu (hos geldin, ad, anahtar, syncthing, tailscale, arkadaslar, hazir).
- Birincil dugme adima gore degisir (Kontrol Et/Baglan/Eslestir/Devam Et/Bitir); dogrulanmadan sonraki adim acilmaz.
- Kodlar yoksa "atla" secenegi onayli; Bitir savunma amacli tekrar dogrular.

## [0.18.1] - 2026-09-23

Sihirbaz kilitlari sikilastirma.

### Fixed
- "Senin kodun" kutusu readonly modda beyaza donuyordu; koyu temaya kilitlendi (kopyalama calisiyor).
- Anahtar adimi sessiz gecilemiyor: ya anahtar yapistirilir ya da "Anahtarim yok" acikca secilir.
- Atla dugmesi eslestirme bitince gizleniyor; Bitir anahtar beyanini da dogruluyor.

## [0.19.0] - 2026-09-23

AI yardim entegrasyonu (sinirli: teshis soru-cevap).

### Added
- `launcher/core/ai.py`: ucuz modele tek soru-cevap cagrisi (stdlib, `gpt-4o-mini`).
- Komut satirinda "AI Yardim" dugmesi: durum ozeti + son konsol ile sorar, Turkce cevap gosterir.
- Ayarlar > AI anahtari alani: anahtar kilitli dosyada saklanir (`openai.key`), repoya/koda gomulmez.

### Notlar
- AI komut calistirmaz, dosya yazmaz, ayar degistirmez; tavsiye verir, uygulamasi kullanicidadir.
- Anahtar limitli tutulur; sohbete yapistirilan anahtarlar icin rotate onerilir.

## [0.20.0] - 2026-09-23

Zorunlu guncelleme kilidi (sahip yayinlar, arkadas guncellemeden giremez).

### Added
- Ayarlar > Guncelleme Yayinla / Bitir (sahip): surum numarasi + arkadas notu ile kilit acar/kapatir. Yayinlarken sunucu kapali ve kimse host degilse izin verir.
- Guncelleme ekrani: surum, not, dosya gelme yuzdesi; dosyalar tam gelmeden Uygula acilmaz.
- Ana ekranda "Guncelleme (X)" dugmesi; kilitliyken Baslat kapali, ekran otomatik acilir.

## [0.22.0] - 2026-09-23

UI/UX vitrin: kartlar, nabiz, renkli konsol, sihirbaz ikonlari.

### Added
- Ana pencere: Durum/Eşitleme/VPN/Sürüm kartları, atan durum noktası (sunucu açıkken nabız).
- Konsol: hata kırmızı, uyarı amber, giriş yeşil, komut mavi; Otomatik kaydır düğmesi + hazır metni.
- Sihirbaz: her adıma kahraman ikonu, çalışırken animasyonlu bekleme çubuğu.

## [0.22.1] - 2026-09-23

Güncelleme denetimi düzeltmesi.

### Fixed
- Etiket ile sabit sayı hiç eşitlenemiyordu (her zaman "güncelleme var" ya da hiç yok). Uygulanan sürüm kaydediliyor, karşılaştırma ona göre.
- Exe ile çalışanlarda güncelleme yeni klasöre açılıyor (çalışan exe'nin üstüne yazılamazdı).

## [0.22.2] - 2026-09-24

Ayarlar penceresi taşması + exe güncelleyici düzeltmesi.

### Fixed
- Ayarlar artık kaydırmalı (fare tekerleği destekli); alanlar alta kesilmiyor.
- Üst barda "Kapalı" iki kez yazıyordu; rozet nokta göstergesine indi.
- Exe ile çalışanda güncelleyici yanlış klasöre (AppData) yazıyordu; yeni klasöre açılıyor.
- Güncelleme notlarındaki ham "**Full Changelog**" satırı temizleniyor.

### Notlar
- Kilit `version.json` + Syncthing ile yayilir; sahibin Yayınla/Bitir akışını kullanması gerekir (doğrudan dosya değiştirmede kilit devreye girmez).
- Durum makinesi test edildi: yayinlaniyor -> bekliyor -> yok.

## [0.21.0] - 2026-09-23

GitHub dagitimi: repo + webinstaller + launcher guncelleme denetimi.

### Added
- Public repo: `xpike-dgm/dgmcraft` (kod + site + configler; dunya/jar/sirlar haric).
- `webinstaller/Kur.ps1` + `TEK-SATIR.txt`: arkadasa tek satirlik kurulum komutu.
- `.github/workflows/build.yml`: `v*` etiketinde Windows exe derleyip Release'e ekler.
- Ayarlar > GitHub repo + Guncellemeleri Denetle: yeni launcher surumu varsa indirip uygular (sunucu kapaliyken).
- `server.properties.example` + ilk acilista RCON guvencesi (sifre uretilir, mevcut ayarlara dokunulmaz).

### Notlar
- Sırlar repoda YOK: `server.properties`, `*.key`, anahtar dosyalari, dunya, yedekler `.gitignore` ile disarida.
- Jar/config ayrimi: launcher+kod GitHub'dan, dunya/plugin jarlari Syncthing ile gelir.

### Fixed
- Ayarlar VPN dugmesi artik arayuzu dondurmuyor (thread + kuyruk).
