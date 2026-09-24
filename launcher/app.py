"""Giriş noktası. Tek EXE / tek klasör ile çalışır. Yalnızca stdlib + tkinter."""
import os
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import store, esitleme, bootstrap
from ui.wizard import Wizard
from ui.main import AnaPencere


def main():
    # Splash: marka ekranı, hazırlık bitene kadar açık kalır.
    splash = None
    try:
        from core import version as _V
        from ui.splash import Splash
        splash = Splash(surum=_V.oku().get("surum", ""))
        splash.mesaj("Hazırlanıyor...")
        splash.update_idletasks()
        splash.update()
    except Exception:
        splash = None

    def _kapat_splash():
        try:
            if splash:
                splash.kapat()
        except Exception:
            pass

    # Exe ile çalışıyorsa tek seferlik AppData kurulumu önce gelir.
    if getattr(sys, "frozen", False):
        try:
            from core import kurulum as _K
            if _K.gerekli():
                _kapat_splash()
                splash = None
                from ui.kurulum import KurulumPenceresi
                w = KurulumPenceresi()
                w.mainloop()
                return
        except Exception:
            pass
    # Çalışma klasörünü hazırla (gömülü dosyalar + version tohumu + RCON güvencesi).
    try:
        if splash:
            splash.mesaj("Dosyalar doğrulanıyor...")
            splash.update()
        bootstrap.version_tohumla()
        bootstrap.gomulu_kopyala()
    except Exception:
        pass
    kok = store.sunucu_kokunu_bul()
    try:
        if splash:
            splash.mesaj("Ayarlar okunuyor...")
            splash.update()
        bootstrap.server_properties_guvence(kok)
    except Exception:
        pass
    _kapat_splash()
    splash = None
    ayar = store.yukle()
    sync = esitleme.SyncthingYonetici(kok)
    if not ayar.get("kurulumTamam"):
        kok2 = {"kok": kok}

        def bitince(yeni_kok=None):
            try:
                kok2["kok"] = yeni_kok or store.sunucu_kokunu_bul()
            except Exception:
                pass

        gizli = tk.Tk()
        gizli.withdraw()
        wiz = Wizard(gizli, kok, ayar, sync, lambda yk=None: bitince(yk))
        # Pencere kapanana kadar bekle (sihirbaz içinden destroy edilir).
        try:
            gizli.wait_window(wiz)
        except Exception:
            pass
        try:
            gizli.destroy()
        except Exception:
            pass
        ayar2 = store.yukle()
        if not ayar2.get("kurulumTamam"):
            # Kullanıcı sihirbazı bitirmeden kapattıysa sessiz çık.
            return
        app = AnaPencere(kok2["kok"], ayar2)
        app.mainloop()
    else:
        app = AnaPencere(kok, ayar)
        app.mainloop()


if __name__ == "__main__":
    main()
