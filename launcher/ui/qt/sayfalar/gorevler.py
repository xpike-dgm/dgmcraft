"""F7 — Görev Ağacı: 750 düğümlük harita; sürükle/klavye ile kaydırma, üstüne
gelince detay kartı.

Harita verisi `core.gorev_agaci`'den gelir. BeautyQuests görev dosyaları
geldiğinde aynı düğümler gerçek ad/durum/ödül bilgisini otomatik alır.
"""
import math
import threading

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (QComboBox, QFrame, QHBoxLayout, QLabel, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)

from .. import ikonlar
from .. import tema as T
from .. import yardimci as Y
from core import gorev_agaci as GA

BASLIK = "Görevler"

DUGUM_R = 30.0        # düğüm yarıçapı (dünya birimi)
EN_KUCUK = 0.26
EN_BUYUK = 1.35
ADIM_KLAVYE = 900.0   # saniyede dünya birimi
KAYDIRMA_SINIR = 1400.0


class DetayKarti(QFrame):
    """Düğümün yanında açılan bilgi kartı."""

    def __init__(self, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setObjectName("agacKart")
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.hide()
        govde = QVBoxLayout(self)
        govde.setContentsMargins(14, 12, 14, 12)
        govde.setSpacing(6)

        self.ustSatir = QHBoxLayout()
        self.ustSatir.setContentsMargins(0, 0, 0, 0)
        self.rozet = QLabel("")
        self.rozet.setObjectName("minik")
        self.rozet.setAlignment(Qt.AlignRight)
        self.ustSatir.addWidget(self.rozet, 1)
        govde.addLayout(self.ustSatir)

        self.ad = QLabel("")
        self.ad.setObjectName("kartBaslik")
        self.ad.setWordWrap(True)
        govde.addWidget(self.ad)

        self.bolum = QLabel("")
        self.bolum.setObjectName("kucuk")
        govde.addWidget(self.bolum)

        self.ozet = QLabel("")
        self.ozet.setObjectName("kucuk")
        self.ozet.setWordWrap(True)
        govde.addWidget(self.ozet)

        self.ayrac = QFrame()
        self.ayrac.setFixedHeight(1)
        self.ayrac.setStyleSheet("background: #242F2B;")
        govde.addWidget(self.ayrac)

        self.odul = QLabel("")
        self.odul.setObjectName("minik")
        self.odul.setWordWrap(True)
        govde.addWidget(self.odul)

        self.ipucu = QLabel("")
        self.ipucu.setObjectName("minik")
        self.ipucu.setWordWrap(True)
        self.ipucu.setStyleSheet("color: #55635D;")
        govde.addWidget(self.ipucu)

    def goster(self, dugum, ekran, tuval):
        ad = dugum.get("ad") or "Görev %03d" % dugum.get("no", 0)
        self.ad.setText(ad)
        durum = dugum.get("durum", GA.DURUM_TANIMSIZ)
        renk = GA.DURUM_RENK.get(durum, T.SILIK)
        self.rozet.setText('<span style="color:%s;font-weight:700;">%s</span>'
                           % (renk, GA.DURUM_ETIKET.get(durum, "")))
        self.bolum.setText("Bölüm %d · %s" % (GA.ARSIV_SIRA.get(dugum["arsiv"], 0) + 1,
                                             GA.ARSIV_ADI.get(dugum["arsiv"], "")))
        ozet = dugum.get("aciklama") or GA.ARSIV_OZET.get(dugum["arsiv"], "")
        if dugum.get("objektif"):
            ozet = ("%d hedef. " % dugum["objektif"]) + ozet
        self.ozet.setText(_kisalt(ozet, 190))
        odul = dugum.get("odul") or []
        self.odul.setText(("Ödül: " + " · ".join(odul[:4])) if odul
                          else "Ödül: görev tanımı gelince yazılacak")
        gerek = dugum.get("oncesi") or []
        self.ipucu.setText(("Ön koşul: " + ", ".join("#%03d" % o for o in gerek[:3]))
                           if gerek else "Ön koşulu yok")
        self.adjustSize()
        gen = self.sizeHint()
        w = max(250, min(320, gen.width()))
        h = gen.height()
        x = ekran.x() + DUGUM_R * 1.2 + 16
        y = ekran.y() - h / 2.0
        if x + w > tuval.width() - 10:
            x = ekran.x() - DUGUM_R * 1.2 - 16 - w
        y = max(8, min(tuval.height() - h - 8, y))
        self.setGeometry(int(x), int(y), int(w), int(h))
        self.show()
        self.raise_()


def _kisalt(metin, sinir):
    m = " ".join((metin or "").split())
    if len(m) <= sinir:
        return m
    return m[:sinir].rsplit(" ", 1)[0] + "…"


class AgacTuvali(QWidget):
    """Kaydırılabilir harita: fare sürükle, WASD/yön tuşları, tekerlek, Q/E döndür."""

    dugum_secili = Signal(object)

    def __init__(self, ebeveyn=None):
        super().__init__(ebeveyn)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)

        self.harita = None
        self.olcek = 0.62
        self.ofset = QPointF(0.0, 0.0)
        self.aci = 0.0
        self._surukle = None
        self._tuslar = set()
        self._uzerinde = None
        self._secili = None
        self._gorunur = []
        self._son_fare = None
        self._arka = None

        self.kart = DetayKarti(self)

        self._saat = QTimer(self)
        self._saat.setInterval(16)
        self._saat.timeout.connect(self._kaydir_ilerle)

    # ------------------------------------------------------------- veri -----
    def harita_yukle(self, harita):
        self.harita = harita
        self._uzerinde = None
        self._secili = None
        self.kart.hide()
        if harita and not getattr(self, "_ilk_gorunum", False):
            self._ilk_gorunum = True
            self.ilk_konuma_getir()
        self.update()

    def _sinir_kutusu(self):
        if not self.harita:
            return (-2000.0, -2000.0, 2000.0, 2000.0)
        x1 = y1 = 1e18
        x2 = y2 = -1e18
        for a in self.harita["arsivler"]:
            s = a.get("sinir")
            if not s:
                continue
            x1 = min(x1, s[0])
            y1 = min(y1, s[1])
            x2 = max(x2, s[2])
            y2 = max(y2, s[3])
        if x1 > x2:
            return (-2000.0, -2000.0, 2000.0, 2000.0)
        return (x1, y1, x2, y2)

    def ilk_konuma_getir(self):
        """Harita açılınca ilk bölümü, bölüm adı görünecek şekilde getirir."""
        self.olcek = 0.62
        self.aci = 0.0
        self._ilk_konum()
        self.update()

    def _ilk_konum(self):
        if not self.harita or not self.harita["arsivler"]:
            return
        a = self.harita["arsivler"][0]
        self.ofset = QPointF(a["merkez"][0], a["ust"] + 260.0)

    def aktif_dugum(self):
        """Henüz tamamlanmamış, oynanabilir ilk gerçek görev."""
        if not self.harita:
            return None
        for g in self.harita["dugumler"]:
            if g.get("durum") == GA.DURUM_AKTIF:
                return g
        return None

    def oyuncuya_git(self, dugum):
        if not dugum:
            return
        self.ofset = QPointF(dugum["x"], dugum["y"])
        self.olcek = max(self.olcek, 0.85)
        self._secili = dugum
        self.update()
        self.dugum_secili.emit(dugum)

    # ---------------------------------------------------------- dönüşüm -----
    def _ekran(self, dunya):
        px = (dunya[0] - self.ofset.x()) * self.olcek
        py = (dunya[1] - self.ofset.y()) * self.olcek
        c, s = math.cos(self.aci), math.sin(self.aci)
        return QPointF(px * c - py * s + self.width() / 2.0,
                       px * s + py * c + self.height() / 2.0)

    def _dunya(self, ekran):
        px = ekran.x() - self.width() / 2.0
        py = ekran.y() - self.height() / 2.0
        c, s = math.cos(-self.aci), math.sin(-self.aci)
        return QPointF((px * c - py * s) / self.olcek + self.ofset.x(),
                       (px * s + py * c) / self.olcek + self.ofset.y())

    def _gorunur_alan(self, pay=140.0):
        noktalar = [QPointF(0, 0), QPointF(self.width(), 0),
                    QPointF(0, self.height()), QPointF(self.width(), self.height())]
        d = [self._dunya(n) for n in noktalar]
        xs = [p.x() for p in d]
        ys = [p.y() for p in d]
        return (min(xs) - pay, min(ys) - pay, max(xs) + pay, max(ys) + pay)

    # ------------------------------------------------------------- çizim -----
    def paintEvent(self, olay):
        boya = QPainter(self)
        boya.setRenderHint(QPainter.Antialiasing, True)
        self._arka_zenit(boya)
        if not self.harita:
            boya.setPen(QColor(T.SILIK))
            font = QFont(self.font())
            font.setPointSize(11)
            boya.setFont(font)
            boya.drawText(self.rect(), Qt.AlignCenter,
                          "Görev ağacı hazırlanıyor…")
            boya.end()
            return
        alan = self._gorunur_alan()
        self._kenarlari_ciz(boya, alan)
        self._arsivleri_ciz(boya, alan)
        self._dugumleri_ciz(boya, alan)
        self._minimap_ciz(boya)
        boya.end()

    def _arka_zenit(self, boya):
        arka = self._arka_pixmap()
        if arka is not None:
            boya.drawPixmap(0, 0, arka)
        else:
            boya.fillRect(self.rect(), QColor(T.BG))
        self._izgara_ciz(boya)

    def _arka_pixmap(self):
        """Arka plan dokusunu bir kez ölçekleyip saklar (her karede ölçek yapmaz)."""
        if self._arka is not None and self._arka.size() == self.size():
            return self._arka
        self._arka = QPixmap(self.size())
        self._arka.fill(QColor(T.BG))
        pm = Y.pixmap("v2", "quest-tree-background.png")
        if pm is not None and not pm.isNull():
            boya = QPainter(self._arka)
            boya.setRenderHint(QPainter.SmoothPixmapTransform, True)
            boya.setOpacity(0.22)
            boya.drawPixmap(QRectF(0, 0, self.width(), self.height()), pm,
                            QRectF(0, 0, pm.width(), pm.height()))
            boya.end()
        return self._arka

    def _izgara_ciz(self, boya):
        """Ekran uzayında dönmüş ızgara; arka plan hissi verir."""
        adim = 150.0
        if self.olcek * adim < 34:
            adim *= 2
        s = adim * self.olcek
        ca, sa = math.cos(self.aci), math.sin(self.aci)
        cx, cy = self.width() / 2.0, self.height() / 2.0
        boya.setPen(QPen(QColor(0x1E, 0x2A, 0x25), 1))
        boya.setBrush(Qt.NoBrush)
        kosa = self.width() + self.height()
        adet = int(kosa / s) + 3
        u = -kosa * 0.5 - s
        # Yatay çizgi ailesi: yön (cos, sin), başlangıç dik doğrultuda.
        for i in range(adet):
            t = u + i * s
            ax, ay = cx - sa * t, cy + ca * t
            boya.drawLine(QPointF(ax, ay),
                          QPointF(ax + ca * kosa, ay + sa * kosa))
        # Dikey çizgi ailesi: yön (-sin, cos).
        for j in range(adet):
            t = u + j * s
            ax, ay = cx + ca * t, cy + sa * t
            boya.drawLine(QPointF(ax, ay),
                          QPointF(ax - sa * kosa, ay + ca * kosa))

    def _kenarlari_ciz(self, boya, alan):
        dugum = {g["no"]: g for g in self.harita["dugumler"]}
        o = self.olcek
        kalin_ana = max(1.0, 1.7 * o)
        kalin_yan = max(0.7, 1.0 * o)
        for a, b, tur in self.harita["kenarlar"]:
            ga, gb = dugum.get(a), dugum.get(b)
            if ga is None or gb is None:
                continue
            if tur == "bolum":
                # Bölüm geçiş çizgisi uzundur; iki ucu da görünürse çiz.
                if not (alan[0] < ga["x"] < alan[2] and alan[1] < ga["y"] < alan[3]):
                    continue
                if not (alan[0] < gb["x"] < alan[2] and alan[1] < gb["y"] < alan[3]):
                    continue
            if max(ga["x"], gb["x"]) < alan[0] or min(ga["x"], gb["x"]) > alan[2]:
                continue
            if max(ga["y"], gb["y"]) < alan[1] or min(ga["y"], gb["y"]) > alan[3]:
                continue
            if tur == "bolum":
                renk = QColor(0x2A, 0x35, 0x31, 0xAA)
                kal = max(1.0, 1.2 * o)
            elif tur == "ana":
                renk = QColor(0x42, 0x55, 0x4A, 0xFF)
                kal = kalin_ana
            else:
                renk = QColor(0x33, 0x40, 0x39, 0xE0)
                kal = kalin_yan
            pen = QPen(renk, kal)
            pen.setCapStyle(Qt.RoundCap)
            if tur == "bolum":
                pen.setStyle(Qt.DashLine)
                pen.setDashPattern([3, 7])
            boya.setPen(pen)
            boya.drawLine(self._ekran((ga["x"], ga["y"])),
                          self._ekran((gb["x"], gb["y"])))

    def _arsivleri_ciz(self, boya, alan):
        for a in self.harita["arsivler"]:
            s = a.get("sinir")
            if not s:
                continue
            if s[2] < alan[0] or s[0] > alan[2] or s[3] < alan[1] or s[1] > alan[3]:
                continue
            merkez = self._ekran((a["merkez"][0], a["ust"]))
            boyut = max(26.0, 40.0 * self.olcek)
            boya.save()
            boya.translate(merkez)
            boya.rotate(math.degrees(self.aci))
            ikonlar.ciz_arsiv(boya, a["amblem"], QPointF(0, 0), boyut, T.VURGU)
            boya.restore()
            yazi = self.font()
            yazi.setPointSizeF(max(7.5, min(13.0, 9.0 * self.olcek + 3.5)))
            yazi.setBold(True)
            boya.setFont(yazi)
            boya.setPen(QColor(T.SOLUK))
            boya.drawText(QRectF(merkez.x() + boyut * 0.75,
                                 merkez.y() - boyut * 0.5,
                                 520 * max(0.5, self.olcek), boyut),
                          Qt.AlignVCenter | Qt.AlignLeft, a["ad"])

    def _dugumleri_ciz(self, boya, alan):
        o = self.olcek
        yaricap = DUGUM_R * o
        if yaricap < 2.2:
            return
        ikon_boyut = max(6.0, yaricap * 1.05)
        kalin = max(1.0, 1.7 * o)
        gorunur = []
        for g in self.harita["dugumler"]:
            if g["x"] < alan[0] or g["x"] > alan[2]:
                continue
            if g["y"] < alan[1] or g["y"] > alan[3]:
                continue
            gorunur.append(g)
            p = self._ekran((g["x"], g["y"]))
            durum = g.get("durum", GA.DURUM_TANIMSIZ)
            renk = QColor(GA.DURUM_RENK.get(durum, T.SILIK))
            vurgulu = g is self._uzerinde or g is self._secili
            if vurgulu:
                yaricap2 = yaricap + 5.0
                boya.setPen(Qt.NoPen)
                boya.setBrush(QBrush(QColor(renk.red(), renk.green(),
                                            renk.blue(), 0x33)))
                boya.drawEllipse(p, yaricap2, yaricap2)
            # halka gövde
            if durum in (GA.DURUM_TAMAM, GA.DURUM_AKTIF):
                boya.setPen(Qt.NoPen)
                boya.setBrush(QBrush(QColor(renk.red(), renk.green(),
                                            renk.blue(), 0x1C)))
                boya.drawEllipse(p, yaricap * 1.55, yaricap * 1.55)
            if durum == GA.DURUM_TANIMSIZ:
                boya.setBrush(QColor(0x0F, 0x15, 0x13, 0xCC))
            else:
                boya.setBrush(QColor(0x0F, 0x15, 0x13, 0xF0))
            pen = QPen(renk, kalin if not vurgulu else kalin + 1.2)
            boya.setPen(pen)
            boya.drawEllipse(p, yaricap, yaricap)
            boya.save()
            boya.translate(p)
            boya.rotate(math.degrees(self.aci))
            ikonlar.ciz(boya, g.get("tur", "agac"), QPointF(0, 0), ikon_boyut,
                        T.YAZI if durum != GA.DURUM_TANIMSIZ else T.SILIK,
                        max(1.5, 2.0 * o))
            boya.restore()
        self._gorunur = gorunur
        for g in (self._uzerinde, self._secili):
            if g is None:
                continue
            p = self._ekran((g["x"], g["y"]))
            yazi = self.font()
            yazi.setPointSizeF(9.0)
            yazi.setBold(True)
            boya.setFont(yazi)
            metin = _kisalt(g.get("ad") or "", 42)
            gen = boya.boundingRect(QRectF(0, 0, 400, 40), Qt.TextWordWrap, metin)
            kutu = QRectF(p.x() - gen.width() / 2.0 - 6,
                          p.y() + yaricap + 6, gen.width() + 12, gen.height() + 6)
            boya.setPen(Qt.NoPen)
            boya.setBrush(QColor(0x0B, 0x0F, 0x0E, 0xE6))
            boya.drawRoundedRect(kutu, 6, 6)
            boya.setPen(QColor(T.YAZI))
            boya.drawText(kutu.adjusted(6, 3, -6, -3), Qt.TextWordWrap, metin)

    def _minimap_ciz(self, boya):
        if not self.harita or not self.harita["arsivler"]:
            return
        x1, y1, x2, y2 = self._sinir_kutusu()
        gx = max(1.0, x2 - x1)
        gy = max(1.0, y2 - y1)
        w, h = 132.0, 132.0 * gy / gx
        if h < 40:
            h = 40.0
        sol = self.width() - w - 14
        ust = self.height() - h - 14
        boya.setPen(Qt.NoPen)
        boya.setBrush(QColor(0x0B, 0x0F, 0x0E, 0xD9))
        boya.drawRoundedRect(QRectF(sol, ust, w, h), 8, 8)
        boya.setPen(QPen(QColor(T.CERCEVE), 1))
        boya.setBrush(Qt.NoBrush)
        boya.drawRoundedRect(QRectF(sol, ust, w, h), 8, 8)

        def dunya_kutu(s):
            return QRectF(sol + (s[0] - x1) / gx * w, ust + (s[1] - y1) / gy * h,
                          (s[2] - s[0]) / gx * w, (s[3] - s[1]) / gy * h)

        boya.setPen(Qt.NoPen)
        for a in self.harita["arsivler"]:
            s = a.get("sinir")
            if not s:
                continue
            r = dunya_kutu(s)
            boya.setBrush(QColor(0x1A, 0x24, 0x20, 0xCC))
            boya.drawRoundedRect(r, 3, 3)
            tamam = sum(1 for g in a["dugumler"]
                        if g.get("durum") == GA.DURUM_TAMAM)
            if tamam:
                oran = tamam / float(max(1, len(a["dugumler"])))
                boya.setBrush(QColor(0xF0, 0xA2, 0x02,
                                     int(0x30 + 0xA0 * oran)))
                boya.drawRoundedRect(r, 3, 3)
        alan = self._gorunur_alan(0)
        gorunur_kutu = dunya_kutu(alan)
        boya.setPen(QPen(QColor(T.VURGU), 1.4))
        boya.setBrush(QColor(0xF0, 0xA2, 0x02, 0x22))
        boya.drawRoundedRect(gorunur_kutu.adjusted(0, 0, -1, -1), 4, 4)

    # ------------------------------------------------------------ olaylar ---
    def _sinirla(self):
        x1, y1, x2, y2 = self._sinir_kutusu()
        genislik = (x2 - x1) / self.olcek
        yukseklik = (y2 - y1) / self.olcek
        if self.width() > genislik:
            self.ofset.setX((x1 + x2) / 2.0)
        else:
            self.ofset.setX(max(x1 - KAYDIRMA_SINIR, min(x2 + KAYDIRMA_SINIR,
                                                        self.ofset.x())))
        if self.height() > yukseklik:
            self.ofset.setY((y1 + y2) / 2.0)
        else:
            self.ofset.setY(max(y1 - KAYDIRMA_SINIR, min(y2 + KAYDIRMA_SINIR,
                                                        self.ofset.y())))

    def mousePressEvent(self, olay):
        if olay.button() != Qt.LeftButton:
            return
        self._surukle = olay.position()
        self._son_fare = olay.position()
        self.setCursor(Qt.ClosedHandCursor)
        self.setFocus(Qt.MouseFocusReason)
        dugum = self._altindaki(olay.position())
        if dugum is not None:
            self._secili = dugum
            self.dugum_secili.emit(dugum)
            self.kart.goster(dugum, self._ekran((dugum["x"], dugum["y"])), self)
            self.update()
        else:
            self.kart.hide()

    def mouseMoveEvent(self, olay):
        p = olay.position()
        if self._surukle is not None:
            fark = p - self._surukle
            self._surukle = p
            c, s = math.cos(-self.aci), math.sin(-self.aci)
            self.ofset.setX(self.ofset.x() - (fark.x() * c - fark.y() * s) / self.olcek)
            self.ofset.setY(self.ofset.y() - (fark.x() * s + fark.y() * c) / self.olcek)
            self._sinirla()
            self.kart.hide()
            self.update()
            return
        dugum = self._altindaki(p)
        if dugum is not self._uzerinde:
            self._uzerinde = dugum
            if dugum is not None:
                self.setCursor(Qt.PointingHandCursor)
                self.kart.goster(dugum, self._ekran((dugum["x"], dugum["y"])), self)
            elif self._secili is None:
                self.kart.hide()
            self.update()
        elif dugum is not None:
            self.kart.goster(dugum, self._ekran((dugum["x"], dugum["y"])), self)
        self._son_fare = p

    def mouseReleaseEvent(self, olay):
        self._surukle = None
        self.unsetCursor()

    def leaveEvent(self, olay):
        self._uzerinde = None
        self._son_fare = None
        if self._secili is None:
            self.kart.hide()
        self.update()

    def wheelEvent(self, olay):
        adim = olay.angleDelta().y()
        if not adim:
            return
        eski = self.olcek
        yeni = max(EN_KUCUK, min(EN_BUYUK, eski * (1.12 if adim > 0 else 1 / 1.12)))
        if abs(yeni - eski) < 0.0005:
            return
        imlec = olay.position()
        sabit = self._dunya(imlec)
        self.olcek = yeni
        c, s = math.cos(self.aci), math.sin(self.aci)
        px = (sabit.x() - self.ofset.x()) * yeni
        py = (sabit.y() - self.ofset.y()) * yeni
        self.ofset.setX(sabit.x() - (px * c + py * s) / yeni)
        self.ofset.setY(sabit.y() - (-px * s + py * c) / yeni)
        self._sinirla()
        if self._uzerinde is not None:
            self.kart.goster(self._uzerinde,
                             self._ekran((self._uzerinde["x"],
                                          self._uzerinde["y"])), self)
        self.update()
        olay.accept()

    def keyPressEvent(self, olay):
        tus = olay.key()
        if tus in (Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D,
                   Qt.Key_Up, Qt.Key_Left, Qt.Key_Down, Qt.Key_Right):
            self._tuslar.add(tus)
            self._saat.start()
            olay.accept()
            return
        if tus == Qt.Key_E:
            self.aci += math.radians(12)
            self.update()
            olay.accept()
            return
        if tus == Qt.Key_Q:
            self.aci -= math.radians(12)
            self.update()
            olay.accept()
            return
        if tus == Qt.Key_F:
            dugum = self._secili or self._uzerinde or self.aktif_dugum()
            if dugum is not None:
                self.oyuncuya_git(dugum)
            olay.accept()
            return
        if tus in (Qt.Key_Plus, Qt.Key_Equal):
            self.olcek = min(EN_BUYUK, self.olcek * 1.2)
            self._sinirla()
            self.update()
            olay.accept()
            return
        if tus == Qt.Key_Minus:
            self.olcek = max(EN_KUCUK, self.olcek / 1.2)
            self._sinirla()
            self.update()
            olay.accept()
            return
        olay.ignore()

    def keyReleaseEvent(self, olay):
        tus = olay.key()
        if tus in self._tuslar:
            self._tuslar.discard(tus)
            if not self._tuslar:
                self._saat.stop()
        olay.accept()

    def focusOutEvent(self, olay):
        self._tuslar.clear()
        self._saat.stop()
        super().focusOutEvent(olay)

    def resizeEvent(self, olay):
        self._arka = None
        self._sinirla()
        super().resizeEvent(olay)

    def _kaydir_ilerle(self):
        if not self._tuslar:
            self._saat.stop()
            return
        dx = dy = 0.0
        if Qt.Key_A in self._tuslar or Qt.Key_Left in self._tuslar:
            dx -= 1
        if Qt.Key_D in self._tuslar or Qt.Key_Right in self._tuslar:
            dx += 1
        if Qt.Key_W in self._tuslar or Qt.Key_Up in self._tuslar:
            dy -= 1
        if Qt.Key_S in self._tuslar or Qt.Key_Down in self._tuslar:
            dy += 1
        if not dx and not dy:
            self._saat.stop()
            return
        adim = ADIM_KLAVYE * (1.0 / 60.0) * 1.5
        c, s = math.cos(self.aci), math.sin(self.aci)
        # D/W sağ-yukarı: kamera dünyada o yöne gider (içerik ters yönde kayar).
        self.ofset.setX(self.ofset.x() + (dx * c - dy * s) * adim / self.olcek)
        self.ofset.setY(self.ofset.y() + (dx * s + dy * c) * adim / self.olcek)
        self._sinirla()
        if self._uzerinde is not None:
            self.kart.goster(self._uzerinde,
                             self._ekran((self._uzerinde["x"],
                                          self._uzerinde["y"])), self)
        self.update()

    def _altindaki(self, ekran):
        yaricap = max(8.0, DUGUM_R * self.olcek + 4)
        en = None
        en_kisa = yaricap * yaricap
        for g in self._gorunur:
            p = self._ekran((g["x"], g["y"]))
            d = (p.x() - ekran.x()) ** 2 + (p.y() - ekran.y()) ** 2
            if d <= en_kisa:
                en_kisa = d
                en = g
        return en


