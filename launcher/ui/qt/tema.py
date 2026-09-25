"""PySide6 arayüzü: tek gerçek kaynak. QSS + gerçek yuvarlak köşe/gölge/gradyan."""
from PySide6.QtGui import QColor, QFont, QFontDatabase

GENISLIK = 1180
YUKSEKLIK = 720
GOLGE = 22
RAY_GENISLIK = 68
UST_YUKSEKLIK = 52
BOSLUK = 16
KART_ARALIK = 12
IKON = 22

# Palet: v2 ile aynı aile, biraz daha yumuşak
BG = "#0B0F0E"
YUZEY = "#111715"
KART = "#151B19"
KART_ACIK = "#1A211E"
CERCEVE = "#242F2B"
CERCEVE_PARLAK = "#3A4A43"
YAZI = "#F2F5F3"
SOLUK = "#96A49C"
SILIK = "#6E7F76"
VURGU = "#F0A202"
VURGU_HOVER = "#FFB61A"
VURGU_YAZI = "#1A1000"
YESIL = "#34D399"
KIRMIZI = "#FB7185"
MAVI = "#93C5FD"

# Hero tonları
HERO_UST = "#17211D"
HERO_ALT = "#101614"

UYGULAMA = "DgmCraft"


def fontlar_yukle():
    """Inter + Chakra Petch dosyalarını Qt'ye tanıtır; yoksa sistem fontuna düşer."""
    yigin = []
    try:
        from core import assets as _A
        import os
        for dosya in ("Inter-Regular.ttf", "Inter-SemiBold.ttf", "Inter-Bold.ttf",
                      "ChakraPetch-Bold.ttf", "ChakraPetch-SemiBold.ttf"):
            yol = _A.yol("fonts", dosya)
            if os.path.isfile(yol):
                kimlik = QFontDatabase.addApplicationFont(yol)
                if kimlik >= 0:
                    yigin.extend(QFontDatabase.applicationFontFamilies(kimlik))
    except Exception:
        pass
    return yigin


