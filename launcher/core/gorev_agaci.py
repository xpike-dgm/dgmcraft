"""F7 — Görev ağacı: 13 bölüm + 750 düğümlük harita ve oyuncu ilerlemesi.

İki kaynak birleştirilir:
- `gorevler.agac()`  → BeautyQuests'tan gelen GERÇEK görevler (dosya adı, ad,
  açıklama, ön koşul, oyuncu ilerlemesi)
- `ARSIVLER`        → 750 görevi taşıyan iskelet (bölüm + görev sayıları)

Görev dosyaları henüz yoksa iskelet gösterilir: harita boş değil, sadece
"tanım bekleniyor" durumunda çizilir. Dosyalar geldiğinde düğümler isim,
durum ve ödül bilgisini gerçek veriden alır; harita aynı yerde kalır.
"""
from . import gorevler

# Bölümler: (sıra, anahtar, ad, ana_görev, yan_görev, amblem, ozet)
ARSIVLER = [
    (0, "uyanis", "Uyanış", 28, 6, "tohum",
     "Gece çöker, üç ateş yanar. Dünya ilk kez kendini gösterir."),
    (1, "orman", "Orman Sözleşmesi", 36, 11, "agac",
     "Orman Bekçisi'nin dili çözülür: ağacın ne istediği."),
    (2, "kuyu", "Toprağın Altındaki Kuyu", 40, 13, "kuyu",
     "İlk derin kazı. Kuyunun dibi bir oda değil, bir kapı."),
    (3, "demir", "Demir Çağı", 42, 12, "demir",
     "Kor Ata'nın külleri dağılmadan önce demir toplanır."),
    (4, "kapilar", "Kızıl Kapılar", 44, 14, "kapi",
     "Nether'da üç kızıl kapı, üç ayrı bedel."),
    (5, "bogaz", "Boğaz", 44, 13, "dalga",
     "Suyun altında konuşan bir şey var; o da konuşmak istiyor."),
    (6, "kemik", "Kemik Bahçesi", 46, 12, "kemik",
     "Derin Kahin ölü değil. Ölü görünüyor."),
    (7, "kirik", "Gökyüzünün Kırığı", 46, 13, "yildiz",
     "End'e giden yol kırık. Kırık parçaları yerine oturtmak gerekiyor."),
    (8, "kardesler", "Kardeşler Arasında", 48, 14, "kardes",
     "Üç kardeş, üç ayrı yol, tek bir karar."),
    (9, "bosluk", "Boşluğun Ötesinde", 48, 12, "bosluk",
     "Boşluk Ejderi'nin ardında hiçbir şey yok. Hiç olmamak da bir yer."),
    (10, "kule", "Uyumsuz Kule", 48, 13, "kule",
     "Dikey bir kule, yatay bir dünya. Uyumsuzluğun mimarisi."),
    (11, "ay", "Kızıl Ay Odası", 50, 12, "ay",
     "Ay kızarır. O gece her şey hesaplanır."),
    (12, "final", "Üç Kardeş", 60, 5, "alev",
     "Üçü bir araya geliyor. Kalan tek soru: kim kazandı."),
    (13, "epilog", "Epilog", 0, 20, "yildiz",
     "Kapanmamış hesaplar, gönül rahatlığı, son ateş."),
]

TAURLER = ["agac", "kazma", "bugday", "balik", "kurek", "ok", "kalkan", "kilic",
           "bot", "iksir", "kitap", "elmas", "sandik", "anahtar", "goz", "tac",
           "portal", "kalp", "yildiz", "mesale"]

DURUM_TAMAM = "tamam"
DURUM_AKTIF = "aktif"
DURUM_KILITLI = "kilitli"
DURUM_TANIMSIZ = "tanimsiz"

DURUM_RENK = {
    DURUM_TAMAM: "#34D399",
    DURUM_AKTIF: "#F0A202",
    DURUM_KILITLI: "#3A4A43",
    DURUM_TANIMSIZ: "#2A3530",
}
DURUM_ETIKET = {
    DURUM_TAMAM: "TAMAMLANDI",
    DURUM_AKTIF: "OYNANABİLİR",
    DURUM_KILITLI: "KİLİTLİ",
    DURUM_TANIMSIZ: "TANIM BEKLENİYOR",
}

