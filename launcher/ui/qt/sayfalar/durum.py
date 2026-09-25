"""F4 — Durum: canlı TPS/MSPT/CPU/RAM + son örneklerin grafiği + oyuncu listesi.
Veri kaynağı core.durum (Plan SQLite + RCON). 5 saniyede bir yenilenir."""
import threading

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QLabel, QSizePolicy,
                               QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Durum"
YENILE_SN = 5


class TpsGrafik(QWidget):
    """Son örneklerin TPS grafiği; 20.0 çizgisi ve renkli bant."""

    def __init__(self, ebeveyn=None):
        super().__init__(ebeveyn)
        self._veri = []
        self.setMinimumHeight(96)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def veri(self, ornekler):
        self._veri = list(ornekler or [])
        self.update()

    def paintEvent(self, _olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        alan = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        boya.setPen(Qt.NoPen)
        boya.setBrush(QColor("#0E1513"))
        boya.drawRoundedRect(alan, 10, 10)
        if len(self._veri) < 2:
            boya.setPen(QColor(T.SILIK))
            boya.drawText(alan, Qt.AlignCenter, "Örnek bekleniyor…")
            boya.end()
            return
        en = 20.0
        veri = self._veri[-60:]
        noktalar = []
        genislik = alan.width() - 16
        yukseklik = alan.height() - 30
        for i, o in enumerate(veri):
            x = alan.left() + 8 + (genislik * i / float(max(1, len(veri) - 1)))
            oran = max(0.0, min(1.0, float(o.get("tps", 0)) / en))
            y = alan.bottom() - 8 - (yukseklik * oran)
            noktalar.append(QPointF(x, y))
        # 20.0 hedef çizgisi
        y20 = alan.bottom() - 8 - yukseklik
        y15 = alan.bottom() - 8 - yukseklik * 0.75
        for y, renk in ((y20, "#25332E"), (y15, "#1E2A26")):
            boya.setPen(QPen(QColor(renk), 1, Qt.DashLine))
            boya.drawLine(QPointF(alan.left() + 8, y), QPointF(alan.right() - 8, y))
        # dolgu (aşağı doğru sönümlenen)
        if noktalar:
            from PySide6.QtGui import QBrush, QLinearGradient, QPainterPath
            ust_y = min(p.y() for p in noktalar)
            g = QLinearGradient(0, ust_y, 0, alan.bottom() - 8)
            g.setColorAt(0.0, QColor(240, 162, 2, 70))
            g.setColorAt(1.0, QColor(240, 162, 2, 0))
            poly = [QPointF(alan.left() + 8, alan.bottom() - 8)]
            poly.extend(noktalar)
            poly.append(QPointF(alan.right() - 8, alan.bottom() - 8))
            yol_tam = QPainterPath()
            yol_tam.moveTo(poly[0])
            for p in poly[1:]:
                yol_tam.lineTo(p)
            yol_tam.closeSubpath()
            boya.fillPath(yol_tam, QBrush(g))
            boya.setPen(QPen(QColor(T.VURGU), 2))
            yol_cizgi = QPainterPath()
            yol_cizgi.moveTo(noktalar[0])
            for p in noktalar[1:]:
                yol_cizgi.lineTo(p)
            boya.drawPath(yol_cizgi)
        boya.setPen(QColor(T.SILIK))
        boya.drawText(QRectF(alan.left() + 10, alan.top() + 4, 160, 16),
                      Qt.AlignLeft | Qt.AlignTop, "TPS (son örnekler)")
        boya.setPen(QColor(T.SILIK))
        boya.drawText(QRectF(alan.right() - 70, alan.top() + 4, 62, 16),
                      Qt.AlignRight | Qt.AlignTop, "20.0")
        boya.end()


class SayacKarti(QFrame):
    """Başlık + büyük değer + alt bilgi."""

    def __init__(self, baslik, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("kart")
        govde = QVBoxLayout(self)
        govde.setContentsMargins(16, 14, 16, 14)
        govde.setSpacing(4)
        b = QLabel(baslik.upper())
        b.setObjectName("bolumBaslik")
        govde.addWidget(b)
        self.deger = QLabel("-")
        self.deger.setObjectName("sayac")
        govde.addWidget(self.deger)
        self.alt = QLabel("")
        self.alt.setObjectName("minik")
        govde.addWidget(self.alt)

    def yaz(self, deger, alt="", renk=None):
        self.deger.setText(deger)
        self.alt.setText(alt)
        if renk:
            self.deger.setStyleSheet("color: %s;" % renk)
        else:
            self.deger.setStyleSheet("")


class DurumSayfasi(QWidget):
    veri_hazir = Signal(object)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._son = None
        self._arayuz_kur()
        self.veri_hazir.connect(self._uygula)
        self._zamanlayici = QTimer(self)
        self._zamanlayici.timeout.connect(self._istek)
        self._zamanlayici.start(YENILE_SN * 1000)

    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(T.KART_ARALIK)

        izgara = QGridLayout()
        izgara.setSpacing(T.KART_ARALIK)
        self.tpsKart = SayacKarti("TPS")
        self.msptKart = SayacKarti("MSPT")
        self.ramKart = SayacKarti("Bellek")
        self.oyuncuKart = SayacKarti("Çevrimiçi")
        izgara.addWidget(self.tpsKart, 0, 0)
        izgara.addWidget(self.msptKart, 0, 1)
        izgara.addWidget(self.ramKart, 0, 2)
        izgara.addWidget(self.oyuncuKart, 0, 3)
        for i in range(4):
            izgara.setColumnStretch(i, 1)
        dis.addLayout(izgara)

        self.grafik = TpsGrafik()
        dis.addWidget(self.grafik)

        alt = QHBoxLayout()
        alt.setSpacing(T.KART_ARALIK)

        sol = QFrame()
        sol.setObjectName("kart")
        solGovde = QVBoxLayout(sol)
        solGovde.setContentsMargins(16, 14, 16, 14)
        solGovde.setSpacing(8)
        b = QLabel("SUNUCU")
        b.setObjectName("bolumBaslik")
        solGovde.addWidget(b)
        self.sunucuSatirlari = {}
        for ad in ("Motor", "Sürüm", "Çalışma süresi", "Son örnek",
                   "Varlık", "Yüklü chunk", "Boş disk", "RCON"):
            satir = QHBoxLayout()
            etiket = QLabel(ad)
            etiket.setObjectName("kucuk")
            satir.addWidget(etiket)
            satir.addStretch(1)
            deger = QLabel("-")
            deger.setObjectName("metin")
            deger.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            satir.addWidget(deger)
            solGovde.addLayout(satir)
            self.sunucuSatirlari[ad] = deger
        solGovde.addStretch(1)
        alt.addWidget(sol, 1)

        sagKart = QFrame()
        sagKart.setObjectName("kart")
        sagKart.setFixedWidth(300)
        sagGovde = QVBoxLayout(sagKart)
        sagGovde.setContentsMargins(16, 14, 16, 14)
        sagGovde.setSpacing(8)
        b2 = QLabel("ÇEVRİMİÇİ OYUNCULAR")
        b2.setObjectName("bolumBaslik")
        sagGovde.addWidget(b2)
        self.oyuncuListe = QVBoxLayout()
        self.oyuncuListe.setContentsMargins(0, 0, 0, 0)
        self.oyuncuListe.setSpacing(6)
        sagGovde.addLayout(self.oyuncuListe)
        self.oyuncuBos = QLabel("Sunucu kapalıyken liste yok.")
        self.oyuncuBos.setObjectName("kucuk")
        self.oyuncuBos.setWordWrap(True)
        sagGovde.addWidget(self.oyuncuBos)
        sagGovde.addStretch(1)
        self.durumEtiketi = QLabel("")
        self.durumEtiketi.setObjectName("kucuk")
        sagGovde.addWidget(self.durumEtiketi)
        alt.addWidget(sagKart)
        dis.addLayout(alt, 1)

    # ---------- veri ----------
    def _istek(self):
        threading.Thread(target=self._oku, daemon=True).start()

    def _oku(self):
        veri = {}
        try:
            from core import durum as _D
            veri = _D.durum_topla(self.h.kok)
        except Exception as e:
            veri = {"hata": str(e)[:200], "canli": False, "ornekler": []}
        self.veri_hazir.emit(veri)

    def _uygula(self, veri):
        self._son = veri
        try:
            from core import durum as _D
        except Exception:
            return
        canli = bool(veri.get("canli"))
        tps = veri.get("tps")
        self.tpsKart.yaz("%.1f" % tps if tps is not None else "-",
                         "hedef 20.0", _D.tps_renk(tps))
        mspt = veri.get("mspt")
        self.msptKart.yaz("%.0f ms" % mspt if mspt is not None else "-",
                          "sunucu ortalaması")
        ram = veri.get("ram")
        self.ramKart.yaz("%d MB" % ram if ram is not None else "-",
                         "Java yığını")
        oyuncular = veri.get("oyuncular") or []
        self.oyuncuKart.yaz("%d/3" % len(oyuncular), "3 kişilik sunucu",
                            T.YESIL if oyuncular else T.SOLUK)
        self.grafik.veri(veri.get("ornekler") or [])

        s = self.sunucuSatirlari
        s["Motor"].setText("Purpur 26.2")
        s["Sürüm"].setText(str(self.h.surum))
        s["Çalışma süresi"].setText(_D.sure_bicim(veri.get("sure")))
        yasi = veri.get("ornek_yasi")
        s["Son örnek"].setText("%d sn önce" % yasi if yasi is not None else "-")
        s["Varlık"].setText("{:,}".format(veri["varlik"]).replace(",", ".")
                            if veri.get("varlik") is not None else "-")
        s["Yüklü chunk"].setText("{:,}".format(veri["chunk"]).replace(",", ".")
                                 if veri.get("chunk") is not None else "-")
        disk = veri.get("disk")
        s["Boş disk"].setText("%d MB" % disk if disk is not None else "-")
        s["RCON"].setText("açık" if canli else "kapalı")
        s["RCON"].setStyleSheet("color: %s;" % (T.YESIL if canli else T.KIRMIZI))

        Y.yerlesim_temizle(self.oyuncuListe)
        self.oyuncuBos.setVisible(not oyuncular)
        for ad in oyuncular:
            satir = QFrame()
            satir.setStyleSheet("background: #131A18; border: 1px solid #1F2A26;"
                                " border-radius: 8px;")
            h = QHBoxLayout(satir)
            h.setContentsMargins(10, 7, 10, 7)
            nokta = QFrame()
            nokta.setFixedSize(6, 6)
            nokta.setStyleSheet("background: %s; border-radius: 3px;" % T.YESIL)
            h.addWidget(nokta, 0, Qt.AlignVCenter)
            h.addSpacing(8)
            lb = QLabel(ad)
            lb.setObjectName("metin")
            h.addWidget(lb, 1)
            self.oyuncuListe.addWidget(satir)
        self.durumEtiketi.setText("5 sn'de bir yenilenir" if canli
                                  else "Sunucu kapalı — son örnekler gösteriliyor")

    # ---------- yaşam döngüsü ----------
    def goster(self):
        self._zamanlayici.start(YENILE_SN * 1000)
        self._istek()

    def gizle(self):
        self._zamanlayici.stop()
