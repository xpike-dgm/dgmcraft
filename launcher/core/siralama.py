"""F6 — Sıralama: iki kaynak.

1) Canlı: ajLeaderboards'ın kendi tabloları (sunucu açıkken RCON 'ajlb list' ve
   'ajlb list <board>'). Sunucuda tablo tanımlı değilse boş döner.
2) Yerel: Essentials (para, son görülme) ve AuraSkills (yetenek toplamı) dosyaları.
   Bunlar doğrudan okunur, sunucu kapalıyken de çalışır.

Kaynak her tabloda ayrıca yazılır; hiçbir sayı uydurulmaz."""
import io
import os
import re
import time

ESSENTIALS_DIZIN = os.path.join("plugins", "Essentials", "userdata")
AURASKILLS_DIZIN = os.path.join("plugins", "AuraSkills", "userdata")
BOS_DEGER = object()


def _oku(yol):
    try:
        with io.open(yol, encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except Exception:
        return []


def _alan(yol, anahtar):
    for satir in _oku(yol):
        s = satir.strip()
        if s.startswith(anahtar + ":"):
            deger = s.split(":", 1)[1].strip().strip("'\"")
            return deger
    return None


def _sayis(metin):
    try:
        s = str(metin).replace(",", "").replace(".", "").replace(" ", "")
        s = re.sub(r"[^0-9]", "", s)
        return float(s) if s else 0.0
    except Exception:
        return 0.0


# ---------- yerel tablolar ----------
def _essentials_kayitlari(kok):
    dizin = os.path.join(kok, ESSENTIALS_DIZIN)
    liste = []
    try:
        dosyalar = os.listdir(dizin)
    except Exception:
        return liste
    for dosya in dosyalar:
        if not dosya.endswith(".yml"):
            continue
        yol = os.path.join(dizin, dosya)
        ad = _alan(yol, "last-account-name") or dosya[:-4][:8]
        para = _sayis(_alan(yol, "money") or 0)
        cikis = _sayis(_alan_cikis(yol))
        giris = _sayis(_alan_giris(yol))
        sure = max(0.0, (cikis - giris) / 60000.0) if cikis and giris else 0.0
        liste.append({"ad": ad, "para": para, "son": cikis, "sure": sure})
    return liste


def _alan_giris(yol):
    giris = None
    for satir in _oku(yol):
        s = satir.strip()
        if s.startswith("timestamps:"):
            continue
        if s.startswith("login:"):
            giris = s.split(":", 1)[1].strip()
    return giris


def _alan_cikis(yol):
    for satir in _oku(yol):
        s = satir.strip()
        if s.startswith("logout:"):
            return s.split(":", 1)[1].strip()
    return None


def _yetenek_toplamlari(kok):
    dizin = os.path.join(kok, AURASKILLS_DIZIN)
    liste = []
    try:
        dosyalar = os.listdir(dizin)
    except Exception:
        return liste
    for dosya in dosyalar:
        if not dosya.endswith(".yml"):
            continue
        yol = os.path.join(dizin, dosya)
        ad = _ad_bul(kok, dosya[:-4]) or dosya[:-4][:8]
        toplam_seviye = 0
        toplam_xp = 0.0
        for satir in _oku(yol):
            s = satir.strip()
            if s.startswith("level:"):
                toplam_seviye += int(_sayis(s.split(":", 1)[1]))
            elif s.startswith("xp:"):
                toplam_xp += _sayis(s.split(":", 1)[1])
        liste.append({"ad": ad, "seviye": toplam_seviye, "xp": toplam_xp})
    return liste


def _ad_bul(kok, uuid):
    yol = os.path.join(kok, ESSENTIALS_DIZIN, uuid + ".yml")
    return _alan(yol, "last-account-name")


def yerel_tablolar(kok):
    kayitlar = _essentials_kayitlari(kok)
    yetenekler = _yetenek_toplamlari(kok)
    tablolar = []
    if kayitlar:
        sırala = sorted(kayitlar, key=lambda x: -x["para"])[:10]
        tablolar.append({
            "ad": "En zengin", "birim": "₺", "kaynak": "yerel veri (Essentials)",
            "satirlar": [{"sira": i + 1, "ad": k["ad"], "deger": k["para"],
                          "metin": "%s ₺" % _para(k["para"])}
                         for i, k in enumerate(sırala)],
        })
        son = sorted([k for k in kayitlar if k["son"]], key=lambda x: -x["son"])[:10]
        if son:
            tablolar.append({
                "ad": "En son oynayan", "birim": "", "kaynak": "yerel veri (Essentials)",
                "satirlar": [{"sira": i + 1, "ad": k["ad"],
                              "deger": k["son"],
                              "metin": _zaman(k["son"])} for i, k in enumerate(son)],
            })
        sure = sorted([k for k in kayitlar if k["sure"] > 0], key=lambda x: -x["sure"])[:10]
        if sure:
            tablolar.append({
                "ad": "En uzun oynayan", "birim": "dk", "kaynak": "yerel veri (Essentials)",
                "satirlar": [{"sira": i + 1, "ad": k["ad"], "deger": k["sure"],
                              "metin": "%d dk" % int(k["sure"])} for i, k in enumerate(sure)],
            })
    if yetenekler:
        sırala = sorted(yetenekler, key=lambda x: (-x["seviye"], -x["xp"]))[:10]
        tablolar.append({
            "ad": "En yetenekli", "birim": "sv", "kaynak": "yerel veri (AuraSkills)",
            "satirlar": [{"sira": i + 1, "ad": k["ad"], "deger": k["seviye"],
                          "metin": "%d seviye" % k["seviye"]} for i, k in enumerate(sırala)],
        })
    return tablolar


def _para(deger):
    try:
        deger = float(deger)
        if deger >= 1000000:
            return "%.1fM" % (deger / 1000000)
        if deger >= 1000:
            return "%.1fB" % (deger / 1000)
        return "%d" % deger
    except Exception:
        return "0"


def _zaman(ms):
    try:
        fark = max(0, int(time.time() * 1000) - int(ms))
        dk = fark // 60000
        if dk < 60:
            return "%d dk önce" % dk
        sa = dk // 60
        if sa < 24:
            return "%d sa önce" % sa
        return "%d gün önce" % (sa // 24)
    except Exception:
        return "-"


# ---------- canlı tablolar (ajLeaderboards) ----------
def _rcon(kok, komut, timeout=6):
    try:
        from core import sunucu as _S
        props = _S.server_properties_oku(kok)
        rc = _S.RconIstemcisi(port=props.get("rcon.port", 25575),
                              sifre=props.get("rcon.password", ""))
        return rc.komut(komut, timeout=timeout)
    except Exception:
        return False, ""


def canli_tablolar(kok):
    """Sunucudaki ajLeaderboards tabloları. Sunucu kapalıysa []."""
    ok, cevap = _rcon(kok, "ajlb list")
    if not ok or not (cevap or "").strip():
        return []
    adlar = []
    for satir in (cevap or "").splitlines():
        s = satir.strip().lstrip("-*• ").strip()
        if not s:
            continue
        if ":" in s and not s.lower().startswith(("boards", "board", "kullanim", "usage")):
            s = s.split(":", 1)[1].strip()
        if s and s not in adlar:
            adlar.append(s)
    tablolar = []
    for ad in adlar[:8]:
        _ok, ic = _rcon(kok, "ajlb list %s" % ad, timeout=8)
        satirlar = _sirala_coz(ic)
        if satirlar:
            tablolar.append({"ad": ad, "birim": "", "kaynak": "ajLeaderboards",
                             "satirlar": satirlar})
    return tablolar


def _sirala_coz(metin):
    """'/ajl list <board>' çıktısından satırları çözer. Dayanıklı: sıra, isim, değer."""
    satirlar = []
    for satir in (metin or "").splitlines():
        s = satir.strip()
        if not s:
            continue
        s = re.sub(r"§[0-9A-FK-ORa-fk-orx]", "", s).strip()
        m = re.match(r"^(\d+)[.)]\s*(.+)$", s)
        if not m:
            continue
        sira = int(m.group(1))
        kalan = m.group(2).strip()
        parcalar = re.split(r"\s+[-–—:]\s+|\t+|\s{2,}", kalan)
        parcalar = [p.strip() for p in parcalar if p.strip()]
        if not parcalar:
            continue
        ad = parcalar[0]
        deger_metin = parcalar[1] if len(parcalar) > 1 else ""
        satirlar.append({"sira": sira, "ad": ad,
                         "deger": _sayis(deger_metin) if deger_metin else 0.0,
                         "metin": deger_metin or "-"})
    return satirlar


def tablolar(kok, canli_dene=True):
    canli = canli_tablolar(kok) if canli_dene else []
    if canli:
        return canli, True
    return yerel_tablolar(kok), False


TABLO_YOK_METNI = (
    "Sunucuda henüz sıralama tablosu tanımlı değil.\n"
    "Oyun içinde şu komutlarla açabilirsin:\n"
    "  /ajlb add %vault_eco_balance% para\n"
    "  /ajlb add %player_time_played% oynama\n"
    "  /ajlb add %statistic_mob_kills% oldurme")
