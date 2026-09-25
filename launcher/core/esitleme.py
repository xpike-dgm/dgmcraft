"""FAZ 2: Syncthing gömülü, sessiz, penceresiz. Yalnızca stdlib."""
import json
import os
import re
import subprocess
import time
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from . import constants as C

CREATE_NO_WINDOW = 0x08000000
API_ADRES = "http://127.0.0.1:8384"


def bin_dizini():
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    yol = os.path.join(base, "DgmCraft", "bin")
    os.makedirs(yol, exist_ok=True)
    return yol


def syncthing_exe():
    aday = os.path.join(bin_dizini(), "syncthing.exe")
    return aday if os.path.isfile(aday) else ""


def zip_indir(hedef_klasor, ilerleme=None):
    os.makedirs(hedef_klasor, exist_ok=True)
    zip_yolu = os.path.join(hedef_klasor, "syncthing.zip")
    if not os.path.isfile(zip_yolu):
        req = urllib.request.Request(C.SYNCTHING_INDIRME_ADRESI, headers={"User-Agent": "DgmCraft"})
        with urllib.request.urlopen(req, timeout=120) as r, open(zip_yolu, "wb") as f:
            toplam = int(r.headers.get("Content-Length", "0") or 0)
            okunan = 0
            while True:
                parca = r.read(512 * 1024)
                if not parca:
                    break
                f.write(parca)
                okunan += len(parca)
                if ilerleme and toplam:
                    try:
                        ilerleme(okunan / toplam)
                    except Exception:
                        pass
    with zipfile.ZipFile(zip_yolu, "r") as z:
        for ad in z.namelist():
            if ad.lower().endswith("syncthing.exe"):
                z.extract(ad, hedef_klasor)
                tam = os.path.join(hedef_klasor, ad)
                hedef = os.path.join(bin_dizini(), "syncthing.exe")
                try:
                    os.replace(tam, hedef)
                except Exception:
                    import shutil as sh
                    sh.copy(tam, hedef)
                return hedef
    raise FileNotFoundError("zip içinde syncthing.exe bulunamadı.")


def kodu_temizle(kod):
    return re.sub(r"[^A-Z0-9]", "", (kod or "").upper())


def kod_gecerli_mi(kod):
    t = kodu_temizle(kod)
    return len(t) >= 52 and re.fullmatch(r"[A-Z0-9]+", t) is not None


def stignore_yaz(sunucu_koku):
    """Eşitlenmesi gerekmeyen dosyaları Syncthing'e bildirir.
    Klasör ayarı uygulanmasa bile dosya mevcut olmalı; aksi halde `.sahip`
    gibi yerel dosyalar arkadaşlara kopyalanır."""
    try:
        yol = os.path.join(sunucu_koku, ".stignore")
        icerik = "\n".join(C.ESITLEME_DISLAMA) + "\n"
        if os.path.isfile(yol):
            with open(yol, "r", encoding="utf-8", errors="replace") as f:
                if f.read() == icerik:
                    return True
        with open(yol, "w", encoding="utf-8") as f:
            f.write(icerik)
        return True
    except Exception:
        return False


class SyncthingYonetici:
    def __init__(self, sunucu_koku):
        self.kok = sunucu_koku
        self.proc = None

    def api_anahtari(self):
        cfg = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Syncthing", "config.xml")
        try:
            agac = ET.parse(cfg)
            kok = agac.getroot()
            gui = kok.find("gui")
            if gui is not None:
                return gui.findtext("apikey") or ""
        except Exception:
            pass
        return os.environ.get("SYNCTHING_API_KEY", "")

    def _istek(self, yol, veri=None, method="GET", timeout=15):
        url = API_ADRES + yol
        baslik = {"X-API-Key": self.api_anahtari()}
        govde = None
        if veri is not None:
            govde = json.dumps(veri).encode("utf-8")
            baslik["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=govde, headers=baslik, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ham = r.read().decode("utf-8") or "{}"
            try:
                return json.loads(ham)
            except Exception:
                return {}

    def calisiyor_mu(self):
        try:
            self._istek("/rest/system/status", timeout=5)
            return True
        except Exception:
            return False

    def sessiz_baslat(self):
        exe = syncthing_exe()
        if not exe:
            return False
        if self.calisiyor_mu():
            return True
        try:
            self.proc = subprocess.Popen(
                [exe, "--no-browser", "--no-console", "--gui-address=127.0.0.1:8384"],
                cwd=self.kok, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=CREATE_NO_WINDOW,
            )
            for _ in range(30):
                time.sleep(1)
                if self.calisiyor_mu():
                    return True
        except Exception:
            pass
        return self.calisiyor_mu()

    def kendi_kimligi(self):
        try:
            return self._istek("/rest/system/status").get("myID", "")
        except Exception:
            return ""

    def klasor_durumu(self):
        try:
            return self._istek("/rest/db/status?folder=" + C.KLASOR_ID)
        except Exception:
            return {}

    def ilerleme_yuzdesi(self):
        d = self.klasor_durumu()
        try:
            need = int(d.get("needBytes", 0) or 0)
            total = int(d.get("globalBytes", 0) or 0)
            if total <= 0 or need <= 0:
                return 100
            return max(0, min(99, int(100 * (total - need) / total)))
        except Exception:
            return 0

    def son_esitleme_durumu(self):
        d = self.klasor_durumu()
        try:
            need = int(d.get("needBytes", 0) or 0)
            if need == 0:
                return "güncel"
            return "eşitleniyor"
        except Exception:
            return "bilinmiyor"

    def otomatik_yapilandir(self, kendi_kodu, arkadas_kodlari):
        tum = [kodu_temizle(kendi_kodu)] + [kodu_temizle(k) for k in arkadas_kodlari if kodu_temizle(k)]
        tum = [k for k in tum if k]
        cfg = self._istek("/rest/config")
        cihazlar = cfg.get("devices", [])
        bilinen = {c.get("deviceID") for c in cihazlar}
        for kod in tum:
            if kod and kod not in bilinen:
                cihazlar.append({"deviceID": kod, "name": kod[:7], "autoAcceptFolders": True})
        cfg["devices"] = cihazlar
        klasorler = cfg.get("folders", [])
        hedef = None
        for f in klasorler:
            if f.get("id") == C.KLASOR_ID:
                hedef = f
        cihaz_refs = [{"deviceID": k} for k in tum]
        if hedef is None:
            klasorler.append({
                "id": C.KLASOR_ID,
                "label": "DgmCraft Sunucu",
                "path": self.kok,
                "type": "sendreceive",
                "rescanIntervalS": 60,
                "devices": cihaz_refs,
            })
        else:
            hedef["path"] = self.kok
            hedef["devices"] = cihaz_refs
        cfg["folders"] = klasorler
        self._istek("/rest/config", veri=cfg, method="POST")
        stignore_yaz(self.kok)
        return True
