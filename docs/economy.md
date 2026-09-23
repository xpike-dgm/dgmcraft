# Economy — DGM Craft

## 1. Gelir Kaynakları

1. `/sell` (Essentials worth.yml, minimal fiyat): madencilik ve fazla blok satışı.
   Market satışı (`/satis`) aynı fiyatlarla çalışır, tek doğruluk kaynağı worth.yml'dir.
2. AuraSkills jobs: skill XP başına ~0.05₺ otomatik ödeme (en fazla 2 aktif job).
3. BeautyQuests: 50-250₺ arası görev ödülü.
4. EliteMobs boss: 500-1500₺ + ekipman drop.
5. Oyuncu ticareti: `/pay` ile serbest (min 1₺).

Başlangıç bakiyesi: 150₺. Maksimum bakiye: 1000000₺ (`max-money`).

## 2. /sell Tablosu (worth.yml minimal)

| Item | Fiyat (₺) | Not |
|---|---|---|
| cobblestone | 0.25 | farm riski izlenir |
| stone / cobbled_deepslate | 0.3 | |
| dirt / sand / gravel / netherrack | 0.1-0.25 | sembolik |
| 6 ana odun (oak/spruce/birch/jungle/acacia/dark_oak) | 1.0 | |
| coal | 2.0 | |
| copper_ingot | 3.0 | izlenir (drowned farm riski) |
| iron_ingot | 8.0 | ana progression |
| gold_ingot | 12.0 | |
| redstone | 4.0 | |
| lapis_lazuli | 5.0 | |
| diamond | 50.0 | geç oyun |
| emerald | 60.0 | |
| netherite_scrap | 200.0 | satmak yerine kullanın |

Blok halleri (demir bloğu, elmas bloğu vb.) ve çiftlik ürünleri (buğday, şeker kamışı, kabak) listede YOK — satış kapalı.

## 3. Lavabolar (para çıkışı)

- `/warp` ücreti 5₺ (`command-costs`). `/home` ve `/spawn` ücretsiz.
- Temalı kitler: günlük 100-250₺, nether 400₺ (3 günlük), haftalık 150-500₺. Tam liste `/menu` > Kitler.
- Market alışları ~5x kolaylık vergili; elmas set, totem, spawner satılmıyor.
- Enchant, örs tamiri, potion malzemesi oyun içinden (villager ticareti serbest).
- Claim bloğu alım/satımı (`/buyclaimblocks`, `/sellclaimblocks`).
- Ölüm cezası dolaylı lavabadır (eşya kaybı).
- Admin shop `buy` tabelası YOK — sonsuz alım enflasyonu engellendi. Sadece `balance/sell/trade/warp/kit/info` tabelaları açık.

## 4. Anti-Exploit Notları

- Otomatik farm + jobs: AuraSkills `check_block_replace` açık ve `disable_unselected_xp=false`; oyuncu koyduğu bloğu kırınca XP yok. Otomatik taş farmı `/sell` ile izlenir, saatlik 500₺ üzeri satış admin kontrolüne girer.
- AFK fishing: tespitinde ürün satışı geri alınır, macro yasaktır.
- `allow-selling-named-items=false`: isimli eşya yanlışlıkla satılamaz.
- Şüpheli durumda `logs/latest.log` ve Essentials `plugins/Essentials/userdata` bakiye geçmişi incelenir.
