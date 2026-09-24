"""Arayüzler arası ortak servisler: Tkinter kabuğu da PySide6 kabuğu da bunu kullanır."""
import queue as _q


class Hizmetler:
    def __init__(self, kok, ayar):
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
