# DGM Craft - Tum Komutlar

> **Not:** Turkce takma adlar ASCII'dir (c, g, s, o, u harfleri yok cunku Minecraft komutlari desteklemez). Ornek: `ev`, `evkur`, `yardim`, `gorevler`.
> Komutlarin kendileri (home, pay, kit...) Ingilizce kalir, degistirilemez.
> Sunucudaki **582 komutun tamami** (vanilla + admin dahil) `komutlar-tam.md` dosyasindadir.

## Hizli Takma Ad Listesi

`ev`=`/home` `evkur`=`/sethome` `evsil`=`/delhome` `para`=`/money` `ode`=`/pay` `sat`=`/sell hand` `deger`=`/worth` `zenginler`=`/balancetop` `kitler`=`/kits` `gorevler`=`/quests` `yetenek`=`/skills` `yardim`=`/help` `kurallar`=`/rules` `tamir`=`/repair` `calisma`=`/workbench` `pusula`=`/compass` `yakin`=`/near` `konum`=`/getpos` `tepe`=`/top` `sure`=`/playtime` `liste`=`/list` `warplar`=`/warp list`

---

## 1. Menu ve Ekranlar

| Komut | Ne ise yarar | Ornek |
|---|---|---|
| `/menu` | Ana dialog menusu (Kitler, Market, Nick, Gorevler, Yetenekler, Bilgi, Liderlik) | `/menu` |
| `F+Shift` | Tusa basarak menu acar | - |
| `/liderlik` | Sunucu siralamalari dialogu | `/liderlik` |
| `/shop` veya `/market` | Market alis ekrani | `/shop` |
| `/satis` | Esya satis ekrani | `/satis` |
| `/quests` | Gorev menusu (`gorevler`) | `/quests` |
| `/skills` | Yetenek menusu (`yetenek`) | `/skills` |
| `/pet` | Evcil hayvan menusu | `/pet` |
| `/petgift` | Baska oyuncuya pet hediye eder | `/petgift Ahmet` |
| `/ultracosmetics` | Sapka/efekt kozmetik menusu | `/ultracosmetics` |
| `/waypoint` | Isaret noktalari | `/waypoint` |
| `/mw` | Anit noktalari | `/mw` |
| `/gsit` | Otur/kalk | `/gsit` |
| `/glay` | Yere uzan | `/glay` |
| `/gspin` | Oldugun yerde don | `/gspin` |
| `/gcrawl` | Surun | `/gcrawl` |
| `/sb` | Scoreboard acar/kapatir | `/sb` |
| `/gecmis` | Son 100 log satiri (sadece sana gorunur) | `/gecmis` |
| `/odul` | Basina odul koyarsin, min 50 (parandan duser) | `/odul Ahmet 100` |
| `/cevrimici` | Kimler cevrimici gosterir | `/cevrimici` |
| `/zar` | Zar atarsin (eglence) | `/zar 100` |
| `/yazitura` | Yazi tura atarsin | `/yazitura` |
| `/plan ingame` | Kendi istatistigin | `/plan ingame` |

## 2. Ev ve Teleport

| Komut | Ne ise yarar | Ornek | Not |
|---|---|---|---|
| `/home` | Kayitli eve isinlar | `/home evim` | `ev`, 3sn bekleme |
| `/sethome` | Eve kaydedersin (en fazla 2) | `/sethome evim` | `evkur` |
| `/delhome` | Evi silersin | `/delhome evim` | `evsil` |
| `/spawn` | Dogus noktasina gidersin | `/spawn` | - |
| `/tpa` | Oyuncuya isinlanma istegi | `/tpa Ahmet` | - |
| `/tpaccept` | Istegi kabul eder | `/tpaccept` | - |
| `/tpdeny` | Istegi reddeder | `/tpdeny` | - |
| `/tpahere` | Oyuncuyu yanina cagirirsin | `/tpahere Ahmet` | - |
| `/back` | Olum/teleport oncesine donersin | `/back` | 30sn cooldown |
| `/top` | Yuzeye cikarsin | `/top` | `tepe` |
| `/warp` | Kayitli noktaya gidersin (5 para) | `/warp market` | - |
| `/trapped` | Claimde sikisirsan kurtarir | `/trapped` | - |

## 3. Ekonomi

| Komut | Ne ise yarar | Ornek | Not |
|---|---|---|---|
| `/money` veya `/balance` | Bakiyeni gosterir | `/money` | `para` |
| `/pay` | Oyuncuya para gonderirsin (min 1) | `/pay Ahmet 100` | `ode` |
| `/sell hand` | Elindekini satarsin | `/sell hand` | `sat` |
| `/worth` | Elindeki esyanin fiyatini gosterir | `/worth` | `deger` |
| `/balancetop` | En zenginler listesi | `/balancetop` | `zenginler` |
| `/kit <ad>` | Kit alirsin (ucretli) | `/kit madenci` | 15 kit, `/menu`de liste |
| `/kits` | Alinabilir kitler | `/kits` | `kitler` |
| `/showkit <ad>` | Kit icerigini onizlersin | `/showkit madenci` | - |
| `/repair` | Elindekini tamir eder (50 para) | `/repair` | `tamir` |

