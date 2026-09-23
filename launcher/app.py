"""Giriş noktası. Tek EXE / tek klasör ile çalışır. Yalnızca stdlib + tkinter."""
import os
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import store, esitleme, bootstrap
from ui.wizard import Wizard
from ui.main import AnaPencere


def main():
    # Çalışma klasörünü hazırla (gömülü dosyalar + version tohumu + RCON güvencesi).
    try:
        bootstrap.version_tohumla()
        bootstrap.gomulu_kopyala()
    except Exception:
        pass
    kok = store.sunucu_kokunu_bul()
    try:
        bootstrap.server_properties_guvence(kok)
    except Exception:
        pass
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
