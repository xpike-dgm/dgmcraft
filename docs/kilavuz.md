# DGM Craft - Plugin Kategorilerine Gore Tam Kullanim Kilavuzu

Komutlar alfabetik degil, komutu saglayan plugin veya sistem kategorisine gore ayrilmistir.
Turkce yazilabilen oyuncu komutlari `DGM Craft Turkce Aliaslari (Skript)` bolumundedir. Her kayitta `Orjinal Komutu` satiri vardir.
ASCII komut adlari kullanilir: `c, g, i, o, s, u` karakterlerinin Turkce karsiliklari yerine Minecraft ile uyumlu ASCII adlar vardir.

## Kullanim Kurali
Oyuncu komutlari herkes icindir; Admin ve Teknik/Vanilla komutlari OP veya admin izni gerektirir. Dunya duzenleyen komutlardan once `scripts/backup.ps1` ile yedek al.

## 1-) DGM Craft Turkce Aliaslari (Skript)
Bu bolumdeki komutlar DGM Craft icin yazilmis Turkce kisayollardir. Her kayitta arkada calisan gercek komut acikca yazilidir.

### /anit
**Ne ise yarar:** Anit ve ozel noktalari gosterir. Haritada isaretli anitlara gitmeden once konum bakmak icin kullanilir.
**Ornek:** `/anit` (anıt nokta listesi acilir)
**Orjinal Komutu:** `/mw` — Skript ile bagli (dgm-turkce2.sk).


### /arsalarim
**Ne ise yarar:** Arsalarini ve kalan claim bloklarini listeler. Yeni claim icin yeterli blogun var mi gorursun.
**Ornek:** `/arsalarim` (tum arsalarin listelenir)
**Orjinal Komutu:** `/claimlist` — Skript ile bagli (dgm-turkce2.sk).


### /arsamsil
**Ne ise yarar:** Uzerinde durdugun arsayi siler. Once esyalari toplaman gerekir.
**Ornek:** `/arsamsil` (bulundugun claim silinir)
**Orjinal Komutu:** `/abandonclaim` — Skript ile bagli (dgm-turkce2.sk).


### /bacak
**Ne ise yarar:** Bacaklari havaya kaldirir (GSit eglence pozu).
**Ornek:** `/bacak` (poz verirsin)
**Orjinal Komutu:** `/glegsup` — Skript ile bagli (dgm-turkce3.sk).


### /bakiye
**Ne ise yarar:** Cuzdanindaki parayi gosterir. Oyuna 150 ile baslanir, maksimum 1000000'dir.
**Ornek:** `/bakiye` (bakiyeni gorursun)
**Orjinal Komutu:** `/money` — Skript ile bagli (dgm-turkce3.sk).


### /baliklama
**Ne ise yarar:** Baliklama atlama hareketi yapar.
**Ornek:** `/baliklama` (animasyon herkese gorunur)
**Orjinal Komutu:** `/gbellyflop` — Skript ile bagli (dgm-turkce3.sk).


### /bilgi
**Ne ise yarar:** Sunucu bilgisini ve tanitim yazisini gosterir.
**Ornek:** `/bilgi` (tanitimi okursun)
**Orjinal Komutu:** `/info` — Skript ile bagli (dgm-turkce3.sk).


### /blokal
**Ne ise yarar:** Parayla ek arsa blogu satin alirsin. Sayi argumani alir.
**Ornek:** `/blokal 100` (100 blok alirsin)
**Orjinal Komutu:** `/buyclaimblocks 100` — Skript ile bagli.


### /bloksat
**Ne ise yarar:** Fazla arsa bloklarini paraya cevirirsin.
**Ornek:** `/bloksat 50` (50 blogu satarsin)
**Orjinal Komutu:** `/sellclaimblocks 50` — Skript ile bagli.


### /bosta
**Ne ise yarar:** AFK durumunu acar kapatir.
**Ornek:** `/bosta` (listede AFK gorunursun, tekrar yazinca kapanir)
**Orjinal Komutu:** `/afk` — Skript ile bagli (dgm-turkce3.sk).


### /cagir
**Ne ise yarar:** Oyuncuyu yanina cagirirsin (ondan sana isinlanmasini istersin). Birlikte maden veya insaat yaparken kullanilir.
**Ornek:** `/cagir Ahmet` (Ahmet kabul ederse yanina isinlanir)
**Orjinal Komutu:** `/tpahere Ahmet` — Skript ile bagli (dgm-turkce2.sk).


### /calisma
**Ne ise yarar:** Oldugun yerde seyyar calisma masasi acar. Madendeyken craft icin idealdir.
**Ornek:** `/calisma` (uretim menusu acilir)
**Orjinal Komutu:** `/workbench` — Skript ile bagli (dgm-turkce2.sk).


### /cevap
**Ne ise yarar:** Sana en son mesaj atan kisiye hizli cevap verirsin.
**Ornek:** `/cevap tamam geliyorum` (son yazana gider)
**Orjinal Komutu:** `/r tamam` — Skript ile bagli (dgm-turkce3.sk).


### /cevrimici
**Ne ise yarar:** Kimlerin cevrimici oldugunu sayi ve isimle gosterir.
**Ornek:** `/cevrimici` (listeyi gorursun)
**Orjinal Komutu:** `/cevrimici` — ozgun Skript komutu (dgm-turkce.sk).


### /cop
**Ne ise yarar:** Sanal cop kutusu acar, icine attigin esya silinir. Maden sonrasi cop bloklari temizlemek icindir.
**Ornek:** `/cop` (cop menusu acilir)
**Orjinal Komutu:** `/disposal` — Skript ile bagli (dgm-turkce3.sk).


### /deger
**Ne ise yarar:** Elindekinin satis fiyatini gosterir (demir 8, elmas 50, odun 1, komur 2, altin 12, zumrut 60). Blok halleri ve ciftlik urunlerinde satis kapalidir.
**Ornek:** `/deger` (elindeki demirin 8 oldugunu gorursun)
**Orjinal Komutu:** `/worth` — Skript ile bagli (dgm-turkce2.sk).


### /dogum
**Ne ise yarar:** Dogus noktasina gider. Kaybolunca merkeze donmek icindir.
**Ornek:** `/dogum` (spawna isinlanirsin)
**Orjinal Komutu:** `/spawn` — Skript ile bagli (dgm-turkce2.sk).


### /don
**Ne ise yarar:** Onceki konumuna doner (`/back` ile ayni, 30sn cooldown).
**Ornek:** `/don` (olum noktasina donup esyalari toplarsin)
**Orjinal Komutu:** `/back` — Skript ile bagli (dgm-turkce2.sk).


### /donme
**Ne ise yarar:** Kendi etrafinda donersin (GSit animasyonu).
**Ornek:** `/donme` (animasyon herkese gorunur)
**Orjinal Komutu:** `/gspin` — Skript ile bagli (dgm-turkce3.sk).


### /ev
**Ne ise yarar:** Kaydettigin evine isinlanirsin. 3sn bekleme ve 10sn cooldown vardir, en fazla 2 ev kaydedilir.
**Ornek:** `/ev evim` (evine isinlanirsin) ; `/ev maden` (maden evine gidersin)
**Orjinal Komutu:** `/home evim` — Skript ile bagli (dgm-turkce2.sk).


### /evad
**Ne ise yarar:** Kayitli evinin adini degistirir.
**Ornek:** `/evad evim yeniev` (adi degisir)
**Orjinal Komutu:** `/renamehome evim yeniev` — Skript ile bagli (dgm-turkce3.sk).


### /evcil
**Ne ise yarar:** Evcil hayvan menusunu acar, petini cagirirsin.
**Ornek:** `/evcil` (pet menusu acilir)
**Orjinal Komutu:** `/pet` — Skript ile bagli (dgm-turkce2.sk).


### /evkur
**Ne ise yarar:** Bulundugun yeri ev noktasi olarak kaydedersin (en fazla 2).
**Ornek:** `/evkur evim` (burayi kaydedersin)
**Orjinal Komutu:** `/sethome evim` — Skript ile bagli (dgm-turkce2.sk).


### /evsil
**Ne ise yarar:** Ev kaydini siler.
**Ornek:** `/evsil evim` (kayit silinir)
**Orjinal Komutu:** `/delhome evim` — Skript ile bagli (dgm-turkce2.sk).


### /eylem
**Ne ise yarar:** Eylem mesaji gonderir (ucuncu sahis gibi gorunur).
**Ornek:** `/eylem madene iniyor` (herkes gorur)
**Orjinal Komutu:** `/me madene iniyor` — Skript ile bagli (dgm-turkce2.sk).


### /fiyat
**Ne ise yarar:** Elindekinin market fiyatini gosterir (GUIShop degeri).
**Ornek:** `/fiyat` (degeri gorursun)
**Orjinal Komutu:** `/value` — Skript ile bagli (dgm-turkce3.sk).


### /gecikme
**Ne ise yarar:** Sunucuya gecikmeni ms olarak gosterir.
**Ornek:** `/gecikme` (kac ms oldugunu gorursun)
**Orjinal Komutu:** `/ping` — Skript ile bagli (dgm-turkce3.sk).


### /gercekad
**Ne ise yarar:** Renkli takma ad kullananin gercek adini gosterir.
**Ornek:** `/gercekad Kral` (gercek ismi gorursun)
**Orjinal Komutu:** `/realname Kral` — Skript ile bagli (dgm-turkce2.sk).


### /girisizni
**Ne ise yarar:** Arsana kapi-dugme kullanma izni verir. Turkcesi accesstrust karsiligidir.
**Ornek:** `/girisizni Ahmet` (kapilari kullanabilir)
**Orjinal Komutu:** `/accesstrust Ahmet` — Skript ile bagli (dgm-turkce2.sk).


### /gorevler
**Ne ise yarar:** Yapabilecegin ve devam eden gorevleri gosterir (oduller 50-250 arasi).
**Ornek:** `/gorevler` (menuyu acarsin)
**Orjinal Komutu:** `/quests` — Skript ile bagli (dgm-turkce2.sk).


### /gorunum
**Ne ise yarar:** Gorunumunu degistirir (SkinsRestorer).
**Ornek:** `/gorunum Notch` (skinin degisir)
**Orjinal Komutu:** `/skin Notch` — Skript ile bagli (dgm-turkce2.sk).


