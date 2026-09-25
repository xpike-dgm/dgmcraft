"""F4 — Durum verisi: Plan (SQLite) + RCON.

Plan her ~10 saniyede bir örnek yazar (plugins/Plan/database.db, plan_tps tablosu).
TPS/MSPT/CPU/RAM buradan okunur; oyuncu listesi RCON 'list' ile alınır.
Sunucu kapalıyken son örnekten "kapalı" durumu üretilir (yanlış canlı veri göstermemek için)."""
import os
import sqlite3
import time

PLAN_DB = os.path.join("plugins", "Plan", "database.db")
TPS_HEDEF = 20.0


def plan_ornegi(kok, son_adet=60):
    """plan_tps tablosundan eskiye doğru örnek listesi. [{'t','tps','mspt',...}]"""
    yol = os.path.join(kok, PLAN_DB)
    if not os.path.isfile(yol):
        return []
    satirlar = []
    try:
        bag = sqlite3.connect("file:%s?mode=ro" % yol.replace("\\", "/"), uri=True,
                              timeout=1.5)
        try:
            sorgu = ("select date, tps, mspt_average, cpu_usage, ram_usage,"
                     " players_online, entities, chunks_loaded, free_disk_space"
                     " from plan_tps order by id desc limit ?")
            for satir in bag.execute(sorgu, (max(1, int(son_adet)),)):
                satirlar.append({
                    "t": int(satir[0] or 0) / 1000.0,
                    "tps": float(satir[1] or 0),
                    "mspt": float(satir[2] or 0),
                    "cpu": float(satir[3] or 0),
                    "ram": int(satir[4] or 0),
                    "oyuncu": int(satir[5] or 0),
                    "varlik": int(satir[6] or 0),
                    "chunk": int(satir[7] or 0),
                    "disk": int(satir[8] or 0),
                })
        finally:
            bag.close()
    except Exception:
        return []
    satirlar.reverse()
    return satirlar


def baslangic_zamani(kok):
    """Çalışma süresi: kilit dosyasındaki başlangıç zamanı (ISO) veya 0."""
    try:
        from core import kilit as _K
        dolu, k = _K.kilit_dolu_mu(kok)
        if not dolu or not k:
            return 0.0
        import datetime
        metin = k.get("baslamaZamani") or ""
        if not metin:
            return 0.0
        dt = datetime.datetime.fromisoformat(metin)
        return dt.timestamp()
    except Exception:
        return 0.0


def oyuncular(kok):
    """RCON 'list' → [isim]. Sunucu kapalıysa []."""
    try:
        from core import sunucu as _S
        props = _S.server_properties_oku(kok)
        rc = _S.RconIstemcisi(port=props.get("rcon.port", 25575),
                              sifre=props.get("rcon.password", ""))
        ham = rc.komut("list") or ""
        liste = []
        for parca in ham.split(":"):
            parca = parca.strip()
            if not parca or ", " not in parca:
                continue
            ad, _bolum = parca.split(", ", 1)
            ad = ad.strip()
            if ad:
                liste.append(ad)
        return liste
    except Exception:
        return []


def rcon_aktif_mi(kok):
    try:
        from core import sunucu as _S
        props = _S.server_properties_oku(kok)
        rc = _S.RconIstemcisi(port=props.get("rcon.port", 25575),
                              sifre=props.get("rcon.password", ""))
        ok, _cevap = rc.komut("list")
        return bool(ok)
    except Exception:
        return False


def durum_topla(kok, rcon_dene=True):
    """Sayfanın ihtiyacı olan tek sözlük. Canlı değilse 'canli': False."""
    ornekler = plan_ornegi(kok, 60)
    canli = rcon_aktif_mi(kok) if rcon_dene else False
    veri = {
        "canli": canli,
        "ornekler": ornekler,
        "tps": None, "mspt": None, "cpu": None, "ram": None,
        "oyuncular": [], "varlik": None, "chunk": None, "disk": None,
        "sure": None, "ornek_yasi": None,
    }
    if ornekler:
        son = ornekler[-1]
        veri.update({
            "tps": son["tps"], "mspt": son["mspt"], "cpu": son["cpu"],
            "ram": son["ram"], "varlik": son["varlik"], "chunk": son["chunk"],
            "disk": son["disk"], "ornek_yasi": max(0, int(time.time() - son["t"])),
        })
    if canli:
        veri["oyuncular"] = oyuncular(kok)
    elif ornekler:
        veri["oyuncular"] = []
    bas = baslangic_zamani(kok)
    if canli and bas:
        veri["sure"] = max(0, int(time.time() - bas))
    return veri


def tps_renk(tps):
    if tps is None:
        return "#6E7F76"
    if tps >= 19.0:
        return "#34D399"
    if tps >= 15.0:
        return "#F5C86B"
    return "#FB7185"


def sure_bicim(saniye):
    try:
        s = int(max(0, saniye or 0))
        gun, kalan = divmod(s, 86400)
        saat, kalan = divmod(kalan, 3600)
        dakika, san = divmod(kalan, 60)
        if gun:
            return "%dg %dsa %dd" % (gun, saat, dakika)
        if saat:
            return "%dsa %dd" % (saat, dakika)
        return "%dd %dsn" % (dakika, san)
    except Exception:
        return "-"
