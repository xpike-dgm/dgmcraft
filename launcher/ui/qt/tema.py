"""05-night tasarım sistemi: tek renk/ölçü kaynağı + ortak bileşenler.

Mevcut iş mantığına dokunmaz; yalnızca görünür arayüzü üretir.
Referans: 1280 x 800 px, yatay üst gezinme, #FF9B2C aksan.
"""
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QColor, QFont, QFontDatabase, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)

GENISLIK = 1280
YUKSEKLIK = 800
GOLGE = 22
UST_YUKSEKLIK = 82
IC_PAY = 36
BOSLUK = 18
KART_ARALIK = 14
IKON = 17
NAV_YUKSEKLIK = 82

# --- 05-night palet (şartname 3.1) ---
BG = "#111517"
YUZEY = "#1B2225"
YUZEY_ACIK = "#252B2E"
SIYAH = "#080B0D"
VURGU = "#FF9B2C"
YAZI = "#F4F5F1"
IKINCIL = "#B0B8B8"
CERCEVE = "#3A4346"
VURGU_YAZI = "#080B0D"

# --- özel tonlar (şartname 3.1) ---
BOLUCU = "#545B5C"
BOLUCU_ACIK = "#5A6060"
PASIF_NAV = "#CED0D0"
KONSOL_ZAMAN = "#838B8A"
KONSOL_UYARI = "#F2B46E"

UYGULAMA = "DgmCraft"
YAZI_TIPI = "Segoe UI"

# --- 05-night'e dönüş sırasında eski adları yeni palete eşler ---
# Sayfalar tek tek dönüştürülürken hiçbir ekran eski palete düşmesin diye.
SOLUK = IKINCIL
SILIK = IKINCIL
KART = YUZEY
KART_ACIK = YUZEY_ACIK
CERCEVE_PARLAK = VURGU
VURGU_HOVER = "#FFAE4F"
YESIL = "#5FC27E"
KIRMIZI = "#F07167"
MAVI = "#8FB8E8"
RAY_GENISLIK = 0
HERO_UST = SIYAH
HERO_ALT = SIYAH

NAV_SIRASI = [
    ("hub", "Hub", "hub"),
    ("komutlar", "Komutlar", "komutlar"),
    ("durum", "Durum", "durum"),
    ("konsol", "Konsol", "konsol"),
    ("gorevler", "Görevler", "gorevler"),
    ("yetenekler", "Yetenekler", "yetenekler"),
    ("siralama", "Sıralama", "siralama"),
    ("ayarlar", "Ayarlar", "ayarlar"),
]


def fontlar_yukle():
    """Segoe UI sistemde varsa kullanılır; yoksa okunabilir sans serif'e düşer."""
    return ["Segoe UI", "Inter", "Arial"]


