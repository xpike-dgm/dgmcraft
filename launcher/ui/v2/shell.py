"""v2 kabuk: sol ray + üst bar + sayfa alanı. Sıfırdan, eski uygulamadan bağımsız."""
import tkinter as tk
from . import tokens as T
from . import widgets as W
from . import kayit


def _koyu_baslik_cubugu(pencere):
    """Windows başlık çubuğunu koyu yapar (10 20H1+). Olmazsa sessiz geçilir."""
    try:
        import ctypes
        deger = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            pencere.winfo_id(), 20, ctypes.byref(deger), ctypes.sizeof(deger))
    except Exception:
        pass


RAY_IKON = {
    "hub": "hub", "komutlar": "commands", "durum": "status", "konsol": "console",
    "gorevler": "quests", "yetenekler": "skills", "siralama": "ranking", "ayarlar": "settings",
}


class Hizmetler:
    def __init__(self, kok, ayar):
        import queue as _q
        self.kok = kok
        self.ayar = ayar
        self.log_kuyrugu = _q.Queue(maxsize=5000)
        self.sunucu = None
        try:
            self.kullanici = (ayar.get("kullaniciAdi") or "").strip() or "Oyuncu"
        except Exception:
            self.kullanici = "Oyuncu"
        try:
            from core import version as _V
            self.surum = _V.oku().get("surum", "?")
        except Exception:
            self.surum = "?"

    def sunucu_al(self):
        if self.sunucu is None:
            from core import sunucu as _S
            self.sunucu = _S.SunucuYoneticisi(self.kok, self.log_kuyrugu)
        return self.sunucu

    def heap_al(self):
        try:
            return max(1, min(16, int(self.ayar.get("heapGB", 3))))
        except Exception:
            return 3

    def heap_kaydet(self, gb):
        try:
            self.ayar["heapGB"] = max(1, min(16, int(gb)))
            from core import store as _ST
            _ST.kaydet(self.ayar)
        except Exception:
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
            gosterge = tk.Frame(b, bg=T.VURGU, width=3)
            govde = tk.Frame(b, bg=T.YUZEY)
            govde.pack(side="left", fill="x", expand=True)
            ikon = self._ray_ikon(govde, kimlik)
            ikon.pack(pady=(8, 2))
            etiket = tk.Label(govde, text=mod.BASLIK, font=("Inter", 8), bg=T.YUZEY, fg=T.SOLUK)
            etiket.pack(pady=(0, 8))
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
                    tk.Label(sag, image=minik, bg=T.BG).pack(side="left", padx=(0, 10))
                except Exception:
                    pass
        except Exception:
            pass
        tk.Label(sag, text="●", font=("Inter", 10), bg=T.BG, fg=T.YESIL).pack(side="left", padx=(0, 6))
        tk.Label(sag, text=self.hizmetler.kullanici, font=T.FONT_BASLIK, bg=T.BG, fg=T.YAZI).pack(side="left", padx=(0, 4))

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
        renk = T.VURGU if aktif else T.SOLUK
        try:
            if aktif:
                oge["gosterge"].pack(side="left", fill="y")
            else:
                oge["gosterge"].pack_forget()
        except Exception:
            pass
        try:
            # PNG ikonlar sabit kalır; yalnızca çizgi ikonlar yeniden boyanır.
            if isinstance(oge["ikon"], tk.Canvas):
                oge["ikon"].destroy()
                yeni_ikon = W.ikon_ciz(oge["govde"], oge["tur"], boyut=26, renk=renk)
                try:
                    yeni_ikon.bind("<Button-1>", lambda e, k=kimlik: self._sayfa_ac(k))
                except Exception:
                    pass
                yeni_ikon.pack(pady=(8, 2), before=oge["etiket"])
                oge["ikon"] = yeni_ikon
        except Exception:
            pass
        try:
            oge["etiket"].configure(fg=T.VURGU if aktif else T.SOLUK)
        except Exception:
            pass

    def _ray_ikon(self, ebeveyn, kimlik, renk=None):
        """PNG varsa onu, yoksa çizgi ikonu kullanır."""
        try:
            from core import assets as _A
            ad = RAY_IKON.get(kimlik, kimlik)
            img = _A.foto("v2", "nav-icons", ad + ".png")
            if img:
                return tk.Label(ebeveyn, image=img, bg=T.YUZEY)
        except Exception:
            pass
        return W.ikon_ciz(ebeveyn, kimlik, boyut=26, renk=renk)

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