ARSIV_ADI = {a[1]: a[2] for a in ARSIVLER}
ARSIV_SIRA = {a[1]: a[0] for a in ARSIVLER}
ARSIV_AMBLEM = {a[1]: a[5] for a in ARSIVLER}
ARSIV_OZET = {a[1]: a[6] for a in ARSIVLER}

TOPLAM = sum(a[3] + a[4] for a in ARSIVLER)


# ---------------------------------------------------------------- iskelet ----
def iskelet():
    """750 düğümlük arşiv + görev listesi (dosyadan bağımsız)."""
    arsivler = []
    sayac = 0
    for sira, anahtar, ad, ana, yan, amblem, ozet in ARSIVLER:
        dugumler = []
        for i in range(ana + yan):
            sayac += 1
            dugumler.append({
                "no": sayac,
                "ad": "%s %03d" % (ad, i + 1),
                "arsiv": anahtar,
                "tur": TAURLER[(sayac * 7) % len(TAURLER)],
                "ana": i < ana,
            })
        arsivler.append({"sira": sira, "anahtar": anahtar, "ad": ad,
                         "amblem": amblem, "ozet": ozet,
                         "dugumler": dugumler, "toplam": len(dugumler)})
    return arsivler


def _onizleme(dugumler):
    """`--gorev-onizleme` için yapay ilerleme (yalnız görüntüleme)."""
    kurulu = 0
    for g in dugumler:
        if kurulu < 40:
            g["durum"] = DURUM_TAMAM
            g["ilerleme"] = [1, 1]
            kurulu += 1
        elif kurulu < 52:
            g["durum"] = DURUM_AKTIF
            g["ilerleme"] = [1, 2]
        else:
            g["durum"] = DURUM_KILITLI
            g["ilerleme"] = []


def agac(kok, uuid=None, onizleme=False):
    """Görev haritası döner: {arsivler, dugumler, ozet, gercek}."""
    gercek = gorevler.gorevleri_oku(kok)
    ilerleme = {}
    if uuid:
        try:
            ilerleme = gorevler.ilerleme_oku(kok, uuid)
        except Exception:
            ilerleme = {}

    arsivler = iskelet()
    gercek_kimlik = {g["id"]: g for g in gercek}
    gercek_ad = {}
    for g in gercek:
        numara = gorevler._tamsayi(g["id"])
        if numara:
            gercek_ad[numara] = g

    dugumler = []
    for arsiv in arsivler:
        for g in arsiv["dugumler"]:
            kaynak = gercek_ad.get(g["no"])
            g["id"] = g["no"]
            g["ad"] = (kaynak or {}).get("ad") or g["ad"]
            g["aciklama"] = (kaynak or {}).get("aciklama") or ""
            g["oncesi"] = (kaynak or {}).get("oncesi") or []
            g["objektif"] = (kaynak or {}).get("objektif_sayisi") or 0
            g["hedefler"] = (kaynak or {}).get("hedefler") or []
            g["odul"] = (kaynak or {}).get("oduller") or []
            g["gercek"] = kaynak is not None
            if kaynak is not None:
                kayit = ilerleme.get(kaynak["id"]) or {}
                if kayit.get("durum") == gorevler.DURUM_TAMAM:
                    g["durum"] = DURUM_TAMAM
                else:
                    g["durum"] = DURUM_AKTIF
                g["ilerleme"] = kayit.get("ilerleme") or []
            else:
                g["durum"] = DURUM_TANIMSIZ
                g["ilerleme"] = []
            dugumler.append(g)

    if onizleme and not gercek:
        _onizleme(dugumler)

    for arsiv in arsivler:
        arsiv["dugum"] = [g["no"] for g in arsiv["dugumler"]]

    ozet = _ozet(dugumler)
    return {"arsivler": arsivler, "dugumler": dugumler,
            "ozet": ozet, "gercek": len(gercek),
            "kimlikler": gercek_kimlik}


def _ozet(dugumler):
    toplam = len(dugumler)
    say = {DURUM_TAMAM: 0, DURUM_AKTIF: 0, DURUM_KILITLI: 0, DURUM_TANIMSIZ: 0}
    for g in dugumler:
        say[g["durum"]] = say.get(g["durum"], 0) + 1
    tanimli = toplam - say[DURUM_TANIMSIZ]
    return {"toplam": toplam, "tanimli": tanimli, "bolum": len(ARSIVLER),
            "tamam": say[DURUM_TAMAM], "aktif": say[DURUM_AKTIF],
            "kilitli": say[DURUM_KILITLI], "oran": (tanimli / float(toplam or 1))}
