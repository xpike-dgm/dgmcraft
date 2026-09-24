"""v2 ortak parçaları: kart, başlık, düğmeler, ikon çizimleri. Sıfırdan."""
import tkinter as tk
from . import tokens as T


def kart(ebeveyn):
    k = tk.Frame(ebeveyn, bg=T.KART, highlightthickness=1, highlightbackground=T.CERCEVE)
    return k


def baslik(ebeveyn, metin):
    return tk.Label(ebeveyn, text=metin, font=T.FONT_DEV, bg=T.BG, fg=T.YAZI)


def alt_baslik(ebeveyn, metin):
    return tk.Label(ebeveyn, text=metin, font=T.FONT_BASLIK, bg=T.BG, fg=T.YAZI)


def aciklama(ebeveyn, metin):
    return tk.Label(ebeveyn, text=metin, font=T.FONT_METIN, bg=T.BG, fg=T.SOLUK,
                    wraplength=640, justify="left")


def birincil_dugme(ebeveyn, metin, komut):
    b = tk.Button(ebeveyn, text=metin, command=komut, bg=T.VURGU, fg=T.VURGU_YAZI,
                  font=("Inter", 11, "bold"), relief="flat", padx=22, pady=10,
                  activebackground=T.VURGU_HOVER, activeforeground=T.VURGU_YAZI,
                  cursor="hand2")
    return b


def ikincil_dugme(ebeveyn, metin, komut):
    b = tk.Button(ebeveyn, text=metin, command=komut, bg=T.YUZEY, fg=T.YAZI,
                  font=T.FONT_METIN, relief="flat", padx=18, pady=8,
                  highlightthickness=1, highlightbackground=T.CERCEVE,
                  activebackground="#1C2622", activeforeground=T.YAZI, cursor="hand2")
    return b


class AdimSlider(tk.Frame):
    """Duraklı kaydırıcı: RAM gibi güvenli aralıklarda seçim.
    degerler=[(etiket, veri), ...], örn. [("2G", 2), ("3G", 3)]."""

    def __init__(self, ebeveyn, degerler, baslangic=1, komut=None, genislik=460):
        super().__init__(ebeveyn, bg=T.KART)
        self.degerler = list(degerler)
        self.komut = komut
        self.secil = max(0, min(len(self.degerler) - 1, baslangic))
        self.genislik = genislik
        self._roz_deger = tk.StringVar(value="")
        tk.Label(self, textvariable=self._roz_deger, font=("Inter", 11, "bold"),
                 bg="#1C2622", fg=T.YESIL).pack(anchor="w", pady=(0, 6))
        self.tuval = tk.Canvas(self, width=genislik, height=44, bg=T.KART,
                               highlightthickness=0)
        self.tuval.pack(fill="x")
        self.tuval.bind("<Button-1>", self._tik)
        self.tuval.bind("<B1-Motion>", self._tik)
        self._ciz()
        self._yansit()

    def _nokta(self, i):
        n = len(self.degerler)
        if n <= 1:
            return 20
        return 20 + i * ((self.genislik - 40) / (n - 1))

    def _ciz(self):
        c = self.tuval
        try:
            c.delete("all")
            y = 14
            c.create_line(20, y, self.genislik - 20, y, fill="#2A3530", width=6, capstyle="round")
            x1 = self._nokta(self.secil)
            c.create_line(20, y, x1, y, fill=T.VURGU, width=6, capstyle="round")
            for i, (etiket, _v) in enumerate(self.degerler):
                x = self._nokta(i)
                c.create_oval(x - 3, y - 3, x + 3, y + 3, fill=T.KART, outline="#3A4A43", width=2)
                c.create_text(x, y + 20, text=etiket, fill=T.SOLUK, font=("Inter", 9))
            c.create_oval(x1 - 9, y - 9, x1 + 9, y + 9, fill=T.VURGU, outline=T.VURGU_HOVER, width=2)
        except Exception:
            pass

    def _tik(self, olay):
        try:
            n = len(self.degerler)
            oran = (olay.x - 20) / max(1, (self.genislik - 40))
            i = max(0, min(n - 1, round(oran * (n - 1))))
            if i != self.secil:
                self.secil = i
                self._ciz()
                self._yansit()
                if self.komut:
                    self.komut(self.degerler[i][1])
        except Exception:
            pass

    def _yansit(self):
        try:
            self._roz_deger.set(str(self.degerler[self.secil][0]))
        except Exception:
            pass

    def deger(self):
        return self.degerler[self.secil][1]


class Anahtar(tk.Frame):
    """Açma-kapama düğmesi. acik=True/False, komut(yeni_deger)."""

    def __init__(self, ebeveyn, acik=False, komut=None, genislik=52, yukseklik=28):
        super().__init__(ebeveyn, bg=T.KART)
        self.acik = bool(acik)
        self.komut = komut
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.tuval = tk.Canvas(self, width=genislik, height=yukseklik, bg=T.KART,
                               highlightthickness=0, cursor="hand2")
        self.tuval.pack()
        self.tuval.bind("<Button-1>", self._degistir)
        self._ciz(False)

    def _ciz(self, anim=True):
        c = self.tuval
        try:
            c.delete("all")
            w, h = self.genislik, self.yukseklik
            r = h // 2
            zemin = T.VURGU if self.acik else "#2A3530"
            c.create_oval(0, 0, h, h, fill=zemin, outline=zemin)
            c.create_oval(w - h, 0, w, h, fill=zemin, outline=zemin)
            c.create_rectangle(r, 0, w - r, h, fill=zemin, outline=zemin)
            dx = w - h + 3 if self.acik else 3
            c.create_oval(dx, 3, dx + h - 6, h - 3, fill="#FFFFFF", outline="")
        except Exception:
            pass

    def _degistir(self, _olay=None):
        self.acik = not self.acik
        self._ciz()
        try:
            if self.komut:
                self.komut(self.acik)
        except Exception:
            pass

    def kur(self, acik):
        self.acik = bool(acik)
        self._ciz()


def giris(ebeveyn, degisken=None, genislik=None):
    e = tk.Entry(ebeveyn, textvariable=degisken, bg="#0F1513", fg=T.YAZI,
                 insertbackground=T.VURGU, relief="flat",
                 highlightthickness=1, highlightbackground=T.CERCEVE,
                 highlightcolor=T.VURGU, font=("Inter", 11))
    if genislik:
        e.configure(width=genislik)
    return e


def ikon_ciz(ebeveyn, tur, boyut=26, renk=None):
    """Ray ikonları: ince çizgi çizimler (dosya gerektirmez)."""
    renk = renk or T.SOLUK
    c = tk.Canvas(ebeveyn, width=boyut, height=boyut, bg=T.YUZEY,
                  highlightthickness=0)
    o = boyut / 26.0
    w = max(2, int(2 * o))

    def cizgi(*noktalar):
        c.create_line(*[n * o for n in noktalar], fill=renk, width=w, capstyle="round", joinstyle="round")

    def dikdortgen(x1, y1, x2, y2):
        c.create_rectangle(x1 * o, y1 * o, x2 * o, y2 * o, outline=renk, width=w)

    if tur == "hub":
        cizgi(13, 22, 13, 11, 4, 11, 4, 22)
        cizgi(22, 22, 22, 11, 18, 11)
        c.create_rectangle(10 * o, 11 * o, 16 * o, 17 * o, outline=renk, width=w)
    elif tur == "komutlar":
        cizgi(4, 7, 22, 7)
        cizgi(4, 13, 22, 13)
        cizgi(4, 19, 14, 19)
        cizgi(18, 19, 22, 19)
    elif tur == "durum":
        cizgi(3, 15, 8, 15, 11, 8, 15, 20, 18, 12, 23, 12)
    elif tur == "konsol":
        cizgi(7, 9, 12, 13, 7, 17)
        cizgi(13, 17, 20, 17)
    elif tur == "gorevler":
        dikdortgen(6, 3, 20, 23)
        cizgi(6, 8, 20, 8)
        cizgi(10, 13, 16, 13)
    elif tur == "yetenekler":
        cizgi(13, 3, 13, 15)
        cizgi(6, 8, 20, 8)
        cizgi(9, 21, 13, 15, 17, 21)
    elif tur == "siralama":
        cizgi(7, 4, 7, 12, 19, 12, 19, 4)
        cizgi(7, 6, 4, 6, 4, 9)
        cizgi(19, 6, 22, 6, 22, 9)
        cizgi(10, 12, 10, 18)
        cizgi(16, 12, 16, 18)
        cizgi(7, 21, 19, 21)
    elif tur == "ayarlar":
        c.create_oval(9 * o, 9 * o, 17 * o, 17 * o, outline=renk, width=w)
        c.create_oval(11.5 * o, 11.5 * o, 14.5 * o, 14.5 * o, outline=renk, width=max(1, int(w * 0.7)))
        for aci in (0, 60, 120, 180, 240, 300):
            import math
            x1 = 13 + 8.5 * math.cos(math.radians(aci))
            y1 = 13 + 8.5 * math.sin(math.radians(aci))
            x2 = 13 + 11 * math.cos(math.radians(aci))
            y2 = 13 + 11 * math.sin(math.radians(aci))
            cizgi(x1, y1, x2, y2)
    return c
