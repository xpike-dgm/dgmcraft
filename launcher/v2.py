"""v2 giriş noktası: yeni kabuk. Eski uygulama aynen durur (DgmCraft-Baslat.bat).
Kullanım: python launcher/v2.py  |  DgmCraft-v2.bat"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    from core import fonts
    try:
        fonts.kaydet()
    except Exception:
        pass
    from core import store
    from ui.v2.shell import Kabuk
    kok = store.sunucu_kokunu_bul()
    ayar = store.yukle()
    app = Kabuk(kok, ayar)
    app.mainloop()


if __name__ == "__main__":
    main()
