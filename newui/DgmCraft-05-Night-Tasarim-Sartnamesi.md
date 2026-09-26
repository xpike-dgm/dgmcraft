# DgmCraft · 05-night arayüz uygulama şartnamesi

**Belge türü:** Tasarım ve ön yüz uygulama şartnamesi  
**Hedef uygulama:** Mevcut PySide6 / QSS masaüstü uygulaması  
**Kapsam:** Sekiz ana sayfa, yedi kurulum adımı, dosya denetimi durumu ve zorunlu güncelleme ekranı  
**Referans çözünürlük:** 1280 × 800 px  
**Tasarım kaynağı:** Bu belgeyle birlikte verilen `dgmcraft-six/05-night/` görselleri ve SVG varlıkları

## 1. Görev tanımı

Mevcut uygulamanın **yalnızca görünür arayüzünü** 05-night tasarımına dönüştür. Sunucu başlatma, veri okuma, bağlantı, eşitleme, güncelleme ve benzeri mevcut işlevleri koru; bunların iş mantığını bu belgeden türetme. Mevcut sinyalleri, servisleri, veri modellerini ve hata akışlarını inceleyip yeni arayüzdeki karşılıklarına bağla. Mockup görsellerindeki örnek sayılar, isimler ve durumlar gerçek veri kaynağı değildir.

05-night tasarımının kimliği bütün ekranlarda aynıdır: çok koyu antrasit zemin, siyaha yakın vurgu alanları, beyaz ana metin, **#FF9B2C** turuncu aksan, üstte yatay gezinme ve gerçek DgmCraft amblemi. Ana sayfalara eski dikey sol çubuğu taşıma. Kurulum ekranını küçük ayrı bir sihirbaz penceresine dönüştürme; ana uygulamayla aynı 1280 × 800 referans alanını kullan.

**Görsel öncelik sırası:** 05-night ekran PNG'leri → bu şartnamedeki ölçüler ve renkler → mevcut uygulamanın işlevsel gereksinimleri. PNG'lerdeki içerik statiktir; uygulamada gerçek veriler ve durumlar gösterilmelidir.

## 2. Teslim edilecek kapsam

| No | Görünüm | Referans PNG |
|---:|---|---|
| 01 | Hub | `dgmcraft-six/05-night/01-hub.png` |
| 02 | Komutlar | `dgmcraft-six/05-night/02-komutlar.png` |
| 03 | Durum | `dgmcraft-six/05-night/03-durum.png` |
| 04 | Konsol | `dgmcraft-six/05-night/04-konsol.png` |
| 05 | Görevler | `dgmcraft-six/05-night/05-gorevler.png` |
| 06 | Yetenekler | `dgmcraft-six/05-night/06-yetenekler.png` |
| 07 | Sıralama | `dgmcraft-six/05-night/07-siralama.png` |
| 08 | Ayarlar | `dgmcraft-six/05-night/08-ayarlar.png` |
| 09–15 | Kurulum: Hoş geldin, Adın, Davet kodun, Dosya eşitleme, Gizli ağ, Arkadaşlar, Hazır | `dgmcraft-six/05-night/09-…15-…png` |
| 16 | Dosya denetimi sürerken kurulum | `dgmcraft-six/05-night/16-kurulum-kontrol-ediliyor.png` |
| 17 | Zorunlu güncelleme | `dgmcraft-six/05-night/17-guncelleme.png` |

Hızlı karşılaştırma için `dgmcraft-six/05-night/00-ana-sayfalar.png` ve `00-kurulum-guncelleme.png` kullanılabilir. Son kontrolü **tekil, tam çözünürlüklü PNG'lerle** yap; kolajlar küçük gösterildiği için ayrıntı doğrulamasına uygun değildir.

## 3. Tasarım sistemi

### 3.1 Renk değişkenleri

