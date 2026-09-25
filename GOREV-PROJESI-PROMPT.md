# DGM CRAFT — 750 Görevlik Hikâye Projesi: AI Üretim Prompt'u

> Bu dosyanın **tamamı** bir AI asistan'a verilecek prompttur. Aşağıdan son satıra kadar
> tek parça olarak kopyalanıp yapıştırılmalıdır. Kod blokları içindeki YAML/şema
> referansları da prompt'un parçasıdır, kopyalamada dahil edilmelidir.

---

# GÖREV: DGM CRAFT SUNUCUSU İÇİN 750 GÖREVLİK HİKÂYE PROJESİ

## 0. ROLÜN VE TESLİMATIN

Sen profesyonel bir **Minecraft Survival+ oyun tasarımcısı, hikâye yazarı ve sistem mimarısısın**.
Aynı zamanda çıktının teknik olarak **çalışır** olduğundan sorumlusun. Elinizdeki veri
gerçek bir, çalışan bir sunucunun doğrulanmış verisidir; hayal varsayımla değil, bu veriyle
çalışacaksın.

**Tek teslimatın iki parçası olacak:**

1. **TASARIM DOKÜMANI** — hikâye, bölüm haritası, görev ağacı, ekonomi denge tablosu,
   karakter/motivasyon notları, kurulum ve doğrulama kılavuzu.
2. **HAZIR YAML** — BeautyQuests 2.1.0 formatında, doğrudan sunucuya yüklenebilecek,
   elle düzeltme gerektirmeyen 750 görev dosyası + manifest.

Bu iki parçayı **ayrı ayrı ve eksiksiz** üreteceksin. Önce tasarım, sonra YAML.

---

## 1. SUNUCU BAĞLAMI (DOĞRULANMIŞ GERÇEK VERİ — DEĞİŞTİRME, TARTIŞMA)

### 1.1 Sunucu kimliği
- Sunucu adı: **DGM CRAFT**
- Tür: **Survival+**, 3 kişilik **özel arkadaş sunucusu** (kalabalık sunucu değil).
- Oyuncu sayısı: **tam olarak 3 kişi** (kurucu + 2 arkadaş). Sunucu 3 kişilik tasarlandı;
  "50 kişilik public" varsayımı yasaktır. Rate limit, slot, queue, anti-bot, ölçekleme
  önerisi getirme.
- Oyun dili: **Türkçe**. Oyuncuya görünen her metin Türkçedir.
- Barınak: arkadaşlar arasında özel ağ (Tailscale), sunucu dışarıya kapalı.

### 1.2 Teknik taban
- Minecraft **26.2**, sunucu **Purpur 26.2 build 2633** (vanilla Paper türevi).
- Java: **Temurin 25** (portable, `runtime/jdk-25.0.4.1+1`).
- Dünya: **tek dünya klasörü** `world/`; Nether `world/dimensions/minecraft/the_nether`,
  End `.../the_end`. Ayrı `world_nether/` klasörü **yoktur ve oluşturulmayacaktır**.
- Dünya tipi: **tamamen vanilla**, `level-seed` boş (rastgele), `generate-structures: true`.
  **Özel biome yok. Özel köy, özel tapınak, özel dungeon, custom arena, schematic YOK.**
- Yapılar **prosedürel vanilla**: köyler, mineshaft'ler, stronghold'lar, ocean monument'ları,
  Nether fortress'ları, bastion'lar, ancient city'ler, end city'ler, ruined portal'lar.
- Spawn: `0, 71, 0` (overworld). Dünya sınırı oyuncunun ulaşabileceği kadar geniş
  (~7.3 milyon blok kenar); sınır kısıtı **pratik değildir**.
- Zorluk: **normal**. `hardcore: false`, `keepInventory: false` → **ölümde eşya gider,
  iade yok.** Görev tasarımı buna göre yapılacak (aşağıda kuralları var).
- Anti-hile: `allow-nether: true`, uyku %100, `spawn-monsters: true`.
- **Dünya henüz oynanmış bir dünya değil; sadece spawn çevresi.** Yani dünyada "keşfedilmiş
  bir şey" olarak anlatabileceğin hazır bir lore **yok**. Hikâyeyi dünyaya **oyuncuların
  kazacağı, dikeceği, kazacağı taşla** yazacaksın.

### 1.3 Kurulu eklentiler (TAM LİSTE — sadece bunlar var)
```
AuraSkills 2.4.0        BeautyQuests 2.1.0       EliteMobs 10.9.5
EssentialsX 2.22.1       EssentialsXSpawn         LuckPerms 5.5.71
VaultUnlocked 2.20.3     PlaceholderAPI 2.12.3     TAB 6.2.0
GriefPrevention 16.18.7  GUIShop 9.4.4             KaMenu 2.0.7
Skript 2.16.2             WorldEdit 7.4.5          WorldGuard 7.0.19
AxGraves 1.32.0           Chunky 1.5.3             FancyHolograms 2.12.0
FancyAnalytics            faststats                GSit 3.7.0
UltraCosmetics 3.16       SkinsRestorer 15.12.6    Plan 5.8
PerformanceAnalyzer       PlugManX 3.2.1            PetCore 1.0.0
BeaconWaypoints 1.1.0     MonumentWaypoints 1.0.0  ajLeaderboards 2.11.0
bStats                    spark (Purpur gömülü)      DgmGecmis 1.0.1 (özel)
```

### 1.4 **KURULU OLMAYANLAR** (tasarımda kullanma — en kritik kısım)
Şu eklentiler **yok**: Citizens, FancyNpcs, ZNPCsPlus, MythicMobs, MythicMobs5, BetonQuest,
Quests, Towny, Slimefun, Factions, mcMMO, Jobs Reborn, Level, Denizen, ArcaneMobs,
DungeonsXL, MMOItems, ItemsAdder, Oraxen, ModelEngine, Trailers, DecentHolograms,
DankMemer, ShopGUI+, BeautyQuests'ın **harici** NPC eklentileri.

