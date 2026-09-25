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
    guncelleme_notu = Signal(str)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self.guncellemeNot = QLabel("")
        self._arayuz_kur()
        self.durum_mesaji.connect(self._mesaj)
        self.vpn_durumu.connect(self._vpn_goster)
        self.guncelleme_notu.connect(self.guncellemeNot.setText)
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
        self._profil_karti()
        self._yz_karti()
        self._baglanti_karti()
        self._guncelleme_karti()
        self._uygulama_karti()
        self._sahip_karti()
        for i in range(2):
            self.izgara.setColumnStretch(i, 1)
        self.izgara.setRowStretch(3, 1)

    # ---------- kartlar ----------
    def _profil_karti(self):
        kart = Kart("Profil")
        self.adGirdi = self._giris(self.h.kullanici)
        kart.satir("Kullanıcı adı", self.adGirdi,
                   "Arkadaşların bu ismiyle sunucuya bağlanır")
        kaydet = self._dugme("Kaydet", self._profil_kaydet, birincil=True)
        kart.govde.addWidget(kaydet, 0, Qt.AlignLeft)
        self.izgara.addWidget(kart, 0, 0)

    def _yz_karti(self):
        kart = Kart("Yapay zeka")
        self.aiGirdi = self._giris()
        self.aiGirdi.setEchoMode(QLineEdit.Password)
        kart.satir("OpenAI anahtarı", self.aiGirdi,
                   "Site yapay zekâ asistanı için; isteğe bağlı")
        satir = QHBoxLayout()
        goster = self._dugme("Göster", self._ai_goster)
        temizle = self._dugme("Temizle", self._ai_temizle)
        satir.addWidget(goster)
        satir.addWidget(temizle)
        satir.addStretch(1)
        kart.govde.addLayout(satir)
        self.izgara.addWidget(kart, 0, 1)

    def _baglanti_karti(self):
        kart = Kart("Bağlantı")
        self.vpnSatir = QLabel("-")
        self.vpnSatir.setObjectName("metin")
        kart.satir("VPN (Tailscale)", self.vpnSatir, "Arkadaşların bağlanabilmesi için")
        satir = QHBoxLayout()
        satir.addWidget(self._dugme("VPN Bağlan", self._vpn_baglan, birincil=True))
        satir.addWidget(self._dugme("Kurulum Sihirbazı", self._sihirbaz_ac))
        satir.addStretch(1)
        kart.govde.addLayout(satir)
        self.izgara.addWidget(kart, 1, 0)

    def _guncelleme_karti(self):
        kart = Kart("Güncelleme")
        try:
            from core import version as _V
            v = _V.oku()
            metin = str(v.get("surum") or "?")
            if v.get("guncelleniyor"):
                metin += " (güncelleme bekliyor)"
        except Exception:
            metin = "-"
        self.guncellemeSatir = QLabel(metin)
        self.guncellemeSatir.setObjectName("metin")
        kart.satir("Sunucu sürümü", self.guncellemeSatir, None)
        satir = QHBoxLayout()
        satir.addWidget(self._dugme("Güncellemeleri Denetle", self._guncelleme_denetle,
                                    birincil=True))
        satir.addStretch(1)
        kart.govde.addLayout(satir)
        self.guncellemeNot = QLabel("")
        self.guncellemeNot.setObjectName("minik")
        self.guncellemeNot.setWordWrap(True)
        kart.govde.addWidget(self.guncellemeNot)
        self.izgara.addWidget(kart, 1, 1)

    def _uygulama_karti(self):
        kart = Kart("Uygulama")
        self.heapKaydirici = Y.BellekKaydirici(
            ["%dG" % gb for gb in (2, 3, 4, 6)],
            (2, 3, 4, 6).index(self.h.heap_al())
            if self.h.heap_al() in (2, 3, 4, 6) else 1)
        self.heapKaydirici.deger_degisti.connect(self._heap_degisti)
        kart.govde.addWidget(self.heapKaydirici)
        not_ = QLabel("Sunucu belleği — sonraki başlatmada geçerli")
        not_.setObjectName("minik")
        kart.govde.addWidget(not_)
        satir = QHBoxLayout()
        satir.addWidget(self._dugme("Klasörü Aç", self._klasor_ac))
        satir.addWidget(self._dugme("Kaldır", self._kaldir))
        satir.addStretch(1)
        kart.govde.addLayout(satir)
        self.izgara.addWidget(kart, 2, 0)

    def _sahip_karti(self):
        try:
            from core import store as _S
            sahip = _S.sahip_mi(self.h.kok)
        except Exception:
            sahip = False
        if not sahip:
            return
        kart = Kart("Sahip")
        kart.rozet.setText("bu makinede yayınlayabilirsin")
        kart.rozet.setStyleSheet("color: %s; font-size: 11px;" % T.VURGU)
        satir = QHBoxLayout()
        satir.addWidget(self._dugme("Güncelleme Yayınla", self._yayinla,
                                    birincil=True))
        satir.addWidget(self._dugme("Bitir ve arkadaşlara aç", self._bitir))
        satir.addStretch(1)
        kart.govde.addLayout(satir)
        self.izgara.addWidget(kart, 2, 1)

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

    def _ai_goster(self):
        try:
            from core import store as _S
            anahtar = _S.ai_anahtar_oku() or ""
        except Exception:
            anahtar = ""
        self.aiGirdi.setText(anahtar)
        self.aiGirdi.setEchoMode(QLineEdit.Normal if anahtar else QLineEdit.Password)
        self._mesaj("Anahtar kayıtlı." if anahtar else "Kayıtlı anahtar yok.")

    def _ai_temizle(self):
        try:
            from core import store as _S
            _S.ai_anahtar_kaydet("")
        except Exception as e:
            self._mesaj("Silinemedi: %s" % e)
            return
        self.aiGirdi.clear()
        self.aiGirdi.setEchoMode(QLineEdit.Password)
        self._mesaj("Anahtar silindi.")

    def _vpn_baglan(self):
        def is_thread():
            try:
                from core import store as _S, vpn as _V
                anahtar = _S.anahtar_oku() or _S.kurulum_anahtari_oto_bul(self.h.kok)
                if not anahtar:
                    self.durum_mesaji.emit(
                        "Kurulum anahtarı yok (kurulum-anahtari.txt).")
                    return
                self.durum_mesaji.emit("VPN bağlanıyor...")
                ok, mesaj = _V.baglan(anahtar, self.h.kullanici)
                self.durum_mesaji.emit(mesaj or ("Bağlandı." if ok else "Bağlanamadı."))
            except Exception as e:
                self.durum_mesaji.emit("VPN hatası: %s" % e)
            self._vpn_durum()

        threading.Thread(target=is_thread, daemon=True).start()

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

    def _guncelleme_denetle(self):
        self.guncellemeNot.setText("Denetleniyor...")

        def is_thread():
            try:
                from core import guncelleme as _G
                sonuc = _G.denetle(self.h.ayar)
            except Exception as e:
                self.guncelleme_notu.emit("Denetleme hatası: %s" % e)
                return
            if sonuc.get("guncelleme_var"):
                yeni = (sonuc.get("yeni") or {}).get("surum", "?")
                self.guncelleme_notu.emit("Yeni sürüm bulundu: %s — kurulum için "
                                          "sunucuyu kapatıp güncellemeyi uygula." % yeni)
            else:
                self.guncelleme_notu.emit("Güncelleme yok, en son sürümdesin.")

        threading.Thread(target=is_thread, daemon=True).start()

    def _heap_degisti(self, deger):
        gb = (2, 3, 4, 6)[max(0, min(3, int(deger)))]
        self.h.heap_kaydet(gb)
        self._mesaj("Bellek %dG olarak kaydedildi (sonraki başlatmada geçerli)." % gb)

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

    def _yayinla(self):
        try:
            from core import store as _S, version as _V, kilit as _K
            if not _S.sahip_mi(self.h.kok):
                self._mesaj("Yetki yok: güncelleme yalnızca sahip makineden yayınlanır.")
                return
            if self.h.host_mu():
                self._mesaj("Önce sunucuyu Güvenli Kapat ile kapat.")
                return
            dolu, k = _K.kilit_dolu_mu(self.h.kok)
            if dolu:
                self._mesaj("%s sunucuyu açık tutuyor." % (k or {}).get("hostAdi", "Bir arkadaş"))
                return
            mevcut = _V.oku().get("surum", "")
            yeni, tamam = self._surum_sor(mevcut)
            if not tamam:
                return
            _V.yayinla(yeni, "")
            self._mesaj("Sürüm %s yayınlandı. Bitir'e basınca arkadaşlar "
                        "güncelleyebilir." % yeni)
            self._yenile()
        except Exception as e:
            self._mesaj("Yayınlanamadı: %s" % e)

    def _surum_sor(self, mevcut):
        from PySide6.QtWidgets import QInputDialog
        import time
        oneri = mevcut or time.strftime("%Y.%m.%d-1")
        yeni, tamam = QInputDialog.getText(self, "Yeni sürüm", "Sürüm damgası:",
                                           text=oneri)
        if not tamam:
            return "", False
        yeni = (yeni or "").strip()
        return yeni, bool(yeni)

    def _bitir(self):
        try:
            from core import store as _S, version as _V
            if not _S.sahip_mi(self.h.kok):
                self._mesaj("Yetki yok.")
                return
            if not _V.guncelleniyor_mu():
                self._mesaj("Yayınlanmış bir güncelleme yok.")
                return
            surum = _V.bitir_guncelleme()
            self.h.ayar["uygulananSurum"] = surum
            _S.kaydet(self.h.ayar)
            self._mesaj("Sürüm %s bitirildi; arkadaşlar güncelleyebilir." % surum)
            self._yenile()
        except Exception as e:
            self._mesaj("Bitirilemedi: %s" % e)

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
            self.vpn_durumu.emit(metin)

        threading.Thread(target=is_thread, daemon=True).start()

    def _vpn_goster(self, metin):
        self.vpnSatir.setText(metin)
