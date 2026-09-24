"""Asset üretim hattı (derleme makinesinde bir kez çalışır).
DgmCraft-Assets ana kaynaklarından launcher ölçülerinde optimize kopyalar üretir.
Çıktı: launcher/assets/ (repoya girer). Pillow gerekir (yalnızca bu script için).
Kullanım: python scripts/uret-launcher-asset.py
"""
import os
import shutil
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow gerekli: pip install pillow")
    sys.exit(1)

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KAYNAK = r"C:\Users\Xpike\Desktop\DgmCraft-Assets"
HEDEF = os.path.join(KOK, "launcher", "assets")

# (kaynak_rel, hedef_rel, (maks_genislik, maks_yukseklik) ya da (w, h) tam boy)
ISLER = [
    ("01-Brand/DgmCraft-logo-horizontal.png", "brand/logo-horizontal-h40.png", (149, 40)),
    ("01-Brand/DgmCraft-logo-horizontal.png", "brand/logo-horizontal-w360.png", (360, 128)),
    ("01-Brand/DgmCraft-app-icon.png", "brand/app-icon-256.png", (256, 256)),
    ("01-Brand/DgmCraft-app-icon.png", "brand/app-icon-128.png", (128, 128)),
    ("01-Brand/DgmCraft-mark-orange-black-white.png", "brand/mark-480.png", (480, 480)),
    ("04-Launcher/splash/DgmCraft-launcher-splash-background.png", "splash/splash-bg-800.png", (800, 450)),
    ("06-Setup-Wizard/steps/DgmCraft-wizard-welcome.png", "wizard/step-welcome.png", (460, 168)),
    ("06-Setup-Wizard/steps/DgmCraft-wizard-name.png", "wizard/step-name.png", (460, 168)),
    ("06-Setup-Wizard/steps/DgmCraft-wizard-vpn-key.png", "wizard/step-key.png", (460, 168)),
    ("06-Setup-Wizard/steps/DgmCraft-wizard-file-sync.png", "wizard/step-sync.png", (460, 168)),
    ("06-Setup-Wizard/steps/DgmCraft-wizard-private-network.png", "wizard/step-vpn.png", (460, 168)),
    ("06-Setup-Wizard/steps/DgmCraft-wizard-friends.png", "wizard/step-friends.png", (460, 168)),
    ("06-Setup-Wizard/states/DgmCraft-wizard-ready.png", "wizard/step-ready.png", (380, 200)),
    ("04-Launcher/illustrations/DgmCraft-server-running.png", "illustrations/server-running-96.png", (96, 96)),
    ("04-Launcher/illustrations/DgmCraft-server-stopped.png", "illustrations/server-stopped-96.png", (96, 96)),
    ("04-Launcher/illustrations/DgmCraft-server-running.png", "illustrations/server-running-40.png", (40, 40)),
    ("04-Launcher/illustrations/DgmCraft-server-stopped.png", "illustrations/server-stopped-40.png", (40, 40)),
    ("04-Launcher/illustrations/DgmCraft-update-illustration.png", "illustrations/update-460.png", (460, 200)),
    ("04-Launcher/illustrations/DgmCraft-vpn-illustration.png", "illustrations/vpn-300.png", (300, 200)),
]


def main():
    if not os.path.isdir(KAYNAK):
        print("Kaynak yok: " + KAYNAK)
        return 1
    say = 0
    bayt = 0
    for k_rel, h_rel, kutu in ISLER:
        k = os.path.join(KAYNAK, k_rel.replace("/", os.sep))
        h = os.path.join(HEDEF, h_rel.replace("/", os.sep))
        if not os.path.isfile(k):
            print("ATLANDI (yok): " + k_rel)
            continue
        os.makedirs(os.path.dirname(h), exist_ok=True)
        im = Image.open(k).convert("RGBA")
        im.thumbnail(kutu, Image.LANCZOS)
        im.save(h, "PNG", optimize=True)
        say += 1
        bayt += os.path.getsize(h)
    # ICO olduğu gibi kopyalanır (Windows çoklu boyut seçer).
    ico_k = os.path.join(KAYNAK, "01-Brand", "DgmCraft-app-icon.ico")
    ico_h = os.path.join(HEDEF, "brand", "DgmCraft-app-icon.ico")
    if os.path.isfile(ico_k):
        os.makedirs(os.path.dirname(ico_h), exist_ok=True)
        shutil.copy2(ico_k, ico_h)
        say += 1
        bayt += os.path.getsize(ico_h)
    else:
        print("ATLANDI (yok): 01-Brand/DgmCraft-app-icon.ico")
    print("uretilen=%d toplam=%.1f MB -> %s" % (say, bayt / 1024 / 1024, HEDEF))
    return 0


if __name__ == "__main__":
    sys.exit(main())
