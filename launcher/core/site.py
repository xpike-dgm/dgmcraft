"""FAZ 5: Site yayın + /api/* + site-link.txt. Yalnızca stdlib."""
import json
import os
import re
import socket
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from . import constants as C

_onay_bekleyenler = {}


def tehlikeli_mi(komut):
    ilk = (komut or "").strip().split(" ")[0].lower().lstrip("/")
    return ilk in C.TEHLIKELI_KOMUTLAR


def site_link_yaz(sunucu_koku, vpn_ip, port, komut_gonderici=None):
    if not vpn_ip:
        return False
    link = "http://%s:%s" % (vpn_ip, port)
    try:
        with open(os.path.join(sunucu_koku, "site-link.txt"), "w", encoding="utf-8") as f:
            f.write(link)
    except Exception:
        pass
    # Oyundaki /site komutunu güncelle: vanilla Skript ile uyumlu statik dosya.
    # Dosya okuma kullanılmaz (skript-io yok), launcher gerçek linki gömer.
    try:
        sk_yol = os.path.join(sunucu_koku, "plugins", "Skript", "scripts", "dgm-site.sk")
        icerik = (
            "# DGM Craft site linki - bu dosya launcher tarafından otomatik yazılır.\n"
            "# Vanilla Skript ile uyumlu (dosya okuma yok, skript-io gerekmez).\n"
            "\n"
            "command /site:\n"
            "\tdescription: Sunucu sitesinin adresini verir.\n"
            "\ttrigger:\n"
            "\t\tsend \"&6Site: &f" + link + "\" to player\n"
        )
        with open(sk_yol, "w", encoding="utf-8") as f:
            f.write(icerik)
    except Exception:
        pass
    # Sunucu açıksa Skript dosyasını yeniden yükle (başarısızsa sunucu
    # yeniden başladığında dosya zaten güncel olacak).
    if komut_gonderici:
        try:
            komut_gonderici("sk reload dgm-site")
        except Exception:
            pass
    return True


def site_klasoru_bul(sunucu_koku):
    """Önce sunucu kökündeki site/, yoksa exe paketindeki site/.
    İkisi de yoksa None (eşitleme henüz gelmemiş)."""
    try:
        aday = os.path.join(sunucu_koku, "site")
        if os.path.isfile(os.path.join(aday, "index.html")):
            return aday
    except Exception:
        pass
    try:
        import sys
        if getattr(sys, "frozen", False):
            base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
            for aday in (os.path.join(base, "site"),
                         os.path.join(os.path.dirname(sys.executable), "site")):
                if os.path.isfile(os.path.join(aday, "index.html")):
                    return aday
    except Exception:
        pass
    return None


def bekleme_sayfasi():
    return """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8">""" \
        """<title>DgmCraft - Hazırlanıyor</title></head>""" \
        """<body style="background:#0B0F0E;color:#F2F5F3;font-family:sans-serif;""" \
        """display:flex;align-items:center;justify-content:center;height:100vh;margin:0">""" \
        """<div style="text-align:center"><h1>DGM CRAFT</h1>""" \
        """<p>Site dosyaları henüz eşleşmedi. Eşitleme bitince bu sayfa kendiliğinden açılır.</p>""" \
        """<p><a href="/" style="color:#F0A202">Tekrar dene</a></p></div></body></html>"""


def son_log_satirlari(sunucu_koku, n=200):
    yol = os.path.join(sunucu_koku, "logs", "latest.log")
    try:
        with open(yol, "r", encoding="utf-8", errors="replace") as f:
            satirlar = f.readlines()
        return satirlar[-n:]
    except Exception as e:
        return ["[log okunamadı: %s]\n" % str(e)[:200]]


def _port_acik_mi(port, host="127.0.0.1"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1.0)
        return s.connect_ex((host, int(port))) == 0
    except Exception:
        return False
    finally:
        try:
            s.close()
        except Exception:
            pass


def _server_properties(sunucu_koku):
    veri = {}
    try:
        with open(os.path.join(sunucu_koku, "server.properties"), "r", encoding="utf-8", errors="replace") as f:
            for satir in f:
                satir = satir.strip()
                if not satir or satir.startswith("#") or "=" not in satir:
                    continue
                k, v = satir.split("=", 1)
                veri[k.strip()] = v.strip()
    except Exception:
        pass
    return veri


