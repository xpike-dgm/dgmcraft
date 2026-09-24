"""v2 ortak parçaları: kart, başlık, düğmeler, ikon çizimleri. Sıfırdan."""
import tkinter as tk
from . import tokens as T


def kart(ebeveyn):
    k = tk.Frame(ebeveyn, bg=T.KART, highlightthickness=1, highlightbackground=T.CERCEVE)
    return k


def baslik(ebeveyn, metin):
    return tk.Label(ebeveyn, text=metin, font=T.FONT_HERO, bg=T.BG, fg=T.YAZI)


def alt_baslik(ebeveyn, metin):
    return tk.Label(ebeveyn, text=metin, font=T.FONT_BASLIK, bg=T.BG, fg=T.YAZI)


def etiket(ebeveyn, metin, fg=None, bg=None):
    return tk.Label(ebeveyn, text=metin, font=T.FONT_ETIKET, bg=bg or T.KART,
                    fg=fg or T.SILIK)


def aciklama(ebeveyn, metin):
    return tk.Label(ebeveyn, text=metin, font=T.FONT_METIN, bg=T.BG, fg=T.SOLUK,
                    wraplength=640, justify="left")


_foto_onbellek = {}


def _hepsap(*parca):
    return "#%02x%02x%02x" % parca


def gradyan(ebeveyn, genislik, yukseklik, bas_renk, son_renk, dikey=True,
            anahtar=None):
    """Gerçek pürüzsüz renk geçişi (PhotoImage.put; harici kütüphane yok).
    SonOyuncu'daki yumuşak arka plan geçişinin tkinter karşılığı."""
    ad = anahtar or ("gr:%d:%d:%s:%s:%s" % (genislik, yukseklik, bas_renk, son_renk, dikey))
    if ad in _foto_onbellek:
        return _foto_onbellek[ad]
    try:
        a = _hex_rgb(bas_renk)
        b = _hex_rgb(son_renk)
        img = tk.PhotoImage(width=genislik, height=yukseklik)
        adimlar = yukseklik if dikey else genislik
        for i in range(max(1, adimlar)):
            oran = i / float(max(1, adimlar - 1))
            renk = tuple(int(a[k] + (b[k] - a[k]) * oran) for k in range(3))
            if dikey:
                img.put(_hepsap(*renk), to=(0, i, genislik, i + 1))
            else:
                img.put(_hepsap(*renk), to=(i, 0, i + 1, yukseklik))
        _foto_onbellek[ad] = img
        return img
    except Exception:
        return None


