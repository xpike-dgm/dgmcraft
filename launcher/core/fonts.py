"""Gömülü font kaydı: pencere açılmadan önce bir kez çağrılır.
Windows'a özel, yönetici istemez, sistemi kirletmez (FR_PRIVATE).
Yalnızca stdlib (ctypes)."""
import ctypes
import os

DOSYALAR = [
    "Inter.ttf",
    "ChakraPetch-Regular.ttf",
    "ChakraPetch-SemiBold.ttf",
    "ChakraPetch-Bold.ttf",
]

AILELER = {
    "Inter.ttf": "Inter",
    "ChakraPetch-Regular.ttf": "Chakra Petch",
    "ChakraPetch-SemiBold.ttf": "Chakra Petch",
    "ChakraPetch-Bold.ttf": "Chakra Petch",
}


def dizin():
    try:
        from . import assets as _A
        d = _A.yol("fonts")
        if os.path.isdir(d):
            return d
    except Exception:
        pass
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts")


def kaydet():
    """Bulunan fontları bu işlem için kaydeder. Kayıtlı aile adlarını döndürür."""
    kayitli = []
    d = dizin()
    try:
        gdi = ctypes.windll.gdi32.AddFontResourceExW
    except Exception:
        return kayitli
    for ad in DOSYALAR:
        p = os.path.join(d, ad)
        try:
            if os.path.isfile(p) and gdi(p, 0x10, 0):
                kayitli.append(AILELER.get(ad, ad))
        except Exception:
            continue
    return kayitli
