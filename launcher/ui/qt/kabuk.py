"""PySide6 kabuk: 82px üst çubuk + yatay gezinme + yığılmış sayfalar (05-night).
  Tkinter v2 ayrı çalışmaya devam eder."""
import os
import sys
import threading

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout,
                               QLabel, QMainWindow, QPushButton, QStackedWidget,
                               QVBoxLayout, QWidget)

from . import tema as T
from . import yardimci as Y
from .guncelleme_ekrani import GuncellemeEkrani
from .sihirbaz import Sihirbaz
from .sayfalar import (ayarlar, durum, gorevler, hub, komutlar, konsol, siralama,
                      yetenekler)

SAYFA_SINIFI = {"hub": "HubSayfasi", "konsol": "KonsolSayfasi",
                "komutlar": "KomutlarSayfasi", "durum": "DurumSayfasi",
                "yetenekler": "YeteneklerSayfasi", "siralama": "SiralamaSayfasi",
                "gorevler": "GorevlerSayfasi", "ayarlar": "AyarlarSayfasi"}
SAYFA_MODUL = {"HubSayfasi": hub, "KonsolSayfasi": konsol,
               "KomutlarSayfasi": komutlar, "DurumSayfasi": durum,
               "YeteneklerSayfasi": yetenekler, "SiralamaSayfasi": siralama,
               "GorevlerSayfasi": gorevler, "AyarlarSayfasi": ayarlar}

SAYFALAR = [
    ("hub", "Hub", "hub"),
    ("komutlar", "Komutlar", "komutlar"),
    ("durum", "Durum", "durum"),
    ("konsol", "Konsol", "konsol"),
    ("gorevler", "Görevler", "gorevler"),
    ("yetenekler", "Yetenekler", "yetenekler"),
    ("siralama", "Sıralama", "siralama"),
    ("ayarlar", "Ayarlar", "ayarlar"),
]

SAYFA_UST_ETIKET = {
    "hub": "SUNUCU MERKEZİ", "komutlar": "OYUN REHBERİ", "durum": "CANLI IZLEME",
    "konsol": "SUNUCU ARAYACI", "gorevler": "MACERA YOLU", "yetenekler": "KARAKTER GELİŞİMİ",
    "siralama": "ARKADAŞLARIN", "ayarlar": "TERCİHLER",
}


def _ornek_sonuc():
    """Görüntüleme amaçlı örnek (gerçek güncelleme yokken ekranı görmek için)."""
    return {"son": "v0.26.0", "mevcut": "v0.25.2", "guncelleme_var": True,
            "notlar": "### Yeni\n- Güncelleme ekranı görüntüleniyor\n- Parola koruması",
            "zip_url": "", "asset_url": ""}


