"""Tek seferlik kurulum ekranı: animasyonlu ilerleme + kısayol + devir.
Worker -> UI kuyruk + ana thread pompa (Tcl tek thread)."""
import os
import queue
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from core import kurulum as K
from core import assets
from ui import theme as TEMA


class KurulumPenceresi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DgmCraft Kurulum")
        try:
            w, h = 560, 560
            x = (self.winfo_screenwidth() - w) // 2
            y = max(0, (self.winfo_screenheight() - h) // 2 - 20)
            self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        except Exception:
            self.geometry("560x560")
        self.resizable(False, False)
        TEMA.uygula(self)
        assets.ikon_pencere(self)
        self.sonuc = "vazgecti"
        self._kuyruk = queue.Queue()
        self._mesgul = False
        dis = tk.Frame(self, bg=TEMA.BG)
        dis.pack(fill="both", expand=True, padx=36, pady=28)
        self._ikon_img = assets.foto("brand", "app-icon-128.png")
        if self._ikon_img:
            tk.Label(dis, image=self._ikon_img, bg=TEMA.BG).pack(pady=(6, 4))
        else:
            tk.Label(dis, text="📦", font=("Segoe UI", 44), bg=TEMA.BG).pack(pady=(6, 4))
        tk.Label(dis, text="DgmCraft kuruluyor", font=("Segoe UI", 22, "bold"),
                 bg=TEMA.BG, fg=TEMA.YAZI).pack()
        tk.Label(dis, text="Tek seferlik. Dosyalar AppData'ya kopyalanıyor, Masaüstüne kısayol konuyor.",
                 font=TEMA.FONT_NORMAL, bg=TEMA.BG, fg=TEMA.SOLUK,
                 wraplength=460, justify="center").pack(pady=(6, 14))
        self.adim_vars = []
        for metin in ("Dosyalar kopyalanıyor", "Kısayollar oluşturuluyor", "Uygulama başlatılıyor"):
            var = tk.StringVar(value="○  " + metin)
            tk.Label(dis, textvariable=var, font=("Segoe UI", 12), bg=TEMA.BG, fg=TEMA.SOLUK,
                     anchor="w").pack(fill="x", pady=3)
            self.adim_vars.append(var)
        self.bar = ttk.Progressbar(dis, maximum=100, length=460, style="Amber.Horizontal.TProgressbar")
        self.bar.pack(fill="x", pady=(16, 6))
        self.durum_var = tk.StringVar(value="Hazır olduğunda Kur ve Başlat'a bas.")
        tk.Label(dis, textvariable=self.durum_var, font=TEMA.FONT_NORMAL, bg=TEMA.BG,
                 fg=TEMA.SOLUK, wraplength=460, justify="center").pack(pady=(0, 14))
        alt = tk.Frame(dis, bg=TEMA.BG)
        alt.pack(fill="x")
        self.kur_btn = ttk.Button(alt, text="Kur ve Başlat", command=self._kur_bas, style="Primary.TButton")
        self.kur_btn.pack(side="right")
        ttk.Button(alt, text="Taşınabilir Kullan", command=self._tasinabilir, style="Secondary.TButton").pack(side="left")
        self.after(150, self._pompa)
        self.protocol("WM_DELETE_WINDOW", self._vazgec)

    # kuyruk
    def _ui(self, fn, *args):
        try:
            self._kuyruk.put_nowait((fn, args))
        except Exception:
            pass

    def _pompa(self):
        try:
            while True:
                fn, args = self._kuyruk.get_nowait()
                try:
                    fn(*args)
                except Exception:
                    pass
        except queue.Empty:
            pass
        except Exception:
            pass
        try:
            if self.winfo_exists():
                self.after(150, self._pompa)
        except Exception:
            pass

    def _adim(self, i, durum):
        # durum: calisiyor | tamam | hata
        adlar = ("Dosyalar kopyalanıyor", "Kısayollar oluşturuluyor", "Uygulama başlatılıyor")
        isaret, renk = {"calisiyor": ("◉  ", TEMA.AMBER_HI), "tamam": ("●  ", TEMA.YESIL),
                        "hata": ("●  ", TEMA.KIRMIZI)}.get(durum, ("○  ", TEMA.SOLUK))
        try:
            self.adim_vars[i].set(isaret + adlar[i])
        except Exception:
            pass

    def _vazgec(self):
        self.sonuc = "vazgecti"
        try:
            self.destroy()
        except Exception:
            pass

    def _tasinabilir(self):
        if self._mesgul:
            return
        try:
            K.marker_yaz({"durum": "tasinabilir"})
        except Exception:
            pass
        self.sonuc = "tasinabilir"
        try:
            self.destroy()
        except Exception:
            pass

    def _kur_bas(self):
        if self._mesgul:
            return
        self._mesgul = True
        try:
            self.kur_btn.configure(state="disabled")
        except Exception:
            pass
        threading.Thread(target=self._kur, daemon=True).start()

    def _kur(self):
        try:
            kaynak = K.exe_dizini()
            hedef = K.hedef_dizin()
            if not K.bosta_alan_var(kaynak):
                self._ui(self._hata, "Diskte yeterli boş alan yok.")
                return
            self._ui(self._adim, 0, "calisiyor")
            self._ui(self.durum_var.set, "Dosyalar kopyalanıyor...")

            def _ilerleme(oran):
                try:
                    self.bar.configure(value=oran * 100)
                except Exception:
                    pass

            K.kopyala(kaynak, hedef, ilerleme=lambda o: self._ui(_ilerleme, o))
            self._ui(self._adim, 0, "tamam")
            self._ui(self._adim, 1, "calisiyor")
            self._ui(self.durum_var.set, "Kısayollar oluşturuluyor...")
            n = K.kisayol_olustur(os.path.join(hedef, K.UYGULAMA_ADI))
            self._ui(self._adim, 1, "tamam" if n else "hata")
            try:
                K.marker_yaz({"durum": "kurulu", "yol": hedef})
            except Exception:
                pass
            self._ui(self._adim, 2, "calisiyor")
            self._ui(self.durum_var.set, "Uygulama başlatılıyor...")
            K.kurulu_exe_baslat()
            self._ui(self._adim, 2, "tamam")
            self._ui(self._bitir_kapat)
        except Exception as e:
            self._ui(self._hata, str(e)[:300])

    def _hata(self, metin):
        try:
            self.bar.configure(value=0)
        except Exception:
            pass
        self._mesgul = False
        try:
            self.kur_btn.configure(state="normal")
        except Exception:
            pass
        self.durum_var.set("Kurulum başarısız: " + metin)
        messagebox.showerror("Kurulum hatası", metin)

    def _bitir_kapat(self):
        self.sonuc = "kuruldu"
        try:
            self.destroy()
        except Exception:
            pass
