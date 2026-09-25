"""F3 — Komutlar: arama, kategori listesi, komut detayı ve kopyalama.
Veri kaynağı docs/kilavuz.md (core.komutlar)."""
import threading

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Komutlar"


class KomutSatiri(QFrame):
    """Sağ panelde tek bir komut satırı; tıklanınca detayı açar."""

    tiklandi = Signal(str)

    def __init__(self, komut, kategori=None, ebeveyn=None):
        super().__init__(ebeveyn)
        self.komut = komut
        self.setObjectName("komutSatir")
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)
        self.setFixedHeight(46)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(14, 0, 14, 0)
        satir.setSpacing(10)
        ad = QLabel(komut["ad"])
        ad.setObjectName("komutAd")
        satir.addWidget(ad)
        if kategori:
            et = QLabel(kategori)
            et.setObjectName("minik")
            satir.addWidget(et)
        satir.addStretch(1)
        ozet = QLabel(self._kisalt(komut.get("aciklama", ""), 70))
        ozet.setObjectName("kucuk")
        ozet.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        ozet.setWordWrap(False)
        ozet.setMinimumWidth(120)
        satir.addWidget(ozet, 1)
        self.setStyleSheet(
            "QFrame#komutSatir { background: #131A18; border: 1px solid #1F2A26;"
            " border-radius: 10px; }"
            "QFrame#komutSatir:hover { background: #18211E; border-color: %s; }"
            % T.CERCEVE_PARLAK)

    @staticmethod
    def _kisalt(metin, sinir):
        metin = " ".join((metin or "").split())
        return metin if len(metin) <= sinir else metin[:sinir - 1].rstrip() + "…"

    def mousePressEvent(self, olay):
        self.tiklandi.emit(self.komut["ad"])


class KategoriSatiri(QFrame):
    secildi = Signal(str)

    def __init__(self, ad, kisa, sayi, ebeveyn=None):
        super().__init__(ebeveyn)
        self.kimlik = ad
        self.setObjectName("kategoriSatir")
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)
        self.setFixedHeight(40)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(12, 0, 12, 0)
        satir.setSpacing(8)
        self.ad = QLabel(kisa)
        self.ad.setObjectName("metin")
        satir.addWidget(self.ad)
        satir.addStretch(1)
        self.sayi = QLabel(str(sayi))
        self.sayi.setObjectName("minik")
        satir.addWidget(self.sayi)

    def mousePressEvent(self, olay):
        self.secildi.emit(self.kimlik)

    def sec(self, aktif):
        self.setStyleSheet(
            "QFrame#kategoriSatir { background: %s; border: 1px solid %s;"
            " border-radius: 10px; }" % (T.KART, T.CERCEVE) if aktif else
            "QFrame#kategoriSatir { background: transparent; border: 1px solid transparent;"
            " border-radius: 10px; }"
            "QFrame#kategoriSatir:hover { background: #151D1A; }")
        self.ad.setStyleSheet("color: %s;" % (T.VURGU if aktif else T.YAZI))


