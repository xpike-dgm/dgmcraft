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
        self.setFixedSize(T.GENISLIK + T.GOLGE, T.YUKSEKLIK + T.GOLGE)
        self._arayuz_kur()
        self.durum_mesaji.connect(self._durum)
        self.ilerleme_yuzde.connect(self._ilerleme)
        self.kurulum_bitti.connect(self._bitti)

    # ---------- görünüm ----------
    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(0)
        dis.addWidget(self._ust_cubuk())

        icKutu = QFrame()
        icKutu.setObjectName("sayfa")
        icDikey = QVBoxLayout(icKutu)
        icDikey.setContentsMargins(0, 0, 0, 0)
        icDikey.setSpacing(0)
        icDikey.addWidget(self._govde_kur())
        dis.addWidget(icKutu, 1)

    def _ust_cubuk(self):
        cubuk = QFrame()
        cubuk.setObjectName("ustCubuk")
        cubuk.setFixedWidth(T.GENISLIK + 2)
        cubuk.setFixedHeight(T.UST_YUKSEKLIK)
        satir = QHBoxLayout(cubuk)
        satir.setContentsMargins(25, 0, 18, 3)
        satir.setSpacing(10)
        logo = QLabel()
        pm = T.mark_pixmap(43)
        if not pm.isNull():
            logo.setPixmap(pm)
        logo.setFixedSize(43, 43)
        logo.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(logo)
        satir.addSpacing(10)
        ad = QLabel("DGMCRAFT")
        ad.setObjectName("markaAd")
        ad.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(ad)
        satir.addSpacing(14)
        bolum = QLabel("GÜNCELLEME")
        bolum.setObjectName("markaAlt")
        bolum.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(bolum)
        satir.addStretch(1)
        hazir = QLabel("YENİ SÜRÜM HAZIR")
        hazir.setObjectName("yardimciEtiket")
        hazir.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        satir.addWidget(hazir)
        satir.addSpacing(16)
        self.kapatDugmesi = Y.BaslikDugmesi("kapat")
        self.kapatDugmesi.setToolTip("Uygulamayı kapat")
        self.kapatDugmesi.clicked.connect(self._kapat)
        satir.addWidget(self.kapatDugmesi)
        return cubuk

    def _govde_kur(self):
        govde = QWidget()
        satir = QHBoxLayout(govde)
        satir.setContentsMargins(T.IC_PAY, 20, T.IC_PAY, 20)
        satir.setSpacing(14)

        # --- sol: eski -> yeni turuncu kart + dugme ---
        sol = QVBoxLayout()
        sol.setContentsMargins(0, 0, 0, 0)
        sol.setSpacing(14)
        solUst = T.etiket("YENİ SÜRÜM", "bolumBaslik")
        sol.addWidget(solUst)
        baslik = T.etiket("DgmCraft yenilendi.", "sayfaBaslik")
        sol.addWidget(baslik)
        self.aciklama = T.etiket("Güncelleme tamamlandı. Yeni sürümle birlikte dünya "
                                 "görünümü ve komutlar yenilendi.", "sayfaAciklama")
        self.aciklama.setWordWrap(True)
        sol.addWidget(self.aciklama)
        sol.addSpacing(6)

        surumKart = T.kart("vurgu")
        surumKart.setFixedHeight(277)
        surumKart.setFixedWidth(560)
        surumGovde = QVBoxLayout(surumKart)
        surumGovde.setContentsMargins(26, 22, 26, 22)
        surumGovde.setSpacing(0)
        mevcut = self.sonuc.get("mevcut") or "—"
        yeni_s = self.sonuc.get("son") or "?"
        surumGovde.addWidget(T.etiket("ESKİ SÜRÜM", "vurguUst"))
        surumGovde.addSpacing(6)
        surumGovde.addWidget(T.etiket(mevcut, "vurguSurum"))
        surumGovde.addStretch(1)
        okSatir = QHBoxLayout()
        okSatir.setContentsMargins(0, 0, 0, 0)
        ok = QLabel("→")
        ok.setObjectName("vurguOk")
        okSatir.addWidget(ok)
        surumGovde.addLayout(okSatir)
        surumGovde.addStretch(1)
        surumGovde.addWidget(T.etiket("YENİ SÜRÜM", "vurguUst"))
        surumGovde.addSpacing(6)
        surumGovde.addWidget(T.etiket(yeni_s, "vurguSurum"))
        sol.addWidget(surumKart)
        sol.addSpacing(4)

        self.cubuk = QProgressBar()
        self.cubuk.setProperty("rol", "ince")
        self.cubuk.setRange(0, 100)
        self.cubuk.setValue(0)
        self.cubuk.setTextVisible(False)
        self.cubuk.setVisible(False)
        sol.addWidget(self.cubuk)
        sol.addSpacing(4)

        self.durumYazi = T.etiket("", "soluk")
        self.durumYazi.setWordWrap(True)
        sol.addWidget(self.durumYazi)
        sol.addSpacing(8)

        self.dugme = T.dugme("Güncellemeyi başlat", "kontrast")
        self.dugme.setFixedHeight(46)
        self.dugme.setFixedWidth(280)
        self.dugme.setFocusPolicy(Qt.StrongFocus)
        self.dugme.clicked.connect(self._guncelle)
        sol.addWidget(self.dugme)
        sol.addSpacing(6)

        ipucu = T.etiket("Güncellemeden uygulamaya girilemez. İstemiyorsan "
                         "penceredeki × ile kapatabilirsin.", "minik")
        ipucu.setWordWrap(True)
        sol.addWidget(ipucu)
        sol.addStretch(1)
        satir.addLayout(sol, 0)

        # --- sag: siyah surum notlari karti ---
        notKart = QFrame()
        notKart.setObjectName("siyahKart")
        notKart.setFixedWidth(617)
        notDikey = QVBoxLayout(notKart)
        notDikey.setContentsMargins(0, 0, 0, 0)
        notDikey.setSpacing(0)

        notUst = QWidget()
        notUstSatir = QHBoxLayout(notUst)
        notUstSatir.setContentsMargins(22, 20, 22, 16)
        notUstSatir.setSpacing(12)
        notUstSatir.addWidget(T.etiket("BU SÜRÜMDE", "bolumBaslik"))
        notUstSatir.addStretch(1)
        notGorsel = QLabel()
        notGorsel.setPixmap(T.mark_pixmap(56))
        notGorsel.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        notUstSatir.addWidget(notGorsel)
        notDikey.addWidget(notUst)
        notDikey.addWidget(T.ayirici(T.BOLUCU_ACIK))

        notlar = QTextBrowser()
        notlar.setObjectName("konsolMetin")
        notlar.setOpenExternalLinks(False)
        notlar.setHtml(_not_html(self.sonuc.get("notlar", "")))
        notDikey.addWidget(notlar, 1)

        notAlt = QWidget()
        notAltSatir = QHBoxLayout(notAlt)
        notAltSatir.setContentsMargins(22, 12, 22, 16)
        notAltSatir.addWidget(T.etiket("DGMCRAFT / GÜNCELLEME", "yardimciEtiket"))
        notDikey.addWidget(notAlt)
        satir.addWidget(notKart, 1)
        return govde

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