Sonuçlar:
- **Görev veren NPC kullanma.** Görevler menüden/otomatik açılmalı. (BeautyQuests'ın
  *dahili* NPC sistemi var ama sen buna bağımlı tasarım yapma; ileride NPC eklenirse
  tasarımın bozulmaması için görevlerin NPC'siz de tamamlanabilir olması şart.)
- **MythicMobs/Boss tipi özel mob takibi yapma.** EliteMobs boss'ları vanilla entity
  tipleriyle özel isimle doğar; `MOBS` aşamasında `entityType` + `name` eşleşmesiyle
  *denenebilir*, ama bunu **"DOĞRULA"** olarak işaretle ve test planına yaz.
- **Dünya günüğü, haftalık, tekrarlayan görev, havuz (pool) kullanma.** Kesinlikle yok.
- Özel yetenek/plugin komutu gerektiren hiçbir mekanik kurma.

### 1.5 AuraSkills (11 yetenek, her biri max 100)
| Skill | Türkçe ad (AuraSkills tr paketi) | Not |
|---|---|---|
| `auraskills/farming` | Çiftçilik | yetenek: bountiful_harvest, farmer, scythe_master, geneticist, growth_aura |
| `auraskills/foraging` | Toplayıcılık | lumberjack, forager, axe_master, valor, shredder |
| `auraskills/mining` | Madencilik | lucky_miner, miner, pick_master, stamina, hardened_armor |
| `auraskills/fishing` | Balıkçılık | lucky_catch, fisher, treasure_hunter, grappler, epic_catch |
| `auraskills/excavation` | Ekskavatör | bigger_scoop, excavator, spade_master, metal_detector, lucky_spades |
| `auraskills/archery` | Okçuluk | retrieval, archer, bow_master, piercing, stun |
| `auraskills/defense` | Savunma | shielding, defender, mob_master, immunity, no_debuff |
| `auraskills/fighting` | Savaş | parry, fighter, sword_master, first_strike, bleed |
| `auraskills/agility` | Çeviklik | light_fall, jumper, golden_heal, fleeting, meal_steal |
| `auraskills/alchemy` | Simya | alchemist, brewer, life_steal, golden_heart, wise_effect |
| `auraskills/enchanting` | Büyüleyici | xp_convert, enchanter, anvil_master, enchanted_strength, lucky_table |

- Her oyuncu **en fazla 2 job** seçebilir (`default_job_limit: 2`), değiştirme cooldown 300 sn.
- Seviye XP eğrisi: `XP(n) = 100 × (n-2)² + 100`. Örnek: seviye 10 = 6.500 XP,
  seviye 20 = 32.500 XP, seviye 40 = 144.500 XP, seviye 50 = 241.000 XP, seviye 100 = 960.500 XP.
- Yetenekler skill 1'de 1, skill 6'da 5, skill 11'de 10, skill 16'da 15 adet açılır.
- Ölümde skill/XP **silinmez**. Yaratıcı modda XP kazanılmaz.
- XP kaynakları örnek: taş 0.2, kömür 1.0, demir 1.8, lapis 30.6, elmas 47.3, zümrüt 100.0;
  buğday 3.0; çipura balığı 25; oyuncu 50. Genel XP kuralı: oyuncu/mob öldürme 50,
  sıradan mob 1.0.
- **Görev ödülü olarak AuraSkills XP veremezsin** (bunun için özel mekanik yok).
  XP kazandıran şey oyuncunun fiilî eylemidir. Görevler oyuncuyu **eyleme** itmeli,
  böylece XP doğal olarak kazanılsın. Tasarımın temel felsefesi budur.

### 1.6 Ekonomi (SABİT — değiştirme, sadece öneri+gerekçe sun)
- Para birimi: **₺** (TL benzeri). Başlangıç bakiyesi **150₺**. Maksimum **1.000.000₺**.
- **Jobs geliri: 0.05₺ / XP** (otomatik, en fazla 2 job).
- `/sell` fiyatları (`worth.yml`, tek doğruluk kaynağı, artırmak yasak):
  cobblestone 0.25 · stone/cobbled_deepslate 0.3 · dirt 0.1 · sand/gravel 0.2 ·
  netherrack 0.25 · 6 ana odun 1.0 · coal 2.0 · copper_ingot 3.0 · redstone 4.0 ·
  lapis_lazuli 5.0 · iron_ingot 8.0 · gold_ingot 12.0 · diamond 50 · emerald 60 ·
  netherite_scrap 200 · rotten_flesh/string 0.1
- **Satış listesi dışında hiçbir eşya satılamaz**: blok halleri, çiftlik ürünleri, mob drop'ları.
- Market (GUIShop) alışları ~5× kolaylık. Örnek: OBSIDIAN 200₺, CRYING_OBSIDIAN 300₺,
  GOLDEN_APPLE 600₺, END_CRYSTAL 400₺, SPONGE 500₺, ENDER_PEARL 120₺, TNT 150₺.
- **Totem yok, spawner yok, elytra satışı yok, ender gözü (ender eye) yok.**
- Kit ücretleri: başlangıç 0₺ (tek sefer) · balıkçı 100 · gececi 100 · kasif 150 ·
  çiftçi 150 · inşaatçı 150 · madenci 200 · savaşçı 250 · okçu 200 · kızıltasçı 200 ·
  dalğıç 200 · nether 400 (3 günlük) · piknik 150 (haftalık) · tamirci 300 (haftalık) ·
  acil 500 (haftalık). `/warp` 5₺, `/tamir` 50₺, `/home` ve `/spawn` ücretsiz.
- Claim (arsa) sistemi: GriefPrevention, oyuncu başına 1000 blok + saatte 200 blok,
  tavan 80.000. Alım/satım **bedava**. PvP: **sadece iki tarafın onayı ile**, doğum noktası
  ve arsa içinde yasak.
- Ölüm cezası dolaylı ve **en büyük para lavabosudur** (eşya gider, iade yok).

### 1.7 EliteMobs boss'ları (hikâyenin 5 dayanağı — HEPSİ SPOT NOKTASIZ)
| Tier | Ad | Entity | Sv | Can× | Hasar× | Ekipman |
|---|---|---|---|---|---|---|
| I | **Orman Bekçisi** | ZOMBIE | 12 | 2.5 | 0.8 | demir |
| II | **Kor Ata** | WITHER_SKELETON | 20 | 3.0 | 1.0 | altın |
| III | **Derin Kahin** (+ 2. faz iskelet) | DROWNED | 28 | 4.0 | 1.1 | turkuaz/zincir |
| IV | **Boşluk Ejderi** | ENDERMAN | 35 | 5.0 | 1.2 | netherit |
| V | **Üç Kardeş** | WITHER_SKELETON | 32 | 5.0 | 1.2 | netherit + kalkan |

Güçler: ground_pound, attack_push, flame_pyre, attack_fire, frost_cone, attack_gravity,
skeleton_pillar, attack_lightning, plasma_blaster, attack_vacuum, spirit_walk, thunderstorm,
bullet_hell. Derin Kahin %50 canda 2. faza geçer.
**Ölümde ödül düşmez (kitap ödülü de yok). Ödül tamamen senin görevlerinden verilecek.**
Boss ödül bantı hedefi: **500–1500₺** + ekipman.

### 1.8 Görev sistemi: BeautyQuests 2.1.0 (TAM ŞEMA — BUNUN DIŞINA ÇIKMA)

**KRİTİK UYARI:** Bu eklentinin eski sürümlerindeki `objectives:` / `rewards:` kök
blokları **artık geçerli değil**. 2.1.0'da görev şeması şöyledir:

```yaml
# kök seviye option anahtarları (yalnız varsayılandan farklıysa yazılır)
name: 'Görev Adı'
description: 'Açıklama'
customItem: {material: BOOK, amount: 1}     # eski adı: customMaterial
cancellable: false
failOnDeath: false
repeatable: false                          # BU SUNUCUDA HER ZAMAN false
timer: 0                                   # süre yok
hideNoRequirements: false
scoreboard: true
customOrder: 10
pool: yok                                  # HAVUZ KULLANILMAZ
auto: false                                # ilk girişte otomatik değil
startMessage: '...'
startDialog: {lines_amount: 4, lines: ['satır1','satır2','satır3','satır4']}
endMsg: '...'
firework: [FIREWORK_ROCKET]
requirements: []                           # görevi BAŞLATMA koşulları
startRewards: []                           # eski adı: startRewardsList
endRewards: []                             # eski adı: rewardsList  (KÖKTE 'rewards' DEĞİL)
manager:
  branches:
    '0':                       # 0 = ana hat (branch index integer OLMAK ZORUNDA)
      stages:
        '0':                   # aşama index'i integer OLMAK ZORUNDA
          stageType: MOBS      # ZORUNLU
          text: 'aşama başlangıç mesajı'
          customText: 'aşamaya özel tek cümle ipucu'
          options:
            progressbar: true
          requirements: []      # aşamayı TAMAMLAMAK için gerekenler
          rewards: []           # aşama bitince
          objects: {}           # MOBS / MINE / PLACE_BLOCKS için
      endingStages: {}          # branchLinked gerekiyorsa
id: 12345
```

**YASAK ANAHTARLAR (2.1.0'da yok, yazarsan görev bozulur):** `objectives:` (kökte),
`rewards:` (kökte), `rewardsList` (eski ad), `customMaterial` (yeni: `customItem`),
`starterID`/`starterNPC` (NPC yok), `multiple` (eski ad), `objective` (yanlış yazım).

#### Aşama tipleri (21 adet — hepsi kullanılabilir)
| stageType | Ne yapar | Özel anahtarlar |
|---|---|---|
| `MOBS` | mob öldürme | `objects:` → `{amount, object:{id, entityType, any, minLevel, factoryName, name, value, customDescription}}`, `shoot`, `preventNpcsForVanilla` |
| `MINE` | blok kırma | `objects:` → `object:{id, blocks:{...}}`, `placeCancelled` |
| `PLACE_BLOCKS` | blok yerleştirme | `objects:` → blok listesi |
| `ITEMS` | **2.1.0 yeni** — envanterde eşya kontrolü | `items` + `itemComparisons` |
| `LOCATION` | koordinata varma | `location: {world, x, y, z, yaw, pitch}` + `radius` (blok) |
| `INTERACT_LOCATION` | koordinatla etkileşim | `location`, `leftClick` |
| `INTERACT_BLOCK` | belirli bloğa sağ/sol tık | `block: {material, location}`, `leftClick`, `material` |
| `CHAT` | sohbet mesajı yazma | `text`, `ignoreCase`, `isRegex`, `cancel`, `placeholders` |
| `DEAL_DAMAGE` | toplam hasar verme | `damage` (int), `targetMobs` |
| `PLAY_TIME` | oynama süresi | `playTicks` + `timeMode: ONLINE\|OFFLINE\|REALTIME` |
| `DEATH` | ölmek | `causes` |
| `EAT_DRINK` | yeme/içme | — |
| `FISH` | balık tutma | — |
| `MELT` | eritme (ocak) | — |
| `ENCHANT` | büyü atma | — |
| `CRAFT` | üretim | `result`, `itemComparisons` |
| `BUCKET` | kovadan su/lava koyma | `bucket`, `amount` |
| `BREED` | hayvan üretme | `entityType`, `any`, `amount` |
| `TAME` | evcilleştirme | `entityType`, `any`, `amount` |
| `NPC` | NPC etkileşimi | **KULLANMA** (NPC yok) |

`BRING_BACK` sınıfı jar'da var ama **kayıtlı değil** — kullanma.

#### Ödül tipleri (hepsi geçerli)
| id | Anahtarlar |
|---|---|
| `moneyReward` | `money` (double) — Vault üzerinden, **temiz yol** |
| `itemReward` | `items` (maplist), `items_amount` |
| `commandReward` | `commands` (maplist: `label`, `console`, `parse`, `delay` tick) |
| `expReward` | `xp_amount` (vanilla XP) |
| `titleReward` | `title` |
| `textReward` | `message` / `text` |
| `tpReward` | `tp` (BQLocation) |
| `firework` (kök option) | `firework: [FIREWORK_ROCKET]` |
| `wait` | `delay`, `ticks` |
| `randomReward` | `min`, `max`, `rewards`, `rewards_amount` |
| `requirementDependentReward` | `requirements` + `rewards` |
| `removeItemsReward` | `items`, `items_amount`, `comparisons` |
| `checkpointReward` | `actions`, `actions_amount` |
| `questStopReward` | — |

**Para ödülü iki yoldan verilebilir:** (a) `moneyReward` + `money: 50` → **tercih edilen**,
(b) `commandReward` + `label: 'eco give {player} 50'`. (b)'yi kullanırsan **`{player}`
placeholder'ı aynen kalacak şekilde** yaz, çevirme/sabitleme yok.

#### Gereksinim tipleri (görev→görev zinciri)
| id | Anahtarlar | Not |
|---|---|---|
| `questRequired` | `questID` (int) | **ANA GEÇİŞ MEKANİZMASI.** Eski `requirements: - GörevAdı` formatı GEÇERSİZ. |
| `levelRequired` | `level` | vanilla seviye |
| `moneyRequirement` | `money` | Vault; oyuncunun parası şart |
| `placeholderRequirement` | `placeholder`, `comparison` (`<`,`>`,`=`,`>=`,`<=`), `value`, `default`, `number`, `parse_value` | **AuraSkills seviyesi şartı için** |
| `equipmentRequired` | `slot`, `item`, `comparisons` | elmas set vb. |
| `permissionRequired` | `permissions`, `permissions_amount`, `message` | dikkatli kullan |
| `scoreboardRequired` | `objective`, `score` | skor tablosu |
| `logicalOr` | alt requirement listesi | alternatif yol açmak için |
| `regionRequired` | `region`, `region_world` | **KULLANMA — WorldGuard'da hiç region tanımlı değil** |

> **Yetenek şartı uyarısı:** `placeholderRequirement` ile AuraSkills seviyesi şartı koyacaksan,
> PlaceholderAPI'nin **tam placeholder adını** doğrula (AuraSkills'in PAPI hook'unu oku
> veya çalışan sunucuda `/papi parse` ile test et). Emin değilsen **placeholder adını
> uydurma**; `# DOĞRULA: <şüpheli placeholder>` notu koy ve doğrulama adımını yaz.
> Emin olduğun yerlerde (`%player_level%` vb.) doğrudan kullan.

### 1.9 Görev verisi nerede duracak
- `plugins/BeautyQuests/quests/` → **şu an boş**, hiç görev yok.
- `plugins/BeautyQuests/questPools.yml` → `{}` boş. **Doldurma.**
- `plugins/BeautyQuests/data.yml` → `version: 2.1.0`, `lastID: 0`.
- Görev dosyaları **UTF-8, BOM'suz** kaydedilecek (BOM eklendiğinde plugin bozulur).
- `redoMinuts: 5`, `maxLaunchedQuests: 0` (sınırsız eşzamanlı görev).
- `scoreboards: true` → görev ilerlemesi sağ üstte skor tablosunda gösterilir; 750 gövde
  yığılmasını önlemek için **her oyuncuda aynı anda açık görev sayısını 12-18 bandında tut**
  (tasarım kuralı, aşağıda).

### 1.10 Mevcut sunucu aşamaları (görev dağılımının iskeleti)
- **Aşama 1 — Başlangıç (ilk 30-60 dk):** barınak, yemek, temel alet, ilk arsa (10x10).
  Çıkış: tam demir set + yay + 150₺ üzeri.
- **Aşama 2 — Meslek (2-4 saat):** en fazla 2 job, ilk gelir döngüsü, ilk 1000₺,
  elmas ekipman + büyü masası, **Orman Bekçisi** denenir. Çıkış: elmas set, 1 yetenek sv20+,
  Nether portalı.
- **Aşama 3 — End sonrası (ilk hafta):** Nether kalesi, blaze, potion altyapısı,
  **Kor Ata** ve **Derin Kahin**, End portalı, ejderha. Ejderha oyunun sonu DEĞİL;
  ondan sonra Tier IV-V açılır. Çıkış: End erişimi, elytra, 10.000₺.
- **Aşama 4 — Oyun sonu (haftalar):** netherite yükseltme, **Boşluk Ejderi**,
  **Üç Kardeş** (15-30 dk raid), çoklu yetenek sv40+, 10.000.000₺ üst kademe ödüller.

### 1.11 Dil ve anlatım kuralları (OYUNCUNUN GÖRDÜĞÜ HER METİN)
- **Görev adı, açıklama, aşama metni, ipucu, diyalog, ödül mesajı, hata mesajı → %100 Türkçe.**
- Sana hitap **tekil ve samimi ("sen")**. Sentrycilik, kurumsal ton, "Değerli oyuncu" yok.
- **Yasak terimler (görünen metinde):** quest, skill, money, balance, spawn, home,
  sethome, shop, sell, claim, trust, leaderboard, top, scoreboard, online, help, rules.
  **Doğru karşılıklar:** görev · yetenek · para · doğum noktası · ev · ev kur · market/pazar ·
  satış · arsa · güven · liderlik · skor tablosu · çevrimiçi · yardım · kurallar.
- Aynı kavram için **her zaman aynı kelime**. Bir yerde "kaya" diyorsan 750 görev boyunca
  "kaya" de (veya arz kararı ver ve tutarlı uygula).
- **Cümle kısası olsun:** görev adı ≤ 6 kelime, açıklama 1-3 cümle, aşama ipucu 1 cümle.
  Lore gerekiyorsa `startDialog` (en fazla 4-6 satır) kullan.
- Renk kodları: bilgi `&7`, vurgu `&6`/`&e`, para `&a`, hata `&c`, başarı `&a`.
  Başlık kartı `&6&lDGM CRAFT`.
- **Placeholder uydurma.** BeautyQuests'in gerçek placeholder'ları:
  `{prefix}` `{nl}` `{quest_name}` `{quest_description}` `{quest_id}` `{player}`
  `{player_display_name}` `{reward_description}` `{requirement_description}`
  `{stage_index}` `{stage_amount}` `{stage_description}` `{name}` `{remaining}`
  `{done}` `{total}` `{percentage}` `{progress_done}` `{progress_remaining}`
  `{progress_total}` `{progress_percentage}`.
- Emoji, meme, günlük dil, argo, siyasi/ dini içerik, cinsellik, 18+ **yok**.

### 1.12 Kurallar (ihlal = proje başarısız)
1. `starting-balance`, `max-money`, `worth.yml`, job gelir katsayısı **değiştirilemez**.
   Değişiklik önereceksen sadece **öneri + gerekçe** yaz, dosyaya dokunma.
2. Teknik adları (komut, permission, config key, plugin option) **Türkçeleştirme**.
3. `docs/quests.md` dosyasındaki eski format **geçersizdir**; onu örnek alma.
4. Boş zamanlı, kronikleşen görev yok; günlük/haftalık/tekrar yok; havuz yok.
5. Oyuncuya hiçbir yerde İngilizce metin gösterme.
6. Dünyada **olmayan** bir şeyi var gibi gösterme (özel köy, özel tapınak, özel dungeon,
   NPC, özel biome, harita işareti yok).
7. Görev ödülü olarak **AuraSkills XP veremezsin**; XP doğal kazanılır.
8. Ölüm eşya kaybı vardır; görev tasarımı buna saygı gösterir (aşağıda kurallar).

---

## 2. TASARIM FELSEFESİ — BUNU EZME

Bu bir "görev listesi" değil. Bu, **3 arkadaşın birlikte yazdığı ve oynayarak
yaşadığı bir dünya hikâyesidir.** Görevler sadece hikâyenin kaydıdır.

### 2.1 Temel ilke
> **Bir görev, oyuncuya "bir şey yap" dediği için değil; dünyada bir şeyin değiştiği için vardır.**

Her görev için şu testi uygula:
1. Bu görev tamamlanınca **dünyada gözle görülür bir iz** bırakıyor mu? (dikilen bir
   yapı, açılan bir kapı, kırılan bir kalıntı, bulunan bir eşya, öldürülen bir yaratık)
2. Bu iz, **hikâyede bir yere oturuyor mu?** Önceki görevle bağı var mı, sonraki görevi
   mi açıyor?
3. Eğer 1 veya 2 cevabı "hayır" ise → **görev yeniden yazılır veya silinir.**

### 2.2 Görev ağacı (quest tree) ilkesi
Görevler **liste değil, ağaç** olacak. Her bölüm (arc) bir ağaçtır:
- **Ana gövde (spine):** o bölümün hikâye sırası, sırayla ilerler.
- **Yan dallar (branches):** ana gövdeden açılan, ana hikâyeyi besleyen alternatif veya
  yan işler. Yan dallar ana hattı **bekletmez** ama tamamlanınca ana hatta **ek ödül** ve
  **hikâye parçası** açar.
- **Kilitli kapılar (gates):** bir görev, birden fazla ön koşul OR'dur
  (`logicalOr` veya paralel `questRequired` ile). Oyuncu "A yolunu ya da B yolunu" seçer.
- **Koridorlar (corridors):** hikâyede birbirini takip eden, oyunun bir bölümünü kaplayan
  görev zincirleri. Her koridor 8-20 görev içerir ve tek bir duygu/olay çözümü üzerine
  kuruludur (keşif, kuşatma, kaçış, kurtarma, yığılma, hesaplaşma, kabul, ihanet, dönüş...).

**Zorunlu kural:** Hiçbir noktada oyuncunun önünde **tek bir doğrusal koridor** olmasın.
Bölüm başına en az **3 paralel dal**, bölüm sonunda en az **2 farklı çıkış** olsun.
Oyuncu ilerledikçe seçenekleri daralsın (erken geniş, geç odaklı).

### 2.3 NPC'siz anlatım
Görev veren NPC yok. Hikâye şu kanallarla anlatılacak:
- **Görev metinleri** (`name`, `description`, `startDialog`, `customText`) — asıl anlatıcı.
- **Bölüm kartları** — bölüm başında `titleReward` ile ekrana çıkan tek satırlık başlık.
- **Dünya eylemi** — oyuncuların kendi diktiği/kazdığı/yaptığı yapılar. Hikâyenin
  fiziksel izi oyuncu yapar. Örnek: bir bölümün sonunda oyuncular bir "sınır ateşi"
  diker, bir "köprü" kurar, bir "tepki" inşa eder.
- **Sessiz çevre notları** (`hologramText` alanı hazır; FancyHolograms ile sonradan
  yerleştirilecek) — tasarım dokümanında "ileride hologram olarak eklenir" diye not
  düş, YAML'da kullanma.
- **Para yerine anlam:** ödülün bir kısmı para değil, **anlatı taşıyıcısı** olsun
  (başlık, eşya, ışık efekti, teleport, harita parçası).

### 2.4 Doldurma (filler) yasağı
- "64 taş kır", "10 koyun öldür", "5 elmas topla" gibi **bağlamından kopuk hedefler yasak**.
  Her hedefin bir **gerekçesi** olmalı: *"Neden bu taşı kırıyor? Kime/için çalışıyor?
  Bunu yapınca hikâyede ne değişiyor?"*
- Aynı kalıp iki kez üst üste kullanılmayacak (aşağıda anti-boring kuralları).
- Bir bloğu toplamak yerine, oyuncuyu **yapı kurmaya, yeri keşfetmeye, bir şeyi taşımaya,
  bir canlıyla uyumaya, bir zorluğu aşmaya** teşvik et. Çeşitliliği önceliklendir.

### 2.5 Ölüm ve risk tasarımı
- Eşya kaybı var. Bu yüzden:
  - Görev tanımlayıcı hedeflerde ödül kaybı **olmamalı** (ispat `MINE` sayacı kaldığı için
    blok kaybı ilerlemeyi sıfırlamaz — doğrula ve buna göre yaz).
  - Taşıma gerektiren aşamalarda (`ITEMS`, `removeItemsReward`) oyuncuyu **yük taşıma
    riskine** sokma; hedefi taşıma yerine bırakılan yeri bulma/hatırlama yap.
  - Ölümde tüm ilerleme sıfırlanacak görev **yazma** (`failOnDeath` yalnız bilinçli
    bir ceza/gerilim aracıysa ve tasarımda gerekçesi yazıyorsa).
  - Ölümde eşya kaybedilen ödülleri (netherit hurdası gibi) yalnız **çok ileri
    bölümlerde** ve hedefi tamamlanmış oyuncuya ver; böylece oyuncu emeğini ölüm yüzünden
    kaybetmesin.

### 2.6 3 kişilik tasarım
- Sunucu **3 kişilik**. Tasarım bu sayıyı ciddiye almalı, ama **hiçbir ana hat görevini
  zorunlu olarak 3 kişiye bağlama** (biri gün gelmezse sunucu kilitlenir).
- Üç kademeli yaklaşım:
  1. **Solo-capable (çoğunluk, ~%70):** tek oyuncu tamamlayabilir, tamamlar.
  2. **Birlikte daha iyi (~%20):** oyuncu tek başına da yapabilir ama 3 kişi birlikte
     yapınca farklı (daha geniş, daha hızlı, daha zengin) bir çözüm açılır.
  3. **Ritüel 3'lü (~%10):** boyut, hikâye ve ödül olarak 3 kişilik tasarlandı. Teknik
     olarak zorunlu kilit yok; üç oyuncu aynı görevi kendi defterinde görür ve
     **üçü de bitirince dünya değişir**.
- **3'lü tasarımların kurgusal karşılığı:** hikâyede üç kahraman/kardeş/soy var.
  Üç oyuncu bu üçü oynar. Her bölümde "kimin yolu?" belirgin olsun.
- **EliteMobs party sistemi** mevcut: en fazla 5 kişi, **128 blok yakınlıkta paylaşımlı
  ilerleme**. Raid/boss görevlerinde bu 128 blok kuralını oyuncuya anlatıcı metin olarak
  yaz ("Beraberce yakın durun, 128 blok ötesinde birliktelik bozulur").
- Ölçeklenebilir hedef kuralı: "3 oyuncu 3 ayrı ayrı 20 taş kırar" yerine
  "3 oyuncu birlikte 20 taş kırar" (3 oyuncu için) → tek oyuncu için hedefi 20'de tut,
  istersen 1-2 oyuncuya daha fazlasını önerme.

---

## 3. HİKÂYE ÇERÇEVESİ

### 3.1 Hikâyenin çekirdeği (bunu değiştirme, DÜZENLE)
5 EliteMobs boss'ı hikâyenin **beş dayanağıdır** ve çoktan tasarlandılar:
Orman Bekçisi → Kor Ata → Derin Kahin → Boşluk Ejderi → **Üç Kardeş**.

**"Üç Kardeş"** hikâyenin kilidi: üç kardeş birbirini izleyen üç koruyucu; en güçlüsü
olan sonuncusudur (haftalık cooldown'lu, raid). Hikâyeye göre **üç oyuncu, üç kardeşten
birerine bağlanır.** Hikâyenin sonu: üç kardeşin yeniden bir araya gelmesi (veya ayrılması
— sen karar ver, ama **sonuç ödülü oyuncuların 40+ saatlik emeğini hak etsin**).

### 3.2 Senin yaratman gereken
- **Dünya kuramı (lore bible):** bu dünyada ne oldu, kardeşler kim, neden ayrıldılar,
  oyuncular neden buradalar, hangi güç onları bir araya getiriyor.
- **Antagonist / itici güç:** oyuncuya düşmanlık eden şey kim veya ne. Vanilla'dan
  türetilmiş olmalı (kızıl ay, çürüme, boşluk, derinlik, yok oluş — kısacası mevcut
  Minecraft düşman dokusu).
- **Factions/haneler:** en az 3, en fazla 5. Her birinin dünyada izi olsun (yıkık yapı,
  özel renk eşyası, özel mob kombinasyonu, özel alan).
- **Zaman çizelgesi:** hikâyenin hangi bölümü oyunun hangi saatinde oynanıyor.
- **Kayıp/şaşırtma katmanları:** 12 bölüm boyunca yavaşça açılan, ilk bölümlerde
  fark edilmeyen, 8. bölümden sonra anlam kazanan en az 3 ayrıntı.
- **Tema uyarısı:** "başlangıçta her şey yeni doğuyor, orta bölümlerde eski dünya
  uyanıyor, finalde bir seçim yapılıyor" gibi bir yay çizgisi kur.

### 3.3 Anlatım tonu
- **Sürüreal folklor + doğa + ışık/karanlık.** Grimdark değil, klişe "iyiye karşı kötü"
  değil. Oyuncu 3 arkadaşla eğlenerek oynuyor; hikâye onları **merak ettirmeli, şaşırtmalı,
  bazen korkutmalı**, ama ağırlaştırmamalı.
- Lore metinleri **4-6 satırı geçmesin**. Kısa, vurucu, tekrar etmeyen.
- Her bölümün tek bir **duygusal cümlesi** olsun ("Bu bölümde ikinci kez yalnız kalırsın",
  "Bu bölümde ilk kez bir şey kaybedersin", "Bu bölümde ilk kez bir şeyi paylaşırsın").
- 750 görevlik bir hikâyede **tekrar eden kalıplar** (her bölüm "bul, topla, getir")
  yasak. Her bölümün **farklı bir anlatı tekniği** olsun: keşif, gerilim, kayıp, dönüş,
  seçim, kurban, kurtuluş, yas, doğum, ihanet, affediş...

### 3.4 Bölüm (arc) mimarisi — ZORUNLU SAYILAR
**Tam 750 görev.** Ana hat + yan görev olarak dağıt. Aşağıdaki tablo **birebir**
uygulanır ve **750'ye tam olarak eşittir** (kontrol toplamı: 580 + 170 = 750):

| # | Arşiv (bölüm) | Ana hat | Yan | Toplam | Oyun saati (tek kişi) | Sunucu aşaması |
|---|---|---|---|---|---|---|
| 0 | **Uyanış** (prolog) | 28 | 6 | 34 | 30-60 dk | Aşama 1 |
| 1 | Orman Sözleşmesi | 36 | 11 | 47 | 1-1.5 sa | Aşama 1→2 |
| 2 | Toprağın Altındaki Kuyu | 40 | 13 | 53 | 1.5-2 sa | Aşama 2 |
| 3 | Demir Çağı | 42 | 12 | 54 | 2-3 sa | Aşama 2 |
| 4 | Kızıl Kapılar | 44 | 14 | 58 | 3-4 sa | Aşama 2→3 |
| 5 | Boğaz | 44 | 13 | 57 | 3-4 sa | Aşama 3 |
| 6 | Kemik Bahçesi | 46 | 12 | 58 | 4-6 sa | Aşama 3 |
| 7 | Gökyüzünün Kırığı | 46 | 13 | 59 | 5-7 sa | Aşama 3 |
| 8 | Kardeşler Arasında | 48 | 14 | 62 | 6-9 sa | Aşama 3 |
| 9 | Boşluğun Ötesinde | 48 | 12 | 60 | 7-10 sa | Aşama 3→4 |
| 10 | Uyumsuz Kule | 48 | 13 | 61 | 8-12 sa | Aşama 4 |
| 11 | Kızıl Ay Odası | 50 | 12 | 62 | 8-12 sa | Aşama 4 |
| 12 | **Üç Kardeş** (final) | 60 | 5 | 65 | 10-15 sa | Aşama 4 |
| — | Epilog / serbest oyun | 0 | 20 | 20 | serbest | Aşama 4 |
| | **TOPLAM** | **580** | **170** | **750** | **~70-100 saat** | |

Bu tablo **değişmez.** Yapı/hesap kontrolü:
Ana hat: 28+36+40+42+44+44+46+46+48+48+48+50+60 = **580**
Yan görev: 6+11+13+12+14+13+12+13+14+12+13+12+5+20 = **170**
Toplam: **750** ✓

Bölüm adları ve sıralaması da sabittir (hikâye yay çizgisi buna göre kurulur).

---

## 4. TASARIM DOKÜMANININ İÇERİĞİ (Aşama 1 çıktısı)

Tek bir `TASARIM.md` (veya eşdeğer) dosyasında şu bölümler, bu sırayla:

1. **Tek sayfa özet:** oyuncuya 5 cümlede ne anlatıyorsun.
2. **Lore bible:** dünya kuramı, kardeşler, hanaeler, itici güç, zaman çizelgesi.
3. **Karakter/rol dosyaları:** 3 oyuncunun oynayacağı 3 yol; her birinin yetenek odağı,
   zorluk profili, hikâyedeki yeri, finaldeki kaderi.
4. **Bölüm haritası (13 arşiv + epilog):** her bölüm için
   - başlık, tek cümlelik duygu, oyun saati, gerekli en az/önerilen en fazla yetenek seviyesi
   - gerekli para bandı (giriş ve çıkış), hikâyede kapı açan diğer bölümler
   - **ASCII veya mermaid görev ağacı**: her bölüm en az 3 dal, koridorları isimlendirilmiş,
     dallarda "A yolu / B yolu" etiketleri, kilit simgeleri (🔒) ve açılma koşulları
   - bölümdeki **koridor listesi** (her koridorun adı, kaç görev, ne hissettirmesi gerektiği)
5. **Görev envanteri tablosu (750 satır):** her görev için
   `ID · Ad · Arşiv · Koridor · Ana/Yan · Zorluk (1-5) · Tahmini süre · Ana ölçüt
    (stageType listesi) · Para ödülü · Eşya ödülü · Başlık ödülü · Ön koşullar (questID) ·
    Sonraki görevler · Dünyaya bıraktığı iz · Co-op seviyesi (1/2/3) · 1-3 cümlelik özet`
6. **Ekonomi denge tablosu:** bölüm bölüm toplam para, eşya, başlık; oyuncu başına kümülatif
   kazanç; bu rakamların jobs geliriyle (0.05₺/XP) ve kit/market lavabolarıyla ilişkisi.
7. **Anti-boring denetim raporu:** aşağıdaki kuralların her biri için sayısal kanıt
   (örn. "MINE aşaması oranı %23, sınır %30").
8. **Yetenek şartı doğrulama tablosu:** kullandığın her PAPI placeholder'ı için
   "doğrulandı / DOĞRULA" durumu ve test komutu.
9. **Kurulum kılavuzu:** dosya adlandırma, ID atama sırası, yükleme adımları,
   UTF-8 BOM uyarısı, doğrulama komutları, geri alma.
10. **Riskler ve açık noktalar:** hangi mekanik test edilemedi, hangi koordinat gerekli,
    hangi boss takibi belirsiz.

---

## 5. GÖREV ANATOMİSİ VE İSİNLİK KURALLARI

### 5.1 Her görevde zorunlu alanlar
- `name` — 2-5 kelime, Türkçe, hikâyeye dokunan, oyuncuya bir şey vaat eden.
- `description` — 1-3 cümle. **Ne yapılacak + neden + hikâyede ne olacağı.**
- `startMessage` (isteğe bağlı ama 180 görevde zorunlu) — sahne kurgusu.
- `startDialog` — bölüm açılışlarında ve kilitli kapılarda 4-6 satır lore.
- `customItem` — her göreve uygun ikon (bölüm temasına göre).
- `customOrder` — bölüm içi okuma sırası.
- `requirements` — ön koşullar (varsa).
- `manager.branches.'0'.stages` — **en az 1 aşama**.
- `endRewards` — her görevde en az 1 ödül (bunlar olmazsa oyuncu ilerlemez).

### 5.2 Aşama kuralı
- Her görevde **1-4 aşama**. Ortalama **2.1**.
- Aşama metni (`customText`) oyuncuya **ne yapması gerektiğini** söyler, ipucu verir.
- `objects` içindeki UUID'ler **dosya içinde benzersiz** olsun, elle yaz.
- Hiçbir aşamanın `objects`/`items` listesi boş bırakılmaz (yapılamıyorsa o aşamayı
  `PLACE_BLOCKS`, `ITEMS` veya `LOCATION` ile yeniden yaz).
- `stageType` dağılımı (tüm sistem geneli, toplam tam 100):
  `MINE %18 · PLACE_BLOCKS %10 · MOBS %18 · LOCATION %10 · ITEMS %8 · INTERACT_BLOCK %6 ·
   CHAT %4 · EAT_DRINK %3 · CRAFT %6 · FISH %4 · TAME %3 · BREED %2 · ENCHANT %3 ·
   DEAL_DAMAGE %3 · PLAY_TIME %1 · MELT %1 · DEATH %0 · BUCKET %0`
  (Kendi dağılımını hesapla, bu tabloyla karşılaştır, farkı raporla.)

### 5.3 Anti-boring kuralları (sayısal, denetlenebilir)
1. **Aynı kalıp üst üste:** Ardışık 3 aşama asla aynı `stageType` olamaz.
2. **MINE sınırı:** Tek görevde `MINE` aşaması en fazla 1; görev içi toplam kırılacak blok
   en fazla 64 (devasa yığın kırma yok). Bölüm genelinde `MINE` aşaması oranı **%25'i geçmez.**
3. **MOBS sınırı:** "N mob öldür" hedeflerinin **%60'ı tek seferde tekrarlanan** olmaz;
   hedeflerin en az %40'ı **belirli bir yer, koşul veya bağlam** taşır (örneğin
   "yalnızca gece", "yalnızca yağmurda", "su altında", "belirli bir yerde 3 kez").
4. **Collect-only yasağı:** Tek başına "topla/ver" içeren görev oranı **%15'i geçmez**
   ve bunlar ya bir hikâye ipucu taşır ya da bir üst görevi besler.
5. **Aynı hedef tekrarları:** 750 görev içinde aynı `object.blocks` + aynı `amount`
   ikilisi **en fazla 2 kez** geçer.
6. **Ödül monotonluğu:** Ardışık 3 görevin parasal ödülü birbirinden **%25'ten az**
   farklı olamaz (sürpriz ödül, bölüm sonu ve final dışında yasak).
7. **Boş dönem yasağı:** Bir bölümde 3 görev üst üste "düz toplama/taşıma" içeremez.
8. **Her bölümde en az:** 1 `PLACE_BLOCKS` (dünyaya iz), 1 keşif aşaması, 1 lore `CHAT`
   veya `startDialog`, 1 yetenek-şartlı geçiş, 1 `logicalOr` kapısı, 1 `titleReward`.
9. **Ölçek:** Hiçbir görev tek başına **45 dakikadan uzun** sürmemeli.
   "45 dk+ görev" ancak bölüm finali veya 3'lü ritüel ise, işaretle.

### 5.4 Koordinat ve konum kuralları
- `LOCATION` / `INTERACT_LOCATION` / `INTERACT_BLOCK` / `tpReward` için **koordinat
  şu an bilinmiyor** (dünya rastgele seed ile üretildi, hiç keşfedilmedi).
- Bu yüzden:
  1. **Yapı tarzına dayalı hedefler** kullan: `location: {world: world, x: 0, y: 0, z: 0,
     radius: 9999}` gibi tüm dünyayı kapsayan yarıçap + `customDescription` ile
     "bir denize, bir kıyıya ulaş" tarzı koşullar.
  2. Gerçekten belirli bir nokta gerekiyorsa **`# COORD_GEREKLI` işareti** koy ve
     tasarım dokümanında "kurulumdan sonra doldurulacak koordinat listesi" başlığı altında
     topla. Koordinat **uydurma.**
  3. Boss türü konum gerektiriyorsa: bossların `spawnLocations: []` boş olduğunu bil —
     yeri **görev sahnesi olarak değil, oyuncu keşfi olarak** tasarla.

---

## 6. ÖDÜL EKONOMİSİ VE DENGE

### 6.1 Para (₺) — bölüm bütçeleri
Sunucunun mevcut kuralı: **görev ödülü 50–250₺ bandında.** 750 görev olduğu için
ortalama ödül düşük tutulmalı, yoksa ekonomi şişer.

| Arşiv | Görev sayısı | **Hedef para toplamı** | Görev başına ortalama |
|---|---|---|---|
| 0 Uyanış | 34 | 1.700₺ | ~50₺ |
| 1 Orman Sözleşmesi | 47 | 2.400₺ | ~51₺ |
| 2 Toprağın Altındaki Kuyu | 53 | 2.800₺ | ~53₺ |
| 3 Demir Çağı | 54 | 2.900₺ | ~54₺ |
| 4 Kızıl Kapılar | 58 | 3.200₺ | ~55₺ |
| 5 Boğaz | 57 | 3.200₺ | ~56₺ |
| 6 Kemik Bahçesi | 58 | 3.300₺ | ~57₺ |
| 7 Gökyüzünün Kırığı | 59 | 3.500₺ | ~59₺ |
| 8 Kardeşler Arasında | 62 | 3.800₺ | ~61₺ |
| 9 Boşluğun Ötesinde | 60 | 3.700₺ | ~62₺ |
| 10 Uyumsuz Kule | 61 | 4.000₺ | ~66₺ |
| 11 Kızıl Ay Odası | 62 | 4.200₺ | ~68₺ |
| 12 Üç Kardeş | 65 | 6.000₺ | ~92₺ |
| Epilog | 20 | 1.200₺ | ~60₺ |
| **TOPLAM** | **750** | **~45.900₺** | **~61₺** |

Kurallar:
- **Sert tavan: 60.000₺.** Bu tavanı aşarsan tasarım yeniden dengelenecek.
- Görev başına ortalama 50-95₺ bandında kalacak; tek görev 250₺'yi **sadece** bölüm
  finali, boss ritüeli ve 3'lü büyük olaylarda geçebilir.
- Yan görevler ana görevlerden **düşük** ödül alır (30-60₺); ana hat %65-75 oranındadır.
- **~150 görev (%20) para yerine anlam ödülü alır** (başlık, eşya, lore, ışık efekti).
  Bu görevlerde para 0'dır ve tasarımda gerekçesi yazılır — 750 görevin hepsine para
  koymak, 70 saatlik oyunda kazanç dengesini bozar.

### 6.2 Para dışı ödüller (bunlar para baskısını söndürür)
- **`titleReward`:** her bölüm başı 1, bölüm sonu 1, 12 bölümde ek ara başlıklar.
  Toplam **28-35 başlık** (fazla değil, özel hissettirmeli). Başlık metinleri kısa ve
  edebî olsun ("Hikâyenin İlk Adımı", "Sessiz Anlaşma", "Kızıl Ayın Altında").
- **`itemReward`:** her zaman hikâyeye bağlı, dünyada bırakılabilir veya kullanılabilir
  eşya. **Yasak listesi:** totem, spawner, elytra, herhangi bir elmas/zümrüt/netherite
  ekipmanın tamamı (çok erken verirsen ekonomi çöker). Netherite yalnız 12. bölümde,
  yalnız **çok az sayıda** (toplam ≤ 6 adet) ve 3'lü ritüellerde.
- **`expReward` (vanilla XP):** yalnızca bölüm sonlarında, 100-500 arası. Her gün değil.
- **`firework`:** bölüm başı ve büyük başarılar (toplam ~20-30).
- **`tpReward`:** keşfedilen yerlere kısayol. `COORD_GEREKLI` gerekir.
- **`textReward`:** lore parçaları (zümrüt, kumanda kağıdı vb. gibi tematik eşya ile).
- **`commandReward`:** sadece zorunluysa (ör. `eco give {player} 50`, `{player}` aynen kalır).
  Başka komut kullanma.

### 6.3 Enjeksiyon kuralları
- **Para ödülünün %70'i bölüm/ara kilometre görevlerinde** toplanmalı; 750 göreve
  eşit dağıtırsan ekonomi şişer.
- Bölüm sonlarında "büyük ödül" tek noktada durmalı (yay çizgisinde iniş çıkış olsun).
- **Kümülatif ekonomi simülasyonu** dokümanda tablo olarak göster: 1. saat, 4. saat,
  1. gün, 1. hafta, 1. ay, tamamlanma anı için (para, eşya, yetenek sv).
- 5. bölümde oyuncu 10.000₺ eşiğini geçmelidir (sunucunun mevcut tasarımı).
- Finalde oyuncunun toplam parası 100.000-150.000₺ bandında olmalı.

### 6.4 Ödül→ilerme bağlantısı
Her ödül, oyuncunun **bir sonraki eylemine** yol açmalı. "Bu ödülü aldın, şimdi şunu
yapabilirsin" mantığı. Ödül tablosunda her bölümün ödülünün **hangi yeni imkânı açtığını**
yaz.

---

## 7. 3 KİŞİLİK BİRLİK TASARIMI

- Her bölümde en az **2** görev `Co-op 2` (birlikte daha iyi), her 3 bölümde en az
  **1** görev `Co-op 3` (ritüel) olsun. Toplam Co-op 3 görev **28-35** civarında olsun.
- 3'lü ritüeller şu yapıda olsun:
  - Üç oyuncu aynı görevi kendi defterinde görür.
  - Her birinin hedefi **kendi rolüne özeldir** (ör. "Sen kuzey kanadını yak").
  - **Üçü de bitirince** dünya değişir (`requirementDependentReward` veya ortak
    `endRewards` tetiklenir).
  - Teknikte "3 kişi kontrolü" yoktur; kapı, zincirin tamamlanmasıyla açılır.
- Her bölümde **en az bir "paylaşım" anı** olsun: ortak yapı (birlikte dikilen yapı),
  ortak kaynak (birlikte toplanan malzeme), ortak kayıp (birinin düşen eşyası).
- **128 blok** paylaşımlı ilerleme kuralını oyuncu metnine şöyle yansıt:
  "Beraber çalışırken aranızda 128 bloktan fazla mesafe olmasın."

---

## 8. ÇIKTI FORMATI VE TESLİMAT PLANI

### 8.1 Dosya yapısı
```
cikti/
  TASARIM.md                 # 4. bölümdeki 10 başlıklı tam doküman
  MANIFEST.csv               # id, dosya, ad, arsiv, koridor, ana/yan, zorluk, para, on_kosul
  00-OKUBENI.md              # bu teslimatın nasıl okunacağı, kurulum sırası
  quests/
    0001-uyanis-orman.yml     # her görev için AYRI dosya, slug ASCII (ö/ü/ş KULLANMA)
    0002-....yml
    ...
    0750-....yml
  kurulum/
    KURULUM.md               # adım adım yükleme + doğrulama + geri alma
    KOORDINATLAR.md           # COORD_GEREKLI listesi
    DOGRULAMA-CHECKLIST.md    # elle yapılacak testler
```

**Dosya adlandırma:** `4 haneli sıra numarası + ASCII slug` (ör. `0042-gece-nobeti.yml`).
Türkçe karakter **yok** (Windows + BOM + plugin yükleme sorunları), görev adı ise
YAML içinde tam Türkçe kalır.

### 8.2 ID atama kuralı (kritik teknik konu)
- `questRequired.questID` **sayısal** referanstır. Bu yüzden ID ataması
  **topolojik sırayla** yapılmalı: bir görevin ön koşulu olan görev **daima daha düşük
  ID'ye** sahip olmalı.
- ID'leri 0001'den 0750'ye kesintisiz ver, `MANIFEST.csv`'de eşle.
- Kurulum sırası: **önce boş `data.yml` ile plugin'i bir kez açıp ID atamasını doğrula**
  (`data.yml:lastID` otomatik artar). Elle yazarken plugin'in gerçek ID atamasıyla
  uyuşmayabilir; bu yüzden `KURULUM.md` içinde **"ID atamasını plugin'e bırakmak için
  dosyaları alfabetik sırayla yükle ve `/bq reload` sonrası `data.yml:lastID` değerini
  kontrol et"** adımını zorunlu kıl.
- Eğer plugin'in ID ataması senin planınla uyuşmuyorsa, kurulum notunda **"önce görevleri
  ön koşul sırasına göre tek tek yükle, `data.yml`'yi izle, `MANIFEST.csv`'yi gerçek
  ID'lerle güncelle"** yolunu ver. Bu, 750 görevde kritiktir.

### 8.3 Doğrulama (kendi kendini test et)
Çıktıyı vermeden önce şu 12 kontrolü kendin çalıştır ve sonuçları `TASARIM.md`'nin
sonuna tablo olarak yaz:
1. Toplam görev sayısı tam **750** mi?
2. Her `questID` referansı manifestte **gerçekten var** mı ve daha düşük ID mi?
3. Her dosyada `manager.branches.'0'` **tam sayı** anahtar mı?
4. Her dosyada en az bir `stageType` **geçerli listeden** mi?
5. Hiçbir yerde `objectives:` / kök `rewards:` / `rewardsList` / `customMaterial` /
   `pool` / `starterNPC` / `BRING_BACK` / `regionRequired` / `NPC` **yok mu**?
6. Toplam para 60.000₺'yi geçmiyor mu?
7. `MINE` oranı %25, collect-only %15 altında mı?
8. Ardışık 3 aşama aynı `stageType` değil mi?
9. Her bölümde zorunlu 8 unsurun tamamı (5.3 madde 8) var mı?
10. Tüm görünen metinlerde yasak İngilizce terim **yok mu**?
11. Uydurulmuş koordinat / dünya dışı mekan **yok mu** (hepsi `COORD_GEREKLI` mi)?
12. Her görevin `endRewards` dolu mu ve `description` en az 1 cümle mi?

### 8.4 Çıktı uzunluğu yönetimi
750 görev tek mesajda sığmaz. Şu protokolü kullan:
- Önce `00-OKUBENI.md` + `TASARIM.md`'nin 1-4. bölümleri.
- Sonra arşiv arşiv YAML: her mesajda **bir arşiv** (ortalama 60-70 görev) ve
  mesajın başında `=== ARŞİV N / 13 — <ad> — görev 0101-0164 ===` yaz.
- Her mesaj sonunda o arşivin `MANIFEST.csv` parçasını da ver.
- **Hiçbir görevi atla, kısaltma veya "devamı gelir" diye bırakma.** 750 göevin
  tamamını teslim etmeden işi bitmiş sayma.
- Her arşiv tesliminden sonra "Bu arşivin özeti" bölümünü (ne anlatıyor, hangi dünya
  izini bırakıyor, ekonomi etkisi) yaz.

### 8.5 Her görev dosyasının şablonu
> **ŞEMA ÖRNEĞİ — son değildir.** `objects` içindeki `id` değerleri (nesne üretici kimlikleri)
> sunucuda `/bq` ile bir görev oluşturup `data.yml`/kaydedilmiş dosyadan **doğrulanmalıdır**.
> Emin değilsen `# DOĞRULA: <nesne id>` notu koy, uydurma. Kalan tüm alanlar şemadaki
> yapıya aynen uyar.

```yaml
# 0037-gece-nobeti.yml
name: 'Gece Nöbeti'
description: 'Orman Bekçisi uyanmadan önce ateş yak. Ateş gece yarısı söndüğünde
  geride yalnızca bir kıvılcım kalır; o kıvılcım yolunu gösterecek.'
customItem: {material: REDSTONE_TORCH, amount: 1}
cancellable: false
failOnDeath: false
repeatable: false
timer: 0
hideNoRequirements: false
scoreboard: true
customOrder: 37
startMessage: '&7Gece yaklaşıyor. Bekçi de uyanıyor.'
startDialog:
  lines_amount: 4
  lines:
    - '&7Ateşi yüksek yak.'
    - '&7Ormanın kenarında bekle.'
    - '&7Kıvılcımın yönünü izle.'
    - '&7Geri dönme.'
endMsg: '&aGece geçti. Bekçinin gözü kısaldı.'
endRewards:
  - id: moneyReward
    money: 55
  - id: expReward
    xp_amount: 50
manager:
  branches:
    '0':
      stages:
        '0':
          stageType: PLACE_BLOCKS
          customText: 'Gece çadırının yanına bir ateş dik.'
          options:
            progressbar: true
          objects:
            'e3b0c442-98fc-1c14-9afb-f4c8996fb924':
              amount: 3
              object:
                id: mc_do_not_use
                blocks: {material: CAMPFIRE}
          rewards:
            - id: textReward
              message: '&7Odunun kokusu dağıldı.'
requirements:
  - id: questRequired
    questID: 31
```

---

## 9. ASLA YAPMA (yasak liste)

1. NPC, MythicMobs, BetonQuest, günlük/haftalık görev, havuz (pool), tekrarlanan görev
   (`repeatable: true`), tekrarlanabilir boss rotasyonu **kurgulama**.
2. `docs/quests.md`'deki eski formatı kullanma.
3. Oyuncuya İngilizce metin gösterme. Plugin option adlarını/permission'ları Türkçeleştirme.
4. Dünyada olmayan lokasyonu, köyü, tapınağı, dungeon'ı, biome'u, harita işaretini
   **var gibi gösterme.** Koordinat uydurma.
5. `starting-balance`, `max-money`, `worth.yml`, job katsayısı, plugin config'i,
   `server.properties`, JVM flag'lerini **değiştirme**.
6. Her bölümde aynı kalıbı tekrarlama; "her bölüm = kır, topla, getir" yapma.
7. Görev ödülü olarak AuraSkills XP verme.
8. 750 görevi doldurmak için **işe yaramaz görev** ekleme. Az ama sağlam > çok ama boş.
   (Sayı sözleşmesi 750'dir; bunu kaliteden ödün vermeden tutturmak senin görevin.)
9. Çıktıyı yarım bırakma, özetleme, "örnek gösterdim gerisini sen yap" tarzı kısaltma.
10. Emoji veya günlük dil görev metnine koyma.

---

## 10. BAŞLANGIÇ: İLK 5 DAKİKADA YAPILACAKLAR

1. `TASARIM.md`'nin lore bible + 13 arşiv + 3 rol bölümünü yaz.
2. 13 arşivin ASCII/mermaid ağacını çiz, koridorları isimlendir.
3. `MANIFEST.csv` başlığını ID sırasıyla doldur (önce iskelet, sonra detay).
4. Ekonomi denge tablosunu hesapla (bölüm toplamları, kümülatif tablo).
5. Arşiv 0'ı (Uyanış, 35 görev) eksiksiz yaz: tasarım + YAML + manifest parçası.
6. Kendi doğrulama tablonu çalıştır ve sonuçları yaz.

Sonra kalan 12 arşivi aynı disiplinle, tek tek teslim et. **Hikâye bütünlüğünü koru:
sonraki arşivi yazmadan önce bir öncekinin hikâye sonucunu ve dünyaya bıraktığı izi
kendin kontrol et.** 750 görev, 70-100 saatlik bir deneyim olmalı — en az o kadar
sürecek kadar derinlikli, en fazla o kadar uzunacak kadar dengeli.