def qss():
    return """
* { outline: 0; }
QWidget { background: transparent; color: %(yazi)s; font-family: "Inter"; font-size: 13px; }

#ray { background: %(yuzey)s; }
#icerik { background: %(bg)s; }
#pencere {
    background: %(yuzey)s; border: 1px solid #1F2A26; border-radius: 12px;
}
#baslikCubugu { background: #0E1412; border-top-left-radius: 11px; border-top-right-radius: 11px; }
#ayrac { background: #1C2422; border: none; max-height: 1px; min-height: 1px; }

QLabel#pencereBaslik {
    font-family: "Chakra Petch"; font-size: 15px; font-weight: 700;
    color: %(yazi)s; letter-spacing: 2px;
}
QLabel#kasaAd { font-size: 13px; color: #C7D0CC; }
QLabel#raySurum { font-size: 9px; color: #55635D; }
QLabel#sihirBaslik {
    font-family: "Chakra Petch"; font-size: 26px; font-weight: 700; color: %(yazi)s;
}
QLabel#sihirAciklama { font-size: 14px; color: %(soluk)s; }
QFrame#sihirNot {
    background: #131A18; border: 1px solid #1F2A26; border-radius: 10px;
}
QFrame#sihirDurum {
    background: #131A18; border: 1px solid #1F2A26; border-radius: 10px;
}
QProgressBar#sihirCubuk {
    background: #1E2824; border: none; border-radius: 2px; height: 4px;
}
QProgressBar#sihirCubuk::chunk { background: %(vurgu)s; border-radius: 2px; }
QFrame#agacKart {
    background: #101715; border: 1px solid #2C3A34; border-radius: 12px;
}
QFrame#agacKart QLabel { background: transparent; }
QLabel#kartBaslik {
    font-family: "Chakra Petch"; font-size: 16px; font-weight: 700; color: %(yazi)s;
}
QLabel#ustBaslik { font-size: 17px; color: %(yazi)s; }
QLabel#sayfaBaslik { font-size: 17px; color: %(yazi)s; font-weight: 500; }
QLabel#bolumBaslik {
    font-size: 11px; color: %(silik)s; font-weight: 600; letter-spacing: 1px;
}
QLabel#metin { font-size: 13px; color: %(yazi)s; }
QLabel#ikincil { font-size: 12px; color: %(soluk)s; }
QLabel#soluk { font-size: 12px; color: %(soluk)s; }
QLabel#minik { font-size: 11px; color: %(silik)s; }
QLabel#kucuk { font-size: 11px; color: %(silik)s; }
QLabel#komutAd {
    font-family: "Consolas"; font-size: 13px; color: %(vurgu)s; font-weight: 600;
}
QLabel#sayac {
    font-family: "Chakra Petch"; font-size: 30px; font-weight: 700; color: %(yazi)s;
}

/* Güncelleme penceresi */
QFrame#guncKart {
    background: %(yuzey)s; border: 1px solid #223029; border-radius: 16px;
}
QLabel#markaAd {
    font-family: "Chakra Petch"; font-size: 15px; font-weight: 700;
    color: %(yazi)s; letter-spacing: 2px;
}
QLabel#rozetUst {
    font-size: 10px; font-weight: 700; color: %(vurgu)s; letter-spacing: 1px;
    background: #1C1710; border: 1px solid #3A2D14; border-radius: 8px;
    padding: 4px 9px;
}
QLabel#guncBaslik {
    font-family: "Chakra Petch"; font-size: 27px; font-weight: 700; color: %(yazi)s;
}
QLabel#guncSurum { font-size: 13px; }
QLabel#guncDurum { font-size: 12px; color: %(soluk)s; }
QFrame#notKutu {
    background: #0E1513; border: 1px solid #1F2A26; border-radius: 12px;
}
QTextBrowser#notMetin {
    background: transparent; border: none; padding: 14px 16px;
    font-size: 12px; color: %(soluk)s;
}
QProgressBar#guncCubuk {
    background: #1E2824; border: none; border-radius: 3px; height: 6px;
}
QProgressBar#guncCubuk::chunk {
    background: %(vurgu)s; border-radius: 3px;
}
QPushButton#kapatDugme {
    background: transparent; border: 1px solid transparent; border-radius: 9px;
    color: #6E7F76; font-size: 17px; padding: 0;
}
QPushButton#kapatDugme:hover {
    background: #2A1A18; border-color: #4A2A26; color: #F08C8C;
}

QLabel#heroBaslik { font-size: 26px; color: %(yazi)s; font-weight: 600; }
QLabel#heroMetin { font-size: 13px; color: %(soluk)s; }
QLabel#rozetYazi { font-size: 11px; color: %(soluk)s; letter-spacing: 1px; }

QFrame#kart {
    background: %(kart)s; border: 1px solid %(cerceve)s; border-radius: 12px;
}
QFrame#kartIc { background: transparent; border: none; }

QPushButton#anaDugme {
    background: %(vurgu)s; color: %(vurguYazi)s; border: none;
    border-radius: 19px; font-size: 14px; font-weight: 600; padding: 11px 28px;
}
QPushButton#anaDugme:hover { background: %(vurguHover)s; }
QPushButton#anaDugme:pressed { background: #D99102; }
QPushButton#anaDugme:disabled { background: #2A3530; color: %(silik)s; }

QPushButton#hayaletDugme {
    background: transparent; color: %(yazi)s; border: 1px solid %(cerceve)s;
    border-radius: 16px; font-size: 12px; padding: 8px 18px;
}
QPushButton#hayaletDugme:hover { border-color: %(cerceveParlak)s; background: #18201D; }
QPushButton#hayaletDugme:pressed { background: #1C2422; }

QPushButton#zoomDugme {
    background: transparent; color: %(yazi)s; border: 1px solid %(cerceve)s;
    border-radius: 18px; font-size: 17px; font-weight: 700; padding: 0px;
    min-width: 36px; max-width: 36px; min-height: 36px; max-height: 36px;
}
QPushButton#zoomDugme:hover { border-color: %(cerceveParlak)s; background: #18201D; }
QPushButton#zoomDugme:pressed { background: #1C2422; }

QPushButton#ikonDugme {
    background: transparent; border: none; border-radius: 8px; padding: 6px;
}
QPushButton#ikonDugme:hover { background: #1A221F; }

QSlider::groove:horizontal {
    height: 4px; background: #2A3530; border-radius: 2px;
}
QSlider::sub-page:horizontal { background: %(vurgu)s; border-radius: 2px; }
QSlider::handle:horizontal {
    background: %(vurgu)s; width: 16px; height: 16px;
    margin: -6px 0; border-radius: 8px;
}
QSlider::handle:horizontal:hover { background: %(vurguHover)s; }

QScrollArea { border: none; background: transparent; }
QScrollBar:vertical {
    background: transparent; width: 10px; margin: 0;
}
QScrollBar::handle:vertical {
    background: #2A3530; border-radius: 5px; min-height: 30px; margin: 2px;
}
QScrollBar::handle:vertical:hover { background: #3A4A43; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

QToolTip {
    background: %(kartAcik)s; color: %(yazi)s; border: 1px solid %(cerceve)s;
    padding: 5px 8px; border-radius: 6px;
}
""" % {
        "bg": BG, "yuzey": YUZEY, "kart": KART, "kartAcik": KART_ACIK,
        "cerceve": CERCEVE, "cerceveParlak": CERCEVE_PARLAK, "yazi": YAZI,
        "soluk": SOLUK, "silik": SILIK, "vurgu": VURGU, "vurguHover": VURGU_HOVER,
        "vurguYazi": VURGU_YAZI, "yesil": YESIL, "kirmizi": KIRMIZI, "mavi": MAVI,
    }