| Ad | Değer | Kullanım |
|---|---|---|
| `background` | `#111517` | Sayfa zemini |
| `surface` | `#1B2225` | Standart kart, liste ve giriş yüzeyi |
| `surfaceRaised` | `#252B2E` | Seçili liste satırı, ikincil vurgu alanı |
| `surfaceBlack` | `#080B0D` | Üst çubuk, yüksek kontrastlı paneller, alt işlem şeridi |
| `accent` | `#FF9B2C` | Birincil düğme, aktif sekme, ilerleme, ikon, önemli sayı |
| `textPrimary` | `#F4F5F1` | Başlık ve temel metin |
| `textSecondary` | `#B0B8B8` | Açıklama, yardımcı bilgi, ikincil değer |
| `border` | `#3A4346` | Standart kart ve alan kenarı |
| `blackOnAccent` | `#080B0D` | Turuncu zemin üzerindeki metin |

**Özel tonlar:** Siyah panellerdeki bölücüler yaklaşık `#505657`–`#5A6060`, pasif nav metni `#CED0D0`, konsolun nötr zaman damgası `#838B8A`, konsol uyarısı `#F2B46E`. Bunları başka renk ailesine çevirmeden, gerektiği yerde kullan.

Durum anlamını yalnızca renkle verme; metin/ikon da göster. Özellikle "sunucu kapalı", "bağlı değil", "denetim sürüyor" ve "hazır" durumları açık yazılmalı. Genel palete yeni yeşil, mavi veya mor aksan ekleme.

### 3.2 Tipografi, boşluk ve biçim

- Yazı ailesi: **Segoe UI**; sistemde yoksa benzer okunabilir sans serif. Tipografi tamamen uygulama içi doğal metindir, görsele gömülü metin değildir.
- Üst marka: yaklaşık **18 pt kalın**. Sayfa ana başlığı: **28 pt kalın**. Büyük hero başlığı: **32 pt kalın**. Büyük metrikler: **22–48 pt**. Kart başlıkları: **13–20 pt**. Standart içerik: **11–12 pt**. Üst etiketler: **9–10 pt kalın** ve büyük harf.
- Dış sayfa payı: solda ve sağda **36 px**. Çoğu kart iç payı **18–24 px**. Bileşen arası temel boşluk **10–18 px**.
- Kart radius: **4 px**; giriş alanı ve düğme radius: **4 px**; kapsül/progress yapıları yalnızca referanstaki yerlerde daha yuvarlak. Bu tasarımın karakteri keskin, derli toplu köşelerdir.
- Standart kart kenarı: **1 px `border`**. Siyah panellerde dış kenar görünmeyebilir. Ayrıştırma için gereksiz gölge, blur, cam efekti veya doku ekleme.
- Birincil düğme: `accent` zemin + `blackOnAccent` kalın yazı. İkincil düğme: `surface` zemin + açık yazı + ince kenar. Kontrast düğmesi: `surfaceBlack` zemin + açık yazı. Giriş odak kenarı: **2 px turuncu**.
- İlerleme çubuğu: pasif hat koyu gri, dolu bölüm `accent`. Yüzdeler ve kalan miktar gerçek veriye göre güncellenir.

### 3.3 Paylaşılan uygulama çerçevesi

- Referans pencere/tuval: **1280 × 800 px**. Yeniden boyutlandırılabilir mevcut uygulama varsa bu oran ve hiyerarşi korunarak uyarlanır; 1280 × 800 kabul ekranıdır. Windows ölçekleme/DPI koşullarında kırpma olmamalı.
- Üst çubuk: **82 px** yüksekliğinde `surfaceBlack`; alt sınırda **3 px turuncu çizgi**. Logo solda yaklaşık `x=25, y=19, 43×43`, yanında `DGMCRAFT` yazısı. Sağdaki oyuncu alanı bir ayırıcı, turuncu durum noktası, isim ve açılır ok içerir.
- Yatay gezinme sırası ve metni **her ana sayfada aynı**: Hub, Komutlar, Durum, Konsol, Görevler, Yetenekler, Sıralama, Ayarlar. Gezinme simgeleri `05-night/assets/*.svg` dosyalarından gelir; yaklaşık **17×17 px**. Etkin sayfanın metni turuncudur ve altında kısa **4 px turuncu çizgi** bulunur.
- Başlık alanı: `x=36` başlangıç; üst küçük etiket yaklaşık `y=102`, ana başlık `y=123`, açıklama `y=170`. Sağ üstte `DGMCRAFT / SAYFA ADI` yardımcı etiketi görünür. Ana içerik çoğunlukla `y=217` ile başlar.
- Aynı amblemi bütün ekranlarda kullan. Markayı farklı çizimlerle yeniden oluşturma.

