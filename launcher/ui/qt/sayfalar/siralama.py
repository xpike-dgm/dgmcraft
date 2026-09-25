"""F6 — Sıralama: podyum + sıralama listeleri.
Kaynak: sunucudaki ajLeaderboards tabloları, yoksa yerel veri (Essentials/AuraSkills)."""
import threading

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton,
                               QScrollArea, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Sıralama"
MADALYALAR = {1: ("#F0A202", "1"), 2: ("#C8D2CE", "2"), 3: ("#C08457", "3")}


class Satir(QFrame):
    def __init__(self, kayit, vurgulu=False, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("tabloSatir")
        self.setStyleSheet(
            "QFrame#tabloSatir { background: %s; border: 1px solid %s;"
            " border-radius: 9px; }" % (("#1A211E" if vurgulu else "#131A18"),
                                        (T.CERCEVE_PARLAK if vurgulu else "#1F2A26")))
        satir = QHBoxLayout(self)
        satir.setContentsMargins(12, 8, 12, 8)
        satir.setSpacing(10)
        sira = QLabel(str(kayit["sira"]))
        sira.setFixedWidth(22)
        sira.setAlignment(Qt.AlignCenter)
        renk = MADALYALAR.get(kayit["sira"], (T.SILIK,))[0]
        sira.setStyleSheet("color: %s; font-size: 12px; font-weight: 700;"
                           " background: transparent;" % renk)
        satir.addWidget(sira, 0, Qt.AlignVCenter)
        ad = QLabel(kayit["ad"])
        ad.setObjectName("metin")
        satir.addWidget(ad, 1)
        deger = QLabel(kayit.get("metin", "-"))
        deger.setObjectName("metin")
        deger.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        deger.setStyleSheet("color: %s; font-size: 13px; font-weight: 600;"
                            " background: transparent;" % T.YAZI)
        satir.addWidget(deger, 0, Qt.AlignVCenter)


class Podyum(QWidget):
    def __init__(self, ilk_uc, ebeveyn=None):
        super().__init__(ebeveyn)
        govde = QHBoxLayout(self)
        govde.setContentsMargins(0, 0, 0, 0)
        govde.setSpacing(8)
        govde.addStretch(1)
        for sira in (2, 1, 3):
            kayit = ilk_uc.get(sira)
            if not kayit:
                continue
            kutu = QVBoxLayout()
            kutu.setSpacing(4)
            kutu.setAlignment(Qt.AlignCenter)
            madalya = QLabel(MADALYALAR[sira][1])
            madalya.setAlignment(Qt.AlignCenter)
            madalya.setFixedSize(26 if sira == 1 else 22, 26 if sira == 1 else 22)
            madalya.setStyleSheet(
                "background: %s; color: #10100C; border-radius: %dpx;"
                " font-size: 13px; font-weight: 700;"
                % (MADALYALAR[sira][0], 13 if sira == 1 else 11))
            kutu.addWidget(madalya, 0, Qt.AlignHCenter)
            ad = QLabel(kayit["ad"])
            ad.setObjectName("metin")
            ad.setAlignment(Qt.AlignCenter)
            kutu.addWidget(ad)
            deger = QLabel(kayit.get("metin", "-"))
            deger.setObjectName("kucuk")
            deger.setAlignment(Qt.AlignCenter)
            kutu.addWidget(deger)
            govde.addLayout(kutu)
        govde.addStretch(1)


class SiralamaSayfasi(QWidget):
    veri_hazir = Signal(object, bool)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._arayuz_kur()
        self.veri_hazir.connect(self._uygula)
        self._yukle()

    def _yukle(self):
        threading.Thread(target=self._oku, daemon=True).start()

    def _oku(self):
        tablolar, canli = [], False
        try:
            from core import siralama as _S
            tablolar, canli = _S.tablolar(self.h.kok)
        except Exception:
            pass
        Y.guvenli_yayin(self.veri_hazir, tablolar, canli)

    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(T.KART_ARALIK)

        ust = QFrame()
        ust.setObjectName("kart")
        satir = QHBoxLayout(ust)
        satir.setContentsMargins(14, 10, 14, 10)
        self.kaynakEtiketi = QLabel("")
        self.kaynakEtiketi.setObjectName("kucuk")
        satir.addWidget(self.kaynakEtiketi)
        satir.addStretch(1)
        yenile = QPushButton("Yenile")
        yenile.setObjectName("hayaletDugme")
        yenile.setCursor(Qt.PointingHandCursor)
        yenile.clicked.connect(self._yukle)
        satir.addWidget(yenile)
        dis.addWidget(ust)

        self.kaydirma = QScrollArea()
        self.kaydirma.setWidgetResizable(True)
        self.kaydirma.setFrameShape(QFrame.NoFrame)
        ic = QWidget()
        self.govde = QGridLayout(ic)
        self.govde.setContentsMargins(0, 0, 0, 0)
        self.govde.setSpacing(T.KART_ARALIK)
        self.kaydirma.setWidget(ic)
        dis.addWidget(self.kaydirma, 1)

    def _uygula(self, tablolar, canli):
        Y.yerlesim_temizle(self.govde)
        if not tablolar:
            self.kaynakEtiketi.setText("Tablo yok")
            kart = QFrame()
            kart.setObjectName("kart")
            govde = QVBoxLayout(kart)
            govde.setContentsMargins(18, 16, 18, 16)
            govde.setSpacing(8)
            b = QLabel("Sıralama tablosu bulunamadı")
            b.setObjectName("metin")
            govde.addWidget(b)
            try:
                from core import siralama as _S
                ipucu = QLabel(_S.TABLO_YOK_METNI)
            except Exception:
                ipucu = QLabel("")
            ipucu.setObjectName("kucuk")
            ipucu.setWordWrap(True)
            ipucu.setTextInteractionFlags(Qt.TextSelectableByMouse)
            govde.addWidget(ipucu)
            govde.addStretch(1)
            self.govde.addWidget(kart, 0, 0, 1, 3)
            return
        kaynak = "ajLeaderboards (canlı)" if canli else "yerel veri"
        self.kaynakEtiketi.setText("Kaynak: %s · %d tablo" % (kaynak, len(tablolar)))
        sutun = 3
        for i, tablo in enumerate(tablolar):
            self.govde.addWidget(self._tablo_karti(tablo), i // sutun, i % sutun)
        for s in range(sutun):
            self.govde.setColumnStretch(s, 1)
        self.govde.setRowStretch((len(tablolar) // sutun) + 1, 1)

    def _tablo_karti(self, tablo):
        kart = QFrame()
        kart.setObjectName("kart")
        kart.setMinimumWidth(300)
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(16, 14, 16, 14)
        govde.setSpacing(8)
        b = QLabel(tablo["ad"].upper())
        b.setObjectName("bolumBaslik")
        govde.addWidget(b)
        k = QLabel(tablo.get("kaynak", ""))
        k.setObjectName("minik")
        govde.addWidget(k)
        satirlar = tablo.get("satirlar") or []
        if satirlar:
            podyum = Podyum({int(s["sira"]): s for s in satirlar if int(s["sira"]) <= 3})
            govde.addWidget(podyum)
            govde.addSpacing(4)
            for kayit in satirlar[:10]:
                govde.addWidget(Satir(kayit, vurgulu=bool(kayit.get("ad", "").lower()
                                                            == self.h.kullanici.lower())))
        else:
            bos = QLabel("Bu tabloda henüz veri yok.")
            bos.setObjectName("kucuk")
            govde.addWidget(bos)
        govde.addStretch(1)
        return kart

    def goster(self):
        self._yukle()

    def gizle(self):
        pass