def qss():
    return """
* { outline: 0; }
QWidget {
    background: transparent; color: %(yazi)s;
    font-family: "Segoe UI", "Inter", "Arial"; font-size: 12px;
}

#pencere { background: %(siyah)s; border: 1px solid #0E1214; }
#sayfa { background: %(bg)s; }
#ustCubuk {
    background: %(siyah)s; border: none;
    border-bottom: 3px solid %(vurgu)s;
}
#markaAd {
    font-size: 18px; font-weight: 700; color: %(yazi)s; letter-spacing: 1px;
}
#markaAlt {
    font-size: 10px; font-weight: 700; color: %(vurgu)s; letter-spacing: 2px;
}
#oyuncuAd { font-size: 12px; font-weight: 600; color: %(yazi)s; }
#sayfaEtiket { font-size: 12px; font-weight: 700; color: %(vurgu)s; letter-spacing: 1px; }
#ustYazi {
    font-size: 10px; font-weight: 700; color: %(vurgu)s; letter-spacing: 2px;
}
#sayfaBaslik { font-size: 28px; font-weight: 700; color: %(yazi)s; }
#sayfaAciklama { font-size: 12px; color: %(ikincil)s; }
#yardimciEtiket {
    font-size: 10px; font-weight: 700; color: %(ikincil)s; letter-spacing: 1px;
}

/* --- kartlar --- */
QFrame#kart {
    background: %(yuzey)s; border: 1px solid %(cerceve)s; border-radius: 4px;
}
QFrame#siyahKart {
    background: %(siyah)s; border: 1px solid %(siyah)s; border-radius: 4px;
}
QFrame#vurguKart {
    background: %(vurgu)s; border: 1px solid %(vurgu)s; border-radius: 4px;
}
QFrame#icKutu {
    background: %(yuzeyAcik)s; border: 1px solid %(cerceve)s; border-radius: 4px;
}
QFrame#bolucu { background: %(bolucu)s; border: none; max-height: 1px; }
QFrame#dikeyBolucu { background: %(bolucuAcik)s; border: none; max-width: 1px; }

/* --- tipografi --- */
QLabel#metrikEtiket {
    font-size: 10px; font-weight: 700; color: %(vurgu)s; letter-spacing: 1px;
}
QLabel#metrikDeger { font-size: 34px; font-weight: 700; color: %(yazi)s; }
QLabel#metrikAlt { font-size: 11px; color: %(ikincil)s; }
QLabel#kartBaslik { font-size: 15px; font-weight: 700; color: %(yazi)s; }
QLabel#bolumBaslik {
    font-size: 10px; font-weight: 700; color: %(vurgu)s; letter-spacing: 2px;
}
QLabel#metin { font-size: 12px; color: %(yazi)s; }
QLabel#ikincil { font-size: 12px; color: %(ikincil)s; }
QLabel#soluk { font-size: 11px; color: %(ikincil)s; }
QLabel#minik { font-size: 10px; color: %(ikincil)s; }
QLabel#komutAd { font-size: 13px; font-weight: 700; color: %(vurgu)s; }
QLabel#konsolZaman { font-size: 11px; color: %(konsolZaman)s; }
QLabel#konsolSatir { font-size: 12px; color: %(yazi)s; }
QLabel#konsolUyari { font-size: 12px; color: %(konsolUyari)s; }
QLabel#vurguYazi { font-size: 12px; font-weight: 700; color: %(vurguYazi)s; }
QLabel#vurguIkincil { font-size: 11px; color: #4A3208; }
QLabel#satirAd { font-size: 12px; font-weight: 600; color: %(yazi)s; }
QLabel#satirSag {
    font-size: 10px; font-weight: 700; color: %(ikincil)s; letter-spacing: 1px;
}
QLabel#listeBaslik {
    font-size: 10px; font-weight: 700; color: %(vurgu)s; letter-spacing: 2px;
}
QLabel#yetenekAd { font-size: 12px; font-weight: 600; color: %(yazi)s; }
QLabel#yetenekSeviye { font-size: 10px; color: %(ikincil)s; }
QLabel#yetenekXp { font-size: 10px; color: %(ikincil)s; }

/* --- hero / turuncu kart --- */
QLabel#heroBaslik { font-size: 32px; font-weight: 700; color: %(yazi)s; }
QLabel#heroMetin { font-size: 12px; color: %(ikincil)s; }
QLabel#rozetYazi { font-size: 10px; font-weight: 700; color: %(yazi)s; }
QLabel#vurguUst {
    font-size: 10px; font-weight: 700; color: %(vurguYazi)s; letter-spacing: 2px;
}
QLabel#vurguSayac { font-size: 48px; font-weight: 700; color: %(vurguYazi)s; }
QLabel#vurguAlt { font-size: 12px; color: #7A4E10; }
QLabel#vurguAltKalin { font-size: 12px; font-weight: 700; color: %(vurguYazi)s; }
QLabel#kartSayac { font-size: 34px; font-weight: 700; color: %(yazi)s; }
QLabel#kartSayacKucuk { font-size: 22px; font-weight: 700; color: %(yazi)s; }
QLabel#bolumAltBaslik { font-size: 13px; font-weight: 700; color: %(yazi)s; }
QLabel#kategoriAd { font-size: 12px; font-weight: 600; color: %(yazi)s; }
QLabel#kategoriSayi { font-size: 10px; font-weight: 700; color: %(ikincil)s; }
QLabel#komutDetayAd { font-size: 22px; font-weight: 700; color: %(yazi)s; }
QLabel#vurguSurum { font-size: 22px; font-weight: 700; color: %(vurguYazi)s; }
QLabel#vurguOk { font-size: 20px; font-weight: 700; color: %(vurguYazi)s; }
QLabel#sihirKartBaslik { font-size: 20px; font-weight: 700; color: %(yazi)s; }

/* --- düğmeler --- */
QPushButton[rol="ana"] {
    background: %(vurgu)s; color: %(vurguYazi)s; border: 1px solid %(vurgu)s;
    border-radius: 4px; font-weight: 700; padding: 0 16px;
}
QPushButton[rol="ana"]:hover { background: #FFAE4F; border-color: #FFAE4F; }
QPushButton[rol="ana"]:pressed { background: #E58620; }
QPushButton[rol="ana"]:disabled { background: #2A3033; color: #5A6467; border-color: #2A3033; }

QPushButton[rol="ikincil"] {
    background: %(yuzey)s; color: %(yazi)s; border: 1px solid %(cerceve)s;
    border-radius: 4px; padding: 0 14px;
}
QPushButton[rol="ikincil"]:hover { border-color: %(vurgu)s; color: %(vurgu)s; }
QPushButton[rol="ikincil"]:pressed { background: %(yuzeyAcik)s; }
QPushButton[rol="ikincil"]:disabled { color: #5A6467; border-color: #2A3033; }

QPushButton[rol="kontrast"] {
    background: %(siyah)s; color: %(yazi)s; border: 1px solid #1C2225;
    border-radius: 4px; padding: 0 14px;
}
QPushButton[rol="kontrast"]:hover { border-color: %(vurgu)s; color: %(vurgu)s; }
QPushButton[rol="kontrast"]:disabled { color: #4A5457; }

QPushButton[rol="sekme"] {
    background: transparent; color: %(ikincil)s; border: 1px solid %(cerceve)s;
    border-radius: 4px; font-weight: 600; padding: 7px 16px;
}
QPushButton[rol="sekme"]:hover { border-color: %(vurgu)s; color: %(yazi)s; }
QPushButton[rol="sekme"][secili="1"] {
    background: %(vurgu)s; color: %(vurguYazi)s; border-color: %(vurgu)s;
}

/* --- gezinme --- */
QPushButton#navDugme {
    background: transparent; border: none; border-bottom: 4px solid transparent;
    color: %(pasifNav)s; font-size: 12px; font-weight: 600;
    padding: 0 4px; text-align: left;
}
QPushButton#navDugme:hover { color: %(vurgu)s; }
QPushButton#navDugme[aktif="1"] { color: %(vurgu)s; border-bottom: 4px solid %(vurgu)s; }

/* --- girişler --- */
QLineEdit {
    background: %(yuzey)s; color: %(yazi)s; border: 1px solid %(cerceve)s;
    border-radius: 4px; padding: 8px 12px;
    selection-background-color: %(vurgu)s; selection-color: %(vurguYazi)s;
}
QLineEdit:focus { border: 2px solid %(vurgu)s; padding: 7px 11px; }
QLineEdit#aramaKutusu { background: %(siyah)s; padding: 10px 12px; }
QLineEdit#aramaKutusu:focus { border: 2px solid %(vurgu)s; padding: 9px 11px; }

/* --- ilerleme --- */
QProgressBar {
    background: #2A3235; border: none; border-radius: 3px; height: 6px;
}
QProgressBar::chunk { background: %(vurgu)s; border-radius: 3px; }
QProgressBar[rol="ince"] { height: 4px; }

/* --- liste satirlari --- */
QListWidget, QListView, QTreeWidget {
    background: transparent; border: none; outline: 0;
}
QListWidget::item { border: none; }
QListWidget::item:selected { background: transparent; }

QFrame#listeSatir {
    background: transparent; border: none; border-left: 4px solid transparent;
    border-radius: 0;
}
QFrame#listeSatir:hover { background: #1F2629; }
QFrame#listeSatir[secili="1"] { background: %(yuzeyAcik)s; border-left: 4px solid %(vurgu)s; }

QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { background: transparent; width: 10px; margin: 0; }
QScrollBar::handle:vertical {
    background: #39423F; border-radius: 5px; min-height: 30px; margin: 2px;
}
QScrollBar::handle:vertical:hover { background: %(vurgu)s; }
QScrollBar:horizontal { background: transparent; height: 10px; margin: 0; }
QScrollBar::handle:horizontal {
    background: #39423F; border-radius: 5px; min-width: 30px; margin: 2px;
}
QScrollBar::handle:horizontal:hover { background: %(vurgu)s; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }
QScrollBar::add-page, QScrollBar::sub-page { background: none; }

QTextBrowser#konsolMetin {
    background: transparent; border: none; color: %(yazi)s; font-size: 12px;
}
QTextEdit {
    background: transparent; border: none; color: %(yazi)s;
    selection-background-color: %(vurgu)s; selection-color: %(vurguYazi)s;
}

QToolTip {
    background: %(yuzeyAcik)s; color: %(yazi)s; border: 1px solid %(cerceve)s;
    padding: 5px 8px;
}

QComboBox {
    background: %(siyah)s; color: %(yazi)s; border: 1px solid %(cerceve)s;
    border-radius: 4px; padding: 6px 10px;
}
QComboBox:hover { border-color: %(vurgu)s; }
QComboBox::drop-down { border: none; width: 18px; }
QComboBox QAbstractItemView {
    background: %(yuzey)s; color: %(yazi)s;
    selection-background-color: %(vurgu)s; selection-color: %(vurguYazi)s;
    border: 1px solid %(cerceve)s;
}
""" % {
        "bg": BG, "yuzey": YUZEY, "yuzeyAcik": YUZEY_ACIK, "siyah": SIYAH,
        "vurgu": VURGU, "yazi": YAZI, "ikincil": IKINCIL, "cerceve": CERCEVE,
        "vurguYazi": VURGU_YAZI, "bolucu": BOLUCU, "bolucuAcik": BOLUCU_ACIK,
        "pasifNav": PASIF_NAV, "konsolZaman": KONSOL_ZAMAN,
        "konsolUyari": KONSOL_UYARI,
    }


