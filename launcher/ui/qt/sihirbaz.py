"""İlk kurulum sihirbazı (PySide6). Uygulamanın kendi boyutunda ve tasarımında.

7 adım: Hoş geldin · Adın · Davet kodun · Dosya eşitleme · Gizli ağ · Arkadaşlar · Hazır
Kurulumu yapmış kullanıcılar bu ekranı hiç görmez (ayar: kurulumTamam)."""
import threading

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit, QProgressBar,
                               QPushButton, QScrollArea, QVBoxLayout, QWidget)

from . import tema as T
from . import yardimci as Y

GENISLIK = T.GENISLIK
YUKSEKLIK = T.YUKSEKLIK

ADIMLAR = [
    ("Hoş geldin", "~2 dk"),
    ("Adın", "~2 dk"),
    ("Davet kodun", "~1 dk"),
    ("Dosya eşitleme", "~1 dk"),
    ("Gizli ağ", "~1 dk"),
    ("Arkadaşlar", "~30 sn"),
    ("Hazır", "bitiş"),
]


class Sihirbaz(QWidget):
    """Çerçevesiz, uygulamanın kabuğuyla aynı boyutta."""

    tamamlandi = Signal()
    _adim_ileti = Signal(str)

    def __init__(self, kok, ayar, ebeveyn=None):
        super().__init__(ebeveyn)
        self.kok = kok
        self.ayar = ayar
        self.adim = 0
        self.sync_ok = False
        self.anahtar_atlandi = False
        self.vpn_kurulu = False
        self.vpn_bagli = False
        self.esles_ok = False
        self.esles_atlandi = False
        self._mesgul = False
        self._adim_ileti.connect(self._ilerleme_goster)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(T.GENISLIK + T.GOLGE, T.YUKSEKLIK + T.GOLGE)
        self._arayuz_kur()

    # ---------- iskelet ----------
    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(11, 11, 11, 11)
        self.pencere = QFrame(self)
        self.pencere.setObjectName("pencere")
        Y.golge(self.pencere, 34, 150, 0)
        dis.addWidget(self.pencere)

        govde = QVBoxLayout(self.pencere)
        govde.setContentsMargins(1, 1, 1, 1)
        govde.setSpacing(0)
        govde.addWidget(self._baslik_kur())

        alt = QHBoxLayout()
        alt.setContentsMargins(0, 0, 0, 0)
        alt.setSpacing(0)
        alt.addWidget(self._ray_kur())

        self.sag = QFrame()
        self.sag.setObjectName("icerik")
        sagDikey = QVBoxLayout(self.sag)
        sagDikey.setContentsMargins(30, 24, 30, 22)
        sagDikey.setSpacing(0)
        self.ustYazi = QLabel("")
        self.ustYazi.setObjectName("minik")
        sagDikey.addWidget(self.ustYazi)
        sagDikey.addSpacing(6)
        self.baslikYazi = QLabel("")
        self.baslikYazi.setObjectName("sihirBaslik")
        sagDikey.addWidget(self.baslikYazi)
        sagDikey.addSpacing(14)

        self.kaydirma = QScrollArea()
        self.kaydirma.setWidgetResizable(True)
        self.kaydirma.setFrameShape(QFrame.NoFrame)
        self.govdeIcerik = QWidget()
        self.govde = QVBoxLayout(self.govdeIcerik)
        self.govde.setContentsMargins(0, 0, 0, 0)
        self.govde.setSpacing(12)
        self.govde.setAlignment(Qt.AlignTop)
        self.kaydirma.setWidget(self.govdeIcerik)
        sagDikey.addWidget(self.kaydirma, 1)
        sagDikey.addSpacing(12)
        self.cubuk = QProgressBar()
        self.cubuk.setObjectName("sihirCubuk")
        self.cubuk.setRange(0, 100)
        self.cubuk.setTextVisible(False)
        self.cubuk.setFixedHeight(4)
        sagDikey.addWidget(self.cubuk)
        sagDikey.addSpacing(14)
        sagDikey.addLayout(self._alt_kur())
        alt.addWidget(self.sag, 1)
        govde.addLayout(alt, 1)

    def _baslik_kur(self):
        cubuk = Y.BaslikCubugu()
        cubuk.setFixedWidth(T.GENISLIK)
        satir = QHBoxLayout(cubuk)
        satir.setContentsMargins(12, 0, 8, 0)
        satir.setSpacing(10)
        logo = Y.pixmap("brand", "mark-480.png")
        if logo is not None and not logo.isNull():
            lb = QLabel()
            lb.setPixmap(logo.scaled(26, 26, Qt.KeepAspectRatio,
                                     Qt.SmoothTransformation))
            lb.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            satir.addWidget(lb)
        ad = QLabel("KURULUM")
        ad.setObjectName("pencereBaslik")
        ad.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(ad)
        satir.addStretch(1)
        kapat = Y.BaslikDugmesi("kapat")
        kapat.clicked.connect(self._kapat)
        satir.addWidget(kapat)
        return cubuk

    def _ray_kur(self):
        ray = QFrame()
        ray.setObjectName("ray")
        ray.setFixedWidth(220)
        dis = QVBoxLayout(ray)
        dis.setContentsMargins(16, 24, 16, 20)
        dis.setSpacing(6)
        self.rayEtiketleri = []
        for i, (ad, _sure) in enumerate(ADIMLAR):
            satir = QHBoxLayout()
            satir.setContentsMargins(0, 0, 0, 0)
            satir.setSpacing(10)
            nokta = QLabel(str(i + 1))
            nokta.setFixedSize(22, 22)
            nokta.setAlignment(Qt.AlignCenter)
            satir.addWidget(nokta)
            yazi = QLabel(ad)
            satir.addWidget(yazi)
            dis.addLayout(satir)
            self.rayEtiketleri.append((nokta, yazi))
        dis.addStretch(1)
        ipucu = QLabel("Her adım bir sonrakini açar.\nİstediğin zaman geri dönebilirsin.")
        ipucu.setObjectName("minik")
        ipucu.setWordWrap(True)
        dis.addWidget(ipucu)
        return ray

    def _alt_kur(self):
        satir = QHBoxLayout()
        satir.setContentsMargins(0, 0, 0, 0)
        satir.setSpacing(10)
        self.geriDugmesi = QPushButton("← Geri")
        self.geriDugmesi.setObjectName("hayaletDugme")
        self.geriDugmesi.setCursor(Qt.PointingHandCursor)
        self.geriDugmesi.clicked.connect(self._geri)
        satir.addWidget(self.geriDugmesi)
        satir.addStretch(1)
        self.ileriDugmesi = QPushButton("Devam Et →")
        self.ileriDugmesi.setObjectName("anaDugme")
        self.ileriDugmesi.setCursor(Qt.PointingHandCursor)
        self.ileriDugmesi.clicked.connect(self._ileri)
        satir.addWidget(self.ileriDugmesi)
        return satir

    def _kapat(self):
        self.close()

    def closeEvent(self, olay):
        from PySide6.QtWidgets import QApplication
        if getattr(self, "_bitis", False):
            super().closeEvent(olay)
            return
        QApplication.quit()

    # ---------- adım çizimi ----------
    def ciz(self):
        for i, (nokta, yazi) in enumerate(self.rayEtiketleri):
            aktif = i == self.adim
            tamam = i < self.adim
            if tamam:
                renk, yazi_rengi = T.YESIL, T.SOLUK
            elif aktif:
                renk, yazi_rengi = T.VURGU, T.YAZI
            else:
                renk, yazi_rengi = "#2A3530", T.SILIK
            nokta.setStyleSheet(
                "background: %s; color: %s; border-radius: 11px; font-size: 11px;"
                " font-weight: 700;" % (renk, "#10100C" if (tamam or aktif) else T.SILIK))
            yazi.setStyleSheet("color: %s; font-size: 12px; font-weight: %s;"
                              " background: transparent;"
                              % (yazi_rengi, "600" if aktif else "400"))
        ad, sure = ADIMLAR[self.adim]
        self.ustYazi.setText("ADIM %d / %d  •  %s" % (self.adim + 1, len(ADIMLAR), sure))
        self.baslikYazi.setText(ad)
        self.cubuk.setValue(int(100 * (self.adim + 1) / len(ADIMLAR)))
        self.geriDugmesi.setVisible(self.adim > 0)
        self.ileriDugmesi.setText("Bitir ve Başla" if self.adim == len(ADIMLAR) - 1
                                 else "Devam Et →")
        Y.yerlesim_temizle(self.govde)
        getattr(self, "_adim_" + ("hosgeldin", "ad", "anahtar", "sync", "vpn",
                                  "arkadas", "hazir")[self.adim])()
        self.govde.addStretch(1)

    # ---------- yardımcılar ----------
    def _aciklama(self, metin):
        lb = QLabel(metin)
        lb.setObjectName("sihirAciklama")
        lb.setWordWrap(True)
        self.govde.addWidget(lb)

    def _not(self, metin, renk=None):
        kutu = QFrame()
        kutu.setObjectName("sihirNot")
        lb = QLabel(metin)
        lb.setWordWrap(True)
        lb.setStyleSheet("color: %s; font-size: 12px; background: transparent;"
                         % (renk or T.SOLUK))
        kutuLayout = QVBoxLayout(kutu)
        kutuLayout.setContentsMargins(14, 10, 14, 10)
        kutuLayout.addWidget(lb)
        self.govde.addWidget(kutu)

    def _girdi(self, yertutucu="", gizli=False, genislik=320):
        e = QLineEdit()
        e.setPlaceholderText(yertutucu)
        e.setFixedWidth(genislik)
        e.setEchoMode(QLineEdit.Password if gizli else QLineEdit.Normal)
        e.setStyleSheet(
            "QLineEdit { background: #0F1513; border: 1px solid %s; border-radius: 10px;"
            " padding: 11px 12px; color: %s; font-size: 14px; }"
            "QLineEdit:focus { border-color: %s; }" % (T.CERCEVE, T.YAZI, T.VURGU))
        self.govde.addWidget(e, 0, Qt.AlignLeft)
        return e

    def _durum_satiri(self, metin, renk=T.SOLUK):
        satir = QHBoxLayout()
        satir.setContentsMargins(0, 0, 0, 0)
        satir.setSpacing(9)
        nokta = QLabel()
        nokta.setFixedSize(8, 8)
        nokta.setStyleSheet("background: %s; border-radius: 4px;" % renk)
        satir.addWidget(nokta, 0, Qt.AlignVCenter)
        lb = QLabel(metin)
        lb.setObjectName("kucuk")
        lb.setWordWrap(True)
        satir.addWidget(lb, 1)
        kutu = QFrame()
        kutu.setObjectName("sihirDurum")
        d = QVBoxLayout(kutu)
        d.setContentsMargins(14, 11, 14, 11)
        d.addLayout(satir)
        self.govde.addWidget(kutu)
        return lb

    def _ilerleme_goster(self, metin):
        try:
            self.notYazi.setText(metin)
        except Exception:
            pass

    def _calistir(self, islev):
        def sarmal():
            try:
                sonuc = islev()
            except Exception as e:
                sonuc = str(e)
            Y.guvenli_yayin(self._adim_ileti, sonuc)
        threading.Thread(target=sarmal, daemon=True).start()

    # ---------- adımlar ----------
    def _adim_hosgeldin(self):
        self._aciklama(
            "3 kişilik arkadaş sunucunu tek düğmeyle yönet. Bu sihirbaz bir kez "
            "çalışır, sonra uygulamayı her açtığında seni atlar.")
        self._not("Kurulumu tamamlamış kullanıcılar bu ekranı görmez.")

    def _adim_ad(self):
        self._aciklama(
            "Sunucuyu kim açtığını bu isimle görünür. Herkes kendi adını yazar.")
        self.adGirdi = self._girdi("Örneğin Xpike")
        mevcut = (self.ayar.get("kullaniciAdi") or "").strip()
        if mevcut:
            self.adGirdi.setText(mevcut)
        self._not("Boş bırakılamaz.")

    def _adim_anahtar(self):
        self._aciklama(
            "Bu kod seni arkadaşlarının özel oyun ağına bağlar. Sadece bu kodu "
            "bilenler girebilir.")
        self.anahtarGirdi = self._girdi("Davet kodunu yapıştır", gizli=True, genislik=380)
        self.anahtarGirdi.textChanged.connect(self._anahtar_taslakla)
        taslak = getattr(self, "_anahtar_taslak", "")
        if taslak:
            self.anahtarGirdi.setText(taslak)
        else:
            try:
                from core import store as _S
                kayitli = _S.anahtar_oku()
                if kayitli:
                    self.anahtarGirdi.setText(kayitli)
            except Exception:
                pass
        self.atlaDugmesi = QPushButton("Kodum yok, sonra eklerim")
        self.atlaDugmesi.setObjectName("hayaletDugme")
        self.atlaDugmesi.setCursor(Qt.PointingHandCursor)
        self.atlaDugmesi.clicked.connect(self._anahtar_atla)
        self.govde.addWidget(self.atlaDugmesi, 0, Qt.AlignLeft)
        self._not("Kodunu alınca Ayarlar > Bağlan ile bağlanırsın.")

    def _anahtar_taslakla(self, metin):
        self._anahtar_taslak = metin

    def _adim_sync(self):
        self._aciklama("Sunucu dosyaların arkadaşlarınla otomatik eşitlenir.")
        self.syncYazi = self._durum_satiri("Kontrol ediliyor...", T.SILIK)
        self.syncKurDugmesi = QPushButton("Dosya eşitlemeyi Kur")
        self.syncKurDugmesi.setObjectName("anaDugme")
        self.syncKurDugmesi.setCursor(Qt.PointingHandCursor)
        self.syncKurDugmesi.clicked.connect(self._sync_kur)
        self.govde.addWidget(self.syncKurDugmesi, 0, Qt.AlignLeft)
        self._not("Yeşile dönmeden devam edemezsin.")
        QTimer.singleShot(50, self._sync_denetle)

    def _adim_vpn(self):
        self._aciklama(
            "Bu program bilgisayarları dışarıdan görünmeyen bir ağda birbirine "
            "bağlar.")
        self.vpnYazi = self._durum_satiri("Kontrol ediliyor...", T.SILIK)
        self.vpnDugmesi = QPushButton("Gizli Ağı Kur ve Bağlan")
        self.vpnDugmesi.setObjectName("anaDugme")
        self.vpnDugmesi.setCursor(Qt.PointingHandCursor)
        self.vpnDugmesi.clicked.connect(self._vpn_kur)
        self.govde.addWidget(self.vpnDugmesi, 0, Qt.AlignLeft)
        self.notYazi = QLabel("Hazır olduğunda burada yazacak.")
        self.notYazi.setObjectName("minik")
        self.notYazi.setWordWrap(True)
        self.govde.addWidget(self.notYazi)
        QTimer.singleShot(50, self._vpn_denetle)

    def _adim_arkadas(self):
        self._aciklama(
            "Arkadaşların cihaz kodunu buraya yaz; eşitleme otomatik kurulur.")
        self.kod1 = self._girdi("Kod 1", genislik=380)
        self.kod2 = self._girdi("Kod 2 (isteğe bağlı)", genislik=380)
        self._kopyalaDugmesi = QPushButton("Kendi cihaz kodunu kopyala")
        self._kopyalaDugmesi.setObjectName("hayaletDugme")
        self._kopyalaDugmesi.setCursor(Qt.PointingHandCursor)
        self._kopyalaDugmesi.clicked.connect(self._kendi_kodu_kopyala)
        self.govde.addWidget(self._kopyalaDugmesi, 0, Qt.AlignLeft)
        self.eslesYazi = self._durum_satiri("Henüz eşleştirilmedi.", T.SILIK)
        self.eslesDugmesi = QPushButton("Eşleştir")
        self.eslesDugmesi.setObjectName("anaDugme")
        self.eslesDugmesi.setCursor(Qt.PointingHandCursor)
        self.eslesDugmesi.clicked.connect(self._esles_kur)
        self.govde.addWidget(self.eslesDugmesi, 0, Qt.AlignLeft)
        self.atlaDugmesi2 = QPushButton("Kodlarım henüz yok, atla")
        self.atlaDugmesi2.setObjectName("hayaletDugme")
        self.atlaDugmesi2.setCursor(Qt.PointingHandCursor)
        self.atlaDugmesi2.clicked.connect(self._esles_atla)
        self.govde.addWidget(self.atlaDugmesi2, 0, Qt.AlignLeft)
        self._not("Kodlar 63 harf olur; elle yazma, kopyala yapıştır yap.")
        QTimer.singleShot(50, self._kendi_kodu_goster)

    def _adim_hazir(self):
        self._aciklama("Hazır! Oynamaya başlayabilirsin.")
        for ad, tamam in (("Adın kaydedildi", True),
                          ("Dosya eşitleme", self.sync_ok),
                          ("Gizli ağ", self.vpn_bagli or self.anahtar_atlandi),
                          ("Arkadaş eşleşmesi", self.esles_ok or self.esles_atlandi)):
            self._durum_satiri(ad, T.YESIL if tamam else T.SILIK)
        self._not("Her şeyi sonra Ayarlar'dan değiştirebilirsin.")

    # ---------- eylemler ----------
    def _anahtar_var(self):
        try:
            return bool(self.anahtarGirdi.text().strip())
        except Exception:
            return False

    def _anahtar_atla(self):
        self.anahtar_atlandi = True
        self._ileri()

    def _sync_denetle(self):
        self._calistir(self._sync_durum_bul)

    def _sync_durum_bul(self):
        from core import esitleme as _E
        if not _E.syncthing_exe():
            return "Syncthing kurulu değil. Aşağıdaki düğmeyle kur."
        yonetici = _E.SyncthingYonetici(self.kok)
        if not yonetici.calisiyor_mu():
            return "Syncthing kurulu ama çalışmıyor. Aşağıdaki düğmeyle başlat."
        self.sync_ok = True
        yuzde = yonetici.ilerleme_yuzdesi() or 0
        return ("Eşitleme çalışıyor (%%%d)." % min(100, int(yuzde))
                if yuzde else "Eşitleme hazır.")

    def _sync_kur(self):
        self.syncKurDugmesi.setEnabled(False)
        self._calistir(self._sync_kur_is)

    def _sync_kur_is(self):
        from core import esitleme as _E
        exe = _E.syncthing_exe()
        if not exe:
            _E.zip_indir(os.path.join(_E.bin_dizini(), "syncthing"))
        yonetici = _E.SyncthingYonetici(self.kok)
        yonetici.sessiz_baslat()
        for _ in range(20):
            if yonetici.calisiyor_mu():
                break
            time_sleep(0.5)
        self.sync_ok = yonetici.calisiyor_mu()
        return ("Eşitleme hazır." if self.sync_ok
                else "Eşitleme başlatılamadı. Tekrar dene.")

    def _vpn_denetle(self):
        self._calistir(self._vpn_durum_bul)

    def _vpn_durum_bul(self):
        from core import vpn as _V
        self.vpn_kurulu = _V.kurulu_mu()
        if not self.vpn_kurulu:
            self.vpnDugmesi.setText("Gizli Ağı Kur ve Bağlan")
            return "Gizli ağ programı kurulu değil. Aşağıdaki düğmeyle kur."
        bagli, ip, _durum = _V.bagli_mi()
        self.vpn_bagli = bool(bagli and ip)
        if self.vpn_bagli:
            self.vpnDugmesi.setText("Gizli Ağa Bağlandı")
            self.vpnDugmesi.setEnabled(False)
            return "Bağlı: %s" % ip
        self.vpnDugmesi.setText("Gizli Ağa Bağlan")
        self.vpnDugmesi.setEnabled(True)
        return "Kurulu ama bağlı değil."

    def _vpn_kur(self):
        self.vpnDugmesi.setEnabled(False)
        self._calistir(self._vpn_kur_is)

    def _vpn_kur_is(self):
        from core import store as _S, vpn as _V
        anahtar = self.anahtarGirdi.text().strip() if hasattr(self, "anahtarGirdi") else ""
        if not anahtar:
            try:
                anahtar = _S.anahtar_oku() or ""
            except Exception:
                anahtar = ""
        if not anahtar:
            return "Bağlantı anahtarı yok. Ayarlar > Bağlan ile sonra bağlanırsın."
        ok, mesaj, _teknik = _V.baglan_veya_kur(anahtar, self.ayar.get("kullaniciAdi", ""))
        self.vpn_bagli = bool(ok)
        if ok:
            try:
                _S.anahtar_kaydet(anahtar)
            except Exception:
                pass
        try:
            self.vpnDugmesi.setText("Gizli Ağa Bağlandı" if ok else "Tekrar Dene")
            self.vpnDugmesi.setEnabled(not ok)
        except Exception:
            pass
        return mesaj

    def _kendi_kodu_goster(self):
        self._calistir(self._kendi_kodu_bul)

    def _kendi_kodu_bul(self):
        from core import esitleme as _E
        yonetici = _E.SyncthingYonetici(self.kok)
        kod = yonetici.kendi_kimligi() or ""
        if kod:
            self.ayar["kendiCihazKodu"] = kod
            try:
                from core import store as _S
                _S.kaydet(self.ayar)
            except Exception:
                pass
            return "Cihaz kodun hazır. Kopyala düğmesiyle al."
        return "Cihaz kodu alınamadı. Dosya eşitleme adımını tamamla."

    def _kendi_kodu_kopyala(self):
        kod = (self.ayar.get("kendiCihazKodu") or "").strip()
        if not kod:
            self._kendi_kodu_goster()
            return
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(kod)
        try:
            self._kopyalaDugmesi.setText("Kopyalandı")
        except Exception:
            pass

    def _esles_atla(self):
        self.esles_atlandi = True
        self._ileri()

    def _esles_kur(self):
        self.eslesDugmesi.setEnabled(False)
        self._calistir(self._esles_kur_is)

    def _esles_kur_is(self):
        from core import esitleme as _E, store as _S
        yonetici = _E.SyncthingYonetici(self.kok)
        kendi = (self.ayar.get("kendiCihazKodu") or "").strip()
        arkadas = [self.kod1.text().strip(), self.kod2.text().strip()]
        arkadas = [a for a in arkadas if a]
        if not kendi:
            return "Önce kendi cihaz kodunu al."
        if not arkadas:
            return "Arkadaş kodu gir."
        yonetici.otomatik_yapilandir(kendi, arkadas)
        self.esles_ok = True
        self.ayar["arkadasKodlari"] = arkadas
        _S.kaydet(self.ayar)
        return "Eşleştirme tamam."

    # ---------- gezinme ----------
    def _ileri(self):
        if self.adim == 1:
            ad = self.adGirdi.text().strip()
            if not ad:
                self.baslikYazi.setText("Adın")
                return
            self.ayar["kullaniciAdi"] = ad
        elif self.adim == 2 and self._anahtar_var():
            try:
                from core import store as _S
                _S.anahtar_kaydet(self.anahtarGirdi.text().strip())
                self.ayar["tailscaleAnahtariSakli"] = True
            except Exception:
                pass
        elif self.adim == 3:
            if not self.sync_ok and not self._mesgul:
                self.baslikYazi.setText("Dosya eşitleme")
                return
        elif self.adim == 4:
            if self.vpn_kurulu and self._anahtar_var() and not self.vpn_bagli:
                self.baslikYazi.setText("Gizli ağ")
                return
        elif self.adim == 5:
            if not (self.esles_ok or self.esles_atlandi):
                self.baslikYazi.setText("Arkadaşlar")
                return
        if self.adim == len(ADIMLAR) - 1:
            self._bitir()
            return
        self.adim += 1
        self.ciz()

    def _geri(self):
        if self.adim > 0:
            self.adim -= 1
            self.ciz()

    def _bitir(self):
        ad = (self.ayar.get("kullaniciAdi") or "").strip()
        if not ad:
            self.adim = 1
            self.ciz()
            return
        ilk = not self.ayar.get("kurulumTamam")
        self.ayar["kurulumTamam"] = True
        self.ayar["kullaniciAdi"] = ad
        try:
            from core import store as _S
            _S.kaydet(self.ayar)
            if ilk:
                from core import version as _V
                self.ayar["uygulananSurum"] = _V.oku().get("surum", "")
                _S.kaydet(self.ayar)
        except Exception:
            pass
        self._bitis = True
        self.tamamlandi.emit()


def time_sleep(saniye):
    import time
    time.sleep(saniye)