class GorevlerSayfasi(QWidget):
    veri_hazir = Signal(object, object)

    def __init__(self, hizmetler, ebeveyn=None):
        super().__init__(ebeveyn)
        self.h = hizmetler
        self._oyuncular = []
        self._yuklendi = False
        self.veri_hazir.connect(self._uygula)
        self._arayuz_kur()
        self._yukle()

    # ------------------------------------------------------------- veri -----
    def _yukle(self):
        threading.Thread(target=self._oku, daemon=True).start()

    def _oku(self):
        oyuncular, harita = [], None
        try:
            from core import gorevler as _G
            oyuncular = _G.oyuncular(self.h.kok)
            uuid = oyuncular[0]["uuid"] if oyuncular else None
            onizleme = bool(getattr(self.h, "gorev_onizleme", False))
            harita = GA.agac(self.h.kok, uuid, onizleme=onizleme)
            GA.yerles(harita["arsivler"])
        except Exception as e:
            harita = {"arsivler": [], "dugumler": [], "kenarlar": [], "hata": str(e)}
        Y.guvenli_yayin(self.veri_hazir, oyuncular, harita)

    # ------------------------------------------------------------ arayüz ----
    def _arayuz_kur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(T.BOSLUK, T.BOSLUK, T.BOSLUK, T.BOSLUK)
        dis.setSpacing(8)

        ust = QFrame()
        ust.setObjectName("kart")
        satir = QHBoxLayout(ust)
        satir.setContentsMargins(14, 9, 14, 9)
        satir.setSpacing(10)

        etiket = QLabel("OYUNCU")
        etiket.setObjectName("bolumBaslik")
        satir.addWidget(etiket)
        self.secici = QComboBox()
        self.secici.setFixedWidth(190)
        self.secici.setStyleSheet(
            "QComboBox { background: #0F1513; border: 1px solid %s; border-radius: 9px;"
            " padding: 7px 10px; color: %s; font-size: 13px; }" % (T.CERCEVE, T.YAZI))
        self.secici.currentIndexChanged.connect(self._oyuncu_degisti)
        satir.addWidget(self.secici)

        self.ozet = QLabel("")
        self.ozet.setObjectName("kucuk")
        satir.addWidget(self.ozet)
        satir.addStretch(1)

        self.buton_ara = self._dugme("◀ Başlangıç", self._ilk)
        satir.addWidget(self.buton_ara)
        self.buton_odak = self._dugme("Odaklan", self._odaklan)
        satir.addWidget(self.buton_odak)
        self.buton_kucult = QPushButton("−")
        self.buton_kucult.setObjectName("zoomDugme")
        self.buton_kucult.setCursor(Qt.PointingHandCursor)
        self.buton_kucult.clicked.connect(self._uzaklastir)
        satir.addWidget(self.buton_kucult)
        self.buton_buyut = QPushButton("+")
        self.buton_buyut.setObjectName("zoomDugme")
        self.buton_buyut.setCursor(Qt.PointingHandCursor)
        self.buton_buyut.clicked.connect(self._yaklastir)
        satir.addWidget(self.buton_buyut)
        dis.addWidget(ust)

        self.tuval = AgacTuvali()
        dis.addWidget(self.tuval, 1)

        alt = QFrame()
        alt.setObjectName("kart")
        satir2 = QHBoxLayout(alt)
        satir2.setContentsMargins(14, 8, 14, 8)
        satir2.setSpacing(14)
        for ad, renk in (("Tamamlandı", GA.DURUM_RENK[GA.DURUM_TAMAM]),
                         ("Oynanabilir", GA.DURUM_RENK[GA.DURUM_AKTIF]),
                         ("Kilitli", GA.DURUM_RENK[GA.DURUM_KILITLI]),
                         ("Tanım bekleniyor", GA.DURUM_RENK[GA.DURUM_TANIMSIZ])):
            satir2.addWidget(self._lejant(ad, renk))
        satir2.addStretch(1)
        ipucu = QLabel("Sürükle: kaydır  ·  WASD / oklar: kaydır  ·  Tekerlek: yakınlaş  ·  Q/E: döndür  ·  F: odaklan")
        ipucu.setObjectName("minik")
        satir2.addWidget(ipucu)
        dis.addWidget(alt)

    def _dugme(self, metin, islev, birincil=False):
        b = QPushButton(metin)
        b.setObjectName("anaDugme" if birincil else "hayaletDugme")
        b.setCursor(Qt.PointingHandCursor)
        b.clicked.connect(islev)
        return b

    def _lejant(self, metin, renk):
        kutu = QWidget()
        satir = QHBoxLayout(kutu)
        satir.setContentsMargins(0, 0, 0, 0)
        satir.setSpacing(6)
        nokta = QLabel("●")
        nokta.setStyleSheet("color: %s; background: transparent;" % renk)
        satir.addWidget(nokta)
        yazi = QLabel(metin)
        yazi.setObjectName("minik")
        satir.addWidget(yazi)
        return kutu

    # -------------------------------------------------------------- olay ----
    def _oyuncu_degisti(self, indeks):
        if indeks < 0 or indeks >= len(self._oyuncular):
            return

        def oku():
            harita = None
            try:
                oyuncu = self._oyuncular[indeks]
                onizleme = bool(getattr(self.h, "gorev_onizleme", False))
                harita = GA.agac(self.h.kok, oyuncu["uuid"], onizleme=onizleme)
                GA.yerles(harita["arsivler"])
            except Exception:
                pass
            if harita is not None:
                Y.guvenli_yayin(self.veri_hazir, self._oyuncular, harita)

        threading.Thread(target=oku, daemon=True).start()

    def _uygula(self, oyuncular, harita):
        if oyuncular and oyuncular != self._oyuncular:
            self._oyuncular = oyuncular
            self.secici.blockSignals(True)
            self.secici.clear()
            for o in oyuncular:
                self.secici.addItem(o["ad"] or o["uuid"][:8])
            self.secici.blockSignals(False)
        self.tuval.harita_yukle(harita)
        self._ozet_yaz(harita)

    def _ozet_yaz(self, harita):
        if not harita or not harita.get("dugumler"):
            self.ozet.setText("görev tanımı yok")
            return
        o = harita["ozet"]
        if o["tanimli"] == 0:
            self.ozet.setText("%d görev · %d bölüm · tanımlar bekleniyor"
                              % (o["toplam"], o["bolum"]))
        else:
            self.ozet.setText("%d / %d görev · %d tamamlandı · %d oynanabilir"
                              % (o["tanimli"], o["toplam"], o["tamam"],
                                 o["aktif"]))

    def _ilk(self):
        self.tuval.ilk_konuma_getir()

    def _odaklan(self):
        self.tuval.oyuncuya_git(self.tuval.aktif_dugum())

    def _yaklastir(self):
        self.tuval.olcek = min(EN_BUYUK, self.tuval.olcek * 1.25)
        self.tuval._sinirla()
        self.tuval.update()

    def _uzaklastir(self):
        self.tuval.olcek = max(EN_KUCUK, self.tuval.olcek / 1.25)
        self.tuval._sinirla()
        self.tuval.update()

    def goster(self):
        if not self._yuklendi:
            self._yuklendi = True
            self._yukle()
        self.tuval.setFocus(Qt.OtherFocusReason)

    def gizle(self):
        self.tuval.kart.hide()