# ==================================================================
# Ortak bileşenler
# ==================================================================

def svg_ikon(ad, boyut=IKON):
    """05-night SVG varlıklarından QIcon üretir. Bulunamazsa boş ikon."""
    try:
        from PySide6.QtSvg import QSvgRenderer
        from PySide6.QtCore import QByteArray
        from core import assets as A
        yol = A.yol("night", "%s.svg" % ad)
        renderer = QSvgRenderer(QByteArray(open(yol, "rb").read()))
        if not renderer.isValid():
            return QIcon()
        pm = QPixmap(boyut * 2, boyut * 2)
        pm.fill(Qt.transparent)
        boya = QPainter(pm)
        renderer.render(boya)
        boya.end()
        pm.setDevicePixelRatio(2.0)
        return QIcon(pm)
    except Exception:
        return QIcon()


def mark_pixmap(boyut=43):
    """Gerçek DgmCraft amblemi (mark.png)."""
    try:
        from core import assets as A
        pm = QPixmap(A.yol("night", "mark.png"))
        if pm.isNull():
            return QPixmap()
        return pm.scaled(boyut, boyut, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    except Exception:
        return QPixmap()


def diger_ikon_yap(path, boyut):
    """Eski varlık yollarını aynı boyutta QIcon yapan geri dönüş."""
    try:
        from PySide6.QtCore import QSize
        pm = QPixmap(path)
        if pm.isNull():
            return QIcon()
        return QIcon(pm.scaled(boyut * 2, boyut * 2,
                               Qt.KeepAspectRatio, Qt.SmoothTransformation))
    except Exception:
        return QIcon()


def ayirici(renk=BOLUCU, dikey=False):
    c = QFrame()
    if dikey:
        c.setObjectName("dikeyBolucu")
        c.setFixedWidth(1)
        c.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
    else:
        c.setObjectName("bolucu")
        c.setFixedHeight(1)
        c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return c


def etiket(metin, ad="metin", ebeveyn=None):
    lb = QLabel(metin, ebeveyn)
    lb.setObjectName(ad)
    return lb


def dugme(metin, rol="ikincil", ebeveyn=None):
    b = QPushButton(metin, ebeveyn)
    b.setProperty("rol", rol)
    b.setCursor(Qt.PointingHandCursor)
    b.setMinimumHeight(32)
    return b


def kart(rol="kart", ebeveyn=None):
    c = QFrame(ebeveyn)
    c.setObjectName({"kart": "kart", "siyah": "siyahKart",
                     "vurgu": "vurguKart", "ic": "icKutu"}.get(rol, "kart"))
    return c


def tut_cocuk(kap, yatay=True, pay=None, aralik=None):
    """Kart içi düzen: kenar 0, boşluk kontrollü."""
    l = QHBoxLayout(kap) if yatay else QVBoxLayout(kap)
    l.setContentsMargins(*(pay or (16, 16, 16, 16)))
    l.setSpacing(aralik if aralik is not None else 12)
    return l


class BaslikAlani(QWidget):
    """Şartname 3.3: etiket / başlık / açıklama + sağ üst yardımcı etiket."""

    def __init__(self, ust_etiket, baslik, aciklama="", sag_etiket="", ebeveyn=None):
        super().__init__(ebeveyn)
        govde = QVBoxLayout(self)
        govde.setContentsMargins(IC_PAY, 16, IC_PAY, 0)
        govde.setSpacing(6)
        self.ustYazi = etiket(ust_etiket.upper(), "ustYazi")
        govde.addWidget(self.ustYazi)
        satir = QHBoxLayout()
        satir.setContentsMargins(0, 0, 0, 0)
        satir.setSpacing(16)
        sol = QVBoxLayout()
        sol.setContentsMargins(0, 0, 0, 0)
        sol.setSpacing(6)
        self.baslikYazi = etiket(baslik, "sayfaBaslik")
        sol.addWidget(self.baslikYazi)
        self.aciklamaYazi = etiket(aciklama, "sayfaAciklama")
        self.aciklamaYazi.setWordWrap(True)
        sol.addWidget(self.aciklamaYazi)
        satir.addLayout(sol, 1)
        if sag_etiket:
            self.sagYazi = etiket(sag_etiket, "sayfaEtiket")
            self.sagYazi.setAlignment(Qt.AlignRight | Qt.AlignTop)
            satir.addWidget(self.sagYazi, 0, Qt.AlignTop)
        govde.addLayout(satir)
        self.setFixedHeight(135)


class Metrik(QWidget):
    """Siyah metrik bandı hücresi: turuncu etiket, büyük değer, alt açıklama."""

    def __init__(self, etiket_ad, deger="-", alt="", ebeveyn=None):
        super().__init__(ebeveyn)
        govde = QVBoxLayout(self)
        govde.setContentsMargins(0, 14, 0, 14)
        govde.setSpacing(3)
        govde.addWidget(etiket(etiket_ad.upper(), "metrikEtiket"))
        self.degerYazi = etiket(deger, "metrikDeger")
        govde.addWidget(self.degerYazi)
        self.altYazi = etiket(alt, "metrikAlt")
        govde.addWidget(self.altYazi)

    def guncelle(self, deger, alt=None, renk=None):
        self.degerYazi.setText(str(deger))
        if alt is not None:
            self.altYazi.setText(alt)
        if renk is not None:
            self.degerYazi.setStyleSheet("color: %s;" % renk)

    def yaz(self, deger, alt=None, renk=None):
        """Eski SayacKarti arayuzuyle uyum."""
        self.guncelle(deger, alt, renk)


class MetrikBandi(QFrame):
    """Yatay siyah bant: metrikler + ince dikey ayırıcılar."""

    def __init__(self, metrikler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("siyahKart")
        self.setFixedHeight(132)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(20, 0, 20, 0)
        satir.setSpacing(0)
        self.metrikler = {}
        for i, (ad, deger, alt) in enumerate(metrikler):
            if i:
                satir.addWidget(ayirici(dikey=True))
            m = Metrik(ad, deger, alt)
            satir.addWidget(m, 1)
            self.metrikler[ad] = m

    def guncelle(self, ad, deger, alt=None):
        m = self.metrikler.get(ad)
        if m is not None:
            m.guncelle(deger, alt)


class BolumBasligi(QWidget):
    """Kart içi turuncu üst etiket + başlık."""

    def __init__(self, ust="", baslik="", ebeveyn=None):
        super().__init__(ebeveyn)
        govde = QVBoxLayout(self)
        govde.setContentsMargins(0, 0, 0, 0)
        govde.setSpacing(4)
        if ust:
            govde.addWidget(etiket(ust.upper(), "bolumBaslik"))
        if baslik:
            govde.addWidget(etiket(baslik, "kartBaslik"))


class ListeSatiri(QFrame):
    """Seçilebilir satır: ad + sağ değer. Turuncu sol çizgi seçimde."""

    def __init__(self, ad="", sag="", orta="", ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("listeSatir")
        self.setMinimumHeight(44)
        self.setProperty("secili", "0")
        satir = QHBoxLayout(self)
        satir.setContentsMargins(14, 8, 14, 8)
        satir.setSpacing(10)
        self.solYazi = etiket(ad, "satirAd")
        self.solYazi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        satir.addWidget(self.solYazi)
        if orta:
            self.ortaYazi = etiket(orta, "soluk")
            self.ortaYazi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            satir.addWidget(self.ortaYazi)
        self.sagYazi = etiket(sag, "satirSag")
        self.sagYazi.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        satir.addWidget(self.sagYazi, 0, Qt.AlignRight)

    def sec(self, deger):
        self.setProperty("secili", "1" if deger else "0")
        self.solYazi.setStyleSheet("color: %s;" % YAZI)

    def yenile(self, ad=None, sag=None, orta=None):
        if ad is not None:
            self.solYazi.setText(ad)
        if sag is not None:
            self.sagYazi.setText(sag)
        if orta is not None and hasattr(self, "ortaYazi"):
            self.ortaYazi.setText(orta)


class AramaKutusu(QWidget):
    """Siyah arama bandı: SVG büyüteç + giriş."""

    def __init__(self, ipucu="Komut ara... yardım, tel, banka", ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("siyahKart")
        self.setFixedHeight(57)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(18, 0, 18, 0)
        satir.setSpacing(12)
        ara = QLabel()
        ara.setPixmap(svg_ikon("search", 17).pixmap(17, 17))
        ara.setFixedWidth(17)
        ara.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(ara)
        self.girdi = QLineEdit()
        self.girdi.setObjectName("aramaKutusu")
        self.girdi.setPlaceholderText(ipucu)
        self.girdi.setFixedHeight(40)
        satir.addWidget(self.girdi, 1)
        self.degistirildi = self.girdi.textChanged


class IlerlemeSatiri(QWidget):
    """Etiket + çubuk + yüzde. Yüzde metni gerçek veriden gelir."""

    def __init__(self, deger=0, ebeveyn=None):
        super().__init__(ebeveyn)
        govde = QVBoxLayout(self)
        govde.setContentsMargins(0, 0, 0, 0)
        govde.setSpacing(6)
        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        self.yuzdeYazi = etiket("%d%%" % int(deger), "satirSag")
        ust.addStretch(1)
        ust.addWidget(self.yuzdeYazi)
        govde.addLayout(ust)
        from PySide6.QtWidgets import QProgressBar
        self.cubuk = QProgressBar()
        self.cubuk.setProperty("rol", "ince")
        self.cubuk.setTextVisible(False)
        self.cubuk.setRange(0, 100)
        self.cubuk.setValue(int(deger))
        govde.addWidget(self.cubuk)

    def guncelle(self, deger):
        self.cubuk.setValue(int(max(0, min(100, deger))))
        self.yuzdeYazi.setText("%d%%" % int(max(0, min(100, deger))))


class MarkaKarti(QFrame):
    """Kurulum/güncelleme sağındaki siyah marka kartı."""

    def __init__(self, ust="", baslik="", metin="", ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("siyahKart")
        govde = QVBoxLayout(self)
        govde.setContentsMargins(28, 28, 28, 28)
        govde.setSpacing(14)
        govde.addStretch(1)
        marka = QLabel()
        marka.setPixmap(mark_pixmap(150))
        marka.setAlignment(Qt.AlignCenter)
        marka.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        govde.addWidget(marka)
        if ust:
            govde.addWidget(etiket(ust.upper(), "bolumBaslik"))
        if baslik:
            b = etiket(baslik, "kartBaslik")
            b.setWordWrap(True)
            govde.addWidget(b)
        if metin:
            m = etiket(metin, "soluk")
            m.setWordWrap(True)
            govde.addWidget(m)
        govde.addStretch(1)


class BosDurum(QWidget):
    """Gerçek veri yokken gösterilen açık durum (hayali değer üretmez)."""

    def __init__(self, mesaj, ebeveyn=None):
        super().__init__(ebeveyn)
        govde = QVBoxLayout(self)
        govde.setContentsMargins(20, 20, 20, 20)
        govde.addStretch(1)
        m = etiket(mesaj, "ikincil")
        m.setAlignment(Qt.AlignCenter)
        m.setWordWrap(True)
        govde.addWidget(m)
        govde.addStretch(1)


class Sekmeler(QWidget):
    """Yatay kategori/sekme düğmeleri. Seçili sekme turuncu."""

    def __init__(self, adaylar, secili=0, ebeveyn=None):
        super().__init__(ebeveyn)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(0, 0, 0, 0)
        satir.setSpacing(10)
        self.dugmeler = []
        self._secili = secili
        for i, ad in enumerate(adaylar):
            b = dugme(ad, "sekme")
            b.setCheckable(True)
            b.setChecked(i == secili)
            b.setProperty("secili", "1" if i == secili else "0")
            b.clicked.connect(lambda _c, k=i: self.sec(k))
            satir.addWidget(b)
            self.dugmeler.append(b)
        satir.addStretch(1)

    def sec(self, indeks):
        if indeks == self._secili:
            return
        self._secili = indeks
        for i, b in enumerate(self.dugmeler):
            b.setChecked(i == indeks)
            b.setProperty("secili", "1" if i == indeks else "0")
        self._stil_yenile()

    @property
    def indeks(self):
        return self._secili

    def _stil_yenile(self):
        for b in self.dugmeler:
            b.style().unpolish(b)
            b.style().polish(b)

    def secili_ad(self):
        return self.dugmeler[self._secili].text()
