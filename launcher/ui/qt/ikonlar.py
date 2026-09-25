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
    elif tur == "gorev-agac":
        cizgi(12, 3, 12, 7)
        cizgi(12, 7, 5, 14)
        cizgi(12, 7, 19, 14)
        cizgi(12, 11, 4, 18)
        cizgi(12, 11, 20, 18)
        cizgi(12, 18, 12, 21)
    elif tur == "ayarlar":
        daire(12, 12, 3.2)
        daire(12, 12, 6.4)
        for aci in range(0, 360, 45):
            a = math.radians(aci)
            cizgi(12 + 6.8 * math.cos(a), 12 + 6.8 * math.sin(a),
                  12 + 9.2 * math.cos(a), 12 + 9.2 * math.sin(a))
    elif tur == "agac":
        yol([(12, 2.5), (16.5, 9.5), (7.5, 9.5)])
        yol([(12, 7), (18, 15.5), (6, 15.5)])
        cizgi(12, 15.5, 12, 21)
    elif tur == "kazma":
        yol([(2.5, 5.5), (12, 11), (21.5, 5.5)])
        cizgi(12, 11, 12, 21.5)
        cizgi(2.5, 5.5, 2.5, 8.6)
        cizgi(21.5, 5.5, 21.5, 8.6)
    elif tur == "bugday":
        cizgi(12, 21.5, 12, 5)
        for sy in (10, 13.5, 17):
            cizgi(12, sy, 7.8, sy - 2.6)
            cizgi(12, sy, 16.2, sy - 2.6)
        yol([(12, 5.4), (14.2, 2.6), (12, 1.2), (9.8, 2.6)])
    elif tur == "balik":
        yol([(3.2, 12), (8, 6.4), (16, 6.4), (20.4, 12), (16, 17.6), (8, 17.6)])
        cizgi(3.2, 12, 1.2, 8)
        cizgi(3.2, 12, 1.2, 16)
        daire(16.2, 10.6, 1.1, True)
    elif tur == "kurek":
        yol([(8.5, 3.5), (15.5, 3.5), (15.5, 11), (12, 14.5), (8.5, 11)])
        cizgi(12, 14.5, 12, 21.5)
        cizgi(9.6, 8.4, 14.4, 8.4)
    elif tur == "ok":
        yol([(7, 3), (13, 6), (15, 12), (13, 18), (7, 21)])
        cizgi(4, 12, 20, 12)
        cizgi(17, 9.5, 20, 12, 17, 14.5)
    elif tur == "kalkan":
        yol([(12, 2.5), (20, 6), (19, 14), (12, 21.5), (5, 14), (4, 6)])
        cizgi(12, 6, 12, 17)
    elif tur == "kilic":
        cizgi(12, 2.5, 12, 15)
        cizgi(8.5, 15.5, 15.5, 15.5)
        cizgi(12, 15.5, 12, 20)
        cizgi(9.5, 20, 14.5, 20)
        cizgi(12, 2.5, 10, 5.5)
    elif tur == "bot":
        yol([(6.4, 2.6), (11.4, 2.6), (11.4, 12.4), (18.6, 14.2), (20.6, 18.4),
             (20.6, 21), (6.4, 21)])
        cizgi(6.4, 16.6, 20.6, 16.6)
        cizgi(6.4, 8, 11.4, 8)
    elif tur == "iksir":
        yol([(9.2, 2.6), (14.8, 2.6), (14.8, 5.4), (17.4, 9.6), (17.4, 18.4),
             (12, 22), (6.6, 18.4), (6.6, 9.6), (9.2, 5.4)])
        cizgi(8.2, 2.6, 15.8, 2.6)
        daire(10, 13.6, 1)
        daire(14.2, 16.4, 0.8)
    elif tur == "kitap":
        yol([(12, 6), (8, 4), (3.5, 5.5), (3.5, 18), (8, 16.5), (12, 18.5)])
        yol([(12, 6), (16, 4), (20.5, 5.5), (20.5, 18), (16, 16.5), (12, 18.5)])
        cizgi(12, 6, 12, 18.5)
    elif tur == "elmas":
        yol([(7, 4), (17, 4), (20.5, 10), (12, 20.5), (3.5, 10)])
        cizgi(7, 4, 9, 10)
        cizgi(17, 4, 15, 10)
        cizgi(9, 10, 15, 10)
        cizgi(9, 10, 12, 20.5)
        cizgi(15, 10, 12, 20.5)
    elif tur == "sandik":
        yol([(2.8, 9), (4.6, 4), (19.4, 4), (21.2, 9)])
        kutu(2.8, 9, 21.2, 20.6, 1)
        cizgi(2.8, 13.4, 21.2, 13.4)
        kutu(10.2, 11.8, 13.8, 16, 0.8)
    elif tur == "anahtar":
        daire(7.4, 7.4, 4.6)
        cizgi(10.8, 10.8, 20.4, 20.4)
        cizgi(16.2, 16.2, 14, 18.4)
        cizgi(19, 19, 16.8, 21.2)
        cizgi(20.4, 20.4, 18.6, 22.2)
    elif tur == "goz":
        yol([(2, 12), (7, 6.5), (17, 6.5), (22, 12), (17, 17.5), (7, 17.5)])
        daire(12, 12, 3.1)
    elif tur == "tac":
        yol([(3, 18), (4.5, 7), (9, 12), (12, 5.5), (15, 12), (19.5, 7), (21, 18)])
        cizgi(3.5, 20.5, 20.5, 20.5)
    elif tur == "portal":
        yol([(6, 21), (6, 9), (8, 4.5), (16, 4.5), (18, 9), (18, 21)])
        cizgi(8.5, 21, 8.5, 10)
        cizgi(15.5, 21, 15.5, 10)
        cizgi(6, 21, 18, 21)
    elif tur == "kalp":
        yol([(12, 21), (3.4, 13), (3.4, 8.2), (6.6, 5.4), (10.2, 6.2), (12, 9.4)])
        yol([(12, 21), (20.6, 13), (20.6, 8.2), (17.4, 5.4), (13.8, 6.2), (12, 9.4)])
        daire(12, 16.6, 1.4, True)
    elif tur == "yildiz":
        for i in range(8):
            a1 = math.radians(i * 45 - 90)
            a2 = math.radians(i * 45 - 90 + 22.5)
            cizgi(12 + 8.6 * math.cos(a2), 12 + 8.6 * math.sin(a2),
                  12 + 3.2 * math.cos(a2), 12 + 3.2 * math.sin(a2))
            cizgi(12 + 3.2 * math.cos(a2), 12 + 3.2 * math.sin(a2),
                  12 + 8.6 * math.cos(a1), 12 + 8.6 * math.sin(a1))
    elif tur == "mesale":
        cizgi(12, 21, 12, 9)
        yol([(8.5, 9), (9.5, 4.5), (12, 2.5), (14.5, 4.5), (15.5, 9)])
        cizgi(9, 8, 15, 8)
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


ARSIV_TURLERI = ("tohum", "agac", "kuyu", "demir", "kapi", "dalga", "kemik",
                 "yildiz", "kardes", "bosluk", "kule", "ay", "alev")


def ciz_arsiv(boya, tur, merkez, boyut, renk, halka=True, kalinlik=1.6):
    """Bölüm amblemi: ince halka + çizgi (outline) simge (24x24 ızgara)."""
    o = boyut / 24.0
    dx = merkez.x() - 12 * o
    dy = merkez.y() - 12 * o
    renk = QColor(renk)
    kal = max(1.2, kalinlik * o * 1.25)

    def nokta(x, y):
        return x * o + dx, y * o + dy

    def yol(noktalar, kapali=True):
        if noktalar and not isinstance(noktalar[0], (tuple, list)):
            noktalar = list(zip(noktalar[::2], noktalar[1::2]))
        p = QPainterPath()
        ilk = True
        for n in noktalar:
            x, y = nokta(*n)
            if ilk:
                p.moveTo(x, y)
                ilk = False
            else:
                p.lineTo(x, y)
        if kapali:
            p.closeSubpath()
        boya.drawPath(p)

    def cizgi(*noktalar):
        yol(list(noktalar), kapali=False)

    if halka:
        boya.setPen(QPen(renk, max(1.0, kalinlik * o * 0.8)))
        boya.setBrush(Qt.NoBrush)
        boya.drawEllipse(QRectF(dx + 1.4 * o, dy + 1.4 * o, 21.2 * o, 21.2 * o))
        boya.setPen(QPen(renk, kal))
    else:
        boya.setPen(QPen(renk, kal))
    boya.setBrush(Qt.NoBrush)
    firca = boya.pen()
    firca.setCapStyle(Qt.RoundCap)
    firca.setJoinStyle(Qt.RoundJoin)
    boya.setPen(firca)

    if tur == "tohum":
        yol([(12, 20.4), (9, 16.6), (9, 12.6), (12, 9.6), (15, 12.6), (15, 16.6)])
        cizgi(12, 10, 12, 4.6)
        yol([(12, 7.4), (15.4, 6.6), (16.8, 3.8), (13.2, 4.6)])
    elif tur == "agac":
        yol([(12, 4), (15.6, 9.8), (8.4, 9.8)])
        cizgi(12, 9.8, 12, 15.2)
        yol([(12, 9.2), (17.6, 15.2), (6.4, 15.2)])
        cizgi(6.4, 15.2, 17.6, 15.2)
        cizgi(10.4, 15.2, 10.4, 20.4)
        cizgi(13.6, 15.2, 13.6, 20.4)
        cizgi(10.4, 20.4, 13.6, 20.4)
    elif tur == "kuyu":
        yol([(5.6, 20.4), (5.6, 11), (8.2, 6.6), (15.8, 6.6), (18.4, 11),
             (18.4, 20.4)], kapali=False)
        cizgi(5.6, 20.4, 9.2, 20.4)
        cizgi(14.8, 20.4, 18.4, 20.4)
        cizgi(9.2, 20.4, 9.2, 11.6)
        cizgi(9.2, 11.6, 14.8, 11.6)
        cizgi(14.8, 11.6, 14.8, 20.4)
        cizgi(6.8, 6.6, 17.2, 6.6)
    elif tur == "demir":
        yol([(4.4, 9.6), (19.6, 9.6), (17.6, 13), (13.4, 13), (12.6, 16.4)])
        cizgi(12.6, 16.4, 16.2, 16.4)
        cizgi(16.2, 16.4, 16.2, 20.4)
        cizgi(16.2, 20.4, 7.8, 20.4)
        cizgi(7.8, 20.4, 7.8, 16.4)
        cizgi(7.8, 16.4, 11.4, 16.4)
        cizgi(11.4, 16.4, 10.6, 13)
        cizgi(10.6, 13, 6.4, 13)
        cizgi(6.4, 13, 4.4, 9.6)
    elif tur == "kapi":
        yol([(5.6, 20.4), (5.6, 10.4), (8.2, 5.6), (15.8, 5.6), (18.4, 10.4),
             (18.4, 20.4)], kapali=False)
        cizgi(5.6, 20.4, 8.8, 20.4)
        cizgi(15.2, 20.4, 18.4, 20.4)
        cizgi(8.8, 20.4, 8.8, 10.8)
        cizgi(8.8, 10.8, 10.2, 8.2)
        cizgi(10.2, 8.2, 13.8, 8.2)
        cizgi(13.8, 8.2, 15.2, 10.8)
        cizgi(15.2, 10.8, 15.2, 20.4)
        cizgi(8.2, 5.6, 15.8, 5.6)
    elif tur == "dalga":
        cizgi(2.8, 13.4, 6.8, 9.4, 10, 13, 14, 8.2, 21.2, 12.6)
        cizgi(2.8, 13.4, 2.8, 19.6)
        cizgi(21.2, 12.6, 21.2, 19.6)
        cizgi(2.8, 19.6, 21.2, 19.6)
        cizgi(9.4, 19.6, 10.8, 13.4, 12.2, 19.6)
    elif tur == "kemik":
        cizgi(5, 5.6, 5, 19.8)
        cizgi(5, 8.4, 18.4, 6.8)
        cizgi(18.4, 6.8, 18.4, 9.4)
        cizgi(18.4, 9.4, 5, 11)
        cizgi(5, 12.4, 18.4, 10.8)
        cizgi(18.4, 10.8, 18.4, 13.4)
        cizgi(18.4, 13.4, 5, 15)
        cizgi(5, 16.4, 18.4, 14.8)
        cizgi(18.4, 14.8, 18.4, 17.4)
        cizgi(18.4, 17.4, 5, 19.8)
    elif tur == "yildiz":
        yol([(12, 3), (14.3, 9.7), (21, 12), (14.3, 14.3), (12, 21),
             (9.7, 14.3), (3, 12), (9.7, 9.7)])
    elif tur == "kardes":
        for cx, cy in ((8, 9.4), (16, 9.4), (12, 15.8)):
            boya.drawEllipse(QRectF(cx * o + dx - 4.3 * o, cy * o + dy - 4.3 * o,
                                    8.6 * o, 8.6 * o))
    elif tur == "bosluk":
        boya.drawEllipse(QRectF(5.6 * o + dx, 5.6 * o + dy, 12.8 * o, 12.8 * o))
        for a in (30, 150, 270):
            r = math.radians(a)
            boya.drawLine(QPointF(12 * o + dx + 5.2 * o * math.cos(r),
                                  12 * o + dy + 5.2 * o * math.sin(r)),
                          QPointF(12 * o + dx + 7.8 * o * math.cos(r),
                                  12 * o + dy + 7.8 * o * math.sin(r)))
    elif tur == "kule":
        yol([(3.6, 20.4), (5.2, 4.4), (8.4, 4.4), (9.4, 20.4)], kapali=False)
        yol([(14.6, 20.4), (15.6, 4.4), (18.8, 4.4), (20.4, 20.4)], kapali=False)
        cizgi(9.4, 20.4, 14.6, 20.4)
        cizgi(9.4, 14.2, 14.6, 14.2)
        cizgi(6.8, 8.4, 6.8, 10.8)
        cizgi(17.2, 8.4, 17.2, 10.8)
    elif tur == "ay":
        yol([(16.8, 4.4), (10, 5.2), (6.4, 9.6), (6.4, 14.4), (10, 18.8),
             (16.8, 19.6), (12.4, 16.2), (10.6, 12), (12.4, 7.8)])
        cizgi(17, 9.2, 19.4, 12, 17, 14.8)
    elif tur == "alev":
        yol([(12, 3.8), (14.2, 8.2), (13.4, 12), (10.6, 12), (9.8, 8.2)])
        yol([(6.2, 7.6), (8.2, 11), (5.4, 14.4), (4, 17.6), (8, 20.2),
             (8.4, 16.8)], kapali=False)
        yol([(17.8, 7.6), (15.8, 11), (18.6, 14.4), (20, 17.6), (16, 20.2),
             (15.6, 16.8)], kapali=False)
        cizgi(3.6, 20.4, 20.4, 20.4)
    boya.setPen(Qt.NoPen)
    boya.setBrush(Qt.NoBrush)
