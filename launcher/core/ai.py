"""Ucuz AI API ile sınırlı yardım: soru girer, Türkçe cevap çıkar.
Bilerek YOK: komut çalıştırma, dosya yazma, ayar değiştirme.
AI tavsiye verir, uygulaması her zaman kullanıcıda kalır. Yalnızca stdlib."""
import json
import urllib.error
import urllib.request

API_ADRES = "https://api.openai.com/v1/chat/completions"
VARSAYILAN_MODEL = "gpt-4o-mini"

SISTEM_MESAJI = (
    "Sen DGM Craft adlı 3 kişilik Minecraft arkadaş sunucusunun (Purpur 26.2, "
    "Windows, Syncthing, Tailscale) teknik yardımcısısın. Türkçe cevap ver. "
    "Kısa ve somut ol: önce olası nedeni tek cümleyle söyle, sonra numaralı "
    "adımlarla çözümü anlat. Asla dosya silen, format atan, kayıt defteri "
    "silen ya da belirsiz PowerShell komutları önerme. Bilgin yetmezse neyin "
    "eksik olduğunu sor, uydurma."
)


def sor(api_key, soru, baglam="", model=None, timeout=60):
    """Tek soru-cevap çağrısı. Anahtar ve soru boşsa Türkçe hata verir."""
    anahtar = (api_key or "").strip()
    if not anahtar:
        raise ValueError("AI anahtarı girilmedi (Ayarlar > AI anahtarı).")
    soru = (soru or "").strip()
    if not soru:
        raise ValueError("Soru boş.")
    baglam = (baglam or "")[:6000]
    kullanici = ("SUNUCU DURUMU:\n" + baglam + "\n\nSORU:\n" + soru) if baglam else soru
    govde = {
        "model": model or VARSAYILAN_MODEL,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SISTEM_MESAJI},
            {"role": "user", "content": kullanici},
        ],
    }
    istek = urllib.request.Request(
        API_ADRES,
        data=json.dumps(govde).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + anahtar},
        method="POST",
    )
    try:
        with urllib.request.urlopen(istek, timeout=timeout) as yanit:
            veri = json.loads(yanit.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            detay = json.loads(e.read().decode("utf-8", errors="replace"))
        except Exception:
            detay = {}
        ileti = ""
        try:
            ileti = (detay.get("error", {}) or {}).get("message", "") or ""
        except Exception:
            pass
        if e.code == 401:
            raise RuntimeError("Anahtar kabul edilmedi (401). Anahtarı kontrol et.")
        if e.code == 429:
            raise RuntimeError("Kota/limit aşıldı (429). Kullanım limitlerini kontrol et.")
        raise RuntimeError("API hatası (%s): %s" % (e.code, (ileti or "bilinmiyor")[:300]))
    except Exception as e:
        raise RuntimeError("Bağlantı hatası: %s" % str(e)[:300])
    try:
        cevap = veri["choices"][0]["message"]["content"]
        return (cevap or "").strip()
    except Exception:
        raise RuntimeError("API beklenmedik cevap verdi.")
