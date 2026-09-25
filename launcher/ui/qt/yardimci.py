"""PySide6 yardımcı parçaları: pixmap yükleme, gölge, gradyan çerçeve, rozet."""
import os

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (QBrush, QColor, QLinearGradient, QPainter, QPen, QPixmap,
                           QRadialGradient)
from PySide6.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QLabel,
                               QPushButton, QVBoxLayout, QWidget)

from . import ikonlar
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


class RayDugmesi(QPushButton):
    """Ray öğesi: seçiliyse koyu yuvarlak kutu + yeşil gösterge,
    ikon ince çizgi olarak çizilir (aktif: açık gri, pasif: soluk)."""

    def __init__(self, tur, ad, ebeveyn=None):
        super().__init__(ebeveyn)
        self.tur = tur
        self.ad = ad
        self.setCheckable(True)
        self.setFixedSize(56, 48)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(ad)
        self.setAttribute(Qt.WA_Hover, True)
        self.setStyleSheet("background: transparent; border: none;")

    def paintEvent(self, olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        kutu = QRectF(self.rect()).adjusted(10, 0, -4, -1)
        if self.isChecked():
            boya.setPen(Qt.NoPen)
            boya.setBrush(QColor("#1A211E"))
            boya.drawRoundedRect(kutu, 12, 12)
            boya.setBrush(QColor(T.YESIL))
            boya.drawRoundedRect(QRectF(1, 12, 3, 24), 1.5, 1.5)
            renk = "#EDF2F0"
        else:
            if self.underMouse():
                boya.setPen(Qt.NoPen)
                boya.setBrush(QColor("#161D1A"))
                boya.drawRoundedRect(kutu, 12, 12)
            renk = "#7E8B86"
        ikonlar.ciz(boya, self.tur, QPointF(34, 24), 22, renk)
        boya.end()


    def resizeEvent(self, olay):
        try:
            for c in self.findChildren(QFrame):
                if c.objectName() == "ayrac":
                    c.setGeometry(0, self.height() - 1, self.width(), 1)
        except Exception:
            pass
        super().resizeEvent(olay)


class BaslikDugmesi(QPushButton):
    """Küçült / kapat: şeffaf, hover'da yuvarlak zemin."""

    def __init__(self, tur, ebeveyn=None):
        super().__init__(ebeveyn)
        self.tur = tur
        self.setFixedSize(38, 34)
        self.setCursor(Qt.ArrowCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_Hover, True)
        self.setStyleSheet("background: transparent; border: none;")

    def paintEvent(self, olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        alan = QRectF(self.rect()).adjusted(3, 3, -3, -3)
        if self.underMouse():
            boya.setPen(Qt.NoPen)
            boya.setBrush(QColor("#B3453B" if self.tur == "kapat" else "#1D2523"))
            boya.drawRoundedRect(alan, 8, 8)
        boya.setPen(QPen(QColor("#9AA8A0"), 1.3))
        if self.tur == "kapat":
            boya.drawLine(13, 11, 25, 23)
            boya.drawLine(25, 11, 13, 23)
        else:
            boya.drawLine(13, 18, 25, 18)
        boya.end()

    def mousePressEvent(self, olay):
        super().mousePressEvent(olay)
        if self.tur == "kapat":
            # self.close() butonu kapatır; pencere için window().close() şart.
            self.window().close()


class BaslikCubugu(QFrame):
    """Kendi başlık çubuğumuz: pencereyi sürükler, çift tık ile küçültür.
    Altındaki çizgi görsel olarak ayırır."""

    def __init__(self, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("baslikCubugu")
        self.setFixedHeight(T.UST_YUKSEKLIK)
        self._baslangic = None
        self._pencere_baslangic = None
        self.setCursor(Qt.ArrowCursor)
        c = QFrame(self)
        c.setObjectName("ayrac")
        c.setGeometry(0, self.height() - 1, self.width(), 1)
        c.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        c.show()

    def _baslat(self, olay):
        if olay.button() != Qt.LeftButton:
            return
        self._baslangic = olay.globalPosition().toPoint()
        self._pencere_baslangic = self.window().frameGeometry().topLeft()

    def _tasi(self, olay):
        if self._baslangic is None or self._pencere_baslangic is None:
            return
        if not (olay.buttons() & Qt.LeftButton):
            return
        fark = olay.globalPosition().toPoint() - self._baslangic
        self.window().move(self._pencere_baslangic + fark)

    def _birak(self, _olay=None):
        self._baslangic = None
        self._pencere_baslangic = None

    def mousePressEvent(self, olay):
        self._baslat(olay)

    def mouseMoveEvent(self, olay):
        self._tasi(olay)

    def mouseReleaseEvent(self, olay):
        self._birak(olay)

    def mouseDoubleClickEvent(self, olay):
        self.window().showMinimized()


class BellekKaydirici(QWidget):
    """Duraklı seçim (2G/3G/4G/6G). Groove, tutamak ve etiketler birlikte
    çizilir; böylece etiket her zaman tutamacın tam altında durur.
    Qt stil motorunun ölçümlerine bağlı kalmaz."""

    deger_degisti = Signal(int)

    def __init__(self, degerler, baslangic=0, ebeveyn=None):
        super().__init__(ebeveyn)
        self.degerler = list(degerler)
        self._adet = len(self.degerler)
        self._secil = max(0, min(self._adet - 1, int(baslangic)))
        self.setFixedHeight(42)
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumWidth(180)

    def value(self):
        return self._secil

    def set_value(self, v, bildir=True):
        v = max(0, min(self._adet - 1, int(v)))
        if v == self._secil:
            return
        self._secil = v
        self.update()
        if bildir:
            self.deger_degisti.emit(v)

    def _nokta(self, i):
        if self._adet <= 1:
            return self.width() / 2.0
        return 9.0 + i * ((self.width() - 18.0) / (self._adet - 1))

    def _en_yakin(self, x):
        if self._adet <= 1:
            return 0
        adim = (self.width() - 18.0) / (self._adet - 1)
        return max(0, min(self._adet - 1, int(round((x - 9.0) / adim))))

    def mousePressEvent(self, olay):
        if olay.button() == Qt.LeftButton:
            self.set_value(self._en_yakin(olay.position().x()))

    def mouseMoveEvent(self, olay):
        if olay.buttons() & Qt.LeftButton:
            self.set_value(self._en_yakin(olay.position().x()))

    def paintEvent(self, _olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        y = 9.0
        sol, sag = self._nokta(0), self._nokta(self._adet - 1)
        boya.setPen(Qt.NoPen)
        boya.setBrush(QColor("#2A3530"))
        boya.drawRoundedRect(QRectF(sol - 1, y - 2, (sag - sol) + 2, 4), 2, 2)
        if self._secil > 0:
            boya.setBrush(QColor(T.VURGU))
            boya.drawRoundedRect(
                QRectF(sol - 1, y - 2, self._nokta(self._secil) - sol + 1, 4), 2, 2)
        boya.setFont(self.font())
        for i, metin in enumerate(self.degerler):
            x = self._nokta(i)
            kutu = QRectF(x - 28, y + 10, 56, 16)
            if i == self._secil:
                boya.setBrush(QColor(T.VURGU_HOVER if self.underMouse() else T.VURGU))
                boya.drawEllipse(QPointF(x, y), 8, 8)
                boya.setPen(QColor("#EDF2F0"))
            else:
                boya.setPen(QColor("#6E7F76"))
            boya.drawText(kutu, Qt.AlignCenter, metin)
        boya.end()


def yerlesim_temizle(yerlesim):
    """Yerleşimdeki tüm çocukları anında kaldırır.
    deleteLater() ertelendiği için tek karede üst üste biner; setParent(None)
    ile hemen görünmez yapılır, sonra silinir."""
    try:
        while yerlesim.count():
            oge = yerlesim.takeAt(0)
            for parca in (oge.widget(),):
                if parca is not None:
                    parca.setParent(None)
                    parca.deleteLater()
            alt = oge.layout()
            if alt is not None:
                yerlesim_temizle(alt)
    except Exception:
        pass


def onay_sor(baba, baslik, metin, tamam="Çalıştır", iptal="Vazgeç"):
    """Koyu temalı onay penceresi. True dönerse tamamlandı."""
    try:
        from PySide6.QtWidgets import QDialog, QDialogButtonBox
        pencere = QDialog(baba)
        pencere.setWindowTitle(T.UYGULAMA)
        pencere.setModal(True)
        pencere.setStyleSheet("QDialog { background: %s; }" % T.KART)
        govde = QVBoxLayout(pencere)
        govde.setContentsMargins(20, 18, 20, 16)
        govde.setSpacing(10)
        b = QLabel(baslik)
        b.setObjectName("metin")
        govde.addWidget(b)
        a = QLabel(metin)
        a.setObjectName("ikincil")
        a.setWordWrap(True)
        a.setMaximumWidth(360)
        govde.addWidget(a)
        govde.addSpacing(6)
        kutu = QDialogButtonBox()
        evet = kutu.addButton(tamam, QDialogButtonBox.AcceptRole)
        hayir = kutu.addButton(iptal, QDialogButtonBox.RejectRole)
        for dugme in (evet, hayir):
            dugme.setCursor(Qt.PointingHandCursor)
            dugme.setObjectName("anaDugme" if dugme is evet else "hayaletDugme")
        kutu.accepted.connect(pencere.accept)
        kutu.rejected.connect(pencere.reject)
        govde.addWidget(kutu)
        return bool(pencere.exec())
    except Exception:
        return False


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
