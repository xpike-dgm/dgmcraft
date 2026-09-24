"""Asset yükleyici: launcher/assets içindeki PNG/ICO dosyaları.
Kaynak çalışmada klasörden, exe'de paketten okur. Yalnızca stdlib + tkinter.
Bulunamazsa None döner; arayüzler her zaman desteksiz (fallback) çalışır."""
import os
import sys

_cache = {}


def kok():
    try:
        if getattr(sys, "frozen", False):
            base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
            aday = os.path.join(base, "launcher", "assets")
            if os.path.isdir(aday):
                return aday
            aday2 = os.path.join(os.path.dirname(sys.executable), "launcher", "assets")
            if os.path.isdir(aday2):
                return aday2
            return aday
    except Exception:
        pass
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def yol(*parca):
    return os.path.join(kok(), *parca)


def mevcut_mu(*parca):
    try:
        return os.path.isfile(yol(*parca))
    except Exception:
        return False


def foto(*parca):
    """tk.PhotoImage (PNG). Önbelleklidir, referans korunur. Yoksa None."""
    anahtar = "/".join(parca)
    if anahtar in _cache:
        return _cache[anahtar]
    try:
        import tkinter as tk
        p = yol(*parca)
        if not os.path.isfile(p):
            return None
        img = tk.PhotoImage(file=p)
        _cache[anahtar] = img
        return img
    except Exception:
        return None


def ikon_pencere(pencere):
    """Pencere simgesi (ICO). Başarısız olursa sessiz geçilir."""
    try:
        ico = yol("brand", "DgmCraft-app-icon.ico")
        if os.path.isfile(ico):
            pencere.iconbitmap(ico)
            return True
    except Exception:
        pass
    return False


def sabit_ikon_yolu(hedef_dizin):
    """Kısayollar için sabit konumlu ICO kopyası. Yol döndürür (yoksa '')."""
    try:
        kay = yol("brand", "DgmCraft-app-icon.ico")
        if not os.path.isfile(kay):
            return ""
        os.makedirs(hedef_dizin, exist_ok=True)
        hdf = os.path.join(hedef_dizin, "DgmCraft.ico")
        if not os.path.isfile(hdf):
            import shutil
            shutil.copy2(kay, hdf)
        return hdf
    except Exception:
        return ""
