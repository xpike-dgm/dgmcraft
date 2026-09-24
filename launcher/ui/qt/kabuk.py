"""PySide6 kabuk: sol ray + üst bar + yığın sayfalar. Tkinter v2 ayrı çalışmaya devam eder."""
import ctypes
import sys

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout,
                               QLabel, QMainWindow, QPushButton, QStackedWidget,
                               QVBoxLayout, QWidget)

from . import tema as T
from . import yardimci as Y
from .sayfalar import hub

RAY_IKON = {
    "hub": "hub", "komutlar": "commands", "durum": "status", "konsol": "console",
    "gorevler": "quests", "yetenekler": "skills", "siralama": "ranking",
    "ayarlar": "settings",
}

# Yeni özellik = bu listeye 1 satır + sayfalar/ altında 1 dosya.
SAYFALAR = [
    ("hub", "Hub", "hub"),
    ("komutlar", "Komutlar", "commands"),
    ("durum", "Durum", "status"),
    ("konsol", "Konsol", "console"),
    ("gorevler", "Görevler", "quests"),
    ("yetenekler", "Yetenekler", "skills"),
    ("siralama", "Sıralama", "ranking"),
    ("ayarlar", "Ayarlar", "settings"),
]
TAHIMAT = {
    "komutlar": "Tüm Türkçe komutlar, arama ve kategori detayı.",
    "durum": "Canlı sunucu verileri: RAM, TPS, çevrimiçi.",
    "konsol": "Canlı sunucu çıktısı ve komut satırı.",
    "gorevler": "Görev ağacı ve ilerleme.",
    "yetenekler": "Yetenek seviyeleri ve sonraki ödüller.",
    "siralama": "Podyum ve sıralama tabloları.",
    "ayarlar": "Profil, bağlantı, güncelleme ve sahip işlemleri.",
}


def koyu_baslik_cubugu(pencere):
    try:
        deger = ctypes.c_int(1)
        for kod in (20, 19):
            try:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    int(pencere.winId()), kod, ctypes.byref(deger), ctypes.sizeof(deger))
            except Exception:
                pass
    except Exception:
        pass


class TahimatSayfasi(QWidget):
    """Henüz taşınmamış sayfa: başlık + kısa açıklama (sonraki fazda dolar)."""

    def __init__(self, baslik, aciklama, ebeveyn=None):
        super().__init__(ebeveyn)
        govde = QVBoxLayout(self)
        govde.setContentsMargins(2, 6, 2, 0)
        govde.setSpacing(6)
        b = QLabel(baslik)
        b.setObjectName("sayfaBaslik")
        govde.addWidget(b)
        a = QLabel(aciklama)
        a.setObjectName("ikincil")
        a.setWordWrap(True)
        govde.addWidget(a)
        govde.addStretch(1)

    def goster(self):
        pass

    def gizle(self):
        pass


