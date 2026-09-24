"""v2 kabuk: sol ray + üst bar + sayfa alanı. Sıfırdan, eski uygulamadan bağımsız."""
import tkinter as tk
from . import tokens as T
from . import widgets as W
from . import kayit


class Hizmetler:
    def __init__(self, kok, ayar):
        self.kok = kok
        self.ayar = ayar
        try:
            self.kullanici = (ayar.get("kullaniciAdi") or "").strip() or "Oyuncu"
        except Exception:
            self.kullanici = "Oyuncu"
        try:
            from core import version as _V
            self.surum = _V.oku().get("surum", "?")
        except Exception:
            self.surum = "?"


class Kabuk(tk.Tk):
    def __init__(self, kok, ayar):
        super().__init__()
        self.title("DgmCraft")
        self.hizmetler = Hizmetler(kok, ayar)
        try:
            x = (self.winfo_screenwidth() - T.GENISLIK) // 2
            y = max(0, (self.winfo_screenheight() - T.YUKSEKLIK) // 2 - 20)
            self.geometry("%dx%d+%d+%d" % (T.GENISLIK, T.YUKSEKLIK, x, y))
        except Exception:
            self.geometry("%dx%d" % (T.GENISLIK, T.YUKSEKLIK))
        self.resizable(False, False)
        self.configure(bg=T.BG)
        self._sayfalar = {}
        self._aktif = None
        self._ray_dugmeler = {}
        self._kur_rail()
        self._kur_ust()
        self._kur_icerik()
        self._sayfa_ac("hub")

    def _kur_rail(self):
        ray = tk.Frame(self, bg=T.YUZEY, width=T.RAY_GENISLIK)
        ray.pack(side="left", fill="y")
        ray.pack_propagate(False)
        try:
            from core import assets as _A
            logo = _A.foto("brand", "mark-480.png")
            if logo:
                try:
                    kucuk = logo.subsample(10, 10)
                    self._logo_ref = kucuk
                    tk.Label(ray, image=kucuk, bg=T.YUZEY).pack(pady=(14, 18))
                except Exception:
                    pass
        except Exception:
            pass
        for kimlik, mod in kayit.SAYFALAR:
            b = tk.Frame(ray, bg=T.YUZEY, cursor="hand2")
            b.pack(fill="x", pady=2)
            ikon = W.ikon_ciz(b, kimlik, boyut=26)
            ikon.pack(pady=(8, 2))
            tk.Label(b, text=mod.BASLIK, font=("Inter", 8), bg=T.YUZEY, fg=T.SOLUK).pack(pady=(0, 8))
            b.bind("<Button-1>", lambda e, k=kimlik: self._sayfa_ac(k))
            for cocuk in (ikon, b.winfo_children()[1]):
                try:
                    cocuk.bind("<Button-1>", lambda e, k=kimlik: self._sayfa_ac(k))
                except Exception:
                    pass
            self._ray_dugmeler[kimlik] = b
        alt = tk.Frame(ray, bg=T.YUZEY)
        alt.pack(side="bottom", fill="x", pady=12)
        tk.Label(alt, text=self.hizmetler.surum, font=("Inter", 8), bg=T.YUZEY, fg=T.SILIK).pack()

    def _kur_ust(self):
        ust = tk.Frame(self, bg=T.BG, height=T.UST_YUKSEKLIK)
        ust.pack(side="top", fill="x", padx=T.BOSLUK, pady=(12, 0))
        ust.pack_propagate(False)
        self._ust_baslik = tk.Label(ust, text="", font=T.FONT_DEV, bg=T.BG, fg=T.YAZI)
        self._ust_baslik.pack(side="left")
        sag = tk.Frame(ust, bg=T.BG)
        sag.pack(side="right")
        try:
            from core import assets as _A2
            kafa = _A2.foto("brand", "app-icon-128.png")
            if kafa:
                try:
                    minik = kafa.subsample(4, 4)
                    self._kafa_ref = minik
                    tk.Label(sag, image=minik, bg=T.BG).pack(side="left", padx=(0, 8))
                except Exception:
                    pass
        except Exception:
            pass
        tk.Label(sag, text=self.hizmetler.kullanici, font=T.FONT_BASLIK, bg=T.BG, fg=T.YAZI).pack(side="left")

    def _kur_icerik(self):
        self._icerik = tk.Frame(self, bg=T.BG)
        self._icerik.pack(side="left", fill="both", expand=True, padx=T.BOSLUK, pady=T.BOSLUK)
        for kimlik, mod in kayit.SAYFALAR:
            sinif = getattr(mod, [n for n in dir(mod) if n.endswith("Sayfasi")][0])
            ornek = sinif(self.hizmetler)
            cerceve = ornek.kur(self._icerik)
            try:
                cerceve.pack_forget()
            except Exception:
                pass
            self._sayfalar[kimlik] = ornek

    def _sayfa_ac(self, kimlik):
        if kimlik == self._aktif:
            return
        try:
            if self._aktif and self._aktif in self._sayfalar:
                eski = self._sayfalar[self._aktif]
                try:
                    eski.gizle()
                except Exception:
                    pass
                try:
                    eski.cerceve.pack_forget()
                except Exception:
                    pass
        except Exception:
            pass
        self._aktif = kimlik
        for kid, dugme in self._ray_dugmeler.items():
            try:
                dugme.configure(bg=T.VURGU if kid == kimlik else T.YUZEY)
            except Exception:
                pass
        yeni = self._sayfalar[kimlik]
        try:
            self._ust_baslik.configure(text=yeni.BASLIK if hasattr(yeni, "BASLIK") else kimlik)
        except Exception:
            pass
        try:
            yeni.cerceve.pack(fill="both", expand=True)
        except Exception:
            pass
        try:
            yeni.goster()
        except Exception:
            pass