**Önemli uygulama ayrıntısı:** Referans bir görsel makettir; üst çubuktaki sekmeler ve düğmeler gerçek PySide6 widget'ları olmalı. Eğer uygulama çerçevesiz pencere kullanıyorsa mevcut taşıma/küçültme/kapatma davranışlarını üst çubukla uyumlu biçimde koru. İşletim sisteminin doğal başlık çubuğu kullanılacaksa içerikte ikinci bir sahte başlık çubuğu üretme.

### 3.4 Varlıklar

- Asıl marka amblemi: `C:\Users\Xpike\Desktop\DgmCraft-Assets\01-Brand\DgmCraft-mark-orange-black-white.png`.
- Uygulama simgesi gerektiğinde aynı klasördeki `DgmCraft-app-icon.ico`.
- 05-night'e özel **12 SVG**: `assets/hub.svg`, `komutlar.svg`, `durum.svg`, `konsol.svg`, `gorevler.svg`, `yetenekler.svg`, `siralama.svg`, `ayarlar.svg`, `search.svg`, `player.svg`, `arrow.svg`, `download.svg`.
- SVG'ler 24×24 koordinat sistemiyle hazırlanmış, `#FF9B2C` çizgili, `#17191A` iç zeminli ve yuvarlak uçludur. Üst gezinmede yaklaşık 17×17 gösterilir. Gerekli diğer küçük simgeleri aynı çizgi kalınlığı ve renkle üret; Emoji veya rastgele sistem simgesi karıştırma.
- Bu dosyaları proje içine taşınabilir bir `assets`/Qt resource konumuna al. Kullanıcının masaüstündeki mutlak yolu çalışma zamanı bağımlılığı yapma.

## 4. Sayfa şartnameleri

### 4.1 Hub — `01-hub.png`

Başlık "Dünyan hazır.". İlk satırda solda yaklaşık **756×262 px** siyah hero, sağda yaklaşık **436×262 px** turuncu oyuncu/durum kartı yer alır. Hero'nun solunda 8 px turuncu şerit, büyük iki satırlı mesaj, kısa sunucu açıklaması, "Sunucuyu başlat" birincil düğmesi ve sağ tarafında gerçek amblem vardır. Turuncu kartta çevrimiçi oyuncu sayısı büyük tipografiyle, altında bağlantı durumu görünür.

Alt satır üç karttır: RAM/bellek ayarı, sunucu sürümü ve klasör bağlantısı, haberler. Bellek kartı gerçek değerle dolan ilerleme/ayar denetimi içerir. Başlatma ve bellek kontrolleri mevcut davranışlara bağlanmalı. Sunucu çalışırken ve kapalıyken yazı, düğme durumu ve çevrimiçi sayı anlamlı şekilde değişmeli.

### 4.2 Komutlar — `02-komutlar.png`

Sayfa başlığının altında tam genişlikte **57 px siyah arama bandı** vardır. Arama kutusu yazdıkça komut listesini süzer. Bunun altında yatay kategori düğmeleri bulunur; seçili kategori turuncu. Alt bölüm yaklaşık **793 px genişlikte komut listesi** ve **397 px genişlikte siyah detay paneli** olarak ayrılır. Listede komut, kısa açıklama ve sağ ok; seçilende koyu yükseltilmiş satır ve 4 px turuncu sol çizgi bulunur. Detay paneli seçili komutun adı, açıklaması, kategorisi ve kopyalama düğmesini gösterir.

Gerçek kategori/komut sayısını kullan; mockuptaki "24 KOMUT" örnektir. Uzun komut açıklamaları kırpılmadan okunabilmeli; liste kaydırılabilir olmalı. Kopyalama düğmesi mevcut panoya kopyalama işlevine bağlanır.

### 4.3 Durum — `03-durum.png`

İlk içerik satırı **1208×132 px siyah metrik bandı**: TPS, MSPT, Bellek, Oyuncular; aralarında ince dikey ayırıcılar. Her metrikte turuncu küçük başlık, büyük açık değer, alt açıklama bulunur. Alt bölüm solda yaklaşık **786×398 px TPS geçmiş kartı**, sağda yaklaşık **404×398 px sistem bilgisi kartı**. Grafik mevcut örnekleri görselleştirir; şematik mockup çubukları sabit veri olarak bırakılmamalı. Sağ kartta motor, sürüm, çalışma süresi, yüklü chunk, boş disk ve RCON satırları bulunur.