class Kabuk(QMainWindow):
    def __init__(self, kok, ayar):
        super().__init__()
        self.setWindowTitle(T.UYGULAMA)
        try:
            ico = Y.pixmap("brand", "DgmCraft-app-icon.ico")
            if ico is not None and not ico.isNull():
                self.setWindowIcon(QIcon(ico))
        except Exception:
            pass
        self.hizmetler = None
        from core.hizmetler import Hizmetler
        self.hizmetler = Hizmetler(kok, ayar)
        self.setFixedSize(T.GENISLIK, T.YUKSEKLIK)
        self._sayfalar = {}
        self._ray_dugmeleri = {}
        self._aktif = None
        self._arayuz_kur()
        QTimer.singleShot(0, self._ilk_ac)
        QTimer.singleShot(60, lambda: koyu_baslik_cubugu(self))

    def _arayuz_kur(self):
        govde = QWidget()
        govde.setObjectName("govde")
        dis = QHBoxLayout(govde)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(0)
        dis.addWidget(self._ray_kur())

        sag = QWidget()
        sag.setObjectName("icerik")
        dikey = QVBoxLayout(sag)
        dikey.setContentsMargins(T.BOSLUK, 12, T.BOSLUK, T.BOSLUK)
        dikey.setSpacing(0)
        dikey.addLayout(self._ust_kur())
        dikey.addSpacing(6)

        self.yigin = QStackedWidget()
        self.yigin.setObjectName("icerik")
        dikey.addWidget(self.yigin, 1)
        dis.addWidget(sag, 1)
        self.setCentralWidget(govde)

        for kimlik, baslik, ikon in SAYFALAR:
            if kimlik == "hub":
                sayfa = hub.HaberSayfasi(self.hizmetler)
            else:
                sayfa = TahimatSayfasi(baslik, TAHIMAT.get(kimlik, ""), self)
            self.yigin.addWidget(sayfa)
            self._sayfalar[kimlik] = sayfa

    # ---------- ray ----------
    def _ray_kur(self):
        ray = QFrame()
        ray.setObjectName("ray")
        ray.setFixedWidth(T.RAY_GENISLIK)
        govde = QVBoxLayout(ray)
        govde.setContentsMargins(0, 14, 0, 10)
        govde.setSpacing(2)

        logo = Y.pixmap("brand", "mark-480.png")
        if logo is not None and not logo.isNull():
            lb = QLabel()
            lb.setPixmap(logo.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            lb.setAlignment(Qt.AlignCenter)
            govde.addWidget(lb)
            govde.addSpacing(14)

        self.rayGrubu = QButtonGroup(self)
        self.rayGrubu.setExclusive(True)
        for kimlik, baslik, ikon in SAYFALAR:
            b = QPushButton(baslik)
            b.setObjectName("rayDugme")
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedHeight(46)
            b.setIconSize(QSize(T.IKON, T.IKON))
            ikonlar = Y.ray_ikon_seti(RAY_IKON.get(ikon, ikon), T.IKON)
            if ikonlar.pasif() is not None:
                b.setIcon(QIcon(ikonlar.pasif()))
                b.setProperty("ikonlar", ikonlar)
            b.clicked.connect(lambda _c, k=kimlik: self.sayfa_ac(k))
            govde.addWidget(b)
            self.rayGrubu.addButton(b)
            self._ray_dugmeleri[kimlik] = b
        govde.addStretch(1)
        surum = QLabel(self.hizmetler.surum)
        surum.setObjectName("minik")
        surum.setAlignment(Qt.AlignCenter)
        govde.addWidget(surum)
        return ray

    # ---------- üst bar ----------
    def _ust_kur(self):
        satir = QHBoxLayout()
        satir.setContentsMargins(4, 0, 4, 0)
        self.ustBaslik = QLabel("Hub")
        self.ustBaslik.setObjectName("sayfaBaslik")
        satir.addWidget(self.ustBaslik)
        satir.addStretch(1)

        kafa = Y.pixmap("brand", "app-icon-128.png")
        if kafa is not None and not kafa.isNull():
            lb = QLabel()
            lb.setPixmap(kafa.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            satir.addWidget(lb)
        nokta = QLabel()
        nokta.setFixedSize(7, 7)
        nokta.setStyleSheet("background: %s; border-radius: 3px;" % T.YESIL)
        satir.addSpacing(8)
        satir.addWidget(nokta)
        satir.addSpacing(7)
        kullanici = QLabel(self.hizmetler.kullanici)
        kullanici.setObjectName("ikincil")
        satir.addWidget(kullanici)
        return satir

    # ---------- sayfalar ----------
    def _ilk_ac(self):
        if SAYFALAR:
            self.sayfa_ac(SAYFALAR[0][0])

    def sayfa_ac(self, kimlik):
        if kimlik == self._aktif:
            return
        eski = self._sayfalar.get(self._aktif)
        if eski is not None:
            try:
                eski.gizle()
            except Exception:
                pass
        self._aktif = kimlik
        sayfa = self._sayfalar.get(kimlik)
        if sayfa is None:
            return
        self.yigin.setCurrentWidget(sayfa)
        for kid, b in self._ray_dugmeleri.items():
            aktif = kid == kimlik
            b.setChecked(aktif)
            ikonlar = b.property("ikonlar")
            if ikonlar is not None:
                b.setIcon(QIcon(ikonlar.aktif() if aktif else ikonlar.pasif()))
        for kid, baslik, _ikon in SAYFALAR:
            if kid == kimlik:
                self.ustBaslik.setText(baslik)
        try:
            sayfa.goster()
        except Exception:
            pass


def calistir(kok, ayar):
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(T.UYGULAMA)
    app.setStyle("Fusion")
    T.fontlar_yukle()
    palet = app.palette()
    palet.setColor(palet.ColorRole.Window, T.BG)
    app.setPalette(palet)
    app.setStyleSheet(T.qss())
    pencere = Kabuk(kok, ayar)
    pencere.show()
    return app, pencere
