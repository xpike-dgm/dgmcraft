"""PySide6 Hub (05-night): siyah hero + turuncu durum kartı + üç bilgi kartı.
Sunucu başlatma, RAM, çevrimiçi ve haber mantığı korunur."""
import threading

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QScrollArea,
                               QSizePolicy, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Hub"
UST_ETIKET = "SUNUCU MERKEZİ"
SAYFA_BASLIK = "Dünyan hazır."
SAYFA_ACIKLAMA = "Arkadaşların aynı dünyada tek dokunuşla oynadığı yer."

HEAP_SECENEKLERI = (2, 3, 4, 6)


def _kisalt(metin, sinir):
    metin = " ".join((metin or "").split())
    if len(metin) <= sinir:
        return metin
    return metin[:sinir].rsplit(" ", 1)[0] + "…"


class HubSayfasi(QWidget):
    """Durum + RAM + oyuncu listesi. UI dışı işler arka plan iş parçacığında."""

    durum_hazir = Signal(str)          # HAZIR | YAYINDA | MİSAFİR | BAKIMDA
    durum_eylem = Signal(str, str)     # baslatilabilir | host | misafir | bakim
    oyuncular_hazir = Signal(list)
    baslat_sonuc = Signal(str)
    kapat_sonuc = Signal(str)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._calisiyor = False
        self._baslatiliyor = False
        self._zamanlayici = None
        self._arayuz_kur()

    # ---------- kurulum ----------
    def baslik_alani_guncelle(self, ust, baslik, aciklama):
        self.baslikAlani.ustYazi.setText(ust.upper())
        self.baslikAlani.baslikYazi.setText(baslik)
        self.baslikAlani.aciklamaYazi.setText(aciklama)

    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(0)

        self.baslikAlani = T.BaslikAlani(UST_ETIKET, SAYFA_BASLIK, SAYFA_ACIKLAMA,
                                         "DGMCRAFT / HUB")
        dis.addWidget(self.baslikAlani)

        govde = QVBoxLayout()
        govde.setContentsMargins(T.IC_PAY, 0, T.IC_PAY, 0)
        govde.setSpacing(14)

        # --- üst satır: siyah hero + turuncu durum kartı (262px) ---
        ust = QHBoxLayout()
        ust.setSpacing(14)
        ust.addWidget(self._hero_kart(), 756)
        ust.addWidget(self._durum_kart(), 436)
        govde.addLayout(ust)

        # --- alt satır: üç kart (262px) ---
        alt = QHBoxLayout()
        alt.setSpacing(14)
        alt.addWidget(self._bellek_kart(), 1)
        alt.addWidget(self._bilgi_kart(), 1)
        alt.addWidget(self._haber_kart(), 1)
        govde.addLayout(alt, 1)
        dis.addLayout(govde, 1)

        self.durum_hazir.connect(self._durum_uygula)
        self.durum_eylem.connect(self._eylem_uygula)
        self.oyuncular_hazir.connect(self._oyuncu_uygula)
        self.baslat_sonuc.connect(self._baslat_bitti)
        self.kapat_sonuc.connect(self._kapat_bitti)

    # ---------- siyah hero (756x262) ----------
    def _hero_kart(self):
        hero = QFrame()
        hero.setObjectName("siyahKart")
        hero.setFixedHeight(262)

        dis = QHBoxLayout(hero)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(0)

        # 8px turuncu sol şerit
        self.serit = QFrame()
        self.serit.setFixedWidth(8)
        self.serit.setStyleSheet("background: %s; border: none;" % T.VURGU)
        dis.addWidget(self.serit)

        sol = QVBoxLayout()
        sol.setContentsMargins(24, 22, 12, 22)
        sol.setSpacing(0)
        sol.addStretch(1)

        self.rozet = QFrame()
        self.rozet.setFixedHeight(22)
        self.rozet.setStyleSheet(
            "background: %s; border-radius: 3px;" % T.YESIL)
        self.rozet.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        rozetSatir = QHBoxLayout(self.rozet)
        rozetSatir.setContentsMargins(9, 0, 9, 0)
        self.rozetYazi = QLabel("HAZIR")
        self.rozetYazi.setObjectName("rozetYazi")
        self.rozetYazi.setStyleSheet(
            "color: %s; font-size: 10px; font-weight: 700;"
            " letter-spacing: 2px; background: transparent;" % T.YAZI)
        rozetSatir.addWidget(self.rozetYazi)
        sol.addWidget(self.rozet)
        sol.addSpacing(14)

        self.baslik = QLabel("Oyunu başlat,\ndünyayı paylaş.")
        self.baslik.setObjectName("heroBaslik")
        self.baslik.setStyleSheet(
            "font-size: 32px; font-weight: 700; color: %s; line-height: 118%%;"
            % T.YAZI)
        sol.addWidget(self.baslik)
        sol.addSpacing(8)

        self.aciklama = QLabel("3 kişilik özel Survival+ sunucun.")
        self.aciklama.setObjectName("heroMetin")
        self.aciklama.setStyleSheet("font-size: 12px; color: %s;" % T.IKINCIL)
        self.aciklama.setWordWrap(True)
        self.aciklama.setMaximumWidth(430)
        sol.addWidget(self.aciklama)
        sol.addSpacing(18)

        self.eylemSatiri = QHBoxLayout()
        self.eylemSatiri.setContentsMargins(0, 0, 0, 0)
        self.eylemSatiri.setSpacing(10)
        self.eylemDugmesi = T.dugme("▸  Sunucuyu başlat", "ana")
        self.eylemDugmesi.setFixedHeight(36)
        self.eylemDugmesi.clicked.connect(self._eylem_tik)
        self.eylemDugmesi.setVisible(False)
        self.eylemSatiri.addWidget(self.eylemDugmesi)
        self.eylemYazi = T.etiket("Durum okunuyor...", "kucuk")
        self.eylemSatiri.addWidget(self.eylemYazi)
        self.eylemSatiri.addStretch(1)
        sol.addLayout(self.eylemSatiri)
        sol.addStretch(1)
        dis.addLayout(sol, 1)

        # sağdaki gerçek amblem
        marka = QLabel()
        marka.setPixmap(T.mark_pixmap(120))
        marka.setAlignment(Qt.AlignCenter)
        marka.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        dis.addWidget(marka, 0, Qt.AlignCenter)
        return hero

    # ---------- turuncu durum kartı (436x262) ----------
    def _durum_kart(self):
        kart = QFrame()
        kart.setObjectName("vurguKart")
        kart.setFixedHeight(262)
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(24, 22, 24, 22)
        govde.setSpacing(0)
        govde.addWidget(T.etiket("BUGÜN", "vurguUst"))
        govde.addSpacing(10)
        self.durumSayac = QLabel("0")
        self.durumSayac.setObjectName("vurguSayac")
        govde.addWidget(self.durumSayac)
        govde.addWidget(T.etiket("çevrimiçi oyuncu", "vurguAlt"))
        govde.addStretch(1)
        self.durumSatiri = T.ayirici("#C97C1C")
        govde.addWidget(self.durumSatiri)
        govde.addSpacing(10)
        alt = QHBoxLayout()
        alt.setContentsMargins(0, 0, 0, 0)
        self.baglantiYazi = T.etiket("Bağlantı", "vurguAlt")
        self.baglantiYazi.setObjectName("vurguAltKalin")
        alt.addWidget(self.baglantiYazi)
        alt.addStretch(1)
        self.durumMetin = T.etiket("Sunucu kapalı", "vurguAlt")
        self.durumMetin.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        alt.addWidget(self.durumMetin)
        govde.addLayout(alt)
        return kart

    # ---------- bellek kartı ----------
    def _bellek_kart(self):
        kart = T.kart()
        kart.setFixedHeight(262)
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(20, 18, 20, 18)
        govde.setSpacing(6)

        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        ust.addWidget(T.etiket("01 / BELLEK", "bolumBaslik"))
        ust.addStretch(1)
        govde.addLayout(ust)
        govde.addSpacing(6)

        self.bellekDeger = QLabel("%d GB" % self.h.heap_al())
        self.bellekDeger.setObjectName("kartSayac")
        govde.addWidget(self.bellekDeger)
        self.bellekAlt = T.etiket("Sunucuya ayrılan RAM", "metrikAlt")
        govde.addWidget(self.bellekAlt)
        govde.addSpacing(14)

        self.bellekCubuk = self._mini_cubuk()
        govde.addWidget(self.bellekCubuk)
        govde.addSpacing(6)

        self.bellekKaydirici = Y.BellekKaydirici(
            ["%dG" % gb for gb in HEAP_SECENEKLERI],
            HEAP_SECENEKLERI.index(self.h.heap_al())
            if self.h.heap_al() in HEAP_SECENEKLERI else 1)
        self.bellekKaydirici.deger_degisti.connect(self._bellek_degisti)
        govde.addWidget(self.bellekKaydirici)
        govde.addStretch(1)
        self.degistirDugmesi = T.dugme("Değişikliği uygula", "kontrast")
        self.degistirDugmesi.clicked.connect(self._bellek_degisti_now)
        govde.addWidget(self.degistirDugmesi)
        return kart

    def _mini_cubuk(self):
        from PySide6.QtWidgets import QProgressBar
        c = QProgressBar()
        c.setProperty("rol", "ince")
        c.setTextVisible(False)
        c.setRange(0, 6)
        c.setValue(self.h.heap_al())
        return c

    # ---------- sunucu bilgisi kartı ----------
    def _bilgi_kart(self):
        kart = T.kart()
        kart.setFixedHeight(262)
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(20, 18, 20, 18)
        govde.setSpacing(6)
        govde.addWidget(T.etiket("02 / SUNUCU", "bolumBaslik"))
        govde.addSpacing(6)
        self.surumDeger = QLabel(str(self.h.surum))
        self.surumDeger.setObjectName("kartSayacKucuk")
        govde.addWidget(self.surumDeger)
        self.surumAlt = T.etiket("Sürüm 2026-09-23-1", "metrikAlt")
        govde.addWidget(self.surumAlt)
        govde.addStretch(1)
        self.bilgiSatirlari = {}
        for ad in ("Sürüm", "Motor", "Bellek"):
            satir = QHBoxLayout()
            satir.setContentsMargins(0, 0, 0, 0)
            satir.addWidget(T.etiket(ad, "soluk"))
            satir.addStretch(1)
            sag = T.etiket("-", "metin")
            sag.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            satir.addWidget(sag)
            govde.addLayout(satir)
            self.bilgiSatirlari[ad] = sag
        govde.addSpacing(10)
        alt = QHBoxLayout()
        alt.setContentsMargins(0, 0, 0, 0)
        alt.addWidget(T.etiket("Sunucu klasörü", "soluk"))
        alt.addStretch(1)
        klasorDugme = T.dugme("Klasörü aç", "kontrast")
        klasorDugme.setFixedHeight(30)
        klasorDugme.clicked.connect(self._klasor_ac)
        alt.addWidget(klasorDugme)
        govde.addLayout(alt)
        self._bilgi_guncelle(0)
        return kart

    # ---------- haber kartı ----------
    def _haber_kart(self):
        kart = T.kart()
        kart.setFixedHeight(262)
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(20, 18, 20, 14)
        govde.setSpacing(8)
        govde.addWidget(T.etiket("03 / HABERLER", "bolumBaslik"))
        govde.addSpacing(4)
        try:
            from core import haber as _H
            veri = _H.changelog_oku(self.h.kok, 3)
        except Exception:
            veri = []
        if not veri:
            veri = [("Sürüm %s" % self.h.surum, "")]
        kaydirma = QScrollArea()
        kaydirma.setWidgetResizable(True)
        kaydirma.setFrameShape(QFrame.NoFrame)
        ic = QWidget()
        liste = QVBoxLayout(ic)
        liste.setContentsMargins(0, 0, 8, 0)
        liste.setSpacing(9)
        for baslik, ozet in veri:
            satir = QHBoxLayout()
            satir.setContentsMargins(0, 0, 0, 0)
            satir.setSpacing(9)
            nokta = QFrame()
            nokta.setFixedSize(6, 6)
            nokta.setStyleSheet("background: %s; border-radius: 3px;"
                                " border: none;" % T.VURGU)
            satir.addWidget(nokta, 0, Qt.AlignTop)
            kutu = QVBoxLayout()
            kutu.setContentsMargins(0, 0, 0, 0)
            kutu.setSpacing(2)
            y1 = QLabel(baslik)
            y1.setObjectName("satirAd")
            kutu.addWidget(y1)
            if ozet:
                y2 = QLabel(_kisalt(ozet, 110))
                y2.setObjectName("minik")
                y2.setWordWrap(True)
                kutu.addWidget(y2)
            satir.addLayout(kutu, 1)
            liste.addLayout(satir)
        liste.addStretch(1)
        kaydirma.setWidget(ic)
        govde.addWidget(kaydirma, 1)
        return kart

    # ---------- oyuncu listesi (durum kartının altına gömülü değil, yardımcı) ----------
    def _oyuncu_kart(self):
        kart = T.kart()
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(20, 18, 20, 18)
        govde.setSpacing(8)
        ust = QHBoxLayout()
        ust.addWidget(T.etiket("ÇEVRİMİÇİ", "bolumBaslik"))
        ust.addStretch(1)
        self.oyuncuSayac = T.etiket("0/3", "satirSag")
        ust.addWidget(self.oyuncuSayac)
        govde.addLayout(ust)
        self.oyuncuListe = QVBoxLayout()
        self.oyuncuListe.setContentsMargins(0, 0, 0, 0)
        self.oyuncuListe.setSpacing(4)
        govde.addLayout(self.oyuncuListe)
        self.oyuncuBos = T.etiket("Sunucu kapalıyken liste yok.", "minik")
        self.oyuncuBos.setWordWrap(True)
        govde.addWidget(self.oyuncuBos)
        self.kopyalaDugmesi = T.dugme("Davet Adresini Kopyala", "ikincil")
        self.kopyalaDugmesi.clicked.connect(self._davet_kopyala)
        govde.addWidget(self.kopyalaDugmesi)
        return kart

    def _bellek_degisti(self, deger):
        deger = max(0, min(len(HEAP_SECENEKLERI) - 1, int(deger)))
        gb = HEAP_SECENEKLERI[deger]
        self.bellekDeger.setText("%d GB" % gb)
        self.bellekCubuk.setValue(gb)
        self.bellekRozet = getattr(self, "bellekRozet", None)
        if self.bellekRozet is not None:
            self.bellekRozet.setText("%dG" % gb)
        try:
            self.h.heap_kaydet(gb)
        except Exception:
            pass

    def _bellek_degisti_now(self):
        self.degistirDugmesi.setText("Uygulandı")
        QTimer.singleShot(1600, lambda: self.degistirDugmesi.setText(
            "Değişikliği uygula"))

    def _klasor_ac(self):
        try:
            from core import paths as _P
            import os
            os.startfile(self.h.kok)
        except Exception:
            pass

    def _bilgi_guncelle(self, oyuncu_sayisi):
        try:
            self.bilgiSatirlari["Sürüm"].setText(str(self.h.surum))
            self.bilgiSatirlari["Bellek"].setText("%d GB" % self.h.heap_al())
            self.bilgiSatirlari["Motor"].setText("Purpur 26.1.2")
            self.durumSayac.setText("0 / 3" if not oyuncu_sayisi
                                    else str(int(oyuncu_sayisi)))
            self.bellekDeger.setText("%d GB" % self.h.heap_al())
            self.bellekCubuk.setValue(self.h.heap_al())
        except Exception:
            pass

    # ---------- durum ----------
    def goster(self):
        self._zamanlayici_baslat()
        self._durum_istek()

    def gizle(self):
        self._zamanlayici_durdur()

    def _zamanlayici_baslat(self):
        if self._zamanlayici is not None:
            return
        self._zamanlayici = QTimer(self)
        self._zamanlayici.timeout.connect(self._durum_istek)
        self._zamanlayici.start(1500)

    def _zamanlayici_durdur(self):
        if self._zamanlayici is not None:
            self._zamanlayici.stop()

    def _durum_istek(self):
        if self._calisiyor:
            return
        self._calisiyor = True
        threading.Thread(target=self._durum_hesapla, daemon=True).start()

    def _durum_hesapla(self):
        durum, host, oyuncular = "HAZIR", "", []
        try:
            from core import kilit as _K, version as _V
            if _V.guncelleniyor_mu():
                Y.guvenli_yayin(self.durum_hazir, "BAKIMDA")
                Y.guvenli_yayin(self.durum_eylem, "bakim", "")
                Y.guvenli_yayin(self.oyuncular_hazir, [])
                return
            calisiyor = False
            try:
                proc = self.h.sunucu_al().proc
                calisiyor = bool(proc and proc.poll() is None)
            except Exception:
                calisiyor = False
            dolu, k = _K.kilit_dolu_mu(self.h.kok)
            if calisiyor:
                durum, host = "YAYINDA", ""
            elif dolu:
                durum, host = "MİSAFİR", (k or {}).get("hostAdi", "Bir arkadaş")
            if calisiyor or dolu:
                oyuncular = self._oyuncu_oku()
        except Exception:
            pass
        Y.guvenli_yayin(self.durum_hazir, durum)
        Y.guvenli_yayin(self.durum_eylem, {
            "HAZIR": "baslatilabilir", "YAYINDA": "host",
            "MİSAFİR": "misafir"}.get(durum, "baslatilabilir"), host)
        Y.guvenli_yayin(self.oyuncular_hazir, oyuncular)
        self._calisiyor = False

    def _durum_uygula(self, durum):
        renkler = {"HAZIR": T.YESIL, "YAYINDA": T.YESIL,
                   "MİSAFİR": T.MAVI, "BAKIMDA": T.VURGU}
        yazi = self.rozet.findChild(QLabel, "rozetYazi")
        if yazi is not None:
            yazi.setText(durum)
            yazi.setStyleSheet("color: %s;" % T.SOLUK)
        for lb in self.rozet.findChildren(QLabel):
            if lb is not yazi:
                lb.setStyleSheet("background: %s; border-radius: 3px;"
                                 % renkler.get(durum, T.SILIK))
        if durum == "YAYINDA":
            self.aciklama.setText("Sunucu yayında. Oyuncular bağlanabilir.")
        elif durum == "MİSAFİR":
            self.aciklama.setText("Sunucu şu anda bir arkadaşın tarafından açık.")

    def _eylem_uygula(self, tur, host):
        if tur == "baslatilabilir":
            self.eylemDugmesi.setText("Sunucuyu Başlat")
            self.eylemDugmesi.setVisible(True)
            self.eylemYazi.setVisible(False)
        elif tur == "host":
            self.eylemDugmesi.setText("Güvenli Kapat")
            self.eylemDugmesi.setVisible(True)
            self.eylemYazi.setVisible(False)
        elif tur == "misafir":
            self.eylemDugmesi.setVisible(False)
            self.eylemYazi.setText("%s sunucuyu başlattı — ona katılabilirsin." % host)
            self.eylemYazi.setVisible(True)
        else:
            self.eylemDugmesi.setVisible(False)
            self.eylemYazi.setText("Bakım bitince buradan başlatırsın.")
            self.eylemYazi.setVisible(True)

    # ---------- oyuncular ----------
    def _oyuncu_istek(self):
        threading.Thread(target=self._oyuncu_oku_tam, daemon=True).start()

    def _oyuncu_oku_tam(self):
        try:
            Y.guvenli_yayin(self.oyuncular_hazir, self._oyuncu_oku())
        except Exception:
            pass

    def _oyuncu_oku(self):
        try:
            from core import sunucu as _S
            props = _S.server_properties_oku(self.h.kok)
            rc = _S.RconIstemcisi(port=props.get("rcon.port", 25575),
                                  sifre=props.get("rcon.password", ""))
            ham = rc.komut("list") or ""
            oyuncular = []
            for parca in ham.split(":"):
                parca = parca.strip()
                if not parca or ", " not in parca:
                    continue
                ad, _bolum = parca.split(", ", 1)
                if ad:
                    oyuncular.append(ad)
            return oyuncular
        except Exception:
            return []

    def _oyuncu_uygula(self, oyuncular):
        try:
            Y.yerlesim_temizle(self.oyuncuListe)
            self.oyuncuBos.setVisible(not oyuncular)
            self.oyuncuSayac.setText("%d/3" % len(oyuncular))
            self._bilgi_guncelle(len(oyuncular))
            for ad in oyuncular:
                satir = QFrame()
                satir.setStyleSheet("background: #1A211E; border-radius: 8px;")
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
        except Exception:
            pass

    # ---------- eylemler ----------
    def _eylem_tik(self):
        if self.eylemDugmesi.text() == "Sunucuyu Başlat":
            self._baslat()
        else:
            self._guvenli_kapat()

    def _baslat(self):
        if self._baslatiliyor:
            return
        self._baslatiliyor = True
        self.eylemDugmesi.setEnabled(False)
        self.eylemDugmesi.setText("Başlatılıyor...")
        threading.Thread(target=self._baslat_is, daemon=True).start()

    def _baslat_is(self):
        hata = ""
        try:
            ok, mesaj = self.h.sunucu_baslat()
            if not ok:
                hata = mesaj
        except Exception as e:
            hata = str(e)
        Y.guvenli_yayin(self.baslat_sonuc, hata)

    def _baslat_bitti(self, hata):
        self._baslatiliyor = False
        self.eylemDugmesi.setEnabled(True)
        if hata:
            self.eylemYazi.setText("Başlatılamadı: %s" % hata)
            self.eylemDugmesi.setVisible(False)
            self.eylemYazi.setVisible(True)
        self._durum_istek()

    def _guvenli_kapat(self):
        self.eylemDugmesi.setEnabled(False)
        self.eylemDugmesi.setText("Kapatılıyor...")
        threading.Thread(target=self._kapat_is, daemon=True).start()

    def _kapat_is(self):
        hata = ""
        try:
            def ilerleme(metin):
                self.h.log_kuyrugu.put("[konsol] " + str(metin))
            kapandi, mesaj = self.h.sunucu_kapat(ilerleme)
            if not kapandi:
                hata = mesaj
        except Exception as e:
            hata = str(e)
        Y.guvenli_yayin(self.kapat_sonuc, hata)

    def _kapat_bitti(self, hata):
        self.eylemDugmesi.setEnabled(True)
        if hata:
            self.eylemYazi.setText("Kapatılamadı: %s" % hata)
            self.eylemDugmesi.setVisible(False)
            self.eylemYazi.setVisible(True)
        self._durum_istek()

    def _davet_kopyala(self):
        adres = ""
        try:
            from core import kilit as _K
            dolu, k = _K.kilit_dolu_mu(self.h.kok)
            if dolu and k.get("vpnIp"):
                adres = "%s:%s" % (k.get("vpnIp"), k.get("port", 25565))
        except Exception:
            pass
        if not adres:
            try:
                from core import vpn as _V
                ip = _V.vpn_ip_bul()
                if ip:
                    adres = "%s:25565" % ip
            except Exception:
                pass
        if not adres:
            self.kopyalaDugmesi.setText("Adres bulunamadı")
            QTimer.singleShot(1600, lambda: self.kopyalaDugmesi.setText(
                "Davet Adresini Kopyala"))
            return
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(adres)
        self.kopyalaDugmesi.setText("Kopyalandı")
        QTimer.singleShot(1600, lambda: self.kopyalaDugmesi.setText(
            "Davet Adresini Kopyala"))