Sunucu kapalıysa başlık altında açıkça "son ölçüm" bilgisi görünür. Ölçüm yoksa boş durum ve uygun metin kullan; hayali değer gösterme.

### 4.4 Konsol — `04-konsol.png`

Tek büyük **1208×548 px siyah panel**; üstte "SUNUCU ÇIKTISI" ve bağlantı durumu, ortada zaman damgalı günlük akışı, altta giriş ve Gönder/Temizle düğmeleri. Panel içindeki alt ayrım ve zaman damgaları görünür; komut satırı **48 px** yüksekliğindedir. Günlükler gerçek zamanlı eklenir, seçim/kopyalama mümkündür, çok satır olduğunda kaydırılır. Komut girişi Enter ile ve Gönder düğmesiyle çalışır. Uygun olmayan bağlantı durumunda gönderme davranışı mevcut uygulamanın mantığına göre devre dışı bırakılır veya hata gösterir. "Temizle" mevcut konsol temizleme davranışına bağlanır.

### 4.5 Görevler — `05-gorevler.png`

Üstte **1208×108 px siyah ilerleme bandı**: tamamlanan / toplam görev, yatay ilerleme, yüzde, bölüm sayısı ve oynanabilir görev sayısı. İkinci satırda bölüm seçme düğmeleri ve sağda görev arama kutusu. Alt bölüm solda yaklaşık **735×333 px** görev listesi; sağda yaklaşık **455×333 px siyah seçili görev paneli**. Seçili görev koyu satır ve turuncu sol çizgiyle ayrılır. Her görev satırında sıra, ad ve durum; ayrıntıda bölüm/numara, başlık, hedef, ödül, takip ve başlatma işlemleri bulunur.

Uygulamada 750+ görev olduğu için liste **veri güdümlü ve kaydırılabilir** olmalı. Bölüm değiştirme, arama ve durum filtreleri mevcut veriyle çalışmalı. Görev sayısı, kilitli/oynanabilir/tamamlanan durumu ve ilerleme gerçek veriden gelmeli. Ayrıntıda uzun açıklamalar, birden fazla hedef, ön koşullar ve çoklu ödüller gerektiğinde panel kendi içinde kaydırılmalı; içerik sessizce kesilmemeli. Görevi başlat, takip et ve seç işlemleri mevcut akışlara bağlanmalı. Mockup yalnızca yoğunluk ve görünümü gösterir; ilk altı görev satırını sabitleme.

### 4.6 Yetenekler — `06-yetenekler.png`

Üstte **1208×101 px siyah özet bandı**: açık yetenek sayısı, toplam seviye, sonraki açılma bilgisi. Altında arama alanı. Yeteneği gösteren kartlar **4 sütun**, yaklaşık **290×82 px**, yatayda 15 px, dikeyde 12 px aralıkla dizilir. Seçili yetenek turuncu zemin ve koyu metinle; diğerleri standart koyu kartla gösterilir. Kartta ad, seviye, XP çubuğu ve XP sayısı bulunur. En altta **1208×94 px siyah seçili yetenek bandı**; XP, kalan XP ve ayrıntı düğmesi yer alır.

Yetenek sayısı değişebilir; kart alanı kaydırılabilir olmalı. XP eşikleri ve seviye değerleri örnek metinlerden türetilmez. Arama ve seçim gerçek veriye bağlıdır.

### 4.7 Sıralama — `07-siralama.png`

Üstte dört yatay kategori sekmesi: En zengin, En son oynayan, En uzun oynayan, En yetenekli. Seçili sekme turuncu. Altta solda yaklaşık **779×478 px** ana sıralama kartı, sağda yaklaşık **411×478 px siyah "Diğer zirveler" kartı**. Ana kartta kategori başlığı, veri kaynağı, ilk sıra için vurgulu siyah satır, oyuncu/değer alanları ve Yenile işlemi bulunur. Sağ kart üç özet sıralama gösterir. Kişi sayısı arttığında tek oyunculu mockup yapısı listeye genişlemeli; boş veri durumunda uygun açıklama çıkmalı. Veri kaynağı ve güncelleme zamanı gerçek olmalı.

