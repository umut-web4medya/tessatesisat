# -*- coding: utf-8 -*-
"""Favicon ve marka görselleri üretir.  Çalıştırma: python3 _src/logo.py

⚠️ Google arama sonucundaki site ikonu kuralları ([[reference_google_favicon_kurallari]]):
   - WebP KABUL EDİLMEZ → ico/png üretiliyor
   - kare ve 48'in katı olmalı → 48/96/192
   - apple-touch-icon BEYAZ zeminli (iOS saydamı SİYAHA çeviriyor)
"""
import os
from PIL import Image, ImageDraw

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(KOK, "images")
os.makedirs(IMG, exist_ok=True)

ALTIN = (190, 154, 86)
KOYU  = (14, 29, 46)

def damla(boy, zemin=None):
    """TESSA TESİSAT işareti: altın damla + içinde koyu damla."""
    b = boy * 4                       # süperörnekleme
    im = Image.new("RGBA", (b, b), zemin or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, pay = b / 2, b * 0.10
    ust, alt = pay, b - pay
    gen = (alt - ust) * 0.80
    # dış damla: üstte sivri, altta yuvarlak
    d.ellipse([cx - gen / 2, alt - gen, cx + gen / 2, alt], fill=ALTIN)
    d.polygon([(cx, ust), (cx - gen / 2, alt - gen * 0.52), (cx + gen / 2, alt - gen * 0.52)],
              fill=ALTIN)
    # iç damla
    ig = gen * 0.52
    ia = alt - gen * 0.12
    iu = ust + (alt - ust) * 0.40
    d.ellipse([cx - ig / 2, ia - ig, cx + ig / 2, ia], fill=KOYU)
    d.polygon([(cx, iu), (cx - ig / 2, ia - ig * 0.52), (cx + ig / 2, ia - ig * 0.52)], fill=KOYU)
    return im.resize((boy, boy), Image.LANCZOS)

def main():
    # favicon.ico — çok boyutlu
    ico = damla(256)
    ico.save(os.path.join(KOK, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    for n in (48, 96, 192):
        damla(n).save(os.path.join(IMG, f"favicon-{n}.png"))
    # ⚠️ apple-touch-icon BEYAZ zeminli — iOS saydam pikseli siyaha çeviriyor
    at = Image.new("RGB", (180, 180), (255, 255, 255))
    at.paste(damla(180), (0, 0), damla(180))
    at.save(os.path.join(IMG, "apple-touch-icon.png"))
    # Organization/logo alanı için (min 112×112)
    lg = Image.new("RGB", (512, 512), (255, 255, 255))
    lg.paste(damla(512), (0, 0), damla(512))
    lg.save(os.path.join(IMG, "logo-512.png"))
    print("✓ favicon.ico + 48/96/192 png + apple-touch-icon + logo-512")

if __name__ == "__main__":
    main()
