"""Asset yükleyici: launcher/assets içindeki PNG/ICO dosyaları.
Kaynak çalışmada klasörden, exe'de paketten okur. Yalnızca stdlib + tkinter.
Bulunamazsa None döner; arayüzler her zaman desteksiz (fallback) çalışır."""
import os
import sys

_cache = {}


def _frozen_adaylar(*parca):
    """Exe paketi içi arama: kök + _internal (PyInstaller 6 tek-klasör düzeni)."""
    try:
        import sys as _sys
        if getattr(_sys, "frozen", False):
            base = getattr(_sys, "_MEIPASS", os.path.dirname(_sys.executable))
            exe_dizini = os.path.dirname(_sys.executable)
            for kok in (base, exe_dizini):
                for alt in (os.path.join(*parca), os.path.join("_internal", *parca)):
                    aday = os.path.join(kok, alt)
                    if os.path.isdir(aday):
                        return aday
    except Exception:
        pass
    return ""


def kok():
    aday = _frozen_adaylar("launcher", "assets")
    if aday:
        return aday
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


def kucult(*parca, hedef=20):
    """PNG'yi hedef boyutta PhotoImage yapar. Pillow varsa kaliteli (LANCZOS),
    yoksa Tk'nin yerleşik azaltması. 48px ray ikonlarını 20px'e indirmek için."""
    anahtar = "kucuk:%d:%s" % (hedef, "/".join(parca))
    if anahtar in _cache:
        return _cache[anahtar]
    resim = None
    try:
        import base64
        import io
        from PIL import Image
        p = yol(*parca)
        if os.path.isfile(p):
            ham = Image.open(p).convert("RGBA")
            w, h = ham.size
            k = hedef / float(max(1, min(w, h)))
            yeni = ham.resize((max(1, int(w * k)), max(1, int(h * k))), Image.LANCZOS)
            tampon = io.BytesIO()
            yeni.save(tampon, format="PNG")
            import tkinter as tk
            resim = tk.PhotoImage(data=base64.b64encode(tampon.getvalue()))
    except Exception:
        resim = None
    if resim is None:
        kaynak = foto(*parca)
        if kaynak is None:
            return None
        try:
            w = int(kaynak.width())
            if w <= hedef:
                resim = kaynak
            else:
                resim = kaynak.subsample(max(1, int(round(w / float(hedef)))))
        except Exception:
            return None
    _cache[anahtar] = resim
    return resim


def olcek(*parca, genislik=None, yukseklik=None):
    """En-boy oranını koruyarak kutuya sığdırır (Pillow yoksa Tk azaltması)."""
    kutu = "olc:%s:%s:%s" % (genislik, yukseklik, "/".join(parca))
    if kutu in _cache:
        return _cache[kutu]
    resim = None
    try:
        import base64
        import io
        from PIL import Image
        p = yol(*parca)
        if os.path.isfile(p):
            ham = Image.open(p).convert("RGBA")
            w, h = ham.size
            k = 1.0
            if genislik:
                k = min(k, genislik / float(w))
            if yukseklik:
                k = min(k, yukseklik / float(h))
            yeni = ham.resize((max(1, int(w * k)), max(1, int(h * k))), Image.LANCZOS)
            tampon = io.BytesIO()
            yeni.save(tampon, format="PNG")
            import tkinter as tk
            resim = tk.PhotoImage(data=base64.b64encode(tampon.getvalue()))
    except Exception:
        resim = None
    if resim is None:
        kaynak = foto(*parca)
        if kaynak is None:
            return None
        try:
            w, h = int(kaynak.width()), int(kaynak.height())
            adim = 1
            if genislik and w > genislik:
                adim = max(adim, int(round(w / float(genislik))))
            if yukseklik and h > yukseklik:
                adim = max(adim, int(round(h / float(yukseklik))))
            resim = kaynak.subsample(adim, adim) if adim > 1 else kaynak
        except Exception:
            return None
    _cache[kutu] = resim
    return resim


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
