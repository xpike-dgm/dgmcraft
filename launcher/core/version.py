"""Sürüm damgası. Sahip güncellerken Başlat kapalı kalır."""
import json
import os
from . import paths


def dosya():
    return os.path.join(paths.work_dir(), "version.json")


def oku():
    try:
        with open(dosya(), "r", encoding="utf-8") as f:
            d = json.load(f)
            if not isinstance(d, dict):
                raise ValueError("bozuk")
            return {
                "surum": d.get("surum", "bilinmiyor") or "bilinmiyor",
                "guncelleniyor": bool(d.get("guncelleniyor")),
                "notlar": d.get("notlar", d.get("aciklama", "")) or "",
            }
    except Exception:
        return {"surum": "bilinmiyor", "guncelleniyor": False, "notlar": ""}


def yaz(surum, guncelleniyor=False, notu=""):
    tmp = dosya() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"surum": surum, "guncelleniyor": bool(guncelleniyor),
                   "notlar": notu, "aciklama": notu}, f, ensure_ascii=False, indent=2)
    os.replace(tmp, dosya())


def yayinla(yeni_surum, notlar=""):
    yaz((yeni_surum or "").strip(), True, notlar or "")
    return (yeni_surum or "").strip()


def bitir_guncelleme():
    v = oku()
    yaz(v.get("surum", "bilinmiyor"), False, v.get("notlar", ""))
    return v.get("surum", "bilinmiyor")


def guncelleniyor_mu():
    try:
        return bool(oku().get("guncelleniyor"))
    except Exception:
        return False