### 4.8 Ayarlar — `08-ayarlar.png`

İçerikte solda yaklaşık **245×548 px siyah bölüm menüsü**, sağda yaklaşık **945×548 px ana ayar kartı**. Bu iç menü, uygulamanın üstteki ortak yatay gezinmesinin yerine geçmez. Seçili "Profil" satırı turuncudur. Sağ panelde Profil, Arkadaş bağlantısı, Uygulama ve güncelleme bölümleri ince çizgilerle ayrılır. Oyuncu adı alanı/Kaydet, bağlantı durumu/Bağlan/Kurulum sihirbazı, sürüm/klasör açma/güncelleme denetleme kontrolleri bulunur. Alanları mevcut ayar verisine ve işlemlerine bağla. Kayıt hatası, bağlantı hatası ve işlem sürerken uygun durum mesajları göster.

## 5. Kurulum akışı — ana pencereyle aynı boyut

Kurulumun **bütün adımları 1280 × 800 px referans alanında** açılır. Ortak 82 px üst çubukta logo, "KURULUM" ve "7 ADIMDA HAZIR" görünür. `x=36,y=103` konumunda yaklaşık **1208×84 px yatay 7 adımlı ilerleme satırı** bulunur. Tamamlanan ve etkin adımlar turuncu, henüz gelinmeyen adımlar koyu/nötrdür. Ana gövde solda yaklaşık **787×529 px** giriş/içerik kartı, sağda yaklaşık **403×529 px siyah marka/açıklama kartı** olarak kurulur. Sağ kartta aynı amblem, turuncu üst yazı, büyük başlık ve kısa yardım metni yer alır. Altta **52 px siyah işlem şeridi**: adım numarası, Geri ve sağda turuncu Devam/Bitir düğmesi. Bütün adımlarda bu çerçeve korunur.

1. **Hoş geldin (`09-…png`)** — Üç açıklayıcı mini kart: adını belirle, bağlantıları hazırla, birlikte oyna. "Kuruluma başla" ile ilerler.
2. **Adın (`10-…png`)** — Oyuncu adı girişi. Boş değer doğrulanır; kayıt ve sonraki adıma geçiş mevcut akışla yapılır. Alan altındaki kısa bilgi kartı korunur.
3. **Davet kodun (`11-…png`)** — Kod girişi, Göster/gizle düğmesi, "Kodum yok, sonra ekle" seçeneği ve açıklama kartı. Gerekli atlama/onay koşullarını mevcut uygulama belirler; tasarım bu koşulların görünür sonucunu sunar.
4. **Dosya eşitleme (`12-…png`)** — Denetim kartı, ilerleme çubuğu, eşitleme başlatma düğmesi. Hazır olmayan durumda Devam pasif. **Denetim sürüyor (`16-…png`)** aynı ekranın ayrı durumu: yüzde/ilerleme hareket eder, ilgili kontroller geçici olarak pasiftir. Başarı ve hata durumlarını aynı görsel dilde ekle.
5. **Gizli ağ (`13-…png`)** — Bağlantı durumu, atanmış cihaz adresi/denetim sonucu ve yeniden denetleme düğmesi. Örnekte bağlı durumu gösterilmiştir; bağlantısız ve hata hallerini gerçek veriyle yansıt.
6. **Arkadaşlar (`14-…png`)** — İki cihaz kodu girişi, kendi kodunu kopyalama, eşleştirme, durum ve kod yoksa atlama. Uzun kodlarda girişi rahat kullanılabilir tut; tam kodu satır içinde kırpılmış örnek veriye dönüştürme.
7. **Hazır (`15-…png`)** — Dört özet satırı: oyuncu adı, dosya eşitleme, gizli ağ, arkadaş eşleşmesi. Gerçek sonuçlar ve "Bitir ve başla" işlemi. Tamamlanmamış izinli adımlar varsa bunları doğru durumla göster.

Adım geçişlerinde ekranın iskeleti ve üst/alt şeritler yer değiştirmemeli. Geri gidildiğinde girilmiş değerler korunmalı. Mevcut kurulumun zorunlu/isteğe bağlı adım mantığı değiştirilmemeli.