### /goster
**Ne ise yarar:** Kit icerigini satin almadan onizlersin (15 kit fiyatlari kilavuzda).
**Ornek:** `/goster madenci` (200'luk seti onizlersin)
**Orjinal Komutu:** `/showkit madenci` — Skript ile bagli (dgm-turkce2.sk).


### /guven
**Ne ise yarar:** Arsana tam yetki verir (insa+kullanim). Ortak ev yaparken kullanilir.
**Ornek:** `/guven Ahmet` (Ahmet arsana ev yapabilir)
**Orjinal Komutu:** `/trust Ahmet` — Skript ile bagli (dgm-turkce2.sk).


### /guvenkaldir
**Ne ise yarar:** Arsa yetkisini geri alir.
**Ornek:** `/guvenkaldir Ahmet` (yetkisi silinir)
**Orjinal Komutu:** `/untrust Ahmet` — Skript ile bagli (dgm-turkce2.sk).


### /guvenlistesi
**Ne ise yarar:** Arsa yetkilerini listeler.
**Ornek:** `/guvenlistesi` (kim yetkili gorursun)
**Orjinal Komutu:** `/trustlist` — Skript ile bagli (dgm-turkce3.sk).


### /havam
**Ne ise yarar:** Sadece senin gordugun havayi degistirir.
**Ornek:** `/havam acik` (yagmur durur)
**Orjinal Komutu:** `/pweather clear` — Skript ile bagli (dgm-turkce3.sk).


### /hediye
**Ne ise yarar:** Petini baska oyuncuya hediye eder.
**Ornek:** `/hediye Ahmet` (petin gider)
**Orjinal Komutu:** `/petgift Ahmet` — Skript ile bagli (dgm-turkce2.sk).


### /kabul
**Ne ise yarar:** Sana gelen isinlanma istegi kabul eder.
**Ornek:** `/kabul` (isteyen yanina gelir)
**Orjinal Komutu:** `/tpaccept` — Skript ile bagli (dgm-turkce2.sk).


### /kitler
**Ne ise yarar:** Alinabilir kit listesini gosterir.
**Ornek:** `/kitler` (15 kiti gorursun)
**Orjinal Komutu:** `/kits` — Skript ile bagli (dgm-turkce3.sk).


### /konum
**Ne ise yarar:** Bulundugun koordinatlari gosterir.
**Ornek:** `/konum` (maden koordinatini kopyalarsin)
**Orjinal Komutu:** `/getpos` — Skript ile bagli (dgm-turkce2.sk).


### /kozmetik
**Ne ise yarar:** Sapka ve efekt menusunu acar.
**Ornek:** `/kozmetik` (kozmetik secersin)
**Orjinal Komutu:** `/ultracosmetics` — Skript ile bagli (dgm-turkce2.sk).


### /kurallar
**Ne ise yarar:** Sunucu kurallarini gosterir.
**Ornek:** `/kurallar` (kurallari okursun)
**Orjinal Komutu:** `/rules` — Skript ile bagli (dgm-turkce2.sk).


### /liste
**Ne ise yarar:** Cevrimici listesini Turkce adla acar.
**Ornek:** `/liste` (kimler oyunda gorursun)
**Orjinal Komutu:** `/list` — Skript ile bagli (dgm-turkce2.sk).


### /mesaj
**Ne ise yarar:** Bir oyuncuya ozel mesaj gonderir, sadece alici gorur. Cevabi `/cevap` ve `/r` iledir.
**Ornek:** `/mesaj Ahmet selam` (sadece Ahmet'e gider)
**Orjinal Komutu:** `/msg Ahmet selam` — Skript ile bagli (dgm-turkce2.sk).


### /mesajkapat
**Ne ise yarar:** Ozel mesajlari kapatip acar (spam korumasi).
**Ornek:** `/mesajkapat` (kimse atamaz olur) ; tekrar yazinca acilir
**Orjinal Komutu:** `/msgtoggle` — Skript ile bagli (dgm-turkce3.sk).


### /mezar
**Ne ise yarar:** Olumde dusen esyani 5 dakika icinde almak icin mezarina isinlanir.
**Ornek:** `/mezar` (olum noktasina gidersin)
**Orjinal Komutu:** `/grave` — Skript ile bagli (dgm-turkce2.sk).


### /karsilama
**Ne ise yarar:** Karsilama mesajini gosterir.
**Ornek:** `/karsilama` (duyuruyu okursun)
**Orjinal Komutu:** `/motd` — Skript ile bagli (dgm-turkce3.sk).


### /nokta
**Ne ise yarar:** Kayitli warp noktasina gider (ucret 5, 3sn bekleme).
**Ornek:** `/nokta market` (markete gidersin)
**Orjinal Komutu:** `/warp market` — Skript ile bagli (dgm-turkce3.sk).


### /noktabilgi
**Ne ise yarar:** Bir warpin nerede oldugunu gosterir, yanlis warpi onler.
**Ornek:** `/noktabilgi market` (konum gosterilir)
**Orjinal Komutu:** `/warpinfo market` — Skript ile bagli (dgm-turkce3.sk).


### /ode
**Ne ise yarar:** Baskasina parandan gonderirsin (min 1, 10sn cooldown, max 1000000). Ticaret ve bounty odemesi bununla yapilir.
**Ornek:** `/ode Ahmet 50` (Ahmet'e 50 gider)
**Orjinal Komutu:** `/pay Ahmet 50` — Skript ile bagli (dgm-turkce2.sk).


### /odemekapat
**Ne ise yarar:** Baskalarinin sana para gondermesini acar kapatir.
**Ornek:** `/odemekapat` (kimse gonderemez, tekrar yazinca acilir)
**Orjinal Komutu:** `/paytoggle` — Skript ile bagli (dgm-turkce3.sk).


### /odul
**Ne ise yarar:** Bir oyuncunun basina odul koyar (min 50, bakiyenden duser, herkese duyurulur). Kendine koyamazsin.
**Ornek:** `/odul Ahmet 100` (100 paran gider, duyurulur)
**Orjinal Komutu:** `/odul` — ozgun Skript komutu (Vault bakiye duser).


### /ol
**Ne ise yarar:** Oldurur, esyalarin yerinde duser (blok icine sikisinca kurtulma icindir, 5dkda alinmalidir).
**Ornek:** `/ol` (olur ve dogarsin)
**Orjinal Komutu:** `/suicide` — Skript ile bagli (dgm-turkce2.sk).


### /otokabul
**Ne ise yarar:** Gelen isinlanma isteklerini otomatik kabul eder. `/istekkapat` tersidir.
**Ornek:** `/otokabul` (istekler sormadan kabul edilir)
**Orjinal Komutu:** `/tpauto` — Skript ile bagli (dgm-turkce3.sk).


### /otur
**Ne ise yarar:** Oldugun yere oturtur, tekrar yazinca kaldirir.
**Ornek:** `/otur` (oturursun)
**Orjinal Komutu:** `/gsit` — Skript ile bagli (dgm-turkce2.sk).


### /ozellik
**Ne ise yarar:** Guc-saglik gibi stat ozelliklerini gosterir.
**Ornek:** `/ozellik` (stat menusu acilir)
**Orjinal Komutu:** `/stats` — Skript ile bagli (dgm-turkce3.sk).


### /para
**Ne ise yarar:** Cuzdanindaki parayi gosterir (baslangic 150, max 1000000). Gelir `/sat`-jobs-gorevle artar.
**Ornek:** `/para` (bakiyen gorulur)
**Orjinal Komutu:** `/money` — Skript ile bagli (dgm-turkce2.sk).


### /pazar
**Ne ise yarar:** Market alis menusunu acar (Bloklar, Yemek, Savas, Aletler). Sadece alis vardir (~5x vergili), satis `/satis` ile ayridir.
**Ornek:** `/pazar` (menu acilir) ; Yemek secimi (ekmek alinir)
**Orjinal Komutu:** `/shop` — Skript ile bagli (dgm-turkce2.sk).


### /posta
**Ne ise yarar:** Gelen cevrimdisi postayi okur.
**Ornek:** `/posta` (mesajlari gorursun)
**Orjinal Komutu:** `/mail read` — Skript ile bagli (dgm-turkce2.sk).


### /postagonder
**Ne ise yarar:** Cevrimdisi oyuncuya mesaj birakir (oyuncu+mesaj zorunlu).
**Ornek:** `/postagonder Ahmet selam` (Ahmet girince okur)
**Orjinal Komutu:** `/mail send Ahmet selam` — Skript ile bagli (dgm-turkce3.sk).


### /pusula
**Ne ise yarar:** Baktigin yonu gosterir (kasif kitiyle baglantili).
**Ornek:** `/pusula` (yonun gosterilir)
**Orjinal Komutu:** `/compass` — Skript ile bagli (dgm-turkce2.sk).


### /rastgele
**Ne ise yarar:** Rastgele araziye isinlanirsin (claimsiz vahsi alan).
**Ornek:** `/rastgele` (bilinmedik yere gidersin)
**Orjinal Komutu:** `/tpr` — Skript ile bagli (dgm-turkce3.sk).


### /red
**Ne ise yarar:** Gelen isinlanma istegi reddeder.
**Ornek:** `/red` (son istek reddedilir)
**Orjinal Komutu:** `/tpdeny` — Skript ile bagli (dgm-turkce2.sk).


### /rutbe
**Ne ise yarar:** Skill siralamadaki yerini gosterir.
**Ornek:** `/rutbe` (siran gorulur, kasinca yukselir)
**Orjinal Komutu:** `/rank` — Skript ile bagli (dgm-turkce3.sk).


### /sandikizni
**Ne ise yarar:** Birine sandik-firin kullanma izni verir (insa vermeden depo paylasirsin).
**Ornek:** `/sandikizni Ahmet` (sandiklari acabilir)
**Orjinal Komutu:** `/containertrust Ahmet` — Skript ile bagli (dgm-turkce2.sk).


### /sapka
**Ne ise yarar:** Elindeki esyayi kafana sapka yaparsin.
**Ornek:** `/sapka` (blok kafana takilir)
**Orjinal Komutu:** `/hat` — Skript ile bagli (dgm-turkce3.sk).


### /sat
**Ne ise yarar:** Elindekini worth fiyatiyla satarsin (demir 8, elmas 50, odun 1, komur 2).
**Ornek:** `/sat` (demir satilir, bakiye artar)
**Orjinal Komutu:** `/sell hand` — Skript ile bagli (dgm-turkce2.sk).


### /saatim
**Ne ise yarar:** Sadece senin saatini degistirir.
**Ornek:** `/saatim gun` (ekranin gunduz olur)
**Orjinal Komutu:** `/ptime gun` — Skript ile bagli (dgm-turkce3.sk).


### /skortablo
**Ne ise yarar:** Skor tablosunu acar kapatir.
**Ornek:** `/skortablo` (gorunum degisir)
**Orjinal Komutu:** `/sb` — Skript ile bagli (dgm-turkce2.sk).


### /sure
**Ne ise yarar:** Toplam oyun sureni gosterir.
**Ornek:** `/sure` (kac saat gorursun)
**Orjinal Komutu:** `/playtime` — Skript ile bagli (dgm-turkce2.sk).


### /surun
**Ne ise yarar:** Surunme pozu alirsin.
**Ornek:** `/surun` (tunelde poz verirsin)
**Orjinal Komutu:** `/gcrawl` — Skript ile bagli (dgm-turkce2.sk).


### /tamir
**Ne ise yarar:** Elindekini onarir (karsiligi 50, ors/villager masrafina alternatif).
**Ornek:** `/tamir` (kazma tamir olur, 50 gider)
**Orjinal Komutu:** `/repair` — Skript ile bagli (dgm-turkce2.sk).


### /tarif
**Ne ise yarar:** Esya tarifini gosterir.
**Ornek:** `/tarif mesale` (tarif acilir)
**Orjinal Komutu:** `/recipe mesale` — Skript ile bagli (dgm-turkce2.sk).


### /tepe
**Ne ise yarar:** En ust bloga isinlar (madende yeryuzune cikarir).
**Ornek:** `/tepe` (yukari isinlanirsin)
**Orjinal Komutu:** `/essentials:top` — Skript ile bagli (dgm-turkce2.sk).


### /tumcagir
**Ne ise yarar:** Herkese isinlanma istegi gonderirsin.
**Ornek:** `/tumcagir` (arenada oyunculari cagirirsin)
**Orjinal Komutu:** `/tpaall` — Skript ile bagli (dgm-turkce3.sk).


### /uzan
**Ne ise yarar:** Yere uzanirsin (dinlenme/fotograf pozu).
**Ornek:** `/uzan` (uzanirsin, tekrar yazinca kalkarsin)
**Orjinal Komutu:** `/glay` — Skript ile bagli (dgm-turkce2.sk).


### /yardim
**Ne ise yarar:** Kullanabilecegin komutlari sayfa sayfa gosterir.
**Ornek:** `/yardim` (yardimi acarsin)
**Orjinal Komutu:** `/help` — Skript ile bagli (dgm-turkce2.sk).


### /yakin
**Ne ise yarar:** Yakindakileri listeler.
**Ornek:** `/yakin` (cevrede kim var gorursun)
**Orjinal Komutu:** `/near` — Skript ile bagli (dgm-turkce2.sk).


### /yazitura
**Ne ise yarar:** Yazi tura atar, sonucu herkese duyurur (eglence/kura).
**Ornek:** `/yazitura` (YAZI/TURA duyurulur)
**Orjinal Komutu:** `/yazitura` — ozgun Skript komutu (dgm-turkce.sk).


### /yetenek
**Ne ise yarar:** 11 yetenek menusunu acar (jobs ~0.05/XP, en fazla 2 job).
**Ornek:** `/yetenek` (seviyeler gorulur)
**Orjinal Komutu:** `/skills` — Skript ile bagli (dgm-turkce2.sk).


### /yetenekskor
**Ne ise yarar:** Yetenek liderlerini gosterir.
**Ornek:** `/yetenekskor` (en iyiler gorulur)
**Orjinal Komutu:** `/auraskills:top` — Skript ile bagli (dgm-turkce3.sk).


### /yetkili
**Ne ise yarar:** Cevrimici yetkililere yardim mesaji gonderir.
**Ornek:** `/yetkili evde sikistim` (mesajin gider)
**Orjinal Komutu:** `/helpop mesaj` — Skript ile bagli (dgm-turkce3.sk).


### /yoksay
**Ne ise yarar:** Oyuncuyu yoksayar, mesajlarini gizler.
**Ornek:** `/yoksay Ahmet` (spam engellenir)
**Orjinal Komutu:** `/ignore Ahmet` — Skript ile bagli (dgm-turkce2.sk).


### /isaret
**Ne ise yarar:** Kayitli beacon waypoint noktalarini acar ve nokta secerek yolunu bulmana yardim eder.
**Ornek:** `/isaret` (kayitli isaretleri gorursun)
**Orjinal Komutu:** `/waypoint` — Skript ile bagli (dgm-turkce2.sk).


### /istatistik
**Ne ise yarar:** Kendi oyun suresi, aktivite ve istatistiklerini Plan ekraninda gosterir.
**Ornek:** `/istatistik` (oyun istatistiklerini acarsin)
**Orjinal Komutu:** `/plan ingame` — Skript ile bagli (dgm-turkce2.sk).


### /istek
**Ne ise yarar:** Bir oyuncuya isinlanma istegi gonderir; karsi taraf `/kabul` veya `/red` ile cevaplar.
**Ornek:** `/istek Ahmet` (Ahmet'e istek gider)
**Orjinal Komutu:** `/tpa Ahmet` — Skript ile bagli (dgm-turkce2.sk).


### /istekkapat
**Ne ise yarar:** Sana teleport istegi gelmesini acar veya kapatir.
**Ornek:** `/istekkapat` (istek alimi kapanir, tekrar yazinca acilir)
**Orjinal Komutu:** `/tptoggle` — Skript ile bagli (dgm-turkce3.sk).


### /warplar
**Ne ise yarar:** Sunucudaki kullanilabilir warp noktalarini listeler. Warp kullanimi 5 para ve 3 saniye bekleme ile calisir.
**Ornek:** `/warplar` (warp listesini gorursun)
**Orjinal Komutu:** `/warp list` — Skript ile bagli (dgm-turkce2.sk).


### /zar
**Ne ise yarar:** Zar atar (varsayilan 100 yuzlu, 1-1000 arasi secilir, sonucu duyurulur).
**Ornek:** `/zar 100` (1-100 arasi atar) ; `/zar 6` (klasik zar)
**Orjinal Komutu:** `/zar` — ozgun Skript komutu (dgm-turkce.sk).


### /zenginler
**Ne ise yarar:** Vault ekonomisine gore en zengin oyunculari siralar.
**Ornek:** `/zenginler` (ilk siradakileri gorursun)
**Orjinal Komutu:** `/balancetop` — Skript ile bagli (dgm-turkce2.sk ve dgm-turkce3.sk).


## 2-) EssentialsX
Ev, isinlanma, sohbet, ekonomi, kit ve genel oyuncu komutlari.

### /back
**Ne ise yarar:** Olmeden onceki yerine ya da son isinlanmadan onceki konumuna doner. Cooldown 30sn'dir.
**Ornek:** `/back` (olum noktasina isinlanirsin)
**Orjinal Komutu:** `/back` — dogrudan Essentials komutu. Turkcesi: `/don`.


### /balance
**Ne ise yarar:** Bakiyeyi gosterir. Turkce karsiliklari `/para` ve `/bakiye`.
**Ornek:** `/balance` (bakiyeni gorursun)
**Orjinal Komutu:** `/balance` — dogrudan Essentials komutu.


### /balancetop
**Ne ise yarar:** En zengin oyunculari siralar.
**Ornek:** `/balancetop` (liste acilir) ; `/balancetop 2` (ikinci sayfa)
**Orjinal Komutu:** `/balancetop` — dogrudan Essentials komutu. Turkcesi: `/zenginler`.


### /compass
**Ne ise yarar:** Baktigin yonu gosterir. Turkcesi `/pusula`.
**Ornek:** `/compass` (yonunu gorursun)
**Orjinal Komutu:** `/compass` — dogrudan Essentials komutu.


### /delhome
**Ne ise yarar:** Kaydettigin ev noktasini siler. Turkcesi `/evsil`.
**Ornek:** `/delhome evim` (kayit silinir)
**Orjinal Komutu:** `/delhome` — dogrudan Essentials komutu.


### /disposal
**Ne ise yarar:** Sanal cop kutusu acar. Turkcesi `/cop`.
**Ornek:** `/disposal` (menuyu acip esya silersin)
**Orjinal Komutu:** `/disposal` — dogrudan Essentials komutu.


### /getpos
**Ne ise yarar:** Bulundugun koordinatlari gosterir. Turkcesi `/konum`.
**Ornek:** `/getpos` (x, y, z gorursun)
**Orjinal Komutu:** `/getpos` — dogrudan Essentials komutu.


### /hat
**Ne ise yarar:** Elindeki esyayi kafana sapka olarak takar. Turkcesi `/sapka`.
**Ornek:** `/hat` (elindeki blogu kafana takarsin)
**Orjinal Komutu:** `/hat` — dogrudan Essentials komutu.


### /help
**Ne ise yarar:** Kullanabilecegin komutlari sayfa sayfa gosterir. Turkcesi `/yardim`.
**Ornek:** `/help` (yardimi acarsin)
**Orjinal Komutu:** `/help` — dogrudan Essentials komutu.


### /helpop
**Ne ise yarar:** Cevrimici yetkililere yardim mesaji gonderir. Turkcesi `/yetkili`.
**Ornek:** `/helpop evimde sikistim` (mesajin gider)
**Orjinal Komutu:** `/helpop` — dogrudan Essentials komutu.


### /ignore
**Ne ise yarar:** Istedigin oyuncunun mesajlarini gizler.
**Ornek:** `/ignore Ahmet` (mesajlarini gormezsin)
**Orjinal Komutu:** `/ignore` — dogrudan Essentials komutu.


### /kit
**Ne ise yarar:** Hazir esya setlerini parayla alirsin (15 kit: baslangic ucretsiz tek seferlik, gunluk 100-250, nether 400/3gun, haftalik 150-500).
**Ornek:** `/kit madenci` (200 karsiligi seti alirsin)
**Orjinal Komutu:** `/kit` — dogrudan Essentials komutu.


### /list
**Ne ise yarar:** Cevrimici oyunculari ve sayisini listeler. Turkcesi `/liste`.
**Ornek:** `/list` (orn. 3 oyuncu listelenir)
**Orjinal Komutu:** `/list` — dogrudan Essentials komutu.


### /mail
**Ne ise yarar:** Cevrimdisiyken sana birakilan postayi okursun (`mail read`).
**Ornek:** `/mail read` (gelen postalari listelersin)
**Orjinal Komutu:** `/mail` — dogrudan Essentials komutu.


### /mail send
**Ne ise yarar:** Cevrimdisi oyuncuya mesaj birakirsin, girince okur.
**Ornek:** `/mail send Ahmet selam` (Ahmet girince okur)
**Orjinal Komutu:** `/mail send` — dogrudan Essentials komutu.


### /me
**Ne ise yarar:** Ucuncu sahis gibi eylem mesaji gonderir. Turkcesi `/eylem`.
**Ornek:** `/me madene iniyor` (herkes gorur)
**Orjinal Komutu:** `/me` — dogrudan Essentials komutu.


### /motd
**Ne ise yarar:** Gunun mesajini ve karsilama yazisini tekrar gosterir. Turkcesi `/karsilama`.
**Ornek:** `/motd` (giris mesajini gorursun)
**Orjinal Komutu:** `/motd` — dogrudan Essentials komutu.


### /msg
**Ne ise yarar:** Ozel mesaj gonderir, genel sohbete dusmez. Cevabi `/r` iledir.
**Ornek:** `/msg Ahmet selam` (sadece Ahmet gorur)
**Orjinal Komutu:** `/msg` — dogrudan Essentials komutu.


### /msgtoggle
**Ne ise yarar:** Ozel mesaj alimini engeller ya da acar. Turkcesi `/mesajkapat`.
**Ornek:** `/msgtoggle` (sessize alirsin)
**Orjinal Komutu:** `/msgtoggle` — dogrudan Essentials komutu.


### /near
**Ne ise yarar:** Yakindaki oyunculari ve mesafelerini listeler. Turkcesi `/yakin`.
**Ornek:** `/near` (cevrede kim var gorursun)
**Orjinal Komutu:** `/near` — dogrudan Essentials komutu.


### /nick renkleri
**Ne ise yarar:** Sohbette gorunen adini renklendirirsin: `/nickyesil`, `/nickkirmizi`, `/nickmavi`, `/nickaltin`, `/nickmor`, `/nicksari`. Sifirlama `/nick off` iledir, gercek ad `/gercekad` ile bulunur.
**Ornek:** `/nickyesil Kral` (adin yesil Kral olur)
**Orjinal Komutu:** `/nick &2Kral` — Bukkit takma adlari (commands.yml).


### /pay
**Ne ise yarar:** Baskasina parandan gonderirsin (min 1, 10sn cooldown). Turkcesi `/ode`.
**Ornek:** `/pay Ahmet 50` (gonderirsin)
**Orjinal Komutu:** `/pay` — dogrudan Essentials komutu.


### /payconfirmtoggle
**Ne ise yarar:** Para gonderirken onay sorulup sorulmayacagini degistirir.
**Ornek:** `/payconfirmtoggle` (onay acilir/kapanir)
**Orjinal Komutu:** `/payconfirmtoggle` — dogrudan Essentials komutu.


### /paytoggle
**Ne ise yarar:** Baskalarinin sana para gondermesini acar kapatir. Turkcesi `/odemekapat`.
**Ornek:** `/paytoggle` (alim kapanir/acilir)
**Orjinal Komutu:** `/paytoggle` — dogrudan Essentials komutu.


### /ping
**Ne ise yarar:** Gecikmeni ms olarak gosterir. Turkcesi `/gecikme`.
**Ornek:** `/ping` (degeri gorursun)
**Orjinal Komutu:** `/ping` — dogrudan Essentials komutu.


### /playtime
**Ne ise yarar:** Toplam oyun sureni gosterir. Turkcesi `/sure`.
**Ornek:** `/playtime` (kac saat gorursun)
**Orjinal Komutu:** `/playtime` — dogrudan Essentials komutu.


### /ptime
**Ne ise yarar:** Sadece senin gordugun oyun saatini degistirir. Turkcesi `/saatim`.
**Ornek:** `/ptime day` (ekranin gunduz olur)
**Orjinal Komutu:** `/ptime` — dogrudan Essentials komutu.


### /pweather
**Ne ise yarar:** Sadece senin gordugun havayi degistirir. Turkcesi `/havam`.
**Ornek:** `/pweather clear` (yagmur durur)
**Orjinal Komutu:** `/pweather` — dogrudan Essentials komutu.


### /r
**Ne ise yarar:** Sana en son mesaj atana hizli cevap verirsin. Turkcesi `/cevap`.
**Ornek:** `/r tamam geliyorum` (son yazana gider)
**Orjinal Komutu:** `/r` — dogrudan Essentials komutu.


### /realname
**Ne ise yarar:** Renkli nicklinin gercek adini gosterir. Turkcesi `/gercekad`.
**Ornek:** `/realname Kral` (gercek ad gorulur)
**Orjinal Komutu:** `/realname` — dogrudan Essentials komutu.


### /renamehome
**Ne ise yarar:** Kayitli evin adini degistirir (ev limiti 2). Turkcesi `/evad`.
**Ornek:** `/renamehome evim yeniev` (adi degisir)
**Orjinal Komutu:** `/renamehome` — dogrudan Essentials komutu.


### /repair
**Ne ise yarar:** Elindekini onarir (karsiligi 50). Turkcesi `/tamir`.
**Ornek:** `/repair` (kazma tamir olur, 50 gider)
**Orjinal Komutu:** `/repair` — dogrudan Essentials komutu.


### /rules
**Ne ise yarar:** Sunucu kurallarini gosterir. Turkcesi `/kurallar`.
**Ornek:** `/rules` (kurallari okursun)
**Orjinal Komutu:** `/rules` — dogrudan Essentials komutu.


### /sethome
**Ne ise yarar:** Bulundugun yeri ev noktasi olarak kaydedersin (en fazla 2). Turkcesi `/evkur`.
**Ornek:** `/sethome evim` (burayi kaydedersin)
**Orjinal Komutu:** `/sethome` — dogrudan Essentials komutu.


### /showkit
**Ne ise yarar:** Kit icerigini satin almadan onizlersin. Turkcesi `/goster`.
**Ornek:** `/showkit madenci` (200'luk seti gorursun)
**Orjinal Komutu:** `/showkit` — dogrudan Essentials komutu.


### /spawn
**Ne ise yarar:** Baslangic noktasina isinlanirsin. Turkcesi `/dogum`.
**Ornek:** `/spawn` (merkeze gidersin)
**Orjinal Komutu:** `/spawn` — dogrudan Essentials komutu.


### /suicide
**Ne ise yarar:** Oldurur, esyalarin yerinde duser. Turkcesi `/ol`.
**Ornek:** `/suicide` (olusup dogarsin)
**Orjinal Komutu:** `/suicide` — dogrudan Essentials komutu.


### /top
**Ne ise yarar:** En ust bloga isinlar. Turkcesi `/tepe`.
**Ornek:** `/top` (madendeysen cikarsin)
**Orjinal Komutu:** `/top` — dogrudan Essentials komutu.


### /tpa
**Ne ise yarar:** Bir oyuncuya isinlanma istegi gonderirsin. Turkcesi `/istek`.
**Ornek:** `/tpa Ahmet` (istegin gider)
**Orjinal Komutu:** `/tpa` — dogrudan Essentials komutu.


### /tpaall
**Ne ise yarar:** Herkese isinlanma istegi gonderirsin. Turkcesi `/tumcagir`.
**Ornek:** `/tpaall` (etkinlikte toplarsin)
**Orjinal Komutu:** `/tpaall` — dogrudan Essentials komutu.


### /tpaccept
**Ne ise yarar:** Gelen istegi kabul edersin. Turkcesi `/kabul`.
**Ornek:** `/tpaccept` (isteyen yanina gelir)
**Orjinal Komutu:** `/tpaccept` — dogrudan Essentials komutu.


### /tpacancel
**Ne ise yarar:** Gonderdigin istegi iptal edersin.
**Ornek:** `/tpacancel` (yanlis isimde geri cekersin)
**Orjinal Komutu:** `/tpacancel` — dogrudan Essentials komutu.


### /tpahere
**Ne ise yarar:** Bir oyuncudan sana isinlanmasini istersin. Turkcesi `/cagir`.
**Ornek:** `/tpahere Ahmet` (cagrin gider)
**Orjinal Komutu:** `/tpahere` — dogrudan Essentials komutu.


### /tpauto
**Ne ise yarar:** Gelen istekleri otomatik kabul eder. Turkcesi `/otokabul`.
**Ornek:** `/tpauto` (sormadan kabul edilir)
**Orjinal Komutu:** `/tpauto` — dogrudan Essentials komutu.


### /tpdeny
**Ne ise yarar:** Gelen istegi reddeder. Turkcesi `/red`.
**Ornek:** `/tpdeny` (son istek reddedilir)
**Orjinal Komutu:** `/tpdeny` — dogrudan Essentials komutu.


### /tpr
**Ne ise yarar:** Rastgele araziye isinlanirsin. Turkcesi `/rastgele`.
**Ornek:** `/tpr` (bilinmedik yere gidersin)
**Orjinal Komutu:** `/tpr` — dogrudan Essentials komutu.


### /tptoggle
**Ne ise yarar:** Sana istek gelmesini engeller. Turkcesi `/istekkapat`.
**Ornek:** `/tptoggle` (kimse atamaz, tekrar yazinca acilir)
**Orjinal Komutu:** `/tptoggle` — dogrudan Essentials komutu.


### /afk
**Ne ise yarar:** AFK oldugunu herkese gosterir, tekrar yazinca donersin. Kisa molalarda kullanilir.
**Ornek:** `/afk` (listede AFK gorunursun)
**Orjinal Komutu:** `/afk` — dogrudan Essentials komutu.


### /info
**Ne ise yarar:** Sunucu bilgisini ve tanitim yazisini gosterir. Turkcesi `/bilgi`.
**Ornek:** `/info` (tanitimi okursun)
**Orjinal Komutu:** `/info` — dogrudan Essentials komutu.


### /rtoggle
**Ne ise yarar:** `/r` alicisini sabitler, coklu sohbette karismayi onler.
**Ornek:** `/rtoggle` (yanit alicisi degisir)
**Orjinal Komutu:** `/rtoggle` — dogrudan Essentials komutu.


## 3-) GriefPrevention
Claim, arsa yetkisi, claim blogu ve guvenlik komutlari.

### /abandonallclaims
**Ne ise yarar:** Tum arsalarini birden siler ve korumayi tamamen kaldirir. Tasinirken veya sifirdan baslarken kullanilir. Geri donusu yoktur, ucretsizdir.
**Ornek:** `/abandonallclaims` (tum claimlerin silinir) ; tasinmadan once esyalari topla sonra yaz
**Orjinal Komutu:** `/abandonallclaims` — dogrudan GriefPrevention komutu.


### /abandonclaim
**Ne ise yarar:** Ustunde durdugun arsayi siler. Yanlis alani sectiginde kullanilir. Once esyalari topla.
**Ornek:** `/abandonclaim` (bulundugun claim silinir) ; `/abandonclaim` (koruma kalkar, bloklar acik kalir)
**Orjinal Komutu:** `/abandonclaim` — dogrudan GriefPrevention komutu.


### /abandontoplevelclaim
**Ne ise yarar:** Ana arsayi ve bagli alt claimleri birden siler. Buyuk uslerde merkezden temizlik icindir.
**Ornek:** `/abandontoplevelclaim` (ana claim ve bolmeler silinir)
**Orjinal Komutu:** `/abandontoplevelclaim` — dogrudan GriefPrevention komutu.


### /accesstrust
**Ne ise yarar:** Arsanda birine kapi-dugme-kol kullanma izni verir, blok kirma vermez. Eve misafir alirken idealdir.
**Ornek:** `/accesstrust Ahmet` (Ahmet kapilari kullanabilir)
**Orjinal Komutu:** `/accesstrust` — dogrudan GriefPrevention komutu.


### /basicclaims
**Ne ise yarar:** Claim modunu normale dondurur.
**Ornek:** `/basicclaims` (alt claim secimi kapanir)
**Orjinal Komutu:** `/basicclaims` — dogrudan GriefPrevention komutu.


### /buyclaimblocks
**Ne ise yarar:** Parayla ek arsa blogu satin alirsin. Turkcesi `/blokal`.
**Ornek:** `/buyclaimblocks 100` (100 blok alirsin)
**Orjinal Komutu:** `/buyclaimblocks` — dogrudan GriefPrevention komutu.


### /claim
**Ne ise yarar:** Secili alani korumali arsa yapar (altin kurekle 2 tik gerekir). Minimum 10x10 onerilir.
**Ornek:** `/claim` (secimin claimin olur)
**Orjinal Komutu:** `/claim` — dogrudan GriefPrevention komutu.


### /claimbook
**Ne ise yarar:** Arsa korumayi anlatan bilgi kitabini verir.
**Ornek:** `/claimbook` (kurekle kullanim ve trust komutlarini okursun)
**Orjinal Komutu:** `/claimbook` — dogrudan GriefPrevention komutu.


### /claimexplosions
**Ne ise yarar:** Arsanda patlamalari acar ya da kapatir (creeper korumasi).
**Ornek:** `/claimexplosions` (koruma degisir)
**Orjinal Komutu:** `/claimexplosions` — dogrudan GriefPrevention komutu.


### /claimslist
**Ne ise yarar:** Arsalarini ve kalan bloklarini gosterir. Turkcesi `/arsalarim`.
**Ornek:** `/claimslist` (durumunu gorursun)
**Orjinal Komutu:** `/claimslist` — dogrudan GriefPrevention komutu.


### /containertrust
**Ne ise yarar:** Birine sandik/firin kullanma izni verir, blok kirma vermez. Ortak depo icin idealdir (kisa hali `/ct`).
**Ornek:** `/containertrust Ahmet` (sandiklari acabilir)
**Orjinal Komutu:** `/containertrust` — dogrudan GriefPrevention komutu. Turkcesi: `/sandikizni`.


### /ct
**Ne ise yarar:** `/containertrust` kisa halidir.
**Ornek:** `/ct Ahmet` (hizli depo izni verirsin)
**Orjinal Komutu:** `/ct` — GriefPrevention kisaltmasi.


### /extendclaim
**Ne ise yarar:** Elindeki kurekle arsani buyutursun (yeterli blogun olmalidir).
**Ornek:** `/extendclaim 5` (5 blok uzatirsin)
**Orjinal Komutu:** `/extendclaim` — dogrudan GriefPrevention komutu.


### /ignoreplayer
**Ne ise yarar:** Bir oyuncunun sohbetini gizler.
**Ornek:** `/ignoreplayer Ahmet` (Ahmet'i yoksayarsin)
**Orjinal Komutu:** `/ignoreplayer` — GriefPrevention ignore komutu.


### /ignoredplayerlist
**Ne ise yarar:** Yoksaydiklarini listeler.
**Ornek:** `/ignoredplayerlist` (listeyi gorursun)
**Orjinal Komutu:** `/ignoredplayerlist` — GriefPrevention ignore komutu.


### /unignoreplayer
**Ne ise yarar:** Yoksaymayi kaldirir.
**Ornek:** `/unignoreplayer Ahmet` (mesajlari tekrar gelir)
**Orjinal Komutu:** `/unignoreplayer` — GriefPrevention ignore komutu.


### /permissiontrust
**Ne ise yarar:** Birine arsanda baskasina yetki verme hakki verir (en ust claim yetkisi). Dikkatli ver.
**Ornek:** `/permissiontrust Ahmet` (Ahmet de trust verebilir)
**Orjinal Komutu:** `/permissiontrust` — dogrudan GriefPrevention komutu.


### /restrictsubclaim
**Ne ise yarar:** Alt arsayi kisitlar, misafir alani ayirmada kullanilir.
**Ornek:** `/restrictsubclaim` (bulundugun alt claim daralir)
**Orjinal Komutu:** `/restrictsubclaim` — dogrudan GriefPrevention komutu.


### /sellclaimblocks
**Ne ise yarar:** Fazla arsa bloklarini paraya cevirir. Turkcesi `/bloksat`.
**Ornek:** `/sellclaimblocks 50` (50 blok satilir)
**Orjinal Komutu:** `/sellclaimblocks` — dogrudan GriefPrevention komutu.


### /subdivideclaims
**Ne ise yarar:** Arsani alt bolgelere ayirma moduna gecer.
**Ornek:** `/subdivideclaims` (kurekle alt claim secersin)
**Orjinal Komutu:** `/subdivideclaims` — dogrudan GriefPrevention komutu.


### /trapped
**Ne ise yarar:** Baskasinin arsasında sikisirsan guvenli yere isinlanirsin.
**Ornek:** `/trapped` (disari cikarsin)
**Orjinal Komutu:** `/trapped` — dogrudan GriefPrevention komutu.


### /trust
**Ne ise yarar:** Birine arsanda tam insa ve kullanim yetkisi verirsin. Turkcesi `/guven`.
**Ornek:** `/trust Ahmet` (Ahmet ev yapabilir)
**Orjinal Komutu:** `/trust` — dogrudan GriefPrevention komutu.


### /trustlist
**Ne ise yarar:** Arsa yetkilerini listelersin. Turkcesi `/guvenlistesi`.
**Ornek:** `/trustlist` (kim yetkili gorursun)
**Orjinal Komutu:** `/trustlist` — dogrudan GriefPrevention komutu.


### /untrust
**Ne ise yarar:** Birinin arsa yetkisini geri alirsin. Turkcesi `/guvenkaldir`.
**Ornek:** `/untrust Ahmet` (yetkisi silinir)
**Orjinal Komutu:** `/untrust` — dogrudan GriefPrevention komutu.


### /unstuck
**Ne ise yarar:** Blok icine sikisirsan seni cikarir.
**Ornek:** `/unstuck` (bogulurken kurtulursun)
**Orjinal Komutu:** `/unstuck` — kurtarma komutu.


## 4-) AuraSkills
11 yetenek, meslek, mana ve skill siralama komutlari.

### /abtoggle
**Ne ise yarar:** Yetenek eylem cubugunu acar kapatir. XP bildirimini gizlemek icin kullanilir.
**Ornek:** `/abtoggle` (cubuk gizlenir) ; tekrar yazinca geri gelir
**Orjinal Komutu:** `/abtoggle` — dogrudan AuraSkills komutu.


### /alchemy
**Ne ise yarar:** Simya yeteneginin seviyesini ve bonuslarini gosterir.
**Ornek:** `/alchemy` (seviyeni ve bonuslari gorursun)
**Orjinal Komutu:** `/alchemy` — dogrudan AuraSkills komutu.


### /archery
**Ne ise yarar:** Okculuk seviyeni ve yay bonuslarini gosterir.
**Ornek:** `/archery` (kritik bonus oranini kontrol edersin)
**Orjinal Komutu:** `/archery` — dogrudan AuraSkills komutu.


### /defense
**Ne ise yarar:** Savunma seviyeni ve hasar azaltma bonuslarini gosterir.
**Ornek:** `/defense` (menuyu acarsin)
**Orjinal Komutu:** `/defense` — dogrudan AuraSkills komutu.


### /excavation
**Ne ise yarar:** Kazi seviyeni ve kurek bonuslarini gosterir.
**Ornek:** `/excavation` (seviyeni kontrol edersin)
**Orjinal Komutu:** `/excavation` — dogrudan AuraSkills komutu.


### /fishing
**Ne ise yarar:** Balikcilik seviyeni ve bonuslarini gosterir. AFK fishing yasaktir, tespitte satis geri alinir.
**Ornek:** `/fishing` (menuyu acarsin)
**Orjinal Komutu:** `/fishing` — dogrudan AuraSkills komutu.


### /foraging
**Ne ise yarar:** Toplayicilik (odunculuk) seviyeni gosterir.
**Ornek:** `/foraging` (bonuslari gorursun)
**Orjinal Komutu:** `/foraging` — dogrudan AuraSkills komutu.


### /mana
**Ne ise yarar:** AuraSkills kalan manani gosterir.
**Ornek:** `/mana` (orn. 20/20 gorulur)
**Orjinal Komutu:** `/mana` — dogrudan AuraSkills komutu.


### /mining
**Ne ise yarar:** Madencilik seviyesini ve kazma bonuslarini gosterir. Demir kazmali madenci kiti (gunluk 200) ile hizli kasilir.
**Ornek:** `/mining` (seviye ve bonuslar listelenir)
**Orjinal Komutu:** `/mining` — dogrudan AuraSkills komutu.


### /sk
**Ne ise yarar:** Yetenek menusunu kisa yoldan acar.
**Ornek:** `/sk` (11 yetenek gorulur)
**Orjinal Komutu:** `/sk` — dogrudan AuraSkills kisayolu.


### /skill
**Ne ise yarar:** Yetenek menusunu acar, seviyeleri gosterir.
**Ornek:** `/skill` (bonuslari okursun)
**Orjinal Komutu:** `/skill` — dogrudan AuraSkills komutu.


### /skillrank
**Ne ise yarar:** Siralamadaki yerini gosterir. Turkcesi `/rutbe`.
**Ornek:** `/skillrank` (siran gorulur)
**Orjinal Komutu:** `/skillrank` — dogrudan AuraSkills komutu.


### /skills
**Ne ise yarar:** Tum yeteneklerin menusunu acar (11 yetenek + jobs ~0.05/XP, en fazla 2 job). Turkcesi `/yetenek`.
**Ornek:** `/skills` (seviyeler gorulur)
**Orjinal Komutu:** `/skills` — dogrudan AuraSkills komutu.

### /skilltop
**Ne ise yarar:** En yuksek yetenek seviyelerini listeler. Turkce wrapper komutu `/yetenekskor` ayni listeyi acar.
**Ornek:** `/skilltop` (yetenek liderlerini gorursun)
**Orjinal Komutu:** `/skilltop` — dogrudan AuraSkills komutu.


### /stats
**Ne ise yarar:** Guc-saglik ozelliklerini gosterir. Turkcesi `/ozellik`.
**Ornek:** `/stats` (stat menusu acilir)
**Orjinal Komutu:** `/stats` — dogrudan AuraSkills komutu.


## 5-) BeautyQuests
Gorev menusu ve gorev yonetimi komutlari.

### /beautyquests
**Ne ise yarar:** Gorevlerin ana menusunu acar. Oduller 50-250 arasi.
**Ornek:** `/beautyquests` (menu acilir)
**Orjinal Komutu:** `/beautyquests` — dogrudan BeautyQuests komutu. Turkcesi: `/gorevler`.


## 6-) EliteMobs
EliteMobs maceraci ve boss yonetimi komutlari.

### /adventurersguild
**Ne ise yarar:** Maceraci lonca menusunu acar.
**Ornek:** `/adventurersguild` (lonca menusu acilir)
**Orjinal Komutu:** `/adventurersguild` — dogrudan EliteMobs lonca komutu.


### /nightbreak
**Ne ise yarar:** EliteMobs hesap durumunu gosterir.
**Ornek:** `/nightbreak` (bilgiyi gorursun).

**Orjinal Komutu:** /nightbreak - dogrudan EliteMobs komutu.

### /nightbreaklogin
**Ne ise yarar:** EliteMobs hesabini baglarsin.
**Ornek:** `/nightbreaklogin` (hesabi baglarsin).

**Orjinal Komutu:** /nightbreaklogin - dogrudan EliteMobs komutu.

### /nightbreaklogout
**Ne ise yarar:** Hesap bagini cozarsin.
**Ornek:** `/nightbreaklogout` (bagi koparirsin).

**Orjinal Komutu:** /nightbreaklogout - dogrudan EliteMobs komutu.

## 7-) GUIShop
Market, satis ve esya fiyat komutlari.

### /guishop
**Ne ise yarar:** Market yardimini gosterir.
**Ornek:** `/guishop` (kullanimi okursun)
**Orjinal Komutu:** `/guishop` — dogrudan GUIShop komutu.


### /guishopuser
**Ne ise yarar:** Market komutlarini listeler.
**Ornek:** `/guishopuser` (alis komutlarini ogrenirsin)
**Orjinal Komutu:** `/guishopuser` — dogrudan GUIShop komutu.


### /market
**Ne ise yarar:** Market alis menusunu acar (Bloklar, Yemek, Savas, Aletler). Sadece alis vardir, satis `/satis` ile ayridir, alislar ~5x vergilidir.
**Ornek:** `/market` (alis menusu acilir) ; Yemek secimi (ekmek alinir)
**Orjinal Komutu:** `/market` — Bukkit takma adi `/shop` komutuna bagli.


### /satis
**Ne ise yarar:** Envanterindekileri satis ekranindan satarsin (saatlik 500 uzeri izlenir).
**Ornek:** `/satis` (menu acilir, secerek satarsin)
**Orjinal Komutu:** `/satis` — dogrudan GUIShop satis menusu.


### /shop
**Ne ise yarar:** Marketten esya alirsin (Bloklar, Yemek, Savas, Aletler). Sadece alis vardir (~5x vergili), elmas set/totem/spawner satilmaz. Turkcesi `/pazar`.
**Ornek:** `/shop` (menu acilir)
**Orjinal Komutu:** `/shop` — dogrudan GUIShop komutu.


### /value
**Ne ise yarar:** Elindeki esyanin market fiyatini gosterir. Turkcesi `/fiyat`.
**Ornek:** `/value` (demirde 8 gorursun)
**Orjinal Komutu:** `/value` — dogrudan GUIShop komutu.


## 8-) KaMenu
Ana menu ve liderlik dialoglari.

### /liderlik
**Ne ise yarar:** Para, avci, sure, guc ve olum siralamalarini dialog menude gosterir. `/balancetop` ve `/skilltop` verilerini tek ekranda toplar.
**Ornek:** `/liderlik` (5 kategori acilir) ; menuden Para secimi (en zenginler listelenir)
**Orjinal Komutu:** `/liderlik` — KaMenu `dgm/liderlik` dialogu.


### /menu
**Ne ise yarar:** Sunucunun ana dialog menusunu acar (Kitler, Market, Nick, Gorevler, Yetenekler, Bilgi, Liderlik). F+Shift ile de acilir.
**Ornek:** `/menu` (ana dialog acilir) ; Kitler secimi (15 kit listelenir)
**Orjinal Komutu:** `/menu` — KaMenu `dgm/menu` ozel komutu.


## 9-) GSit
Oturma, uzanma, donme ve diger oyuncu pozlari.

### /gbellyflop
**Ne ise yarar:** Baliklama atlama hareketi yapar. Turkcesi `/baliklama`.
**Ornek:** `/gbellyflop` (atlarsin)
**Orjinal Komutu:** `/gbellyflop` — dogrudan GSit komutu.


### /gcrawl
**Ne ise yarar:** Surunme pozu alirsin. Turkcesi `/surun`.
**Ornek:** `/gcrawl` (surunursun)
**Orjinal Komutu:** `/gcrawl` — dogrudan GSit komutu.


### /glay
**Ne ise yarar:** Yere uzanirsin. Turkcesi `/uzan`.
**Ornek:** `/glay` (uzanirsin, tekrar yazinca kalkarsin)
**Orjinal Komutu:** `/glay` — dogrudan GSit komutu.


### /glegsup
**Ne ise yarar:** Bacaklari havaya kaldirirsin. Turkcesi `/bacak`.
**Ornek:** `/glegsup` (eglenirsin)
**Orjinal Komutu:** `/glegsup` — dogrudan GSit komutu.


### /gsit
**Ne ise yarar:** Oldugun yere oturursun, tekrar yazinca kalkarsin. Turkcesi `/otur`.
**Ornek:** `/gsit` (oturursun)
**Orjinal Komutu:** `/gsit` — dogrudan GSit komutu.


### /gspin
**Ne ise yarar:** Kendi etrafinda donersin. Turkcesi `/donme`.
**Ornek:** `/gspin` (animasyon gosterirsin)
**Orjinal Komutu:** `/gspin` — dogrudan GSit komutu.


## 10-) PetCore
Evcil hayvan ve pet sahipligi komutlari.

### /pet
**Ne ise yarar:** Evcil hayvan menusunu acar. Turkcesi `/evcil`.
**Ornek:** `/pet` (petini cagirirsin)
**Orjinal Komutu:** `/pet` — dogrudan PetCore komutu.


### /petgift
**Ne ise yarar:** Petini baska oyuncuya hediye edersin. Turkcesi `/hediye`.
**Ornek:** `/petgift Ahmet` (sahiplik degisir)
**Orjinal Komutu:** `/petgift` — dogrudan PetCore komutu.


## 11-) UltraCosmetics
Sapka, efekt ve kozmetik komutlari.

### /ultracosmetics
**Ne ise yarar:** Sapka ve efekt menusunu acar. Turkcesi `/kozmetik`.
**Ornek:** `/ultracosmetics` (kozmetik secersin)
**Orjinal Komutu:** `/ultracosmetics` — dogrudan UltraCosmetics komutu.


## 12-) SkinsRestorer
Oyuncu skin gorunumunu yoneten komutlar.

### /skin
**Ne ise yarar:** Gorunumunu degistirir. Turkcesi `/gorunum`.
**Ornek:** `/skin Notch` (skinin degisir)
**Orjinal Komutu:** `/skin` — dogrudan SkinsRestorer komutu.


## 13-) AxGraves
Olum mezari ve mezar kurtarma komutlari.

### /grave
**Ne ise yarar:** Mezarin oldugu yere isinlanirsin (5 dakika icinde topla).
**Ornek:** `/grave` (olum noktasina donersin). Turkcesi: `/mezar`.
**Orjinal Komutu:** `/grave` — dogrudan AxGraves komutu.


### /axgrave
**Ne ise yarar:** Mezarin hakkinda bilgi verir. Olumde esyalarin nerede korundugunu ogrenmek icin kullanilir (5 dakika icinde alinmalidir).
**Ornek:** `/axgrave` (mezar suresi ve konumu listelenir)
**Orjinal Komutu:** `/axgrave` — dogrudan AxGraves komutu.


## 14-) BeaconWaypointsReloaded ve MonumentWaypoints
Isaret ve anit waypoint komutlari.

### /mw
**Ne ise yarar:** Anit ve ozel noktalari gosterir. Turkcesi `/anit`.
**Ornek:** `/mw` (kayitli noktalar gorulur)
**Orjinal Komutu:** `/mw` — dogrudan MonumentWaypoints komutu.


## 15-) TAB
Scoreboard ve TAB gorunumu komutlari.

### /sb
**Ne ise yarar:** Sagdaki skor tablosunu acar kapatir. Turkcesi `/skortablo`.
**Ornek:** `/sb` (tablo gizlenir, tekrar yazinca acilir)
**Orjinal Komutu:** `/sb` — dogrudan TAB komutu.


## 16-) Plan
Oyun suresi ve oyuncu istatistikleri.

### /plan
**Ne ise yarar:** Oyun istatistiklerini gosterir (`plan ingame`). Turkcesi `/istatistik`.
**Ornek:** `/plan ingame` (suren ve aktiviten gorulur)
**Orjinal Komutu:** `/plan` — dogrudan Plan komutu.


### /plan reload
**Ne ise yarar:** Istatistik ayarlarini yeniler.
**Ornek:** `/plan reload` (configi yeniden yukler).

**Orjinal Komutu:** /plan reload - sunucu veya cekirdek admin komutu.

## 17-) ajLeaderboards
Skor panolari ve siralama komutlari.

### /ajleaderboards (ajlb)
**Ne ise yarar:** Skor panolarini yonetirsin.
**Ornek:** `/ajlb add %vault_eco_balance%` (pano eklersin).

**Orjinal Komutu:** /ajleaderboards (ajlb) - dogrudan ajLeaderboards komutu.

## 18-) DgmGecmis
Oyuncunun kendi gecmis loglarini gosterir.

### /gecmis
**Ne ise yarar:** Son 100 log satirini sadece sana gosterir (kim ne yapmis, suphe arastirma).
**Ornek:** `/gecmis` (100 satiri okursun)
**Orjinal Komutu:** `/gecmis` — dogrudan DgmGecmis komutu.


## 19-) LuckPerms
Yetki, grup ve kullanici izin yonetimi.

### /luckperms (lp)
**Ne ise yarar:** Yetki gruplarini ve izinleri yonetirsin.
**Ornek:** `/lp user Ahmet parent set admin` (Ahmet'i admin yaparsin).
**Dikkat:** Yanlis izin kilitler, once yedek al.

**Orjinal Komutu:** /luckperms (lp) - dogrudan LuckPerms komutu.

## 20-) WorldGuard
Admin bolgeleri ve bolge koruma ayarlari.

### /region (rg)
**Ne ise yarar:** WorldGuard bolgesi olusturur yonetirsin.
**Ornek:** `/region define spawn` (alani bolge yaparsin).
**Dikkat:** Yanlis bayrak korumayi bozar.

**Orjinal Komutu:** /region (rg) - dogrudan WorldGuard komutu.

### /worldguard (wg)
**Ne ise yarar:** Koruma ana komutudur.
**Ornek:** `/worldguard reload` (ayarlari yenilersin).

**Orjinal Komutu:** /worldguard (wg) - dogrudan WorldGuard komutu.

## 21-) WorldEdit
Admin dunya duzenleme, secim ve yapi araclari.

### //wand
**Ne ise yarar:** Secim baltasi verirsin, sag-sol tikla alan secersin.
**Ornek:** `//wand` (araci alirsin).

**Orjinal Komutu:** //wand - dogrudan WorldEdit komutu.

### //pos1, //pos2, //hpos1, //hpos2
**Ne ise yarar:** Secim noktalarini koyarsin (h: baktigin blok).
**Ornek:** `//pos1` (ayagindakini isaretlersin).

**Orjinal Komutu:** //pos1, //pos2, //hpos1, //hpos2 - dogrudan WorldEdit komutu.

### //sel, //selwand, //navwand, //farwand
**Ne ise yarar:** Secim araclarini yonetirsin.
**Ornek:** `//selwand` (baltayi verir).

**Orjinal Komutu:** //sel, //selwand, //navwand, //farwand - dogrudan WorldEdit komutu.

### //set
**Ne ise yarar:** Secili alani tek blokla doldurursun.
**Ornek:** `//set stone` (secimi tas yaparsin).
**Dikkat:** Secimi siler.

**Orjinal Komutu:** //set - dogrudan WorldEdit komutu.

### //replace
**Ne ise yarar:** Secimdeki bir blogu baskasiyla degistirirsin.
**Ornek:** `//replace dirt stone` (topragi tasa cevirirsin).
**Dikkat:** Binlerce blogu degistirir.

**Orjinal Komutu:** //replace - dogrudan WorldEdit komutu.

### //copy, //cut, //paste
**Ne ise yarar:** Secimi kopyalar, keser ve yapistirirsin.
**Ornek:** `//copy` (kopyalarsin) ; `//paste` (onune yapistirirsin).
**Dikkat:** Buyuk secim RAM sisirir, uzerine yazdigi yapiyi siler.

**Orjinal Komutu:** //copy, //cut, //paste - dogrudan WorldEdit komutu.

### //rotate, //revolve, //flip
**Ne ise yarar:** Panoyu dondurur, cogaltir ve aynalarsin.
**Ornek:** `//rotate 90` (90 derece cevirirsin).
**Dikkat:** Cok kopya lag yapar.

**Orjinal Komutu:** //rotate, //revolve, //flip - dogrudan WorldEdit komutu.

### //move
**Ne ise yarar:** Secimi belirttigin yone tasiyabilirsin.
**Ornek:** `//move 5 up` (5 blok yukari tasirsin).
**Dikkat:** Eski yer silinir.

**Orjinal Komutu:** //move - dogrudan WorldEdit komutu.

### //stack
**Ne ise yarar:** Secimi ayni yonde ust uste yigarsin.
**Ornek:** `//stack 5 north` (kuzeye 5 kez yigarsin).
**Dikkat:** Devasa alan olur.

**Orjinal Komutu:** //stack - dogrudan WorldEdit komutu.

### //undo, //redo
**Ne ise yarar:** Son islemi geri alir ya da tekrar uygularsin.
**Ornek:** `//undo` (yanlis seti dondurursun).

**Orjinal Komutu:** //undo, //redo - dogrudan WorldEdit komutu.

### //schematic
**Ne ise yarar:** Sematik dosyayi kaydeder ve yuklersin.
**Ornek:** `//schematic save evim` (secimi kaydedersin).
**Dikkat:** Yanlis yukleme ust uste bindirir.

**Orjinal Komutu:** //schematic - dogrudan WorldEdit komutu.

### //mask, //gmask
**Ne ise yarar:** Hangi bloklarin degisecegini sinirlarsin.
**Ornek:** `//mask stone` (sadece tasi degistirirsin).

**Orjinal Komutu:** //mask, //gmask - dogrudan WorldEdit komutu.

### //count, //distr, //size
**Ne ise yarar:** Secimi sayar, dagilimi ve boyutu gosterirsin.
**Ornek:** `//count stone` (kac tas oldugunu soyler).

**Orjinal Komutu:** //count, //distr, //size - dogrudan WorldEdit komutu.

### //expand, //contract, //shift, //inset, //outset
**Ne ise yarar:** Secimi buyutur, kucultur ve kaydirirsin.
**Ornek:** `//expand 10 up` (yukari genisletirsin).

**Orjinal Komutu:** //expand, //contract, //shift, //inset, //outset - dogrudan WorldEdit komutu.

### //forest, //forestgen, //flora, //pumpkins
**Ne ise yarar:** Secime doga uretirsin (agac, cicek, balkabagi).
**Ornek:** `//forest oak` (meselik olusturursun).
**Dikkat:** Yuzlerce obje lag yapar.

**Orjinal Komutu:** //forest, //forestgen, //flora, //pumpkins - dogrudan WorldEdit komutu.

### //cyl, //hcyl, //sphere, //hsphere, //pyramid, //hpyramid, //cone
**Ne ise yarar:** Geometrik sekiller cizersin (dolu/bos).
**Ornek:** `//sphere stone 5` (kure yaparsin).
**Dikkat:** Buyuk yaricap binlerce blok koyar.

**Orjinal Komutu:** //cyl, //hcyl, //sphere, //hsphere, //pyramid, //hpyramid, //cone - dogrudan WorldEdit komutu.

### //line, //curve, //walls, //center
**Ne ise yarar:** Cizgi, egri, duvar ve merkez isaretlersin.
**Ornek:** `//line stone` (tas cizgi cekersin).
**Dikkat:** Uzun cizgi yapinin ustune yazar.

**Orjinal Komutu:** //line, //curve, //walls, //center - dogrudan WorldEdit komutu.

### //naturalize, //smooth, //snow, //snowsmooth, //thaw, //green
**Ne ise yarar:** Araziyi dogallastirir, yumusatir ve iklimlendirirsin.
**Ornek:** `//smooth 2` (engebeyi yumusatirsin).
**Dikkat:** Yapili alani bozar.

**Orjinal Komutu:** //naturalize, //smooth, //snow, //snowsmooth, //thaw, //green - dogrudan WorldEdit komutu.

### //drain, //fixwater, //fixlava, //floodfill
**Ne ise yarar:** Sivilari bosaltir, duzeltir ve doldurursun.
**Ornek:** `//drain 10` (siviyi kurutursun).
**Dikkat:** Gol ve tuzak silinir.

**Orjinal Komutu:** //drain, //fixwater, //fixlava, //floodfill - dogrudan WorldEdit komutu.

### //overlay, //hollow
**Ne ise yarar:** Ustu kaplar ya da ici bosaltirsin.
**Ornek:** `//hollow` (icini bosaltirsin).
**Dikkat:** Icindeki sandik silinir.

**Orjinal Komutu:** //overlay, //hollow - dogrudan WorldEdit komutu.

### //regen, //restore, //snapshot
**Ne ise yarar:** Secimi yeniler, yedekten dondurur ve goruntu yonetirsin.
**Ornek:** `//regen` (araziyi yenilersin).
**Dikkat:** Oyuncu yapilari silinir.

**Orjinal Komutu:** //regen, //restore, //snapshot - dogrudan WorldEdit komutu.

### //search, //replacebiome, //setbiome
**Ne ise yarar:** Blok arar ve biyom degistirirsin.
**Ornek:** `//search diamond_ore` (elmasi ararsin).
**Dikkat:** Dogma degisir.

**Orjinal Komutu:** //search, //replacebiome, //setbiome - dogrudan WorldEdit komutu.

### //replacenear, //removenear, //removeabove, //removebelow
**Ne ise yarar:** Yakinindakileri duzenler ve temizlersin.
**Ornek:** `//replacenear 20 stone cobblestone` (cevreyi degistirirsin).
**Dikkat:** Yapiyi bozar, yaricapi kucuk tut.

**Orjinal Komutu:** //replacenear, //removenear, //removeabove, //removebelow - dogrudan WorldEdit komutu.

### //limit, //timeout, //fast
**Ne ise yarar:** Islem sinirlarini ve hizi ayarlarsin.
**Ornek:** `//limit 50000` (limiti ayarlarsin).
**Dikkat:** Fiziksiz modda kum havada kalir.

**Orjinal Komutu:** //limit, //timeout, //fast - dogrudan WorldEdit komutu.

### //superpickaxe, //tool
**Ne ise yarar:** Alan kiran kazma verir ve alet baglarsin.
**Ornek:** `//superpickaxe area 3` (3x3 kirarsin).
**Dikkat:** Yanlis vurus deler, bitince kapat.

**Orjinal Komutu:** //superpickaxe, //tool - dogrudan WorldEdit komutu.

### //toggleeditwand, //toggleplace
**Ne ise yarar:** Duzenleme ve koyma modlarini acar kapatirsin.
**Ornek:** `//toggleeditwand` (kapatirsin).

**Orjinal Komutu:** //toggleeditwand, //toggleplace - dogrudan WorldEdit komutu.

### //brush, //generate, //generatebiome, //deform
**Ne ise yarar:** Firca ve formulle uretim yaparsin.
**Ornek:** `//brush sphere stone 3` (fircayi yaparsin).
**Dikkat:** Binlerce blok koyar, once yedek al.

**Orjinal Komutu:** //brush, //generate, //generatebiome, //deform - dogrudan WorldEdit komutu.

### //up, //ceil, //descend, //thru, //jumpto
**Ne ise yarar:** Dikey hareket edersin.
**Ornek:** `//up 10` (10 blok cikarsin).

**Orjinal Komutu:** //up, //ceil, //descend, //thru, //jumpto - dogrudan WorldEdit komutu.

### //trim, //calculate, //listchunks
**Ne ise yarar:** Dunyayi kirpar, hesap yapar ve chunk listelersin.
**Ornek:** `//trim` (boslari silersin).
**Dikkat:** Silinen geri gelmez, yedeksiz yapma.

**Orjinal Komutu:** //trim, //calculate, //listchunks - dogrudan WorldEdit komutu.

### //sel, //mask, //material, //range
**Ne ise yarar:** Secim ve malzeme ayarlarini gosterirsin.
**Ornek:** `//sel` (bilgiyi gorursun).

**Orjinal Komutu:** //sel, //mask, //material, //range - dogrudan WorldEdit komutu.

### //wpos1, //wpos2, //pos1, //pos2
**Ne ise yarar:** Nokta secersin (w: dunya koordinatiyla).
**Ornek:** `//pos1` (ayagindakini isaretlersin).

**Orjinal Komutu:** //wpos1, //wpos2, //pos1, //pos2 - dogrudan WorldEdit komutu.

### //deltree
**Ne ise yarar:** Baktigin agaci kokunden silersin.
**Ornek:** `//deltree` (agaci kaldirirsin).
**Dikkat:** Bitisik yapiyi goturebilir.

**Orjinal Komutu:** //deltree - dogrudan WorldEdit komutu.

### /cycler, //lrbuild, //placement, //reorder
**Ne ise yarar:** Varyant ve yerlestirme araclarini kullanirsin (`/cycler` slashsizdir).
**Ornek:** `/cycler` (tikla yonu cevirirsin).
**Dikkat:** Denemeden buyuk alanda kullanma.

**Orjinal Komutu:** /cycler, //lrbuild, //placement, //reorder - dogrudan WorldEdit komutu.

### //tracemask
**Ne ise yarar:** Isin izinin gectigi blogu ayarlarsin.
**Ornek:** `//tracemask glass` (cami yok sayarsin).

**Orjinal Komutu:** //tracemask - dogrudan WorldEdit komutu.

### //update
**Ne ise yarar:** Secimdeki blok isigini guncellersin.
**Ornek:** `//update` (karanligi aydinlatirsin).

**Orjinal Komutu:** //update - dogrudan WorldEdit komutu.

### /we, /worldedit, /rg, /region, /wg, /worldguard
**Ne ise yarar:** Ana komutlar ve kisayollari (detay yukaridaki satirlarda).
**Ornek:** `/we version` (surumu gorursun).

**Orjinal Komutu:** /we, /worldedit, /rg, /region, /wg, /worldguard - dogrudan WorldEdit komutu.

### /worldedit (we)
**Ne ise yarar:** WorldEdit ana komutudur.
**Ornek:** `/we version` (surumu gorursun).
**Dikkat:** Buyuk islemden once yedek al.

**Orjinal Komutu:** /worldedit (we) - dogrudan WorldEdit komutu.

## 22-) Chunky
Haritayi onceden uretme ve chunk islemleri.

### /chunky
**Ne ise yarar:** Haritayi onceden uretirsin.
**Ornek:** `/chunky spawn` + `/chunky radius 2500` + `/chunky start` (uretime baslarsin).

**Orjinal Komutu:** /chunky - dogrudan Chunky komutu.

## 23-) PlugManX
Pluginleri yonetmek icin admin komutlari.

### /plugman
**Ne ise yarar:** Plugini kapatmadan acar kapatirsin.
**Ornek:** `/plugman disable EliteMobs` (gecici kapatirsin).
**Dikkat:** Once yedek al.

**Orjinal Komutu:** /plugman - dogrudan PlugManX komutu.

## 24-) PerformanceAnalyzer ve LagPeek
TPS, tick ve lag analiz komutlari.

### /worldstats
**Ne ise yarar:** Dunya boyutu ve dosya bilgisi verir.
**Ornek:** `/worldstats` (klasor buyuklugunu gorursun).

**Orjinal Komutu:** /worldstats - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /entitystats
**Ne ise yarar:** Yuklu canli ve esya sayisini gosterir.
**Ornek:** `/entitystats` (hangi mob cok gorursun).

**Orjinal Komutu:** /entitystats - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /chunkstats
**Ne ise yarar:** Yuklu chunk durumunu gosterir.
**Ornek:** `/chunkstats` (yuku gorursun).

**Orjinal Komutu:** /chunkstats - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /perfhistory
**Ne ise yarar:** Gecmis performans kayitlarini listeler.
**Ornek:** `/perfhistory` (dalgalanmalari gorursun).

**Orjinal Komutu:** /perfhistory - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /perfstatus
**Ne ise yarar:** Anlik performansi ozetler.
**Ornek:** `/perfstatus` (TPS ve yuku gorursun).

**Orjinal Komutu:** /perfstatus - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /perfgui
**Ne ise yarar:** Performansi oyun ici ekranda gosterir.
**Ornek:** `/perfgui` (paneli acarsin).

**Orjinal Komutu:** /perfgui - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /perfreload
**Ne ise yarar:** Izleyici ayarlarini yeniler.
**Ornek:** `/perfreload` (ayarlari yukler).

**Orjinal Komutu:** /perfreload - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /perfincidents
**Ne ise yarar:** Kaydedilmis lag olaylarini listeler.
**Ornek:** `/perfincidents` (donmalari gorursun).

**Orjinal Komutu:** /perfincidents - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /perfsilent
**Ne ise yarar:** Performans uyarilarini sessize alir.
**Ornek:** `/perfsilent on` (mesajlari gizlersin).

**Orjinal Komutu:** /perfsilent - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /perfcalibrate
**Ne ise yarar:** Olceri kalibre eder.
**Ornek:** `/perfcalibrate` (esikleri ayarlarsin).

**Orjinal Komutu:** /perfcalibrate - dogrudan PerformanceAnalyzer/LagPeek komutu.

### /lagpeek
**Ne ise yarar:** Anlik lag kaynagini analiz eder.
**Ornek:** `/lagpeek` (ne kastigini gorursun).

**Orjinal Komutu:** /lagpeek - dogrudan PerformanceAnalyzer/LagPeek komutu.

## 25-) Vault ve PlaceholderAPI
Ekonomi koprusu ve placeholder yonetimi.

### /vault-info
**Ne ise yarar:** Ekonomi baglantisini gosterir.
**Ornek:** `/vault-info` (hangi ekonomi bagli gorursun).

**Orjinal Komutu:** /vault-info - dogrudan Vault/PlaceholderAPI komutu.

### /vault-convert
**Ne ise yarar:** Ekonomi verisini donusturur.
**Ornek:** `/vault-convert` (veriyi tasirsin).
**Dikkat:** Para bozulabilir, once yedek al.

**Orjinal Komutu:** /vault-convert - dogrudan Vault/PlaceholderAPI komutu.

## 26-) FancyHolograms
Admin hologram yonetimi.

_Bu plugin icin dogrudan oyuncu komutu kayitli degil; plugin sunucu altyapisi olarak calisir._

## 27-) Vanilla Minecraft
Minecraft cekirdeginin admin ve oyuncu komutlari.

### /recipe
**Ne ise yarar:** Esya tarifini gosterir. Turkcesi `/tarif`.
**Ornek:** `/recipe torch` (tarif acilir)
**Orjinal Komutu:** `/recipe` — dogrudan Essentials komutu.


### /advancement
**Ne ise yarar:** Oyuncuya basarim verir ya da alirsin.
**Ornek:** `/advancement grant Ahmet everything` (tum basarimlari verirsin).

**Orjinal Komutu:** /advancement - Minecraft vanilla komutu.

### /attribute
**Ne ise yarar:** Can ve hiz gibi ozellikleri duzenlersin.
**Ornek:** `/attribute Ahmet minecraft:generic.max_health base set 20` (cani 20 yaparsin).

**Orjinal Komutu:** /attribute - Minecraft vanilla komutu.

### /ban-ip
**Ne ise yarar:** IP adresini yasaklarsin.
**Ornek:** `/ban-ip 1.2.3.4` (IP'yi yasaklarsin).
**Dikkat:** Tum haneyi engelleyebilir.

**Orjinal Komutu:** /ban-ip - Minecraft vanilla komutu.

### /banlist
**Ne ise yarar:** Yasakli listesini gosterirsin.
**Ornek:** `/banlist players` (yasaklilari listelersin).

**Orjinal Komutu:** /banlist - Minecraft vanilla komutu.

### /bossbar
**Ne ise yarar:** Ekran ustu cubuk olusturursun.
**Ornek:** `/bossbar add duyuru Bakim` (duyuru cubugu acarsin).

**Orjinal Komutu:** /bossbar - Minecraft vanilla komutu.

### /clear
**Ne ise yarar:** Oyuncu envanterini temizlersin.
**Ornek:** `/clear Ahmet` (envanteri siler).
**Dikkat:** Esyalar geri gelmez.

**Orjinal Komutu:** /clear - Minecraft vanilla komutu.

### /clone
**Ne ise yarar:** Alani aynen kopyalarsin.
**Ornek:** `/clone 0 60 0 10 70 10 20 60 20` (alani tasiyarak kopyalarsin).
**Dikkat:** Hedefteki bloklar silinir.

**Orjinal Komutu:** /clone - Minecraft vanilla komutu.

### /data
**Ne ise yarar:** Blok ve canli verisini gorur duzenlersin.
**Ornek:** `/data get entity @e[type=pig,limit=1]` (domuz verisini gorursun).
**Dikkat:** Yanlis NBT bozar.

**Orjinal Komutu:** /data - Minecraft vanilla komutu.

### /datapack
**Ne ise yarar:** Veri paketlerini acar kapatirsin.
**Ornek:** `/datapack list` (paketleri listelersin).

**Orjinal Komutu:** /datapack - Minecraft vanilla komutu.

### /debug
**Ne ise yarar:** Hata ayiklama profili baslatirsin.
**Ornek:** `/debug start` (10sn kayit alirsin).

**Orjinal Komutu:** /debug - Minecraft vanilla komutu.

### /defaultgamemode
**Ne ise yarar:** Yeni girenlerin modunu belirlersin.
**Ornek:** `/defaultgamemode survival` (varsayilani ayarlarsin).
**Dikkat:** Herkesi etkiler.

**Orjinal Komutu:** /defaultgamemode - Minecraft vanilla komutu.

### /demo
**Ne ise yarar:** Demo ekranini gosterir.
**Ornek:** `/demo` (mesaji tetiklersin).

**Orjinal Komutu:** /demo - Minecraft vanilla komutu.

### /difficulty
**Ne ise yarar:** Zorlugu ayarlarsin.
**Ornek:** `/difficulty hard` (zora alirsin).
**Dikkat:** Dengeyi degistirir.

**Orjinal Komutu:** /difficulty - Minecraft vanilla komutu.

### /effect
**Ne ise yarar:** Oyuncuya efekt verir ya da temizlersin.
**Ornek:** `/effect give Ahmet minecraft:speed 60 1` (hiz verirsin).

**Orjinal Komutu:** /effect - Minecraft vanilla komutu.

### /fill
**Ne ise yarar:** Alani tek blokla doldurursun.
**Ornek:** `/fill 0 60 0 10 70 10 stone` (tasla doldurursun).
**Dikkat:** Binlerce blogu siler.

**Orjinal Komutu:** /fill - Minecraft vanilla komutu.

### /fillbiome
**Ne ise yarar:** Alanin biyomunu degistirirsin.
**Ornek:** `/fillbiome 0 0 0 16 0 16 plains` (ova yaparsin).
**Dikkat:** Geri almak zordur.

**Orjinal Komutu:** /fillbiome - Minecraft vanilla komutu.

### /function
**Ne ise yarar:** Kayitli fonksiyonu calistirirsin.
**Ornek:** `/function ornek:baslat` (calistirirsin).

**Orjinal Komutu:** /function - Minecraft vanilla komutu.

### /gamerule
**Ne ise yarar:** Oyun kurallarini degistirirsin.
**Ornek:** `/gamerule keepInventory true` (olumde esya korunur).
**Dikkat:** Tum dunyayi etkiler.

**Orjinal Komutu:** /gamerule - Minecraft vanilla komutu.

### /jfr
**Ne ise yarar:** Java kaydi alirsin.
**Ornek:** `/jfr start` (performans kaydi baslatirsin).

**Orjinal Komutu:** /jfr - Minecraft vanilla komutu.

### /kick
**Ne ise yarar:** Oyuncuyu sunucudan atarsin.
**Ornek:** `/kick Ahmet` (gerekceyle atarsin).
**Dikkat:** Tekrar girebilir, kalici icin ban gerekir.

**Orjinal Komutu:** /kick - Minecraft vanilla komutu.

### /kill
**Ne ise yarar:** Canliyi ya da oyuncuyu oldurursun.
**Ornek:** `/kill Ahmet` (esyalari duser).
**Dikkat:** Esya kaybi olur.

**Orjinal Komutu:** /kill - Minecraft vanilla komutu.

### /locate
**Ne ise yarar:** En yakin yapiyi bulursun.
**Ornek:** `/locate structure village` (koy koordinati verir).

**Orjinal Komutu:** /locate - Minecraft vanilla komutu.

### /loot
**Ne ise yarar:** Ganimet tablosundan esya verirsin.
**Ornek:** `/loot give Ahmet loot minecraft:chests/simple_dungeon` (ganimet verirsin).

**Orjinal Komutu:** /loot - Minecraft vanilla komutu.

### /pardon
**Ne ise yarar:** Oyuncu yasagini kaldirirsin.
**Ornek:** `/pardon Ahmet` (bani acarsin).
**Dikkat:** Griefer donebilir.

**Orjinal Komutu:** /pardon - Minecraft vanilla komutu.

### /pardon-ip
**Ne ise yarar:** IP yasagini kaldirirsin.
**Ornek:** `/pardon-ip 1.2.3.4` (acar).

**Orjinal Komutu:** /pardon-ip - Minecraft vanilla komutu.

### /particle
**Ne ise yarar:** Belirtilen yerde parcacik gosterirsin.
**Ornek:** `/particle minecraft:flame 0 70 0` (alev gosterirsin).

**Orjinal Komutu:** /particle - Minecraft vanilla komutu.

### /place
**Ne ise yarar:** Yapi yerlestirirsin.
**Ornek:** `/place structure village` (koy yerlestirirsin).
**Dikkat:** Uzerine biner.

**Orjinal Komutu:** /place - Minecraft vanilla komutu.

### /playsound
**Ne ise yarar:** Oyuncuya ses calarsin.
**Ornek:** `/playsound minecraft:bell master Ahmet` (can sesi calarsin).

**Orjinal Komutu:** /playsound - Minecraft vanilla komutu.

### /publish
**Ne ise yarar:** Dunyayi LAN'e acar (kullanma).
**Ornek:** `/publish` (gereksiz acik olusturur, kullanma).

**Orjinal Komutu:** /publish - Minecraft vanilla komutu.

### /reload
**Ne ise yarar:** Yenilemeye calisir.
**Ornek:** `/reload` (ASLA kullanma, pluginleri bozar).

**Orjinal Komutu:** /reload - Minecraft vanilla komutu.

### /save-all
**Ne ise yarar:** Tum dunyalari diske kaydedersin.
**Ornek:** `/save-all` (hemen kaydedersin).
**Dikkat:** `/stop` oncesi mutlaka yap.

**Orjinal Komutu:** /save-all - Minecraft vanilla komutu.

### /save-off
**Ne ise yarar:** Otomatik kaydi kapatirsin.
**Ornek:** `/save-off` (durdurursun).
**Dikkat:** Acik unutursan ilerleme gider, sonra `/save-on` yap.

**Orjinal Komutu:** /save-off - Minecraft vanilla komutu.

### /save-on
**Ne ise yarar:** Otomatik kaydi acarsin.
**Ornek:** `/save-on` (yeniden acarsin).

**Orjinal Komutu:** /save-on - Minecraft vanilla komutu.

### /say
**Ne ise yarar:** Sunucuya duyuru yazarsin.
**Ornek:** `/say 5dk sonra bakim` (herkes gorur).

**Orjinal Komutu:** /say - Minecraft vanilla komutu.

### /schedule
**Ne ise yarar:** Komutu gecikmeli calistirirsin.
**Ornek:** `/schedule function ornek:kapat 60s` (60sn sonra calisir).

**Orjinal Komutu:** /schedule - Minecraft vanilla komutu.

### /scoreboard
**Ne ise yarar:** Skor tahtasi hedeflerini yonetirsin.
**Ornek:** `/scoreboard objectives add olum deathCount` (olum sayaci eklersin).

**Orjinal Komutu:** /scoreboard - Minecraft vanilla komutu.

### /seed
**Ne ise yarar:** Dunya tohumunu gosterirsin.
**Ornek:** `/seed` (chatte gosterirsin).

**Orjinal Komutu:** /seed - Minecraft vanilla komutu.

### /setblock
**Ne ise yarar:** Tek blogu degistirirsin.
**Ornek:** `/setblock 0 70 0 diamond_block` (elmas koyarsin).
**Dikkat:** Altindaki silinir.

**Orjinal Komutu:** /setblock - Minecraft vanilla komutu.

### /setidletimeout
**Ne ise yarar:** AFK atma suresini ayarlarsin.
**Ornek:** `/setidletimeout 10` (10dk hareketsizi atar).

**Orjinal Komutu:** /setidletimeout - Minecraft vanilla komutu.

### /setworldspawn
**Ne ise yarar:** Dunyanin dogus noktasini ayarlarsin.
**Ornek:** `/setworldspawn 0 70 0` (tasiyabilirsin).
**Dikkat:** Havaya ya da lava koyma.

**Orjinal Komutu:** /setworldspawn - Minecraft vanilla komutu.

### /spawnpoint
**Ne ise yarar:** Oyuncunun dogus noktasini ayarlarsin.
**Ornek:** `/spawnpoint Ahmet 0 70 0` (ayarlarsin).

**Orjinal Komutu:** /spawnpoint - Minecraft vanilla komutu.

### /spectate
**Ne ise yarar:** Izleyici modda birini takip edersin.
**Ornek:** `/spectate Ahmet` (izlersin).

**Orjinal Komutu:** /spectate - Minecraft vanilla komutu.

### /spreadplayers
**Ne ise yarar:** Oyunculari alana dagitirsin.
**Ornek:** `/spreadplayers 0 0 100 500 false @a` (dagitirsin).
**Dikkat:** Lava bosluga dusurebilir.

**Orjinal Komutu:** /spreadplayers - Minecraft vanilla komutu.

### /stop
**Ne ise yarar:** Sunucuyu guvenli kapatirsin.
**Ornek:** Once `/save-all`, sonra `/stop`.
**Dikkat:** EliteMobs takilirsa 90sn bekle, sonra taskkill.

**Orjinal Komutu:** /stop - Minecraft vanilla komutu.

### /stopsound
**Ne ise yarar:** Calan sesi durdurursun.
**Ornek:** `/stopsound Ahmet master minecraft:bell` (kesersin).

**Orjinal Komutu:** /stopsound - Minecraft vanilla komutu.

### /summon
**Ne ise yarar:** Belirtilen canliyi dogurursun.
**Ornek:** `/summon zombie 0 70 0` (zombi cikarirsin).
**Dikkat:** Cok sayida lag yapar.

**Orjinal Komutu:** /summon - Minecraft vanilla komutu.

### /tag
**Ne ise yarar:** Oyuncu ve canlilara etiket eklersin.
**Ornek:** `/tag Ahmet add admin` (etiketlersin).

**Orjinal Komutu:** /tag - Minecraft vanilla komutu.

### /team
**Ne ise yarar:** Takim olusturur yonetirsin.
**Ornek:** `/team add mavi` (takim kurarsin).

**Orjinal Komutu:** /team - Minecraft vanilla komutu.

### /teammsg
**Ne ise yarar:** Takima ozel mesaj gonderirsin.
**Ornek:** `/teammsg Toplanin` (takima atarsin).

**Orjinal Komutu:** /teammsg - Minecraft vanilla komutu.

### /teleport
**Ne ise yarar:** Oyuncuyu koordinata ya da oyuncuya isinlarsin.
**Ornek:** `/teleport Ahmet 0 70 0` (isinlarsin).

**Orjinal Komutu:** /teleport - Minecraft vanilla komutu.

### /tellraw
**Ne ise yarar:** Tiklanabilir mesaj gonderirsin.
**Ornek:** `/tellraw @a Bakim var` (formatli atarsin).

**Orjinal Komutu:** /tellraw - Minecraft vanilla komutu.

### /test
**Ne ise yarar:** Test komutlarini calistirirsin.
**Ornek:** `/test run testim` (calistirirsin).

**Orjinal Komutu:** /test - Minecraft vanilla komutu.

### /tick
**Ne ise yarar:** Tick hizini yonetirsin.
**Ornek:** `/tick freeze` (oyunu dondurursun).
**Dikkat:** Acik unutursan herkes donar.

**Orjinal Komutu:** /tick - Minecraft vanilla komutu.

### /title
**Ne ise yarar:** Ekrana buyuk baslik gosterirsin.
**Ornek:** `/title @a title Bakim` (herkes gorur).

**Orjinal Komutu:** /title - Minecraft vanilla komutu.

### /tm
**Ne ise yarar:** Teknik islem calistirirsin.
**Ornek:** `/tm durum` (cikti verir).

**Orjinal Komutu:** /tm - Minecraft vanilla komutu.

### /transfer
**Ne ise yarar:** Oyuncuyu baska sunucuya tasiyabilirsin.
**Ornek:** `/transfer Ahmet mc.ornek.com` (gonderirsin).
**Dikkat:** Bu sunucudan duser.

**Orjinal Komutu:** /transfer - Minecraft vanilla komutu.

### /trigger
**Ne ise yarar:** Oyuncunun skor tetikleyicisini calistirir. (Oyuncu da kullanabilir.)
**Ornek:** `/trigger gorev set 1` (skoru ayarlarsin).

**Orjinal Komutu:** /trigger - Minecraft vanilla komutu.

### /weather
**Ne ise yarar:** Havayi degistirirsin.
**Ornek:** `/weather clear` (havayi acarsin).

**Orjinal Komutu:** /weather - Minecraft vanilla komutu.

### /whitelist
**Ne ise yarar:** Beyaz listeyi yonetirsin (bakim modu).
**Ornek:** `/whitelist on` (yeni girisleri engellersin).
**Dikkat:** Kendini disarida birakma.

**Orjinal Komutu:** /whitelist - Minecraft vanilla komutu.

### /worldborder
**Ne ise yarar:** Dunya sinirini ayarlarsin.
**Ornek:** `/worldborder set 5000` (sinir koyarsin).
**Dikkat:** Cok kucultursen bogar.

**Orjinal Komutu:** /worldborder - Minecraft vanilla komutu.

### /xp
**Ne ise yarar:** Tecrube verirsin.
**Ornek:** `/xp add Ahmet 10 levels` (10 seviye verirsin).

**Orjinal Komutu:** /xp - Minecraft vanilla komutu.

### /op
**Ne ise yarar:** Oyuncuya tam yetki verirsin.
**Ornek:** `/op Ahmet` (tam kontrol verirsin).
**Dikkat:** Tek adminli sunucuda kimseye verme.

**Orjinal Komutu:** /op - Minecraft vanilla komutu.

## 28-) Admin ve Sunucu Islemleri
Sunucu bakimi, cekirdek, yetki ve guvenli kapatma komutlari.

### /chunkinfo
**Ne ise yarar:** Bulundugun chunk bilgisini verir.
**Ornek:** `/chunkinfo` (koordinat ve yuku gorursun).

**Orjinal Komutu:** /chunkinfo - sunucu veya cekirdek admin komutu.

### /spark
**Ne ise yarar:** Lag nedenini olcersin.
**Ornek:** `/spark tps` (TPS degerini gorursun).

**Orjinal Komutu:** /spark - sunucu veya cekirdek admin komutu.

### /mspt
**Ne ise yarar:** Tick suresini milisaniye gosterir.
**Ornek:** `/mspt` (degeri gorursun).

**Orjinal Komutu:** /mspt - sunucu veya cekirdek admin komutu.

### /tps
**Ne ise yarar:** TPS degerini gosterir (20 ideal).
**Ornek:** `/tps` (lag varsa duser).

**Orjinal Komutu:** /tps - sunucu veya cekirdek admin komutu.

### /paper
**Ne ise yarar:** Cekirdek surum bilgisini gosterir.
**Ornek:** `/paper version` (surumu dogrularsin).

**Orjinal Komutu:** /paper - sunucu veya cekirdek admin komutu.

### /purpur
**Ne ise yarar:** Purpur surumunu gosterir.
**Ornek:** `/purpur version` (26.1.2 buildini dogrularsin).

**Orjinal Komutu:** /purpur - sunucu veya cekirdek admin komutu.

### /spigot
**Ne ise yarar:** Spigot ayarlarini gosterir.
**Ornek:** `/spigot version` (surumu gorursun).

**Orjinal Komutu:** /spigot - sunucu veya cekirdek admin komutu.

### /timings
**Ne ise yarar:** Hangi pluginin lag yaptigini bulur.
**Ornek:** `/timings on` (olcumu baslatirsin).

**Orjinal Komutu:** /timings - sunucu veya cekirdek admin komutu.

### /version (ver)
**Ne ise yarar:** Sunucu ve plugin surumunu gosterir.
**Ornek:** `/version Essentials` (surumu gorursun).

**Orjinal Komutu:** /version (ver) - sunucu veya cekirdek admin komutu.

### /about
**Ne ise yarar:** Plugin adi ve surumunu gosterir.
**Ornek:** `/about WorldEdit` (bilgiyi gorursun).

**Orjinal Komutu:** /about - sunucu veya cekirdek admin komutu.

### /setspawn
**Ne ise yarar:** Sunucu dogus noktasini ayarlarsin.
**Ornek:** `/setspawn` (durdugun yer spawn olur).
**Dikkat:** Herkesi etkiler.

**Orjinal Komutu:** /setspawn - sunucu veya cekirdek admin komutu.

### /settpr
**Ne ise yarar:** Rastgele isinlanma alanini ayarlarsin.
**Ornek:** `/settpr 5000` (alani 5000 yaparsin).

**Orjinal Komutu:** /settpr - sunucu veya cekirdek admin komutu.

### /deop
**Ne ise yarar:** OP yetkisini alirsin.
**Ornek:** `/deop Ahmet` (yetkiyi geri alirsin).
**Dikkat:** Kendi OP'ni alirsan konsoldan geri verirsin.

**Orjinal Komutu:** /deop - sunucu veya cekirdek admin komutu.

