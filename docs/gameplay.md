# Gameplay — Kurallar ve Komutlar

## 1. Oyuncu Kuralları

1. Grief, hırsızlık ve izinsiz blok kırma yasaktır.
2. PvP sadece iki tarafın onayı ile yapılır. Spawn ve claim içinde PvP yasaktır.
3. Hile, X-ray resource pack, autoclicker, macro yasaktır.
4. Küfür, hakaret, spam, reklam yasaktır.
5. AFK makine ile sunucuyu zorlamak yasaktır.
6. Boss ve dungeon loot ihtiyaca göre paylaşılır, anlaşmazlıkta admin karar verir.
7. Ölümde eşya iadesi yoktur. Eşyalar 5 dakika içinde alınmalıdır.

## 2. Komut Listesi

Komut ve permission adları değiştirilmeden kullanılır.

Menü ve market (önerilen yol):
- `/menu` — ana menü (Kitler, Market, Nick Rengi, Görevler, Yetenekler, Bilgi)
- `/shop` veya `/market` — market menüsü
- `/satis` — eşya satış menüsü
- `/gecmis` — son 100 log satırı (sadece sana görünür, herkes kullanabilir)

Spawn ve teleport:
- `/spawn` — spawn noktasına gider
- `/sethome [isim]` — en fazla 2 ev
- `/home [isim]` — eve gider (delay 3sn, cooldown 10sn)
- `/delhome [isim]` — ev siler
- `/tpa <oyuncu>` — teleport isteği gönderir
- `/tpaccept` — isteği kabul eder
- `/tpdeny` — isteği reddeder
- `/back` — son ölüm/teleport noktasına döner (cooldown 30sn)

Ekonomi:
- `/money` — bakiye görür
- `/pay <oyuncu> <miktar>` — oyuncuya para gönderir (bounty ödemesi bununla yapılır)
- `/sell hand` — eldeki itemi satar
- `/worth` — eldeki itemin fiyatını gösterir
- `/balancetop` — sunucu zenginlik sıralaması

Meslek ve skill:
- `/skills` — AuraSkills menüsü
- AuraSkills jobs geliri otomatiktir, ayrı `/jobs` komutu yoktur. Jobs Reborn kurulu değildir.

Görev:
- `/quests` — BeautyQuests menüsü

Başlangıç:
- `/kit baslangic` — ilk ekipman (tek seferlik)
- `/kit madenci` — günlük, 200₺ (demir kazma seti)
- `/kit savasci` — günlük, 250₺ (demir kılıç + yay seti)
- `/kit kasif` — günlük, 150₺ (pusula + tekne seti)

Renkli nick (Türkçe komutlar):
- `/nickyesil <isim>` — yeşil nick (örn. `/nickyesil Kral`)
- `/nickkirmizi`, `/nickmavi`, `/nickaltin`, `/nickmor`, `/nicksari`
- Nicki sıfırlamak için `/nick off`

Claim:
- Altın kürekle iki köşeye sağ tık — claim oluşturur
- `/abandonclaim` — claim siler
- `/trust <oyuncu>` — claim içine erişim verir (`/t` kısayolu)
- `/untrust <oyuncu>` — erişimi kaldırır (`/ut` kısayolu)
- `/containertrust <oyuncu>` — sandık erişimi (`/ct` kısayolu)
- `/trustlist` — güven listesi
- `/buyclaimblocks <sayı>` — claim bloğu satın alır
- `/sellclaimblocks <sayı>` — claim bloğu satar

Admin (sadece `admin` grubu): `/setspawn`, `/setwarp`, `/eco`, `/setworth`, LuckPerms komutları.

## 3. Claim Kılavuzu

1. Altın kürek alın.
2. İlk köşeye sağ tık, karşı köşeye sağ tık. Minimum 10x10 önerilir.
3. Claim bloğu kürekle görünür, sohbette alan bilgisi çıkar.
4. Ev ve sandıklar claim içinde olmalıdır. Claim dışı kayıplarda iade yok.
5. Arkadaş eklemek için claim içinde `/trust <isim>` yazın.
6. Ayrılma: `/abandonclaim` tüm claimi siler, önce eşyaları toplayın.

## 4. Ölüm ve Bounty Politikası

- Hardcore yok. Ölümde vanilla kayıp uygulanır, keepInventory kapalıdır.
- Hafif bounty sistemi (otomatik plugin yok):
  - Ödül koymak isteyen oyuncu hedef ismi ve miktarı söyler.
  - Ödeme `/pay` ile elden yapılır.
  - Skor takibi TAB scoreboard + `/balancetop` ile manuel tutulur.
  - Anlaşmazlıkta admin Essentials ekonomi loguna bakar.
