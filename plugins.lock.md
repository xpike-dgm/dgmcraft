# plugins.lock — Kilitli Sürüm Listesi

Tarih: 2026-09-21 kuruldu / 2026-09-22 doğrulandı / **2026-09-26 MC 26.1.2'ye düşürüldü ve doğrulandı.**
Değişiklik için AI_MANAGER kuralı geçerlidir: yedek + CHANGELOG zorunlu.

| Ad | Sürüm | MC Uyumu | Kaynak | Tarih | Bağımlılık | Amaç |
|---|---|---|---|---|---|---|
| Purpur | **26.1.2 build 2592** | 26.1.2 | purpurmc.org (resmi API) | 2026-09-26 | Java 25 | sunucu çekirdeği (26.2 build 2633 `geri-donus/` değil, kökte `purpur-26.2-2633.jar` olarak saklanıyor) |
| LuckPerms-Bukkit | 5.5.71 | 26.2 (ve 26.3) | Modrinth (resmi) | 2026-09-21 | — | permission, `oyuncu` / `admin` grupları |
| VaultUnlocked | 2.20.3 | 26.2 (ve 26.3) | Modrinth (resmi) | 2026-09-21 | — | ekonomi köprüsü (aktif fork) |
| EssentialsX | 2.22.1-dev+24-49a2f10 | 26.2 | Jenkins ci.ender.zone (resmi dev) | 2026-09-21 | VaultUnlocked | home, teleport, money, kit, sell |
| EssentialsX Spawn | 2.22.1-dev+24-49a2f10 | 26.2 | Jenkins ci.ender.zone (resmi dev) | 2026-09-21 | EssentialsX | spawn yönetimi |
| AuraSkills | 2.4.0 | 26.2 (ve 26.3) | Modrinth (resmi) | 2026-09-21 | VaultUnlocked, PlaceholderAPI | 11 skill + jobs geliri |
| BeautyQuests | 2.1.0 (release) | 26.2 | Modrinth (resmi) | 2026-09-21 | — | görev sistemi (JVM EN locale flag gerekli, bkz AI_MANAGER §2) |
| EliteMobs | 10.9.5 | 26.2 (ve 26.3) | Modrinth (resmi) | 2026-09-21 | — | boss + dungeon (MythicMobs yerine ücretsiz) |
| GriefPrevention | 16.18.7 | 26.2 | Modrinth (resmi) | 2026-09-21 | — | claim koruması |
| PlaceholderAPI | 2.12.3 | 26.2 | Modrinth (resmi) | 2026-09-21 | — | placeholder altyapısı |
| TAB | 6.2.0 | 26.2 (ve 26.3) | Modrinth (resmi) | 2026-09-21 | PlaceholderAPI | tablist, scoreboard |
| KaMenu | 2.0.7 | 26.2 | Modrinth (resmi) | 2026-09-22 | PlaceholderAPI (soft) | dialog /menu hub (sandık menü yok) |
| GUIShop | 9.4.4 | 26.2 | Modrinth (resmi) | 2026-09-22 | Vault | market (alis/satis, DGM fiyatli) |
| packetEvents | 2.13.0+spigot | 26.2 | Modrinth (resmi) | 2026-09-22 | — | kutuphane (GUIShop bagimliligi) |
| Chunky | 1.5.3 (Bukkit) | 26.2 | Modrinth (resmi) | 2026-09-22 | — | harita on-uretimi (lag azaltma) |
| DgmGecmis | 1.0.1 | 26.2 (ozel derleme) | yerinde derlendi (paper-api 26.2) | 2026-09-22 | — | /gecmis: son 100 log satiri (kisisel, IP filtreli) + gamemode degisikligi denetimi |
| Skript | 2.16.2 | 26.2 | Modrinth (resmi) | 2026-09-22 | Vault (soft) | Turkce komut paketi (60+ komut): /odul /cevrimici /zar /yazitura + tum gunluk komutlarin Turkcesi (/ev /para /guven /pazar ...) |
| WorldGuard | **7.0.18** | 26.1, 26.1.1, 26.1.2, 26.2, 26.3 | Modrinth (resmi) | 2026-09-26 | — | bölge koruması (elite mob spawn alanı) |
| WorldEdit | 7.4.5+7590 | 26.1 / 26.2 | Modrinth (resmi) | 2026-09-21 | — | düzenleme aracı, WE silahları kapalı |
| spark | gömülü (Purpur) | 26.2 | gömülü | 2026-09-21 | — | profilleme, ayrı jar yok |

Notlar:
- **2026-09-26 sürüm düşürme:** Purpur 26.2 build 2633 → **26.1.2 build 2592** (MD5 `0d01a9bcabd5e32b1e5e5d48901f1f17` ile doğrulandı). WorldGuard 7.0.19 `api-version: "26.2"` olduğu için 26.1'de yüklenmiyordu → **7.0.18**'e düşürüldü (26.1–26.3 arası uyumlu). Kullanılmayan 7.0.19 jar'ı `geri-donus/worldguard-bukkit-7.0.19.jar` olarak `plugins/` DIŞINA taşındı.
  - **TÜM 31 eklenti 26.1.2'de 0 ERROR/SEVERE ile yüklendi**, BeautyQuests 750 görev/0 havuz ile açıldı, 8/8 örneğinde 4 dakika kararlı kaldı.
- **`plugins/` içinde yedeklenen `.jar` SAKLAMA.** Paper tüm `.jar` uzantılı dosyaları eklenti sayar; yedek jar `plugins/` içinde kalırsa `Ambiguous plugin name` hatasıyla sunucu açılmaz. Geri dönüş jar'ları kökte `geri-donus/` klasöründe tutulur.
- EssentialsX için stabil 2.22.0 yalnızca 26.1.2 etiketliydi; 26.2'ye geçişte resmi dev build (2.22.1-dev+24) kullanılmıştı. **26.1.2'ye dönüşte stabil 2.22.0'a geçirmek değerlendirilebilir** (şu an dev build 26.1.2'de sorunsuz çalışıyor, değişiklik gerekmedi).
- BeautyQuests 2.2.0+build.156 (alpha) denendi, locale NPE verdi; 2.1.0 release + JVM flag ile çalıştı.
- Hepsi ücretsiz. Ücretli plugin yok.

## Neden Yok Listesi

- Jobs Reborn — Yok. Gerekçe: AuraSkills dahili jobs geliri yeterli, ikinci jobs sistemi ekonomi dengesini bozar ve config yükü ekler.
- MythicMobs — Yok. Gerekçe: ücretli lisans gerektirir, 3 oyuncu için EliteMobs ücretsiz alternatif olarak yeterli.
- Citizens — Yok. Gerekçe: NPC ihtiyacı yok, questler BeautyQuests menü ile veriliyor.
- Towny — Yok. Gerekçe: GriefPrevention claim yeterli, 3 oyuncu için ulus/şehir sistemi gereksiz yük.
- Anti-cheat — Yok. Gerekçe: özel 3 kişilik sunucu, davranışsal güven esas. Şüphede log + admin incelemesi.
- Ayrı shop plugin — Yok. Gerekçe: EssentialsX `/sell` + sign shop yeterli.
- Ayrı backup plugin — Yok. Gerekçe: dosya tabanlı `scripts/backup.ps1` yeterli ve şeffaf.