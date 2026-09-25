"""Ayar deposu + sunucu kökü bulma. Yalnızca standart kütüphane."""
import json
import os
import sys


def exe_dizini():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    # launcher/core/store.py -> launcher -> sunucu kökü (bir üst)
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def sunucu_kokunu_bul():
    # Öncelik: gömülü çalışma klasörü (AppData) kuruluysa onu kullan.
    # Yoksa geliştirme/portable kökü (purpur.jar yanı) kullan.
    try:
        from . import paths as _P
        w = os.path.abspath(_P.work_dir())
        if os.path.isfile(os.path.join(w, "purpur.jar")):
            return w
    except Exception:
        pass
    for aday in (exe_dizini(), os.getcwd()):
        aday = os.path.abspath(aday)
        if os.path.isfile(os.path.join(aday, "purpur.jar")):
            return aday
    try:
        from . import paths as _P2
        return os.path.abspath(_P2.work_dir())
    except Exception:
        pass
    return os.path.abspath(exe_dizini())


def veri_dizini():
    # paths.appdata ile aynı konumu kullan (tek kaynak).
    try:
        from . import paths as _P
        return _P.appdata()
    except Exception:
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        yol = os.path.join(base, "DgmCraft")
        os.makedirs(yol, exist_ok=True)
        return yol


def ayar_dosyasi():
    return os.path.join(veri_dizini(), "launcher.json")


VARSAYILAN_AYAR = {
    "kurulumTamam": False,
    "kullaniciAdi": "",
    "sitePort": 8000,
    "kendiCihazKodu": "",
    "arkadasKodlari": ["", ""],
    "tailscaleAnahtariSakli": False,
    "sonEsitleme": "",
    "uygulananSurum": "",
    "githubRepo": "",
    "heapGB": 3,
}


def yukle():
    try:
        with open(ayar_dosyasi(), "r", encoding="utf-8") as f:
            veri = json.load(f)
        out = dict(VARSAYILAN_AYAR)
        out.update(veri if isinstance(veri, dict) else {})
        return out
    except Exception:
        return dict(VARSAYILAN_AYAR)


def kaydet(ayar):
    tmp = ayar_dosyasi() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ayar, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ayar_dosyasi())


def anahtar_dosyasi():
    return os.path.join(veri_dizini(), "tailscale.key")


def anahtar_kaydet(key):
    yol = anahtar_dosyasi()
    with open(yol, "w", encoding="utf-8") as f:
        f.write((key or "").strip())
    try:
        import subprocess
        ad = os.environ.get("USERNAME", "")
        if ad:
            subprocess.run(
                ["icacls", yol, "/inheritance:r", "/grant:r", ad + ":F"],
                capture_output=True, timeout=10,
            )
    except Exception:
        pass


def anahtar_oku():
    try:
        with open(anahtar_dosyasi(), "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def ai_anahtar_dosyasi():
    return os.path.join(veri_dizini(), "openai.key")


def ai_anahtar_kaydet(key):
    yol = ai_anahtar_dosyasi()
    with open(yol, "w", encoding="utf-8") as f:
        f.write((key or "").strip())
    try:
        import subprocess
        ad = os.environ.get("USERNAME", "")
        if ad:
            subprocess.run(
                ["icacls", yol, "/inheritance:r", "/grant:r", ad + ":F"],
                capture_output=True, timeout=10,
            )
    except Exception:
        pass


def ai_anahtar_oku():
    try:
        with open(ai_anahtar_dosyasi(), "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def kurulum_anahtari_oto_bul(sunucu_koku):
    aday = os.path.join(sunucu_koku, "kurulum-anahtari.txt")
    try:
        with open(aday, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def sahip_durumu(sunucu_koku):
    """'evet' | 'hayir' | 'bilinmiyor'

    Eşitlenen `.sahip` dosyası tek başına yeterli değil: Syncthing onu
    arkadaşlara da kopyalayabiliyor. Bu yüzden karar, yalnızca bu bilgisayarda
    duran yerel bir işaretle verilir; ilk kez çalışınca kullanıcıya bir kez
    sorulur."""
    try:
        from . import constants as _C
        isaret = os.path.join(veri_dizini(), _C.SAHIP_DOSYASI)
        if os.path.isfile(isaret):
            try:
                with open(isaret, "r", encoding="utf-8") as f:
                    return (f.read().strip() or "hayir")
            except Exception:
                return "hayir"
        if os.path.isfile(os.path.join(sunucu_koku, _C.SAHIP_DOSYASI)):
            return "bilinmiyor"
    except Exception:
        pass
    return "hayir"


def sahip_isaretle(sunucu_koku, deger):
    """Bu bilgisayarın sahip olup olmadığını kalıcı olarak işaretler."""
    try:
        from . import constants as _C
        isaret = os.path.join(veri_dizini(), _C.SAHIP_DOSYASI)
        deger = "evet" if deger in (True, "evet", "yes", 1) else "hayir"
        os.makedirs(veri_dizini(), exist_ok=True)
        with open(isaret, "w", encoding="utf-8") as f:
            f.write(deger)
        return deger
    except Exception:
        return "hayir"


def sahip_mi(sunucu_koku):
    """Sahip kipi: yalnızca bu bilgisayar sahip olarak işaretlenmişse True.
    Arkadaşların makinelerinde `.sahip` eşitlenmiş olsa bile False döner."""
    return sahip_durumu(sunucu_koku) == "evet"
