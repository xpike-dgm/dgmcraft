"""Ray ikonları: ince çizgi (outline) çizimler, QPainter ile.
Dosya gerektirmez; her ikon 26x26'lık bir ızgarada tanımlı, 22px'e ölçeklenir."""
import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen


def ciz(boya, tur, merkez, boyut, renk, kalinlik=1.7):
    """İkonu verilen merkeze, verilen boyutta çizer (24x24 ızgara)."""
    o = boyut / 24.0
    dx = merkez.x() - 12 * o
    dy = merkez.y() - 12 * o
    firca = QPen(QColor(renk), max(1.0, kalinlik * o))
    firca.setCapStyle(Qt.RoundCap)
    firca.setJoinStyle(Qt.RoundJoin)
    boya.setPen(firca)
    boya.setBrush(Qt.NoBrush)

    def yol(noktalar, kapali=True):
        if noktalar and not isinstance(noktalar[0], (tuple, list)):
            noktalar = list(zip(noktalar[::2], noktalar[1::2]))
        p = QPainterPath()
        p.moveTo(noktalar[0][0] * o + dx, noktalar[0][1] * o + dy)
        for n in noktalar[1:]:
            p.lineTo(n[0] * o + dx, n[1] * o + dy)
        if kapali:
            p.closeSubpath()
        boya.drawPath(p)

    def cizgi(*noktalar):
        yol(list(noktalar), kapali=False)

    def kutu(x1, y1, x2, y2, yaricap=0):
        boya.drawRoundedRect(QRectF(x1 * o + dx, y1 * o + dy,
                                    (x2 - x1) * o, (y2 - y1) * o),
                             yaricap * o, yaricap * o)

    def daire(x, y, r, dolu=False):
        alan = QRectF((x - r) * o + dx, (y - r) * o + dy, 2 * r * o, 2 * r * o)
        if dolu:
            boya.setBrush(QColor(renk))
            boya.drawEllipse(alan)
            boya.setBrush(Qt.NoBrush)
        else:
            boya.drawEllipse(alan)

    if tur == "hub":
        yol([(4, 10), (12, 4), (20, 10), (20, 20), (4, 20)])
        kutu(9, 13, 15, 20, 1)
    elif tur == "komutlar":
        kutu(3.5, 4.5, 20.5, 19.5, 2.5)
        cizgi(7, 9, 9, 12)
        cizgi(12, 12, 17, 12)
        cizgi(7, 15, 9, 15)
        cizgi(12, 15, 15, 15)
    elif tur == "durum":
        cizgi(3, 16, 8, 16, 11, 8, 15, 19, 18, 12, 21, 12)
        daire(21, 12, 1.6)
    elif tur == "konsol":
        kutu(3, 4.5, 21, 19.5, 2.5)
        cizgi(7, 9.5, 10.5, 13)
        cizgi(10.5, 13, 7, 16.5)
        cizgi(13, 16.5, 17, 16.5)
    elif tur == "gorevler":
        cizgi(9, 5, 15, 5)
        cizgi(10, 5, 10, 4)
        cizgi(14, 5, 14, 4)
        yol([(12, 3), (19, 6), (19, 11), (12, 14), (5, 11), (5, 6)])
        daire(12, 8.5, 1.8)
    elif tur == "yetenekler":
        cizgi(12, 20, 12, 4)
        cizgi(5.5, 8.5, 18.5, 8.5)
        cizgi(8, 20, 12, 16, 16, 20)
    elif tur == "siralama":
        cizgi(6, 4, 6, 12, 18, 12, 18, 4)
        cizgi(6, 6, 3.5, 6, 3.5, 9)
        cizgi(18, 6, 20.5, 6, 20.5, 9)
        cizgi(9, 12, 9, 18)
        cizgi(15, 12, 15, 18)
        cizgi(6, 20.5, 18, 20.5)
    elif tur == "ayarlar":
        daire(12, 12, 3.2)
        daire(12, 12, 6.4)
        for aci in range(0, 360, 45):
            a = math.radians(aci)
            cizgi(12 + 6.8 * math.cos(a), 12 + 6.8 * math.sin(a),
                  12 + 9.2 * math.cos(a), 12 + 9.2 * math.sin(a))
    else:
        kutu(5, 5, 19, 19, 2)


def pixmap_icin_uret(tur, boyut, renk):
    """QPixmap üretir (araçlar/kaydetme için)."""
    from PySide6.QtGui import QPixmap
    pm = QPixmap(boyut, boyut)
    pm.fill(Qt.transparent)
    boya = QPainter(pm)
    boya.setRenderHint(QPainter.Antialiasing, True)
    ciz(boya, tur, QPointF(boyut / 2.0, boyut / 2.0), boyut, renk)
    boya.end()
    return pm
