"""PySide6 Hub: hero + başlat/kapat + bellek slider + çevrimiçi + haberler."""
import threading

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QPushButton,
                               QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Hub"

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
    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(T.KART_ARALIK)

        self.hero = Y.HeroCerceve(
            self, T.HERO_UST, T.HERO_ALT, T.VURGU, guc=0.15,
            gorsel=Y.pixmap("v2", "hub-hero-soft.png"))
        if self.hero._gorsel is not None and not self.hero._gorsel.isNull():
            self.hero._gorsel = self.hero._gorsel.scaledToHeight(
                182, Qt.SmoothTransformation)
        dis.addWidget(self.hero)

        katman = QVBoxLayout(self.hero)
        katman.setContentsMargins(26, 24, 26, 20)
        katman.setSpacing(0)
        katman.addStretch(1)

        self.rozet = Y.rozet(self.hero, "HAZIR", T.YESIL)
        self.rozetKutu = QHBoxLayout()
        self.rozetKutu.setContentsMargins(0, 0, 0, 0)
        self.rozetKutu.addWidget(self.rozet)
        self.rozetKutu.addStretch(1)
        katman.addLayout(self.rozetKutu)
        katman.addSpacing(12)

        self.baslik = QLabel("Sunucuyu Başlat")
        self.baslik.setObjectName("heroBaslik")
        katman.addWidget(self.baslik)
        katman.addSpacing(4)

        self.aciklama = QLabel("3 kişilik özel Survival+ sunucun.")
        self.aciklama.setObjectName("heroMetin")
        self.aciklama.setWordWrap(True)
        self.aciklama.setMaximumWidth(430)
        katman.addWidget(self.aciklama)
        katman.addSpacing(18)

        self.eylemSatiri = QHBoxLayout()
        self.eylemSatiri.setContentsMargins(0, 0, 0, 0)
        self.eylemSatiri.setSpacing(10)
        self.eylemDugmesi = QPushButton("Sunucuyu Başlat")
        self.eylemDugmesi.setObjectName("anaDugme")
        self.eylemDugmesi.setCursor(Qt.PointingHandCursor)
        self.eylemDugmesi.clicked.connect(self._eylem_tik)
        self.eylemSatiri.addWidget(self.eylemDugmesi)
        self.eylemDugmesi.setVisible(False)
        self.eylemYazi = QLabel("Durum okunuyor...")
        self.eylemYazi.setObjectName("kucuk")
        self.eylemSatiri.addWidget(self.eylemYazi)
        self.eylemSatiri.addStretch(1)
        katman.addLayout(self.eylemSatiri)
        katman.addStretch(1)

        alt = QHBoxLayout()
        alt.setSpacing(T.KART_ARALIK)
        sol = QVBoxLayout()
        sol.setSpacing(T.KART_ARALIK)
        sol.addWidget(self._bellek_kart())
        self.haberKart = self._haber_kart()
        sol.addWidget(self.haberKart)
        sol.addWidget(self._bilgi_kart(), 1)
        alt.addLayout(sol, 1)
        alt.addWidget(self._oyuncu_kart(), 0)
        dis.addLayout(alt, 1)

        self.durum_hazir.connect(self._durum_uygula)
        self.durum_eylem.connect(self._eylem_uygula)
        self.oyuncular_hazir.connect(self._oyuncu_uygula)
        self.baslat_sonuc.connect(self._baslat_bitti)
        self.kapat_sonuc.connect(self._kapat_bitti)

    def _kart(self, ebeveyn=None):
        k = QFrame(ebeveyn or self)
        k.setObjectName("kart")
        return k

    # ---------- bellek kartı ----------
    def _bellek_kart(self):
        kart = self._kart()
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(16, 14, 16, 14)
        govde.setSpacing(2)

        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        etiket = QLabel("SUNUCU BELLEĞİ")
        etiket.setObjectName("bolumBaslik")
        ust.addWidget(etiket)
        ust.addStretch(1)
        self.bellekRozet = QLabel("3G")
        self.bellekRozet.setStyleSheet("color: %s; font-size: 12px; font-weight: 600;" % T.VURGU)
        ust.addWidget(self.bellekRozet)
        govde.addLayout(ust)

        ipucu = QLabel("Sunucuya ayrılacak maksimum RAM miktarı")
        ipucu.setObjectName("kucuk")
        govde.addWidget(ipucu)
        govde.addSpacing(10)

        self.bellekKaydirici = Y.BellekKaydirici(
            ["%dG" % gb for gb in HEAP_SECENEKLERI],
            HEAP_SECENEKLERI.index(self.h.heap_al())
            if self.h.heap_al() in HEAP_SECENEKLERI else 1)
        self.bellekKaydirici.deger_degisti.connect(self._bellek_degisti)
        govde.addWidget(self.bellekKaydirici)
        govde.addSpacing(2)

        not_ = QLabel("Sonraki başlatmada geçerli olur.")
        not_.setObjectName("minik")
        govde.addWidget(not_)
        return kart

    def _bellek_degisti(self, deger):
        deger = max(0, min(len(HEAP_SECENEKLERI) - 1, int(deger)))
        self.bellekRozet.setText("%dG" % HEAP_SECENEKLERI[deger])
        try:
            self.h.heap_kaydet(HEAP_SECENEKLERI[deger])
        except Exception:
            pass

    def _bilgi_kart(self):
        kart = self._kart()
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(16, 14, 16, 14)
        govde.setSpacing(8)
        etiket = QLabel("SUNUCU BİLGİSİ")
        etiket.setObjectName("bolumBaslik")
        govde.addWidget(etiket)
        govde.addSpacing(2)
        self.bilgiSatirlari = {}
        for ad in ("Sürüm", "Oyuncu", "Bellek", "Motor"):
            satir = QHBoxLayout()
            satir.setContentsMargins(0, 0, 0, 0)
            sol = QLabel(ad)
            sol.setObjectName("kucuk")
            satir.addWidget(sol)
            satir.addStretch(1)
            sag = QLabel("-")
            sag.setObjectName("metin")
            sag.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            satir.addWidget(sag)
            govde.addLayout(satir)
            self.bilgiSatirlari[ad] = sag
        govde.addStretch(1)
        self._bilgi_guncelle(0)
        return kart

    def _bilgi_guncelle(self, oyuncu_sayisi):
        try:
            self.bilgiSatirlari["Sürüm"].setText(str(self.h.surum))
            self.bilgiSatirlari["Oyuncu"].setText("%d / 3" % int(oyuncu_sayisi))
            self.bilgiSatirlari["Bellek"].setText("%d GB" % self.h.heap_al())
            self.bilgiSatirlari["Motor"].setText("Purpur 26.2")
        except Exception:
            pass

    def _bellek_degisti(self, deger):
        deger = max(0, min(len(HEAP_SECENEKLERI) - 1, int(deger)))
        self.bellekRozet.setText("%dG" % HEAP_SECENEKLERI[deger])
        try:
            self.h.heap_kaydet(HEAP_SECENEKLERI[deger])
        except Exception:
            pass

    # ---------- haber kartı ----------
    def _haber_kart(self):
        kart = self._kart()
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(16, 14, 16, 14)
        govde.setSpacing(8)
        etiket = QLabel("HABERLER")
        etiket.setObjectName("bolumBaslik")
        govde.addWidget(etiket)
        govde.addSpacing(4)
        try:
            from core import haber as _H
            veri = _H.changelog_oku(self.h.kok, 3)
        except Exception:
            veri = []
        if not veri:
            veri = [("Sürüm %s" % self.h.surum, "")]
        for baslik, ozet in veri:
            satir = QHBoxLayout()
            satir.setContentsMargins(0, 0, 0, 0)
            satir.setSpacing(10)
            nokta = QFrame()
            nokta.setFixedSize(5, 5)
            nokta.setStyleSheet("background: %s; border-radius: 2px;" % T.VURGU)
            satir.addWidget(nokta, 0, Qt.AlignTop)
            satir.addSpacing(2)
            kutu = QVBoxLayout()
            kutu.setContentsMargins(0, 0, 0, 0)
            kutu.setSpacing(3)
            y1 = QLabel(baslik)
            y1.setObjectName("metin")
            kutu.addWidget(y1)
            if ozet:
                y2 = QLabel(_kisalt(ozet, 96))
                y2.setObjectName("kucuk")
                y2.setWordWrap(True)
                kutu.addWidget(y2)
            satir.addLayout(kutu, 1)
            govde.addLayout(satir)
        govde.addStretch(1)
        return kart

    # ---------- oyuncu kartı ----------
    def _oyuncu_kart(self):
        kart = self._kart()
        kart.setFixedWidth(300)
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(16, 14, 16, 14)
        govde.setSpacing(8)
        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        etiket = QLabel("ÇEVRİMİÇİ")
        etiket.setObjectName("bolumBaslik")
        ust.addWidget(etiket)
        ust.addStretch(1)
        self.oyuncuSayac = QLabel("0/3")
        self.oyuncuSayac.setObjectName("kucuk")
        ust.addWidget(self.oyuncuSayac)
        govde.addLayout(ust)
        govde.addSpacing(2)

        self.oyuncuListe = QVBoxLayout()
        self.oyuncuListe.setContentsMargins(0, 0, 0, 0)
        self.oyuncuListe.setSpacing(6)
        govde.addLayout(self.oyuncuListe)
        govde.addStretch(1)
        self.oyuncuBos = QLabel("Sunucu kapalıyken liste yok.")
        self.oyuncuBos.setObjectName("kucuk")
        self.oyuncuBos.setWordWrap(True)
        govde.addWidget(self.oyuncuBos)
        govde.addSpacing(12)

        self.kopyalaDugmesi = QPushButton("Davet Adresini Kopyala")
        self.kopyalaDugmesi.setObjectName("hayaletDugme")
        self.kopyalaDugmesi.setCursor(Qt.PointingHandCursor)
        self.kopyalaDugmesi.clicked.connect(self._davet_kopyala)
        govde.addWidget(self.kopyalaDugmesi)
        return kart

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
                self.durum_hazir.emit("BAKIMDA")
                self.durum_eylem.emit("bakim", "")
                self.oyuncular_hazir.emit([])
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
        self.durum_hazir.emit(durum)
        self.durum_eylem.emit({
            "HAZIR": "baslatilabilir", "YAYINDA": "host",
            "MİSAFİR": "misafir"}.get(durum, "baslatilabilir"), host)
        self.oyuncular_hazir.emit(oyuncular)
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
            self.oyuncular_hazir.emit(self._oyuncu_oku())
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
        self.baslat_sonuc.emit(hata)

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
        self.kapat_sonuc.emit(hata)

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
