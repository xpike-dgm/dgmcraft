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
    app, _pencere = calistir(kok, ayar)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
