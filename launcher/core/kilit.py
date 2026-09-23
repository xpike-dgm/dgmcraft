"""FAZ 4: host.lock.json sözleşmesi. Eşitlenen klasörde durur."""
import json
import os
import threading
from datetime import datetime, timezone
from . import constants as C


def kilit_yolu(sunucu_koku):
    return os.path.join(sunucu_koku, "host.lock.json")


def simdi_iso():
    return datetime.now(timezone.utc).isoformat()


def kilit_oku(sunucu_koku):
    try:
        with open(kilit_yolu(sunucu_koku), "r", encoding="utf-8") as f:
            veri = json.load(f)
            return veri if isinstance(veri, dict) else None
    except Exception:
        return None


def kilit_yasi_sn(kilit):
    try:
        kalp = datetime.fromisoformat(kilit.get("kalpAtisi", ""))
        return (datetime.now(timezone.utc) - kalp).total_seconds()
    except Exception:
        return 10 ** 9


def kilit_dolu_mu(sunucu_koku):
    k = kilit_oku(sunucu_koku)
    if not k:
        return False, None
    if kilit_yasi_sn(k) > C.KILIT_OLUM_ESIGI_SN:
        return False, k
    return True, k


def kilit_al(sunucu_koku, host_adi, vpn_ip, port=25565):
    veri = {
        "hostAdi": host_adi,
        "vpnIp": vpn_ip,
        "port": port,
        "baslamaZamani": simdi_iso(),
        "kalpAtisi": simdi_iso(),
        "surum": 1,
    }
    tmp = kilit_yolu(sunucu_koku) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)
    os.replace(tmp, kilit_yolu(sunucu_koku))
    return veri


def kilit_birak(sunucu_koku):
    try:
        os.remove(kilit_yolu(sunucu_koku))
    except FileNotFoundError:
        pass
    except Exception:
        pass


class KalpAtisi:
    def __init__(self, sunucu_koku):
        self.kok = sunucu_koku
        self.dur = threading.Event()
        self.t = None

    def baslat(self):
        self.dur.clear()
        self.t = threading.Thread(target=self._dongu, daemon=True)
        self.t.start()

    def durdur(self):
        self.dur.set()

    def _dongu(self):
        import time
        while not self.dur.wait(C.KALP_ATISI_SN):
            try:
                k = kilit_oku(self.kok)
                if not k:
                    continue
                k["kalpAtisi"] = simdi_iso()
                tmp = kilit_yolu(self.kok) + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(k, f, ensure_ascii=False, indent=2)
                os.replace(tmp, kilit_yolu(self.kok))
            except Exception:
                continue
