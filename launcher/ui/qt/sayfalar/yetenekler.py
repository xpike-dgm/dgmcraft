"""F5 — Yetenekler: AuraSkills ilerlemesi (11 yetenek), XP çubukları, sonraki açılış."""
import threading

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QScrollArea, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Yetenekler"


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
        boya.setBrush(QColor("#222E2A"))
        boya.drawRoundedRect(alan, 3, 3)
        if self._oran > 0:
            dolu = QRectF(alan.left(), alan.top(), alan.width() * self._oran, alan.height())
            boya.setBrush(QColor(T.VURGU))
            boya.drawRoundedRect(dolu, 3, 3)
        boya.end()


class YetenekKarti(QFrame):
    def __init__(self, veri, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("kart")
        govde = QHBoxLayout(self)
        govde.setContentsMargins(14, 12, 14, 12)
        govde.setSpacing(12)

        ikon = QLabel()
        pm = Y.pixmap("v2", "skills", "%s.png" % veri["ikon"])
        if pm is not None and not pm.isNull():
            ikon.setPixmap(pm.scaled(38, 38, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        govde.addWidget(ikon, 0, Qt.AlignVCenter)

        sag = QVBoxLayout()
        sag.setSpacing(3)
        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        ad = QLabel(veri["ad"])
        ad.setObjectName("metin")
        ust.addWidget(ad)
        ust.addStretch(1)
        seviye = QLabel("Sv. %d" % veri["seviye"])
        seviye.setStyleSheet("color: %s; font-size: 12px; font-weight: 600;" % T.SOLUK)
        ust.addWidget(seviye)
        sag.addLayout(ust)

        self.cubuk = XpCubugu()
        sag.addWidget(self.cubuk)
        self.cubuk.oran(veri["oran"])

        alt = QHBoxLayout()
        alt.setContentsMargins(0, 0, 0, 0)
        xp = QLabel("%d / %d XP" % (veri["xp"], veri["gerekli"]))
        xp.setObjectName("minik")
        alt.addWidget(xp)
        alt.addStretch(1)
        kalan = max(0, int(veri["gerekli"] - veri["xp"]))
        if kalan:
            kalanEtiket = QLabel("%d XP kaldı" % kalan)
            kalanEtiket.setObjectName("minik")
            alt.addWidget(kalanEtiket)
        sag.addLayout(alt)
        govde.addLayout(sag, 1)


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
        self.veri_hazir.emit(oyuncular, yetenekler)

    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(T.KART_ARALIK)

        ust = QFrame()
        ust.setObjectName("kart")
        satir = QHBoxLayout(ust)
        satir.setContentsMargins(14, 10, 14, 10)
        satir.setSpacing(10)
        etiket = QLabel("OYUNCU")
        etiket.setObjectName("bolumBaslik")
        satir.addWidget(etiket)
        self.secici = QComboBox()
        self.secici.setFixedWidth(220)
        self.secici.setStyleSheet(
            "QComboBox { background: #0F1513; border: 1px solid %s; border-radius: 9px;"
            " padding: 7px 10px; color: %s; font-size: 13px; }" % (T.CERCEVE, T.YAZI))
        self.secici.currentIndexChanged.connect(self._oyuncu_degisti)
        satir.addWidget(self.secici)
        satir.addStretch(1)
        self.ozet = QLabel("")
        self.ozet.setObjectName("kucuk")
        satir.addWidget(self.ozet)
        dis.addWidget(ust)

        self.kaydirma = QScrollArea()
        self.kaydirma.setWidgetResizable(True)
        self.kaydirma.setFrameShape(QFrame.NoFrame)
        ic = QWidget()
        self.izgara = QGridLayout(ic)
        self.izgara.setContentsMargins(0, 0, 0, 0)
        self.izgara.setSpacing(T.KART_ARALIK)
        self.kaydirma.setWidget(ic)
        dis.addWidget(self.kaydirma, 1)

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
            self.veri_hazir.emit(self._oyuncular, liste)

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
        sutun = 2
        for i, veri in enumerate(yetenekler):
            self.izgara.addWidget(YetenekKarti(veri), i // sutun, i % sutun)
        for s in range(sutun):
            self.izgara.setColumnStretch(s, 1)
        self.izgara.setRowStretch((len(yetenekler) // sutun) + 1, 1)

    def goster(self):
        if not self._oyuncular:
            self._yukle()

    def gizle(self):
        pass
