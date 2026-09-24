"""FAZ 3: Tailscale gömülü yönetim. Key kodda sabit değil."""
import json
import os
import re
import shutil
import subprocess
import urllib.request
from . import constants as C

CREATE_NO_WINDOW = 0x08000000


def program_files():
    for k in ("ProgramW6432", "ProgramFiles"):
        v = os.environ.get(k)
        if v:
            return v
    return os.path.join(os.environ.get("SystemDrive", "C:") + "\\", "Program Files")


def tailscale_exe():
    for aday in [
        os.path.join(program_files(), "Tailscale", "tailscale.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Tailscale", "tailscale.exe"),
    ]:
        if aday and os.path.isfile(aday):
            return aday
    return shutil.which("tailscale") or ""


def kurulu_mu():
    return bool(tailscale_exe())


def msi_indir(hedef_klasor, ilerleme=None):
    os.makedirs(hedef_klasor, exist_ok=True)
    hedef = os.path.join(hedef_klasor, "tailscale-setup.msi")
    if os.path.isfile(hedef):
        return hedef
    req = urllib.request.Request(C.TAILSCALE_INDIRME_ADRESI, headers={"User-Agent": "DgmCraft"})
    with urllib.request.urlopen(req, timeout=120) as r, open(hedef, "wb") as f:
        toplam = int(r.headers.get("Content-Length", "0") or 0)
        okunan = 0
        while True:
            parca = r.read(256 * 1024)
            if not parca:
                break
            f.write(parca)
            okunan += len(parca)
            if ilerleme and toplam:
                try:
                    ilerleme(okunan / toplam)
                except Exception:
                    pass
    return hedef


def sessiz_kur(msi_yolu):
    """(basarili_mi, mesaj) döndürür. Kurulum ilerlemesi görünür (/passive),
    böylece Windows onayı güvenilir şekilde sorulur; sessiz mod onayı
    bastırıp 1603'e düşürebiliyordu. Hata günlüğü Türkçe özetlenir."""
    import tempfile
    try:
        if os.path.getsize(msi_yolu) < 1024 * 1024:
            return False, "İndirilen dosya bozuk (çok küçük). İnterneti kontrol edip tekrar dene."
    except Exception:
        return False, "Kurulum dosyası bulunamadı. Tekrar dene."
    log = os.path.join(tempfile.gettempdir(), "dgm-tailscale-msi.log")
    try:
        pr = subprocess.run(["msiexec", "/i", msi_yolu, "/passive", "/norestart",
                             "/l*v", log],
                            capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return False, "Kurulum zaman aşımına uğradı. Bilgisayarı yeniden başlatıp tekrar dene."
    except FileNotFoundError:
        return False, "msiexec bulunamadı (Windows sorunu)."
    kod = pr.returncode
    if kod == 0:
        return True, "Kuruldu."
    if kod == 1603:
        return False, "Kurulum yarıda kaldı (1603). " + _log_ozeti(log)
    if kod == 1625:
        return False, "Sistem kurulumu engelliyor (1625): yönetici politikası."
    if kod == 1618:
        return False, "Başka bir kurulum sürüyor (1618): bitince tekrar dene."
    if kod == 1601:
        return False, "Windows kurulum servisi çalışmıyor (1601): bilgisayarı yeniden başlatıp dene."
    if kod == 3010:
        return True, "Kuruldu (yeniden başlatma gerekiyor)."
    cikti = ((pr.stdout or "") + (pr.stderr or "")).strip().replace("\n", " ")
    detay = _log_ozeti(log)
    return False, "Kurulum hatası (kod %s). %s" % (kod, detay or (cikti[:200] if cikti else "Detay yok."))


def _log_ozeti(log_yolu):
    """MSI günlüğünden hataya en yakın satırları bulur (en fazla ~200 karakter)."""
    try:
        with open(log_yolu, "r", encoding="utf-8", errors="replace") as f:
            satirlar = f.read().splitlines()
    except Exception:
        try:
            with open(log_yolu, "r", encoding="utf-16", errors="replace") as f:
                satirlar = f.read().splitlines()
        except Exception:
            return ""
    for s in reversed(satirlar[-400:]):
        t = s.strip()
        if not t:
            continue
        k = t.lower()
        if "return value 3" in k or " error " in k or k.startswith("error"):
            return "Günlük: " + t[-180:]
    for s in reversed(satirlar[-50:]):
        t = s.strip()
        if t:
            return "Günlük sonu: " + t[-180:]
    return ""


def baglan(preauth_key, host_adi=""):
    exe = tailscale_exe()
    if not exe:
        return False, "Tailscale kurulu değil."
    key = (preauth_key or "").strip()
    if not key:
        return False, "Bağlantı anahtarı girilmedi. Genel yöneticiden al."
    cmd = [exe, "up", "--authkey=" + key]
    if host_adi:
        cmd.append("--hostname=" + re.sub(r"[^A-Za-z0-9-]", "-", host_adi)[:30])
    try:
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=90, creationflags=CREATE_NO_WINDOW)
        out = ((pr.stdout or "") + (pr.stderr or ""))[:600]
        return (pr.returncode == 0), (out or "Bağlandı.")
    except Exception as e:
        return False, str(e)[:400]


def durum_json():
    exe = tailscale_exe()
    if not exe:
        return {}
    try:
        pr = subprocess.run([exe, "status", "--json"], capture_output=True, text=True, timeout=15, creationflags=CREATE_NO_WINDOW)
        return json.loads(pr.stdout or "{}")
    except Exception:
        return {}


def vpn_ip_bul():
    exe = tailscale_exe()
    if exe:
        try:
            pr = subprocess.run([exe, "ip", "-4"], capture_output=True, text=True, timeout=10, creationflags=CREATE_NO_WINDOW)
            for satir in (pr.stdout or "").splitlines():
                s = satir.strip()
                if re.match(r"^100\.\d+\.\d+\.\d+$", s):
                    return s
        except Exception:
            pass
    d = durum_json()
    try:
        for ip in (d.get("TailscaleIPs") or []):
            if isinstance(ip, str) and ip.startswith("100."):
                return ip
    except Exception:
        pass
    return ""


def bagli_mi():
    d = durum_json()
    ip = vpn_ip_bul()
    backend = (d.get("BackendState") or "")
    return bool(ip), ip, backend


def otomatik_baslat_ayarla():
    try:
        subprocess.run(["sc", "config", "Tailscale", "start=", "auto"], capture_output=True, timeout=15)
        subprocess.run(["sc", "start", "Tailscale"], capture_output=True, timeout=15)
        return True
    except Exception:
        return False
