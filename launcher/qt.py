"""PySide6 arayüzü (yeni kuşak). Tkinter v2 aynen çalışmaya devam eder.
Kullanım: python launcher/qt.py  |  DgmCraft-Qt.bat"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    from core import store
    from ui.qt.kabuk import calistir
    kok = store.sunucu_kokunu_bul()
    ayar = store.yukle()
    # "--guncelleme" ekranı gerçek güncelleme olmadan da gösterir (görüntüleme)
    goster = any("guncelleme" in a for a in sys.argv[1:])
    # "--gorev-onizleme" görev ağacını yapay ilerleme ile doldurur (görüntüleme)
    onizleme = any("gorev-onizleme" in a for a in sys.argv[1:])
    app, _pencere = calistir(kok, ayar, guncelleme_goster=goster,
                             gorev_onizleme=onizleme)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
