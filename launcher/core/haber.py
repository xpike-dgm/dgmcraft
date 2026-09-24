"""CHANGELOG'dan en yeni haberleri okur (Hub haber akışı). Sıra: tarih, sonra sürüm."""
import os
import re

_DESKI = re.compile(r"\[([^\]]+)\]\s*-\s*(\d{4})-(\d{2})-(\d{2})")


def surum_anahtari(baslik):
    """'[0.22.4] - 2026-09-24' -> ((2026,9,24),(0,22,4)); etiketsiz -> en eski."""
    try:
        m = _DESKI.search(baslik or "")
        if not m:
            return ((0, 0, 0), (0, 0, 0))
        ver = [int(x) for x in re.findall(r"\d+", m.group(1))[:3]]
        while len(ver) < 3:
            ver.append(0)
        return ((int(m.group(2)), int(m.group(3)), int(m.group(4))), tuple(ver))
    except Exception:
        return ((0, 0, 0), (0, 0, 0))


def changelog_oku(kok, adet=3):
    """[(başlık, özet)] — en yeniden en eskiye, yalnızca sürümlü kayıtlar."""
    yol = os.path.join(kok, "CHANGELOG.md")
    haberler = []
    try:
        with open(yol, "r", encoding="utf-8", errors="replace") as f:
            baslik, maddeler = "", []
            for satir in f:
                s = satir.strip()
                if s.startswith("## "):
                    if baslik:
                        haberler.append((baslik, "; ".join(maddeler[:2])))
                    baslik = s[3:].strip()
                    maddeler = []
                elif s.startswith("- ") and baslik:
                    maddeler.append(s[2:].strip()[:120])
            if baslik:
                haberler.append((baslik, "; ".join(maddeler[:2])))
    except Exception:
        pass
    try:
        haberler.sort(key=lambda h: surum_anahtari(h[0]), reverse=True)
    except Exception:
        pass
    etiketli = [h for h in haberler if surum_anahtari(h[0]) != ((0, 0, 0), (0, 0, 0))]
    return etiketli[:max(1, int(adet))]
