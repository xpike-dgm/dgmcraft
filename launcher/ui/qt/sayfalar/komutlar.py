"""F3 — Komutlar: arama, kategori listesi, komut detayı ve kopyalama.
Veri kaynağı docs/kilavuz.md (core.komutlar)."""
import threading

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Komutlar"

UST_ETIKET = "OYUN REHBERİ"
SAYFA_BASLIK = "Komutları kolayca bul."
SAYFA_ACIKLAMA = "Kategorileri gez, bir komut seç ve ne yaptığını oku."


class KomutSatiri(QFrame):
    """Komut listesi satırı: ad + sağ ok; seçili satırda turuncu sol çizgi."""

    tiklandi = Signal(str)

    def __init__(self, komut, kategori=None, ebeveyn=None):
        super().__init__(ebeveyn)
        self.komut = komut
        self.setObjectName("listeSatir")
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)
        self.setProperty("secili", "0")
        self.setMinimumHeight(46)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(16, 8, 14, 8)
        satir.setSpacing(12)
        ad = T.etiket(komut["ad"], "komutAd")
        satir.addWidget(ad)
        if kategori:
            et = T.etiket(kategori, "minik")
            satir.addWidget(et)
        satir.addStretch(1)
        ozet = T.etiket(self._kisalt(komut.get("aciklama", ""), 78), "soluk")
        ozet.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        ozet.setWordWrap(False)
        ozet.setMinimumWidth(140)
        satir.addWidget(ozet, 1)
        ok = QLabel()
        ok.setPixmap(T.svg_ikon("arrow", 13).pixmap(13, 13))
        ok.setFixedWidth(13)
        ok.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(ok)

    def sec(self, deger):
        self.setProperty("secili", "1" if deger else "0")
        self.style().unpolish(self)
        self.style().polish(self)

    @staticmethod
    def _kisalt(metin, sinir):
        metin = " ".join((metin or "").split())
        return metin if len(metin) <= sinir else metin[:sinir - 1].rstrip() + "…"

    def mousePressEvent(self, olay):
        self.tiklandi.emit(self.komut["ad"])