def _komut_gecmisi_dosyasi(sunucu_koku):
    try:
        from . import paths as _P
        yol = os.path.join(_P.appdata(), "komut-gecmisi.json")
    except Exception:
        yol = os.path.join(sunucu_koku, "komut-gecmisi.json")
    return yol


def komut_gecmisine_ekle(sunucu_koku, komut, calistiran="site"):
    try:
        yol = _komut_gecmisi_dosyasi(sunucu_koku)
        try:
            with open(yol, "r", encoding="utf-8") as f:
                liste = json.load(f)
                if not isinstance(liste, list):
                    liste = []
        except Exception:
            liste = []
        liste.append({
            "komut": komut,
            "calistiran": calistiran,
            "zaman": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        liste = liste[-200:]
        tmp = yol + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(liste, f, ensure_ascii=False, indent=2)
        os.replace(tmp, yol)
    except Exception:
        pass


def komut_gecmisini_oku(sunucu_koku):
    try:
        with open(_komut_gecmisi_dosyasi(sunucu_koku), "r", encoding="utf-8") as f:
            veri = json.load(f)
            return veri if isinstance(veri, list) else []
    except Exception:
        return []


def _cevrimici_listesi_rcon(komut_gonderici):
    """RCON/komut yoluyla 'list' çalıştırıp isimleri ayıkla. Başarısızsa []."""
    try:
        ok, cevap = komut_gonderici("list")
        if not ok or not cevap:
            return []
        # Essentials list çıktısı genelde "Online players (3): a, b, c" içerir.
        m = re.search(r":\s*(.+)$", cevap.strip().replace("\n", " "))
        if not m:
            return []
        adaylar = [a.strip() for a in m.group(1).split(",")]
        return [a for a in adaylar if a and len(a) < 32 and " " not in a][:20]
    except Exception:
        return []


def _auraskills_seviyeleri(sunucu_koku, oyuncu_adi=None):
    """plugins/AuraSkills/userdata/*.yml dosyalarından seviye+XP oku.
    Oyuncu adı verilirse Essentials userdata ile UUID eşleştirmeye çalışır."""
    out = []
    try:
        import glob
        # UUID -> ad eşleştirme (Essentials userdata)
        uuid_ad = {}
        for yol in glob.glob(os.path.join(sunucu_koku, "plugins", "Essentials", "userdata", "*.yml")):
            try:
                with open(yol, "r", encoding="utf-8", errors="replace") as f:
                    icerik = f.read()
                m = re.search(r"last-account-name:\s*(.+)", icerik)
                if m:
                    uid = os.path.splitext(os.path.basename(yol))[0]
                    uuid_ad[uid.lower()] = m.group(1).strip()
            except Exception:
                continue
        hedef_uuid = None
        if oyuncu_adi:
            for uid, ad in uuid_ad.items():
                if ad.lower() == oyuncu_adi.lower():
                    hedef_uuid = uid
                    break
        dosyalar = glob.glob(os.path.join(sunucu_koku, "plugins", "AuraSkills", "userdata", "*.yml"))
        for yol in dosyalar:
            uid = os.path.splitext(os.path.basename(yol))[0].lower()
            if hedef_uuid and uid != hedef_uuid:
                continue
            try:
                with open(yol, "r", encoding="utf-8", errors="replace") as f:
                    icerik = f.read()
                # skills: altında "auraskills/mining:\n    level: 12\n    xp: 3450" blokları
                for m in re.finditer(r"auraskills/([a-z_]+):\s*\n\s*level:\s*(\d+)\s*\n\s*xp:\s*([\d.]+)", icerik):
                    out.append({
                        "id": m.group(1),
                        "seviye": int(m.group(2)),
                        "xp": float(m.group(3)),
                        "uuid": uid,
                        "ad": uuid_ad.get(uid, ""),
                    })
            except Exception:
                continue
    except Exception:
        pass
    return out


def _olaylari_parse_et(satirlar):
    olaylar = []
    for satir in satirlar[-500:]:
        s = satir.strip()
        tur = None
        if re.search(r"joined the game|oyuna (girdi|katıldı)", s, re.IGNORECASE):
            tur = "giris"
        elif re.search(r"left the game|lost connection|ayrıldı", s, re.IGNORECASE):
            tur = "cikis"
        elif re.search(r"(was slain|died|öldu|yanarak|boğuldu|lava)", s, re.IGNORECASE) and "joined" not in s.lower():
            # Sohbet satırlarını ölüm sanmamak için köşeli oyuncu mesajlarını ele
            if "<" not in s or "died" in s.lower() or "was slain" in s.lower():
                tur = "olum"
        elif re.search(r"ERROR|Exception|SEVERE|FAILED", s):
            tur = "uyari"
        if tur:
            # Zaman damgası: [12:34:56] bloğu
            zm = re.search(r"\[(\d{2}:\d{2}:\d{2})", s)
            olaylar.append({
                "zaman": zm.group(1) if zm else "",
                "tur": tur,
                "metin": s[-300:],
            })
    return olaylar[-100:]


MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
}


class SiteSunucusu:
    def __init__(self, sunucu_koku, komut_gonderici):
        self.kok = sunucu_koku
        self.komut_gonderici = komut_gonderici
        self.httpd = None
        self.thread = None
        self.adres = ""

    def baslat(self, vpn_ip, port):
        if not vpn_ip:
            return False, "VPN bağlı değil, site açılamaz."
        self.durdur()
        kok = self.kok
        gonderici = self.komut_gonderici

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _cors(self):
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")

            def _json(self, veri, kod=200):
                ham = json.dumps(veri, ensure_ascii=False).encode("utf-8")
                self.send_response(kod)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(ham)))
                self._cors()
                self.end_headers()
                self.wfile.write(ham)

            def do_OPTIONS(self):
                self.send_response(204)
                self._cors()
                self.end_headers()

            def do_GET(self):
                yol_sade = self.path.split("?")[0]
                if self.path.startswith("/api/log"):
                    n = 200
                    m = re.search(r"son=(\d+)", self.path)
                    if m:
                        n = max(20, min(500, int(m.group(1))))
                    satirlar = son_log_satirlari(kok, n)
                    props = _server_properties(kok)
                    oyun_port = int(props.get("server-port", "25565") or 25565)
                    self._json({"satirlar": satirlar, "sunucuAcik": _port_acik_mi(oyun_port)})
                    return
                if yol_sade == "/api/durum":
                    props = _server_properties(kok)
                    oyun_port = int(props.get("server-port", "25565") or 25565)
                    acik = _port_acik_mi(oyun_port)
                    cevrimici = _cevrimici_listesi_rcon(gonderici) if acik else []
                    self._json({
                        "tps": None,
                        "mspt": None,
                        "ramKullanimMB": None,
                        "ramMaxMB": 3072,
                        "cevrimici": cevrimici,
                        "maxOyuncu": int(props.get("max-players", "10") or 10),
                        "sunucuAcik": acik,
                        "hazirDegil": ["tps", "mspt", "ram"],
                    })
                    return
                if yol_sade == "/api/oyuncular":
                    props = _server_properties(kok)
                    oyun_port = int(props.get("server-port", "25565") or 25565)
                    acik = _port_acik_mi(oyun_port)
                    isimler = _cevrimici_listesi_rcon(gonderici) if acik else []
                    self._json({"oyuncular": [
                        {"ad": a, "cevrimici": True, "x": None, "y": None, "z": None,
                         "dunya": None, "para": None, "ping": None, "oyunSuresiDakika": None}
                        for a in isimler
                    ], "sunucuAcik": acik})
                    return
                if yol_sade in ("/api/liderlik", "/api/ekonomi", "/api/gorevler"):
                    self._json({"hazirDegil": True, "not": "Bu veri uygulama güncellemesi bekliyor (dosya okuma henüz bağlı değil).", "veriler": []})
                    return
                if yol_sade == "/api/yetenekler":
                    m = re.search(r"oyuncu=([^&]+)", self.path)
                    ad = None
                    if m:
                        try:
                            from urllib.parse import unquote
                            ad = unquote(m.group(1))
                        except Exception:
                            ad = m.group(1)
                    sev = _auraskills_seviyeleri(kok, ad)
                    self._json({"yetenekler": [
                        {"id": s["id"], "seviye": s["seviye"], "xp": s["xp"]} for s in sev
                    ]})
                    return
                if yol_sade == "/api/komutlar":
                    self._json({"komutlar": komut_gecmisini_oku(kok)})
                    return
                if yol_sade == "/api/olaylar":
                    satirlar = son_log_satirlari(kok, 500)
                    self._json({"olaylar": _olaylari_parse_et(satirlar)})
                    return
                if yol_sade == "/api/envanter":
                    self._json({"hazirDegil": True, "not": "Bu özellik uygulama güncellemesi bekliyor.", "esya": []})
                    return
                # Statik site dosyaları
                site_klasoru = site_klasoru_bul(kok)
                if not site_klasoru:
                    ham = bekleme_sayfasi().encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(ham)))
                    self.end_headers()
                    self.wfile.write(ham)
                    return
                istenen = self.path.split("?")[0].lstrip("/")
                if istenen == "":
                    istenen = "index.html"
                tam = os.path.abspath(os.path.join(site_klasoru, istenen))
                if not tam.startswith(os.path.abspath(site_klasoru)):
                    self.send_error(403)
                    return
                if not os.path.isfile(tam):
                    tam = os.path.join(site_klasoru, "index.html")
                    if not os.path.isfile(tam):
                        self._json({"hata": "sayfa bulunamadı"}, 404)
                        return
                try:
                    with open(tam, "rb") as f:
                        ham = f.read()
                    self.send_response(200)
                    ext = os.path.splitext(tam)[1].lower()
                    self.send_header("Content-Type", MIME.get(ext, "application/octet-stream"))
                    self.send_header("Content-Length", str(len(ham)))
                    self._cors()
                    self.end_headers()
                    self.wfile.write(ham)
                except Exception as e:
                    self._json({"hata": str(e)[:300]}, 500)

            def do_POST(self):
                if not self.path.startswith("/api/cmd"):
                    self._json({"hata": "bilinmeyen adres"}, 404)
                    return
                try:
                    n = int(self.headers.get("Content-Length", "0") or 0)
                    ham = self.rfile.read(n).decode("utf-8", errors="replace") if n else "{}"
                    veri = json.loads(ham or "{}")
                except Exception:
                    self._json({"hata": "bozuk istek"}, 400)
                    return
                komut = (veri.get("komut") or "").strip()
                onay = (veri.get("onayKodu") or "").strip()
                if not komut:
                    self._json({"hata": "komut boş"}, 400)
                    return
                if tehlikeli_mi(komut) and not onay:
                    kod = uuid.uuid4().hex[:8]
                    _onay_bekleyenler[kod] = komut
                    self._json({
                        "onayGerekli": True,
                        "onayKodu": kod,
                        "soru": "'%s' tehlikeli bir komut. Çalıştırmak için onayKodu ile tekrar gönder." % komut,
                    })
                    return
                if onay:
                    beklenen = _onay_bekleyenler.pop(onay, None)
                    if beklenen != komut:
                        self._json({"hata": "onay kodu geçersiz"}, 403)
                        return
                try:
                    ok, cevap = gonderici(komut)
                except Exception as e:
                    ok, cevap = False, str(e)[:500]
                komut_gecmisine_ekle(kok, komut, "site")
                self._json({"tamam": ok, "cevap": cevap})

        try:
            self.httpd = ThreadingHTTPServer((vpn_ip, int(port)), Handler)
            self.adres = "http://%s:%s" % (vpn_ip, port)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            try:
                site_link_yaz(self.kok, vpn_ip, port, gonderici)
            except Exception:
                pass
            return True, self.adres
        except Exception as e:
            return False, "Site açılamadı: %s" % str(e)[:400]

    def durdur(self):
        try:
            if self.httpd:
                self.httpd.shutdown()
                self.httpd.server_close()
        except Exception:
            pass
        self.httpd = None
