"""F7 — Görevler: BeautyQuests görev ağacı ve oyuncu ilerlemesi.
Görev içeriği ayrı çalışma kolundan geliyor; tanım yokken "yakında" gösterilir."""
import threading

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QScrollArea, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Görevler"

DURUM_RENK = {"tamam": ("#34D399", "TAMAMLANDI"),
              "aktif": ("#F0A202", "AKTİF"),
              "kilitli": ("#55635D", "KİLİTLİ"),
              "yok": ("#55635D", "—")}


class GorevKarti(QFrame):
    def __init__(self, gorev, ebeveyn=None):
        super().__init__(ebeveyn)
        self.gorev = gorev
        durum = gorev.get("durum", "yok")
        renk, _etiket = DURUM_RENK.get(durum, DURUM_RENK["yok"])
        self.setObjectName("gorevKarti")
        kenarlik = renk if durum in ("tamam", "aktif") else "#1F2A26"
        self.setStyleSheet(
            "QFrame#gorevKarti { background: #131A18; border: 1px solid %s;"
            " border-radius: 11px; }"
            "QFrame#gorevKarti:hover { background: #18211E; }" % kenarlik)
        govde = QVBoxLayout(self)
        govde.setContentsMargins(14, 12, 14, 12)
        govde.setSpacing(5)

        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        ad = QLabel(gorev.get("ad") or gorev.get("id"))
        ad.setObjectName("metin")
        ad.setWordWrap(True)
        ust.addWidget(ad, 1)
        rozet = QLabel(_etiket)
        rozet.setStyleSheet("color: %s; font-size: 10px; font-weight: 700;"
                            " background: transparent;" % renk)
        ust.addWidget(rozet, 0, Qt.AlignTop)
        govde.addLayout(ust)

        if gorev.get("aciklama"):
            a = QLabel(gorev["aciklama"])
            a.setObjectName("kucuk")
            a.setWordWrap(True)
            govde.addWidget(a)

        alt = QHBoxLayout()
        alt.setContentsMargins(0, 0, 0, 0)
        if gorev.get("objektif_sayisi"):
            o = QLabel("%d hedef" % gorev["objektif_sayisi"])
            o.setObjectName("minik")
            alt.addWidget(o)
        alt.addStretch(1)
        if gorev.get("onceki"):
            b = QLabel(" Gereken: %s" % ", ".join(gorev["onceki"][:3]))
            b.setObjectName("minik")
            alt.addWidget(b)
        govde.addLayout(alt)

        if gorev.get("oduller"):
            r = QLabel("Ödül: " + ", ".join(gorev["oduller"][:3]))
            r.setObjectName("minik")
            r.setWordWrap(True)
            govde.addWidget(r)


class GorevlerSayfasi(QWidget):
    veri_hazir = Signal(object, object, object)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._oyuncular = []
        self._yuklendi = False
        self._arayuz_kur()
        self.veri_hazir.connect(self._uygula)
        self._yukle()

    def _yukle(self):
        threading.Thread(target=self._oku, daemon=True).start()

    def _oku(self):
        oyuncular, dugumler, ozet = [], [], None
        try:
            from core import gorevler as _G
            oyuncular = _G.oyuncular(self.h.kok)
            uuid = None
            if oyuncular:
                uuid = oyuncular[0]["uuid"]
            dugumler = _G.agac(self.h.kok, uuid)
            ozet = _G.ilerleme_ozeti(dugumler)
        except Exception as e:
            dugumler = [{"hata": str(e)[:200]}]
        Y.guvenli_yayin(self.veri_hazir, oyuncular, dugumler, ozet)

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

        def oku():
            dugumler, ozet = [], None
            try:
                from core import gorevler as _G
                dugumler = _G.agac(self.h.kok, oyuncu["uuid"])
                ozet = _G.ilerleme_ozeti(dugumler)
            except Exception:
                pass
            Y.guvenli_yayin(self.veri_hazir, self._oyuncular, dugumler, ozet)

        threading.Thread(target=oku, daemon=True).start()

    def _uygula(self, oyuncular, dugumler, ozet):
        if oyuncular and oyuncular != self._oyuncular:
            self._oyuncular = oyuncular
            self.secici.blockSignals(True)
            self.secici.clear()
            for o in oyuncular:
                self.secici.addItem(o["ad"] or o["uuid"][:8])
            self.secici.blockSignals(False)
        Y.yerlesim_temizle(self.izgara)
        if not dugumler:
            self.ozet.setText("görev tanımı yok")
            kart = QFrame()
            kart.setObjectName("kart")
            govde = QVBoxLayout(kart)
            govde.setContentsMargins(18, 16, 18, 16)
            govde.setSpacing(8)
            b = QLabel("Görevler yakında")
            b.setObjectName("metin")
            govde.addWidget(b)
            a = QLabel(
                "BeautyQuests görev tanımları henüz sunucuya eklenmedi. "
                "Tanımlar eklendiği anda burada ağaç olarak görünecek: "
                "tamamlanan, aktif ve kilitli görevler, ödüller ve hedefler.")
            a.setObjectName("kucuk")
            a.setWordWrap(True)
            govde.addWidget(a)
            govde.addStretch(1)
            self.izgara.addWidget(kart, 0, 0, 1, 3)
            return
        if ozet:
            self.ozet.setText("%d görev · %d tamamlandı · %d aktif · %d kilitli" % (
                ozet["toplam"], ozet["tamam"], ozet["aktif"], ozet["kilitli"]))
        sutun = 3
        for i, gorev in enumerate(dugumler):
            self.izgara.addWidget(GorevKarti(gorev), i // sutun, i % sutun)
        for s in range(sutun):
            self.izgara.setColumnStretch(s, 1)
        self.izgara.setRowStretch((len(dugumler) // sutun) + 1, 1)

    def goster(self):
        if not self._yuklendi:
            self._yuklendi = True
            self._yukle()

    def gizle(self):
        pass
