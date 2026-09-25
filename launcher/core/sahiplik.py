"""Sahip parolası: güncellemeyi herkese gönderme işlemini korur.

Parolanın kendisi hiçbir yerde saklanmaz; yalnızca tuzlanmış (salted) SHA-256
parmak izi tutulur. Böylece dosyayı gören biri parolayı okuyamaz.
Dosya: launcher/owner-parola.txt (biçim: <tuz>:<sha256>)"""
import hashlib
import hmac
import os
import secrets

DOSYA_ADI = "owner-parola.txt"
VARSAYILAN_TUZ = "dgmcraft"


def _dosya_yolu():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), DOSYA_ADI)


def _oku():
    try:
        with open(_dosya_yolu(), "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def parma_izle(parola, tuz=VARSAYILAN_TUZ):
    return hashlib.sha256(("%s:%s" % (tuz, parola or "")).encode("utf-8")).hexdigest()


def parola_ayarla(parola, tuz=VARSAYILAN_TUZ):
    parola = (parola or "").strip()
    if len(parola) < 6:
        raise ValueError("Parola en az 6 karakter olmalı.")
    with open(_dosya_yolu(), "w", encoding="utf-8") as f:
        f.write("%s:%s" % (tuz, parma_izle(parola, tuz)))
    try:
        os.chmod(_dosya_yolu(), 0o600)
    except Exception:
        pass
    return True


def parola_var_mi():
    icerik = _oku()
    return ":" in icerik and len(icerik.split(":", 1)[1]) == 64


def parola_dogru(parola):
    icerik = _oku()
    if ":" not in icerik:
        return False
    tuz, iz = icerik.split(":", 1)
    return hmac.compare_digest(iz.strip(), parma_izle(parola, tuz.strip()))


def yeni_surum_olustur(mevcut=""):
    """Yayınlanacak sürüm damgası: mevcut damganın ardışığı veya bugünün saati."""
    import time
    mevcut = (mevcut or "").strip()
    bugun = time.strftime("%Y.%m.%d")
    if mevcut.startswith(bugun + "-") and mevcut.split("-")[-1].isdigit():
        return "%s-%d" % (bugun, int(mevcut.split("-")[-1]) + 1)
    return time.strftime("%Y.%m.%d-%H%M")


def herkese_gonder(mevcut_surum="", notlar=""):
    """Tüm makinelerin güncellemesi için sürüm kilidini yazar.
    (basarili_mi, mesaj) döner."""
    try:
        from core import version as _V
    except Exception as e:
        return False, "Sürüm servisi yok: %s" % e
    yeni = yeni_surum_olustur(mevcut_surum)
    try:
        _V.yayinla(yeni, notlar)
    except Exception as e:
        return False, "Gönderilemedi: %s" % e
    return True, ("Sürüm %s gönderildi. Arkadaşların uygulamayı açtığında "
                  "güncelleme kendiliğinden kurulacak." % yeni)


def parola_uret(uzunluk=12):
    """Kurulum için rastgele parola üretir (kullanıcıya gösterilir)."""
    alfabe = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alfabe) for _ in range(max(8, int(uzunluk))))
