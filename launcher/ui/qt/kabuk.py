"""PySide6 kabuk: kendi başlık çubuğu + sol ray + yığın sayfalar.
Tkinter v2 ayrı çalışmaya devam eder."""
import sys
import threading

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout,
                               QLabel, QMainWindow, QPushButton, QStackedWidget,
                               QVBoxLayout, QWidget)

from . import ikonlar
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

RAY_IKON = {
    "hub": "hub", "komutlar": "komutlar", "durum": "durum", "konsol": "konsol",
    "gorevler": "gorevler", "yetenekler": "yetenekler", "siralama": "siralama",
    "ayarlar": "ayarlar",
}

# Yeni özellik = bu listeye 1 satır + sayfalar/ altında 1 dosya.
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
TAHIMAT = {
    "komutlar": "Tüm Türkçe komutlar, arama ve kategori detayı.",
    "durum": "Canlı sunucu verileri: RAM, TPS, çevrimiçi.",
    "gorevler": "Görev ağacı ve ilerleme.",
    "yetenekler": "Yetenek seviyeleri ve sonraki ödüller.",
    "siralama": "Podyum ve sıralama tabloları.",
    "ayarlar": "Profil, bağlantı ve uygulama işlemleri.",
}


def _ornek_sonuc():
    """Görüntüleme amaçlı örnek (gerçek güncelleme yokken ekranı görmek için)."""
    return {"son": "v0.26.0", "mevcut": "v0.25.2", "guncelleme_var": True,
            "notlar": "### Yeni\n- Güncelleme ekranı görüntüleniyor\n- Parola koruması",
            "zip_url": "", "asset_url": ""}


class TahimatSayfasi(QWidget):
    """Henüz taşınmamış sayfa: başlık + kısa açıklama (sonraki fazda dolar)."""

    def __init__(self, baslik, aciklama, ebeveyn=None):
        super().__init__(ebeveyn)
        govde = QVBoxLayout(self)
        govde.setContentsMargins(2, 4, 2, 0)
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
    _guncelleme_sonuc = Signal(object)

    def __init__(self, kok, ayar, guncelleme_goster=False, gorev_onizleme=False):
        super().__init__()
        self._guncelleme_zorla = bool(guncelleme_goster)
        self.setWindowTitle(T.UYGULAMA)
        try:
            ico = Y.pixmap("brand", "DgmCraft-app-icon.ico")
            if ico is not None and not ico.isNull():
                self.setWindowIcon(QIcon(ico))
        except Exception:
            pass
        from core.hizmetler import Hizmetler
        self.hizmetler = Hizmetler(kok, ayar, gorev_onizleme=gorev_onizleme)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(T.GENISLIK + T.GOLGE, T.YUKSEKLIK + T.GOLGE)
        self._sayfalar = {}
        self._ray_dugmeleri = {}
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
        if self._sihirbaz_acik:
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
            self._ray.setVisible(True)
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
            self._ray.setVisible(False)
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
        govde.addWidget(self._baslik_kur())

        alt = QHBoxLayout()
        alt.setContentsMargins(0, 0, 0, 0)
        alt.setSpacing(0)
        self._ray = self._ray_kur()
        alt.addWidget(self._ray)
        self._icerik = QFrame()
        self._icerik.setObjectName("icerik")
        ic = QVBoxLayout(self._icerik)
        ic.setContentsMargins(T.BOSLUK, 12, T.BOSLUK, T.BOSLUK)
        ic.setSpacing(0)
        self.yigin = QStackedWidget()
        self.yigin.setObjectName("icerik")
        ic.addWidget(self.yigin, 1)
        alt.addWidget(self._icerik, 1)
        govde.addLayout(alt, 1)

        for kimlik, baslik, _ikon in SAYFALAR:
            sinif_adi = SAYFA_SINIFI.get(kimlik)
            if sinif_adi:
                sayfa = getattr(SAYFA_MODUL[sinif_adi], sinif_adi)(self.hizmetler)
            else:
                sayfa = TahimatSayfasi(baslik, TAHIMAT.get(kimlik, ""))
            self.yigin.addWidget(sayfa)
            self._sayfalar[kimlik] = sayfa
        self.setCentralWidget(dis)

    # ---------- başlık çubuğu ----------
    def _baslik_kur(self):
        cubuk = Y.BaslikCubugu()
        cubuk.setFixedWidth(T.GENISLIK)
        satir = QHBoxLayout(cubuk)
        satir.setContentsMargins(12, 0, 8, 0)
        satir.setSpacing(10)

        logo = Y.pixmap("brand", "mark-480.png")
        if logo is not None and not logo.isNull():
            lb = QLabel()
            lb.setPixmap(logo.scaled(26, 26, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            lb.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            satir.addWidget(lb)
        self.ustBaslik = QLabel("HUB")
        self.ustBaslik.setObjectName("pencereBaslik")
        self.ustBaslik.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(self.ustBaslik)
        satir.addStretch(1)

        self.kasa = QLabel()
        self.kasa.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.kasa.setPixmap(self._yuvarlak("brand", "app-icon-128.png", boyut=30))
        satir.addWidget(self.kasa)
        nokta = QFrame()
        nokta.setFixedSize(7, 7)
        nokta.setStyleSheet("background: %s; border-radius: 3px;" % T.YESIL)
        satir.addSpacing(2)
        satir.addWidget(nokta)
        satir.addSpacing(8)
        kullanici = QLabel(self.hizmetler.kullanici)
        kullanici.setObjectName("kasaAd")
        kullanici.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(kullanici)
        satir.addSpacing(14)

        self.kucultDugmesi = Y.BaslikDugmesi("kucult")
        self.kucultDugmesi.clicked.connect(self.showMinimized)
        satir.addWidget(self.kucultDugmesi)
        self.kapatDugmesi = Y.BaslikDugmesi("kapat")
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

    # ---------- ray ----------
    def _ray_kur(self):
        ray = QFrame()
        ray.setObjectName("ray")
        ray.setFixedWidth(T.RAY_GENISLIK)
        govde = QVBoxLayout(ray)
        govde.setContentsMargins(0, 14, 0, 12)
        govde.setSpacing(6)
        govde.addStretch(1)
        self.rayGrubu = QButtonGroup(self)
        self.rayGrubu.setExclusive(True)
        for kimlik, baslik, ikon in SAYFALAR:
            b = Y.RayDugmesi(RAY_IKON.get(ikon, ikon), baslik)
            b.clicked.connect(lambda _c, k=kimlik: self.sayfa_ac(k))
            govde.addWidget(b, 0, Qt.AlignHCenter)
            self.rayGrubu.addButton(b)
            self._ray_dugmeleri[kimlik] = b
        govde.addStretch(1)
        surum = QLabel(self.hizmetler.surum)
        surum.setObjectName("raySurum")
        surum.setAlignment(Qt.AlignCenter)
        govde.addWidget(surum)
        return ray

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
            b.setChecked(kid == kimlik)
        for kid, baslik, _ikon in SAYFALAR:
            if kid == kimlik:
                self.ustBaslik.setText(baslik.upper())
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
