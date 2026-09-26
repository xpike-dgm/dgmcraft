"""F5 — Yetenekler: AuraSkills ilerlemesi (11 yetenek), XP çubukları, sonraki açılış."""
import threading

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QScrollArea, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Yetenekler"

UST_ETIKET = "KARAKTER GELİŞİMİ"
SAYFA_BASLIK = "Seviyeni büyüt."
SAYFA_ACIKLAMA = "Her yeteneğin XP yolculuğunu tek bakışta takip et."


class XpCubugu(QWidget):
    """İnce yuvarlak XP çubuğu."""

    def __init__(self, ebeveyn=None):
        super().__init__(ebeveyn)
        self._oran = 0.0
        self.setFixedHeight(6)

    def oran(self, deger):
        self._oran = max(0.0, min(1.0, float(deger or 0)))
        self.update()

    def paintEvent(self, _olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        alan = QRectF(self.rect())
        boya.setPen(Qt.NoPen)
        boya.setBrush(QColor("#4B4F50"))
        boya.drawRoundedRect(alan, 3, 3)
        if self._oran > 0:
            dolu = QRectF(alan.left(), alan.top(), alan.width() * self._oran, alan.height())
            boya.setBrush(QColor(T.VURGU))
            boya.drawRoundedRect(dolu, 3, 3)
        boya.end()


class YetenekKarti(QFrame):
    """290x82 yetenek karti. Secili durumda turuncuzemin + koyu metin."""

    secildi = Signal(object)

    def __init__(self, veri, ebeveyn=None):
        super().__init__(ebeveyn)
        self.veri = veri
        self._secili = False
        self.setObjectName("kart")
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)

        govde = QVBoxLayout(self)
        govde.setContentsMargins(14, 10, 14, 10)
        govde.setSpacing(4)

        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        self.ad = T.etiket(veri["ad"], "yetenekAd")
        ust.addWidget(self.ad)
        ust.addStretch(1)
        self.seviye = T.etiket("Sv. %d" % veri["seviye"], "yetenekSeviye")
        ust.addWidget(self.seviye)
        govde.addLayout(ust)

        self.cubuk = XpCubugu()
        govde.addWidget(self.cubuk)
        self.cubuk.oran(veri["oran"])

        alt = QHBoxLayout()
        alt.setContentsMargins(0, 0, 0, 0)
        self.xp = T.etiket("%d / %d XP" % (veri["xp"], veri["gerekli"]),
                           "yetenekXp")
        alt.addWidget(self.xp)
        alt.addStretch(1)
        kalan = max(0, int(veri["gerekli"] - veri["xp"]))
        self.kalan = T.etiket("%d XP kaldı" % kalan if kalan else "dolu",
                              "yetenekXp")
        alt.addWidget(self.kalan)
        govde.addLayout(alt)
        self._stil()

    def _stil(self):
        if self._secili:
            self.setStyleSheet(
                "QFrame { background: %s; border: 1px solid %s; border-radius: 4px; }"
                % (T.VURGU, T.VURGU))
            self.ad.setStyleSheet("color: %s; font-size: 12px; font-weight: 700;"
                                  % T.VURGU_YAZI)
            self.seviye.setStyleSheet("color: #7A4E10; font-size: 10px; font-weight: 700;")
            self.xp.setStyleSheet("color: #7A4E10; font-size: 10px;")
            self.kalan.setStyleSheet("color: #7A4E10; font-size: 10px;")
        else:
            self.setStyleSheet(
                "QFrame { background: %s; border: 1px solid %s; border-radius: 4px; }"
                "QFrame:hover { border-color: %s; }"
                % (T.YUZEY, T.CERCEVE, T.VURGU))
            self.ad.setStyleSheet("color: %s; font-size: 12px; font-weight: 600;"
                                  % T.YAZI)
            self.seviye.setStyleSheet("color: %s; font-size: 10px;" % T.IKINCIL)
            self.xp.setStyleSheet("color: %s; font-size: 10px;" % T.IKINCIL)
            self.kalan.setStyleSheet("color: %s; font-size: 10px;" % T.IKINCIL)

    def sec(self, deger):
        self._secili = bool(deger)
        self._stil()

    def mousePressEvent(self, olay):
        self.secildi.emit(self.veri)


