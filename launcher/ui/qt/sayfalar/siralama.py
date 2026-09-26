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

UST_ETIKET = "ARKADAŞLARIN"
SAYFA_BASLIK = "Dünya kayıtları."
SAYFA_ACIKLAMA = "Dört kişi ölçüde kim önce, tek ekranda gör."


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
                                              "DGMCRAFT / SIRALAMA")
        dis.addWidget(self.baslikAlani)
        icKutu = QWidget()
        dis.addWidget(icKutu, 1)
        ic = QVBoxLayout(icKutu)
        ic.setContentsMargins(T.IC_PAY, 0, T.IC_PAY, 0)
        ic.setSpacing(T.KART_ARALIK)

        # --- dört yatay kategori sekmesi ---
        self.sekmeler = T.Sekmeler(["En zengin", "En son oynayan",
                                    "En uzun oynayan", "En yetenekli"])
        for _b in self.sekmeler.dugmeler:
            _b.clicked.connect(self._sekme_tik)
        ic.addWidget(self.sekmeler)

        # --- ana sıralama kartı + siyah "Diğer zirveler" kartı ---
        govde = QHBoxLayout()
        govde.setSpacing(T.KART_ARALIK)

        self.anaKart = QFrame()
        self.anaKart.setObjectName("kart")
        self.anaKart.setFixedWidth(779)
        anaGovde = QVBoxLayout(self.anaKart)
        anaGovde.setContentsMargins(20, 18, 20, 18)
        anaGovde.setSpacing(10)

        anaUst = QHBoxLayout()
        anaUst.setContentsMargins(0, 0, 0, 0)
        self.anaBaslik = T.etiket("SIRALAMA", "bolumAltBaslik")
        anaUst.addWidget(self.anaBaslik)
        anaUst.addStretch(1)
        yenile = T.dugme("Yenile", "kontrast")
        yenile.setFixedHeight(30)
        yenile.clicked.connect(self._yukle)
        anaUst.addWidget(yenile)
        anaGovde.addLayout(anaUst)
        self.kaynakEtiketi = T.etiket("", "minik")
        anaGovde.addWidget(self.kaynakEtiketi)

        self.kaydirma = QScrollArea()
        self.kaydirma.setWidgetResizable(True)
        self.kaydirma.setFrameShape(QFrame.NoFrame)
        icDugum = QWidget()
        self.govde = QVBoxLayout(icDugum)
        self.govde.setContentsMargins(0, 0, 0, 0)
        self.govde.setSpacing(4)
        self.kaydirma.setWidget(icDugum)
        anaGovde.addWidget(self.kaydirma, 1)
        self.anaAlt = T.etiket("", "minik")
        anaGovde.addWidget(self.anaAlt)
        govde.addWidget(self.anaKart, 1)

        self.zirveKart = T.kart("siyah")
        self.zirveKart.setFixedWidth(411)
        zirveGovde = QVBoxLayout(self.zirveKart)
        zirveGovde.setContentsMargins(20, 18, 20, 18)
        zirveGovde.setSpacing(12)
        zirveGovde.addWidget(T.etiket("DİĞER ZİRVELER", "bolumBaslik"))
        self.zirveGovde = zirveGovde
        zirveGovde.addStretch(1)
        govde.addWidget(self.zirveKart, 0)
        ic.addLayout(govde, 1)

    def _uygula(self, tablolar, canli):
        Y.yerlesim_temizle(self.govde)
        Y.yerlesim_temizle(self.zirveGovde)
        self._tablolar = list(tablolar or [])
        if not self._tablolar:
            self.kaynakEtiketi.setText("Tablo yok")
            self.anaBaslik.setText("Sıralama tablosu bulunamadı")
            bos = T.kart()
            bosGovde = QVBoxLayout(bos)
            bosGovde.setContentsMargins(18, 16, 18, 16)
            bosGovde.setSpacing(8)
            b = T.etiket("Sıralama tablosu bulunamadı", "metin")
            b.setWordWrap(True)
            bosGovde.addWidget(b)
            try:
                from core import siralama as _S
                ipucu = _S.TABLO_YOK_METNI
            except Exception:
                ipucu = ""
            ip = T.etiket(ipucu, "soluk")
            ip.setWordWrap(True)
            ip.setTextInteractionFlags(Qt.TextSelectableByMouse)
            bosGovde.addWidget(ip)
            bosGovde.addStretch(1)
            self.govde.addWidget(bos)
            return
        kaynak = "ajLeaderboards (canlı)" if canli else "yerel veri"
        self.kaynakEtiketi.setText("Kaynak: %s · %d tablo" % (kaynak, len(self._tablolar)))
        self.sekme_degisti(self.sekmeler.indeks)

    def sekme_degisti(self, indeks):
        """Seçili sekmenin tablosunu ana kartta, kalanlar siyah kartta gösterir."""
        if not getattr(self, "_tablolar", None):
            return
        Y.yerlesim_temizle(self.govde)
        Y.yerlesim_temizle(self.zirveGovde)
        indeks = max(0, min(indeks, len(self._tablolar) - 1))
        secili = self._tablolar[indeks]
        self.anaBaslik.setText(secili["ad"])
        self.anaKart.setFixedWidth(779)
        self.govde.addWidget(self._tablo_karti(secili, buyuk=True))
        self.govde.addStretch(1)
        digerleri = [t for i, t in enumerate(self._tablolar) if i != indeks][:3]
        for i, tablo in enumerate(digerleri):
            self.zirveGovde.addWidget(self._ozet_kart(tablo, i + 1))
        self.zirveGovde.addStretch(1)
        if not digerleri:
            self.zirveGovde.addWidget(T.BosDurum("Başka kategori yok."))

    def _tablo_karti(self, tablo, buyuk=False):
        kart = QFrame()
        kart.setObjectName("siyahKart" if buyuk else "kart")
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(20, 18, 20, 18)
        govde.setSpacing(8)
        b = T.etiket(tablo["ad"].upper(), "bolumBaslik")
        govde.addWidget(b)
        k = T.etiket(tablo.get("kaynak", ""), "minik")
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
            bos = T.etiket("Bu tabloda henüz veri yok.", "soluk")
            bos.setWordWrap(True)
            govde.addWidget(bos)
        govde.addStretch(1)
        return kart

    def _ozet_kart(self, tablo, sira):
        """Siyah 'Diğer zirveler' kartındaki tek satırlık özet."""
        kutu = QFrame()
        kutu.setStyleSheet("background: transparent; border: none;")
        govde = QVBoxLayout(kutu)
        govde.setContentsMargins(0, 0, 0, 0)
        govde.setSpacing(4)
        satir = QHBoxLayout()
        satir.setContentsMargins(0, 0, 0, 0)
        satir.addWidget(T.etiket(tablo["ad"].upper(), "listeBaslik"))
        satir.addStretch(1)
        govde.addLayout(satir)
        satirlar = tablo.get("satirlar") or []
        if satirlar:
            for kayit in satirlar[:2]:
                s = QHBoxLayout()
                s.setContentsMargins(0, 0, 0, 0)
                s.setSpacing(8)
                ad = T.etiket(str(kayit.get("ad", "-")), "satirAd")
                s.addWidget(ad)
                s.addStretch(1)
                deger = T.etiket(self._deger_metni(kayit), "satirSag")
                deger.setStyleSheet("color: %s;" % T.VURGU)
                s.addWidget(deger)
                govde.addLayout(s)
        else:
            govde.addWidget(T.etiket("Veri yok", "minik"))
        return kutu

    @staticmethod
    def _deger_metni(kayit):
        """Veri kaynağının hazırladığı metni kullan, yoksa sayıyı biçimlendir."""
        metin = (kayit.get("metin") or "").strip()
        if metin:
            return metin
        for anahtar, birim in (("bakiye", "₺"), ("sure", "dk"),
                              ("seviye", "seviye"), ("xp", "XP")):
            if kayit.get(anahtar) is not None:
                try:
                    return "%.0f %s" % (float(kayit[anahtar]), birim)
                except (TypeError, ValueError):
                    return "%s %s" % (kayit[anahtar], birim)
        deger = kayit.get("deger")
        if isinstance(deger, (int, float)):
            return "%.0f" % deger
        return str(deger if deger is not None else "-")

    def _sekme_tik(self):
        self.sekme_degisti(self.sekmeler.indeks)

    def goster(self):
        self._yukle()

    def gizle(self):
        pass