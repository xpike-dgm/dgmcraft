"""docs/kilavuz.md dosyasını komut kataloğuna çevirir (kategori + komut + alanlar).
Dosya ~74 KB, ayrıştırma birkaç milisaniye sürer; bu yüzden önbellek dosyası yok.
Arayüzler (site/launcher) aynı kaynaktan beslenir."""
import io
import os
import re

KATEGORI = re.compile(r"^##\s+(?:\d+\s*[)-]+\s*)?(.+?)\s*$")
KOMUT = re.compile(r"^###\s+(.+?)\s*$")
ALAN = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$")

ALAN_ADLARI = {
    "ne ise yarar": "aciklama",
    "ornek": "ornek",
    "orjinal komutu": "orijinal",
    "orijinal komutu": "orijinal",
    "dikkat": "dikkat",
    "admin": "admin",
    "izin": "izin",
}


def _normalize(metin):
    """Türkçe duyarsız arama anahtarı: küçük harf, aksan atılmış, sadeleştirilmiş."""
    try:
        s = (metin or "").lower()
        cevir = {"ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g",
                 "ü": "u", "Ü": "u", "ö": "o", "Ö": "o", "ç": "c", "Ç": "c"}
        for a, b in cevir.items():
            s = s.replace(a, b)
        return re.sub(r"\s+", " ", s).strip()
    except Exception:
        return (metin or "").lower()


def _komut_temizle(metin):
    return (metin or "").strip().strip("`").strip()


def katalog_oku(kok):
    """{'kategoriler': [{'ad','aciklama','komutlar':[...]}], 'sayi': n} döner."""
    yol = os.path.join(kok, "docs", "kilavuz.md")
    kategoriler = []
    toplam = 0
    try:
        with io.open(yol, encoding="utf-8", errors="replace") as f:
            satirlar = f.read().splitlines()
    except Exception:
        return {"kategoriler": [], "sayi": 0, "hata": "docs/kilavuz.md bulunamadı"}

    kategori = None
    komut = None
    for satir in satirlar:
        satir = satir.strip()
        if satir.startswith("### "):
            m = KOMUT.match(satir)
            if m and kategori is not None:
                komut = {"ad": _komut_temizle(m.group(1)), "aciklama": "",
                         "ornek": "", "orijinal": "", "izin": ""}
                komut["arama"] = _normalize(komut["ad"])
                kategori["komutlar"].append(komut)
                toplam += 1
            continue
        if satir.startswith("## "):
            m = KATEGORI.match(satir)
            if m:
                kategori = {"ad": m.group(1), "aciklama": "", "komutlar": [],
                            "kisa": _kisa_ad(m.group(1))}
                kategori["arama"] = _normalize(kategori["ad"])
                kategoriler.append(kategori)
            komut = None
            continue
        if kategori is None:
            continue
        m = ALAN.match(satir)
        if m:
            alan = ALAN_ADLARI.get(_normalize(m.group(1)))
            if komut is not None and alan:
                komut[alan] = (komut.get(alan, "") + " " + m.group(2)).strip()
            elif alan == "aciklama" and not kategori["aciklama"]:
                kategori["aciklama"] = m.group(2).strip()
            continue
        if komut is None and satir and not satir.startswith("#"):
            kategori["aciklama"] = (kategori["aciklama"] + " " + satir).strip()

    for kategori in kategoriler:
        if not kategori["komutlar"]:
            continue
        for komut in kategori["komutlar"]:
            komut["arama"] = _normalize(" ".join([
                komut["ad"], komut.get("aciklama", ""), komut.get("ornek", ""),
                komut.get("orijinal", ""), komut.get("dikkat", "")]))
    kategoriler = [k for k in kategoriler if k["komutlar"]]
    return {"kategoriler": kategoriler, "sayi": toplam}


def _kisa_ad(ad):
    """Kategori adından kısa etiket: '3-) Ekonomi (Vault)' -> 'Ekonomi'."""
    s = re.sub(r"^\d+\s*[)-]+\s*", "", ad or "").strip()
    s = re.sub(r"\s*\(.*?\)\s*$", "", s).strip()
    return s or (ad or "")


def ara(veri, sorgu, en_fazla=200):
    """Tüm kategorilerde arama. [{'kategori': ad, 'komut': {..}}] döner."""
    q = _normalize(sorgu)
    if not q:
        return []
    sonuc = []
    for kategori in veri.get("kategoriler", []):
        for komut in kategori.get("komutlar", []):
            if q in komut.get("arama", "") or q in kategori.get("arama", ""):
                sonuc.append({"kategori": kategori["ad"], "kisa": kategori["kisa"],
                              "komut": komut})
                if len(sonuc) >= en_fazla:
                    return sonuc
    return sonuc