## 4. Gorev, Skill, Skor

| Komut | Ne ise yarar | Ornek |
|---|---|---|
| `/quests` | Gorev menusu | `/quests` |
| `/skills` | Yetenek agaci | `/skills` |
| `/rank` | Skill rutbeni gosterir | `/rank` |
| `/liderlik` | Zenginlik, avci, sure, guc, olum siralamalari | `/liderlik` |
| Bosslar | Komutsuz, dunyada dogar (Tier I-V) | - |

## 5. Claim ve Arsa

| Komut | Ne ise yarar | Ornek |
|---|---|---|
| Altin kurek + sag tik x2 | Claim olusturur | - |
| `/trust` (`/t`) | Yapim+acma izni verirsin | `/trust Ahmet` |
| `/untrust` (`/ut`) | Izni kaldirirsin | `/untrust Ahmet` |
| `/containertrust` (`/ct`) | Sandik/kapi izni | `/ct Ahmet` |
| `/accesstrust` (`/at`) | Giris/dugme izni | `/at Ahmet` |
| `/trustlist` | Guven listesi | `/trustlist` |
| `/abandonclaim` | Claimi silersin | `/abandonclaim` |
| `/claimlist` | Claimlerin | `/claimlist` |
| `/buyclaimblocks` | Blok satin alirsin | `/buyclaimblocks 100` |
| `/sellclaimblocks` | Blok satarsin | `/sellclaimblocks 50` |

## 6. Nick ve Gorunum

| Komut | Ne ise yarar | Ornek |
|---|---|---|
| `/nickyesil`, `/nickkirmizi`, `/nickmavi`, `/nickaltin`, `/nickmor`, `/nicksari` | Renkli nick yaparsin | `/nickyesil Kral` |
| `/nick off` | Nicki sifirlarsin | `/nick off` |
| `/skin <isim>` | Skinini degistirirsin | `/skin Notch` |
| `/hat` | Elindekini sapka yaparsin (eglence) | `/hat` |

## 7. Yardimci

| Komut | Ne ise yarar | Ornek |
|---|---|---|
| `/msg` | Ozel mesaj | `/msg Ahmet selam` (`/r` ile cevap) |
| `/mail send` | Cevrimdisi mesaj birakirsin | `/mail send Ahmet selam` |
| `/rules` | Kurallar (`kurallar`) | `/rules` |
| `/motd` | Karsilama mesaji | `/motd` |
| `/list` | Cevrimiciler (`liste`) | `/list` |
| `/near` | Yakindakiler (`yakin`) | `/near` |
| `/compass` | Yon (`pusula`) | `/compass` |
| `/getpos` | Konumun (`konum`) | `/getpos` |
| `/playtime` | Oynama suren (`sure`) | `/playtime` |
| `/ping` | Gecikmen | `/ping` |
| `/help` | Yardim (`yardim`) | `/help` |
| `/workbench` | Seyyar calisma masasi (`calisma`) | `/workbench` |

## 8. Admin (sadece admin/OP)

Bakim modu: ayri plugin yok. `whitelist on` acilir (yeni girisler engellenir), bitince `whitelist off`.

| Komut | Ne ise yarar |
|---|---|
| `/setspawn`, `/setwarp`, `/delwarp` | Spawn/warp yonetimi |
| `/eco`, `/setworth`, `/createkit` | Ekonomi yonetimi |
| `/gamemode`, `/give`, `/tp`, `/time`, `/weather`, `/ban`, `/kick`, `/op`, `/whitelist` | Klasik yonetim |
| `/save-all`, `/stop` | Kaydet/kapat |
| `/spark tps`, `/perfstatus`, `/lagpeek` | Performans |
| `/chunky ...` | Harita on-uretimi |
| `//wand` vb. | WorldEdit duzenleme |
| `/region ...` | WorldGuard bolge |
| `/lp ...` | LuckPerms yetki |
| `/plugman ...` | Plugin ac/kapa |
| `/km reload menu` | KaMenu yenileme |
| `/bq ...` | Quest yonetimi (GUI ile kurulum onerilir) |
| `/em ...` | Boss kurulumu (`/em place boss <dosya>`) |
| `/papi ...` | Placeholder islemleri |
| `/hologram ...` | FancyHolograms yonetimi |
| `/plan reload` | Plan yenileme |
