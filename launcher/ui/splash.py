"""Açılış splash'i: marka arka planı + logo + ilerleme. Hata verirse sessiz geçilir."""
import tkinter as tk
from tkinter import ttk
from core import assets
from ui import theme as TEMA


class Splash(tk.Tk):
    def __init__(self, surum=""):
        super().__init__()
        self.title("DgmCraft")
        assets.ikon_pencere(self)
        try:
            w, h = 800, 500
            x = (self.winfo_screenwidth() - w) // 2
            y = max(0, (self.winfo_screenheight() - h) // 2 - 30)
            self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        except Exception:
            self.geometry("800x500")
        self.resizable(False, False)
        TEMA.uygula(self)
        self.configure(bg="#0B0F0E")
        self.overrideredirect(False)
        self._bg_img = assets.foto("splash", "splash-bg-800.png")
        if self._bg_img:
            tk.Label(self, image=self._bg_img, bg="#0B0F0E").place(x=0, y=0, relwidth=1, relheight=1)
        orta = tk.Frame(self, bg="#0B0F0E")
        orta.place(relx=0.5, rely=0.42, anchor="center")
        self._logo_img = assets.foto("brand", "logo-horizontal-w360.png")
        if self._logo_img:
            tk.Label(orta, image=self._logo_img, bg="#0B0F0E").pack()
        else:
            tk.Label(orta, text="DGM CRAFT", font=("Segoe UI", 28, "bold"),
                     bg="#0B0F0E", fg=TEMA.YAZI).pack()
        self.durum_var = tk.StringVar(value="Hazırlanıyor...")
        tk.Label(orta, textvariable=self.durum_var, font=TEMA.FONT_NORMAL,
                 bg="#0B0F0E", fg=TEMA.SOLUK).pack(pady=(10, 0))
        self.bar = ttk.Progressbar(self, mode="indeterminate", style="Amber.Horizontal.TProgressbar")
        self.bar.place(relx=0.5, rely=0.88, anchor="center", relwidth=0.6)
        try:
            self.bar.start(12)
        except Exception:
            pass
        tk.Label(self, text="Sürüm %s" % (surum or "?"), font=TEMA.FONT_KUCUK,
                 bg="#0B0F0E", fg=TEMA.SOLUK2).place(relx=0.5, rely=0.95, anchor="center")

    def mesaj(self, metin):
        try:
            self.durum_var.set(metin)
            self.update_idletasks()
        except Exception:
            pass

    def kapat(self):
        try:
            self.bar.stop()
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass
