"""Kurulum sihirbazı: tek konulu adımlar, kapılı ilerleme, sekme yok.
Worker -> UI kuyruk + ana thread pompa (Tcl tek thread)."""
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from core import store, vpn, esitleme, assets
from ui import texts as T
from ui import theme as TEMA

FONT_ADIM_BASLIK = ("Segoe UI", 22, "bold")
FONT_GOVDE = ("Segoe UI", 12)
FONT_GIRIS = ("Segoe UI", 13)


class Wizard(tk.Toplevel):
    def __init__(self, master, sunucu_koku, ayar, sync_yoneticisi, bitince, kapatilabilir=False):
        super().__init__(master)
        self.title("DgmCraft Kurulum")
        self.geometry("640x660")
        self.resizable(False, False)
        TEMA.uygula(self)
        assets.ikon_pencere(self)
        self.kok = sunucu_koku
        self.ayar = ayar
        self.sync = sync_yoneticisi
        self.bitince = bitince
        # Doğrulama durumu (worker'lar kuyruk üzerinden günceller).
        self.sync_ok = False
        self.vpn_kurulu = False
        self.vpn_bagli = False
        self.vpn_ip = ""
        self.esles_ok = False
        self.esles_atlandi = False
        self.anahtar_atlandi = False
        self._mesgul = False
        self.ad_var = tk.StringVar(value=ayar.get("kullaniciAdi", ""))
        self.key_var = tk.StringVar(value="")
        self.kod1_var = tk.StringVar(value=(ayar.get("arkadasKodlari", ["", ""]) + ["", ""])[0])
        self.kod2_var = tk.StringVar(value=(ayar.get("arkadasKodlari", ["", ""]) + ["", ""])[1])
        self.kendi_kod_var = tk.StringVar(value="")
        self._ui_kuyrugu = queue.Queue()
        self.adim = 0
        self.adimlar = [
            ("Hoş geldin", self._adim_hosgeldin),
            ("Adın", self._adim_ad),
            ("VPN anahtarı", self._adim_anahtar),
            ("Dosya eşitleme", self._adim_sync),
            ("Gizli ağ", self._adim_vpn),
            ("Arkadaşlar", self._adim_arkadas),
            ("Hazır", self._adim_hazir),
        ]
        # Üst: ilerleme başlığı
        ust = tk.Frame(self, bg=TEMA.BG)
        ust.pack(fill="x", padx=32, pady=(24, 0))
        self.adim_sayisi_var = tk.StringVar(value="")
        tk.Label(ust, textvariable=self.adim_sayisi_var, font=TEMA.FONT_KUCUK,
                 bg=TEMA.BG, fg=TEMA.SOLUK).pack(anchor="w")
        self.adim_baslik_var = tk.StringVar(value="")
        tk.Label(ust, textvariable=self.adim_baslik_var, font=FONT_ADIM_BASLIK,
                 bg=TEMA.BG, fg=TEMA.YAZI).pack(anchor="w", pady=(2, 10))
        self.adim_artlar = ["step-welcome", "step-name", "step-key", "step-sync",
                            "step-vpn", "step-friends", "step-ready"]
        self.bar = ttk.Progressbar(ust, maximum=100, length=560,
                                   style="Amber.Horizontal.TProgressbar")
        self.bar.pack(fill="x", pady=(0, 6))
        # Orta: adım içeriği (kaydırmalı, uzun adımlar taşmaz)
        self.icerik_kutu = tk.Frame(self, bg=TEMA.BG)
        self.icerik_kutu.pack(fill="both", expand=True, padx=32, pady=12)
        self._icerik_canvas = tk.Canvas(self.icerik_kutu, bg=TEMA.BG, highlightthickness=0)
        self._icerik_kaydir = ttk.Scrollbar(self.icerik_kutu, orient="vertical",
                                            command=self._icerik_canvas.yview)
        self._icerik_canvas.configure(yscrollcommand=self._icerik_kaydir.set)
        self.icerik = tk.Frame(self._icerik_canvas, bg=TEMA.BG)
        self._icerik_pencere = self._icerik_canvas.create_window((0, 0), window=self.icerik, anchor="nw")
        self.icerik.bind("<Configure>", lambda e: self._icerik_canvas.configure(scrollregion=self._icerik_canvas.bbox("all")))
        self._icerik_canvas.bind("<Configure>", lambda e: self._icerik_canvas.itemconfigure(self._icerik_pencere, width=e.width))
        self._icerik_canvas.pack(side="left", fill="both", expand=True)
        self._icerik_kaydir.pack(side="right", fill="y")
        self.bind_all("<MouseWheel>", self._icerik_tekerlek, add="+")
        # Alt: gezinme
        alt = tk.Frame(self, bg=TEMA.BG)
        alt.pack(fill="x", padx=32, pady=(0, 24))
        self.geri_btn = ttk.Button(alt, text="← Geri", command=self._geri, style="Secondary.TButton")
        self.geri_btn.pack(side="left")
        self.birincil_btn = ttk.Button(alt, text="Başla →", command=self._birincil_bas, style="Primary.TButton")
        self.birincil_btn.pack(side="right")
        self.mesgul_bar = ttk.Progressbar(self, mode="indeterminate", style="Amber.Horizontal.TProgressbar")
        self.after(150, self._ui_pompa)
        # Çarpı her zaman çalışır: ilk kurulumda sessiz çıkış (bir dahaki
        # açılışta sihirbaz yine gelir), sonradan açıldıysa bir şey kaydedilmez.
        self.protocol("WM_DELETE_WINDOW", self._vazgec_kapat)
        self._ciz()

    # ---------- altyapı ----------
    def _ui(self, fn, *args, **kwargs):
        try:
            self._ui_kuyrugu.put_nowait((fn, args, kwargs))
        except Exception:
            pass

    def _ui_pompa(self):
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
        try:
            if self.winfo_exists():
                self.after(150, self._ui_pompa)
        except Exception:
            pass

    def _icerik_tekerlek(self, event):
        try:
            self._icerik_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def _tekerlek_temizle(self):
        try:
            self.unbind_all("<MouseWheel>")
        except Exception:
            pass

    def _vazgec_kapat(self):
        self._tekerlek_temizle()
        try:
            self.destroy()
        except Exception:
            pass
        try:
            self.bitince(self.kok)
        except TypeError:
            self.bitince()

    def _temizle_icerik(self):
        for w in self.icerik.winfo_children():
            try:
                w.destroy()
            except Exception:
                pass
        # Adım görseli (yoksa sessiz geçilir, düzen bozulmaz).
        try:
            art = self.adim_artlar[self.adim % len(self.adim_artlar)]
            self._art_img = assets.foto("wizard", art + ".png")
            if self._art_img:
                tk.Label(self.icerik, image=self._art_img, bg=TEMA.BG).pack(anchor="w", pady=(0, 8))
        except Exception:
            pass

    def _govde(self, metin):
        tk.Label(self.icerik, text=metin, font=FONT_GOVDE, bg=TEMA.BG,
                 fg=TEMA.YAZI, wraplength=560, justify="left").pack(anchor="w", pady=6)

    def _not(self, metin):
        tk.Label(self.icerik, text=metin, font=TEMA.FONT_NORMAL, bg=TEMA.BG,
                 fg=TEMA.SOLUK, wraplength=560, justify="left").pack(anchor="w", pady=6)

    def _durum(self, metin=""):
        var = tk.StringVar(value=metin)
        lbl = tk.Label(self.icerik, textvariable=var, font=("Segoe UI", 12, "bold"),
                       bg=TEMA.BG, fg=TEMA.SOLUK, wraplength=560, justify="left")
        lbl.pack(anchor="w", pady=10)
        return var, lbl

    def _durum_boya(self, var, lbl, metin, renk):
        var.set(metin)
        try:
            lbl.configure(fg={"yesil": TEMA.YESIL, "kirmizi": TEMA.KIRMIZI,
                              "amber": TEMA.AMBER_HI}.get(renk, TEMA.SOLUK))
        except Exception:
            pass

    def _ciz(self):
        baslik, kurucu = self.adimlar[self.adim]
        self.adim_sayisi_var.set("ADIM %d / %d" % (self.adim + 1, len(self.adimlar)))
        self.adim_baslik_var.set(baslik)
        try:
            self.bar.configure(value=100 * (self.adim + 1) / len(self.adimlar))
        except Exception:
            pass
        self._temizle_icerik()
        kurucu()
        self._birincil_yenile()
        try:
            self.geri_btn.configure(state="normal" if self.adim > 0 else "disabled")
        except Exception:
            pass

    # ---------- adımlar ----------
    def _adim_hosgeldin(self):
        self._govde(T.HOSGELDIN_ACIKLAMA)
        self._not("Sana 7 kısa adımda her şeyi hazırlatacağım. Her adım, bir önceki doğrulanmadan açılmaz.")

    def _adim_ad(self):
        self._govde(T.AD_ACIKLAMA)
        tk.Label(self.icerik, text=T.AD_SOR, font=FONT_GOVDE, bg=TEMA.BG, fg=TEMA.YAZI).pack(anchor="w", pady=(10, 4))
        g = TEMA.giris(self.icerik, textvariable=self.ad_var, width=28)
        try:
            g.configure(font=FONT_GIRIS)
        except Exception:
            pass
        g.pack(anchor="w", pady=2, ipady=8)

    def _adim_anahtar(self):
        self._govde(T.ANAHTAR_ACIKLAMA)
        g = TEMA.giris(self.icerik, textvariable=self.key_var, width=44)
        try:
            g.configure(font=FONT_GIRIS, show="*")
        except Exception:
            pass
        g.pack(anchor="w", pady=(10, 2), ipady=8)
        self._not(T.ANAHTAR_YOK_NOTU)
        if not self.key_var.get().strip():
            ttk.Button(self.icerik, text="Anahtarım yok, sonra ekleyeceğim",
                       command=self._anahtar_atla, style="Secondary.TButton").pack(anchor="w", pady=(8, 0))

    def _anahtar_atla(self):
        if self._mesgul:
            return
        if messagebox.askyesno("Anahtarsız devam", "VPN anahtarı olmadan devam ediyorsun. Anahtarı alınca Ayarlar > VPN Bağlan ile bağlanırsın. Devam edilsin mi?"):
            self.anahtar_atlandi = True
            try:
                self.key_var.set("")
            except Exception:
                pass
            self._birincil_yenile()

    def _adim_sync(self):
        self._govde(T.SYNC_ACIKLAMA)
        self._not(T.SYNC_KONTROL)
        self.sync_durum_var, self.sync_durum_lbl = self._durum()

    def _adim_vpn(self):
        self._govde(T.VPN_ACIKLAMA)
        self.vpn_durum_var, self.vpn_durum_lbl = self._durum()
        if not self.vpn_kurulu:
            self._durum_boya(self.vpn_durum_var, self.vpn_durum_lbl, "Henüz kontrol edilmedi.", "amber")
        if not self._anahtar_var():
            self._not(T.VPN_ANAHTARSIZ_NOTU)

    def _adim_arkadas(self):
        self._govde(T.ARKADAS_ACIKLAMA)
        tk.Label(self.icerik, text=T.KENDI_KODUN, font=FONT_GOVDE, bg=TEMA.BG, fg=TEMA.YAZI).pack(anchor="w", pady=(10, 2))
        kod = self.kendi_kod_var.get() or self.ayar.get("kendiCihazKodu", "") or "alınıyor..."
        kod_giris = TEMA.giris(self.icerik, width=52)
        kod_giris.pack(anchor="w", pady=2, ipady=6)
        try:
            kod_giris.insert(0, kod)
            # readonly mod sistem beyazına döner; koyu temada kilitle.
            kod_giris.configure(state="readonly", readonlybackground=TEMA.KART2,
                                fg=TEMA.YAZI)
        except Exception:
            pass
        tk.Label(self.icerik, text=T.ARKADAS_KODU_1, font=FONT_GOVDE, bg=TEMA.BG, fg=TEMA.YAZI).pack(anchor="w", pady=(12, 2))
        g1 = TEMA.giris(self.icerik, textvariable=self.kod1_var, width=52)
        g1.pack(anchor="w", pady=2, ipady=6)
        tk.Label(self.icerik, text=T.ARKADAS_KODU_2, font=FONT_GOVDE, bg=TEMA.BG, fg=TEMA.YAZI).pack(anchor="w", pady=(12, 2))
        g2 = TEMA.giris(self.icerik, textvariable=self.kod2_var, width=52)
        g2.pack(anchor="w", pady=2, ipady=6)
        self.esles_durum_var, self.esles_durum_lbl = self._durum()
        if self.esles_ok:
            self._durum_boya(self.esles_durum_var, self.esles_durum_lbl, "Eşleştirme tamam.", "yesil")
        else:
            ttk.Button(self.icerik, text="Kodlarım henüz yok, atla", command=self._esles_atla,
                       style="Secondary.TButton").pack(anchor="w", pady=(12, 0))

    def _adim_hazir(self):
        self._govde(T.HAZIR_BASLIK)
        satirlar = [
            "Adın: %s" % (self.ad_var.get().strip() or "—"),
            "Dosya eşitleme: %s" % ("hazır" if self.sync_ok else "eksik"),
            "VPN: %s" % ("bağlı (%s)" % self.vpn_ip if self.vpn_bagli else ("kurulu" if self.vpn_kurulu else "eksik")),
            "Eşleştirme: %s" % ("tamam" if self.esles_ok else ("atlandı" if self.esles_atlandi else "eksik")),
        ]
        for s in satirlar:
            tk.Label(self.icerik, text="•  " + s, font=FONT_GOVDE, bg=TEMA.BG, fg=TEMA.YAZI, anchor="w").pack(fill="x", pady=3)

    # ---------- yardımcılar ----------
    def _anahtar_var(self):
        try:
            if self.key_var.get().strip():
                return True
        except Exception:
            pass
        try:
            if store.kurulum_anahtari_oto_bul(self.kok) or store.anahtar_oku():
                return True
        except Exception:
            pass
        return False

    def _cozulen_anahtar(self):
        try:
            k = self.key_var.get().strip()
            if k:
                return k
        except Exception:
            pass
        try:
            return store.kurulum_anahtari_oto_bul(self.kok) or store.anahtar_oku()
        except Exception:
            return ""

    # ---------- birincil düğme ----------
    def _birincil_yenile(self):
        try:
            self.birincil_btn.configure(state="normal")
        except Exception:
            pass
        if self.adim == 0:
            self.birincil_btn.configure(text="Başla →")
        elif self.adim in (1, 2):
            self.birincil_btn.configure(text="Devam Et →")
        elif self.adim == 3:
            self.birincil_btn.configure(text="Devam Et →" if self.sync_ok else "Kontrol Et")
        elif self.adim == 4:
            if not self.vpn_kurulu:
                self.birincil_btn.configure(text="Kontrol Et")
            elif self._anahtar_var() and not self.vpn_bagli:
                self.birincil_btn.configure(text="Bağlan")
            else:
                self.birincil_btn.configure(text="Devam Et →")
        elif self.adim == 5:
            self.birincil_btn.configure(text="Devam Et →" if (self.esles_ok or self.esles_atlandi) else "Eşleştir")
        else:
            self.birincil_btn.configure(text="Bitir")

    def _birincil_bas(self):
        if self._mesgul:
            return
        if self.adim == 0:
            self._ileri()
        elif self.adim == 1:
            if not self.ad_var.get().strip():
                messagebox.showwarning("Ad gerekli", "Devam etmek için adını yazmalısın.")
                return
            self.ayar["kullaniciAdi"] = self.ad_var.get().strip()
            store.kaydet(self.ayar)
            self._ileri()
        elif self.adim == 2:
            try:
                anahtar = self.key_var.get().strip()
            except Exception:
                anahtar = ""
            if anahtar:
                try:
                    store.anahtar_kaydet(anahtar)
                    self.ayar["tailscaleAnahtariSakli"] = True
                    store.kaydet(self.ayar)
                except Exception:
                    pass
                self.anahtar_atlandi = False
                self._ileri()
            elif self.anahtar_atlandi:
                self._ileri()
            else:
                messagebox.showwarning("Anahtar belirtilmedi", "Anahtarın varsa yukarı yapıştır, yoksa aşağıdaki düğmeyle belirtmeden geçemezsin.")
                return
        elif self.adim == 3:
            if self.sync_ok:
                self._ileri()
            else:
                self._kontrol_sync_thread()
        elif self.adim == 4:
            if not self.vpn_kurulu:
                self._kontrol_vpn_thread()
            elif self._anahtar_var() and not self.vpn_bagli:
                self._baglan_thread()
            else:
                self._ileri()
        elif self.adim == 5:
            if self.esles_ok or self.esles_atlandi:
                self._ileri()
            else:
                self._eslestir_thread()
        else:
            self._bitir()

    def _geri(self):
        if self._mesgul or self.adim <= 0:
            return
        self.adim -= 1
        self._ciz()

    def _ileri(self):
        if self.adim < len(self.adimlar) - 1:
            self.adim += 1
            self._ciz()
            # Arkadaş adımına girerken kod hazır değilse arka planda al.
            if self.adim == 5 and not (self.kendi_kod_var.get() or self.ayar.get("kendiCihazKodu", "")):
                self._kontrol_sync_thread(sessiz=True)

    # ---------- worker'lar ----------
    def _mesgul_ac(self, metin):
        self._mesgul = True
        try:
            self.birincil_btn.configure(state="disabled")
            self.geri_btn.configure(state="disabled")
            self.mesgul_bar.pack(fill="x", padx=32, pady=(0, 12))
            self.mesgul_bar.start(12)
        except Exception:
            pass
        return metin

    def _mesgul_kapat(self):
        self._ui(self._mesgul_kapat_ana)

    def _mesgul_kapat_ana(self):
        self._mesgul = False
        try:
            self.mesgul_bar.stop()
            self.mesgul_bar.pack_forget()
        except Exception:
            pass
        try:
            self.birincil_btn.configure(state="normal")
            self.geri_btn.configure(state="normal" if self.adim > 0 else "disabled")
        except Exception:
            pass
        self._birincil_yenile()

    def _kontrol_sync_thread(self, sessiz=False):
        if self._mesgul:
            return
        self._mesgul_ac(None)
        if not sessiz and self.adim == 3:
            self._durum_boya(self.sync_durum_var, self.sync_durum_lbl, "Kontrol ediliyor...", "amber")
        threading.Thread(target=self._kontrol_sync, daemon=True).start()

    def _kontrol_sync(self):
        try:
            if not esitleme.syncthing_exe():
                self.sync_ok = False
                self._ui(self._durum_boya, self.sync_durum_var, self.sync_durum_lbl,
                         "Syncthing kurulu değil — https://syncthing.net adresinden kur.", "kirmizi")
            else:
                self.sync.sessiz_baslat()
                kid = self.sync.kendi_kimligi()
                if kid:
                    self.sync_ok = True
                    self._ui(self.kendi_kod_var.set, kid)
                    self.ayar["kendiCihazKodu"] = kid
                    store.kaydet(self.ayar)
                    self._ui(self._durum_boya, self.sync_durum_var, self.sync_durum_lbl,
                             "Syncthing hazır ve çalışıyor.", "yesil")
                else:
                    self.sync_ok = False
                    self._ui(self._durum_boya, self.sync_durum_var, self.sync_durum_lbl,
                             "Syncthing kurulu ama yanıt vermiyor — programı bir kez aç.", "kirmizi")
        except Exception as e:
            self.sync_ok = False
            self._ui(self._durum_boya, self.sync_durum_var, self.sync_durum_lbl,
                     "Kontrol hatası: %s" % str(e)[:200], "kirmizi")
        finally:
            self._mesgul_kapat()

    def _kontrol_vpn_thread(self):
        if self._mesgul:
            return
        self._mesgul_ac(None)
        if self.adim == 4:
            self._durum_boya(self.vpn_durum_var, self.vpn_durum_lbl, "Kontrol ediliyor...", "amber")
        threading.Thread(target=self._kontrol_vpn, daemon=True).start()

    def _kontrol_vpn(self):
        try:
            if not vpn.kurulu_mu():
                self.vpn_kurulu = False
                self.vpn_bagli = False
                self._ui(self._durum_boya, self.vpn_durum_var, self.vpn_durum_lbl,
                         "Tailscale kurulu değil — https://tailscale.com/download adresinden kur.", "kirmizi")
            else:
                self.vpn_kurulu = True
                bagli, ip, _b = vpn.bagli_mi()
                self.vpn_bagli = bool(bagli)
                self.vpn_ip = ip or ""
                if bagli:
                    self._ui(self._durum_boya, self.vpn_durum_var, self.vpn_durum_lbl,
                             "Tailscale bağlı (%s)." % ip, "yesil")
                elif self._anahtar_var():
                    self._ui(self._durum_boya, self.vpn_durum_var, self.vpn_durum_lbl,
                             "Tailscale kurulu ama bağlı değil — Bağlan'a bas.", "amber")
                else:
                    self._ui(self._durum_boya, self.vpn_durum_var, self.vpn_durum_lbl,
                             "Tailscale kurulu. " + T.VPN_ANAHTARSIZ_NOTU, "amber")
        except Exception as e:
            self._ui(self._durum_boya, self.vpn_durum_var, self.vpn_durum_lbl,
                     "Kontrol hatası: %s" % str(e)[:200], "kirmizi")
        finally:
            self._mesgul_kapat()

    def _baglan_thread(self):
        if self._mesgul:
            return
        anahtar = self._cozulen_anahtar()
        if not anahtar:
            messagebox.showwarning("Anahtar yok", "Bağlanmak için önce VPN anahtarını gir (2. adım).")
            return
        ad = self.ad_var.get().strip() or "DgmCraft"
        self._mesgul_ac(None)
        if self.adim == 4:
            self._durum_boya(self.vpn_durum_var, self.vpn_durum_lbl, "Bağlanıyor...", "amber")
        threading.Thread(target=self._baglan, args=(anahtar, ad), daemon=True).start()

    def _baglan(self, anahtar, ad):
        try:
            ok, msg = vpn.baglan(anahtar, ad)
            if ok:
                try:
                    store.anahtar_kaydet(anahtar)
                    self.ayar["tailscaleAnahtariSakli"] = True
                    store.kaydet(self.ayar)
                except Exception:
                    pass
                bagli, ip, _b = vpn.bagli_mi()
                self.vpn_bagli = bool(bagli)
                self.vpn_ip = ip or ""
                self._ui(self._durum_boya, self.vpn_durum_var, self.vpn_durum_lbl,
                         "Tailscale bağlı (%s)." % (ip or "bağlandı"), "yesil")
            else:
                self._ui(self._durum_boya, self.vpn_durum_var, self.vpn_durum_lbl,
                         "Bağlanamadı: %s" % (msg or "")[:200], "kirmizi")
        except Exception as e:
            self._ui(self._durum_boya, self.vpn_durum_var, self.vpn_durum_lbl,
                     "Bağlantı hatası: %s" % str(e)[:200], "kirmizi")
        finally:
            self._mesgul_kapat()

    def _eslestir_thread(self):
        if self._mesgul:
            return
        k1 = self.kod1_var.get()
        k2 = self.kod2_var.get()
        kid = self.kendi_kod_var.get() or self.ayar.get("kendiCihazKodu", "")
        if not kid:
            messagebox.showwarning("Kod yok", "Kodun henüz alınamadı — biraz bekleyip tekrar dene.")
            return
        if not k1.strip() and not k2.strip():
            messagebox.showwarning("Kod yok", "En az 1 arkadaş kodu yapıştırmalısın, yoksa kimseyle eşitlenmezsin.")
            return
        for k in (k1, k2):
            if k.strip() and not esitleme.kod_gecerli_mi(k):
                messagebox.showwarning("Kod hatalı", "Kodlar çok kısa görünüyor. Kopyalarken eksik almış olabilirsin.")
                return
        self._mesgul_ac(None)
        if self.adim == 5:
            self._durum_boya(self.esles_durum_var, self.esles_durum_lbl, "Eşleştiriliyor...", "amber")
        threading.Thread(target=self._eslestir, args=(kid, k1, k2), daemon=True).start()

    def _eslestir(self, kid, k1, k2):
        try:
            self.sync.sessiz_baslat()
            self.sync.otomatik_yapilandir(kid, [k1, k2])
            self.ayar["kendiCihazKodu"] = kid
            self.ayar["arkadasKodlari"] = [k1.strip(), k2.strip()]
            store.kaydet(self.ayar)
            self.esles_ok = True
            self._ui(self._durum_boya, self.esles_durum_var, self.esles_durum_lbl,
                     "Eşleştirme tamam.", "yesil")
            self._ui(messagebox.showinfo, "Tamam", "Eşleştirme kaydedildi.")
        except Exception as e:
            self._ui(self._durum_boya, self.esles_durum_var, self.esles_durum_lbl,
                     "Eşleştirme başarısız: %s" % str(e)[:300], "kirmizi")
        finally:
            self._mesgul_kapat()

    def _esles_atla(self):
        if self._mesgul or self.esles_ok:
            return
        if messagebox.askyesno("Atla", "Arkadaş kodları olmadan devam ediyorsun — kimseyle eşitlenmezsin. Sonradan Ayarlar > Kurulum Sihirbazı ile ekleyebilirsin. Atlanılsın mı?"):
            self.esles_atlandi = True
            self._durum_boya(self.esles_durum_var, self.esles_durum_lbl, "Atlandı — sonra eklenebilir.", "amber")
            self._birincil_yenile()

    # ---------- bitir ----------
    def _bitir(self):
        ad = self.ad_var.get().strip()
        if not ad:
            self.adim = 1
            self._ciz()
            return
        if not self.sync_ok:
            self.adim = 3
            self._ciz()
            return
        if not self._anahtar_var() and not self.anahtar_atlandi:
            self.adim = 2
            self._ciz()
            return
        if self.vpn_kurulu and self._anahtar_var() and not self.vpn_bagli:
            self.adim = 4
            self._ciz()
            return
        if not self.esles_ok and not self.esles_atlandi:
            self.adim = 5
            self._ciz()
            return
        ilk_kurulum = not self.ayar.get("kurulumTamam")
        self.ayar["kurulumTamam"] = True
        self.ayar["kullaniciAdi"] = ad
        store.kaydet(self.ayar)
        if ilk_kurulum:
            # İlk kurulumda eldeki sürüm güncel sayılır (sonradan açılan
            # sihirbaz burayı ezmez, yoksa güncelleme kilidi delinirdi).
            try:
                from core import version as _V
                self.ayar["uygulananSurum"] = _V.oku().get("surum", "")
                store.kaydet(self.ayar)
            except Exception:
                pass
        try:
            yeni_kok = store.sunucu_kokunu_bul()
        except Exception:
            yeni_kok = self.kok
        self._tekerlek_temizle()
        self.destroy()
        try:
            self.bitince(yeni_kok)
        except TypeError:
            self.bitince()
