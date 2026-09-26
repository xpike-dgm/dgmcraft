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
        alan = QRectF(self.rect()).adjusted(1, 1, -1, 1)
        boya.setPen(Qt.NoPen)
        boya.setBrush(QColor(T.SIYAH))
        boya.drawRect(alan)
        if len(self._veri) < 2:
            boya.setPen(QColor(T.IKINCIL))
            boya.drawText(alan, Qt.AlignCenter, "Henüz ölçüm yok")
            boya.end()
            return
        en = 20.0
        veri = self._veri[-24:]
        taban = alan.bottom() - 22
        ust_kenar = alan.top() + 14
        yukseklik = taban - ust_kenar
        # 20.0 hedef çizgisi
        boya.setPen(QPen(QColor("#2A3235"), 1, Qt.DashLine))
        boya.drawLine(QPointF(alan.left() + 10, ust_kenar),
                      QPointF(alan.right() - 10, ust_kenar))
        genislik = alan.width() - 20
        adim = genislik / float(max(1, len(veri)))
        cubuk = max(4.0, adim * 0.52)
        for i, o in enumerate(veri):
            tps = float(o.get("tps", 0) or 0)
            oran = max(0.0, min(1.0, tps / en))
            h = max(2.0, yukseklik * oran)
            x = alan.left() + 10 + adim * i + (adim - cubuk) / 2.0
            boya.setPen(Qt.NoPen)
            boya.setBrush(QColor(T.VURGU) if tps < 15.0 else QColor(T.YAZI))
            boya.drawRect(QRectF(x, taban - h, cubuk, h))
        # taban çizgisi + eksen
        boya.setPen(QPen(QColor(T.BOLUCU), 1))
        boya.drawLine(QPointF(alan.left() + 10, taban),
                      QPointF(alan.right() - 10, taban))
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
        dis.setSpacing(T.KART_ARALIK)
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
        alt.setSpacing(T.KART_ARALIK)

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
        self.ornekYazi = T.etiket("son ölçüm", "minik")
        grafikUst.addWidget(self.ornekYazi)
        solGovde.addLayout(grafikUst)
        self.grafik = TpsGrafik()
        self.grafik.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        solGovde.addWidget(self.grafik, 1)
        self.grafikAlt = T.etiket("Son 60 ölçüm · 20,0 hedef", "minik")
        solGovde.addWidget(self.grafikAlt)
        alt.addWidget(sol, 786)

        # --- sağ: sistem bilgisi kartı ---
        sagKart = QFrame()
        sagKart.setObjectName("kart")
        sagKart.setFixedWidth(404)
        sagGovde = QVBoxLayout(sagKart)
        sagGovde.setContentsMargins(20, 18, 20, 16)
        sagGovde.setSpacing(4)
        b1 = T.etiket("Sistem", "bolumAltBaslik")
        sagGovde.addWidget(b1)
        sagGovde.addSpacing(8)
        self.sunucuSatirlari = {}
        for ad in ("Motor", "Sürüm", "Çalışma süresi", "Son örnek", "Varlık",
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
        sagGovde.addStretch(1)
        alt.addWidget(sagKart, 0)
        ic.addLayout(alt, 1)

        self.durumEtiketi = T.etiket("", "minik")
        self.oyuncuBos = T.BosDurum("Sunucu kapalıyken çevrimiçi liste yok.")
        self.oyuncuListeKart = T.kart()
        oyuncuKartGovde = QVBoxLayout(self.oyuncuListeKart)
        oyuncuKartGovde.setContentsMargins(20, 16, 20, 16)
        oyuncuKartGovde.setSpacing(8)
        oyuncuUst = QHBoxLayout()
        oyuncuUst.setContentsMargins(0, 0, 0, 0)
        oyuncuUst.addWidget(T.etiket("ÇEVRİMİÇİ OYUNCULAR", "bolumBaslik"))
        oyuncuUst.addStretch(1)
        oyuncuUst.addWidget(self.durumEtiketi)
        oyuncuKartGovde.addLayout(oyuncuUst)
        self.oyuncuListe = QVBoxLayout()
        self.oyuncuListe.setContentsMargins(0, 0, 0, 0)
        self.oyuncuListe.setSpacing(4)
        oyuncuKartGovde.addLayout(self.oyuncuListe)
        oyuncuKartGovde.addWidget(self.oyuncuBos, 1)
        self.oyuncuListeKart.setFixedHeight(120)
        ic.addWidget(self.oyuncuListeKart)

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