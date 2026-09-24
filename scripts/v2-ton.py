#!/usr/bin/env python
# v2 görsel ton düzeltmesi: ray ikonlarını gri/amber çiftine çevirir,
# hero görselini kenar tüyü (alpha) ile arka plana eritir.
# Pillow gerekir; yalnızca geliştirme makinesinde çalıştırılır, çıktı PNG'ler repoya girer.
import os

from PIL import Image, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IKON_DIZIN = os.path.join(KOK, "launcher", "assets", "v2", "nav-icons")
HERO = os.path.join(KOK, "launcher", "assets", "v2", "hub-hero.png")
HERO_SOFT = os.path.join(KOK, "launcher", "assets", "v2", "hub-hero-soft.png")

GRI = (150, 160, 155)
AMBER = (240, 162, 2)


def ikonlari_tonla():
    say = 0
    for ad in sorted(os.listdir(IKON_DIZIN)):
        if not ad.endswith(".png") or ad.endswith("@2x.png"):
            continue
        yol = os.path.join(IKON_DIZIN, ad)
        im = Image.open(yol).convert("RGBA")
        for renk, son_ad in ((GRI, ad[:-4] + "-gri.png"), (AMBER, ad[:-4] + "-aktif.png")):
            yeni = Image.new("RGBA", im.size, (0, 0, 0, 0))
            alfa = im.getchannel("A")
            dolgu = Image.new("RGBA", im.size, renk + (255,))
            yeni.paste(dolgu, (0, 0), alfa)
            yeni.save(os.path.join(IKON_DIZIN, son_ad), "PNG", optimize=True)
        say += 1
    return say


def hero_yumusat():
    im = Image.open(HERO).convert("RGBA")
    w, h = im.size
    maske = Image.new("L", (w, h), 0)
    p = maske.load()
    for y in range(h):
        for x in range(w):
            sol = min(1.0, x / 240.0)
            sag = min(1.0, (w - x) / 90.0)
            ust = min(1.0, y / 70.0)
            alt = min(1.0, (h - y) / 70.0)
            deger = sol * sag * ust * alt
            p[x, y] = int(215 * deger)
    maske = maske.filter(ImageFilter.GaussianBlur(18))
    im.putalpha(maske)
    im.save(HERO_SOFT, "PNG", optimize=True)
    return im.size


def main():
    if not os.path.isdir(IKON_DIZIN) or not os.path.isfile(HERO):
        print("v2 assetleri yok")
        return 1
    print("ikon tonlandi: %d" % ikonlari_tonla())
    print("hero yumusatildi: %s" % (hero_yumusat(),))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
