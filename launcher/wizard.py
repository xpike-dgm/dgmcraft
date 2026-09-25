"""Kurulum sihirbazını tek başına çalıştıran giriş noktası.
PySide6 uygulamasındaki "Kurulum Sihirbazı" düğmesi bunu ayrı süreçte açar.
Kullanım: python launcher/wizard.py | DgmCraft-Sihirbaz.bat"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    import tkinter as tk
    from core import store
    from core.esitleme import SyncthingYonetici
    from core import fonts
    from ui.wizard import Wizard

    try:
        fonts.kaydet()
    except Exception:
        pass
    kok = store.sunucu_kokunu_bul()
    ayar = store.yukle()
    kok_pencere = tk.Tk()
    kok_pencere.withdraw()

    def bitti():
        try:
            store.kaydet(ayar)
        except Exception:
            pass
        try:
            kok_pencere.quit()
        except Exception:
            pass

    pencere = Wizard(kok_pencere, kok, ayar, SyncthingYonetici(kok), bitti,
                     kapatilabilir=True)
    try:
        pencere.deiconify()
        pencere.lift()
        pencere.focus_force()
    except Exception:
        pass
    kok_pencere.mainloop()


if __name__ == "__main__":
    main()