class YeteneklerSayfasi(QWidget):
    veri_hazir = Signal(object, object)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._oyuncular = []
        self._aktif = None
        self._arayuz_kur()
        self.veri_hazir.connect(self._uygula)
        self._yukle()

    def _yukle(self):
        threading.Thread(target=self._oku, daemon=True).start()

    def _oku(self):
        oyuncular, yetenekler = [], []
        try:
            from core import yetenekler as _Y
            oyuncular = _Y.oyuncular(self.h.kok)
            if oyuncular:
                yetenekler = _Y.yetenekler(self.h.kok, oyuncular[0]["uuid"])
        except Exception as e:
            yetenekler = [{"hata": str(e)[:200]}]
        Y.guvenli_yayin(self.veri_hazir, oyuncular, yetenekler)

    def baslik_alani_guncelle(self, ust, baslik, aciklama):
        self.baslikAlani.ustYazi.setText(ust.upper())
        self.baslikAlani.baslikYazi.setText(baslik)
        self.baslikAlani.aciklamaYazi.setText(aciklama)

    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(T.KART_ARALIK)
        self.baslikAlani = T.BaslikAlani(UST_ETIKET, SAYFA_BASLIK,
                                              SAYFA_ACIKLAMA,
                                              "DGMCRAFT / YETENEKLER")
        dis.addWidget(self.baslikAlani)
        icKutu = QWidget()
        dis.addWidget(icKutu, 1)
        ic = QVBoxLayout(icKutu)
        ic.setContentsMargins(T.IC_PAY, 0, T.IC_PAY, 0)
        ic.setSpacing(T.KART_ARALIK)

        # --- 1208x101 siyah ozet bandi ---
        self.band = T.MetrikBandi([
            ("Açık yetenek", "-", "toplam"),
            ("Toplam seviye", "0", "birikmiş"),
            ("Son açılış", "-", "sıradaki yetenek"),
        ])
        self.band.setFixedHeight(101)
        ic.addWidget(self.band)

        # --- oyuncu secici + arama ---
        ust = QFrame()
        ust.setObjectName("seffaf")
        ust.setFixedHeight(40)
        satir = QHBoxLayout(ust)
        satir.setContentsMargins(0, 0, 0, 0)
        satir.setSpacing(10)
        self.secici = QComboBox()
        self.secici.setFixedWidth(220)
        self.secici.setFixedHeight(32)
        self.secici.currentIndexChanged.connect(self._oyuncu_degisti)
        satir.addWidget(self.secici)
        satir.addStretch(1)
        self.aramaKutusu = T.AramaKutusu("Yetenek ara...")
        self.aramaKutusu.setFixedHeight(34)
        self.aramaKutusu.girdi.setFixedHeight(30)
        self.aramaKutusu.girdi.textChanged.connect(self._suz)
        self.arama = self.aramaKutusu.girdi
        satir.addWidget(self.aramaKutusu, 0)
        self.ozet = T.etiket("", "minik")
        satir.addSpacing(12)
        satir.addWidget(self.ozet, 0)
        ic.addWidget(ust)

        self.kaydirma = QScrollArea()
        self.kaydirma.setWidgetResizable(True)
        self.kaydirma.setFrameShape(QFrame.NoFrame)
        icDugum = QWidget()
        self.izgara = QGridLayout(icDugum)
        self.izgara.setContentsMargins(0, 0, 0, 0)
        self.izgara.setHorizontalSpacing(15)
        self.izgara.setVerticalSpacing(12)
        self.kaydirma.setWidget(icDugum)
        ic.addWidget(self.kaydirma, 1)

        # --- 1208x94 siyah secili yetenek bandi ---
        self.seciliKart = T.kart("siyah")
        self.seciliKart.setFixedHeight(94)
        seciliGovde = QVBoxLayout(self.seciliKart)
        seciliGovde.setContentsMargins(20, 12, 20, 14)
        seciliGovde.setSpacing(6)
        ustSatir = QHBoxLayout()
        ustSatir.setContentsMargins(0, 0, 0, 0)
        self.seciliUst = T.etiket("SEÇİLİ YETENEK", "bolumBaslik")
        ustSatir.addWidget(self.seciliUst)
        ustSatir.addStretch(1)
        self.seciliAd = T.etiket("-", "bolumAltBaslik")
        ustSatir.addWidget(self.seciliAd)
        seciliGovde.addLayout(ustSatir)
        altSatir = QHBoxLayout()
        altSatir.setContentsMargins(0, 0, 0, 0)
        altSatir.setSpacing(14)
        self.seciliXp = T.etiket("0 / 0 XP", "metin")
        self.seciliXp.setMinimumWidth(150)
        altSatir.addWidget(self.seciliXp)
        self.seciliCubuk = T.IlerlemeSatiri(0)
        altSatir.addWidget(self.seciliCubuk, 1)
        self.seciliKalan = T.etiket("-", "soluk")
        self.seciliKalan.setMinimumWidth(120)
        altSatir.addWidget(self.seciliKalan)
        self.seciliDugme = T.dugme("Ayrıntılar aç", "kontrast")
        self.seciliDugme.setFixedHeight(32)
        altSatir.addWidget(self.seciliDugme)
        seciliGovde.addLayout(altSatir)
        ic.addWidget(self.seciliKart)

        self._tum_yetenekler = []
        self._aktif_yetenek = None

    def _oyuncu_degisti(self, indeks):
        if indeks < 0 or indeks >= len(self._oyuncular):
            return
        oyuncu = self._oyuncular[indeks]

        def oku_ve_yolla():
            liste = []
            try:
                from core import yetenekler as _Y
                liste = _Y.yetenekler(self.h.kok, oyuncu["uuid"])
            except Exception:
                liste = []
            Y.guvenli_yayin(self.veri_hazir, self._oyuncular, liste)

        threading.Thread(target=oku_ve_yolla, daemon=True).start()

    def _uygula(self, oyuncular, yetenekler):
        if oyuncular and oyuncular != self._oyuncular:
            self._oyuncular = oyuncular
            self.secici.blockSignals(True)
            self.secici.clear()
            for o in oyuncular:
                self.secici.addItem(o["ad"] or o["uuid"][:8])
            self.secici.blockSignals(False)
        Y.yerlesim_temizle(self.izgara)
        if not yetenekler:
            bos = QLabel("AuraSkills verisi yok. Sunucuda bir oyuncu oynadığında burası dolar.")
            bos.setObjectName("kucuk")
            bos.setAlignment(Qt.AlignCenter)
            self.izgara.addWidget(bos, 0, 0)
            self.ozet.setText("")
            return
        toplam_seviye = sum(int(y.get("seviye", 0)) for y in yetenekler)
        en_iyi = max(yetenekler, key=lambda y: y.get("oran", 0))
        seviye_no, adet = en_iyi.get("sonraki_acilis") or (0, 0)
        if seviye_no:
            ek = " · Sv. %d'de %d yetenek açılır" % (seviye_no, adet)
        else:
            ek = " · tüm yetenekler açık"
        self.ozet.setText("%d yetenek · toplam seviye %d · en yakın: %s%s" % (
            len(yetenekler), toplam_seviye, en_iyi["ad"], ek))
        self.band.guncelle("Açık yetenek", str(len(yetenekler)), "toplam")
        self.band.guncelle("Toplam seviye", str(toplam_seviye), "birikmiş")
        self.band.guncelle(
            "Son açılış", ("Sv. %d" % seviye_no) if seviye_no else " Hepsi açık",
            ("%d yetenek" % adet) if seviye_no else "sıradaki yok")
        self._tum_yetenekler = list(yetenekler)
        self._suz(self.arama.text())

    def _suz(self, metin):
        """Arama metnine göre yetenek kartlarını yeniden üretir."""
        Y.yerlesim_temizle(self.izgara)
        if not self._tum_yetenekler:
            return
        aranan = (metin or "").strip().lower()
        gosterilecek = [y for y in self._tum_yetenekler
                        if not aranan or aranan in (y.get("ad") or "").lower()]
        if not gosterilecek:
            self.izgara.addWidget(T.BosDurum("Eşleşen yetenek yok."), 0, 0)
            return
        sutun = 4
        for i, veri in enumerate(gosterilecek):
            kart = YetenekKarti(veri)
            kart.setFixedSize(290, 82)
            kart.secildi.connect(lambda v: self._yetenek_sec(v))
            if self._aktif_yetenek is not None and \
                    veri.get("ad") == self._aktif_yetenek.get("ad"):
                kart.sec(True)
            self.izgara.addWidget(kart, i // sutun, i % sutun)
        for s in range(sutun):
            self.izgara.setColumnStretch(s, 1)
        self.izgara.setRowStretch((len(gosterilecek) // sutun) + 1, 1)

    def _yetenek_sec(self, veri):
        """Seçili yeteneği siyah alt bantta gösterir."""
        self._aktif_yetenek = veri
        self.seciliAd.setText(str(veri.get("ad") or "-"))
        mevcut = veri.get("xp") or 0
        gerekli = veri.get("xpGerekli") or 0
        seviye = veri.get("seviye") or 0
        self.seciliXp.setText("%d / %d XP · Sv. %d" % (mevcut, gerekli, seviye))
        oran = veri.get("oran")
        if oran is None:
            oran = (mevcut / float(gerekli)) if gerekli else 0.0
        self.seciliCubuk.guncelle(max(0.0, min(1.0, oran)) * 100)
        kalan = max(0, int(gerekli) - int(mevcut))
        self.seciliKalan.setText("%d XP kaldı" % kalan if kalan else "Seviye doldu")
        self._suz(self.arama.text())

    def goster(self):
        if not self._oyuncular:
            self._yukle()

    def gizle(self):
        pass