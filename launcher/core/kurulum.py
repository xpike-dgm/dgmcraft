"""Tek seferlik AppData kurulumu. Yalnızca exe (frozen) çalışmalarda.
Kaynak koddan çalışanlarda (geliştirici) hiçbir şey yapmaz. Yalnızca stdlib."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

UYGULAMA_ADI = "DgmCraft.exe"
KISAYOL_ADI = "DGM Craft.lnk"


def _appdata():
    return os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")


def hedef_dizin():
    return os.path.join(_appdata(), "DgmCraft", "App")


def exe_dizini():
    return os.path.dirname(sys.executable)


def marker_yolu():
    return os.path.join(_appdata(), "DgmCraft", "install.json")


def marker_oku():
    try:
        with open(marker_yolu(), "r", encoding="utf-8") as f:
            veri = json.load(f)
            return veri if isinstance(veri, dict) else {}
    except Exception:
        return {}


def marker_yaz(veri):
    yol = marker_yolu()
    try:
        os.makedirs(os.path.dirname(yol), exist_ok=True)
    except Exception:
        pass
    tmp = yol + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)
    os.replace(tmp, yol)


def kurulu_mu():
    try:
        if not bool(getattr(sys, "frozen", False)):
            return False
        if os.path.abspath(exe_dizini()) != os.path.abspath(hedef_dizin()):
            return False
        if not os.path.isfile(os.path.join(hedef_dizin(), UYGULAMA_ADI)):
            return False
        return marker_oku().get("durum") == "kurulu"
    except Exception:
        return False


def gerekli():
    """Kurulum ekranı gösterilsin mi?"""
    try:
        if not bool(getattr(sys, "frozen", False)):
            return False
        if os.path.abspath(exe_dizini()) == os.path.abspath(hedef_dizin()):
            return False
        m = marker_oku()
        if m.get("durum") == "tasinabilir":
            return False
        return True
    except Exception:
        return False


def _atlanacak_mi(kok, ad):
    if ad == "guncelle-beni.bat":
        return True
    if ad.startswith("DgmCraft-v"):
        return True
    return False


def boyut_hesapla(kaynak):
    toplam = 0
    for kok, _, dosyalar in os.walk(kaynak):
        for ad in dosyalar:
            if _atlanacak_mi(kok, ad):
                continue
            try:
                toplam += os.path.getsize(os.path.join(kok, ad))
            except Exception:
                continue
    return toplam


def kopyala(kaynak, hedef, ilerleme=None):
    """Gerçek bayt ilerlemeli kopya. Dönen: kopyalanan dosya sayısı."""
    say = 0
    yapilan = 0
    toplam = boyut_hesapla(kaynak) or 1
    for kok, _, dosyalar in os.walk(kaynak):
        for ad in dosyalar:
            if _atlanacak_mi(kok, ad):
                continue
            s = os.path.join(kok, ad)
            rel = os.path.relpath(s, kaynak)
            h = os.path.join(hedef, rel)
            try:
                os.makedirs(os.path.dirname(h), exist_ok=True)
                shutil.copy2(s, h)
                say += 1
                try:
                    yapilan += os.path.getsize(s)
                except Exception:
                    pass
                if ilerleme:
                    try:
                        ilerleme(min(1.0, yapilan / toplam))
                    except Exception:
                        pass
            except Exception:
                continue
    if ilerleme:
        try:
            ilerleme(1.0)
        except Exception:
            pass
    return say


def kisayol_olustur(hedef_exe):
    """Masaüstü + Başlat menüsü kısayolu. Dönen: oluşturulan sayısı."""
    ok = 0
    for klasor in (os.path.join(os.path.expanduser("~"), "Desktop"),
                   os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")):
        lnk = os.path.join(klasor, KISAYOL_ADI)
        try:
            if not os.path.isdir(klasor):
                continue
            komut = (
                "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%s');"
                "$s.TargetPath='%s';$s.WorkingDirectory='%s';$s.Save()"
                % (lnk.replace("'", "''"), hedef_exe.replace("'", "''"),
                   os.path.dirname(hedef_exe).replace("'", "''"))
            )
            pr = subprocess.run(["powershell", "-NoProfile", "-Command", komut],
                                capture_output=True, timeout=60)
            if pr.returncode == 0 and os.path.isfile(lnk):
                ok += 1
        except Exception:
            continue
    return ok


def kurulu_exe_baslat():
    hedef = os.path.join(hedef_dizin(), UYGULAMA_ADI)
    subprocess.Popen([hedef], close_fds=False)


def kaldir_hazirla():
    """Kaldırma scriptini yazar. (bat, pid, dizin) döndürür. Kurulu değilse hata."""
    if not kurulu_mu():
        raise ValueError("Uygulama kurulu modda değil, kaldırılacak bir şey yok.")
    dizin = hedef_dizin()
    bat = os.path.join(dizin, "kaldir-beni.bat")
    satirlar = [
        "@echo off",
        "cd /d \"%TEMP%\"",
        "set PID=%~1",
        'set DIZIN=%~2',
        ":bekle",
        'tasklist /fi "PID eq %PID%" 2>nul | find "%PID%" >nul',
        "if %errorlevel%==0 (timeout /t 1 /nobreak >nul & goto bekle)",
        "timeout /t 2 /nobreak >nul",
        "del \"%USERPROFILE%\\Desktop\\" + KISAYOL_ADI + "\" 2>nul",
        "del \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\" + KISAYOL_ADI + "\" 2>nul",
        'rmdir /s /q "%DIZIN%" 2>nul',
        'del "%~f0"',
    ]
    with open(bat, "w", encoding="utf-8") as f:
        f.write("\r\n".join(satirlar) + "\r\n")
    return bat, os.getpid(), dizin


def bosta_alan_var(kaynak, hedef_suruculu=None):
    try:
        gerek = boyut_hesapla(kaynak) * 2 + 50 * 1024 * 1024
        surucu = os.path.splitdrive(os.path.abspath(hedef_dizin()))[0] or "C:"
        return shutil.disk_usage(surucu).free > gerek
    except Exception:
        return True
