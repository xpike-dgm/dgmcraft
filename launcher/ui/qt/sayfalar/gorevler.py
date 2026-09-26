"""F7 — Görevler: ilerleme özeti, bölüm listesi ve seçili görevin detay kartı.

Sol sütunda arama + filtreler ve bölüm bölüm açılan görev listesi; sağda
seçili görevin hedefleri, ön koşulları, ödülleri ve aksiyonları.
Veri `core.gorev_agaci`'den gelir; BeautyQuests dosyaları geldiğinde satırlar
gerçek ad, durum, hedef ve ödül bilgisini otomatik alır.
"""
import threading

from PySide6.QtCore import QPoint, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QSizePolicy, QVBoxLayout,
                               QWidget)

from core import gorev_agaci as GA
from .. import ikonlar
from .. import tema as T
from .. import yardimci as Y

BASLIK = "Görevler"

CIZGI = "#242F2B"
ZEMIN = "#121816"
VURGU_ZEMIN = "#16211D"
YESIL = "#34D399"

DURUM_GEYSI = {
    GA.DURUM_TAMAM: (YESIL, "#08150F", "tamam"),
    GA.DURUM_AKTIF: (T.VURGU, "#1A1000", "oyna"),
    GA.DURUM_KILITLI: ("#2A3530", T.SILIK, "kilit"),
    GA.DURUM_TANIMSIZ: ("#232E29", "#55635D", "kilit"),
}

HEDEF_ADI = {
    "MOBS": "Yaratık avla", "MINE": "Blok kaz", "PLACE_BLOCKS": "Blok yerleştir",
    "ITEMS": "Eşya topla", "LOCATION": "Yere ulaş",
    "INTERACT_LOCATION": "Yerle etkileş", "INTERACT_BLOCK": "Bloğa dokun",
    "CHAT": "Söyle", "DEAL_DAMAGE": "Hasar ver", "PLAY_TIME": "Süre geçir",
    "DEATH": "Öl", "EAT_DRINK": "Ye iç", "FISH": "Balık tut", "MELT": "Erit",
    "ENCHANT": "Büyü at", "CRAFT": "Üret", "BUCKET": "Kova kullan",
    "BREED": "Yavrulat", "TAME": "Evcilleştir",
}

HEDEF_SIMGE = {
    "MOBS": "kilic", "MINE": "kazma", "PLACE_BLOCKS": "bot", "ITEMS": "sandik",
    "LOCATION": "goz", "INTERACT_LOCATION": "anahtar", "INTERACT_BLOCK": "kalkan",
    "CHAT": "mesale", "DEAL_DAMAGE": "kilic", "PLAY_TIME": "yildiz",
    "DEATH": "kalp", "EAT_DRINK": "bugday", "FISH": "balik", "MELT": "iksir",
    "ENCHANT": "kitap", "CRAFT": "kalkan", "BUCKET": "kurek", "BREED": "agac",
    "TAME": "kalp",
}


def _kisalt(metin, sinir=90):
    m = " ".join((metin or "").split())
    return m if len(m) <= sinir else m[:sinir].rstrip() + "…"


def _elips(etiket):
    """Etiketi mevcut genişliğine göre tek satırda kısaltır."""
    if etiket.width() <= 10:
        return
    metin = etiket.text()
    olcum = etiket.fontMetrics()
    if olcum.horizontalAdvance(metin) <= etiket.width():
        return
    while metin and olcum.horizontalAdvance(metin + "…") > etiket.width():
        metin = metin[:-1]
    etiket.setText(metin + "…")

UST_ETIKET = "MACERA YOLU"
SAYFA_BASLIK = "750 görev. Tek yolculuk."
SAYFA_ACIKLAMA = "14 bölümde nereden oynadığına ve sıradaki hedefe gider."


