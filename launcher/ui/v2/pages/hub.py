# v2 sayfa iskeleti: F0. İçerik F1-F8 fazlarında gelecek.
import tkinter as tk
from .. import tokens as T
from .. import widgets as W

BASLIK = "Hub"
IKON = "hub"
ACIKLAMA = "Sunucu durumu, başlatma, bellek, çevrimiçi oyuncular, haberler."

class HubSayfasi:
    def __init__(self, hizmetler):
        self.hizmetler = hizmetler
        self.cerceve = None

    def kur(self, ebeveyn):
        self.cerceve = tk.Frame(ebeveyn, bg=T.BG)
        W.baslik(self.cerceve, BASLIK).pack(anchor="w", pady=(0, 4))
        W.aciklama(self.cerceve, ACIKLAMA + " Bu sayfa sıradaki fazda inşa edilecek.").pack(anchor="w")
        return self.cerceve

    def goster(self):
        pass

    def gizle(self):
        pass