class Kabuk(QMainWindow):
    _guncelleme_sonuc = Signal(object)

    def __init__(self, kok, ayar, guncelleme_goster=False, gorev_onizleme=False):
        super().__init__()
        self._guncelleme_zorla = bool(guncelleme_goster)
        self.setWindowTitle(T.UYGULAMA)
        try:
            ico = T.svg_ikon("hub", 64)
            if not ico.isNull():
                self.setWindowIcon(ico)
            else:
                from core import assets as _A
                pm = Y.pixmap("brand", "DgmCraft-app-icon.ico")
                if pm is not None and not pm.isNull():
                    self.setWindowIcon(QIcon(pm))
        except Exception:
            pass
        from core.hizmetler import Hizmetler
        self.hizmetler = Hizmetler(kok, ayar, gorev_onizleme=gorev_onizleme)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(T.GENISLIK + T.GOLGE, T.YUKSEKLIK + T.GOLGE)
        self._sayfalar = {}
        self._nav_dugmeleri = {}
        self._aktif = None
        self._guncelleme_penceresi = None
        self._arayuz_kur()
        self._guncelleme_sonuc.connect(self._guncelleme_goster)
        QTimer.singleShot(120, self._acilis_kontrol)

    def _acilis_kontrol(self):
        """Kurulumu yapmamış kullanıcıya sihirbazı gösterir; herkes için
        güncelleme denetimini başlatır."""
        try:
            kurulu = bool(self.hizmetler.ayar.get("kurulumTamam"))
        except Exception:
            kurulu = False
        self._sihirbaz_acik = not kurulu
        if self._sihirbaz_acik or os.environ.get("DGM_SIHIRBAZ_GEC", "0") == "1":
            try:
                self._sihirbaz = Sihirbaz(self.hizmetler.kok, self.hizmetler.ayar)
                self._sihirbaz.tamamlandi.connect(self._sihirbaz_bitti)
                self._sihirbaz.ciz()
                self._sihirbaz.show()
                self.hide()
                QTimer.singleShot(300, self._yerel_hazirligi)
                return
            except Exception:
                pass
        self._ilk_ac()
        QTimer.singleShot(300, self._yerel_hazirligi)

    def _sihirbaz_bitti(self):
        try:
            if getattr(self, "_sihirbaz", None) is not None:
                self._sihirbaz.close()
                self._sihirbaz = None
            self._icerik.setVisible(True)
            self.show()
            self.raise_()
        except Exception:
            pass
        self._ilk_ac()

    def _yerel_hazirligi(self):
        """Uygulama açılışında: eşitleme kurallarını yazar, güncelleme denetimi
        başlatır, gerekirse güncelleme ekranını açar."""
        try:
            from core import esitleme as _E
            _E.stignore_yaz(self.hizmetler.kok)
        except Exception:
            pass
        QTimer.singleShot(600, self._guncelleme_denetle)

    def _guncelleme_denetle(self):
        def is_thread():
            try:
                from core import guncelleme as _G
                sonuc = _G.denetle(self.hizmetler.ayar)
            except Exception:
                if self._guncelleme_zorla:
                    Y.guvenli_yayin(self._guncelleme_sonuc, _ornek_sonuc())
                return
            if sonuc.get("guncelleme_var") or self._guncelleme_zorla:
                Y.guvenli_yayin(self._guncelleme_sonuc,
                                sonuc if sonuc.get("guncelleme_var")
                                else _ornek_sonuc())

        threading.Thread(target=is_thread, daemon=True).start()

    def _guncelleme_goster(self, sonuc):
        """Güncelleme ekranı ayrı, kapatılamayan pencerede açılır."""
        try:
            self._guncelleme_penceresi = GuncellemeEkrani(self.hizmetler, sonuc)
            self._guncelleme_penceresi.kurulum_bitti.connect(self._guncelleme_tamam)
            self._icerik.setVisible(False)
            self._guncelleme_penceresi.show()
        except Exception:
            pass

    def _guncelleme_tamam(self, tamam):
        try:
            if tamam and self._guncelleme_penceresi is not None:
                self._guncelleme_penceresi.hide()
                self._guncelleme_penceresi.setParent(None)
                self._guncelleme_penceresi = None
        except Exception:
            pass

    def _arayuz_kur(self):
        dis = QWidget(self)
        dis.setObjectName("dis")
        dis.setStyleSheet("QWidget#dis { background: transparent; }")
        kaplayan = QVBoxLayout(dis)
        kaplayan.setContentsMargins(0, 0, 0, 0)
        kaplayan.setSpacing(0)

        self.pencere = QFrame(dis)
        self.pencere.setObjectName("pencere")
        Y.golge(self.pencere, 34, 150, 0)
        kaplayan.addWidget(self.pencere)

        govde = QVBoxLayout(self.pencere)
        govde.setContentsMargins(1, 1, 1, 1)
        govde.setSpacing(0)
        govde.addWidget(self._ust_cubuk_kur())

        self._icerik = QFrame()
        self._icerik.setObjectName("sayfa")
        ic = QVBoxLayout(self._icerik)
        ic.setContentsMargins(0, 0, 0, 0)
        ic.setSpacing(0)
        self.yigin = QStackedWidget()
        self.yigin.setObjectName("sayfa")
        ic.addWidget(self.yigin, 1)
        govde.addWidget(self._icerik, 1)

        for kimlik, baslik, _ikon in SAYFALAR:
            sinif_adi = SAYFA_SINIFI.get(kimlik)
            sayfa = getattr(SAYFA_MODUL[sinif_adi], sinif_adi)(self.hizmetler)
            sayfa.setObjectName("sayfa")
            self.yigin.addWidget(sayfa)
            self._sayfalar[kimlik] = sayfa
        self.setCentralWidget(dis)

    # ---------- 82px üst çubuk + yatay gezinme (tek satır) ----------
    def _ust_cubuk_kur(self):
        cubuk = QFrame()
        cubuk.setObjectName("ustCubuk")
        cubuk.setFixedHeight(T.UST_YUKSEKLIK)

        satir = QHBoxLayout(cubuk)
        satir.setContentsMargins(25, 0, 18, 3)
        satir.setSpacing(0)

        logo = QLabel()
        pm = T.mark_pixmap(43)
        if not pm.isNull():
            logo.setPixmap(pm)
        logo.setFixedSize(43, 43)
        logo.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(logo)
        satir.addSpacing(10)

        marka = QLabel("DGMCRAFT")
        marka.setObjectName("markaAd")
        marka.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(marka)
        satir.addSpacing(34)

        self.navGrubu = QButtonGroup(self)
        self.navGrubu.setExclusive(True)
        for kimlik, baslik, ikon in SAYFALAR:
            b = QPushButton(baslik)
            b.setObjectName("navDugme")
            b.setProperty("aktif", "0")
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedHeight(79)
            b.setMinimumWidth(76)
            b.setIcon(T.svg_ikon(ikon, T.IKON))
            b.setIconSize(QSize(T.IKON, T.IKON))
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _c, k=kimlik: self.sayfa_ac(k))
            satir.addWidget(b)
            self.navGrubu.addButton(b)
            self._nav_dugmeleri[kimlik] = b
            satir.addSpacing(6)

        satir.addStretch(1)

        self.kasa = QLabel()
        self.kasa.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.kasa.setPixmap(self._yuvarlak("brand", "app-icon-128.png", boyut=30))
        satir.addWidget(self.kasa)
        nokta = QFrame()
        nokta.setFixedSize(8, 8)
        nokta.setStyleSheet("background: %s; border-radius: 4px; border: none;"
                            % T.VURGU)
        satir.addSpacing(6)
        satir.addWidget(nokta)
        satir.addSpacing(8)
        self.kullaniciYazi = QLabel(self.hizmetler.kullanici)
        self.kullaniciYazi.setObjectName("oyuncuAd")
        self.kullaniciYazi.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(self.kullaniciYazi)
        ok = QLabel()
        ok.setPixmap(T.svg_ikon("arrow", 12).pixmap(12, 12))
        ok.setFixedWidth(12)
        ok.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addSpacing(10)
        satir.addWidget(ok)
        satir.addSpacing(14)

        self.kucultDugmesi = Y.BaslikDugmesi("kucult")
        self.kucultDugmesi.clicked.connect(self.showMinimized)
        satir.addWidget(self.kucultDugmesi)
        self.kapatDugmesi = Y.BaslikDugmesi("kapat")
        self.kapatDugmesi.clicked.connect(self.close)
        satir.addWidget(self.kapatDugmesi)
        return cubuk

    @staticmethod
    def _yuvarlak(*parca, boyut=30):
        try:
            from PySide6.QtCore import QRect
            from PySide6.QtGui import QPainter, QPixmap
            pm = Y.pixmap(*parca)
            if pm is None or pm.isNull():
                return QPixmap()
            pm = pm.scaled(boyut, boyut, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            yuvarlak = QPixmap(boyut, boyut)
            yuvarlak.fill(Qt.transparent)
            boya = QPainter(yuvarlak)
            boya.setRenderHint(QPainter.Antialiasing, True)
            boya.setBrush(pm)
            boya.setPen(Qt.NoPen)
            boya.drawEllipse(QRect(0, 0, boyut - 1, boyut - 1))
            boya.end()
            return yuvarlak
        except Exception:
            return Y.pixmap(*parca) or QPixmap()

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
        for kid, b in self._nav_dugmeleri.items():
            b.setChecked(kid == kimlik)
            b.setProperty("aktif", "1" if kid == kimlik else "0")
            b.style().unpolish(b)
            b.style().polish(b)
        for kid, baslik, _ikon in SAYFALAR:
            if kid == kimlik:
                self.kucultDugmesi.setToolTip("DGMCRAFT / %s" % baslik.upper())
        try:
            sayfa.goster()
        except Exception:
            pass

    def closeEvent(self, olay):
        try:
            for sayfa in self._sayfalar.values():
                sayfa.gizle()
        except Exception:
            pass
        super().closeEvent(olay)


def calistir(kok, ayar, guncelleme_goster=False, gorev_onizleme=False):
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(T.UYGULAMA)
    app.setStyle("Fusion")
    T.fontlar_yukle()
    palet = app.palette()
    palet.setColor(palet.ColorRole.Window, T.BG)
    app.setPalette(palet)
    app.setStyleSheet(T.qss())
    pencere = Kabuk(kok, ayar, guncelleme_goster=guncelleme_goster,
                    gorev_onizleme=gorev_onizleme)
    pencere.show()
    return app, pencere
