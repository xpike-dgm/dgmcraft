"""Açılışta otomatik güncelleme ekranı.

Kurallar:
- Güncelleme varsa uygulamanın içine girilmez; bu pencere kapanana kadar engellenir.
- "Şimdi değil" yoktur: sürüm güncel değilse uygulama kullanılamaz.
- Parola bu ekranda değildir; parola Ayarlar > Güncelleme > Yayınla içindedir.
"""
import os
import subprocess
import sys
import threading

from PySide6.QtCore import QPoint, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QProgressBar,
                               QPushButton, QTextBrowser, QVBoxLayout, QWidget)

from . import tema as T
from . import yardimci as Y

GENISLIK = 620
YUKSEKLIK = 540


class GuncellemePenceresi(QWidget):
    """Çerçevesiz, kapatılamayan güncelleme penceresi."""

    durum_mesaji = Signal(str)
    ilerleme_yuzde = Signal(int)
    kurulum_bitti = Signal(bool)

    def __init__(self, hizmetler, sonuc, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self.sonuc = sonuc or {}
        self._surukle = None
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(GENISLIK + 24, YUKSEKLIK + 24)
        self._arayuz_kur()
        self.durum_mesaji.connect(self._durum)
        self.ilerleme_yuzde.connect(self._ilerleme)
        self.kurulum_bitti.connect(self._bitti)

    # ---------- görünüm ----------
    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(12, 12, 12, 12)
        kart = QFrame(self)
        kart.setObjectName("guncKart")
        Y.golge(kart, 40, 170, 0)
        dis.addWidget(kart)

        ic = QVBoxLayout(kart)
        ic.setContentsMargins(34, 28, 34, 28)
        ic.setSpacing(0)

        # başlık: logo + uygulama adı
        ust = QHBoxLayout()
        ust.setContentsMargins(0, 0, 0, 0)
        ust.setSpacing(12)
        logo = QLabel()
        pm = Y.pixmap("brand", "mark-480.png")
        if pm is not None and not pm.isNull():
            logo.setPixmap(pm.scaled(30, 30, Qt.KeepAspectRatio,
                                     Qt.SmoothTransformation))
        ust.addWidget(logo)
        ad = QLabel("DgmCraft")
        ad.setObjectName("markaAd")
        ust.addWidget(ad)
        ust.addStretch(1)
        rozet = QLabel("GÜNCELLEME")
        rozet.setObjectName("rozetUst")
        ust.addWidget(rozet)
        ust.addSpacing(10)
        self.kapatDugmesi = QPushButton("×")
        self.kapatDugmesi.setObjectName("kapatDugme")
        self.kapatDugmesi.setToolTip("Uygulamayı kapat")
        self.kapatDugmesi.setFixedSize(30, 30)
        self.kapatDugmesi.setCursor(Qt.PointingHandCursor)
        self.kapatDugmesi.clicked.connect(self._kapat)
        ust.addWidget(self.kapatDugmesi)
        ic.addLayout(ust)
        ic.addSpacing(26)

        baslik = QLabel("Yeni sürüm hazır")
        baslik.setObjectName("guncBaslik")
        ic.addWidget(baslik)
        ic.addSpacing(6)

        surum = QLabel()
        surum.setObjectName("guncSurum")
        mevcut = self.sonuc.get("mevcut") or "—"
        yeni = self.sonuc.get("son") or "?"
        surum.setText('<span style="color:#6E7F76">%s</span>  <span style="color:#F0A202">'
                      "→</span>  <span style=\"color:#F2F5F3\">%s</span>"
                      % (mevcut, yeni))
        ic.addWidget(surum)
        ic.addSpacing(22)

        notKutu = QFrame()
        notKutu.setObjectName("notKutu")
        notKutu.setMinimumHeight(150)
        notKutu.setMaximumHeight(230)
        notDikey = QVBoxLayout(notKutu)
        notDikey.setContentsMargins(0, 0, 0, 0)
        notlar = QTextBrowser()
        notlar.setObjectName("notMetin")
        notlar.setOpenExternalLinks(False)
        notlar.setHtml(_not_html(self.sonuc.get("notlar", "")))
        notDikey.addWidget(notlar)
        ic.addWidget(notKutu, 1)
        ic.addSpacing(18)

        self.cubuk = QProgressBar()
        self.cubuk.setObjectName("guncCubuk")
        self.cubuk.setRange(0, 100)
        self.cubuk.setValue(0)
        self.cubuk.setTextVisible(False)
        self.cubuk.setFixedHeight(6)
        self.cubuk.setVisible(False)
        ic.addWidget(self.cubuk)
        ic.addSpacing(8)

        self.durumYazi = QLabel("")
        self.durumYazi.setObjectName("guncDurum")
        self.durumYazi.setWordWrap(True)
        ic.addWidget(self.durumYazi)
        ic.addSpacing(16)

        self.dugme = QPushButton("Güncelle")
        self.dugme.setObjectName("anaDugme")
        self.dugme.setCursor(Qt.PointingHandCursor)
        self.dugme.setFixedHeight(46)
        self.dugme.setFocusPolicy(Qt.StrongFocus)
        self.dugme.clicked.connect(self._guncelle)
        ic.addWidget(self.dugme)
        ic.addSpacing(12)

        ipucu = QLabel("Güncellemeden uygulamaya girilemez. İstemiyorsan penceredeki "
                       "× ile kapatabilirsin.")
        ipucu.setObjectName("minik")
        ipucu.setAlignment(Qt.AlignCenter)
        ipucu.setWordWrap(True)
        ic.addWidget(ipucu)

    # ---------- sürükleme / kapatma engeli ----------
    def mousePressEvent(self, olay):
        if olay.button() == Qt.LeftButton:
            self._surukle = (olay.globalPosition().toPoint(),
                             self.frameGeometry().topLeft())

    def mouseMoveEvent(self, olay):
        if self._surukle and (olay.buttons() & Qt.LeftButton):
            fark = olay.globalPosition().toPoint() - self._surukle[0]
            self.move(self._surukle[1] + fark)

    def mouseReleaseEvent(self, olay):
        self._surukle = None

    def closeEvent(self, olay):
        """Güncelleme bitene kadar uygulamaya girilemez; ama kullanıcı
        istemezse uygulamayı kapatabilir."""
        olay.accept()
        QTimer.singleShot(0, QGuiApplication.quit)

    def _kapat(self):
        QTimer.singleShot(0, QGuiApplication.quit)

    def kapatilabilir_mi(self):
        return self._bitti_mi

    _bitti_mi = False

    def _bitti(self, tamam):
        self._bitti_mi = True
        if tamam:
            try:
                _yeniden_baslat()
            except Exception:
                pass
            QTimer.singleShot(250, QGuiApplication.quit)
        else:
            self.close_ok = True
            self.hide()

    # ---------- akış ----------
    def _durum(self, metin):
        self.durumYazi.setText(metin or "")

    def _ilerleme(self, yuzde):
        self.cubuk.setValue(max(0, min(100, int(yuzde))))

    def _guncelle(self):
        self.dugme.setEnabled(False)
        self.dugme.setText("Güncelleniyor...")
        self.cubuk.setVisible(True)
        self._ilerleme(2)
        threading.Thread(target=self._is, daemon=True).start()

    def _is(self):
        try:
            from core import guncelleme as _G
            sonuc = dict(self.sonuc)
            sonuc["zip_url"] = sonuc.get("zip_url") or _dogrudan_paket_url(sonuc)
            _G.uygula(self.h.kok, sonuc, durum_yaz=self._durum_gunvenli,
                      ilerleme=self._ilerleme)
        except Exception as e:
            Y.guvenli_yayin(self.durum_mesaji, _hata_mesaji(e))
            try:
                self.dugme.setEnabled(True)
                self.dugme.setText("Tekrar Dene")
                self.cubuk.setVisible(False)
            except Exception:
                pass
            return
        Y.guvenli_yayin(self.durum_mesaji, "Tamam. Uygulama yeniden başlatılıyor...")
        Y.guvenli_yayin(self.kurulum_bitti, True)

    def _durum_gunvenli(self, metin):
        Y.guvenli_yayin(self.durum_mesaji, metin)


def _hata_mesaji(hata):
    """Teknik hataları günlük diliyle anlatır."""
    s = str(hata or "")
    dusuk = s.lower()
    if "404" in dusuk or "not found" in dusuk:
        return ("Güncelleme dosyası bulunamadı. Bu sürüm henüz yayınlanmamış "
                "olabilir; biraz sonra tekrar dene.")
    if "urlopen error" in dusuk or "connection" in dusuk or "timeout" in dusuk \
            or "zaman aşımı" in dusuk or "ssl" in dusuk:
        return "İnternet bağlantısı yok. Bağlandıktan sonra tekrar dene."
    if "zip" in dusuk or "zipfile" in dusuk or "paket doğrulanamadı" in dusuk:
        return "Güncelleme dosyası bozuk geldi. Tekrar indirmeyi dene."
    if "izin" in dusuk or "access is denied" in dusuk or "permission" in dusuk:
        return ("Dosyalara yazma izni yok. Uygulamayı yönetici olarak "
                "çalıştırmayı dene.")
    if "kilit" in dusuk or "lock" in dusuk:
        return "Uygulama dosyaları kullanımda. Uygulamayı kapatıp tekrar dene."
    return "Güncelleme kurulamadı: %s" % s[:160]


def _dogrudan_paket_url(sonuc):
    """Release'ta zip yoksa tag'dan zipball üret."""
    from urllib.parse import quote
    tag = (sonuc.get("son") or "").strip()
    repo = sonuc.get("repo") or "xpike-dgm/dgmcraft"
    if not tag:
        return ""
    return "https://github.com/%s/archive/refs/tags/%s.zip" % (repo, quote(tag))


def _not_html(metin):
    import html
    satirlar = [s.rstrip() for s in (metin or "").splitlines()]
    temiz = []
    for s in satirlar:
        t = s.strip()
        if not t or "Full Changelog" in t or t.startswith("**"):
            continue
        if t.startswith("#"):
            continue
        t = t.lstrip("-*• ").strip()
        if t:
            temiz.append(html.escape(t))
    if not temiz:
        return '<p style="color:#6E7F76">Bu sürüm için açıklama yok.</p>'
    return ('<ul style="margin:0; padding-left:18px; color:#B9C5C0;">%s</ul>'
            % "".join("<li style='margin:4px 0'>%s</li>" % t for t in temiz[:12]))


def _yeniden_baslat():
    if getattr(sys, "frozen", False):
        os.startfile(sys.executable)
        return
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    betik = os.path.join(kok, "qt.py")
    exe = sys.executable
    if os.path.basename(exe).lower() == "python.exe":
        aday = os.path.join(os.path.dirname(exe), "pythonw.exe")
        if os.path.isfile(aday):
            exe = aday
    subprocess.Popen([exe, betik], cwd=kok, creationflags=0x08000000)


# Eski ad korunur (kabuk bu adı kullanıyor).
GuncellemeEkrani = GuncellemePenceresi
