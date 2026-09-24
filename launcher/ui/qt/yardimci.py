"""PySide6 yardımcı parçaları: pixmap yükleme, gölge, gradyan çerçeve, rozet."""
import os

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (QBrush, QColor, QLinearGradient, QPainter, QPen, QPixmap,
                           QRadialGradient)
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QLabel

from . import tema as T

_onbellek = {}


def pixmap(*parca):
    """assets altındaki PNG/ICO'yu QPixmap yapar (önbellekli)."""
    anahtar = "/".join(parca)
    if anahtar in _onbellek:
        return _onbellek[anahtar]
    try:
        from core import assets as _A
        yol = _A.yol(*parca)
        if not os.path.isfile(yol):
            _onbellek[anahtar] = None
            return None
        pm = QPixmap(yol)
        _onbellek[anahtar] = pm
        return pm
    except Exception:
        return None


def ikon_pixmap(ad, kutu=20):
    """Ray ikonu tek görsel (ölçekli)."""
    return _kucult("v2", "nav-icons", ("%s.png" % ad), kutu=kutu)


class IkonSeti:
    """Pasif (gri) ve aktif (amber) ikon çifti."""

    def __init__(self, pasif, aktif=None):
        self._p = pasif
        self._a = aktif if aktif is not None else pasif

    def pasif(self):
        return self._p

    def aktif(self):
        return self._a


def ray_ikon_seti(ad, kutu=20):
    """nav-icons/<ad>-gri.png + -aktif.png çiftini ölçekli döndürür."""
    p = _kucult("v2", "nav-icons", ("%s-gri.png" % ad), kutu=kutu)
    a = _kucult("v2", "nav-icons", ("%s-aktif.png" % ad), kutu=kutu)
    if p is None and a is None:
        return IkonSeti(None, None)
    return IkonSeti(p, a)


def _kucult(*parca, kutu=20):
    anahtar = "k:%d:%s" % (kutu, "/".join(parca))
    if anahtar in _onbellek:
        return _onbellek[anahtar]
    try:
        from core import assets as _A
        yol = _A.yol(*parca)
        if not os.path.isfile(yol):
            return None
        pm = QPixmap(yol)
        if not pm.isNull():
            pm = pm.scaled(kutu, kutu, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        _onbellek[anahtar] = pm
        return pm
    except Exception:
        return None


def golge(widget, yaricapi=22, karartma=95, ofset=6):
    """Gerçek yumuşak gölge (QSS desteklemez, Qt effect ile)."""
    try:
        efekt = QGraphicsDropShadowEffect(widget)
        efekt.setBlurRadius(yaricapi)
        efekt.setOffset(0, ofset)
        efekt.setColor(QColor(0, 0, 0, karartma))
        widget.setGraphicsEffect(efekt)
        return efekt
    except Exception:
        return None


class HeroCerceve(QFrame):
    """Dikey gradyan + solda yumuşak ışıma + sağda kenar tüylü görsel.
    Tkinter'da piksel piksel yazılan efektin Qt karşılığı."""

    def __init__(self, ebeveyn, ust, alt, isik_rengi, guc=0.13, gorsel=None,
                 isik_x=150, isik_y=150, isik_r=300):
        super().__init__(ebeveyn)
        self._ust = ust
        self._alt = alt
        self._isik_rengi = isik_rengi
        self._guc = guc
        self._gorsel = gorsel
        self._ix, self._iy, self._ir = isik_x, isik_y, isik_r
        self.setMinimumHeight(212)

    def paintEvent(self, olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        alan = QRectF(self.rect())
        dikey = QLinearGradient(alan.topLeft(), alan.bottomLeft())
        dikey.setColorAt(0.0, QColor(self._ust))
        dikey.setColorAt(1.0, QColor(self._alt))
        boya.fillRect(alan, dikey)
        if self._gorsel is not None and not self._gorsel.isNull():
            hedef_x = int(alan.right() - self._gorsel.width())
            hedef_y = int(alan.center().y() - self._gorsel.height() / 2)
            boya.setOpacity(0.95)
            boya.drawPixmap(hedef_x, hedef_y, self._gorsel)
            boya.setOpacity(1.0)
        if self._guc > 0:
            yaricap = self._ir
            g = QRadialGradient(QPointF(self._ix, self._iy), yaricap)
            g.setColorAt(0.0, QColor(240, 162, 2, int(255 * self._guc)))
            g.setColorAt(0.55, QColor(240, 162, 2, int(255 * self._guc * 0.35)))
            g.setColorAt(1.0, QColor(240, 162, 2, 0))
            boya.fillRect(alan, QBrush(g))
        boya.setPen(QPen(QColor(36, 47, 43), 1))
        boya.setBrush(Qt.NoBrush)
        boya.drawRoundedRect(alan.adjusted(0.5, 0.5, -0.5, -0.5), 12, 12)


def rozet(ebeveyn, metin, renk, nokta=True):
    """Küçük durum hapı: nokta + yazı."""
    kutu = QFrame(ebeveyn)
    kutu.setObjectName("rozet")
    kutu.setStyleSheet(
        "QFrame#rozet { background: #141D18; border: 1px solid #1E2A25; border-radius: 9px; }")
    satir = QHBoxLayout(kutu)
    satir.setContentsMargins(8, 0, 9, 0)
    satir.setSpacing(6)
    if nokta:
        n = QFrame(kutu)
        n.setFixedSize(6, 6)
        n.setStyleSheet("background: %s; border-radius: 3px;" % renk)
        satir.addWidget(n, 0, Qt.AlignVCenter)
    yazi = QLabel(metin, kutu)
    yazi.setObjectName("rozetYazi")
    yazi.setStyleSheet("color: %s; font-size: 11px;" % T.SOLUK)
    satir.addWidget(yazi, 0, Qt.AlignVCenter)
    kutu.setFixedHeight(19)
    return kutu
