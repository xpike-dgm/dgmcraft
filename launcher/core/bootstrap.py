"""İlk kurulum: küçük dosyalar paketten, büyükler indirme/eşitleme ile. Dünya gömülmez."""
import json
import os
import shutil


def gomulu_kopyala(ilerleme=None):
    from . import paths
    src = paths.embedded_dir()
    dst = paths.work_dir()
    if not os.path.isdir(src):
        return 0
    say = 0
    for kok, _, dosyalar in os.walk(src):
        for ad in dosyalar:
            s = os.path.join(kok, ad)
            rel = os.path.relpath(s, src)
            if rel.lower().startswith("world"):
                continue
            if "runtime" in rel.lower().split(os.sep):
                continue
            h = os.path.join(dst, rel)
            if os.path.isfile(h):
                continue
            os.makedirs(os.path.dirname(h), exist_ok=True)
            shutil.copy2(s, h)
            say += 1
    return say


def server_properties_guvence(kok):
    """server.properties yoksa örnekten kurar; RCON anahtarlarını garantiler.
    Mevcut dosyanın diğer ayarlarına dokunmaz, sadece 3 satırı düzeltir."""
    import secrets
    yol = os.path.join(kok, "server.properties")
    if not os.path.isfile(yol):
        ornek = os.path.join(kok, "server.properties.example")
        try:
            if os.path.isfile(ornek):
                shutil.copy2(ornek, yol)
            else:
                with open(yol, "w", encoding="utf-8") as f:
                    f.write("server-port=25565\nenable-rcon=true\nrcon.port=25575\n")
        except Exception:
            return False
    try:
        with open(yol, "r", encoding="utf-8", errors="replace") as f:
            satirlar = f.read().splitlines()
    except Exception:
        return False
    anahtarlar = {}
    for i, s in enumerate(satirlar):
        t = s.strip()
        if t and not t.startswith("#") and "=" in t:
            anahtarlar[t.split("=", 1)[0].strip()] = i
    izle = []

    def _koy(k, v):
        if k in anahtarlar:
            i = anahtarlar[k]
            if satirlar[i].split("=", 1)[1].strip() != v:
                satirlar[i] = "%s=%s" % (k, v)
                izle.append(k)
        else:
            satirlar.append("%s=%s" % (k, v))
            izle.append(k)

    _koy("enable-rcon", "true")
    _koy("rcon.port", "25575")
    mevcut_sifre = ""
    if "rcon.password" in anahtarlar:
        mevcut_sifre = satirlar[anahtarlar["rcon.password"]].split("=", 1)[1].strip()
    if not mevcut_sifre:
        _koy("rcon.password", secrets.token_urlsafe(24))
    if izle:
        tmp = yol + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("\n".join(satirlar) + "\n")
        os.replace(tmp, yol)
    return True


def java_eksik_mi(kok=None):
    from . import paths
    w = kok or paths.work_dir()
    # runtime/ altındaki herhangi bir java.exe yeterli
    if os.path.isfile(os.path.join(w, "runtime", "bin", "java.exe")):
        return False
    rt = os.path.join(w, "runtime")
    if os.path.isdir(rt):
        for ad in os.listdir(rt):
            if os.path.isfile(os.path.join(rt, ad, "bin", "java.exe")):
                return False
    return True


def version_tohumla():
    """work_dir/version.json yoksa embedded sürümü kopyala."""
    from . import paths
    try:
        dst = os.path.join(paths.work_dir(), "version.json")
        if os.path.isfile(dst):
            return False
        src = os.path.join(paths.embedded_dir(), "version.json")
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            return True
    except Exception:
        pass
    return False


def calisma_klasorunu_hazirla(dev_koku=None):
    """Arkadaş PC'sinde ilk açılış: gömülü dosyaları work_dir'e kopyala + version tohumla.
    Sahip PC'sinde (dev_koku içinde purpur.jar varsa) kopya yapmaz, dev kökü kullanılır.
    Dönüş: (work_dir, kaynaktan_kullanilan_kok)"""
    from . import paths
    w = paths.work_dir()
    version_tohumla()
    gomulu_kopyala()
    # Eğer work_dir'de purpur.jar yoksa ama dev kökte varsa, sahibi modundayız:
    # work_dir'e kopyalamak yerine dev kökü kullan (çift dünya oluşmasın).
    if dev_koku and os.path.isfile(os.path.join(dev_koku, "purpur.jar")):
        if not os.path.isfile(os.path.join(w, "purpur.jar")):
            return w, dev_koku
    return w, w
