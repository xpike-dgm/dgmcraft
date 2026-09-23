"""FAZ 1: Java bulma, port kontrol, RCON, sunucu süreç yönetimi, yedekleme."""
import os
import re
import shutil
import socket
import struct
import subprocess
import threading
import time
import queue
import zipfile
from datetime import datetime
from . import constants as C

CREATE_NO_WINDOW = 0x08000000


def portable_java_adaylari(sunucu_koku):
    aday = [
        os.path.join(sunucu_koku, "runtime", "bin", "java.exe"),
        os.path.join(sunucu_koku, "runtime", "bin", "java"),
    ]
    try:
        rt = os.path.join(sunucu_koku, "runtime")
        if os.path.isdir(rt):
            for ad in os.listdir(rt):
                aday.append(os.path.join(rt, ad, "bin", "java.exe"))
                aday.append(os.path.join(rt, ad, "bin", "java"))
    except Exception:
        pass
    try:
        from . import paths as _P
        w = _P.work_dir()
        if os.path.abspath(w) != os.path.abspath(sunucu_koku):
            aday.append(os.path.join(w, "runtime", "bin", "java.exe"))
            rt2 = os.path.join(w, "runtime")
            if os.path.isdir(rt2):
                for ad in os.listdir(rt2):
                    aday.append(os.path.join(rt2, ad, "bin", "java.exe"))
    except Exception:
        pass
    return aday


def java_bul(sunucu_koku):
    for p in portable_java_adaylari(sunucu_koku):
        if os.path.isfile(p):
            return p, "portable"
    sys_java = shutil.which("java")
    if sys_java:
        return sys_java, "sistem"
    return "", "yok"


def java_surumu(java_yolu):
    try:
        pr = subprocess.run([java_yolu, "-version"], capture_output=True, text=True, timeout=15)
        out = (pr.stderr or "") + (pr.stdout or "")
        m = re.search(r'version "(\d+)', out)
        if m:
            return int(m.group(1)), out.strip()[:300]
        return -1, out.strip()[:300]
    except Exception as e:
        return -1, str(e)[:300]


def port_dolu_mu(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1.0)
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


def server_properties_oku(sunucu_koku):
    yol = os.path.join(sunucu_koku, "server.properties")
    veri = {"rcon.password": "", "rcon.port": str(C.RCON_VARSAYILAN_PORT), "server-port": str(C.OYUN_PORT)}
    try:
        with open(yol, "r", encoding="utf-8", errors="replace") as f:
            for satir in f:
                satir = satir.strip()
                if not satir or satir.startswith("#") or "=" not in satir:
                    continue
                k, v = satir.split("=", 1)
                veri[k.strip()] = v.strip()
    except Exception:
        pass
    return veri


class RconIstemcisi:
    def __init__(self, host="127.0.0.1", port=25575, sifre=""):
        self.host = host
        self.port = int(port)
        self.sifre = sifre

    def _paket(self, req_id, tip, govde):
        data = govde.encode("utf-8") + b"\x00\x00"
        return struct.pack("<iii", len(data) + 6, req_id, tip) + data

    def komut(self, komut, timeout=8):
        import random
        rid = random.randint(1, 10 ** 6)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((self.host, self.port))
            s.sendall(self._paket(rid, 3, self.sifre))
            auth = s.recv(4096)
            if len(auth) < 12 or struct.unpack("<i", auth[8:12])[0] == -1:
                return False, "RCON şifresi kabul edilmedi."
            s.sendall(self._paket(rid, 2, komut))
            parcalar = []
            s.settimeout(4)
            try:
                while True:
                    chunk = s.recv(8192)
                    if not chunk:
                        break
                    if len(chunk) >= 12:
                        parcalar.append(chunk[12:].rstrip(b"\x00").decode("utf-8", errors="replace"))
                    if len(chunk) < 8192:
                        break
            except socket.timeout:
                pass
            return True, "".join(parcalar)
        except Exception as e:
            return False, str(e)[:500]
        finally:
            try:
                s.close()
            except Exception:
                pass