class Cizgi(QFrame):
    """1px ayraç."""

    def __init__(self, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setFixedHeight(1)
        self.setStyleSheet("background: %s; border: none;" % CIZGI)


class DaireSimge(QWidget):
    """Daire içinde simge (durum rozetleri ve küçük ikonlar)."""

    def __init__(self, tur, renk, cap=22, kalinlik=1.9, ebeveyn=None):
        super().__init__(ebeveyn)
        self.tur = tur
        self.renk = renk
        self._kalinlik = kalinlik
        self.setFixedSize(cap, cap)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def paintEvent(self, olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        m = self.rect().center()
        dolu = self.tur in ("tamam", "oyna") and self.renk in (YESIL, T.VURGU)
        if dolu:
            boya.setPen(Qt.NoPen)
            boya.setBrush(QColor(self.renk))
            glif_rengi = "#08150F" if self.renk == YESIL else "#1A1000"
        else:
            boya.setPen(QPen(QColor(self.renk), 1.6))
            boya.setBrush(Qt.NoBrush)
            glif_rengi = self.renk
        yari = self.width() / 2.0 - 1.0
        boya.drawEllipse(m, yari, yari)
        ikonlar.ciz(boya, self.tur, m, self.width() * 0.64, glif_rengi,
                    self._kalinlik)
        boya.end()


class SimgeKutusu(QWidget):
    """40px yuvarlak köşeli simge kutusu."""

    def __init__(self, tur, renk, boyut=40, ebeveyn=None):
        super().__init__(ebeveyn)
        self.tur = tur
        self.renk = renk
        self.setFixedSize(boyut, boyut)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def paintEvent(self, olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        boya.setPen(QPen(QColor("#1F2A26"), 1))
        boya.setBrush(QColor("#0F1513"))
        boya.drawRoundedRect(QRectF(0.5, 0.5, self.width() - 1, self.height() - 1),
                             10, 10)
        ikonlar.ciz(boya, self.tur, self.rect().center(), self.width() * 0.54,
                    self.renk, 1.9)
        boya.end()


class OzetRozet(QWidget):
    """Başlıktaki küçük istatistik: ikon + değer + etiket."""

    def __init__(self, tur, renk, ebeveyn=None):
        super().__init__(ebeveyn)
        dikey = QHBoxLayout(self)
        dikey.setContentsMargins(0, 0, 0, 0)
        dikey.setSpacing(9)
        dikey.addWidget(DaireSimge(tur, renk, 26, 1.8), 0, Qt.AlignVCenter)
        metin = QVBoxLayout()
        metin.setContentsMargins(0, 0, 0, 0)
        metin.setSpacing(0)
        self.deger = QLabel("0")
        self.deger.setObjectName("rozetDeger")
        metin.addWidget(self.deger)
        self.etiket = QLabel("")
        self.etiket.setObjectName("rozetEtiket")
        metin.addWidget(self.etiket)
        dikey.addLayout(metin)


class GorevSatiri(QFrame):
    """Sol listede tek satır görev."""

    def __init__(self, dugum, ebeveyn=None):
        super().__init__(ebeveyn)
        self.dugum = dugum
        self.setObjectName("gorevSatir")
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self._secili = False

        satir = QHBoxLayout(self)
        satir.setContentsMargins(10, 0, 10, 0)
        satir.setSpacing(10)
        renk, glif, _t = DURUM_GEYSI.get(dugum.get("durum"),
                                          DURUM_GEYSI[GA.DURUM_TANIMSIZ])
        satir.addWidget(DaireSimge(_t, renk, 20, 1.8), 0, Qt.AlignVCenter)
        metin = QVBoxLayout()
        metin.setContentsMargins(0, 0, 0, 0)
        metin.setSpacing(0)
        self.ad = QLabel(_kisalt(dugum.get("ad") or "Görev", 40))
        self.ad.setObjectName("satirAd")
        self.aciklama = QLabel(_kisalt(dugum.get("aciklama") or
                                       GA.ARSIV_OZET.get(dugum["arsiv"], ""), 80))
        self.aciklama.setObjectName("satirAlt")
        metin.addWidget(self.ad)
        metin.addWidget(self.aciklama)
        satir.addLayout(metin, 1)
        self.sag = QLabel("%s · #%03d" % (GA.ARSIV_ADI.get(dugum["arsiv"], ""),
                                          dugum.get("no", 0)))
        self.sag.setObjectName("satirSag")
        satir.addWidget(self.sag, 0, Qt.AlignVCenter)
        self._renk = renk

    def _yenile(self):
        self.setObjectName("gorevSecili" if self._secili else "gorevSatir")
        stil = self.style()
        stil.unpolish(self)
        stil.polish(self)

    def sec(self, secili):
        if self._secili != bool(secili):
            self._secili = bool(secili)
            self._yenile()

    def resizeEvent(self, olay):
        super().resizeEvent(olay)
        _elips(self.sag)


class BolumSatiri(QFrame):
    """Bölüm başlığı: açılıp kapanır, altında görev satırları."""

    def __init__(self, arsiv, dugumler, toplam=None, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("seffaf")
        self.arsiv = arsiv
        self._tum = dugumler
        self.toplam = len(arsiv["dugumler"]) if toplam is None else toplam
        self.satirlar = []
        self._acik = False
        self._kuruldu = False
        self._suzgecli = len(dugumler) != self.toplam

        govde = QVBoxLayout(self)
        govde.setContentsMargins(0, 0, 0, 0)
        govde.setSpacing(2)

        self.baslik = QFrame()
        self.baslik.setObjectName("bolumBaslik")
        self.baslik.setCursor(Qt.PointingHandCursor)
        self.baslik.setFixedHeight(34)
        satir = QHBoxLayout(self.baslik)
        satir.setContentsMargins(4, 0, 8, 0)
        satir.setSpacing(7)
        self.okSimge = QLabel()
        self.okSimge.setFixedSize(14, 14)
        self.okSimge.setPixmap(ikonlar.pixmap_icin_uret("sagok", 14, T.SILIK))
        satir.addWidget(self.okSimge)
        self.ad = QLabel("Bölüm %d · %s" % (arsiv["sira"] + 1, arsiv["ad"]))
        self.ad.setObjectName("bolumAd")
        satir.addWidget(self.ad)
        satir.addStretch(1)
        self.sayi = QLabel("%d görev" % self.toplam)
        self.sayi.setObjectName("bolumSayi")
        satir.addWidget(self.sayi)
        self.baslik.mousePressEvent = self._baslik_tik
        govde.addWidget(self.baslik)

        self.liste = QVBoxLayout()
        self.liste.setContentsMargins(20, 2, 0, 6)
        self.liste.setSpacing(1)
        govde.addLayout(self.liste)

    def _baslik_tik(self, olay):
        self.acik_degistir()

    def kur(self, dugumler=None, acik=False):
        """Satırlar yalnızca bölüm açıldığında üretilir (kapalıyken boş kalır)."""
        if dugumler is not None:
            self._tum = dugumler
            self._suzgecli = len(dugumler) != self.toplam
        self.sayiyi_guncelle()
        self.acik_degistir(acik)

    def _satirlari_kur(self):
        if self._kuruldu:
            return
        self._kuruldu = True
        for g in self._tum:
            s = GorevSatiri(g)
            s.mousePressEvent = (lambda e, d=g: self._satir_tik(d))
            self.satirlar.append(s)
            self.liste.addWidget(s)

    def sayiyi_guncelle(self):
        if self._suzgecli:
            self.sayi.setText("%d eşleşme" % len(self._tum))
        else:
            self.sayi.setText("%d görev" % self.toplam)

    def _satir_tik(self, dugum):
        for s in self.satirlar:
            s.sec(s.dugum is dugum)
        if self.tiklandi:
            self.tiklandi(dugum)

    tiklandi = None

    def acik_degistir(self, zorla=None):
        yeni = (not self._acik) if zorla is None else bool(zorla)
        self._acik = yeni
        if yeni:
            self._satirlari_kur()
        for s in self.satirlar:
            s.setVisible(yeni)
        self.okSimge.setPixmap(ikonlar.pixmap_icin_uret(
            "asagi" if yeni else "sagok", 14, T.SOLUK))
        self.baslik.setStyleSheet(
            "QFrame#bolumBaslik { background: %s; border-radius: 7px; }"
            "QFrame#bolumBaslik:hover { background: #151D1A; }"
            % ("#141B19" if yeni else "transparent"))

    def uygula(self, arama, durum):
        """Arama/durum filtresini uygular; eşleşme yoksa bölümü gizler.
        Satırlar henüz üretilmemişse veri üzerinden sayılır (kapalı bölüm
        yanlışlıkla gizlenmesin)."""
        kelime = arama.strip().lower()

        def uygun(g):
            if durum != "tumu" and g.get("durum") != durum:
                return False
            if not kelime:
                return True
            havuz = ("%s %s" % (g.get("ad", ""),
                                g.get("aciklama") or "")).lower()
            return kelime in havuz

        say = sum(1 for g in self._tum if uygun(g))
        for s in self.satirlar:
            s.setVisible(self._acik and uygun(s.dugum))
        if kelime or durum != "tumu":
            self.sayi.setText("%d / %d" % (say, self.toplam))
        else:
            self.sayi.setText("%d görev" % self.toplam)
        self.setVisible(say > 0)
        return say


class OdulKutusu(QFrame):
    """Detay kartındaki ödül kutusu."""

    def __init__(self, metin, tur, renk, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("odulKutu")
        self.setFixedHeight(46)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(10, 0, 10, 0)
        satir.setSpacing(9)
        satir.addWidget(SimgeKutusu(tur, renk, 30), 0, Qt.AlignVCenter)
        etiket = QLabel(metin)
        etiket.setObjectName("odulYazi")
        etiket.setWordWrap(True)
        satir.addWidget(etiket, 1)


class DetayKarti(QFrame):
    """Sağ sütun: seçili görevin tüm bilgisi."""

    def __init__(self, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("detayKart")
        self.dugum = None
        govde = QVBoxLayout(self)
        govde.setContentsMargins(20, 18, 20, 18)
        govde.setSpacing(10)
        self.govde = govde
        self._bos_goster()

    def _temizle(self):
        Y.yerlesim_temizle(self.govde)
        self.govde.setSpacing(10)

    def _bos_goster(self):
        self._temizle()
        kutu = QVBoxLayout()
        kutu.addStretch(1)
        ikon = QLabel()
        ikon.setAlignment(Qt.AlignCenter)
        ikon.setPixmap(ikonlar.pixmap_icin_uret("kitap", 44, T.SILIK))
        kutu.addWidget(ikon)
        baslik = QLabel("Bir görev seç")
        baslik.setObjectName("detayBaslik")
        baslik.setAlignment(Qt.AlignCenter)
        kutu.addWidget(baslik)
        aciklama = QLabel("Soldaki listeden bir göreve tıkla; hedefleri, ön koşulları ve ödülleri burada görürsün.")
        aciklama.setObjectName("kucuk")
        aciklama.setAlignment(Qt.AlignCenter)
        aciklama.setWordWrap(True)
        kutu.addWidget(aciklama)
        kutu.addStretch(1)
        self.govde.addLayout(kutu)

    def goster(self, dugum, takip_cb, basla_cb):
        self._temizle()
        self.dugum = dugum
        durum = dugum.get("durum", GA.DURUM_TANIMSIZ)
        renk, glif, _t = DURUM_GEYSI.get(durum, DURUM_GEYSI[GA.DURUM_TANIMSIZ])
        etiket = {GA.DURUM_TAMAM: "Tamamlandı", GA.DURUM_AKTIF: "Oynanabilir",
                  GA.DURUM_KILITLI: "Kilitli"}.get(durum, "Tanım bekleniyor")

        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        ust.setSpacing(10)
        simge = SimgeKutusu(dugum.get("tur", "agac"),
                            T.VURGU if durum == GA.DURUM_AKTIF else T.SOLUK, 40)
        ust.addWidget(simge, 0, Qt.AlignTop)
        basliklar = QVBoxLayout()
        basliklar.setContentsMargins(0, 0, 0, 0)
        basliklar.setSpacing(2)
        ad = QLabel(dugum.get("ad") or "Görev")
        ad.setObjectName("detayBaslik")
        ad.setWordWrap(True)
        basliklar.addWidget(ad)
        alt = QLabel("Bölüm %d — %s · #%03d" % (
            GA.ARSIV_SIRA.get(dugum["arsiv"], 0) + 1,
            GA.ARSIV_ADI.get(dugum["arsiv"], ""), dugum.get("no", 0)))
        alt.setObjectName("detayAlt")
        basliklar.addWidget(alt)
        ust.addLayout(basliklar, 1)
        rozet = QLabel("▶  " + etiket)
        rozet.setObjectName("durumRozeti")
        rozet_rengi = T.SOLUK if durum == GA.DURUM_TANIMSIZ else renk
        rozet.setStyleSheet("QLabel { color: %s; background: %s; border: 1px solid %s;"
                            " border-radius: 11px; padding: 5px 11px; font-size: 11px;"
                            " font-weight: 700; }" % (rozet_rengi, _zemin(rozet_rengi),
                                                     _kenar(rozet_rengi)))
        ust.addWidget(rozet, 0, Qt.AlignTop)
        self.govde.addLayout(ust)

        alinti = QLabel(GA.ARSIV_OZET.get(dugum["arsiv"], ""))
        alinti.setObjectName("detayAlinti")
        alinti.setWordWrap(True)
        self.govde.addWidget(alinti)

        aciklama = dugum.get("aciklama") or ""
        if aciklama:
            a = QLabel(aciklama)
            a.setObjectName("kucuk")
            a.setWordWrap(True)
            self.govde.addWidget(a)
        self.govde.addWidget(Cizgi())

        hedefler = dugum.get("hedefler") or []
        self.govde.addWidget(self._bolum_etiketi("Hedefler"))
        if hedefler:
            for h in hedefler:
                self.govde.addWidget(self._hedef_satiri(h, dugum))
        else:
            bilgi = QLabel("Hedefler görev tanımı gelince burada listelenir.")
            bilgi.setObjectName("minik")
            bilgi.setWordWrap(True)
            self.govde.addWidget(bilgi)

        self.govde.addWidget(Cizgi())
        self.govde.addWidget(self._bolum_etiketi("Ön koşullar"))
        oncesi = dugum.get("oncesi") or []
        if oncesi:
            satir = QHBoxLayout()
            satir.setSpacing(8)
            satir.addWidget(DaireSimge("kilit", T.SILIK, 16, 1.7), 0, Qt.AlignTop)
            o = QLabel(", ".join("#%03d" % x for x in oncesi[:4]))
            o.setObjectName("kucuk")
            o.setWordWrap(True)
            satir.addWidget(o, 1)
            self.govde.addLayout(satir)
        else:
            satir = QHBoxLayout()
            satir.setSpacing(8)
            satir.addWidget(DaireSimge("tamam", YESIL, 16, 1.7), 0, Qt.AlignTop)
            o = QLabel("Ön koşulu yok")
            o.setObjectName("kucuk")
            satir.addWidget(o)
            self.govde.addLayout(satir)

        self.govde.addWidget(Cizgi())
        self.govde.addWidget(self._bolum_etiketi("Ödül"))
        odul = dugum.get("odul") or []
        if odul:
            izgara = QHBoxLayout()
            izgara.setSpacing(8)
            for o in odul[:2]:
                izgara.addWidget(OdulKutusu(o, _odul_simge(o), _odul_renk(o)), 1)
            self.govde.addLayout(izgara)
        else:
            bilgi = QLabel("Ödül bilgisi görev tanımıyla gelir.")
            bilgi.setObjectName("minik")
            self.govde.addWidget(bilgi)

        self.govde.addStretch(1)
        dugmeler = QHBoxLayout()
        dugmeler.setSpacing(8)
        takipli = False
        try:
            takipli = self.h.ayar.get("takipGorev") == dugum.get("no")
        except Exception:
            pass
        takip = QPushButton(("★  Takip ediliyor" if takipli else "☆  Takip et"))
        takip.setObjectName("anaDugme" if takipli else "hayaletDugme")
        takip.setCursor(Qt.PointingHandCursor)
        takip.setMinimumHeight(42)
        takip.clicked.connect(lambda: takip_cb(dugum))
        dugmeler.addWidget(takip, 1)
        basla = QPushButton("▶  Göreve Başla")
        basla.setObjectName("anaDugme")
        basla.setCursor(Qt.PointingHandCursor)
        basla.setMinimumHeight(42)
        basla.clicked.connect(lambda: basla_cb(dugum))
        dugmeler.addWidget(basla, 1)
        self.govde.addLayout(dugmeler)

    def _bolum_etiketi(self, metin):
        et = QLabel(metin.upper())
        et.setObjectName("detayBolum")
        return et

    def _hedef_satiri(self, hedef, dugum):
        satir = QFrame()
        satir.setObjectName("seffaf")
        yatay = QHBoxLayout(satir)
        yatay.setContentsMargins(0, 0, 0, 0)
        yatay.setSpacing(9)
        kutu = QLabel("□")
        kutu.setObjectName("hedefKutu")
        yatay.addWidget(kutu, 0, Qt.AlignTop)
        metinler = QVBoxLayout()
        metinler.setContentsMargins(0, 0, 0, 0)
        metinler.setSpacing(0)
        ad = HEDEF_ADI.get(hedef.get("tip", ""), hedef.get("tip", "Hedef"))
        if hedef.get("adet"):
            ad = "%s (%d)" % (ad, hedef["adet"])
        ilk = QLabel(ad)
        ilk.setObjectName("satirAd")
        metinler.addWidget(ilk)
        if hedef.get("ipucu"):
            ip = QLabel(_kisalt(hedef["ipucu"], 70))
            ip.setObjectName("satirAlt")
            ip.setWordWrap(True)
            metinler.addWidget(ip)
        yatay.addLayout(metinler, 1)
        return satir


def _zemin(renk):
    return {"#34D399": "#10241B", "#F0A202": "#241A08"}.get(renk, "#1A211E")


def _kenar(renk):
    return {"#34D399": "#1E4A38", "#F0A202": "#4A3410"}.get(renk, CIZGI)


def _odul_renk(metin):
    if "₺" in metin:
        return YESIL
    if "XP" in metin:
        return T.VURGU
    return T.SOLUK


def _odul_simge(metin):
    if "₺" in metin:
        return "elmas"
    if "XP" in metin:
        return "yildiz"
    return "sandik"


class FiltreDugmesi(QPushButton):
    """Tümü / Oynanabilir / Tamamlandı / Kilitli düğmeleri."""

    def __init__(self, metin, kimlik, ebeveyn=None):
        super().__init__(ebeveyn)
        self.kimlik = kimlik
        self.setText(metin)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(30)
        self.setCheckable(True)

    def sec(self, secili):
        self.setChecked(secili)
        if secili:
            self.setStyleSheet(
                "QPushButton { background: %s; color: #06210F; border: 1px solid %s;"
                " border-radius: 15px; font-size: 12px; font-weight: 700;"
                " padding: 0px 14px; }" % (YESIL, YESIL))
        else:
            self.setStyleSheet(
                "QPushButton { background: transparent; color: %s;"
                " border: 1px solid %s; border-radius: 15px; font-size: 12px;"
                " padding: 0px 14px; }"
                "QPushButton:hover { border-color: #3A4A43; background: #151D1A; }"
                % (T.SOLUK, CIZGI))


class GorevlerSayfasi(QWidget):
    veri_hazir = Signal(object, object)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._oyuncular = []
        self._yuklendi = False
        self._bolumler = []
        self._arama = ""
        self._durum = "tumu"
        self.harita = None
        self._secili = None
        self.veri_hazir.connect(self._uygula)
        self._arayuz_kur()
        self._yukle()

    # ------------------------------------------------------------- veri -----
    def _yukle(self):
        threading.Thread(target=self._oku, daemon=True).start()

    def _oku(self):
        oyuncular, harita = [], None
        try:
            from core import gorevler as _G
            oyuncular = _G.oyuncular(self.h.kok)
            uuid = oyuncular[0]["uuid"] if oyuncular else None
            onizleme = bool(getattr(self.h, "gorev_onizleme", False))
            harita = GA.agac(self.h.kok, uuid, onizleme=onizleme)
        except Exception as e:
            harita = {"arsivler": [], "dugumler": [], "hata": str(e)}
        Y.guvenli_yayin(self.veri_hazir, oyuncular, harita)

    # ------------------------------------------------------------ arayüz ----
    def baslik_alani_guncelle(self, ust, baslik, aciklama):
        self.baslikAlani.ustYazi.setText(ust.upper())
        self.baslikAlani.baslikYazi.setText(baslik)
        self.baslikAlani.aciklamaYazi.setText(aciklama)

    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(0)
        self.baslikAlani = T.BaslikAlani(UST_ETIKET, SAYFA_BASLIK,
                                        SAYFA_ACIKLAMA, "DGMCRAFT / GÖREVLER")
        dis.addWidget(self.baslikAlani)

        icKutu = QWidget()
        dis.addWidget(icKutu, 1)
        ic = QVBoxLayout(icKutu)
        ic.setContentsMargins(T.IC_PAY, 0, T.IC_PAY, 0)
        ic.setSpacing(12)
        ic.addWidget(self._baslik_kismi())

        govde = QHBoxLayout()
        govde.setContentsMargins(0, 0, 0, 0)
        govde.setSpacing(12)
        govde.addWidget(self._sol_sutun(), 58)
        self.detay = DetayKarti()
        govde.addWidget(self.detay, 42)
        ic.addLayout(govde, 1)

    def _baslik_kismi(self):
        """1208x108 siyah ilerleme bandi: tamamlanan, çubuk, %, bölüm, oynanabilir."""
        kutu = QFrame()
        kutu.setObjectName("siyahKart")
        kutu.setFixedHeight(108)
        satir = QHBoxLayout(kutu)
        satir.setContentsMargins(20, 14, 20, 14)
        satir.setSpacing(18)

        sol = QVBoxLayout()
        sol.setContentsMargins(0, 0, 0, 0)
        sol.setSpacing(6)
        sol.addWidget(T.etiket("TAMAMLANAN", "bolumBaslik"))
        self.altBaslik = T.etiket("0 / 0 tamamlandı", "kartSayacKucuk")
        sol.addWidget(self.altBaslik)
        cubukSatir = QHBoxLayout()
        cubukSatir.setContentsMargins(0, 4, 0, 0)
        cubukSatir.setSpacing(10)
        self.cubuk = Cubuk()
        cubukSatir.addWidget(self.cubuk, 1)
        self.yuzde = T.etiket("0%", "satirSag")
        self.yuzde.setStyleSheet("color: %s; font-size: 14px; font-weight: 700;"
                                 % T.YAZI)
        cubukSatir.addWidget(self.yuzde)
        sol.addLayout(cubukSatir)
        satir.addLayout(sol, 1)
        satir.addWidget(T.ayirici(dikey=True))

        self.rozetBolum = OzetRozet("kitap", T.IKINCIL)
        self.rozetBolum.etiket.setText("bölüm")
        self.rozetAktif = OzetRozet("oyna", T.VURGU)
        self.rozetAktif.etiket.setText("oynanabilir")
        self.rozetTamam = OzetRozet("tamam", T.IKINCIL)
        self.rozetTamam.etiket.setText("tamamlandı")
        for r in (self.rozetBolum, self.rozetAktif, self.rozetTamam):
            satir.addWidget(r, 0, Qt.AlignVCenter)
        return kutu

    def _sol_sutun(self):
        kutu = QFrame()
        kutu.setObjectName("listeKutu")
        dis = QVBoxLayout(kutu)
        dis.setContentsMargins(10, 10, 10, 10)
        dis.setSpacing(8)

        araclar = QHBoxLayout()
        araclar.setContentsMargins(0, 0, 0, 0)
        araclar.setSpacing(7)
        self.arama = QLineEdit()
        self.arama.setObjectName("aramaKutusu")
        self.arama.setPlaceholderText("Görev ara...")
        self.arama.setClearButtonEnabled(True)
        self.arama.setFixedWidth(168)
        self.arama.textChanged.connect(self._arama_degisti)
        araclar.addWidget(self.arama)

        self.secim = QComboBox()
        self.secim.addItem("Tümü")
        self.secim.addItem("Oynanabilir")
        self.secim.addItem("Tamamlandı")
        self.secim.addItem("Kilitli")
        self.secim.setFixedWidth(112)
        self.secim.currentIndexChanged.connect(self._secim_degisti)
        araclar.addWidget(self.secim)

        self.filtreler = []
        for metin, kimlik in (("Tümü", "tumu"), ("Oynanabilir", GA.DURUM_AKTIF),
                              ("Tamamlandı", GA.DURUM_TAMAM),
                              ("Kilitli", GA.DURUM_KILITLI)):
            b = FiltreDugmesi(metin, kimlik)
            b.clicked.connect(lambda _c, k=kimlik: self._filtre_sec(k))
            self.filtreler.append(b)
            araclar.addWidget(b)
        araclar.addStretch(1)
        dis.addLayout(araclar)

        self.kaydirma = QScrollArea()
        self.kaydirma.setWidgetResizable(True)
        self.kaydirma.setFrameShape(QFrame.NoFrame)
        self.kaydirma.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ic = QWidget()
        ic.setObjectName("seffaf")
        self.bolum_alan = QVBoxLayout(ic)
        self.bolum_alan.setContentsMargins(0, 0, 6, 0)
        self.bolum_alan.setSpacing(3)
        self.kaydirma.setWidget(ic)
        dis.addWidget(self.kaydirma, 1)

        self.alt = QLabel("")
        self.alt.setObjectName("minik")
        self.alt.setAlignment(Qt.AlignRight)
        dis.addWidget(self.alt)
        return kutu

    # -------------------------------------------------------------- olay ----
    def _filtre_sec(self, kimlik):
        self._durum = kimlik
        for b in self.filtreler:
            b.sec(b.kimlik == kimlik)
        self._suzgeci_uygula()

    def _secim_degisti(self, indeks):
        kimlik = ["tumu", GA.DURUM_AKTIF, GA.DURUM_TAMAM,
                  GA.DURUM_KILITLI][max(0, min(3, indeks))]
        self._filtre_sec(kimlik)
        for b in self.filtreler:
            b.sec(b.kimlik == self._durum)
        self.secim.blockSignals(True)
        self.secim.setCurrentIndex(["tumu", GA.DURUM_AKTIF, GA.DURUM_TAMAM,
                                    GA.DURUM_KILITLI].index(self._durum))
        self.secim.blockSignals(False)

    def _arama_degisti(self, metin):
        self._arama = metin
        self._liste_kur(bool(metin.strip()))

    def _suzgeci_uygula(self):
        kelime = self._arama.strip()
        toplam = 0
        for b in self._bolumler:
            toplam += b.uygula(self._arama, self._durum)
        if not self.harita:
            return
        o = self.harita["ozet"]
        bolum = sum(1 for b in self._bolumler if b.isVisible())
        if kelime or self._durum != "tumu":
            on = '"%s" · ' % kelime if kelime else ""
            self.alt.setText("%s%d görev · %d bölüm" % (on, toplam, bolum))
        else:
            self.alt.setText("Toplam %d bölüm · %d görev" % (o["bolum"], o["toplam"]))

    def _uygun(self, dugum):
        if self._durum != "tumu" and dugum.get("durum") != self._durum:
            return False
        kelime = self._arama.strip().lower()
        if not kelime:
            return True
        havuz = ("%s %s" % (dugum.get("ad", ""),
                            dugum.get("aciklama") or "")).lower()
        return kelime in havuz

    def _liste_kur(self, filtreli):
        """Bölüm listesini kurar; satırlar yalnız açılan bölümde üretilir."""
        if not self.harita:
            return
        onceki = self._secili
        Y.yerlesim_temizle(self.bolum_alan)
        self._bolumler = []
        gruplar = {}
        for g in self.harita["dugumler"]:
            gruplar.setdefault(g["arsiv"], []).append(g)
        for arsiv in self.harita["arsivler"]:
            tum = gruplar.get(arsiv["anahtar"], [])
            dugumler = [g for g in tum if self._uygun(g)] if filtreli else tum
            if filtreli and not dugumler:
                continue
            b = BolumSatiri(arsiv, dugumler, toplam=len(tum))
            b.tiklandi = self._gorev_sec
            self.bolum_alan.addWidget(b)
            self._bolumler.append(b)
        self._ilk_ac(filtreli)
        self._suzgeci_uygula()

    def _ilk_ac(self, filtreli):
        """Oynanabilir görevin bölümünü (yoksa ilk bölümü) açar."""
        hedef = None
        for g in self.harita["dugumler"]:
            if g.get("durum") == GA.DURUM_AKTIF and self._uygun(g):
                hedef = g
                break
        if hedef is None and filtreli and self._bolumler:
            hedef = self._bolumler[0]._tum[0] if self._bolumler[0]._tum else None
        secilecek = None
        for b in self._bolumler:
            if hedef is not None and b.arsiv["anahtar"] == hedef["arsiv"]:
                secilecek = (b, hedef)
                break
        if secilecek is None and self._bolumler:
            b = self._bolumler[0]
            secilecek = (b, b._tum[0] if b._tum else None)
        if secilecek:
            b, g = secilecek
            b.acik_degistir(True)
            if g is not None:
                self._gorev_sec(g)

    def _uygula(self, oyuncular, harita):
        if oyuncular and oyuncular != self._oyuncular:
            self._oyuncular = oyuncular
        Y.yerlesim_temizle(self.bolum_alan)
        self._bolumler = []
        self.harita = harita
        self._secili = None
        self.detay._temizle()
        if not harita or not harita.get("arsivler"):
            self.alt.setText("görev tanımı yok")
            return
        o = harita["ozet"]
        oran = (o["tamam"] / float(o["toplam"])) if o["toplam"] else 0.0
        self.altBaslik.setText("%d / %d tamamlandı" % (o["tamam"], o["toplam"]))
        self.yuzde.setText("%%%d" % round(oran * 100))
        self.cubuk.set_oran(oran)
        self.rozetBolum.deger.setText(str(o["bolum"]))
        self.rozetAktif.deger.setText(str(o["aktif"]))
        self.rozetTamam.deger.setText(str(o["tamam"]))
        self._liste_kur(False)

    def _bolumu_kur(self, bolum, gruplar=None):
        if bolum._kuruldu:
            return
        if gruplar is None:
            gruplar = {}
            for g in self.harita["dugumler"]:
                gruplar.setdefault(g["arsiv"], []).append(g)
        bolum.kur(gruplar.get(bolum.arsiv["anahtar"], []), acik=False)

    def _gorev_sec(self, dugum):
        self._secili = dugum
        for b in self._bolumler:
            for s in b.satirlar:
                s.sec(s.dugum is dugum)
        self.detay.goster(dugum, self._takip_degistir, self._baslat)

    def _takip_degistir(self, dugum):
        try:
            ayar = dict(self.h.ayar)
            takip = ayar.get("takipGorev")
            ayar["takipGorev"] = None if takip == dugum.get("no") else dugum.get("no")
            from core import store as _S
            _S.kaydet(ayar)
            self.h.ayar = ayar
        except Exception:
            pass
        self.detay.goster(dugum, self._takip_degistir, self._baslat)

    def _baslat(self, dugum):
        try:
            from core import store as _S
            ayar = dict(self.h.ayar)
            ayar["takipGorev"] = dugum.get("no")
            _S.kaydet(ayar)
            self.h.ayar = ayar
        except Exception:
            pass
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(dugum.get("ad") or "")
        self.detay.goster(dugum, self._takip_degistir, self._baslat)

    def goster(self):
        if not self._yuklendi:
            self._yuklendi = True
            self._yukle()

    def gizle(self):
        pass


class Cubuk(QWidget):
    """6px yuvarlak ilerleme çubuğu."""

    def __init__(self, ebeveyn=None):
        super().__init__(ebeveyn)
        self.oran = 0.0
        self.setFixedHeight(7)

    def set_oran(self, oran):
        self.oran = max(0.0, min(1.0, float(oran)))
        self.update()

    def paintEvent(self, olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        h = self.height()
        boya.setPen(Qt.NoPen)
        boya.setBrush(QColor("#1B2421"))
        boya.drawRoundedRect(QRectF(0, 0, self.width(), h), h / 2.0, h / 2.0)
        if self.oran > 0:
            boya.setBrush(QColor(YESIL))
            boya.drawRoundedRect(QRectF(0, 0, max(h, self.width() * self.oran), h),
                                 h / 2.0, h / 2.0)
        boya.end()