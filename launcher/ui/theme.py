"""SaaS koyu tema: siteyle aynı dil (warm-dark + slate + amber, saf siyah yok)."""
import tkinter as tk
from tkinter import ttk

BG = "#0B0F0E"
PANEL = "#141B19"
KART = "#131917"
KART2 = "#0F1513"
BORDER = "#26332E"
BORDER_YUMUSAK = "#1C2622"
YAZI = "#F2F5F3"
SOLUK = "#9AA8A0"
SOLUK2 = "#6E7F76"
AMBER = "#F0A202"
AMBER_HI = "#FFC14D"
AMBER_KOYU_YAZI = "#1A1000"
YESIL = "#34D399"
YESIL_KOYU = "#12261C"
KIRMIZI = "#FB7185"
KIRMIZI_KOYU = "#2E1414"
MAVI = "#93C5FD"
MAVI_KOYU = "#15202E"

FONT_BASLIK = ("Segoe UI", 16, "bold")
FONT_ALT = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_KUCUK = ("Segoe UI", 9)
FONT_KONSOL = ("Consolas", 10)
FONT_ROZET = ("Segoe UI", 10, "bold")

RENK_HARITASI = {
    "yesil": (YESIL_KOYU, YESIL),
    "kirmizi": (KIRMIZI_KOYU, KIRMIZI),
    "amber": ("#2A2007", AMBER_HI),
    "mavi": (MAVI_KOYU, MAVI),
    "gri": (PANEL, SOLUK),
}


def uygula(pencere):
    """ttk clam teması + tüm stiller. Kök oluştuktan sonra bir kez çağrılır."""
    stil = ttk.Style(pencere)
    try:
        stil.theme_use("clam")
    except Exception:
        pass
    pencere.configure(bg=BG)
    stil.configure(".", background=BG, foreground=YAZI, font=FONT_NORMAL,
                   fieldbackground=KART2, bordercolor=BORDER)
    stil.configure("TFrame", background=BG)
    stil.configure("Panel.TFrame", background=PANEL)
    stil.configure("Kart.TFrame", background=KART)
    stil.configure("TLabel", background=BG, foreground=YAZI, font=FONT_NORMAL)
    stil.configure("Panel.TLabel", background=PANEL, foreground=YAZI)
    stil.configure("Soluk.TLabel", background=BG, foreground=SOLUK, font=FONT_KUCUK)
    stil.configure("PanelSoluk.TLabel", background=PANEL, foreground=SOLUK, font=FONT_KUCUK)
    stil.configure("Baslik.TLabel", background=BG, foreground=YAZI, font=FONT_BASLIK)
    stil.configure("PanelBaslik.TLabel", background=PANEL, foreground=YAZI, font=FONT_ALT)
    # Birincil düğme (amber)
    stil.configure("Primary.TButton", background=AMBER, foreground=AMBER_KOYU_YAZI,
                   font=("Segoe UI", 10, "bold"), padding=(14, 8), borderwidth=0)
    stil.map("Primary.TButton", background=[("active", AMBER_HI), ("disabled", "#4A3A10")],
             foreground=[("disabled", "#8A7A50")])
    # İkincil düğme
    stil.configure("Secondary.TButton", background="#223029", foreground="#E8EEEA",
                   font=FONT_NORMAL, padding=(12, 7), borderwidth=1, bordercolor=BORDER)
    stil.map("Secondary.TButton", background=[("active", "#2C3E35")],
             bordercolor=[("active", AMBER)])
    # Tehlikeli düğme
    stil.configure("Danger.TButton", background="#3A1D18", foreground=KIRMIZI,
                   font=FONT_NORMAL, padding=(12, 7), borderwidth=1, bordercolor="#5A2B1A")
    stil.map("Danger.TButton", background=[("active", "#4A241D")])
    # Sekmeler
    stil.configure("TNotebook", background=BG, borderwidth=0)
    stil.configure("TNotebook.Tab", background=PANEL, foreground=SOLUK,
                   font=FONT_NORMAL, padding=(14, 8))
    stil.map("TNotebook.Tab", background=[("selected", KART)], foreground=[("selected", YAZI)])
    # İlerleme çubuğu
    stil.configure("Amber.Horizontal.TProgressbar", background=AMBER, troughcolor=KART2,
                   borderwidth=0, thickness=10)
    return stil


def ayirici(parent, bg=BG):
    c = tk.Frame(parent, bg=BORDER_YUMUSAK, height=1)
    c.pack(fill="x")
    return c


def rozet(parent, bg_parent, ilk_metin=""):
    """Durum hapı. (label, renk_degistirici) döndürür."""
    arka, yazi = RENK_HARITASI["gri"]
    lbl = tk.Label(parent, text=ilk_metin, font=FONT_ROZET, bg=arka, fg=yazi,
                   padx=12, pady=5)
    lbl.pack(side="left")
    def boya(renk):
        arka2, yazi2 = RENK_HARITASI.get(renk, RENK_HARITASI["gri"])
        try:
            lbl.configure(bg=arka2, fg=yazi2)
        except Exception:
            pass
    return lbl, boya


def giris(parent, textvariable=None, width=None):
    e = tk.Entry(parent, textvariable=textvariable, bg=KART2, fg=YAZI,
                 insertbackground=AMBER, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=AMBER, font=FONT_NORMAL)
    if width:
        e.configure(width=width)
    return e


def konsol(parent, height=22):
    from tkinter import scrolledtext
    alan = scrolledtext.ScrolledText(parent, height=height, wrap="word",
                                     bg=KART2, fg="#C4CFC8", insertbackground=AMBER,
                                     relief="flat", highlightthickness=1,
                                     highlightbackground=BORDER_YUMUSAK,
                                     font=FONT_KONSOL, padx=8, pady=8)
    return alan
