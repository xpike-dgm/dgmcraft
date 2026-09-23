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
    """(tag, notlar, zip_url, asset_url) döndürür. Release yoksa ValueError."""
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
    asset_url = ""
    try:
        for a in (veri.get("assets") or []):
            ad = (a.get("name") or "").lower()
            if ad.endswith(".zip") and a.get("browser_download_url"):
                asset_url = a["browser_download_url"]
                break
    except Exception:
        pass
    return tag, (veri.get("body") or ""), veri.get("zipball_url", ""), asset_url


def denetle(ayar, timeout=15):
    repo = depo(ayar)
    if not repo:
        return {"kapali": True, "mesaj": "GitHub deposu ayarlanmamış (Ayarlar > GitHub repo)."}
    try:
        taban = ((ayar or {}).get("launcherSurumu") or "").strip() or C.PAKET_SURUMU
    except Exception:
        taban = C.PAKET_SURUMU
    tag, notlar, zip_url, asset_url = son_surum(repo, timeout)
    return {
        "kapali": False,
        "repo": repo,
        "mevcut": taban,
        "son": tag,
        "guncelleme_var": tag != taban,
        "notlar": (notlar or "")[:1500],
        "zip_url": zip_url,
        "asset_url": asset_url,
    }


def _kok_bul(ayiklanan):
    """zipball içindeki tek üst klasörü bul (sahip-sürüm/)."""
    for ad in os.listdir(ayiklanan):
        tam = os.path.join(ayiklanan, ad)
        if os.path.isdir(tam) and os.path.isfile(os.path.join(tam, "launcher", "app.py")):
            return tam
    raise ValueError("Paket doğrulanamadı (launcher/app.py yok).")


def _indir(url, hedef, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "DgmCraft"})
    with urllib.request.urlopen(req, timeout=timeout) as r, open(hedef, "wb") as f:
        while True:
            parca = r.read(512 * 1024)
            if not parca:
                break
            f.write(parca)


def uygula(kok, sonuc, durum_yaz=None, timeout=120):
    """Paketi indirip uygular. Sunucu çalışırken çağrılmamalı (UI kontrol eder).
    Kaynaktan çalışıyorsa dosyaların üstüne yazar; exe ile çalışıyorsa yeni
    klasöre çıkarır (çalışan exe'nin üstüne yazılamaz). (hedef, exe_mi) döndürür."""
    import sys
    exe_mi = bool(getattr(sys, "frozen", False))
    if exe_mi:
        return _uygula_exe(sonuc, durum_yaz, timeout), True

    def _yaz(m):
        try:
            if durum_yaz:
                durum_yaz(m)
        except Exception:
            pass
    zip_url = (sonuc or {}).get("zip_url", "")
    if not zip_url:
        raise ValueError("İndirme adresi alınamadı.")
    _yaz("Paket indiriliyor...")
    tmp = tempfile.mkdtemp(prefix="dgm-upd-")
    zip_yolu = os.path.join(tmp, "paket.zip")
    _indir(zip_url, zip_yolu, timeout)
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
    return kok, False


def _uygula_exe(sonuc, durum_yaz=None, timeout=120):
    """Exe ile çalışanlar için: Release zipini exe yanına yeni klasöre çıkarır."""
    import sys

    def _yaz(m):
        try:
            if durum_yaz:
                durum_yaz(m)
        except Exception:
            pass
    asset_url = (sonuc or {}).get("asset_url", "")
    if not asset_url:
        raise ValueError("Exe paketi bu sürümde yok.")
    exe_dizini = os.path.dirname(sys.executable)
    tag = (sonuc.get("son") or "yeni").strip().replace("/", "-")
    hedef = os.path.join(exe_dizini, "DgmCraft-%s" % tag)
    _yaz("Exe paketi indiriliyor...")
    tmp = tempfile.mkdtemp(prefix="dgm-upd-")
    zip_yolu = os.path.join(tmp, "paket.zip")
    _indir(asset_url, zip_yolu, timeout)
    _yaz("Paket açılıyor...")
    if os.path.isdir(hedef):
        shutil.rmtree(hedef, ignore_errors=True)
    os.makedirs(hedef, exist_ok=True)
    with zipfile.ZipFile(zip_yolu, "r") as z:
        z.extractall(hedef)
    try:
        shutil.rmtree(tmp, ignore_errors=True)
    except Exception:
        pass
    _yaz("Yeni sürüm klasöre açıldı.")
    return hedef
