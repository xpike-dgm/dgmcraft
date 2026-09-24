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
        self._eylem_dugmesi = None
        self._oyuncu_listesi = None
        self._oyuncu_bos = None
        self._haber_alani = None
        self._bellek_kaydirici = None

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
        hero = tk.Frame(self.cerceve, bg=T.KART, highlightthickness=1,
                        highlightbackground=T.CERCEVE)
        hero.pack(fill="x")
        tuval = tk.Canvas(hero, bg=T.KART, highlightthickness=0, height=212)
        tuval.pack(fill="x")
        self._hero_tuval = tuval
        try:
            zemin = W.gradyan(tuval, 1072, 212, "#17211D", "#101614", anahtar="hero-arka")
            if zemin:
                self._hero_zemin = zemin
                tuval.create_image(0, 0, image=zemin, anchor="nw")
        except Exception:
            pass
        try:
            bg = _A.olcek("v2", "hub-hero-soft.png", yukseklik=182)
            if bg:
                self._hero_ref = bg
                tuval.create_image(800, 106, image=bg)
        except Exception:
            pass
        try:
            serit = W.gradyan_serit("#17211D", "#101614", 212) or ["#141B18"]
            isik = W.parlama(tuval, 620, 200, T.VURGU, guc=0.13, zemin=serit,
                             merkez=(150, 150), anahtar="hero-isik")
            if isik:
                self._hero_isik = isik
                tuval.create_image(150, 150, image=isik)
        except Exception:
            pass
        # Durum rozeti: hap şeklinde koyu kutu + nokta + yazı
        self._rozet_kutu = tuval.create_rectangle(30, 26, 96, 48, fill="#131A17",
                                                  outline="#1E2A25", width=1)
        tuval.create_oval(35, 34, 41, 40, fill=T.YESIL, outline="")
        self._rozet_yazi = tuval.create_text(47, 37, anchor="w", text="HAZIR",
                                             fill=T.SOLUK, font=("Inter", 8))
        tuval.create_text(30, 78, anchor="w", text="Sunucuyu Başlat",
                          fill=T.YAZI, font=T.FONT_HERO)
        self._bilgi_yazi = tuval.create_text(
            30, 100, anchor="nw", text="3 kişilik özel Survival+ sunucun.",
            fill=T.SOLUK, font=("Inter", 9), width=430)
        self._eylem_alani = None
        self._eylem_dugmesi = None
        self._eylem_yazi = None
        self._eylem_ciz("yukleniyor")

    def _eylem_ciz(self, durum, host=None):
        try:
            for w in self._eylem_alani.winfo_children():
                w.destroy()
        except Exception:
            pass
        self._eylem_dugmesi = None
        self._eylem_yazi = None
        if durum == "yukleniyor":
            self._eylem_yazi = self._hero_tuval.create_text(
                30, 140, anchor="w", text="Durum okunuyor...",
                fill=T.SILIK, font=("Inter", 9))
        elif durum == "baslatilabilir":
            self._eylem_dugmesi = W.OvalDugme(
                self._hero_tuval, "Sunucuyu Başlat", self._baslat,
                vurgu=True, genislik=176, yukseklik=38, bg="#141B18")
            self._eylem_dugmesi.place(x=30, y=124)
        elif durum == "misafir":
            self._eylem_yazi = self._hero_tuval.create_text(
                30, 143, anchor="w",
                text="%s sunucuyu başlattı — ona katılabilirsin." % host,
                fill=T.YAZI, font=("Inter", 10))
        elif durum == "host":
            self._eylem_dugmesi = W.OvalDugme(
                self._hero_tuval, "Güvenli Kapat", self._guvenli_kapat,
                vurgu=False, genislik=150, yukseklik=38, bg="#141B18")
            self._eylem_dugmesi.place(x=30, y=124)
        elif durum == "bakim":
            self._eylem_yazi = self._hero_tuval.create_text(
                30, 143, anchor="w", text="Bakım bitince buradan başlatırsın.",
                fill=T.SILIK, font=("Inter", 9))

    # ---------- bellek ----------
    def _kur_bellek(self, ebeveyn):
        kart = W.kart(ebeveyn)
        kart.pack(fill="x", pady=(0, T.KART_ARALIK))
        govde = tk.Frame(kart, bg=T.KART)
        govde.pack(fill="x", padx=16, pady=14)
        ust_satir = tk.Frame(govde, bg=T.KART)
        ust_satir.pack(fill="x")
        tk.Label(ust_satir, text="SUNUCU BELLEĞİ", font=T.FONT_ETIKET,
                 bg=T.KART, fg=T.SILIK).pack(side="left")
        self._bellek_rozet = tk.Label(ust_satir, text="", font=("Inter", 9),
                                      bg=T.KART, fg=T.VURGU)
        self._bellek_rozet.pack(side="right")
        tk.Label(govde, text="Sunucuya ayrılacak maksimum RAM miktarı",
                 font=T.FONT_KUCUK, bg=T.KART, fg=T.SOLUK).pack(anchor="w", pady=(2, 10))
        secili = self.hizmetler.heap_al()
        baslangic = HEAP_SECENEKLERI.index(secili) if secili in HEAP_SECENEKLERI else 1
        self._bellek_kaydirici = W.AdimSlider(
            govde, degerler=[("%dG" % gb, gb) for gb in HEAP_SECENEKLERI],
            baslangic=baslangic, komut=self._bellek_sec, genislik=418,
            rozet=self._bellek_rozet)
        self._bellek_kaydirici.pack(fill="x", pady=(0, 2))
        tk.Label(govde, text="Sonraki başlatmada geçerli olur.",
                 font=T.FONT_KUCUK, bg=T.KART, fg=T.SILIK).pack(anchor="w", pady=(2, 0))

    def _bellek_sec(self, gb):
        try:
            self.hizmetler.heap_kaydet(gb)
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
            tk.Label(kutu, text=baslik, font=("Inter", 10), bg=T.KART, fg=T.YAZI, anchor="w").pack(fill="x")
            if ozet:
                tk.Label(kutu, text=ozet, font=T.FONT_KUCUK, bg=T.KART, fg=T.SOLUK,
                         anchor="w", wraplength=520, justify="left").pack(fill="x")

    def _haber_oku(self):
        from core import haber as _H
        try:
            return _H.changelog_oku(self.hizmetler.kok, 3)
        except Exception:
            return []

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
        W.OvalDugme(govde, "Davet Adresini Kopyala", self._davet_kopyala,
                    vurgu=False, genislik=186, yukseklik=32,
                    bg=T.KART).pack(anchor="w", pady=(14, 0))

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
                self._kuyruk.put_nowait(("rozet", ("BAKIMDA", "#2A2007", T.VURGU_HOVER)))
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

    def _bilgi_degistir(self, metin):
        try:
            self._hero_tuval.itemconfigure(self._bilgi_yazi, text=metin)
        except Exception:
            pass

    def _bosalt(self):
        try:
            while True:
                tur, veri = self._kuyruk.get_nowait()
                if tur == "rozet":
                    metin, arka, yazi = veri
                    try:
                        self._rozet_yazi2 = self._hero_tuval.itemconfigure(
                            self._rozet_yazi, text=metin, fill=yazi)
                    except Exception:
                        pass
                elif tur == "eylem":
                    durum, host = veri
                    try:
                        self._eylem_ciz(durum, host)
                        if durum == "bakim":
                            self._bilgi_degistir("Sunucu dosyaları güncelleniyor.")
                        elif durum == "misafir":
                            self._bilgi_degistir("Sürüm %s." % self.hizmetler.surum)
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
                tk.Label(satir, text=ad, font=("Inter", 10), bg=T.KART, fg=T.YAZI).pack(side="left")
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
