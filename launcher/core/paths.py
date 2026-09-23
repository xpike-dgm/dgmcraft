"""Gizli çalışma klasörü. Arayüzde yol gösterilmez."""
import os
import sys


def appdata():
    b = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    p = os.path.join(b, "DgmCraft")
    os.makedirs(p, exist_ok=True)
    return p


def work_dir():
    p = os.path.join(appdata(), "sunucu")
    os.makedirs(p, exist_ok=True)
    return p


def bin_dir():
    p = os.path.join(appdata(), "bin")
    os.makedirs(p, exist_ok=True)
    return p


def embedded_dir():
    if getattr(sys, "frozen", False):
        try:
            return os.path.join(sys._MEIPASS, "embedded")
        except Exception:
            return os.path.join(os.path.dirname(sys.executable), "embedded")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "embedded")
