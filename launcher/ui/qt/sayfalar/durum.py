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

UST_ETIKET = "CANLI İZLEME"
SAYFA_BASLIK = "Sunucunun nabzı."
SAYFA_ACIKLAMA = "Sunucu kapalıyken aşağıdaki değerler son ölçümü gösterir."


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
        boya.setBrush(QColor(T.SIYAH))
        boya.drawRect(alan)

        sol, sag = alan.left() + 10, alan.right() - 10
        ust_kenar, taban = alan.top() + 14, alan.bottom() - 22
        yukseklik = taban - ust_kenar
        en = 20.0

        # yatay izgara: veri olmasa da cerceve her zaman durur
        boya.setPen(QPen(QColor("#242B2E"), 1))
        for k in range(1, 4):
            y = taban - yukseklik * k / 4.0
            boya.drawLine(QPointF(sol, y), QPointF(sag, y))

        # 20.0 hedef cizgisi (ince, kesintisiz)
        boya.setPen(QPen(QColor("#3F4749"), 1))
        boya.drawLine(QPointF(sol, ust_kenar), QPointF(sag, ust_kenar))

        # taban cizgisi
        boya.setPen(QPen(QColor(T.BOLUCU), 1))
        boya.drawLine(QPointF(sol, taban), QPointF(sag, taban))

        veri = self._veri[-24:]
        if len(veri) >= 2:
            genislik = sag - sol
            adim = genislik / float(len(veri))
            cubuk = max(4.0, adim * 0.52)
            for i, o in enumerate(veri):
                tps = float(o.get("tps", 0) or 0)
                oran = max(0.0, min(1.0, tps / en))
                h = max(2.0, yukseklik * oran)
                x = sol + adim * i + (adim - cubuk) / 2.0
                boya.setPen(Qt.NoPen)
                boya.setBrush(QColor(T.VURGU) if tps < 15.0 else QColor(T.YAZI))
                boya.drawRect(QRectF(x, taban - h, cubuk, h))
        else:
            boya.setPen(QColor("#545B5C"))
            boya.drawText(QRectF(sol, ust_kenar, sag - sol, taban - ust_kenar),
                          Qt.AlignCenter, "Henüz ölçüm yok")
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

    def baslik_alani_guncelle(self, ust, baslik, aciklama):
        self.baslikAlani.ustYazi.setText(ust.upper())
        self.baslikAlani.baslikYazi.setText(baslik)
        self.baslikAlani.aciklamaYazi.setText(aciklama)

    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(0)
        self.baslikAlani = T.BaslikAlani(UST_ETIKET, SAYFA_BASLIK,
                                              SAYFA_ACIKLAMA,
                                              "DGMCRAFT / DURUM")
        dis.addWidget(self.baslikAlani)
        icKutu = QWidget()
        dis.addWidget(icKutu, 1)
        ic = QVBoxLayout(icKutu)
        ic.setContentsMargins(T.IC_PAY, 0, T.IC_PAY, 0)
        ic.setSpacing(T.KART_ARALIK)

        # --- siyah metrik bandı (1208x132) ---
        self.band = T.MetrikBandi([
            ("TPS", "-", "son 5 saniye"),
            ("MSPT", "-", "sunucu milisaniyesi"),
            ("Bellek", "-", "Java heap kullanımı"),
            ("Oyuncular", "-", "sunucuya bağlı"),
        ])
        ic.addWidget(self.band)
        self.tpsKart = self.band.metrikler["TPS"]
        self.msptKart = self.band.metrikler["MSPT"]
        self.ramKart = self.band.metrikler["Bellek"]
        self.oyuncuKart = self.band.metrikler["Oyuncular"]

        alt = QHBoxLayout()
        alt.setSpacing(20)

        # --- sol: TPS geçmiş kartı ---
        sol = QFrame()
        sol.setObjectName("kart")
        solGovde = QVBoxLayout(sol)
        solGovde.setContentsMargins(20, 18, 20, 16)
        solGovde.setSpacing(10)
        grafikUst = QHBoxLayout()
        grafikUst.setContentsMargins(0, 0, 0, 0)
        b0 = T.etiket("TPS geçmişi", "bolumAltBaslik")
        grafikUst.addWidget(b0)
        grafikUst.addStretch(1)
        self.ornekYazi = T.etiket("SON 5 DAKİKA", "bolumBaslik")
        self.ornekYazi.setStyleSheet("color: %s; font-size: 13px; font-weight: 700;" % T.VURGU)
        grafikUst.addWidget(self.ornekYazi)
        solGovde.addLayout(grafikUst)
        self.grafik = TpsGrafik()
        self.grafik.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        solGovde.addWidget(self.grafik, 1)
        grafikAltSatir = QHBoxLayout()
        grafikAltSatir.setContentsMargins(0, 0, 0, 0)
        grafikAltSatir.addWidget(T.etiket("\u2212 5 dk", "minik"))
        grafikAltSatir.addStretch(1)
        self.grafikAlt = T.etiket("son ölçüm", "minik")
        grafikAltSatir.addWidget(self.grafikAlt)
        solGovde.addLayout(grafikAltSatir)
        sol.setFixedWidth(784)
        sol.setFixedHeight(400)
        alt.addWidget(sol)

        # --- sağ: sistem bilgisi kartı ---
        sagKart = QFrame()
        sagKart.setObjectName("kart")
        sagKart.setFixedWidth(404)
        sagKart.setFixedHeight(400)
        sagGovde = QVBoxLayout(sagKart)
        sagGovde.setContentsMargins(20, 18, 20, 16)
        sagGovde.setSpacing(4)
        b1 = T.etiket("Sistem", "bolumAltBaslik")
        sagGovde.addWidget(b1)
        sagGovde.addSpacing(8)
        self.sunucuSatirlari = {}
        for ad in ("Motor", "Sürüm", "Çalışma süresi",
                   "Yüklü chunk", "Boş disk", "RCON"):
            satir = QHBoxLayout()
            satir.setContentsMargins(0, 0, 0, 0)
            satir.addWidget(T.etiket(ad, "soluk"))
            satir.addStretch(1)
            deger = T.etiket("-", "metin")
            deger.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            satir.addWidget(deger)
            sagGovde.addLayout(satir)
            self.sunucuSatirlari[ad] = deger
            if ad != "RCON":
                ay = T.ayirici()
                ay.setContentsMargins(0, 6, 0, 6)
                sagGovde.addWidget(ay)
        sagGovde.addStretch(1)
        alt.addWidget(sagKart, 0)
        ic.addLayout(alt, 1)

        # Çevrimiçi oyuncular: ayrı kart değil, Sistem panelinin içinde.
        # Referansta sunucu kapalıyken bu alan boş kalır (panel 6 satır).
        self.durumEtiketi = T.etiket("", "minik")
        self.oyuncuBos = T.BosDurum("Sunucu kapalıyken çevrimiçi liste yok.")
        self.oyuncuListe = QVBoxLayout()
        self.oyuncuListe.setContentsMargins(0, 0, 0, 0)
        self.oyuncuListe.setSpacing(4)

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
        Y.guvenli_yayin(self.veri_hazir, veri)

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
        s["Motor"].setText("Purpur 26.1.2")
        s["Sürüm"].setText(str(self.h.surum))
        s["Çalışma süresi"].setText(_D.sure_bicim(veri.get("sure")))
        s["Yüklü chunk"].setText("{:,}".format(veri["chunk"]).replace(",", ".")
                                 if veri.get("chunk") is not None else "-")
        disk = veri.get("disk")
        s["Boş disk"].setText("%d MB" % disk if disk is not None else "-")
        s["RCON"].setText("açık" if canli else "kapalı")
        s["RCON"].setStyleSheet("color: %s;" % (T.YESIL if canli else T.KIRMIZI))

        Y.yerlesim_temizle(self.oyuncuListe)
        self.oyuncuBos.setVisible(not oyuncular)
        for ad in oyuncular:
            satir = T.ListeSatiri(ad if isinstance(ad, str) else str(ad))
            self.oyuncuListe.addWidget(satir)
        self.durumEtiketi.setText("5 sn'de bir yenilenir" if canli
                                  else "Sunucu kapalı — son örnekler gösteriliyor")

    # ---------- yaşam döngüsü ----------
    def goster(self):
        self._zamanlayici.start(YENILE_SN * 1000)
        self._istek()

    def gizle(self):
        self._zamanlayici.stop()