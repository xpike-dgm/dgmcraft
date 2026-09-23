"""GitHub Releases üzerinden launcher güncellemesi.
Yalnızca launcher/, scripts/, site/, docs/ klasörlerine dokunur.
Sunucu içeriği (world, plugins, config) Syncthing + sürüm kilidiyle gelir.
Yalnızca stdlib."""
import json
import os
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile
from . import constants as C

UYGULANACAK_KLASORLER = ["launcher", "scripts", "site", "docs"]


def depo(ayar):
    try:
        return ((ayar or {}).get("githubRepo") or "").strip().strip("/")
    except Exception:
        return ""


def son_surum(repo, timeout=15):
    """(tag, notlar, zip_url) döndürür. Release yoksa ValueError."""
    req = urllib.request.Request(
        "https://api.github.com/repos/%s/releases/latest" % repo,
        headers={"User-Agent": "DgmCraft", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as y:
            veri = json.loads(y.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError("Henüz yayınlanmış sürüm yok.")
        raise RuntimeError("GitHub hatası (%s)." % e.code)
    except Exception as e:
        raise RuntimeError("Bağlantı hatası: %s" % str(e)[:200])
    tag = (veri.get("tag_name") or "").strip()
    if not tag:
        raise ValueError("Sürüm bilgisi okunamadı.")
    return tag, (veri.get("body") or ""), veri.get("zipball_url", "")


def denetle(ayar, timeout=15):
    repo = depo(ayar)
    if not repo:
        return {"kapali": True, "mesaj": "GitHub deposu ayarlanmamış (Ayarlar > GitHub repo)."}
    mevcut = C.PAKET_SURUMU
    tag, notlar, zip_url = son_surum(repo, timeout)
    return {
        "kapali": False,
        "repo": repo,
        "mevcut": mevcut,
        "son": tag,
        "guncelleme_var": tag != mevcut,
        "notlar": (notlar or "")[:1500],
        "zip_url": zip_url,
    }


def _kok_bul(ayiklanan):
    """zipball içindeki tek üst klasörü bul (sahip-sürüm/)."""
    for ad in os.listdir(ayiklanan):
        tam = os.path.join(ayiklanan, ad)
        if os.path.isdir(tam) and os.path.isfile(os.path.join(tam, "launcher", "app.py")):
            return tam
    raise ValueError("Paket doğrulanamadı (launcher/app.py yok).")


def uygula(kok, zip_url, durum_yaz=None, timeout=120):
    """Paketi indirip uygular. Sunucu çalışırken çağrılmamalı (UI kontrol eder)."""
    def _yaz(m):
        try:
            if durum_yaz:
                durum_yaz(m)
        except Exception:
            pass
    _yaz("Paket indiriliyor...")
    tmp = tempfile.mkdtemp(prefix="dgm-upd-")
    zip_yolu = os.path.join(tmp, "paket.zip")
    req = urllib.request.Request(zip_url, headers={"User-Agent": "DgmCraft"})
    with urllib.request.urlopen(req, timeout=timeout) as r, open(zip_yolu, "wb") as f:
        while True:
            parca = r.read(512 * 1024)
            if not parca:
                break
            f.write(parca)
    _yaz("Paket doğrulanıyor...")
    with zipfile.ZipFile(zip_yolu, "r") as z:
        z.extractall(tmp)
    kaynak = _kok_bul(tmp)
    yedek_kok = os.path.join(kok, "backups", "launcher-upd")
    try:
        os.makedirs(yedek_kok, exist_ok=True)
    except Exception:
        pass
    import time as _t
    yedek = os.path.join(yedek_kok, _t.strftime("%Y%m%d_%H%M%S"))
    for klasor in UYGULANACAK_KLASORLER:
        kyn = os.path.join(kaynak, klasor)
        hdf = os.path.join(kok, klasor)
        if not os.path.isdir(kyn):
            continue
        if os.path.isdir(hdf):
            try:
                shutil.copytree(hdf, os.path.join(yedek, klasor))
            except Exception:
                pass
        _yaz("%s güncelleniyor..." % klasor)
        for kok2, _, dosyalar in os.walk(kyn):
            for ad in dosyalar:
                s = os.path.join(kok2, ad)
                rel = os.path.relpath(s, kyn)
                h = os.path.join(hdf, rel)
                try:
                    os.makedirs(os.path.dirname(h), exist_ok=True)
                    shutil.copy2(s, h)
                except Exception:
                    continue
    try:
        shutil.rmtree(tmp, ignore_errors=True)
    except Exception:
        pass
    _yaz("Güncelleme uygulandı. Değişikliklerin geçmesi için uygulamayı kapatıp aç.")
    return True
