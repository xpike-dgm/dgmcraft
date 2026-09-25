"""F8 — Ayarlar: Profil, Yapay zeka, Bağlantı, Güncelleme, Uygulama, Sahip.
v1'deki kartların PySide6 karşılığı; aynı core servislerini kullanır."""
import os
import subprocess
import sys
import threading

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Ayarlar"


class Kart(QFrame):
    """Başlıklı ayar kartı."""

    def __init__(self, baslik, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("kart")
        govde = QVBoxLayout(self)
        govde.setContentsMargins(16, 14, 16, 16)
        govde.setSpacing(8)
        b = QLabel(baslik.upper())
        b.setObjectName("bolumBaslik")
        govde.addWidget(b)
        self.govde = govde
        self.rozet = QLabel("")
        self.rozet.setStyleSheet("color: %s; font-size: 11px;" % T.SILIK)
        govde.addWidget(self.rozet)

    def satir(self, etiket, denetim=None, aciklama=None):
        s = QHBoxLayout()
        s.setContentsMargins(0, 0, 0, 0)
        sol = QVBoxLayout()
        sol.setSpacing(1)
        a = QLabel(etiket)
        a.setObjectName("metin")
        sol.addWidget(a)
        if aciklama:
            d = QLabel(aciklama)
            d.setObjectName("minik")
            d.setWordWrap(True)
            sol.addWidget(d)
        s.addLayout(sol, 1)
        if denetim is not None:
            s.addWidget(denetim, 0, Qt.AlignVCenter)
        self.govde.addLayout(s)
        return s


class AyarlarSayfasi(QWidget):
    durum_mesaji = Signal(str)
    vpn_durumu = Signal(str)
    vpn_bitti = Signal(bool)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._arayuz_kur()
        self.durum_mesaji.connect(self._mesaj)
        self.vpn_durumu.connect(self._vpn_goster)
        self.vpn_bitti.connect(self.vpn_bitti_uygula)
        self._yenile()

    # ---------- kurulum ----------
    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(T.KART_ARALIK)
        self.kaydirma = QScrollArea()
        self.kaydirma.setWidgetResizable(True)
        self.kaydirma.setFrameShape(QFrame.NoFrame)
        ic = QWidget()
        self.izgara = QGridLayout(ic)
        self.izgara.setContentsMargins(0, 0, 0, 0)
        self.izgara.setSpacing(T.KART_ARALIK)
        self.kaydirma.setWidget(ic)
        dis.addWidget(self.kaydirma, 1)
        self.mesaj = QLabel("")
        self.mesaj.setObjectName("kucuk")
        dis.addWidget(self.mesaj)

    def _dugme(self, metin, islev, birincil=False):
        b = QPushButton(metin)
        b.setObjectName("anaDugme" if birincil else "hayaletDugme")
        b.setCursor(Qt.PointingHandCursor)
        b.clicked.connect(islev)
        return b

    def _giris(self, metin=""):
        e = QLineEdit(metin)
        e.setFixedWidth(190)
        e.setStyleSheet(
            "QLineEdit { background: #0F1513; border: 1px solid %s; border-radius: 9px;"
            " padding: 8px 10px; color: %s; font-size: 13px; }"
            "QLineEdit:focus { border-color: %s; }" % (T.CERCEVE, T.YAZI, T.VURGU))
        return e

    def _yenile(self):
        Y.yerlesim_temizle(self.izgara)
        self._profil_karti()      # 0,0
        self._baglanti_karti()    # 0,1
        self._uygulama_karti()    # 1,0
        self._bilgi_karti()       # 1,1
        for i in range(2):
            self.izgara.setColumnStretch(i, 1)
        self.izgara.setRowStretch(2, 1)

    # ---------- kartlar ----------
    def _profil_karti(self):
        kart = Kart("Profil")
        self.adGirdi = self._giris(self.h.kullanici)
        kart.satir("Kullanıcı adı", self.adGirdi,
                   "Arkadaşların bu ismiyle sunucuya bağlanır")
        kaydet = self._dugme("Kaydet", self._profil_kaydet, birincil=True)
        kart.govde.addWidget(kaydet, 0, Qt.AlignLeft)
        self.izgara.addWidget(kart, 0, 0)

    def _baglanti_karti(self):
        kart = Kart("Bağlantı")
        self.vpnSatir = QLabel("Bağlanmadı")
        self.vpnSatir.setObjectName("metin")
        kart.satir("Arkadaş bağlantısı (Tailscale)", self.vpnSatir,
                   "Arkadaşların sunucuya bu bağlantı üzerinden ulaşır")
        satir = QHBoxLayout()
        self.vpnDugmesi = self._dugme("Bağlan", self._vpn_baglan, birincil=True)
        satir.addWidget(self.vpnDugmesi)
        satir.addWidget(self._dugme("Kurulum Sihirbazı", self._sihirbaz_ac))
        satir.addStretch(1)
        kart.govde.addLayout(satir)
        self.izgara.addWidget(kart, 0, 1)

    def _uygulama_karti(self):
        kart = Kart("Uygulama")
        satir = QHBoxLayout()
        satir.addWidget(self._dugme("Sunucu Klasörünü Aç", self._klasor_ac))
        satir.addWidget(self._dugme("Uygulamayı Kaldır", self._kaldir))
        satir.addStretch(1)
        kart.govde.addLayout(satir)
        not_ = QLabel("Sunucu belleği Hub sayfasından ayarlanır.")
        not_.setObjectName("minik")
        kart.govde.addWidget(not_)
        self.izgara.addWidget(kart, 1, 0)

    def _bilgi_karti(self):
        kart = Kart("Güncelleme")
        try:
            from core import version as _V
            v = _V.oku()
            metin = str(v.get("surum") or "?")
            if v.get("guncelleniyor"):
                metin += " — güncelleme bekliyor"
        except Exception:
            metin = "bilinmiyor"
        durum = QLabel(metin)
        durum.setObjectName("metin")
        kart.satir("Sunucu sürümü", durum, "Uygulama açılışında güncelleme kendiliğinden denetlenir")
        kart.rozet.setText("güncelleme yoksa ekran açılır")
        self.izgara.addWidget(kart, 1, 1)

    # ---------- eylemler ----------
    def _mesaj(self, metin):
        self.mesaj.setText(metin or "")

    def _profil_kaydet(self):
        ad = self.adGirdi.text().strip()
        if not ad:
            return
        self.h.kullanici = ad
        self.h.ayar["kullaniciAdi"] = ad
        try:
            from core import store as _S
            _S.kaydet(self.h.ayar)
        except Exception as e:
            self._mesaj("Kaydedilemedi: %s" % e)
            return
        self._mesaj("Kullanıcı adı kaydedildi: %s" % ad)

    def _vpn_baglan(self):
        """Tailscale kuruluysa otomatik açar ve bağlanır; kurulu değilse
        kullanıcıya sorup indirip kurar. İlerleme ve sonuç bildirim kutusunda."""
        try:
            self.vpnDugmesi.setEnabled(False)
        except Exception:
            pass

        def ilerleme(metin):
            Y.guvenli_yayin(self.durum_mesaji, metin)

        def izin():
            evet = Y.onay_sor(
                self, "Tailscale kurulu değil",
                "Arkadaşların bağlanabilmesi için Tailscale gerekiyor. "
                "Şimdi indirip kursam mı?",
                tamam="Evet, indir ve kur", iptal="Şimdi değil")
            Y.guvenli_yayin(self.durum_mesaji,
                            "Tailscale indiriliyor..." if evet
                            else "Kurulum iptal edildi.")
            return evet

        def is_thread():
            try:
                from core import store as _S, vpn as _V
                anahtar = _S.anahtar_oku() or _S.kurulum_anahtari_oto_bul(self.h.kok)
                if not anahtar:
                    Y.guvenli_yayin(
                        self.durum_mesaji,
                        "Bağlantı anahtarı yok. Genel yöneticinden iste.")
                    return
                ok, mesaj, _teknik = _V.baglan_veya_kur(
                    anahtar, self.h.kullanici, ilerleme=ilerleme, izin=izin)
            except Exception as e:
                ok, mesaj = False, "Bağlantı kurulamadı: %s" % e
            Y.guvenli_yayin(self.durum_mesaji, mesaj)
            Y.guvenli_yayin(self.vpn_bitti, bool(ok))

        threading.Thread(target=is_thread, daemon=True).start()

    def vpn_bitti_uygula(self, basarili):
        try:
            self.vpnDugmesi.setEnabled(True)
        except Exception:
            pass
        self._vpn_durum()

    def _sihirbaz_ac(self):
        try:
            kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            betik = os.path.join(kok, "wizard.py")
            if not os.path.isfile(betik):
                self._mesaj("Sihirbaz dosyası bulunamadı.")
                return
            if sys.executable.lower().endswith("pythonw.exe"):
                exe = sys.executable
            else:
                exe = sys.executable
            subprocess.Popen([exe, betik], cwd=kok, creationflags=0x08000000)
            self._mesaj("Kurulum sihirbazı ayrı pencerede açıldı.")
        except Exception as e:
            self._mesaj("Sihirbaz açılamadı: %s" % e)

    def _klasor_ac(self):
        try:
            if sys.platform.startswith("win"):
                os.startfile(self.h.kok)
            else:
                subprocess.Popen(["xdg-open", self.h.kok])
            self._mesaj("Sunucu klasörü açıldı.")
        except Exception as e:
            self._mesaj("Klasör açılamadı: %s" % e)

    def _kaldir(self):
        if not Y.onay_sor(self, "Uygulamayı kaldır",
                          "Kurulum dosyaları silinsin mi? Sunucu klasörü "
                          "korunur.", tamam="Kaldır"):
            return
        try:
            from core import kurulum as _K
            self._mesaj(_K.kaldir_hazirla())
        except Exception as e:
            self._mesaj("Kaldırılamadı: %s" % e)

    # ---------- yaşam döngüsü ----------
    def goster(self):
        self._yenile()
        self._vpn_durum()

    def gizle(self):
        pass

    def _vpn_durum(self):
        def is_thread():
            try:
                from core import vpn as _V
                bagli, ip, _b = _V.bagli_mi()
                metin = ("bağlı · %s" % ip) if bagli and ip else "bağlı değil"
            except Exception as e:
                metin = "bilinmiyor (%s)" % e
            Y.guvenli_yayin(self.vpn_durumu, metin)

        threading.Thread(target=is_thread, daemon=True).start()

    def _vpn_goster(self, metin):
        self.vpnSatir.setText(metin)
