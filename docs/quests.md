# DGM Craft Görev Tasarımı — BeautyQuests ile oyun içinden kurulur
# NOT: BeautyQuests görevleri resmi olarak oyun-içi GUI (/bq create) ile
# oluşturulur; elle YAML yazımı desteklenmez. Bu dosya admin için
# kopyala-uygula içerik spesifikasyonudur. Her görev GUI'de açılır,
# aşağıdaki hedef/ödül/süre aynen girilir, /bq save ile kaydedilir.
# Ödül komutlarında {player} placeholder aynen kalır (çevrilmez).

## Başlangıç (tek seferlik, ilk gün)
1. Orman Uyanışı — MINE 16 OAK_LOG (placeCancelled) — ödül: eco 50 + ekmek x8
2. Köy Çanı — LOCATION spawn 100 blok yarıçap — ödül: 25 coin + 10 XP
3. İlk Ev — PLACE 20 OAK_PLANKS + starter ev — ödül: 40 coin

## Günlük (pool: gunluk, havuz süresi 1 gün, her giriş 2 görev)
4. Günlük Odun — MINE 32 OAK_LOG — ödül: 40 coin
5. Mağara Temizliği — MOBS ZOMBIE x10 + SPIDER x5 — ödül: 60 coin + demir x4

## Haftalık (pool: haftalik, havuz süresi 7 gün)
6. Madenci Haftası — MINE IRON_ORE x24 + COAL_ORE x32 — ödül: 200 coin + elmas x2
7. Orman Bekçisi — MOBS custom boss dgm_orman_bekcisi x1 — ödül: 150 coin + boss loot

## Keşif / Av / Toplama (tek seferlik zincir)
8. Kayıp Tapınak — LOCATION + NPC dialog 4 satır — ödül: 100 coin
9. Nether Kapısı — LOCATION nether + MOBS BLAZE x6 — ödül: 250 coin

## Grup (3 kişi, herkes ayrı alır)
10. Üçlü Baskın — DEALDAMAGE 200 + MOBS SKELETON x15 — ödül: her oyuncuya 120 coin

## Challenge (tek seferlik)
11. Ölmeden 30 Dakika — PLAYTIME 30dk (ölümde sıfırlanır) — ödül: netherite hurdası x1

## Havuz ayarları (GUI: Pools menüsü)
- gunluk: poolTime 1 gün, poolQuestsPerLaunch 2, poolRedo true
- haftalik: poolTime 7 gün, poolQuestsPerLaunch 2, poolRedo true
- Menü: categorize quests by pools = true (config'te açık)
