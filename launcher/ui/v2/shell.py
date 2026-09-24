"""v2 kabuk: sol ray + üst bar + sayfa alanı. Sıfırdan, eski uygulamadan bağımsız."""
import tkinter as tk
from core.hizmetler import Hizmetler as _Hizmetler
from . import tokens as T
from . import widgets as W
from . import kayit


def _koyu_baslik_cubugu(pencere):
    """Windows başlık çubuğunu koyu yapar. 19 = Win10 1809, 20 = 20H1+.
    Olmazsa sessiz geçilir."""
    try:
        import ctypes
        deger = ctypes.c_int(1)
        for kod in (20, 19):
            try:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    pencere.winfo_id(), kod, ctypes.byref(deger), ctypes.sizeof(deger))
            except Exception:
                pass
    except Exception:
        pass


RAY_IKON = {
    "hub": "hub", "komutlar": "commands", "durum": "status", "konsol": "console",
    "gorevler": "quests", "yetenekler": "skills", "siralama": "ranking", "ayarlar": "settings",
}


class Hizmetler(_Hizmetler):
    """Uyumluluk katmanı: v2 kabuğu core.hizmetler.Hizmetler'ı kullanır."""
    pass


class Kabuk(tk.Tk):
    def __init__(self, kok, ayar):
        super().__init__()
        self.title("DgmCraft")
        try:
            from core import assets as _A
            _A.ikon_pencere(self)
        except Exception:
            pass
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
        try:
            self.update_idletasks()
            _koyu_baslik_cubugu(self)
        except Exception:
            pass
        self._sayfa_ac("hub")

    def _kur_rail(self):
        ray = tk.Frame(self, bg=T.YUZEY, width=T.RAY_GENISLIK)
        ray.pack(side="left", fill="y")
        ray.pack_propagate(False)
        try:
            from core import assets as _A
            logo = _A.kucult("brand", "mark-480.png", hedef=28)
            if logo:
                self._logo_ref = logo
                tk.Label(ray, image=logo, bg=T.YUZEY).pack(pady=(14, 14))
        except Exception:
            pass
        for kimlik, mod in kayit.SAYFALAR:
            b = tk.Frame(ray, bg=T.YUZEY, cursor="hand2")
            b.pack(fill="x", pady=1)
            gosterge = tk.Frame(b, bg=T.VURGU, width=2)
            govde = tk.Frame(b, bg=T.YUZEY)
            govde.pack(side="left", fill="x", expand=True)
            ikon = self._ray_ikon(govde, kimlik)
            ikon.pack(pady=(6, 1))
            etiket = tk.Label(govde, text=mod.BASLIK, font=("Inter", 7),
                              bg=T.YUZEY, fg=T.SILIK)
            etiket.pack(pady=(0, 6))
            b.bind("<Button-1>", lambda e, k=kimlik: self._sayfa_ac(k))
            for cocuk in (ikon, etiket):
                try:
                    cocuk.bind("<Button-1>", lambda e, k=kimlik: self._sayfa_ac(k))
                except Exception:
                    pass
            self._ray_dugmeler[kimlik] = {"kutu": b, "govde": govde, "gosterge": gosterge,
                                          "ikon": ikon, "etiket": etiket, "tur": kimlik}
            self._ray_boya(kimlik, False)
        alt = tk.Frame(ray, bg=T.YUZEY)
        alt.pack(side="bottom", fill="x", pady=12)
        tk.Label(alt, text=self.hizmetler.surum, font=("Inter", 8), bg=T.YUZEY, fg=T.SILIK).pack()

    def _kur_ust(self):
        ust = tk.Frame(self, bg=T.BG, height=T.UST_YUKSEKLIK)
        ust.pack(side="top", fill="x", padx=T.BOSLUK, pady=(12, 0))
        ust.pack_propagate(False)
        self._ust_baslik = tk.Label(ust, text="", font=T.FONT_SAYFA, bg=T.BG, fg=T.YAZI)
        self._ust_baslik.pack(side="left")
        sag = tk.Frame(ust, bg=T.BG)
        sag.pack(side="right")
        try:
            from core import assets as _A2
            kafa = _A2.kucult("brand", "app-icon-128.png", hedef=24)
            if kafa:
                self._kafa_ref = kafa
                tk.Label(sag, image=kafa, bg=T.BG).pack(side="left", padx=(0, 8))
        except Exception:
            pass
        tk.Label(sag, text="●", font=("Inter", 7), bg=T.BG, fg=T.YESIL).pack(side="left", padx=(0, 5))
        tk.Label(sag, text=self.hizmetler.kullanici, font=("Inter", 10), bg=T.BG,
                 fg=T.SOLUK).pack(side="left", padx=(0, 2))

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

    def _ray_boya(self, kimlik, aktif):
        oge = self._ray_dugmeler[kimlik]
        try:
            if aktif:
                oge["gosterge"].pack(side="left", fill="y")
            else:
                oge["gosterge"].pack_forget()
        except Exception:
            pass
        try:
            oge["etiket"].configure(fg=T.VURGU if aktif else T.SILIK)
        except Exception:
            pass
        self._ray_ikon_degistir(kimlik, aktif)

    def _ray_ikon(self, ebeveyn, kimlik, aktif=False):
        """PNG varsa onu (20px), yoksa çizgi ikonu. Gri/ton: aktifse amber."""
        try:
            from core import assets as _A
            ad = RAY_IKON.get(kimlik, kimlik)
            son_ad = ad + ("-aktif.png" if aktif else "-gri.png")
            img = _A.kucult("v2", "nav-icons", son_ad, hedef=T.IKON)
            if img:
                return tk.Label(ebeveyn, image=img, bg=T.YUZEY)
        except Exception:
            pass
        return W.ikon_ciz(ebeveyn, kimlik, boyut=T.IKON, renk=T.VURGU if aktif else T.SILIK)

    def _ray_ikon_degistir(self, kimlik, aktif):
        """Aktif durum değişince ikonu yeniden kurar (PNG/çizgi fark etmez)."""
        try:
            oge = self._ray_dugmeler[kimlik]
            yeni = self._ray_ikon(oge["govde"], kimlik, aktif)
            try:
                yeni.bind("<Button-1>", lambda e, k=kimlik: self._sayfa_ac(k))
            except Exception:
                pass
            yeni.pack(pady=(6, 1), before=oge["etiket"])
            try:
                oge["ikon"].destroy()
            except Exception:
                pass
            oge["ikon"] = yeni
        except Exception:
            pass

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
        for kid in self._ray_dugmeler:
            try:
                self._ray_boya(kid, kid == kimlik)
            except Exception:
                pass
        yeni = self._sayfalar[kimlik]
        try:
            self._ust_baslik.configure(text=self._sayfa_adi(kimlik))
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

    def _sayfa_adi(self, kimlik):
        for k, mod in kayit.SAYFALAR:
            if k == kimlik:
                return getattr(mod, "BASLIK", kimlik)
        return kimlik