class KomutlarSayfasi(QWidget):
    veri_hazir = Signal(object)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._veri = {"kategoriler": [], "sayi": 0}
        self._aktif_kategori = None
        self._kategori_satirlari = []
        self._arayuz_kur()
        self.veri_hazir.connect(self._veri_uygula)
        self._yukle()

    def _yukle(self):
        threading.Thread(target=self._oku, daemon=True).start()

    def _oku(self):
        veri = {"kategoriler": [], "sayi": 0}
        try:
            from core import komutlar as _K
            veri = _K.katalog_oku(self.h.kok)
        except Exception as e:
            veri["hata"] = str(e)[:200]
        Y.guvenli_yayin(self.veri_hazir, veri)

    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(T.KART_ARALIK)

        arama = QFrame()
        arama.setObjectName("kart")
        aramaSatir = QHBoxLayout(arama)
        aramaSatir.setContentsMargins(14, 10, 14, 10)
        aramaSatir.setSpacing(10)
        self.arama = QLineEdit()
        self.arama.setPlaceholderText("Komut ara: anit, claim, bakiye, telif …")
        self.arama.setStyleSheet(
            "QLineEdit { background: #0F1513; border: 1px solid %s; border-radius: 10px;"
            " padding: 9px 12px; color: %s; font-size: 13px; }"
            "QLineEdit:focus { border-color: %s; }" % (T.CERCEVE, T.YAZI, T.VURGU))
        self.arama.textChanged.connect(self._sorgu_degisti)
        aramaSatir.addWidget(self.arama, 1)
        self.sonucEtiketi = QLabel("")
        self.sonucEtiketi.setObjectName("kucuk")
        aramaSatir.addWidget(self.sonucEtiketi)
        dis.addWidget(arama)

        govde = QHBoxLayout()
        govde.setSpacing(T.KART_ARALIK)

        solKart = QFrame()
        solKart.setObjectName("kart")
        solKart.setFixedWidth(286)
        solGovde = QVBoxLayout(solKart)
        solGovde.setContentsMargins(10, 12, 10, 12)
        solGovde.setSpacing(4)
        baslik = QLabel("KATEGORİLER")
        baslik.setObjectName("bolumBaslik")
        solGovde.addWidget(baslik)
        solGovde.addSpacing(6)
        self.kategoriAlani = QVBoxLayout()
        self.kategoriAlani.setContentsMargins(0, 0, 0, 0)
        self.kategoriAlani.setSpacing(2)
        liste = QWidget()
        self.kategoriAlani_kap = liste
        listeDikey = QVBoxLayout(liste)
        listeDikey.setContentsMargins(0, 0, 0, 0)
        listeDikey.setSpacing(2)
        listeDikey.addLayout(self.kategoriAlani)
        listeDikey.addStretch(1)
        kaydir = QScrollArea()
        kaydir.setWidgetResizable(True)
        kaydir.setFrameShape(QFrame.NoFrame)
        kaydir.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        kaydir.setWidget(liste)
        solGovde.addWidget(kaydir, 1)
        govde.addWidget(solKart)

        sagKart = QFrame()
        sagKart.setObjectName("kart")
        sagGovde = QVBoxLayout(sagKart)
        sagGovde.setContentsMargins(0, 0, 0, 0)
        sagGovde.setSpacing(0)
        self.sagBaslik = QLabel("")
        self.sagBaslik.setObjectName("bolumBaslik")
        self.sagBaslik.setContentsMargins(16, 14, 16, 6)
        sagGovde.addWidget(self.sagBaslik)
        self.sagAciklama = QLabel("")
        self.sagAciklama.setObjectName("kucuk")
        self.sagAciklama.setWordWrap(True)
        self.sagAciklama.setContentsMargins(16, 0, 16, 8)
        sagGovde.addWidget(self.sagAciklama)
        self.ayrac = QFrame()
        self.ayrac.setObjectName("ayrac")
        self.ayrac.setFixedHeight(1)
        sagGovde.addWidget(self.ayrac)

        self.icerik = QWidget()
        self.icerikDikey = QVBoxLayout(self.icerik)
        self.icerikDikey.setContentsMargins(14, 12, 14, 14)
        self.icerikDikey.setSpacing(8)
        kaydirma = QScrollArea()
        kaydirma.setWidgetResizable(True)
        kaydirma.setFrameShape(QFrame.NoFrame)
        kaydirma.setWidget(self.icerik)
        sagGovde.addWidget(kaydirma, 1)
        govde.addWidget(sagKart, 1)
        dis.addLayout(govde, 1)

    # ---------- veri ----------
    def _veri_uygula(self, veri):
        self._veri = veri or {"kategoriler": [], "sayi": 0}
        self._kategori_satirlari = []
        for k in self._veri.get("kategoriler", []):
            satir = KategoriSatiri(k["ad"], k["kisa"], len(k["komutlar"]))
            satir.secildi.connect(self._kategori_sec)
            self.kategoriAlani.addWidget(satir)
            self._kategori_satirlari.append(satir)
        ilk = self._veri.get("kategoriler") or []
        if ilk and self._aktif_kategori is None:
            self._kategori_sec(ilk[0]["ad"])
        else:
            self._liste_yenile()

    def _kategori_sec(self, ad):
        self._aktif_kategori = ad
        if self.arama.text():
            self.arama.blockSignals(True)
            self.arama.clear()
            self.arama.blockSignals(False)
        for satir in self._kategori_satirlari:
            satir.sec(satir.kimlik == ad)
        self._liste_yenile()

    def _sorgu_degisti(self, metin):
        self._liste_yenile()

    def _liste_yenile(self):
        Y.yerlesim_temizle(self.icerikDikey)
        sorgu = self.arama.text().strip()
        if sorgu:
            from core import komutlar as _K
            sonuclar = _K.ara(self._veri, sorgu)
            self.sonucEtiketi.setText("%d sonuç" % len(sonuclar))
            self.sagBaslik.setText('ARAMA: "%s"' % sorgu)
            self.sagAciklama.setText("")
            if not sonuclar:
                self._bos_mesaj("Eşleşen komut yok. Farklı bir kelime dene.")
                return
            for kayit in sonuclar:
                self.icerikDikey.addWidget(self._satir(kayit["komut"], kayit["kisa"]))
            self.icerikDikey.addStretch(1)
            return
        self.sonucEtiketi.setText("")
        kategori = None
        for k in self._veri.get("kategoriler", []):
            if k["ad"] == self._aktif_kategori:
                kategori = k
                break
        if kategori is None:
            self._bos_mesaj("Kategori yok.")
            return
        self.sagBaslik.setText(kategori["ad"].upper())
        self.sagAciklama.setText(kategori["aciklama"][:220])
        for komut in kategori["komutlar"]:
            self.icerikDikey.addWidget(self._satir(komut, None))
        self.icerikDikey.addStretch(1)

    def _satir(self, komut, kategori_adi):
        satir = KomutSatiri(komut, kategori_adi)
        satir.tiklandi.connect(self._komut_sec)
        return satir

    def _bos_mesaj(self, metin):
        lb = QLabel(metin)
        lb.setObjectName("kucuk")
        lb.setAlignment(Qt.AlignCenter)
        lb.setContentsMargins(0, 30, 0, 0)
        self.icerikDikey.addWidget(lb)

    # ---------- detay ----------
    def _komut_sec(self, ad):
        komut = None
        for k in self._veri.get("kategoriler", []):
            for c in k["komutlar"]:
                if c["ad"] == ad:
                    komut = c
                    break
            if komut:
                break
        if not komut:
            return
        Y.yerlesim_temizle(self.icerikDikey)
        self.sagBaslik.setText(komut["ad"].upper())
        self.sagAciklama.setText("")
        self.icerikDikey.addWidget(self._alan_kart(
            "Ne ise yarar", komut.get("aciklama", ""), komut["ad"]))
        if komut.get("ornek"):
            self.icerikDikey.addWidget(self._alan_kart(
                "Örnek", komut["ornek"], self._ilk_komut(komut["ornek"])))
        if komut.get("orijinal"):
            self.icerikDikey.addWidget(self._alan_kart(
                "Orijinal komutu", komut["orijinal"],
                self._ilk_komut(komut["orijinal"])))
        if komut.get("dikkat"):
            self.icerikDikey.addWidget(self._alan_kart(
                "Dikkat", komut["dikkat"], "", uyarı=True))
        geri = QPushButton("← Listeye dön")
        geri.setObjectName("hayaletDugme")
        geri.setCursor(Qt.PointingHandCursor)
        geri.clicked.connect(self._detay_kapat)
        self.icerikDikey.addWidget(geri, 0, Qt.AlignLeft)
        self.icerikDikey.addStretch(1)

    @staticmethod
    def _ilk_komut(metin):
        import re
        m = re.search(r"(/[A-Za-z0-9_çğıöşüÇĞİÖŞÜçğıöşü-]+)", metin or "")
        return m.group(1) if m else (metin or "").strip()[:40]

    def _alan_kart(self, baslik, metin, kopyalanacak, uyarı=False):
        kart = QFrame()
        kart.setObjectName("icKart")
        kart.setStyleSheet(
            "QFrame#icKart { background: %s; border: 1px solid %s; border-radius: 10px; }"
            % (("#1C1710", "#4A3A18") if uyarı else ("#131A18", "#1F2A26")))
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(14, 12, 14, 12)
        govde.setSpacing(6)
        ust = QHBoxLayout()
        b = QLabel(baslik.upper())
        b.setObjectName("bolumBaslik")
        ust.addWidget(b)
        ust.addStretch(1)
        if kopyalanacak:
            dugme = QPushButton("Kopyala")
            dugme.setObjectName("hayaletDugme")
            dugme.setCursor(Qt.PointingHandCursor)
            dugme.clicked.connect(lambda _c, m=kopyalanacak: self._kopyala(m))
            ust.addWidget(dugme)
        govde.addLayout(ust)
        m = QLabel(metin or "-")
        m.setObjectName("metin")
        m.setWordWrap(True)
        m.setTextInteractionFlags(Qt.TextSelectableByMouse)
        govde.addWidget(m)
        return kart

    def _kopyala(self, metin):
        try:
            QApplication.clipboard().setText((metin or "").strip())
        except Exception:
            pass

    def _detay_kapat(self):
        self._liste_yenile()

    # ---------- yaşam döngüsü ----------
    def goster(self):
        if not self._veri.get("kategoriler") and not self._yuklendi:
            self._yuklendi = True
            self._yukle()

    def gizle(self):
        pass