## 6. Zorunlu güncelleme — `17-guncelleme.png`

Aynı **1280 × 800 px** yüzey ve aynı marka başlığı kullanılır. Üst çubukta "GÜNCELLEME" ve "YENİ SÜRÜM HAZIR" metinleri bulunur; ana sayfa sekmeleri görünmez. Sol tarafta başlık, kısa açıklama, yaklaşık **560×277 px turuncu eski→yeni sürüm kartı**, altında büyük "Güncellemeyi başlat" düğmesi ve erişim notu yer alır. Sağ tarafta yaklaşık **617×627 px siyah sürüm notları kartı**; amblem, başlık ve maddeler vardır. Sürüm numaraları ve maddeler güncelleme verisinden gelir; örnek `v0.25.2 → v0.26.0` sabit bırakılmamalı. İndirme/kurulum sürerken ilerleme ve hata durumlarını bu ekranda gösterecek alanlar tasarla; mevcut zorunlu güncelleme kararını koru.

## 7. PySide6 / QSS uygulama yaklaşımı

1. **Ortak tema katmanı kur.** Yukarıdaki renkleri tek kaynakta tut; düğme, giriş, kart, sekme, metin, kenarlık, scrollbar, hover, pressed, focus ve disabled durumlarını QSS ile tanımla. Sayfalara dağılmış sabit renkleri azalt.
2. **Ortak bileşenleri gerçek widget olarak kur.** `AppHeader`, `PageHeading`, `SurfaceCard`, `Metric`, `ActionButton`, `Progress`, `EmptyState`, `WizardHeader/Stepper/Footer` gibi tekrar eden öğeleri tek tasarım kuralıyla üret. Mevcut proje mimarisinin adlandırmasına uyarlanabilir.
3. **Yerleşimi layout'larla kur.** PNG koordinatları 1280×800 referansıdır. PySide6'da `QHBoxLayout`, `QVBoxLayout`, `QGridLayout`, `QSplitter`/esnek alanlar, `QScrollArea` veya uygun liste modeli kullan. Bütün sayfayı sabit `setGeometry` çağrılarıyla kurmak gereksiz kırpma oluşturur. Minimum genişlik ve içerik alanı hesaplarıyla tasarım oranını koru.
4. **Büyük listeleri sanallaştır.** 750+ görev ve uzun komut listesi için `QListView`/model veya eşdeğer verimli yaklaşım uygula; her görev için yüzlerce kalıcı kart widget'ı yaratma. Seçim, arama ve filtreyi model katmanından besle. Görsel öğe çizimi gerekiyorsa delegate kullan.
5. **SVG varlıklarını yeniden kullan.** `QIcon`/`QSvgRenderer` veya Qt resources ile yükle. İkonlar net ve aynı boyda olmalı; rasterleştirme yapılıyorsa yüksek DPI için uygun çözünürlük kullan.
6. **Grafik ve özel ilerleme için Qt'nin uygun aracını kullan.** Durum sayfasındaki çubuk grafik `QPainter`/uygun grafik widget'ıyla; basit ilerleme `QProgressBar` + QSS veya hafif özel widget ile yapılabilir. Ana etkileşimler standart erişilebilir Qt kontrolleri olarak kalmalı.
7. **Canlı arayüz davranışlarını bağla.** Seçili nav ve sekme, fare üstü, klavye odağı, devre dışı durum, yükleniyor, başarı, hata ve boş veri halleri görünür olsun. "Çalışıyor" hissi için sahte animasyon ekleme; yalnızca gerçek işlem durumunu göster.
8. **İçerik ve metin uzunluklarına dayan.** Kullanıcı adı, bölüm adı, görev başlığı ve sürüm notları değişebilir. Kaydırma, uygun satır kırma ve tool tip kullan; tek satırlık görsel ölçüleri veri kaybına neden olmasın.

### Örnek tema çekirdeği

Bu parça tam stil dosyası değildir; renk ve temel durumların tutarlı kalması için başlangıç kuralıdır. Seçici adlarını uygulamanın widget `objectName`/özelliklerine göre tamamla.

