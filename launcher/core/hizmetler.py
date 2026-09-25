"""Arayüzler arası ortak servisler: Tkinter kabuğu da PySide6 kabuğu da bunu kullanır."""
import queue as _q
import threading


class Hizmetler:
    def __init__(self, kok, ayar, gorev_onizleme=False):
        self.kok = kok
        self.ayar = ayar
        self.gorev_onizleme = bool(gorev_onizleme)
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

    # ---------- host akışı (kilit + kalp atışı + site) ----------
    def host_mu(self):
        try:
            from core import kilit as _K
            dolu, k = _K.kilit_dolu_mu(self.kok)
            if dolu and (k or {}).get("hostAdi") == self.kullanici:
                return True
        except Exception:
            pass
        try:
            proc = self.sunucu_al().proc
            return bool(proc and proc.poll() is None)
        except Exception:
            return False

    def sunucu_baslat(self):
        """Kilit al → sunucuyu başlat → kalp atışını başlat.
        (ok, mesaj) döner. Başlatılamazsa kilit geri bırakılır."""
        try:
            from core import kilit as _K, version as _V, vpn as _Vpn
        except Exception as e:
            return False, "Servisler yüklenemedi: %s" % e
        try:
            if _V.guncelleniyor_mu():
                return False, "Sunucu dosyaları güncelleniyor, biraz sonra dene."
        except Exception:
            pass
        try:
            dolu, k = _K.kilit_dolu_mu(self.kok)
            if dolu and (k or {}).get("hostAdi") != self.kullanici:
                return False, "%s sunucuyu açık tutuyor, ona katılabilirsin." % (
                    (k or {}).get("hostAdi", "Bir arkadaş"))
        except Exception:
            pass
        ip = ""
        try:
            _bagli, ip, _bilgi = _Vpn.bagli_mi()
        except Exception:
            ip = ""
        try:
            port = int(self.ayar.get("port", 25565) or 25565)
        except Exception:
            port = 25565
        try:
            _K.kilit_al(self.kok, self.kullanici, ip or "VPN yok", port)
        except Exception as e:
            return False, "Kilit alınamadı: %s" % e
        ok, mesaj = self.sunucu_al().baslat(heap_gb=self.heap_al())
        if not ok:
            try:
                _K.kilit_birak(self.kok)
            except Exception:
                pass
            return False, mesaj
        if getattr(self, "_kalp", None) is None:
            self._kalp = _K.KalpAtisi(self.kok)
        try:
            self._kalp.baslat()
        except Exception:
            pass
        threading.Thread(target=self._site_otomatik, daemon=True).start()
        return True, mesaj

    def _site_otomatik(self):
        try:
            from core import site as _S, vpn as _Vpn
            _bagli, ip, _b = _Vpn.bagli_mi()
            if not ip:
                return
            port = int(self.ayar.get("sitePort", 8000) or 8000)
            if getattr(self, "site_srv", None) is None:
                self.site_srv = _S.SiteSunucusu(self.kok)
            self.site_srv.baslat(ip, port)
        except Exception:
            pass

    def sunucu_kapat(self, ilerleme=None, zorla=False):
        """Güvenli kapat → kilit bırak → kalp atışını durdur."""
        yaz = ilerleme or (lambda _m: None)
        try:
            kapandi = True
            proc = self.sunucu_al().proc
            if proc and proc.poll() is None:
                if zorla:
                    self.sunucu_al().zorla_kapat()
                else:
                    kapandi = self.sunucu_al().guvenli_kapat(yaz)
        except Exception as e:
            return False, str(e)[:300]
        try:
            from core import kilit as _K
            _K.kilit_birak(self.kok)
            if getattr(self, "_kalp", None) is not None:
                self._kalp.durdur()
        except Exception:
            pass
        return bool(kapandi), "Sunucu kapatıldı." if kapandi else "Sunucu kapanmadı."
