# -*- coding: utf-8 -*-
"""Görsel türevleri ve video posterleri üretir.  Çalıştırma: python3 _src/media.py

Kullanım akışı:
  1. Kaynak görseller  → images/<ad>.webp   (kaynaklar SİLİNMEZ)
  2. Kaynak videolar   → videos/<ad>.mp4
  3. Bu betiği çalıştır → images/w500|w900|w1600/<ad>.webp + videos/<ad>.jpg

⚠️ cwebp'nin varsayılanı (-m 6 -pass 10) görsel başına saniyelerce CPU yiyor ve
   dosyayı BÜYÜTEBİLİYOR. Burada Pillow kullanılıyor, kalite sabit.
   ([[reference_medialibrary_cwebp_optimizer]])
⚠️ Postersiz <video> mobilde ilk karede boş siyah kutu gösteriyor.
"""
import os, subprocess, glob
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG, VID = os.path.join(KOK, "images"), os.path.join(KOK, "videos")
GENISLIKLER = (500, 900, 1600)
ATLA = ("favicon-", "apple-touch-icon", "logo-512")

def gorseller():
    n = 0
    for kaynak in sorted(glob.glob(os.path.join(IMG, "*.webp"))
                         + glob.glob(os.path.join(IMG, "*.jpg"))
                         + glob.glob(os.path.join(IMG, "*.jpeg"))
                         + glob.glob(os.path.join(IMG, "*.png"))):
        ad = os.path.splitext(os.path.basename(kaynak))[0]
        if any(ad.startswith(x) for x in ATLA):
            continue
        with Image.open(kaynak) as im:
            im = im.convert("RGB")
            for g in GENISLIKLER:
                hedef_dizin = os.path.join(IMG, f"w{g}")
                os.makedirs(hedef_dizin, exist_ok=True)
                hedef = os.path.join(hedef_dizin, ad + ".webp")
                if im.width < g and g != GENISLIKLER[0]:
                    continue          # kaynaktan büyütme yok
                if os.path.exists(hedef) and os.path.getmtime(hedef) > os.path.getmtime(kaynak):
                    continue
                oran = min(g / im.width, 1.0)
                yeni = im.resize((max(1, round(im.width * oran)),
                                  max(1, round(im.height * oran))), Image.LANCZOS)
                yeni.save(hedef, "WEBP", quality=82, method=4)
                n += 1
    return n

def posterler():
    """Videonun 1. saniyesinden poster çıkarır (ffmpeg varsa)."""
    if subprocess.call(["which", "ffmpeg"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL) != 0:
        return -1
    n = 0
    for v in sorted(glob.glob(os.path.join(VID, "*.mp4"))):
        hedef = os.path.splitext(v)[0] + ".jpg"
        if os.path.exists(hedef) and os.path.getmtime(hedef) > os.path.getmtime(v):
            continue
        subprocess.call(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", v,
                         "-frames:v", "1", "-vf", "scale=900:-2", "-q:v", "4", hedef])
        if os.path.exists(hedef):
            n += 1
    return n

if __name__ == "__main__":
    g = gorseller()
    p = posterler()
    print(f"✓ {g} görsel türevi üretildi")
    print("✓ ffmpeg yok, video posteri atlandı" if p < 0 else f"✓ {p} video posteri üretildi")
    print("→ şimdi: python3 _src/build.py")