```qss
QWidget {
    background-color: #111517;
    color: #F4F5F1;
    font-family: "Segoe UI";
}
QFrame[role="surface"] {
    background-color: #1B2225;
    border: 1px solid #3A4346;
    border-radius: 4px;
}
QFrame[role="blackSurface"] {
    background-color: #080B0D;
    border: 1px solid #080B0D;
    border-radius: 4px;
}
QPushButton[variant="primary"] {
    background-color: #FF9B2C;
    color: #080B0D;
    border: 1px solid #FF9B2C;
    border-radius: 4px;
    font-weight: 700;
    padding: 0 14px;
}
QPushButton[variant="secondary"] {
    background-color: #1B2225;
    color: #F4F5F1;
    border: 1px solid #3A4346;
    border-radius: 4px;
    padding: 0 14px;
}
QLineEdit {
    background-color: #1B2225;
    color: #F4F5F1;
    border: 1px solid #3A4346;
    border-radius: 4px;
    padding: 0 14px;
    selection-background-color: #FF9B2C;
    selection-color: #080B0D;
}
QLineEdit:focus { border: 2px solid #FF9B2C; }
```

Widget dinamik özellikleri değiştiğinde Qt stilini yeniden uygula. Butonların `hover`, `pressed`, `disabled` halleri ve `QScrollBar` stili proje genelinde ayrıca tanımlanmalı; referans tasarımın renkleri korunmalı.

## 8. Görsel ve işlevsel kabul ölçütleri

1. Sekiz ana sayfa, yedi kurulum adımı, denetim durumu ve güncelleme ekranı ayrı ayrı çalışır; toplam **17 görünüm** incelemeye hazırdır.
2. 1280×800 ve Windows %100/%125 ölçeklemede hiçbir temel metin, giriş, düğme veya durum kırpılmaz. Kurulum ekranı ana uygulamayla aynı pencere alanını kullanır.
3. Bütün ana sayfalarda aynı logo, 82 px üst çubuk, gezinme sırası, aktif çizgi, turuncu tonu, font hiyerarşisi ve kart biçimi vardır. Kurulum/güncelleme çerçevesi aynı markayı kullanır.
4. Turuncu yalnızca belirgin eylem, aktif seçim, değer veya vurgu içindir; geniş siyah/koyu yüzeyler ve açık yazı dengesi referansa yakındır. Eski tasarımdan dikey uygulama menüsü, farklı logo veya yeşil ana aksan kalmaz.
5. Görev/komut/yetenek araması, seçimler, gezinme, kopyalama, kurulum geri/ileri ve temel düğmeler mevcut gerçek işlevlerle bağlıdır. Örnek veriler sabit bırakılmaz.
6. Uzun listeler, boş veri, yükleniyor, başarı ve hata durumları tasarımla uyumlu, okunabilir ve kullanılabilirdir.
7. Ana ekranların ve kurulum/güncellemenin 1280×800 ekran görüntüleri, eşleşen 05-night referans PNG'leriyle yan yana gözden geçirilir; önemli yerleşim ve renk sapmaları düzeltilir.
8. Logo ve SVG'ler uygulama paketinde bulunur; başka bilgisayarda kullanıcı masaüstü yoluna bağımlılık olmadan yüklenir.

## 9. Yönetici AI için uygulama talimatı

> Mevcut PySide6 uygulama kodunu incele. İş mantığını koruyarak yalnızca görünür arayüzü bu şartname ve `05-night` referans PNG'leri doğrultusunda uygula. Önce ortak tema, üst gezinme ve varlıkları kur; ardından sekiz ana sayfa, yedi adımlı kurulum, denetim durumu ve güncelleme ekranını dönüştür. Gerçek veri ve mevcut eylemleri yeni bileşenlere bağla. 1280×800 ekran görüntüleri alarak referanslarla karşılaştır ve belirgin farklılıkları düzelt. Sonunda değişen dosyaları, çalıştırma yolunu ve varsa uygulama kodundan kaynaklanan kalan sınırlamaları bildir.

---

**Not:** `05-night` PNG'leri gerçek uygulama ekranları değil, PySide6 ile oluşturulmuş statik tasarım maketleridir. Bu belge yerleşim ve görünüm için bağlayıcıdır; kodun mevcut projeye uyarlanması ve canlı veri bağlantıları uygulama geliştirme işidir.