class SunucuYoneticisi:
    def __init__(self, sunucu_koku, log_kuyrugu):
        self.kok = sunucu_koku
        self.kuyruk = log_kuyrugu
        self.proc = None
        self.calisiyor = False

    def _yaz(self, metin):
        try:
            self.kuyruk.put_nowait(metin)
        except queue.Full:
            pass

    def baslat(self):
        if self.proc and self.proc.poll() is None:
            return False, "Sunucu zaten çalışıyor."
        if port_dolu_mu(C.OYUN_PORT):
            return False, "25565 portu dolu. Başka bir host açık olabilir. Ana ekrandaki katılma bilgisine bak."
        jar = os.path.join(self.kok, "purpur.jar")
        if not os.path.isfile(jar):
            return False, "purpur.jar bulunamadı. Eşitleme bitmeden başlatamazsın."
        java_yolu, kaynak = java_bul(self.kok)
        if not java_yolu:
            return False, "Java bulunamadı. runtime/ klasörü eksik ve sistemde java yok. Genel yöneticiden portable Java iste."
        major, _ham = java_surumu(java_yolu)
        if major != -1 and major != C.BEKLENEN_JAVA_MAJOR:
            self._yaz("[UYARI] Java sürümü %s, beklenen 25. Devam ediliyor.\n" % major)
        cmd = [java_yolu] + C.JVM_SABIT_BAYRAKLAR + C.HEAP_BAYRAKLARI + ["-jar", "purpur.jar", C.NOGUI_BAYRAGI]
        self._yaz("Çalıştırılıyor: " + " ".join(cmd) + "\n")
        try:
            self.proc = subprocess.Popen(
                cmd, cwd=self.kok, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, encoding="utf-8", errors="replace",
                bufsize=1, creationflags=CREATE_NO_WINDOW,
            )
        except Exception as e:
            return False, "Başlatılamadı: %s" % str(e)[:400]
        self.calisiyor = True
        t = threading.Thread(target=self._oku, daemon=True)
        t.start()
        return True, "Başlatıldı (%s java)." % kaynak

    def _oku(self):
        try:
            for satir in self.proc.stdout:
                self._yaz(satir)
        except Exception as e:
            self._yaz("[log okuma bitti: %s]\n" % str(e)[:200])
        self.calisiyor = False
        try:
            kod = self.proc.wait(timeout=5)
            self._yaz("[sunucu kapandı, kod=%s]\n" % kod)
        except Exception:
            pass

    def stdin_gonder(self, komut):
        try:
            if self.proc and self.proc.poll() is None and self.proc.stdin:
                self.proc.stdin.write(komut.strip() + "\n")
                self.proc.stdin.flush()
                return True
        except Exception:
            pass
        return False

    def komut_gonder(self, komut):
        if self.stdin_gonder(komut):
            return True, "Gönderildi (konsol)."
        props = server_properties_oku(self.kok)
        rc = RconIstemcisi(port=props.get("rcon.port", "25575"), sifre=props.get("rcon.password", ""))
        if not rc.sifre:
            return False, "Konsol yanıt vermiyor ve RCON şifresi okunamadı."
        ok, cevap = rc.komut(komut)
        return ok, ("RCON yanıtı: " + cevap) if ok else ("RCON hatası: " + cevap)

    def guvenli_kapat(self, durum_yaz):
        durum_yaz("Kaydediliyor (save-all flush)...")
        self.komut_gonder("save-all flush")
        for _ in range(C.KAPANMA_SAVE_BEKLEME_SN):
            time.sleep(1)
            if self.proc is None or self.proc.poll() is not None:
                return True
        durum_yaz("'stop' gönderiliyor...")
        self.komut_gonder("stop")
        for _ in range(C.KAPANMA_UST_SINIR_SN):
            time.sleep(1)
            if self.proc is None or self.proc.poll() is not None:
                return True
        durum_yaz("Sunucu 90 sn içinde kapanmadı. EliteMobs kapanışta nadiren takılır, veri kaybı olmaz çünkü save-all önce çalıştı. 'Zorla Kapat'ı kullanabilirsin.")
        return False

    def zorla_kapat(self):
        try:
            if self.proc and self.proc.poll() is None:
                self.proc.kill()
                return True
        except Exception:
            pass
        return False


def yedek_al(sunucu_koku, durum_yaz=None):
    klasor = os.path.join(sunucu_koku, "backups")
    os.makedirs(klasor, exist_ok=True)
    ad = "DgmCraft_%s.zip" % datetime.now().strftime("%Y%m%d_%H%M%S")
    hedef = os.path.join(klasor, ad)
    dahil = ["world", "plugins", "server.properties", "commands.yml"]
    with zipfile.ZipFile(hedef, "w", zipfile.ZIP_DEFLATED) as z:
        for oge in dahil:
            yol = os.path.join(sunucu_koku, oge)
            if os.path.isdir(yol):
                for kok, _, dosyalar in os.walk(yol):
                    if os.path.basename(kok) in ("cache",):
                        continue
                    for d in dosyalar:
                        # Sunucu açıkken kilitli olur, yedeğe gerek yok.
                        if d in ("session.lock",):
                            continue
                        tam = os.path.join(kok, d)
                        try:
                            z.write(tam, os.path.relpath(tam, sunucu_koku))
                        except OSError:
                            continue
            elif os.path.isfile(yol):
                try:
                    z.write(yol, oge)
                except OSError:
                    continue
    if durum_yaz:
        durum_yaz("Yedek alındı: " + ad)
    return hedef
