"""F7 — Görevler: BeautyQuests görev tanımları + oyuncu ilerlemesi.

Kaynaklar:
- plugins/BeautyQuests/quests/**.yml  → görev tanımları
- plugins/BeautyQuests/questers/*.yml → oyuncu ilerlemesi (uuid eşlemesi Essentials'ten)

Görev içeriği ayrı bir çalışma kolundan geliyor; tanım yoksa sayfa "yakında" der,
uydurma görev üretmez."""
import io
import os
import re

QUESTS_DIZIN = os.path.join("plugins", "BeautyQuests", "quests")
QUESTERS_DIZIN = os.path.join("plugins", "BeautyQuests", "questers")
ESSENTIALS_DIZIN = os.path.join("plugins", "Essentials", "userdata")

DURUM_YOK = "yok"
DURUM_KILITLI = "kilitli"
DURUM_AKTIF = "aktif"
DURUM_TAMAM = "tamam"


def _dosyalar(kok, dizin):
    kok_yol = os.path.join(kok, dizin)
    liste = []
    for taban, _alt, adlar in os.walk(kok_yol):
        for ad in adlar:
            if ad.endswith(".yml"):
                liste.append(os.path.join(taban, ad))
    return sorted(liste)


def _oku(yol):
    try:
        with io.open(yol, encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except Exception:
        return []


def _temizle(metin):
    """Renk kodlarını (&a, §a) ve YAML tırnaklarını temizler."""
    s = metin or ""
    s = re.sub(r"[&§][0-9a-fk-orA-FK-ORx]", "", s)
    return s.replace("'", "").replace('"', "").strip()


def _tamsayi(deger):
    """'0037-gece-nobeti' → 37 ; '37' → 37 ; olmayan → None"""
    sayi = re.match(r"^(\d+)", str(deger or "").strip())
    return int(sayi.group(1)) if sayi else None


def anahtar_temizle(satir):
    """'- id: moneyReward' → 'id' ; 'questID: 31' → 'questID'"""
    s = (satir or "").strip().lstrip("-").strip()
    return s.split(":", 1)[0].strip().strip("'\"").lower()


_ODUL_ADI = {"moneyreward": "para", "expreward": "XP", "itemreward": "eşya",
             "titlereward": "başlık", "textreward": "not",
             "tpreward": "ışınlama", "commandreward": "komut", "wait": "bekleme",
             "randomreward": "rastgele ödül", "checkpointreward": "kilit noktası"}


def gorevleri_oku(kok):
    """[{id, no, ad, aciklama, oncesi, objektif_sayisi, oduller}]

    Hem eski (kökte objectives/rewards) hem BeautyQuests 2.1.0
    (manager.branches -> stages) düzenini okur.
    """
    gorevler = []
    for yol in _dosyalar(kok, QUESTS_DIZIN):
        kimlik = os.path.splitext(os.path.basename(yol))[0]
        if kimlik.startswith("_"):
            continue
        numara = _tamsayi(kimlik)
        ad = aciklama = ""
        oncesi = []
        objektif = 0
        oduller = []
        hedefler = []
        hedef = None
        bolum = ""
        blok = ""
        odul_turu = ""
        aciklama_ekli = False
        for satir in _oku(yol):
            ham = satir
            s = satir.strip()
            girinti = len(ham) - len(ham.lstrip())
            if not s or s.startswith("#"):
                if aciklama_ekli and not s and aciklama:
                    aciklama_ekli = False
                continue
            if anahtar_temizle(s) in ("provider", "identifier", "uuid", "completed"):
                continue
            anahtar, _, deger = s.partition(":")
            anahtar = anahtar.strip().strip("'\"")
            deger = deger.strip()

            if girinti == 0:
                bolum = anahtar.lower()
                blok = ""
                odul_turu = ""
                if bolum == "name":
                    ad = _temizle(deger)
                elif bolum == "description":
                    aciklama = _temizle(deger)
                    aciklama_ekli = bool(deger)
                elif bolum == "firework":
                    oduller.append("ışık efekti")
                continue

            if bolum == "description" and aciklama_ekli:
                aciklama = (aciklama + " " + _temizle(s)).strip()
                continue

            # Her aşama bir 'stageType:' satırı taşır (stages ve endingStages).
            if anahtar.lower() == "stagetype" and deger:
                objektif += 1
                hedef = {"tip": deger.strip().upper(), "adet": 0, "ipucu": ""}
                hedefler.append(hedef)
                continue
            if hedef is not None:
                if anahtar.lower() == "customtext" and deger:
                    hedef["ipucu"] = _temizle(deger)
                elif anahtar.lower() == "amount" and not hedef["adet"]:
                    sayi = re.search(r"\d+", deger)
                    if sayi:
                        hedef["adet"] = int(sayi.group())
            # Blok anahtarı: sayısal indeksler ("'0':") ebeveyn bağlamını bozmaz.
            if s.endswith(":") and not s.startswith("-"):
                blok_adi = anahtar.lower()
                if not re.match(r"^['\"]?\d+['\"]?$", blok_adi):
                    if bolum == "objectives":
                        objektif += 1
                    blok = blok_adi
                continue
            if bolum == "requirements":
                if anahtar.lower() == "questid" and deger:
                    no = _tamsayi(deger)
                    if no and no not in oncesi:
                        oncesi.append(no)
                elif s.startswith("- id:"):
                    blok = deger.lower()
            elif bolum in ("endrewards", "rewards", "rewardslist", "startrewards"):
                if s.startswith("- id:"):
                    odul_turu = deger.lower()
                    if odul_turu not in ("moneyreward", "expreward"):
                        oduller.append(_ODUL_ADI.get(odul_turu, odul_turu))
                elif odul_turu == "moneyreward" and anahtar.lower() == "money":
                    oduller.append("%s₺" % deger)
                    odul_turu = ""
                elif odul_turu == "expreward" and anahtar.lower() in ("xp_amount", "xp"):
                    oduller.append("%s XP" % deger)
                    odul_turu = ""
                elif s.startswith("-") and ":" not in s:
                    # eski düzen: "- money 30"
                    parca = _temizle(s.lstrip("- ")).split(" ", 1)
                    if len(parca) == 2 and parca[0].lower() in ("money", "para", "eco"):
                        oduller.append("%s₺" % parca[1])
                    elif parca:
                        oduller.append(parca[0])
        if not ad and not aciklama:
            continue
        gorevler.append({
            "id": kimlik, "no": numara,
            "ad": ad or kimlik, "aciklama": aciklama,
            "oncesi": oncesi, "objektif_sayisi": objektif,
            "oduller": _tekrar(oduller)[:6], "hedefler": hedefler,
        })
    gorevler.sort(key=lambda g: (g["no"] is None, g["no"] or 0))
    return gorevler


def _tekrar(liste):
    gorulen = set()
    sonuc = []
    for x in liste:
        if x and x not in gorulen:
            gorulen.add(x)
            sonuc.append(x)
    return sonuc


def oyuncular(kok):
    liste = []
    dizin = os.path.join(kok, QUESTERS_DIZIN)
    try:
        dosyalar = [a for a in os.listdir(dizin) if a.endswith(".yml")
                    and not a.startswith("_")]
    except Exception:
        return liste
    for dosya in dosyalar:
        uuid = dosya[:-4]
        # BeautyQuests oyuncu dosyası '0.yml' gibi olabilir; gerçek kimlik
        # dosyanın içindeki 'identifier' alanındadır.
        for satir in _oku(os.path.join(dizin, dosya)):
            s = satir.strip()
            if s.startswith("identifier:"):
                deger = _temizle(s.split(":", 1)[1])
                if deger:
                    uuid = deger
                break
        ad = _ad_bul(kok, uuid)
        liste.append({"uuid": uuid, "ad": ad or uuid[:8]})
    liste.sort(key=lambda x: (x["ad"] or x["uuid"]).lower())
    return liste


def _ad_bul(kok, uuid):
    yol = os.path.join(kok, ESSENTIALS_DIZIN, uuid + ".yml")
    for satir in _oku(yol):
        s = satir.strip()
        if s.startswith("last-account-name:"):
            return s.split(":", 1)[1].strip().strip("'\"")
    return ""


def _quester_yolu(kok, uuid):
    """Oyuncu ilerleme dosyasını bulur. Dosya adı '0.yml' gibi olabilir;
    gerçek bağlantı 'identifier' alanıdır."""
    dizin = os.path.join(kok, QUESTERS_DIZIN)
    dogrudan = os.path.join(dizin, "%s.yml" % uuid)
    if os.path.isfile(dogrudan):
        return dogrudan
    try:
        dosyalar = os.listdir(dizin)
    except Exception:
        return ""
    for dosya in dosyalar:
        if not dosya.endswith(".yml"):
            continue
        yol = os.path.join(dizin, dosya)
        for satir in _oku(yol):
            s = satir.strip()
            if s.startswith("identifier:"):
                if _temizle(s.split(":", 1)[1]) == uuid:
                    return yol
                break
    return ""


def ilerleme_oku(kok, uuid):
    """{gorev_id: {'durum':..., 'hedef':n, 'ilerleme':[n,...]}}
    BeautyQuests ilerleme dosyası oyuncu oynadıkça dolar; şu an çoğu boş."""
    yol = _quester_yolu(kok, uuid)
    if not yol or not os.path.isfile(yol):
        return {}
    sonuc = {}
    gorev = None
    bolum = ""
    for satir in _oku(yol):
        ham = satir
        s = satir.strip()
        if not s:
            continue
        girinti = len(ham) - len(ham.lstrip())
        if ":" not in s:
            continue
        anahtar = s.split(":", 1)[0].strip().strip("'\"")
        deger = s.split(":", 1)[1].strip()
        if girinti == 0:
            bolum = anahtar.lower()
            gorev = None
            continue
        if bolum not in ("quests", "currentquest", "completedquests", "data"):
            continue
        if girindi_meta(anahtar):
            continue
        if girinti <= 2:
            gorev = anahtar
            sonuc.setdefault(gorev, {"durum": DURUM_AKTIF, "hedef": 0,
                                     "ilerleme": []})
            if _dogru_mu(deger):
                sonuc[gorev]["durum"] = DURUM_TAMAM
            continue
        if gorev is None:
            continue
        if anahtar.lower() in ("complete", "completed", "status", "state"):
            if _dogru_mu(deger):
                sonuc[gorev]["durum"] = DURUM_TAMAM
            continue
        if s.startswith("-") or anahtar.isdigit():
            sayi = re.search(r"\d+", s)
            if sayi:
                sonuc[gorev]["ilerleme"].append(int(sayi.group()))
    return sonuc


def girindi_meta(anahtar):
    return anahtar.lower() in ("provider", "identifier", "uuid", "name", "completed")


def _dogru_mu(deger):
    return str(deger).strip().strip("'\"").lower() in ("true", "yes", "1",
                                                      "complete", "completed",
                                                      "done")


def agac(kok, uuid=None):
    """Görevleri bağımlılık grafiğiyle birlikte döner (yönsüz: bağımlı → önceki)."""
    gorevler = gorevleri_oku(kok)
    ilerleme = ilerleme_oku(kok, uuid) if uuid else {}
    kimlikler = {g["id"] for g in gorevler}
    for g in gorevler:
        g["oncesi"] = [o for o in g["oncesi"] if o in kimlikler]
        kayit = ilerleme.get(g["id"]) or {}
        if kayit.get("durum") == DURUM_TAMAM:
            g["durum"] = DURUM_TAMAM
        elif g["oncesi"] and any(
                (ilerleme.get(o) or {}).get("durum") != DURUM_TAMAM
                for o in g["oncesi"]):
            g["durum"] = DURUM_KILITLI
        elif kayit:
            g["durum"] = DURUM_AKTIF
        else:
            # Ön koşulları tamamlanmış, kaydı olmayan görev oynanabilir.
            g["durum"] = DURUM_AKTIF
        g["ilerleme"] = kayit.get("ilerleme", [])
    return gorevler


def ilerleme_ozeti(dugumler):
    toplam = len(dugumler)
    tamam = sum(1 for g in dugumler if g["durum"] == DURUM_TAMAM)
    aktif = sum(1 for g in dugumler if g["durum"] == DURUM_AKTIF)
    kilitli = sum(1 for g in dugumler if g["durum"] == DURUM_KILITLI)
    oran = (tamam / float(toplam)) if toplam else 0.0
    return {"toplam": toplam, "tamam": tamam, "aktif": aktif, "kilitli": kilitli,
            "oran": oran}
