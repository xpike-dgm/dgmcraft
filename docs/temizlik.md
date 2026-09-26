# Klasör Düzeni — DGM Craft

Sunucu kökü 19 klasör + 30 dosya. Bunların hepsi "kirlilik" değil; her birinin
bir görevi var. Bu belge neyin ne olduğunu ve neden durduğunu açıklar.

## Çalıştırmak için gerekli (dokunma)

| Klasör | Boyut | Görev |
|---|---|---|
| `plugins/` | 190 MB | 31 eklenti + tüm verileri (para, XP, görev, izin, claim). **Sunucunun kalbi.** |
| `libraries/` | 156 MB | Sunucunun indirdiği Java kütüphaneleri. Silinir, yeniden indirilir. |
| `versions/` | 58 MB | Paperclip'in çıkardığı sunucu jar'ı. Silinir, yeniden oluşur. |
| `cache/` | 121 MB | Paperclip'in indirdiği Minecraft sunucu dosyaları. Silinir, yeniden indirilir. |
| `runtime/` | 303 MB | Portable Java 25. Launcher sunucuyu bu JDK ile başlatır. |
| `world/` | 6,6 MB | **Aktif dünya.** Silinmez. |
| `config/` | 13 KB | Paper config klasörü. |
| `logs/` | 108 KB | Sunucu logları. Son 5 döndürülmüş log tutulur. |
| `webinstaller/` | 3 KB | Tek tuşla kurulum yardımcısı. |

## Belge ve kaynak

| Klasör | Boyut | Görev |
|---|---|---|
| `launcher/` | 6,5 MB | PySide6 arayüzünün kaynak kodu (8 sayfa + sihirbaz). |
| `docs/` | 128 KB | Mimari, ekonomi, kılavuz, kurtarma, eklenti listesi. |
| `scripts/` | 5 MB | Yedekleme ve görev üretimi scriptleri. |
| `arsiv/` | 715 KB | Sıkıştırılmış kaynak arşivleri. `gorev-projesi-750.zip` = 750 görevin kaynak kopyası. |
| `.git/` | 62 MB | Sürüm geçmişi. |
| `.github/` | 1 KB | CI tanımı. |
| `.paper/` | 68 bayt | Paper ayarı. |

## Geri dönüş varlıkları (sıfırdan yapılana kadar sakla)

| Yol | Ne |
|---|---|
| `purpur-26.2-2633.jar` | 26.2 build 2633 sunucusu (67 MB). `purpur.jar` 26.1.2 build 2592. |
| `geri-donus/worldguard-bukkit-7.0.19.jar` | WorldGuard 7.0.19 (26.2'de çalışan sürüm). |
| `world-26.2-yedek/` | 26.2 dünyası, 17 MB. 26.1.2 açamıyordu. |
| `backups/*.zip` | Tam yedekler. Artık 5 eski + 2 bugünkü tutulur. |

## Silinenler ve neden

### `site/` (55 MB) → git geçmişinde
Kullanıcı site'yi kullanmıyor. İçindeki commit edilmemiş değişiklikler ve 94 marka
görseli `2e2b61e` commit'iyle saklandı. Geri almak için:

```powershell
git checkout 2e2b61e -- site/
```

Launcher hâlâ site sunucusunu açabilir; klasör yoksa **bekleme sayfası** servis eder
(`launcher/core/site.py` → `bekleme_sayfasi()`). Yani silmek arayüzü bozmaz.

### `cikti/` (756 dosya) → `arsiv/gorev-projesi-750.zip`
750 görev + tasarım dokümanı + manifest + kurulum rehberi. Arşivlenmeden önce
`plugins/BeautyQuests/quests/` ile 750/750 birebir aynı olduğu doğrulandı.
Çalışan görevler `plugins/BeautyQuests/quests/` içinde, kaynak arşivde.

### Eski yedekler (11 adet, 1,73 GB)
26.1.2'ye geçişten önceki yedekler. Geriye 26.1.2 sonrası 2 yedek kaldı:
`dgmcraft_2026-09-26_18-02.zip` (temizlik öncesi) ve `dgmcraft_2026-09-26_18-15.zip` (temizlik sonrası).

### `embedded/`, `site-link.txt`, `permissions.yml`
Boş dosya/klasörler. `site-link.txt` artık otomatik oluşmuyor (`site.py` koşullu yazıyor).

## Yeni yedek alırken

```powershell
powershell -ExecutionPolicy Bypass -File scripts\backup.ps1
```

Rotasyon sayı sınırlıdır: **5 eski + 2 bugünkü**. Fazlası anında silinir, disk şişmez.

## Disk nerede gitti

| Durum | Serbest |
|---|---|
| Temizlik öncesi | 13,2 GB |
| Temizlik sonrası | ~15,1 GB |
