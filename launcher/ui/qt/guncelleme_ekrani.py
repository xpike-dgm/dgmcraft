"""Açılışta otomatik güncelleme denetimi ve güncelleme ekranı.

Akış:
1) Uygulama açılır açılmaz kendi sürümünü kontrol eder.
2) Yeni sürüm varsa ana arayüzün yerine sadece bu ekran açılır.
3) [Güncelle] basılır: parola doğruysa önce herkese gönderilir,
   sonra bu bilgisayarda kurulur ve uygulama otomatik yeniden başlatılır."""
import os
import subprocess
import sys
import threading
import time

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QVBoxLayout, QWidget)

from . import tema as T
from . import yardimci as Y


class GuncellemeEkrani(QWidget):
    """Yeni sürüm bildirimi: parola alanı + Güncelle düğmesi."""

    durum_mesaji = Signal(str)
    bitti = Signal(bool)

    def __init__(self, hizmetler, sonuc, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self.sonuc = sonuc or {}
        self._arayuz_kur()
        self.durum_mesaji.connect(self._mesaj)
        self.bitti.connect(self._bitti)

    def _arayuz_kur(self):
        self.setObjectName("guncellemeEkrani")
        self.setStyleSheet(
            "QWidget#guncellemeEkrani { background: %s; }" % T.KART)
        dis = QVBoxLayout(self)
        dis.setContentsMargins(28, 30, 28, 30)
        dis.setSpacing(10)
        dis.addStretch(1)

        baslik = QLabel("Yeni sürüm hazır")
        baslik.setObjectName("sayfaBaslik")
        dis.addWidget(baslik)

        surum = QLabel("Bu bilgisayarda yeni sürüm bulundu: %s" % self.sonuc.get("son", "?"))
        surum.setObjectName("ikincil")
        dis.addWidget(surum)
        dis.addSpacing(8)

        notlar = QLabel(_kisa_notlar(self.sonuc.get("notlar", "")))
        notlar.setObjectName("kucuk")
        notlar.setWordWrap(True)
        notlar.setMaximumWidth(520)
        notlar.setAlignment(Qt.AlignTop)
        dis.addWidget(notlar)
        dis.addSpacing(16)

        satir = QHBoxLayout()
        satir.setSpacing(10)
        self.parola = QLineEdit()
        self.parola.setPlaceholderText("Parola (yalnızca sahip için)")
        self.parola.setEchoMode(QLineEdit.Password)
        self.parola.setFixedWidth(220)
        self.parola.setStyleSheet(
            "QLineEdit { background: #0F1513; border: 1px solid %s; border-radius: 9px;"
            " padding: 9px 11px; color: %s; font-size: 13px; }"
            "QLineEdit:focus { border-color: %s; }" % (T.CERCEVE, T.YAZI, T.VURGU))
        satir.addWidget(QLabel("Parola:"))
        satir.addWidget(self.parola)
        satir.addStretch(1)
        dis.addLayout(satir)

        dis.addSpacing(6)
        self.dugme = QPushButton("Güncelle")
        self.dugme.setObjectName("anaDugme")
        self.dugme.setCursor(Qt.PointingHandCursor)
        self.dugme.setFixedWidth(190)
        self.dugme.clicked.connect(self._guncelle)
        dis.addWidget(self.dugme, 0, Qt.AlignLeft)

        self.mesaj = QLabel("")
        self.mesaj.setObjectName("kucuk")
        self.mesaj.setWordWrap(True)
        dis.addWidget(self.mesaj)
        dis.addSpacing(6)

        gec = QPushButton("Şimdi değil")
        gec.setObjectName("hayaletDugme")
        gec.setCursor(Qt.PointingHandCursor)
        gec.clicked.connect(lambda: self.bitti.emit(False))
        dis.addWidget(gec, 0, Qt.AlignLeft)
        dis.addStretch(1)

    def _mesaj(self, metin):
        self.mesaj.setText(metin or "")

    def _bitti(self, tamam):
        self.setVisible(False)

    def _guncelle(self):
        parola = self.parola.text().strip()
        self.dugme.setEnabled(False)
        self.dugme.setText("Güncelleniyor...")
        threading.Thread(target=self._is, args=(parola,), daemon=True).start()

    def _is(self, parola):
        try:
            from core import guncelleme as _G, sahiplik as _S
            Y.guvenli_yayin(self.durum_mesaji, "Parola kontrol ediliyor...")
            sahiplik_var = False
            try:
                sahiplik_var = _S.parola_var_mi() and _S.parola_dogru(parola)
            except Exception:
                sahiplik_var = False
            if sahiplik_var:
                Y.guvenli_yayin(self.durum_mesaji,
                                "Parola doğru. Herkese gönderiliyor...")
                _ok, mesaj = _S.herkese_gonder(self.h.ayar.get("launcherSurumu", ""))
                Y.guvenli_yayin(self.durum_mesaji, mesaj)
            elif parola:
                Y.guvenli_yayin(self.durum_mesaji,
                                "Parola yanlış; yalnızca bu bilgisayar güncellenecek.")
            Y.guvenli_yayin(self.durum_mesaji, "Paket indiriliyor...")
            sonuc = _G.uygula(self.h.kok, self.sonuc, durum_yaz=self._durum)
        except Exception as e:
            Y.guvenli_yayin(self.durum_mesaji, "Güncelleme kurulamadı: %s" % e)
            try:
                self.dugme.setEnabled(True)
                self.dugme.setText("Tekrar Dene")
            except Exception:
                pass
            return
        Y.guvenli_yayin(self.durum_mesaji, "Kuruldu. Uygulama yeniden başlatılıyor...")
        QTimer.singleShot(900, self._yeniden_baslat)

    def _durum(self, metin):
        Y.guvenli_yayin(self.durum_mesaji, metin)

    def _yeniden_baslat(self):
        try:
            _uygulama_yeniden_baslat()
        except Exception:
            pass
        Y.guvenli_yayin(self.bitti, True)
        try:
            QGuiApplication.quit()
        except Exception:
            pass


def _kisa_notlar(metin):
    satirlar = [s.strip(" -*#") for s in (metin or "").splitlines()]
    satirlar = [s for s in satirlar if s and "Full Changelog" not in s]
    return "\n".join(satirlar[:4]) or "Detay yok."


def _uygulama_yeniden_baslat():
    """Uygulamayı kapatıp aynı şekilde yeniden başlatır."""
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


def guncelleme_deneti(kok, ayar, tamamlandi):
    """Açılış denetimi. (sonuc, hata) — tamamlandi(sonuc) çağrılır."""
    try:
        from core import guncelleme as _G
        sonuc = _G.denetle(ayar)
    except Exception as e:
        tamamlandi({"hata": str(e)})
        return
    tamamlandi(sonuc)
