# -*- coding: utf-8 -*-
"""Commit ÖNCESİ denetim.  Çalıştırma: python3 _src/denetim.py  (hatada 1 döner)"""
import os, re, sys, glob, collections

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

hata, uyari = [], []

sayfalar = [y for y in glob.glob(os.path.join(KOK, "**", "index.html"), recursive=True)
            if "_src" not in y] + [os.path.join(KOK, "404.html")]

def goreli(y):
    return os.path.relpath(y, KOK)

basliklar, aciklamalar = collections.defaultdict(list), collections.defaultdict(list)
tum_yollar = set()
for y in sayfalar:
    d = os.path.dirname(goreli(y))
    tum_yollar.add((d + "/") if d and d != "." else "")
tum_yollar.add("404.html")

for y in sayfalar:
    s = open(y, encoding="utf-8").read()
    g = goreli(y)
    duz = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    metin = re.sub(r"<[^>]+>", " ", duz)
    kucuk_metin = metin.replace("İ", "i").replace("I", "ı").lower()

    # ⛔ Üstünlük iddiası — Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği
    for k in D.YASAK_IDDIA:
        if k in kucuk_metin:
            hata.append(f"{g}: üstünlük iddiası → '{k}'")

    # ⏳ Teyit edilmemiş rakam/iddia
    for k in D.TEYITSIZ:
        if k.lower() in kucuk_metin:
            uyari.append(f"{g}: teyit edilmemiş ifade → '{k}'")

    # Türkçe küçük harf bozulması (i + U+0307)
    if "i̇" in s:
        hata.append(f"{g}: bozuk Türkçe küçük harf (i + birleşen nokta)")

    # title / description
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    if not t:
        hata.append(f"{g}: <title> yok")
    else:
        tb = t.group(1).strip()
        basliklar[tb].append(g)
        if len(tb) > 70:
            uyari.append(f"{g}: title {len(tb)} karakter (>70)")
    a = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
    if not a:
        hata.append(f"{g}: meta description yok")
    else:
        ab = a.group(1).strip()
        aciklamalar[ab].append(g)
        if not (80 <= len(ab) <= 170):
            uyari.append(f"{g}: description {len(ab)} karakter (80-170 dışı)")

    # canonical mutlak mı
    c = re.search(r'<link rel="canonical" href="(.*?)"', s)
    if not c or not c.group(1).startswith("https://"):
        hata.append(f"{g}: canonical mutlak değil")

    # ⚠️ Kök-göreli varlık yolu (404 hariç) — alt yolda 404 verir
    if g != "404.html":
        for m in re.findall(r'(?:href|src)="(/[^/][^"]*)"', s):
            hata.append(f"{g}: kök-göreli yol → {m}")

    # Web4Medya imzası: bağlantı YALNIZ marka adını sarmalı
    if "w4-bag" in s:
        if s.count('class="w4-ad"') != 1:
            hata.append(f"{g}: imzada w4-ad sayısı 1 değil")
        if re.search(r'<a[^>]*class="w4-bag"', s):
            hata.append(f"{g}: rozetin tamamı <a> yapılmış (link şeması riski)")
    else:
        hata.append(f"{g}: Web4Medya imzası yok")

    # harita facade: ilk yükte iframe olmamalı
    if "<iframe" in s:
        hata.append(f"{g}: sayfada gömülü <iframe> var (facade bozulmuş)")

# yinelenen title / description
for tb, yl in basliklar.items():
    if len(yl) > 1:
        hata.append(f"yinelenen title ({len(yl)} sayfa): {tb[:60]} → {yl[:3]}")
for ab, yl in aciklamalar.items():
    if len(yl) > 1:
        hata.append(f"yinelenen description ({len(yl)} sayfa): {ab[:60]} → {yl[:3]}")

print(f"denetlenen sayfa: {len(sayfalar)}")
for u in uyari[:25]:
    print("  ⚠️ " + u)
if len(uyari) > 25:
    print(f"  ⚠️ ... ve {len(uyari)-25} uyarı daha")
for h in hata[:40]:
    print("  ⛔ " + h)
if len(hata) > 40:
    print(f"  ⛔ ... ve {len(hata)-40} hata daha")
print(f"\nsonuç: {len(hata)} hata, {len(uyari)} uyarı")
sys.exit(1 if hata else 0)
