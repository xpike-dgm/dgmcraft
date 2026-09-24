"""Sayfa kaydı: yeni özellik = bu listeye 1 satır. Başka yere dokunulmaz."""
from .pages import hub, komutlar, durum, konsol, gorevler, yetenekler, siralama, ayarlar

SAYFALAR = [
    ("hub", hub),
    ("komutlar", komutlar),
    ("durum", durum),
    ("konsol", konsol),
    ("gorevler", gorevler),
    ("yetenekler", yetenekler),
    ("siralama", siralama),
    ("ayarlar", ayarlar),
]
