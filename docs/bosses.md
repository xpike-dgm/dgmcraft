# Bosses — EliteMobs (5 Tier)

EliteMobs 10.9.5 kullanılır. MythicMobs yoktur (ücretli olduğu için ücretsiz alternatif seçildi).
Tüm bosslar regional boss olarak ayarlanır, telegraph saldırılar kullanılır, 3 oyuncu dengesine göre ölçeklenir.
Vanilla dışı EliteMobs sistemleri kapalıdır: Elite ekonomisi, prosedürel loot, rastgele event bossları, custom enchantment dağıtımı.

## Genel Kurallar

- Bosslar arena dışına çıkarılamaz (leash menzili içinde).
- Telegraph: zeminde işaret/parçacık görüldüğünde kaçının, kalkanlı yönü kullanın.
- Ölümde boss can yenilemez, 5 dakika içinde dönülebilir.
- Dungeon hedef süresi: 15-30 dakika.

## Tier Listesi

### Tier I — Orman Bekçisi (orman/mağara)
- Zombie, level 12, health x2.5, damage x0.8
- Güçler: ground_pound, attack_push (telegraph'lı alan saldırısı)
- Respawn: 30 dk. Ödül: ~50₺ + demir ekipman (BeautyQuests üzerinden)
- Gereksinim: demir set, Progression Aşama 1-2

### Tier II — Kor Ata (Nether)
- Wither Skeleton, level 20, health x3.0, damage x1.0
- Güçler: flame_pyre, attack_fire
- Respawn: 60 dk. Ödül: blaze çubuğu + orta kademe coin
- Gereksinim: elmas ekipman başlangıcı, ateş direnci

### Tier III — Derin Kahin (okyanus/Ancient City)
- Drowned, level 28, health x4.0, damage x1.1
- Güçler: frost_cone, attack_gravity; %50 canda faz 2 (skeleton_pillar)
- Respawn: 120 dk.
- Gereksinim: tam elmas set, su nefesliliği

### Tier IV — Boşluk Ejderi (End sonrası)
- Enderman, level 35, health x5.0, damage x1.2
- Güçler: plasma_blaster, attack_vacuum, spirit_walk
- Respawn: 180 dk, timeout 15 dk.
- Gereksinim: End seti, Progression Aşama 3 (ejderha sonrası)

### Tier V — Final: Üç Kardeş (raid)
- 3 fazlı final: Zombie 30 → Skeleton 30 (bullet_hell) → Wither Skeleton 32 (thunderstorm + reinforcement)
- Hedef süre 15-25 dk, 3 oyuncu zorunlu.
- Ödül: kupa + üst kademe coin (500-1500₺ bandı üstü)

## Denge Gerekçesi

3 kişi elmas set DPS ~20-25/sn. Tier I ~90 HP = kaçınma ile 2-3 dk encounter.
Final ~1500 HP + parti ölçeği + faz geçişleri = 15-25 dk.
`damageMultiplier` 1.4 üzerine çıkarılmaz (tek yeme riski). Süre ayarı önce `healthMultiplier` ile yapılır.
