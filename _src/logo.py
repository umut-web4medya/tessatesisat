# -*- coding: utf-8 -*-
"""Gerçek marka logosundan tüm türevleri üretir.  Çalıştırma: python3 _src/logo.py

Kaynak: images/tessa-tikaniklik-acma-logo.png  (2172×724, BEYAZ zeminli, alfa YOK)

⚠️ Beyazı global olarak silmek YANLIŞ: damlanın içindeki musluk da beyaz, o
   şeffaf olmamalı. Bu yüzden arka plan KENARDAN taşkın dolguyla bulunuyor.
⚠️ Google arama sonucundaki site ikonu kuralları ([[reference_google_favicon_kurallari]]):
   - WebP KABUL EDİLMEZ → favicon ico/png üretiliyor
   - kare ve 48'in katı olmalı → 48/96/192
   - apple-touch-icon BEYAZ zeminli (iOS saydamı SİYAHA çeviriyor)
"""
import os
from collections import deque
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(KOK, "images")
KAYNAK = os.path.join(IMG, "tessa-tikaniklik-acma-logo.png")

# Logodan örneklenen gerçek marka renkleri
LACIVERT = (5, 59, 124)     # #053B7C — TESSA sözcük işareti + damla gövdesi
MAVI     = (7, 150, 223)    # #0796DF — TESİSAT satırı + damla dış halkası


def seffaf(yol=KAYNAK):
    """Beyaz zemini alfaya çevirir (kenardan taşkın dolgu) ve sıkı kırpar."""
    im = Image.open(yol).convert("RGB")
    W, H = im.size
    px = list(im.getdata())

    def beyaz(i):
        r, g, b = px[i]
        return r > 236 and g > 236 and b > 236

    arka = bytearray(W * H)
    dq = deque()
    for x in range(W):
        for y in (0, H - 1):
            i = y * W + x
            if beyaz(i) and not arka[i]:
                arka[i] = 1; dq.append(i)
    for y in range(H):
        for x in (0, W - 1):
            i = y * W + x
            if beyaz(i) and not arka[i]:
                arka[i] = 1; dq.append(i)
    while dq:
        i = dq.popleft()
        x, y = i % W, i // W
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < W and 0 <= ny < H:
                j = ny * W + nx
                if not arka[j] and beyaz(j):
                    arka[j] = 1; dq.append(j)

    alfa = bytearray(W * H)
    for i in range(W * H):
        if arka[i]:
            continue
        r, g, b = px[i]
        l = (r + g + b) / 3
        # yarı beyaz kenar pikseli kısmen saydam → tırtıklı kenar olmaz
        alfa[i] = 255 if l < 232 else max(0, min(255, int((255 - l) * 255 / 23)))

    out = im.convert("RGBA")
    out.putalpha(Image.frombytes("L", (W, H), bytes(alfa)))
    return out.crop(out.getbbox())


def damla_kirp(logo):
    """Soldaki damla işaretini sözcük işaretinden ayırır.
    Tamamen saydam sütunlardan oluşan İLK büyük boşluk ayırma noktası."""
    W, H = logo.size
    a = logo.getchannel("A")
    dolu = [max(a.crop((x, 0, x + 1, H)).getextrema()) > 12 for x in range(W)]
    bos, en_iyi = 0, None
    for x in range(W):
        if dolu[x]:
            if bos >= W * 0.02 and en_iyi is None and x > W * 0.05:
                en_iyi = x - bos
            bos = 0
        else:
            bos += 1
    kes = en_iyi or int(W * 0.24)
    return logo.crop((0, 0, kes, H)).crop(logo.crop((0, 0, kes, H)).getbbox())


def kare(im, boy, zemin=None, pay=0.06):
    """İşareti kare tuvale ortalar (favicon için)."""
    ic = int(boy * (1 - pay * 2))
    oran = min(ic / im.width, ic / im.height)
    kucuk = im.resize((max(1, round(im.width * oran)), max(1, round(im.height * oran))),
                      Image.LANCZOS)
    tuval = Image.new("RGBA", (boy, boy), zemin or (0, 0, 0, 0))
    tuval.paste(kucuk, ((boy - kucuk.width) // 2, (boy - kucuk.height) // 2), kucuk)
    return tuval


def genislige(im, g):
    oran = g / im.width
    return im.resize((g, max(1, round(im.height * oran))), Image.LANCZOS)


def main():
    if not os.path.exists(KAYNAK):
        print("✗ kaynak logo yok:", KAYNAK); return
    logo = seffaf()
    print(f"  saydam logo: {logo.size[0]}×{logo.size[1]}")

    # Yatay logo — başlıkta 46px, alt bilgide 52px görünüyor; 4× retina payı
    genislige(logo, 760).save(os.path.join(IMG, "logo-tessa.webp"),
                              "WEBP", quality=92, method=6)

    # Damla işareti — koyu zeminde de okunur (gövde lacivert, halka mavi, musluk beyaz)
    d = damla_kirp(logo)
    print(f"  damla işareti: {d.size[0]}×{d.size[1]}")
    genislige(d, 320).save(os.path.join(IMG, "logo-damla.webp"), "WEBP", quality=92, method=6)

    # ⚠️ Favicon damladan üretiliyor: yatay logo 16px'te okunmaz hâle geliyor.
    kare(d, 256).save(os.path.join(KOK, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    for n in (48, 96, 192):
        kare(d, n).save(os.path.join(IMG, f"favicon-{n}.png"))

    # ⚠️ apple-touch-icon BEYAZ zeminli — iOS saydam pikseli siyaha çeviriyor
    kare(d, 180, zemin=(255, 255, 255, 255)).convert("RGB").save(
        os.path.join(IMG, "apple-touch-icon.png"))

    # Organization/logo şeması (min 112×112) — kare, beyaz zemin
    kare(d, 512, zemin=(255, 255, 255, 255)).convert("RGB").save(
        os.path.join(IMG, "logo-512.png"))

    print("✓ logo-tessa.webp + logo-damla.webp + favicon.ico + 48/96/192 + apple-touch + logo-512")


if __name__ == "__main__":
    main()
