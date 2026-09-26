"""F2 — Konsol: canlı sunucu çıktısı + komut satırı.
Çıktı sunucu kuyruğundan (log_kuyrugu) okunur; komutlar stdin/RCON üzerinden gider.
Tehlikeli komutlar (constants.TEHLIKELI_KOMUTLAR) onay ister."""
import html
import queue
import threading

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
                               QPushButton, QVBoxLayout, QWidget)

from .. import tema as T
from .. import yardimci as Y

BASLIK = "Konsol"

RENK_NORMAL = "#B9C5C0"
RENK_UYARI = "#F5C86B"
RENK_HATA = "#F08C8C"
RENK_KOMUT = "#F0A202"
RENK_CEVAP = "#93C5FD"
AZAMI_SATIR = 3000

UST_ETIKET = "SUNUCU ARAYACI"
SAYFA_BASLIK = "Komut satırı."
SAYFA_ACIKLAMA = "Cihazın üzerinden komutlar doğrudan buradan gönder."


class KonsolSayfasi(QWidget):
    cikti_hazir = Signal(str, str)
    tamamlandi = Signal()

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._gecmis = []
        self._gecmis_yeri = 0
        self._kuyruk = hizmetler.log_kuyrugu
        self._bekleyen = []
        self._gizli = True
        self._arayuz_kur()
        self.cikti_hazir.connect(self.yaz)
        self.tamamlandi.connect(self._gonder_bitti)
        self._zamanlayici = QTimer(self)
        self._zamanlayici.timeout.connect(self._kuyrugu_bosalt)
        self._zamanlayici.start(250)

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
                                              "DGMCRAFT / KONSOL")
        dis.addWidget(self.baslikAlani)
        icKutu = QWidget()
        dis.addWidget(icKutu, 1)
        ic = QVBoxLayout(icKutu)
        ic.setContentsMargins(T.IC_PAY, 0, T.IC_PAY, 0)
        ic.setSpacing(T.KART_ARALIK)

        kart = QFrame()
        kart.setObjectName("siyahKart")
        govde = QVBoxLayout(kart)
        govde.setContentsMargins(0, 0, 0, 0)
        govde.setSpacing(0)

        # üst şerit: SUNUCU ÇIKTISI + bağlantı durumu
        ustSerit = QWidget()
        ustSatir = QHBoxLayout(ustSerit)
        ustSatir.setContentsMargins(20, 14, 20, 12)
        ustSatir.setSpacing(10)
        ustSatir.addWidget(T.etiket("SUNUCU ÇIKTISI", "bolumBaslik"))
        ustSatir.addStretch(1)
        self.baglantiNokta = QFrame()
        self.baglantiNokta.setFixedSize(7, 7)
        self.baglantiNokta.setStyleSheet(
            "background: %s; border-radius: 3px; border: none;" % T.KIRMIZI)
        ustSatir.addWidget(self.baglantiNokta)
        ustSatir.addSpacing(4)
        self.baglantiYazi = T.etiket("BAĞLI DEĞİL", "soluk")
        ustSatir.addWidget(self.baglantiYazi)
        govde.addWidget(ustSerit)
        govde.addWidget(T.ayirici(T.BOLUCU_ACIK))

        self.cikti = QPlainTextEdit(kart)
        self.cikti.setReadOnly(True)
        self.cikti.setUndoRedoEnabled(False)
        self.cikti.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.cikti.setMaximumBlockCount(AZAMI_SATIR)
        self.cikti.setStyleSheet(
            "QPlainTextEdit { background: transparent; border: none;"
            " padding: 14px 20px; color: %s;"
            " font-family: 'Consolas'; font-size: 12px; }" % RENK_NORMAL)
        self.cikti.setFont(QFont("Consolas", 10))
        govde.addWidget(self.cikti, 1)

        ayrac = QFrame(kart)
        ayrac.setObjectName("ayrac")
        ayrac.setFixedHeight(1)
        ayrac.setStyleSheet("background: %s; border: none;" % T.BOLUCU_ACIK)
        govde.addWidget(ayrac)

        satir = QHBoxLayout()
        satir.setContentsMargins(20, 14, 20, 16)
        satir.setSpacing(10)
        self.girdi = QLineEdit()
        self.girdi.setPlaceholderText("Komut yaz — örn: say Merhaba, tp Xpike 10 64 -20 120")
        self.girdi.setStyleSheet(
            "QLineEdit { background: #10161A; border: 1px solid %s; border-radius: 4px;"
            " padding: 11px 12px; color: %s; font-size: 12px; }"
            "QLineEdit:focus { border: 2px solid %s; }" % (T.CERCEVE, T.YAZI, T.VURGU))
        self.girdi.returnPressed.connect(self.gonder)
        satir.addWidget(self.girdi, 1)
        self.gonderDugmesi = T.dugme("Gönder", "ana")
        self.gonderDugmesi.setCursor(Qt.PointingHandCursor)
        self.gonderDugmesi.clicked.connect(self.gonder)
        satir.addWidget(self.gonderDugmesi)
        self.temizDugmesi = T.dugme("Temizle", "kontrast")
        self.temizDugmesi.clicked.connect(self.temizle)
        satir.addWidget(self.temizDugmesi)
        govde.addLayout(satir)
        ic.addWidget(kart, 1)

        ipucu = QLabel("Yukarı ok geçmişteki komutları gezinir · tehlikeli komutlar onay ister")
        ipucu.setObjectName("minik")
        ic.addWidget(ipucu)
        dis.addSpacing(2)
        self.girdi.installEventFilter(self)

    # ---------- giriş geçmişi ----------
    def eventFilter(self, nesne, olay):
        try:
            from PySide6.QtCore import QEvent
            from PySide6.QtGui import QKeyEvent
            if nesne is self.girdi and olay.type() == QEvent.KeyPress:
                tus = QKeyEvent(olay).key()
                if tus == Qt.Key_Up:
                    self._gecmis_yeri = max(0, self._gecmis_yeri - 1)
                    self._gecmiziyi_goster()
                    return True
                if tus == Qt.Key_Down:
                    self._gecmis_yeri = min(len(self._gecmis), self._gecmis_yeri + 1)
                    self._gecmiziyi_goster()
                    return True
        except Exception:
            pass
        return super().eventFilter(nesne, olay)

    def _gecmiziyi_goster(self):
        try:
            if 0 <= self._gecmis_yeri < len(self._gecmis):
                self.girdi.setText(self._gecmis[self._gecmis_yeri])
            else:
                self.girdi.clear()
        except Exception:
            pass

    # ---------- çıktı ----------
    def yaz(self, metin, renk=RENK_NORMAL):
        try:
            temiz = str(metin).replace("\r", "").rstrip("\n")
            for parca in temiz.split("\n"):
                self.cikti.appendHtml(
                    '<span style="color:%s">%s</span>'
                    % (renk, html.escape(parca)))
        except Exception:
            pass

    def temizle(self):
        try:
            self.cikti.clear()
            self.yaz("Konsol temizlendi.", RENK_NORMAL)
        except Exception:
            pass

    def _kuyrugu_bosalt(self):
        """Sunucu kuyruğundan gelen satırları alır.
        Sayfa gizliyse ekrana yazmaz, tampona alır (kayıt kaybolmaz).
        Görünürken sefer başına sınırlı sayıda satır basar; arayüz donmaz."""
        try:
            islem = 0
            while islem < 200:
                try:
                    satir = self._kuyruk.get_nowait()
                except queue.Empty:
                    break
                islem += 1
                if self._gizli:
                    self._bekleyen.append(satir)
                    if len(self._bekleyen) > AZAMI_SATIR:
                        del self._bekleyen[:-AZAMI_SATIR]
                    continue
                for parca in str(satir).replace("\r", "").split("\n"):
                    if parca.strip():
                        self.yaz(parca, self._renk_bul(parca))
                if islem >= 200:
                    QTimer.singleShot(30, self._kuyrugu_bosalt)
        except Exception:
            pass

    @staticmethod
    def _renk_bul(satir):
        ust = satir.upper()
        if "ERROR" in ust or "EXCEPTION" in ust or "FATAL" in ust:
            return RENK_HATA
        if "WARN" in ust:
            return RENK_UYARI
        if satir.startswith(">"):
            return RENK_KOMUT
        if "RCON" in ust:
            return RENK_CEVAP
        return RENK_NORMAL

    # ---------- komut gönderme ----------
    def gonder(self):
        komut = self.girdi.text().strip()
        if not komut:
            return
        try:
            from core import constants as C
            tehlikeli = C.TEHLIKELI_KOMUTLAR
        except Exception:
            tehlikeli = ("stop", "op", "deop", "reload")
        ilk = komut.lstrip("/").split(" ")[0].lower()
        if ilk in tehlikeli:
            onay = Y.onay_sor(
                self, "Tehlikeli komut",
                "'%s' sunucuyu doğrudan etkiler. Emin misin?" % komut,
                tamam="Evet, çalıştır")
            if not onay:
                self.yaz("İptal edildi: %s" % komut, RENK_UYARI)
                return
        if komut not in self._gecmis:
            self._gecmis.append(komut)
            self._gecmis = self._gecmis[-50:]
        self._gecmis_yeri = len(self._gecmis)
        self.yaz("> " + komut, RENK_KOMUT)
        self.girdi.clear()
        self.gonderDugmesi.setEnabled(False)
        threading.Thread(target=self._gonder_is, args=(komut,), daemon=True).start()

    def _gonder_is(self, komut):
        ok, cevap = False, ""
        try:
            ok, cevap = self.h.sunucu_al().komut_gonder(komut)
        except Exception as e:
            ok, cevap = False, str(e)
        Y.guvenli_yayin(self.cikti_hazir, 
            cevap or ("Gönderildi." if ok else "Gönderilemedi."), RENK_CEVAP)
        Y.guvenli_yayin(self.tamamlandi)

    def _gonder_bitti(self):
        try:
            self.gonderDugmesi.setEnabled(True)
        except Exception:
            pass

    # ---------- yaşam döngüsü ----------
    def goster(self):
        self._gizli = False
        self._kuyrugu_bosalt()
        if self._bekleyen:
            for satir in self._bekleyen[-200:]:
                for parca in str(satir).replace("\r", "").split("\n"):
                    if parca.strip():
                        self.yaz(parca, self._renk_bul(parca))
            self._bekleyen = []
        if self.cikti.blockCount() <= 1:
            self.yaz("Sunucu çıktısı burada akar. Komut yazıp Gönder'e basabilirsin.",
                     RENK_NORMAL)
        self._zamanlayici.start(250)
        self.girdi.setFocus()

    def gizle(self):
        self._gizli = True