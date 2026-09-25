"""F5 — Yetenekler: AuraSkills oyuncu verisi (userdata/*.yml) + sunucu ayarları.

Gösterilen her sayı doğrulanabilir kaynaktan gelir:
- seviye ve XP: plugins/AuraSkills/userdata/<uuid>.yml
- sonraki seviye XP'si: plugins/AuraSkills/xp_requirements.yml formülü
- "yeni yetenek açılır" sayısı: plugins/AuraSkills/abilities.yml unlock değerleri
Uydurma değer konmaz; veri yoksa "veri yok" yazılır."""
import io
import os
import re

VERI_DIZIN = os.path.join("plugins", "AuraSkills", "userdata")
XP_DOSYA = os.path.join("plugins", "AuraSkills", "xp_requirements.yml")
YETENEK_DOSYA = os.path.join("plugins", "AuraSkills", "abilities.yml")
ESSENTIALS_DIZIN = os.path.join("plugins", "Essentials", "userdata")

# AuraSkills iç anahtarı -> arayüz adı / ikon adı
SKILL_AD = {
    "foraging": ("Toplama", "woodcutting"),
    "farming": ("Çiftçilik", "farming"),
    "defense": ("Savunma", "defense"),
    "agility": ("Çeviklik", "agility"),
    "alchemy": ("Alşimi", "alchemy"),
    "archery": ("Okçuluk", "archery"),
    "enchanting": ("Büyücülük", "magic"),
    "mining": ("Madencilik", "mining"),
    "excavation": ("Kazı", "excavation"),
    "fishing": ("Balıkçılık", "fishing"),
    "fighting": ("Savaş", "combat"),
    "acrobatics": ("Akrobasi", "agility"),
    "sniper": ("Keskin Nişancı", "archery"),
    "woodcutting": ("Odunculuk", "woodcutting"),
}


def _yaml_satirlar(yol):
    try:
        with io.open(yol, encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except Exception:
        return []


def oyuncular(kok):
    """[{uuid, ad}] — AuraSkills userdata + Essentials'ten isim eşlemesi."""
    liste = []
    dizin = os.path.join(kok, VERI_DIZIN)
    try:
        dosyalar = os.listdir(dizin)
    except Exception:
        return liste
    for dosya in dosyalar:
        if not dosya.endswith(".yml"):
            continue
        uuid = dosya[:-4]
        ad = isim_bul(kok, uuid)
        liste.append({"uuid": uuid, "ad": ad})
    liste.sort(key=lambda x: (x["ad"] or x["uuid"]).lower())
    return liste


def isim_bul(kok, uuid):
    yol = os.path.join(kok, ESSENTIALS_DIZIN, uuid + ".yml")
    for satir in _yaml_satirlar(yol):
        s = satir.strip()
        if s.startswith("last-account-name:"):
            return s.split(":", 1)[1].strip().strip("'\"") or ""
    return ""


def xp_kurallari(kok):
    """xp_requirements.yml'deki varsayılan formül: {'multiplier','base','expression'}"""
    kural = {"multiplier": 100.0, "base": 100.0, "expression": ""}
    for satir in _yaml_satirlar(os.path.join(kok, XP_DOSYA)):
        s = satir.strip()
        if s.startswith("expression:"):
            kural["expression"] = s.split(":", 1)[1].strip().strip("'\"")
        elif s.startswith("multiplier:"):
            try:
                kural["multiplier"] = float(s.split(":", 1)[1].strip())
            except Exception:
                pass
        elif s.startswith("base:"):
            try:
                kural["base"] = float(s.split(":", 1)[1].strip())
            except Exception:
                pass
    return kural


def xp_gereken(mevcut_seviye, kural):
    """AuraSkills varsayılan formülü: multiplier * (level - 2)^2 + base.
    'level' = sonraki seviye numarasıdır (AuraSkills davranışı)."""
    try:
        sonraki = int(mevcut_seviye) + 1
        m = float(kural.get("multiplier", 100.0))
        b = float(kural.get("base", 100.0))
        return max(1.0, m * ((sonraki - 2) ** 2) + b)
    except Exception:
        return 100.0


def yetenekler(kok, uuid):
    """Seçili oyuncu için yetenek listesi."""
    yol = os.path.join(kok, VERI_DIZIN, "%s.yml" % uuid)
    satirlar = _yaml_satirlar(yol)
    kural = xp_kurallari(kok)
    acilis = acilis_ozeti(kok)
    liste = []
    aktif = None
    for satir in satirlar:
        ham = satir
        s = satir.strip()
        if s.startswith("skills:"):
            continue
        if s.startswith("-") or not s:
            continue
        girinti = len(ham) - len(ham.lstrip())
        if ":" not in s:
            continue
        anahtar, deger = s.split(":", 1)
        anahtar = anahtar.strip()
        deger = deger.strip()
        if girinti <= 2 and anahtar.startswith("auraskills/"):
            aktif = anahtar.split("/", 1)[1]
            liste.append({"anahtar": aktif, "seviye": 0, "xp": 0.0})
            continue
        if aktif is None:
            continue
        for alan in liste[::-1]:
            if alan["anahtar"] == aktif:
                if anahtar == "level":
                    try:
                        alan["seviye"] = int(float(deger))
                    except Exception:
                        alan["seviye"] = 0
                elif anahtar == "xp":
                    try:
                        alan["xp"] = float(deger)
                    except Exception:
                        alan["xp"] = 0.0
                break
    for alan in liste:
        ad, ikon = SKILL_AD.get(alan["anahtar"], (alan["anahtar"].capitalize(),
                                                alan["anahtar"]))
        alan["ad"] = ad
        alan["ikon"] = ikon
        alan["gerekli"] = xp_gereken(alan["seviye"], kural)
        alan["oran"] = 0.0
        if alan["gerekli"] > 0:
            alan["oran"] = max(0.0, min(1.0, alan["xp"] / alan["gerekli"]))
        alan["sonraki_acilis"] = _sonraki_acilis(alan["seviye"], acilis)
    liste.sort(key=lambda x: (-x["oran"], x["ad"]))
    return liste


def acilis_ozeti(kok):
    """abilities.yml'deki unlock değerlerinden {seviye: adet}.
    '{start}+2' -> o yetenek, ilgili yeteneğin başlangıç seviyesine +2'de açılır."""
    yol = os.path.join(kok, YETENEK_DOSYA)
    sonuc = {}
    for satir in _yaml_satirlar(yol):
        s = satir.strip()
        if not s.startswith("unlock:"):
            continue
        deger = s.split(":", 1)[1].strip().strip("'\"")
        m = re.search(r"start\}\s*\+\s*(\d+)", deger)
        if not m:
            continue
        seviye = int(m.group(1))
        sonuc[seviye] = sonuc.get(seviye, 0) + 1
    return sonuc


def _sonraki_acilis(mevcut_seviye, acilis):
    """Bir sonraki yetenek açılışı: (seviye, adet) veya (0, 0)."""
    for seviye in sorted(acilis or {}):
        if seviye > mevcut_seviye:
            return seviye, acilis[seviye]
    return 0, 0
