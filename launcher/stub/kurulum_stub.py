"""DgmCraft bootstrapper: tek dosyalık mini kurulum exe'si.
Akış: indir (latest) -> SHA256 doğrula -> AppData'ya çıkar -> kısayol -> başlat.
Yarım kalan kurulum çöpe atılır, bozuk paket asla çalıştırılmaz. Yalnızca stdlib."""
import hashlib
import os
import queue
import shutil
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

INDIR_ADRES = "https://github.com/xpike-dgm/dgmcraft/releases/latest/download/DgmCraft-windows.zip"
OZET_ADRES = INDIR_ADRES + ".sha256"

BG = "#0B0F0E"
YAZI = "#F2F5F3"
SOLUK = "#9AA8A0"
AMBER = "#F0A202"


def _appdata():
    return os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")


HEDEF_DIZIN = os.path.join(_appdata(), "DgmCraft", "App")
HEDEF_EXE = os.path.join(HEDEF_DIZIN, "DgmCraft.exe")


class StubPencere(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DgmCraft Kurulum")
        try:
            from core import assets as _A
            _A.ikon_pencere(self)
        except Exception:
            pass
        try:
            w, h = 560, 600
            x = (self.winfo_screenwidth() - w) // 2
            y = max(0, (self.winfo_screenheight() - h) // 2 - 20)
            self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        except Exception:
            self.geometry("560x600")
        self.resizable(False, False)
        self.configure(bg=BG)
        try:
            st = ttk.Style(self)
            st.theme_use("clam")
            st.configure("Amber.Horizontal.TProgressbar", background=AMBER,
                         troughcolor="#141B19", borderwidth=0, thickness=12)
        except Exception:
            pass
        self._kuyruk = queue.Queue()
        self._iptal = False
        try:
            from core import assets as _A2
            self._bg_img = _A2.foto("splash", "splash-bg-800.png")
            if self._bg_img:
                tk.Label(self, image=self._bg_img, bg=BG).place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            pass
        kart = tk.Frame(self, bg="#101615", highlightthickness=1, highlightbackground="#26332E")
        kart.place(relx=0.5, rely=0.52, anchor="center", width=460, height=460)
        try:
            from core import assets as _A3
            self._logo_img = _A3.foto("brand", "app-icon-128.png")
            if self._logo_img:
                tk.Label(kart, image=self._logo_img, bg="#101615").pack(pady=(22, 6))
        except Exception:
            pass
        tk.Label(kart, text="DGM CRAFT", font=("Segoe UI", 22, "bold"), bg="#101615", fg=YAZI).pack()
        tk.Label(kart, text="Kurulum", font=("Segoe UI", 12), bg="#101615", fg=AMBER).pack(pady=(0, 10))
        self.durum_var = tk.StringVar(value="Hazır olduğunda Kur'a bas.")
        tk.Label(kart, textvariable=self.durum_var, font=("Segoe UI", 11), bg="#101615", fg=SOLUK,
                 wraplength=400, justify="center").pack(pady=(0, 10))
        self.bar = ttk.Progressbar(kart, maximum=100, style="Amber.Horizontal.TProgressbar")
        self.bar.pack(fill="x", padx=30, pady=(0, 16))
        alt = tk.Frame(kart, bg="#101615")
        alt.pack(fill="x", padx=30, pady=(0, 20))
        self.kur_btn = tk.Button(alt, text="Kur", command=self._kur_bas, bg=AMBER, fg="#1A1000",
                                 font=("Segoe UI", 11, "bold"), relief="flat", padx=24, pady=8)
        self.kur_btn.pack(side="right")
        tk.Button(alt, text="Kapat", command=self._kapat, bg="#223029", fg="#E8EEEA",
                  font=("Segoe UI", 10), relief="flat", padx=18, pady=8).pack(side="left")
        tk.Label(self, text="Sürüm: DgmCraft Kurulum", font=("Segoe UI", 8), bg=BG, fg="#6E7F76").place(relx=0.5, rely=0.97, anchor="center")
        self.after(150, self._pompa)
        self.protocol("WM_DELETE_WINDOW", self._kapat)

    def _ui(self, fn, *args, **kwargs):
        try:
            self._kuyruk.put_nowait((fn, args, kwargs))
        except Exception:
            pass

    def _pompa(self):
        try:
            while True:
                fn, args, kwargs = self._kuyruk.get_nowait()
                try:
                    fn(*args, **kwargs)
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

    def _kapat(self):
        self._iptal = True
        try:
            self.destroy()
        except Exception:
            pass

    def _kur_bas(self):
        try:
            self.kur_btn.configure(state="disabled")
        except Exception:
            pass
        if os.path.isfile(HEDEF_EXE):
            if not messagebox.askyesno("Zaten kurulu", "DgmCraft zaten kurulu görünüyor. Üstüne temiz kurulum yapılsın mı?"):
                try:
                    self.kur_btn.configure(state="normal")
                except Exception:
                    pass
                return
        threading.Thread(target=self._kur, daemon=True).start()

    def _durum(self, metin):
        self._ui(self.durum_var.set, metin)

    def _oran(self, deger):
        self._ui(self.bar.configure, value=deger)

    def _kur(self):
        staging = None
        try:
            self._durum("Paket indiriliyor...")
            staging = tempfile.mkdtemp(prefix="dgm-stub-")
            zip_yolu = os.path.join(staging, "paket.zip")
            self._indir(INDIR_ADRES, zip_yolu)
            if self._iptal:
                return
            self._durum("Paket doğrulanıyor...")
            beklenen = self._metin_indir(OZET_ADRES).split()[0]
            gercek = self._sha256(zip_yolu)
            if beklenen != gercek:
                raise ValueError("Doğrulama tutmadı (bozuk indirme). Tekrar dene.")
            self._durum("Kuruluyor...")
            self._ui(self.bar.configure, value=100)
            if os.path.isdir(HEDEF_DIZIN):
                shutil.rmtree(HEDEF_DIZIN, ignore_errors=True)
            os.makedirs(HEDEF_DIZIN, exist_ok=True)
            import zipfile
            with zipfile.ZipFile(zip_yolu, "r") as z:
                z.extractall(HEDEF_DIZIN)
            if not os.path.isfile(HEDEF_EXE):
                raise ValueError("Paket hatalı (exe bulunamadı).")
            self._durum("Kısayollar oluşturuluyor...")
            try:
                from core import kurulum as _K
                _K.kisayol_olustur(HEDEF_EXE)
                _K.marker_yaz({"durum": "kurulu", "yol": HEDEF_DIZIN})
            except Exception:
                pass
            self._durum("Başlatılıyor...")
            import subprocess
            subprocess.Popen([HEDEF_EXE])
            self._ui(self._bitir)
        except Exception as e:
            self._ui(self._hata, str(e)[:300])
        finally:
            if staging:
                try:
                    shutil.rmtree(staging, ignore_errors=True)
                except Exception:
                    pass

    def _indir(self, url, hedef):
        req = urllib.request.Request(url, headers={"User-Agent": "DgmCraft-Kurulum"})
        with urllib.request.urlopen(req, timeout=30) as r:
            toplam = int(r.headers.get("Content-Length", "0") or 0)
            okunan = 0
            with open(hedef, "wb") as f:
                while True:
                    if self._iptal:
                        raise InterruptedError("İptal edildi.")
                    parca = r.read(512 * 1024)
                    if not parca:
                        break
                    f.write(parca)
                    okunan += len(parca)
                    if toplam:
                        self._oran(okunan / toplam * 100)

    def _metin_indir(self, url):
        req = urllib.request.Request(url, headers={"User-Agent": "DgmCraft-Kurulum"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="replace").strip()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValueError("Doğrulama dosyası yok (eski sürüm). Yeni sürümü bekle.")
            raise

    def _sha256(self, yol):
        h = hashlib.sha256()
        with open(yol, "rb") as f:
            while True:
                parca = f.read(1024 * 1024)
                if not parca:
                    break
                h.update(parca)
        return h.hexdigest()

    def _hata(self, metin):
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return
        if self._iptal:
            return
        try:
            self.bar.configure(value=0)
        except Exception:
            pass
        try:
            self.kur_btn.configure(state="normal")
        except Exception:
            pass
        self.durum_var.set("Kurulum başarısız: " + metin)
        messagebox.showerror("Kurulum hatası", metin)

    def _bitir(self):
        try:
            self.destroy()
        except Exception:
            pass


def main():
    w = StubPencere()
    w.mainloop()


if __name__ == "__main__":
    main()