def parlama(ebeveyn, genislik, yukseklik, renk, guc=0.30, zemin=None,
            merkez=None, anahtar=None):
    """Yumuşak radyal ışık: oval düğmenin arkasındaki renk geçişi.
    zemin liste/tuple ise her satırın kendi rengi kullanılır (dikişsiz)."""
    ad = anahtar or ("pl:%d:%d:%s:%s:%s" % (genislik, yukseklik, renk, guc, zemin))
    if ad in _foto_onbellek:
        return _foto_onbellek[ad]
    try:
        z = _hex_rgb(zemin or T.KART)
        r = _hex_rgb(renk)
        mx, my = merkez or (genislik // 2, yukseklik // 2)
        en = float(max(1, max(mx, genislik - mx, my, yukseklik - my)))
        img = tk.PhotoImage(width=genislik, height=yukseklik)
        for y in range(yukseklik):
            if isinstance(zemin, (list, tuple)) and y < len(zemin):
                zy = _hex_rgb(zemin[y])
            else:
                zy = z
            for x in range(0, genislik, 2):
                d = ((x - mx) ** 2 + (y - my) ** 2) ** 0.5 / en
                t = max(0.0, 1.0 - d) ** 2.2 * guc
                renk_p = tuple(int(zy[k] + (r[k] - zy[k]) * t) for k in range(3))
                img.put(_hepsap(*renk_p), to=(x, y, min(genislik, x + 2), y + 1))
        _foto_onbellek[ad] = img
        return img
    except Exception:
        return None


def gradyan_serit(bas_renk, son_renk, yukseklik):
    """Dikey gradyanın satır renklerini listeler (parlama ile dikişsiz birleşir)."""
    try:
        a = _hex_rgb(bas_renk)
        b = _hex_rgb(son_renk)
        serit = []
        for i in range(max(1, yukseklik)):
            t = i / float(max(1, yukseklik - 1))
            serit.append(_hepsap(*[int(a[k] + (b[k] - a[k]) * t) for k in range(3)]))
        return serit
    except Exception:
        return None


def _hex_rgb(renk):
    try:
        s = renk.lstrip("#")
        return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
    except Exception:
        return (0, 0, 0)


class OvalDugme(tk.Canvas):
    """Yuvarlak (hap şeklinde) düğme. vurgu=True turuncu dolu, False çerçeveli."""

    def __init__(self, ebeveyn, metin, komut, vurgu=True, genislik=190,
                 yukseklik=42, bg=None, font=None):
        super().__init__(ebeveyn, width=genislik, height=yukseklik + 18,
                         bg=bg or T.KART, highlightthickness=0, cursor="hand2")
        self._metin = metin
        self._komut = komut
        self._vurgu = vurgu
        self._g = genislik
        self._y = yukseklik
        self._font = font or ("Inter", 11, "bold")
        self._ust = 9
        self.bind("<Button-1>", self._bas)
        self.bind("<Enter>", lambda e: self._ciz(True))
        self.bind("<Leave>", lambda e: self._ciz(False))
        self._ciz(False)

    def metin(self, yeni):
        self._metin = yeni
        self._ciz(False)

    def _ciz(self, uzerinde=False):
        try:
            self.delete("all")
            g, y, r = self._g, self._y, self._y // 2
            if self._vurgu:
                dolgu = T.VURGU_HOVER if uzerinde else T.VURGU
                self.create_oval(0, self._ust, y, self._ust + y, fill=dolgu, outline=dolgu)
                self.create_oval(g - y, self._ust, g, self._ust + y, fill=dolgu, outline=dolgu)
                self.create_rectangle(r, self._ust, g - r, self._ust + y, fill=dolgu, outline=dolgu)
                yazi = T.VURGU_YAZI
            else:
                self.create_oval(0, self._ust, y, self._ust + y, outline=T.CERCEVE_PARLAK, width=1)
                self.create_oval(g - y, self._ust, g, self._ust + y, outline=T.CERCEVE_PARLAK, width=1)
                self.create_rectangle(r, self._ust, g - r, self._ust + y, outline=T.CERCEVE_PARLAK, width=1)
                yazi = T.YAZI
            self.create_text(g // 2, self._ust + y // 2, text=self._metin,
                             fill=yazi, font=self._font)
        except Exception:
            pass

    def _bas(self, _olay=None):
        try:
            if self._komut:
                self._komut()
        except Exception:
            pass


def birincil_dugme(ebeveyn, metin, komut):
    b = tk.Button(ebeveyn, text=metin, command=komut, bg=T.VURGU, fg=T.VURGU_YAZI,
                  font=("Inter", 10, "bold"), relief="flat", padx=18, pady=7,
                  activebackground=T.VURGU_HOVER, activeforeground=T.VURGU_YAZI,
                  cursor="hand2", bd=0)
    return b


def ikincil_dugme(ebeveyn, metin, komut):
    b = tk.Button(ebeveyn, text=metin, command=komut, bg=T.YUZEY, fg=T.YAZI,
                  font=("Inter", 9), relief="flat", padx=14, pady=6, bd=0,
                  highlightthickness=1, highlightbackground=T.CERCEVE,
                  activebackground="#1C2622", activeforeground=T.YAZI, cursor="hand2")
    return b


class AdimSlider(tk.Frame):
    """Duraklı kaydırıcı: RAM gibi güvenli aralıklarda seçim.
    degerler=[(etiket, veri), ...], örn. [("2G", 2), ("3G", 3)]."""

    def __init__(self, ebeveyn, degerler, baslangic=1, komut=None, genislik=460,
                 rozet=None):
        super().__init__(ebeveyn, bg=T.KART)
        self.degerler = list(degerler)
        self.komut = komut
        self.rozet = rozet
        self.secil = max(0, min(len(self.degerler) - 1, baslangic))
        self.genislik = genislik
        self._roz_deger = tk.StringVar(value="")
        self.tuval = tk.Canvas(self, width=genislik, height=34, bg=T.KART,
                               highlightthickness=0)
        self.tuval.pack(fill="x")
        self.tuval.bind("<Button-1>", self._tik)
        self.tuval.bind("<B1-Motion>", self._tik)
        self._ciz()
        self._yansit()

    def _nokta(self, i):
        n = len(self.degerler)
        if n <= 1:
            return 18
        return 18 + i * ((self.genislik - 36) / (n - 1))

    def _ciz(self):
        c = self.tuval
        try:
            c.delete("all")
            y = 12
            c.create_line(18, y, self.genislik - 18, y, fill="#2A3530", width=3, capstyle="round")
            x1 = self._nokta(self.secil)
            c.create_line(18, y, x1, y, fill=T.VURGU, width=3, capstyle="round")
            for i, (etiket, _v) in enumerate(self.degerler):
                x = self._nokta(i)
                c.create_text(x, y + 16, text=etiket, fill=T.SILIK, font=("Inter", 8))
            c.create_oval(x1 - 7, y - 7, x1 + 7, y + 7, fill=T.VURGU, outline=T.VURGU)
        except Exception:
            pass

    def _tik(self, olay):
        try:
            n = len(self.degerler)
            oran = (olay.x - 18) / max(1, (self.genislik - 36))
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
            if self.rozet is not None:
                self.rozet.configure(text=str(self.degerler[self.secil][0]))
        except Exception:
            pass

    def deger(self):
        return self.degerler[self.secil][1]


class Anahtar(tk.Frame):
    """Açma-kapama düğmesi. acik=True/False, komut(yeni_deger)."""

    def __init__(self, ebeveyn, acik=False, komut=None, genislik=44, yukseklik=24):
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
            c.create_oval(dx, 3, dx + h - 6, h - 3, fill="#E8EEEB", outline="")
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


def ikon_ciz(ebeveyn, tur, boyut=20, renk=None, bg=None):
    """Ray ikonları: ince çizgi çizimler (dosya gerektirmez)."""
    renk = renk or T.SOLUK
    c = tk.Canvas(ebeveyn, width=boyut, height=boyut, bg=bg or T.YUZEY,
                  highlightthickness=0)
    o = boyut / 26.0
    w = max(1, int(round(1.6 * o)))

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
