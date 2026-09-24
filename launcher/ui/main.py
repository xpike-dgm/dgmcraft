"""Ana ekran: durum, Başlat/Katıl, log, komut, Site, Yedek, Ayarlar."""
import queue
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import os
import subprocess
from core import store, sunucu, kilit, esitleme, vpn, site, version, bootstrap, guncelleme, assets
from core import ai as YARDIMCI
from core import constants as C
from core import paths as P
from ui import texts as T
from ui import theme as TEMA


class AnaPencere(tk.Tk):
    def __init__(self, sunucu_koku, ayar):
        super().__init__()
        self.title("DgmCraft Sunucu Başlatıcı")
        assets.ikon_pencere(self)
        try:
            w, h = 980, 700
            x = (self.winfo_screenwidth() - w) // 2
            y = max(0, (self.winfo_screenheight() - h) // 2 - 20)
            self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        except Exception:
            self.geometry("980x700")
        self.resizable(False, False)
        self.kok = sunucu_koku
        self.ayar = ayar
        self.log_q = queue.Queue(maxsize=5000)
        # Worker thread -> UI güncellemeleri için kuyruk (Tcl tek thread).
        self._ui_kuyrugu = queue.Queue(maxsize=500)
        self.sunucu = sunucu.SunucuYoneticisi(sunucu_koku, self.log_q)
        self.sync = esitleme.SyncthingYonetici(sunucu_koku)
        self.site_srv = site.SiteSunucusu(sunucu_koku, self.sunucu.komut_gonder)
        self.kalp = kilit.KalpAtisi(sunucu_koku)
        self.host_mod = False
        self.durum_var = tk.StringVar(value=T.DURUM_KAPALI)
        self.katil_var = tk.StringVar(value="")
        self.sync_var = tk.StringVar(value="Eşitleme: denetleniyor...")
        self.vpn_var = tk.StringVar(value="VPN: denetleniyor...")
        self._guncelle_penceresi = None
        self._otomatik_acilan_surum = ""
        self._arayuz()
        self._yaz_ana("DGM Craft konsolu hazır.\nSunucuyu başlatınca çıktılar burada renklenecek.\n")
        self.after(500, self._log_pompa)
        self.after(2000, self._periyodik)
        self.after(800, self._nokta_pompa)
        self.protocol("WM_DELETE_WINDOW", self._kapanis_sor)
        self._ilk_kilit_kontrol()

    def _arayuz(self):
        TEMA.uygula(self)
        # --- üst bar ---
        head = tk.Frame(self, bg=TEMA.PANEL)
        head.pack(fill="x")
        sol = tk.Frame(head, bg=TEMA.PANEL)
        sol.pack(side="left", padx=16, pady=12)
        logo = tk.Frame(sol, bg=TEMA.PANEL)
        logo.pack(anchor="w")
        self._logo_img = assets.foto("brand", "logo-horizontal-h40.png")
        if self._logo_img:
            tk.Label(logo, image=self._logo_img, bg=TEMA.PANEL).pack(side="left")
        else:
            tk.Label(logo, text="DGM", font=TEMA.FONT_BASLIK, bg=TEMA.PANEL, fg=TEMA.YAZI).pack(side="left")
            tk.Label(logo, text="CRAFT", font=TEMA.FONT_BASLIK, bg=TEMA.PANEL, fg=TEMA.AMBER).pack(side="left")
        tk.Label(sol, text="Sunucu Başlatıcı", font=TEMA.FONT_KUCUK, bg=TEMA.PANEL, fg=TEMA.SOLUK).pack(anchor="w")
        self._img_running = assets.foto("illustrations", "server-running-40.png")
        self._img_stopped = assets.foto("illustrations", "server-stopped-40.png")
        sag = tk.Frame(head, bg=TEMA.PANEL)
        sag.pack(side="right", padx=16, pady=12)
        self.nokta_lbl = tk.Label(sag, text="●", font=("Segoe UI", 16), bg=TEMA.PANEL, fg=TEMA.SOLUK2)
        self.nokta_lbl.pack(side="left", padx=(0, 6))
        self._nokta_acik = True
        self.durum_img = tk.Label(sag, bg=TEMA.PANEL)
        self.durum_img.pack(side="left", padx=(0, 6))
        try:
            if self._img_stopped:
                self.durum_img.configure(image=self._img_stopped)
        except Exception:
            pass
        self.durum_lbl = tk.Label(sag, textvariable=self.durum_var, font=TEMA.FONT_ROZET, bg=TEMA.PANEL, fg=TEMA.YAZI)
        self.durum_lbl.pack(side="left", padx=(10, 0))
        tk.Label(sag, textvariable=self.vpn_var, font=TEMA.FONT_KUCUK, bg=TEMA.PANEL, fg=TEMA.SOLUK).pack(side="left", padx=(12, 0))
        TEMA.ayirici(self)
        # --- bilgi şeridi ---
        bilgi = tk.Frame(self, bg=TEMA.BG)
        bilgi.pack(fill="x", padx=16, pady=(10, 0))
        tk.Label(bilgi, textvariable=self.katil_var, font=("Segoe UI", 10, "bold"), bg=TEMA.BG, fg=TEMA.MAVI).pack(side="left")
        tk.Label(bilgi, textvariable=self.sync_var, font=TEMA.FONT_KUCUK, bg=TEMA.BG, fg=TEMA.SOLUK).pack(side="right")
        tk.Label(self, text=T.SINIRLI_NOT, font=TEMA.FONT_KUCUK, bg=TEMA.BG, fg=TEMA.SOLUK2).pack(anchor="w", padx=16)
        # --- istatistik kartları ---
        kartlar = tk.Frame(self, bg=TEMA.BG)
        kartlar.pack(fill="x", padx=16, pady=(10, 0))
        self.kart_durum_var = tk.StringVar(value="Kapalı")
        self.kart_eslesme_var = tk.StringVar(value="—")
        self.kart_vpn_var = tk.StringVar(value="—")
        self.kart_surum_var = tk.StringVar(value="—")
        for baslik, var in (("Durum", self.kart_durum_var), ("Eşitleme", self.kart_eslesme_var),
                            ("VPN", self.kart_vpn_var), ("Sürüm", self.kart_surum_var)):
            k = tk.Frame(kartlar, bg=TEMA.KART, highlightthickness=1, highlightbackground=TEMA.BORDER_YUMUSAK)
            k.pack(side="left", fill="x", expand=True, padx=(0, 8))
            tk.Label(k, text=baslik.upper(), font=("Segoe UI", 8, "bold"), bg=TEMA.KART, fg=TEMA.SOLUK2).pack(anchor="w", padx=10, pady=(8, 0))
            tk.Label(k, textvariable=var, font=("Segoe UI", 13, "bold"), bg=TEMA.KART, fg=TEMA.YAZI).pack(anchor="w", padx=10, pady=(0, 8))
        try:
            self.kart_surum_var.set((version.oku().get("surum") or "—")[:24])
        except Exception:
            pass
        # --- eylemler ---
        btn = tk.Frame(self, bg=TEMA.BG)
        btn.pack(fill="x", padx=12, pady=10)
        self.baslat_btn = ttk.Button(btn, text=T.BASLAT, command=self._baslat_akisi, style="Primary.TButton")
        self.baslat_btn.pack(side="left", padx=4)
        ttk.Button(btn, text=T.KAPAT_GUVENLI, command=self._guvenli_kapat_akisi, style="Secondary.TButton").pack(side="left", padx=4)
        ttk.Button(btn, text="Zorla Kapat", command=self._zorla, style="Danger.TButton").pack(side="left", padx=4)
        ttk.Button(btn, text=T.SITE_AC, command=self._site_ac, style="Secondary.TButton").pack(side="left", padx=4)
        ttk.Button(btn, text=T.YEDEK_AL, command=self._yedek, style="Secondary.TButton").pack(side="left", padx=4)
        self.guncelle_btn = ttk.Button(btn, text="Güncelleme", command=self._guncelle_pencere_ac, style="Primary.TButton")
        ttk.Button(btn, text="Ayarlar", command=self._ayarlar, style="Secondary.TButton").pack(side="right", padx=4)
        # --- konsol kartı ---
        kart = tk.Frame(self, bg=TEMA.KART, highlightthickness=1, highlightbackground=TEMA.BORDER_YUMUSAK)
        kart.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        kart_bas = tk.Frame(kart, bg=TEMA.KART)
        kart_bas.pack(fill="x", padx=10, pady=(8, 4))
        tk.Label(kart_bas, text="KONSOL", font=("Segoe UI", 9, "bold"), bg=TEMA.KART, fg=TEMA.SOLUK).pack(side="left")
        self.otomatik_kaydir_var = tk.BooleanVar(value=True)
        oto = tk.Checkbutton(kart_bas, text="Otomatik kaydır", variable=self.otomatik_kaydir_var,
                             bg=TEMA.KART, fg=TEMA.SOLUK, selectcolor=TEMA.KART2,
                             activebackground=TEMA.KART, activeforeground=TEMA.YAZI, font=TEMA.FONT_KUCUK)
        oto.pack(side="right", padx=(0, 8))
        ttk.Button(kart_bas, text="Temizle", command=self._log_temizle, style="Secondary.TButton").pack(side="right")
        self.log_alani = TEMA.konsol(kart, height=20)
        self.log_alani.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for ad, renk in (("hata", "#FF8A8A"), ("uyari", TEMA.AMBER_HI), ("giris", TEMA.YESIL),
                         ("cikis", TEMA.SOLUK), ("komut", TEMA.MAVI), ("soluk", TEMA.SOLUK2)):
            try:
                self.log_alani.tag_configure(ad, foreground=renk)
            except Exception:
                pass
        self.log_alani.configure(state="disabled")
        # --- komut satırı ---
        alt = tk.Frame(self, bg=TEMA.BG)
        alt.pack(fill="x", padx=16, pady=(0, 6))
        self.komut_var = tk.StringVar()
        giris = TEMA.giris(alt, textvariable=self.komut_var)
        giris.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=6)
        ttk.Button(alt, text="Gönder", command=self._komut, style="Primary.TButton").pack(side="left")
        ttk.Button(alt, text="AI Yardım", command=self._ai_yardim, style="Secondary.TButton").pack(side="left", padx=(8, 0))
        self.komut_var.set("")
        # --- alt bilgi ---
        try:
            surum = version.oku().get("surum", "?")
        except Exception:
            surum = "?"
        tk.Label(self, text="Sürüm %s  •  Kapatma düğmesi sunucuyu ÖLDÜRMEZ (simgeye alır ya da güvenli kapatır)" % surum,
                 font=TEMA.FONT_KUCUK, bg=TEMA.BG, fg=TEMA.SOLUK2).pack(pady=(0, 10))
        self.bind("<Return>", lambda e: self._komut())

    def _durum_gorsel(self, calisiyor):
        try:
            img = self._img_running if calisiyor else self._img_stopped
            if img:
                self.durum_img.configure(image=img)
        except Exception:
            pass

    def _log_temizle(self):
        try:
            self.log_alani.configure(state="normal")
            self.log_alani.delete("1.0", "end")
            self.log_alani.configure(state="disabled")
        except Exception:
            pass

    def _ui(self, fn, *args, **kwargs):
        try:
            self._ui_kuyrugu.put_nowait((fn, args, kwargs))
        except Exception:
            pass

    def _yaz(self, metin):
        # Worker thread'den çağrılabilir -> ana thread'e yönlendir.
        try:
            if threading.current_thread() is not threading.main_thread():
                self._ui(self._yaz_ana, metin)
                return
        except Exception:
            pass
        self._yaz_ana(metin)

    @staticmethod
    def _satir_etiketi(satir):
        s = satir.strip()
        if s.startswith("> "):
            return "komut"
        kucuk = s.lower()
        if "error" in kucuk or "exception" in kucuk or "severe" in kucuk or "failed" in kucuk or "hata" in kucuk:
            return "hata"
        if "warn" in kucuk or "uyarı" in kucuk or "uyari" in kucuk:
            return "uyari"
        if "joined the game" in kucuk or "katıldı" in kucuk:
            return "giris"
        if "left the game" in kucuk or "lost connection" in kucuk or "ayrıldı" in kucuk:
            return "cikis"
        return None

    def _yaz_ana(self, metin):
        try:
            self.log_alani.configure(state="normal")
            for satir in (metin or "").splitlines(True):
                etiket = self._satir_etiketi(satir)
                if etiket:
                    self.log_alani.insert("end", satir if satir.endswith("\n") else satir + "\n", etiket)
                else:
                    self.log_alani.insert("end", satir if satir.endswith("\n") else satir + "\n")
            try:
                if self.otomatik_kaydir_var.get():
                    self.log_alani.see("end")
            except Exception:
                self.log_alani.see("end")
            self.log_alani.configure(state="disabled")
        except Exception:
            pass

    def _nokta_pompa(self):
        try:
            calisiyor = bool(self.sunucu.proc and self.sunucu.proc.poll() is None)
        except Exception:
            calisiyor = False
        try:
            if calisiyor:
                self._nokta_acik = not self._nokta_acik
                self.nokta_lbl.configure(fg=TEMA.YESIL if self._nokta_acik else "#1E3A2E")
            else:
                self.nokta_lbl.configure(fg=TEMA.SOLUK2)
        except Exception:
            pass
        try:
            self.after(600, self._nokta_pompa)
        except Exception:
            pass

    def _surum_kart_yenile(self):
        try:
            self.kart_surum_var.set((version.oku().get("surum") or "—")[:24])
        except Exception:
            pass

    def _log_pompa(self):
        try:
            while True:
                self._yaz_ana(self.log_q.get_nowait())
        except queue.Empty:
            pass
        # Worker'lardan gelen UI güncellemelerini ana thread'de uygula.
        try:
            while True:
                fn, args, kwargs = self._ui_kuyrugu.get_nowait()
                try:
                    fn(*args, **kwargs)
                except Exception:
                    pass
        except queue.Empty:
            pass
        except Exception:
            pass
        self.after(300, self._log_pompa)

    def _periyodik(self):
        threading.Thread(target=self._durum_guncelle, daemon=True).start()
        self.after(10000, self._periyodik)

    def _durum_guncelle(self):
        # Ağ/dosya işleri worker'da, tüm widget dokunuşları after ile.
        try:
            self.sync.sessiz_baslat()
        except Exception:
            pass
        try:
            yuzde = self.sync.ilerleme_yuzdesi()
            durum = self.sync.son_esitleme_durumu()
            self._ui(self.sync_var.set, "Eşitleme: %s (%s%%)" % (durum, yuzde))
            self._ui(self.kart_eslesme_var.set, "%s %s%%" % (durum, yuzde))
        except Exception:
            self._ui(self.sync_var.set, "Eşitleme: bilinmiyor")
            self._ui(self.kart_eslesme_var.set, "—")
        try:
            bagli, ip, _backend = vpn.bagli_mi()
            self._ui(self.vpn_var.set, "VPN: bağlı (%s)" % ip if bagli else "VPN: bağlı değil — " + T.VPN_KAPALI_COZUM)
            self._ui(self.kart_vpn_var.set, ip if bagli else "kapalı")
            if bagli and not self.site_srv.httpd:
                try:
                    port = int(self.ayar.get("sitePort", 8000))
                except Exception:
                    port = 8000
                try:
                    self.site_srv.baslat(ip, port)
                except Exception:
                    pass
        except Exception as e:
            self._ui(self.vpn_var.set, "VPN: hata (%s)" % str(e)[:100])
            self._ui(self.kart_vpn_var.set, "hata")
        self._ui(lambda: self._ilk_kilit_kontrol(sessiz=True))

    def _rozet_renk(self, renk):
        try:
            self.durum_lbl.configure(fg={"yesil": TEMA.YESIL, "mavi": TEMA.MAVI,
                                          "amber": TEMA.AMBER_HI}.get(renk, TEMA.YAZI))
        except Exception:
            pass

    def _guncelleme_durumu(self):
        """('yok'|'yayinlaniyor'|'bekliyor', surum, notlar). Ana thread'de çağrılır."""
        try:
            v = version.oku()
        except Exception:
            return ("yok", "", "")
        surum = (v.get("surum") or "").strip()
        if not surum or surum == "bilinmiyor":
            return ("yok", "", "")
        notlar = v.get("notlar", "") or ""
        if version.guncelleniyor_mu():
            return ("yayinlaniyor", surum, notlar)
        try:
            uygulanan = (self.ayar.get("uygulananSurum") or "").strip()
        except Exception:
            uygulanan = ""
        if uygulanan != surum:
            return ("bekliyor", surum, notlar)
        return ("yok", surum, notlar)

    def _ilk_kilit_kontrol(self, sessiz=False):
        gdurum, surum, _notlar = self._guncelleme_durumu()
        try:
            if gdurum == "yok":
                self.guncelle_btn.pack_forget()
            else:
                self.guncelle_btn.configure(text="Güncelleme (%s)" % surum)
                self.guncelle_btn.pack(side="left", padx=4)
        except Exception:
            pass
        if gdurum == "yayinlaniyor":
            self.durum_var.set("güncelleme yayınlanıyor, bekle (sürüm %s)" % surum)
            self._rozet_renk("amber")
            self.baslat_btn.configure(state="disabled")
            try:
                self.kart_durum_var.set("Bakım")
                self._durum_gorsel(False)
            except Exception:
                pass
            return
        if gdurum == "bekliyor":
            self.durum_var.set("yeni sürüm hazır: %s — güncellemeden başlayamazsın" % surum)
            self._rozet_renk("amber")
            self.baslat_btn.configure(state="disabled")
            try:
                self.kart_durum_var.set("Bakım")
                self._durum_gorsel(False)
            except Exception:
                pass
            if surum != self._otomatik_acilan_surum:
                self._otomatik_acilan_surum = surum
                self._guncelle_pencere_ac()
            return
        if version.guncelleniyor_mu():
            self.durum_var.set("sunucu dosyaları güncelleniyor")
            self._rozet_renk("amber")
            self.baslat_btn.configure(state="disabled")
            try:
                self.kart_durum_var.set("Bakım")
                self._durum_gorsel(False)
            except Exception:
                pass
            return
        dolu, k = kilit.kilit_dolu_mu(self.kok)
        calisiyor = self.sunucu.proc and self.sunucu.proc.poll() is None
        if dolu and not calisiyor:
            host = k.get("hostAdi", "Bir arkadaş")
            ip = k.get("vpnIp", "")
            self.durum_var.set(T.DURUM_MISAFIR.format(host=host))
            self._rozet_renk("mavi")
            try:
                self.kart_durum_var.set("Misafir")
                self._durum_gorsel(True)
            except Exception:
                pass
            self.katil_var.set(T.KATIL_ADRESI.format(adres="%s:%s" % (ip, k.get("port", 25565))))
            self.baslat_btn.configure(state="disabled")
            if not sessiz:
                self._yaz("%s şu an sunucuyu açık tutuyor, sen ona katılabilirsin.\n" % host)
        elif not dolu and not calisiyor:
            if k and not sessiz:
                self._yaz(T.KILIT_OLU_DEVIR + "\n")
            self.durum_var.set(T.DURUM_KAPALI)
            self._rozet_renk("gri")
            self.katil_var.set("")
            self.baslat_btn.configure(state="normal")
            try:
                self.kart_durum_var.set("Kapalı")
                self._durum_gorsel(False)
            except Exception:
                pass
        elif calisiyor:
            self.durum_var.set(T.DURUM_ACIK)
            self._rozet_renk("yesil")
            self.baslat_btn.configure(state="disabled")
            try:
                self.kart_durum_var.set("Açık")
                self._durum_gorsel(True)
            except Exception:
                pass

    def _baslat_akisi(self):
        if version.guncelleniyor_mu():
            messagebox.showinfo("Bakım", "sunucu dosyaları güncelleniyor, biraz sonra tekrar dene.")
            return
        dolu, k = kilit.kilit_dolu_mu(self.kok)
        if dolu:
            messagebox.showinfo("Dolu", "%s şu an sunucuyu açık tutuyor, sen ona katılabilirsin." % k.get("hostAdi", "Bir arkadaş"))
            return
        eski = kilit.kilit_oku(self.kok)
        ad = self.ayar.get("kullaniciAdi", "") or "Ben"
        _bagli, ip, _b = vpn.bagli_mi()
        kilit.kilit_al(self.kok, ad, ip or "VPN yok")
        if eski:
            self._yaz(T.KILIT_OLU_DEVIR + "\n")
        ok, msg = self.sunucu.baslat()
        self._yaz(msg + "\n")
        if not ok:
            kilit.kilit_birak(self.kok)
            messagebox.showerror("Başlatılamadı", msg)
            return
        self.host_mod = True
        self.kalp.baslat()
        self._ilk_kilit_kontrol(sessiz=True)
        self.durum_var.set(T.DURUM_ACIK)
        threading.Thread(target=self._site_otomatik, daemon=True).start()

    def _site_otomatik(self):
        try:
            _bagli, ip, _b = vpn.bagli_mi()
            if ip:
                port = int(self.ayar.get("sitePort", 8000))
                self.site_srv.baslat(ip, port)
        except Exception:
            pass

    def _guvenli_kapat_akisi(self):
        if not (self.sunucu.proc and self.sunucu.proc.poll() is None):
            kilit.kilit_birak(self.kok)
            self.kalp.durdur()
            self.host_mod = False
            self.durum_var.set(T.DURUM_KAPALI)
            self.baslat_btn.configure(state="normal")
            return
        self._yaz("Güvenli kapatma başladı...\n")
        threading.Thread(target=self._guvenli_kapat_thread, daemon=True).start()

    def _guvenli_kapat_thread(self):
        kapandi = self.sunucu.guvenli_kapat(self._yaz)
        if kapandi:
            kilit.kilit_birak(self.kok)
            self.kalp.durdur()
            self.host_mod = False
            self._ui(self.durum_var.set, T.DURUM_KAPALI)
            self._ui(lambda: self.baslat_btn.configure(state="normal"))
            self._yaz("Sunucu güvenli şekilde kapandı. Kilit bırakıldı.\n")
        else:
            self._yaz("Kapanmadı. 'Zorla Kapat' seçeneğini kullanabilirsin.\n")

    def _zorla(self):
        if messagebox.askyesno("Zorla Kapat", "İşlem sonlandırılsın mı? save-all önce çalıştı, veri kaybı olmaz."):
            self.sunucu.zorla_kapat()
            kilit.kilit_birak(self.kok)
            self.kalp.durdur()
            self.host_mod = False
            self.durum_var.set(T.DURUM_KAPALI)
            self.baslat_btn.configure(state="normal")

    def _komut(self):
        k = self.komut_var.get().strip()
        if not k:
            return
        self.komut_var.set("")
        self._yaz("> " + k + "\n")
        threading.Thread(target=self._komut_thread, args=(k,), daemon=True).start()

    def _komut_thread(self, k):
        ok, cevap = self.sunucu.komut_gonder(k)
        self._yaz((cevap or "") + "\n")

    def _site_ac(self):
        if self.site_srv.adres:
            webbrowser.open(self.site_srv.adres)
        else:
            _bagli, ip, _b = vpn.bagli_mi()
            if not ip:
                messagebox.showwarning("Site kapalı", "Site şu an kapalı (VPN bağlı değil).")
                return
            port = int(self.ayar.get("sitePort", 8000))
            ok, msg = self.site_srv.baslat(ip, port)
            messagebox.showinfo("Site", msg)
            if ok:
                webbrowser.open(msg)

    def _yedek(self):
        try:
            hedef = sunucu.yedek_al(self.kok, self._yaz)
            messagebox.showinfo("Yedek", "Yedek alındı:\n" + hedef)
        except Exception as e:
            messagebox.showerror("Yedek hatası", str(e)[:400])

    def _ayarlar(self):
        win = tk.Toplevel(self)
        win.title("Ayarlar")
        assets.ikon_pencere(win)
        try:
            w, h = 600, 700
            x = (win.winfo_screenwidth() - w) // 2
            y = max(0, (win.winfo_screenheight() - h) // 2 - 20)
            win.geometry("%dx%d+%d+%d" % (w, h, x, y))
        except Exception:
            win.geometry("600x700")
        win.resizable(False, False)
        win.configure(bg=TEMA.BG)
        canvas = tk.Canvas(win, bg=TEMA.BG, highlightthickness=0)
        kaydir = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=kaydir.set)
        kaydir.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        ic = tk.Frame(canvas, bg=TEMA.BG)
        canvas.create_window((0, 0), window=ic, anchor="nw", width=440)

        def _bolge(event=None):
            try:
                canvas.configure(scrollregion=canvas.bbox("all"))
            except Exception:
                pass

        ic.bind("<Configure>", _bolge)

        def _tekerlek(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except Exception:
                pass

        win.bind_all("<MouseWheel>", _tekerlek, add="+")

        def _kapat():
            try:
                win.unbind_all("<MouseWheel>")
            except Exception:
                pass
            try:
                win.destroy()
            except Exception:
                pass

        win.protocol("WM_DELETE_WINDOW", _kapat)

        def kart(baslik):
            k = tk.Frame(ic, bg=TEMA.KART, highlightthickness=1, highlightbackground=TEMA.BORDER_YUMUSAK)
            k.pack(fill="x", pady=(0, 10))
            tk.Label(k, text=baslik.upper(), font=("Segoe UI", 8, "bold"), bg=TEMA.KART, fg=TEMA.SOLUK2).pack(anchor="w", padx=12, pady=(10, 4))
            govde = tk.Frame(k, bg=TEMA.KART)
            govde.pack(fill="x", padx=12, pady=(0, 12))
            return govde

        # Profil
        g = kart("Profil")
        satir = tk.Frame(g, bg=TEMA.KART)
        satir.pack(fill="x")
        sol = tk.Frame(satir, bg=TEMA.KART)
        sol.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(sol, text="Adın", font=TEMA.FONT_NORMAL, bg=TEMA.KART, fg=TEMA.YAZI).pack(anchor="w", pady=(0, 2))
        ad_var = tk.StringVar(value=self.ayar.get("kullaniciAdi", ""))
        e_ad = TEMA.giris(sol, textvariable=ad_var)
        e_ad.pack(fill="x", ipady=5)
        sagc = tk.Frame(satir, bg=TEMA.KART)
        sagc.pack(side="left")
        tk.Label(sagc, text="Site portu", font=TEMA.FONT_NORMAL, bg=TEMA.KART, fg=TEMA.YAZI).pack(anchor="w", pady=(0, 2))
        port_var = tk.StringVar(value=str(self.ayar.get("sitePort", 8000)))
        e_port = TEMA.giris(sagc, textvariable=port_var, width=12)
        e_port.pack(ipady=5)
        # Yapay zeka
        g = kart("Yapay zeka")
        try:
            ai_kayitli = bool(store.ai_anahtar_oku())
        except Exception:
            ai_kayitli = False
        tk.Label(g, text="AI anahtarı" + (" (kayıtlı anahtar var)" if ai_kayitli else ""),
                 font=TEMA.FONT_NORMAL, bg=TEMA.KART, fg=TEMA.YAZI).pack(anchor="w", pady=(0, 2))
        ai_var = tk.StringVar(value="")
        ai_giris = TEMA.giris(g, textvariable=ai_var)
        ai_giris.pack(fill="x", ipady=5)
        try:
            ai_giris.configure(show="*")
        except Exception:
            pass
        # Bağlantı
        g = kart("Bağlantı")
        satir2 = tk.Frame(g, bg=TEMA.KART)
        satir2.pack(fill="x", pady=(4, 0))
        ttk.Button(satir2, text="VPN Bağlan", command=self._vpn_baglan, style="Secondary.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(satir2, text="Kurulum Sihirbazı", command=self._sihirbaz_ac, style="Secondary.TButton").pack(side="left")
        tk.Label(g, text="VPN anahtarı kurulumda saklanır; yoksa sihirbazdan eklenir.",
                 font=TEMA.FONT_KUCUK, bg=TEMA.KART, fg=TEMA.SOLUK).pack(anchor="w", pady=(6, 0))
        # Güncelleme
        g = kart("Güncelleme")
        tk.Label(g, text="GitHub repo (boşsa denetim kapalı)",
                 font=TEMA.FONT_NORMAL, bg=TEMA.KART, fg=TEMA.YAZI).pack(anchor="w", pady=(0, 2))
        repo_var = tk.StringVar(value=self.ayar.get("githubRepo", ""))
        TEMA.giris(g, textvariable=repo_var).pack(fill="x", ipady=5)
        try:
            tk.Label(g, text="Yüklü launcher: %s" % C.PAKET_SURUMU,
                     font=TEMA.FONT_KUCUK, bg=TEMA.KART, fg=TEMA.SOLUK).pack(anchor="w", pady=(6, 0))
        except Exception:
            pass
        ttk.Button(g, text="Güncellemeleri Denetle", command=self._guncelleme_denetle, style="Secondary.TButton").pack(anchor="w", pady=(8, 0))
        # Sahip
        g = kart("Sahip")
        try:
            vs = version.oku()
            tk.Label(g, text="Sunucu sürümü: %s%s" % (vs.get("surum", "?"), " (hazırlanıyor)" if vs.get("guncelleniyor") else ""),
                     font=TEMA.FONT_NORMAL, bg=TEMA.KART, fg=TEMA.YAZI).pack(anchor="w", pady=(0, 6))
        except Exception:
            pass
        satir3 = tk.Frame(g, bg=TEMA.KART)
        satir3.pack(fill="x")
        ttk.Button(satir3, text="Klasörü Aç", command=self._klasor_ac, style="Secondary.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(satir3, text="Güncelleme Yayınla", command=self._guncelleme_yayinla, style="Secondary.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(satir3, text="Bitir", command=self._guncelleme_bitir, style="Secondary.TButton").pack(side="left")
        ttk.Button(satir3, text="Kaldır (uygulama)", command=self._kaldir, style="Danger.TButton").pack(side="left", padx=(8, 0))

        def kaydet_kapat():
            try:
                self.ayar["sitePort"] = int(port_var.get().strip())
            except Exception:
                pass
            self.ayar["kullaniciAdi"] = ad_var.get().strip()
            try:
                self.ayar["githubRepo"] = repo_var.get().strip()
            except Exception:
                pass
            store.kaydet(self.ayar)
            try:
                yeni_ai = ai_var.get().strip()
                if yeni_ai:
                    store.ai_anahtar_kaydet(yeni_ai)
            except Exception:
                pass
            _kapat()

        ttk.Button(ic, text="Kaydet ve Kapat", command=kaydet_kapat, style="Primary.TButton").pack(fill="x", pady=(2, 6))

    def _klasor_ac(self):
        try:
            subprocess.Popen(["explorer", self.kok])
        except Exception as e:
            messagebox.showerror("Hata", str(e)[:300])

    def _kaldir(self):
        if self.sunucu.proc and self.sunucu.proc.poll() is None:
            messagebox.showwarning("Önce kapat", "Kaldırmadan önce sunucuyu Güvenli Kapat ile kapatmalısın.")
            return
        try:
            from core import kurulum as _K
        except Exception:
            messagebox.showerror("Hata", "Kaldırma modülü yüklenemedi.")
            return
        if not _K.kurulu_mu():
            messagebox.showinfo("Kaldır", "Uygulama kurulu modda değil (taşınabilir çalışıyor). Klasörü silmen yeterli.")
            return
        if not messagebox.askyesno("Kaldır", "Uygulama ve kısayollar silinecek.\nSunucu verilerin (dünya, ayarlar) DURACAK.\nDevam edilsin mi?"):
            return
        try:
            bat, pid, dizin = _K.kaldir_hazirla()
        except Exception as e:
            messagebox.showerror("Hata", str(e)[:300])
            return
        try:
            subprocess.Popen([bat, str(pid), dizin], creationflags=0x08000000)
        except Exception as e:
            messagebox.showerror("Başlatılamadı", str(e)[:300])
            return
        try:
            self.site_srv.durdur()
        except Exception:
            pass
        try:
            self.kalp.durdur()
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass

    def _guncelleme_denetle(self):
        try:
            self.ayar = store.yukle()
        except Exception:
            pass
        self._yaz("Güncelleme denetleniyor...\n")
        threading.Thread(target=self._guncelleme_denetle_thread, daemon=True).start()

    def _guncelleme_denetle_thread(self):
        try:
            sonuc = guncelleme.denetle(self.ayar)
        except Exception as e:
            self._ui(messagebox.showwarning, "Güncelleme", "Denetim başarısız: %s" % str(e)[:300])
            return
        if sonuc.get("kapali"):
            self._ui(messagebox.showinfo, "Güncelleme", sonuc.get("mesaj", "Kapalı."))
            return
        if not sonuc.get("guncelleme_var"):
            self._ui(messagebox.showinfo, "Güncelleme", "Launcher güncel (sürüm %s)." % sonuc.get("mevcut", "?"))
            return
        self._ui(self._guncelleme_sor, sonuc)

    @staticmethod
    def _notlari_temizle(notlar):
        satirlar = []
        for s in (notlar or "").splitlines():
            t = s.strip()
            if not t:
                continue
            if t.startswith("**Full Changelog**"):
                continue
            if t.startswith("https://github.com/") and "compare" in t:
                continue
            satirlar.append(s)
        temiz = "\n".join(satirlar).strip()
        return temiz[:800] if temiz else "Not yok."

    def _guncelleme_sor(self, sonuc):
        metin = "Yeni launcher sürümü: %s (sende %s).\n\n%s\n\nİndirip uygulansın mı? (Uygulamayı kapatıp açman gerekir.)" % (
            sonuc.get("son", "?"), sonuc.get("mevcut", "?"), self._notlari_temizle(sonuc.get("notlar")))
        if not messagebox.askyesno("Güncelleme var", metin):
            return
        if self.sunucu.proc and self.sunucu.proc.poll() is None:
            messagebox.showwarning("Önce kapat", "Uygulamadan önce sunucuyu Güvenli Kapat ile kapatmalısın.")
            return
        threading.Thread(target=self._guncelleme_uygula_thread, args=(sonuc,), daemon=True).start()

    def _guncelleme_uygula_thread(self, sonuc):
        try:
            bilgi = guncelleme.uygula(self.kok, sonuc, durum_yaz=self._yaz)
        except Exception as e:
            self._ui(messagebox.showerror, "Güncelleme hatası", str(e)[:400])
            return
        try:
            self.ayar["launcherSurumu"] = (sonuc or {}).get("son", "")
            store.kaydet(self.ayar)
        except Exception:
            pass
        if not bilgi.get("exe"):
            self._ui(messagebox.showinfo, "Güncelleme", "Güncelleme uygulandı. Değişiklikler için uygulamayı kapatıp aç.")
            return
        self._ui(self._exe_yeniden_sor, bilgi)

    def _exe_yeniden_sor(self, bilgi):
        if not messagebox.askyesno("Hazır", "Güncelleme indirildi. Şimdi uygulayıp yeniden başlatılsın mı?\n(Eski sürüm klasörleri temizlenecek.)"):
            return
        try:
            subprocess.Popen([bilgi["bat"], str(bilgi["pid"]), bilgi["hedef"], bilgi["kaynak"]],
                             creationflags=0x08000000)
        except Exception as e:
            messagebox.showerror("Başlatılamadı", "Güncelleyici çalışmadı: %s" % str(e)[:300])
            return
        try:
            self.site_srv.durdur()
        except Exception:
            pass
        try:
            self.kalp.durdur()
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass

    def _sihirbaz_ac(self):
        try:
            from ui.wizard import Wizard
        except Exception:
            from launcher.ui.wizard import Wizard  # type: ignore
        Wizard(self, self.kok, self.ayar, self.sync, self._sihirbaz_bitti, kapatilabilir=True)

    def _sihirbaz_bitti(self, _yeni_kok=None):
        try:
            self.ayar = store.yukle()
        except Exception:
            pass

    # ---------- zorunlu güncelleme ----------
    def _guncelle_pencere_ac(self):
        try:
            if self._guncelle_penceresi and self._guncelle_penceresi.winfo_exists():
                self._guncelle_penceresi.lift()
                return
        except Exception:
            pass
        gdurum, surum, notlar = self._guncelleme_durumu()
        if gdurum == "yok":
            messagebox.showinfo("Güncelleme", "Güncelleme yok, sürümün güncel.")
            return
        win = tk.Toplevel(self)
        win.title("Güncelleme")
        win.geometry("520x640")
        win.resizable(False, False)
        win.configure(bg=TEMA.BG)
        self._guncelle_penceresi = win
        assets.ikon_pencere(win)
        ic = tk.Frame(win, bg=TEMA.BG)
        ic.pack(fill="both", expand=True, padx=24, pady=18)
        self._img_update = assets.foto("illustrations", "update-460.png")
        if self._img_update:
            tk.Label(ic, image=self._img_update, bg=TEMA.BG).pack(anchor="w", pady=(0, 10))
        tk.Label(ic, text="GÜNCELLEME VAR", font=("Segoe UI", 9, "bold"), bg=TEMA.BG, fg=TEMA.AMBER_HI).pack(anchor="w")
        tk.Label(ic, text="Sürüm %s" % surum, font=("Segoe UI", 18, "bold"), bg=TEMA.BG, fg=TEMA.YAZI).pack(anchor="w", pady=(4, 8))
        if notlar:
            tk.Label(ic, text=notlar, font=TEMA.FONT_NORMAL, bg=TEMA.BG, fg=TEMA.YAZI,
                     wraplength=460, justify="left").pack(anchor="w", pady=(0, 8))
        durum_var = tk.StringVar(value="")
        tk.Label(ic, textvariable=durum_var, font=("Segoe UI", 11, "bold"), bg=TEMA.BG, fg=TEMA.SOLUK,
                 wraplength=460, justify="left").pack(anchor="w", pady=(0, 6))
        bar = ttk.Progressbar(ic, maximum=100, length=460, style="Amber.Horizontal.TProgressbar")
        bar.pack(fill="x", pady=(0, 12))
        uygula_btn = ttk.Button(ic, text="Güncellemeyi Uygula", style="Primary.TButton")
        uygula_btn.pack(anchor="w")

        def yenile():
            try:
                if not win.winfo_exists():
                    return
            except Exception:
                return
            g, s, _n = self._guncelleme_durumu()
            if g == "yok":
                try:
                    win.destroy()
                except Exception:
                    pass
                self._guncelle_penceresi = None
                self._ilk_kilit_kontrol(sessiz=True)
                return
            if g == "yayinlaniyor":
                durum_var.set("Sahip güncellemeyi hazırlıyor, bitirmesini bekle. Bu ekranda bekleyebilirsin.")
                try:
                    bar.configure(value=10)
                    uygula_btn.configure(state="disabled")
                except Exception:
                    pass
            else:
                try:
                    yuzde = self.sync.ilerleme_yuzdesi()
                except Exception:
                    yuzde = 0
                try:
                    bar.configure(value=yuzde)
                except Exception:
                    pass
                if yuzde >= 100:
                    durum_var.set("Dosyalar geldi. Uygula'ya bas, sonra Başlat açılır.")
                    try:
                        uygula_btn.configure(state="normal")
                    except Exception:
                        pass
                else:
                    durum_var.set("Yeni dosyalar alınıyor: %%%d. Bitmeden kapatma." % yuzde)
                    try:
                        uygula_btn.configure(state="disabled")
                    except Exception:
                        pass
            try:
                win.after(2000, yenile)
            except Exception:
                pass

        def uygula():
            g, s, _n = self._guncelleme_durumu()
            if g == "yayinlaniyor":
                messagebox.showinfo("Bekle", "Sahip güncellemeyi henüz bitirmedi.")
                return
            try:
                yuzde = self.sync.ilerleme_yuzdesi()
            except Exception:
                yuzde = 0
            if yuzde < 100:
                messagebox.showwarning("Erken", "Dosyalar henüz tam gelmedi (%%%d). Biraz bekle." % yuzde)
                return
            self.ayar["uygulananSurum"] = s
            store.kaydet(self.ayar)
            try:
                win.destroy()
            except Exception:
                pass
            self._guncelle_penceresi = None
            self._surum_kart_yenile()
            self._yaz("Sürüm %s uygulandı.\n" % s)
            self._ilk_kilit_kontrol(sessiz=True)

        uygula_btn.configure(command=uygula)
        yenile()

    def _guncelleme_yayinla(self):
        if self.sunucu.proc and self.sunucu.proc.poll() is None:
            messagebox.showwarning("Önce kapat", "Yayınlamadan önce sunucuyu Güvenli Kapat ile kapatmalısın.")
            return
        try:
            dolu, k = kilit.kilit_dolu_mu(self.kok)
        except Exception:
            dolu, k = False, None
        if dolu:
            messagebox.showwarning("Meşgul", "%s şu an sunucuyu açık tutuyor. O kapatmadan yayınlama." % (k or {}).get("hostAdi", "Bir arkadaş"))
            return
        try:
            mevcut = version.oku().get("surum", "")
        except Exception:
            mevcut = ""
        oneri = time.strftime("%Y.%m.%d-%H%M")
        yeni = simpledialog.askstring("Sürüm", "Yeni sürüm numarası:", initialvalue=oneri, parent=self)
        if not yeni or not yeni.strip():
            return
        notlar = simpledialog.askstring("Not", "Arkadaşların göreceği not (örnek: 3 plugin güncellendi):", parent=self) or ""
        version.yayinla(yeni.strip(), notlar.strip())
        self.ayar["uygulananSurum"] = yeni.strip()
        store.kaydet(self.ayar)
        self._yaz("Sürüm %s yayınlandı. Plugin değişikliklerini yap, bitince Ayarlar > Güncellemeyi Bitir.\n" % yeni.strip())
        messagebox.showinfo("Yayınlandı", "Arkadaşların uygulaması kilitlendi. Değişiklikleri yap, sonra Güncellemeyi Bitir'e bas.")
        self._ilk_kilit_kontrol(sessiz=True)

    def _guncelleme_bitir(self):
        try:
            v = version.oku()
        except Exception:
            v = {"guncelleniyor": False}
        if not v.get("guncelleniyor"):
            messagebox.showinfo("Yok", "Yayınlanmış bir güncelleme yok.")
            return
        surum = version.bitir_guncelleme()
        self.ayar["uygulananSurum"] = surum
        store.kaydet(self.ayar)
        self._yaz("Sürüm %s bitirildi, arkadaşlar güncelleyebilir.\n" % surum)
        messagebox.showinfo("Bitti", "Güncelleme yayınlandı (sürüm %s)." % surum)
        self._ilk_kilit_kontrol(sessiz=True)

    def _vpn_baglan(self):
        key = store.anahtar_oku() or store.kurulum_anahtari_oto_bul(self.kok)
        if not key:
            messagebox.showwarning("Anahtar yok", "kurulum-anahtari.txt bulunamadı. Genel yöneticiden iste.")
            return
        ad = self.ayar.get("kullaniciAdi", "")
        self._yaz("VPN bağlanıyor...\n")
        threading.Thread(target=self._vpn_baglan_thread, args=(key, ad), daemon=True).start()

    def _vpn_baglan_thread(self, key, ad):
        ok, msg = vpn.baglan(key, ad)
        kisa = (msg or "")[:500]
        self._yaz(("VPN: " + kisa if ok else "VPN hatası: " + kisa) + "\n")
        self._ui(messagebox.showinfo, "VPN", kisa or ("Bağlandı." if ok else "Bağlanamadı."))

    def _ai_baglam(self):
        """AI'ye gönderilen durum özeti. Ana thread'de çağrılır."""
        satirlar = []
        for var in (self.durum_var, self.sync_var, self.vpn_var):
            try:
                satirlar.append(var.get())
            except Exception:
                pass
        try:
            kuyruk = self.log_alani.get("1.0", "end-1c")
            if len(kuyruk) > 3000:
                kuyruk = "...\n" + kuyruk[-3000:]
            satirlar.append("SON KONSOL:\n" + kuyruk)
        except Exception:
            pass
        return "\n".join(satirlar)[:6000]

    def _ai_yardim(self):
        win = tk.Toplevel(self)
        win.title("AI Yardım")
        assets.ikon_pencere(win)
        win.geometry("580x540")
        win.configure(bg=TEMA.BG)
        ic = tk.Frame(win, bg=TEMA.BG)
        ic.pack(fill="both", expand=True, padx=20, pady=16)
        tk.Label(ic, text="Sorunu yaz, AI Türkçe teşhis + çözüm adımları verir. AI komut çalıştırmaz.",
                 font=TEMA.FONT_KUCUK, bg=TEMA.BG, fg=TEMA.SOLUK, wraplength=520, justify="left").pack(anchor="w", pady=(0, 8))
        soru_kutusu = tk.Text(ic, height=4, bg=TEMA.KART2, fg=TEMA.YAZI, insertbackground=TEMA.AMBER,
                              relief="flat", highlightthickness=1, highlightbackground=TEMA.BORDER,
                              highlightcolor=TEMA.AMBER, font=TEMA.FONT_NORMAL, wrap="word")
        soru_kutusu.pack(fill="x", pady=(0, 8))
        gonder_btn = ttk.Button(ic, text="Sor", style="Primary.TButton")
        gonder_btn.pack(anchor="w", pady=(0, 8))
        cevap_kutusu = TEMA.konsol(ic, height=16)
        cevap_kutusu.pack(fill="both", expand=True)
        cevap_kutusu.configure(state="disabled")

        def cevap_yaz(metin):
            try:
                cevap_kutusu.configure(state="normal")
                cevap_kutusu.delete("1.0", "end")
                cevap_kutusu.insert("end", metin)
                cevap_kutusu.configure(state="disabled")
            except Exception:
                pass

        def gonder():
            soru = soru_kutusu.get("1.0", "end").strip()
            if not soru:
                messagebox.showwarning("Soru boş", "Önce sorunu yazmalısın.")
                return
            try:
                anahtar = store.ai_anahtar_oku()
            except Exception:
                anahtar = ""
            if not anahtar:
                messagebox.showwarning("Anahtar yok", "Önce Ayarlar > AI anahtarı alanına anahtarını kaydet.")
                return
            baglam = self._ai_baglam()
            self._ui(cevap_yaz, "Soruluyor, bekleniyor...")
            gonder_btn.configure(state="disabled")
            threading.Thread(target=self._ai_sor_thread,
                             args=(anahtar, soru, baglam, cevap_yaz), daemon=True).start()

        def bitti(cevap):
            cevap_yaz(cevap)
            try:
                gonder_btn.configure(state="normal")
            except Exception:
                pass

        gonder_btn.configure(command=gonder)
        self._ai_bitti = bitti

    def _ai_sor_thread(self, anahtar, soru, baglam, cevap_yaz):
        try:
            cevap = YARDIMCI.sor(anahtar, soru, baglam)
        except Exception as e:
            cevap = "Soramadım: %s" % str(e)[:500]
        self._ui(self._ai_bitti, cevap)

    def _kapanis_sor(self):
        calisiyor = self.sunucu.proc and self.sunucu.proc.poll() is None
        if not calisiyor:
            self.site_srv.durdur()
            try:
                self.kalp.durdur()
            except Exception:
                pass
            self.destroy()
            return
        cevap = messagebox.askyesnocancel(
            "Sunucu çalışıyor",
            "Sunucu hâlâ çalışıyor. Pencere kapatılsa bile sunucu ÖLDÜRÜLMEYECEK.\n\n"
            "Evet = pencereyi simge durumuna küçült (sunucu çalışmaya devam eder)\n"
            "Hayır = güvenli kapat (save-all + stop) sonra çık\n"
            "Vazgeç = pencerede kal",
        )
        if cevap is None:
            return
        if cevap is True:
            try:
                self.iconify()
            except Exception:
                pass
            self._yaz("Pencere simge durumuna alındı, sunucu çalışmaya devam ediyor. Kilit sende duruyor.\n")
        else:
            self._guvenli_kapat_akisi()
            self.after(2000, self._kapanis_sor_tekrar)

    def _kapanis_sor_tekrar(self):
        calisiyor = self.sunucu.proc and self.sunucu.proc.poll() is None
        if not calisiyor:
            self.site_srv.durdur()
            self.destroy()
        else:
            self.deiconify()
