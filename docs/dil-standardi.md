# DGM Craft — Dil Standardı

Oyuncunun gördüğü her metin Türkçedir. Aynı kavrama hep aynı kelime kullanılır.

## 1. Karakter kuralı

- Komut adları ASCII'dir (`c,g,i,o,s,u` yok): `/evkur`, `/gorevler`, `/yetenek`, `/pazar`.
  Neden: Minecraft komut adında `ç,ğ,ı,ö,ş,ü` kabul etmez.
- Sohbet, menü, hologram, TAB, MOTD (oyun içi), kurallar: tam Türkçe
  (`ç,ğ,ı,İ,ö,ş,ü` serbest).
- İstisna: `server.properties` içindeki `motd` ASCII kalır (dosya kodlama riski).
  `server-name` ASCII kalır.

## 2. Terim sözlüğü (görünen ad → yasaklı karşılıklar)

| Kullanılacak | Kullanılmayacak |
|---|---|
| para | money, balance, bakiye (görünen metinde) |
| ev | home |
| ev kur | sethome |
| ev sil | delhome |
| doğum noktası | spawn (görünen metinde) |
| istek / kabul / red | tpa, tpaccept, tpdeny (görünen metinde) |
| görev | quest |
| yetenek | skill |
| market / pazar | shop (görünen metinde) |
| satış | sell (görünen metinde) |
| arsa | claim (görünen metinde) |
| güven | trust (görünen metinde) |
| liderlik | leaderboard, top (görünen metinde) |
| skor tablosu | scoreboard (görünen metinde) |
| çevrimiçi | online, cevrimici |
| yardım | help (görünen metinde) |
| kurallar | rules (görünen metinde) |

Not: Komut rehberlerinde (`kilavuz.md`) orijinal İngilizce komut her kaydın
`Orjinal Komutu` satırında yazmaya devam eder. Yasak olan, oyuncuya gösterilen
menü/mesaj metninde İngilizce terim kullanmaktır.

## 3. Renk ve prefix

- Bilgi: `&7`, vurgu: `&6`/`&e`, para: `&a` (sayı `&f` de olabilir, mevcut menülerle tutarlı kal).
- Hata: `&c`, başarı: `&a`.
- Başlıklar: `&6&lDGM CRAFT` (TAB + KaMenu ana menüde aynı).

## 4. Uygulanan yerler

- `plugins/Essentials/motd.txt`: Türkçe giriş mesajı.
- `plugins/TAB/config.yml`: başlık, alt bilgi, skor tablosu Türkçe.
- `plugins/TAB/messages.yml`: oyuncuya giden mesajlar Türkçe.
- `plugins/KaMenu/menus/dgm/*.yml`: menü metinleri tam Türkçe, komut listeleri Türkçe-öncelikli.
- `plugins/Skript/scripts/dgm-turkce.sk`: sohbet mesajları tam Türkçe.
- `plugins/Essentials/config.yml`: `locale: tr`, `per-player-locale: false` (değişmedi, standart).
- `plugins/BeautyQuests/config.yml`: `lang: tr_TR` (değişmedi, standart).

## 5. Elle yapılacaklar (dosya ile olmaz)

- `server-icon.png`: 64x64 PNG, sunucu kök dizinine konur. Logo metni: `DGM CRAFT`.
- Spawn hologramları (oyunda, op ile):
  - `/hologram create spawn-bilgi`
  - Satırlar: `&6&lDGM CRAFT`, `&7Hoş geldin!`, `&e/menu &7ile başla`,
    `&e/gorevler &7görevler`, `&e/pazar &7market`
