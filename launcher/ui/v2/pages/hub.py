# v2 Hub: hero + başlat/kilit + bellek + çevrimiçi + haberler. F1.
import queue
import threading
import tkinter as tk
from .. import tokens as T
from .. import widgets as W

BASLIK = "Hub"
IKON = "hub"
ACIKLAMA = "Sunucu durumu, başlatma, bellek, çevrimiçi oyuncular, haberler."

HEAP_SECENEKLERI = (2, 3, 4, 6)


class HubSayfasi:
    def __init__(self, hizmetler):
        self.hizmetler = hizmetler
        self.cerceve = None
        self._kuyruk = queue.Queue()
        self._izleyici = False
        self._rozet_var = None
        self._bilgi_var = None
        self._eylem_alani = None
        self._oyuncu_listesi = None
        self._oyuncu_bos = None
        self._haber_alani = None
        self._bellek_dugmeler = {}

    def kur(self, ebeveyn):
        self.cerceve = tk.Frame(ebeveyn, bg=T.BG)
        self._kur_hero()
        alt = tk.Frame(self.cerceve, bg=T.BG)
        alt.pack(fill="both", expand=True, pady=(T.KART_ARALIK, 0))
        sol = tk.Frame(alt, bg=T.BG)
        sol.pack(side="left", fill="both", expand=True, padx=(0, T.KART_ARALIK))
        self._kur_bellek(sol)
        self._kur_haberler(sol)
        self._kur_oyuncular(alt)
        return self.cerceve

    # ---------- hero ----------
    def _kur_hero(self):
        from core import assets as _A
        hero = tk.Frame(self.cerceve, bg="#0D1312", highlightthickness=1,
                        highlightbackground=T.CERCEVE)
        hero.pack(fill="x")
        tuval = tk.Canvas(hero, bg="#0D1312", highlightthickness=0, height=240)
        tuval.pack(fill="x")
        try:
            bg = _A.foto("v2", "hub-hero.png")
            if bg:
                self._hero_ref = bg
                tuval.create_image(500, 120, image=bg)
        except Exception:
            pass
        katman = tk.Frame(tuval, bg="#0D1312")
        try:
            katman.place(x=28, y=28)
        except Exception:
            pass
        self._rozet_var = tk.StringVar(value="HAZIR")
        self._rozet = tk.Label(katman, textvariable=self._rozet_var, font=("Inter", 9, "bold"),
                               bg="#12261C", fg=T.YESIL)
        self._rozet.pack(anchor="w")
        tk.Label(katman, text="Sunucuyu Başlat", font=("Chakra Petch", 26, "bold"),
                 bg="#0D1312", fg=T.YAZI).pack(anchor="w", pady=(8, 4))
        self._bilgi_var = tk.StringVar(value="3 kişilik özel Survival+ sunucun.")
        tk.Label(katman, textvariable=self._bilgi_var, font=T.FONT_METIN,
                 bg="#0D1312", fg=T.SOLUK, wraplength=560, justify="left").pack(anchor="w")
        self._eylem_alani = tk.Frame(katman, bg="#0D1312")
        self._eylem_alani.pack(anchor="w", pady=(14, 0))
        self._eylem_ciz("yukleniyor")

    def _eylem_ciz(self, durum, host=None):
        try:
            for w in self._eylem_alani.winfo_children():
                w.destroy()
        except Exception:
            pass
        if durum == "yukleniyor":
            tk.Label(self._eylem_alani, text="Durum okunuyor...",
                     font=T.FONT_METIN, bg="#0D1312", fg=T.SOLUK).pack(anchor="w")
        elif durum == "baslatilabilir":
            W.birincil_dugme(self._eylem_alani, "SUNUCUYU BAŞLAT", self._baslat).pack(anchor="w")
        elif durum == "misafir":
            tk.Label(self._eylem_alani, text="%s sunucuyu başlattı — ona katılabilirsin." % host,
                     font=("Inter", 12, "bold"), bg="#0D1312", fg=T.YAZI).pack(anchor="w")
        elif durum == "host":
            W.ikincil_dugme(self._eylem_alani, "Güvenli Kapat", self._guvenli_kapat).pack(anchor="w")
        elif durum == "bakim":
            tk.Label(self._eylem_alani, text="Bakım bitince buradan başlatırsın.",
                     font=T.FONT_METIN, bg="#0D1312", fg=T.SOLUK).pack(anchor="w")

    # ---------- bellek ----------
    def _kur_bellek(self, ebeveyn):
        kart = W.kart(ebeveyn)
        kart.pack(fill="x", pady=(0, T.KART_ARALIK))
        govde = tk.Frame(kart, bg=T.KART)
        govde.pack(fill="x", padx=14, pady=12)
        tk.Label(govde, text="SUNUCU BELLEĞİ", font=("Inter", 8, "bold"),
                 bg=T.KART, fg=T.SILIK).pack(anchor="w")
        satir = tk.Frame(govde, bg=T.KART)
        satir.pack(fill="x", pady=(8, 0))
        for gb in HEAP_SECENEKLERI:
            b = tk.Button(satir, text="%dG" % gb, font=("Inter", 11, "bold"),
                          relief="flat", padx=16, pady=6, cursor="hand2",
                          command=lambda v=gb: self._bellek_sec(v))
            b.pack(side="left", padx=(0, 8))
            self._bellek_dugmeler[gb] = b
        tk.Label(govde, text="Sonraki başlatmada geçerli olur.",
                 font=T.FONT_KUCUK, bg=T.KART, fg=T.SOLUK).pack(anchor="w", pady=(8, 0))
        self._bellek_boya()

    def _bellek_boya(self):
        secili = self.hizmetler.heap_al()
        for gb, b in self._bellek_dugmeler.items():
            try:
                if gb == secili:
                    b.configure(bg=T.VURGU, fg=T.VURGU_YAZI, activebackground=T.VURGU_HOVER)
                else:
                    b.configure(bg=T.YUZEY, fg=T.YAZI, activebackground="#1C2622")
            except Exception:
                pass

    def _bellek_sec(self, gb):
        try:
            self.hizmetler.heap_kaydet(gb)
            self._bellek_boya()
        except Exception:
            pass

    # ---------- haberler ----------
    def _kur_haberler(self, ebeveyn):
        kart = W.kart(ebeveyn)
        kart.pack(fill="both", expand=True)
        govde = tk.Frame(kart, bg=T.KART)
        govde.pack(fill="both", expand=True, padx=14, pady=12)
        tk.Label(govde, text="HABERLER", font=("Inter", 8, "bold"),
                 bg=T.KART, fg=T.SILIK).pack(anchor="w", pady=(0, 6))
        self._haber_alani = govde
        self._haber_ciz()

    def _haber_ciz(self):
        import os
        try:
            for w in list(self._haber_alani.winfo_children())[1:]:
                w.destroy()
        except Exception:
            pass
        for baslik, ozet in self._haber_oku()[:3]:
            satir = tk.Frame(self._haber_alani, bg=T.KART)
            satir.pack(fill="x", pady=3)
            tk.Label(satir, text="●", font=("Inter", 10), bg=T.KART, fg=T.VURGU).pack(side="left", padx=(0, 8))
            kutu = tk.Frame(satir, bg=T.KART)
            kutu.pack(side="left", fill="x", expand=True)
            tk.Label(kutu, text=baslik, font=("Inter", 11, "bold"), bg=T.KART, fg=T.YAZI, anchor="w").pack(fill="x")
            if ozet:
                tk.Label(kutu, text=ozet, font=T.FONT_KUCUK, bg=T.KART, fg=T.SOLUK,
                         anchor="w", wraplength=520, justify="left").pack(fill="x")

    def _haber_oku(self):
        import os
        yol = os.path.join(self.hizmetler.kok, "CHANGELOG.md")
        haberler = []
        try:
            with open(yol, "r", encoding="utf-8", errors="replace") as f:
                baslik, maddeler = "", []
                for satir in f:
                    s = satir.strip()
                    if s.startswith("## "):
                        if baslik:
                            haberler.append((baslik, "; ".join(maddeler[:2])))
                            if len(haberler) >= 3:
                                break
                        baslik = s[3:].strip()
                        maddeler = []
                    elif s.startswith("- ") and baslik:
                        maddeler.append(s[2:].strip()[:120])
                if baslik and len(haberler) < 3:
                    haberler.append((baslik, "; ".join(maddeler[:2])))
        except Exception:
            pass
        if not haberler:
            try:
                haberler = [("Sürüm %s" % self.hizmetler.surum, "")]
            except Exception:
                pass
        return haberler

    # ---------- oyuncular ----------
    def _kur_oyuncular(self, ebeveyn):
        kart = W.kart(ebeveyn)
        kart.pack(side="left", fill="y", padx=(0, 0))
        kart.configure(width=300)
        govde = tk.Frame(kart, bg=T.KART)
        govde.pack(fill="both", expand=True, padx=14, pady=12)
        tk.Label(govde, text="ÇEVRİMİÇİ", font=("Inter", 8, "bold"),
                 bg=T.KART, fg=T.SILIK).pack(anchor="w")
        self._oyuncu_bos = tk.Label(govde, text="Sunucu kapalıyken liste yok.",
                                    font=T.FONT_METIN, bg=T.KART, fg=T.SOLUK,
                                    wraplength=260, justify="left")
        self._oyuncu_bos.pack(anchor="w", pady=(8, 0))
        self._oyuncu_listesi = tk.Frame(govde, bg=T.KART)
        self._oyuncu_listesi.pack(fill="x", pady=(8, 0))
        W.ikincil_dugme(govde, "Davet Adresini Kopyala", self._davet_kopyala).pack(anchor="w", pady=(12, 0))

    def _davet_kopyala(self):
        try:
            from core import kilit as _K, vpn as _V
            adres = ""
            try:
                dolu, k = _K.kilit_dolu_mu(self.hizmetler.kok)
                if dolu and k.get("vpnIp"):
                    adres = "%s:%s" % (k.get("vpnIp"), k.get("port", 25565))
            except Exception:
                pass
            if not adres:
                try:
                    ip = _V.vpn_ip_bul()
                    if ip:
                        adres = "%s:25565" % ip
                except Exception:
                    pass
            if not adres:
                return
            self.cerceve.clipboard_clear()
            self.cerceve.clipboard_append(adres)
        except Exception:
            pass

    # ---------- durum döngüsü ----------
    def goster(self):
        self._izleyici = True
        try:
            import threading
            threading.Thread(target=self._yokla, daemon=True).start()
        except Exception:
            pass
        self._dongu()

    def gizle(self):
        self._izleyici = False

    def _dongu(self):
        if not self._izleyici:
            return
        try:
            import threading
            threading.Thread(target=self._yokla, daemon=True).start()
        except Exception:
            pass
        try:
            self.cerceve.after(10000, self._dongu)
        except Exception:
            pass

    def _yokla(self):
        try:
            from core import kilit as _K, sunucu as _S, version as _V
            if _V.guncelleniyor_mu():
                self._kuyruk.put_nowait(("rozet", ("BAKIMDA", "#2A2007", T.AMBER_HI)))
                self._kuyruk.put_nowait(("eylem", ("bakim", None)))
                self._kuyruk.put_nowait(("oyuncular", []))
                return
            try:
                proc = self.hizmetler.sunucu_al().proc
                calisiyor = bool(proc and proc.poll() is None)
            except Exception:
                calisiyor = False
            dolu, k = _K.kilit_dolu_mu(self.hizmetler.kok)
            if calisiyor:
                self._kuyruk.put_nowait(("rozet", ("YAYINDA", "#12261C", T.YESIL)))
                self._kuyruk.put_nowait(("eylem", ("host", None)))
            elif dolu:
                host = (k or {}).get("hostAdi", "Bir arkadaş")
                self._kuyruk.put_nowait(("rozet", ("MİSAFİR", "#15202E", T.MAVI)))
                self._kuyruk.put_nowait(("eylem", ("misafir", host)))
            else:
                self._kuyruk.put_nowait(("rozet", ("HAZIR", "#12261C", T.YESIL)))
                self._kuyruk.put_nowait(("eylem", ("baslatilabilir", None)))
            self._kuyruk.put_nowait(("oyuncular", self._oyuncu_oku() if (calisiyor or dolu) else []))
        except Exception:
            pass
        try:
            self.cerceve.after(500, self._bosalt)
        except Exception:
            pass

    def _bosalt(self):
        try:
            while True:
                tur, veri = self._kuyruk.get_nowait()
                if tur == "rozet":
                    metin, arka, yazi = veri
                    try:
                        self._rozet_var.set(metin)
                        self._rozet.configure(bg=arka, fg=yazi)
                    except Exception:
                        pass
                elif tur == "eylem":
                    durum, host = veri
                    try:
                        self._eylem_ciz(durum, host)
                        if durum == "bakim":
                            self._bilgi_var.set("Sunucu dosyaları güncelleniyor.")
                        elif durum == "misafir":
                            self._bilgi_var.set("Sürüm %s." % self.hizmetler.surum)
                    except Exception:
                        pass
                elif tur == "oyuncular":
                    self._oyuncu_ciz(veri)
        except queue.Empty:
            pass
        except Exception:
            pass

    def _oyuncu_oku(self):
        try:
            from core import sunucu as _S
            props = _S.server_properties_oku(self.hizmetler.kok)
            rc = _S.RconIstemcisi(port=props.get("rcon.port", "25575"),
                                  sifre=props.get("rcon.password", ""))
            ok, cevap = rc.komut("list")
            if not ok or not cevap:
                return []
            import re
            m = re.search(r":\s*(.+)$", cevap.strip().replace("\n", " "))
            if not m:
                return []
            return [a.strip() for a in m.group(1).split(",") if a.strip() and len(a.strip()) < 32][:20]
        except Exception:
            return []

    def _oyuncu_ciz(self, isimler):
        try:
            for w in self._oyuncu_listesi.winfo_children():
                w.destroy()
            if not isimler:
                self._oyuncu_bos.pack(anchor="w", pady=(8, 0))
                return
            self._oyuncu_bos.pack_forget()
            for ad in isimler:
                satir = tk.Frame(self._oyuncu_listesi, bg=T.KART)
                satir.pack(fill="x", pady=2)
                tk.Label(satir, text="●", font=("Inter", 9), bg=T.KART, fg=T.YESIL).pack(side="left", padx=(0, 6))
                tk.Label(satir, text=ad, font=("Inter", 11, "bold"), bg=T.KART, fg=T.YAZI).pack(side="left")
        except Exception:
            pass

    # ---------- başlat / kapat ----------
    def _baslat(self):
        try:
            from core import kilit as _K, version as _V, vpn as _V2
            if _V.guncelleniyor_mu():
                return
            dolu, k = _K.kilit_dolu_mu(self.hizmetler.kok)
            if dolu:
                return
            ad = self.hizmetler.kullanici
            try:
                _bagli, ip, _b = _V2.bagli_mi()
            except Exception:
                ip = ""
            _K.kilit_al(self.hizmetler.kok, ad, ip or "VPN yok")
            ok, mesaj = self.hizmetler.sunucu_al().baslat(self.hizmetler.heap_al())
            if not ok:
                _K.kilit_birak(self.hizmetler.kok)
        except Exception:
            pass
        self._yokla()

    def _guvenli_kapat(self):
        try:
            from core import kilit as _K
            import threading as _t

            def _is():
                try:
                    self.hizmetler.sunucu_al().guvenli_kapat(lambda m: None)
                except Exception:
                    pass
                try:
                    _K.kilit_birak(self.hizmetler.kok)
                except Exception:
                    pass
                self._yokla()

            _t.Thread(target=_is, daemon=True).start()
        except Exception:
            pass