class KategoriSatiri(QFrame):
    """Yatay kategori sekmesi."""

    secildi = Signal(str)

    def __init__(self, ad, kisa, sayi, ebeveyn=None):
        super().__init__(ebeveyn)
        self.kimlik = ad
        self.setObjectName("kategoriSatir")
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)
        self.setFixedHeight(34)
        self.ad = T.etiket(kisa, "kategoriAd")
        self.sayi = T.etiket(str(sayi), "kategoriSayi")
        self.ad.adjustSize()
        self.sayi.adjustSize()
        genislik = (self.ad.sizeHint().width() + self.sayi.sizeHint().width()
                    + 16 * 2 + 8 + 14)
        self.setFixedWidth(max(84, genislik))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(16, 0, 16, 0)
        satir.setSpacing(8)
        satir.addWidget(self.ad)
        satir.addWidget(self.sayi)

    def mousePressEvent(self, olay):
        self.secildi.emit(self.kimlik)

    def sec(self, aktif):
        self.setStyleSheet(
            "QFrame#kategoriSatir { background: %s; border: 1px solid %s;"
            " border-radius: 4px; }" % (T.VURGU, T.VURGU) if aktif else
            "QFrame#kategoriSatir { background: %s; border: 1px solid %s;"
            " border-radius: 4px; }"
            "QFrame#kategoriSatir:hover { border-color: %s; }"
            % (T.YUZEY, T.CERCEVE, T.VURGU))
        self.ad.setStyleSheet("color: %s; font-size: 12px; font-weight: 600;"
                              % (T.VURGU_YAZI if aktif else T.YAZI))
        self.sayi.setStyleSheet("color: %s; font-size: 10px; font-weight: 700;"
                                % ("#7A4E10" if aktif else T.IKINCIL))


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
                                              "DGMCRAFT / KOMUTLAR")
        dis.addWidget(self.baslikAlani)
        icKutu = QWidget()
        dis.addWidget(icKutu, 1)
        ic = QVBoxLayout(icKutu)
        ic.setContentsMargins(T.IC_PAY, 0, T.IC_PAY, 0)
        ic.setSpacing(T.KART_ARALIK)

        # --- siyah arama bandı (57px) ---
        self.aramaKutusu = T.AramaKutusu("Komut ara... anit, claim, banka")
        self.aramaKutusu.girdi.textChanged.connect(self._sorgu_degisti)
        self.arama = self.aramaKutusu.girdi
        ic.addWidget(self.aramaKutusu)

        # --- yatay kategori sekmeleri (kaydirilabilir) ---
        self.kategoriSerit = QScrollArea()
        self.kategoriSerit.setFixedHeight(46)
        self.kategoriSerit.setWidgetResizable(False)
        self.kategoriSerit.setFrameShape(QFrame.NoFrame)
        self.kategoriSerit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.kategoriSerit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        icKutuKategori = QWidget()
        self.kategoriAlani = QHBoxLayout(icKutuKategori)
        self.kategoriAlani.setContentsMargins(0, 6, 0, 6)
        self.kategoriAlani.setSpacing(10)
        self.kategoriSerit.setWidget(icKutuKategori)
        self.kategoriAlani_kap = icKutuKategori
        ic.addWidget(self.kategoriSerit)

        # --- liste + siyah detay paneli ---
        govde = QHBoxLayout()
        govde.setSpacing(T.KART_ARALIK)

        solKart = QFrame()
        solKart.setObjectName("kart")
        solKart.setFixedWidth(793)
        solGovde = QVBoxLayout(solKart)
        solGovde.setContentsMargins(0, 0, 0, 0)
        solGovde.setSpacing(0)
        self.sonucEtiketi = T.etiket("", "minik")
        self.sonucEtiketi.setContentsMargins(16, 12, 16, 8)
        solGovde.addWidget(self.sonucEtiketi)
        self.komutAlani = QVBoxLayout()
        self.komutAlani.setContentsMargins(10, 0, 10, 10)
        self.komutAlani.setSpacing(4)
        liste = QWidget()
        listeDikey = QVBoxLayout(liste)
        listeDikey.setContentsMargins(0, 0, 0, 0)
        listeDikey.setSpacing(4)
        listeDikey.addLayout(self.komutAlani)
        listeDikey.addStretch(1)
        kaydir = QScrollArea()
        kaydir.setWidgetResizable(True)
        kaydir.setFrameShape(QFrame.NoFrame)
        kaydir.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        kaydir.setWidget(liste)
        solGovde.addWidget(kaydir, 1)
        govde.addWidget(solKart, 1)

        sagKart = QFrame()
        sagKart.setObjectName("siyahKart")
        sagKart.setFixedWidth(397)
        sagGovde = QVBoxLayout(sagKart)
        sagGovde.setContentsMargins(0, 0, 0, 0)
        sagGovde.setSpacing(0)
        self.sagBaslik = T.etiket("", "bolumBaslik")
        self.sagBaslik.setContentsMargins(20, 18, 20, 6)
        sagGovde.addWidget(self.sagBaslik)
        self.sagAciklama = T.etiket("", "soluk")
        self.sagAciklama.setWordWrap(True)
        self.sagAciklama.setContentsMargins(20, 0, 20, 10)
        sagGovde.addWidget(self.sagAciklama)
        self.ayrac = T.ayirici(T.BOLUCU_ACIK)
        sagGovde.addWidget(self.ayrac)

        self.icerik = QWidget()
        self.icerikDikey = QVBoxLayout(self.icerik)
        self.icerikDikey.setContentsMargins(20, 16, 20, 20)
        self.icerikDikey.setSpacing(12)
        kaydirma = QScrollArea()
        kaydirma.setWidgetResizable(True)
        kaydirma.setFrameShape(QFrame.NoFrame)
        kaydirma.setWidget(self.icerik)
        sagGovde.addWidget(kaydirma, 1)
        govde.addWidget(sagKart, 0)
        ic.addLayout(govde, 1)

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
        self.kategoriAlani_kap.setFixedWidth(
            sum(s.width() for s in self._kategori_satirlari)
            + 10 * max(0, len(self._kategori_satirlari) - 1) + 4)
        self.kategoriAlani.activate()

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
            self.sonucEtiketi.setText("%d komut" % len(sonuclar))
            self.sagBaslik.setText("ARAMA")
            self.sagAciklama.setText('"%s" icin %d sonuc bulundu.'
                                  % (sorgu, len(sonuclar)))
            if not sonuclar:
                self._bos_mesaj("Eşleşen komut yok. Farklı bir kelime dene.")
                return
            Y.yerlesim_temizle(self.komutAlani)
            self._satirlar = []
            for kayit in sonuclar:
                satir = self._satir(kayit["komut"], kayit["kisa"])
                self.komutAlani.addWidget(satir)
                self._satirlar.append(satir)
            self.komutAlani.addStretch(1)
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
        self.sagBaslik.setText("SEÇİLİ KATEGORİ")
        self.sagAciklama.setText(kategori["ad"] + " — " + kategori["aciklama"][:180])
        Y.yerlesim_temizle(self.komutAlani)
        self._satirlar = []
        for komut in kategori["komutlar"]:
            satir = self._satir(komut, None)
            self.komutAlani.addWidget(satir)
            self._satirlar.append(satir)
        self.komutAlani.addStretch(1)

    def _satir(self, komut, kategori_adi):
        satir = KomutSatiri(komut, kategori_adi)
        satir.tiklandi.connect(self._komut_sec)
        return satir

    def _secim_isaretle(self, ad):
        for satir in getattr(self, "_satirlar", []):
            satir.sec(satir.komut["ad"] == ad)

    def _bos_mesaj(self, metin):
        Y.yerlesim_temizle(self.komutAlani)
        lb = T.etiket(metin, "soluk")
        lb.setAlignment(Qt.AlignCenter)
        lb.setContentsMargins(0, 30, 0, 0)
        lb.setWordWrap(True)
        self.komutAlani.addWidget(lb)

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
        self._secim_isaretle(komut["ad"])
        self.sagBaslik.setText("SEÇİLİ KOMUT")
        self.sagAciklama.setText("")
        komutAdi = T.etiket(komut["ad"], "komutDetayAd")
        self.icerikDikey.addWidget(komutAdi)
        self.icerikDikey.addWidget(T.ayirici())
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