# -*- coding: utf-8 -*-
"""
tessatesisat.online üreticisi.

⛔ Üretilen HTML'i ELLE DÜZENLEME — bu betik her çalıştığında üzerine yazar.
   Metin/veri değişikliği `data.py`'ye yapılır.

Çalıştırma:  python3 _src/build.py
Denetim:     python3 _src/denetim.py   (commit ÖNCESİ çalıştır, hatada 1 döner)
"""
import os, sys, html, hashlib, collections, json, re

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

S = D.SITE
ALAN = S["alan"]

# ── Göreli yol ──────────────────────────────────────────────────────────────
# ⚠️ Kök-göreli (/assets/...) yollar GitHub Pages ALT YOLUNDA 404 verir ve site
#    çıplak metne döner (umut-web4medya.github.io/tessatesisat/ önizlemesi).
#    Her sayfa yazılmadan önce ONEK derinliğe göre kuruluyor.
#    ⛔ 404.html istisna: GitHub onu her derinlikteki uydurma URL için servis
#       ettiği için orada kök yol ("/") kalır.
ONEK = ""

def ic(gorece=""):
    """İç bağlantı. Boş girdi = bulunulan sayfa (href="" geçersizdir)."""
    if not gorece:
        return ONEK if ONEK else "./"
    return ONEK + gorece.lstrip("/")

# ── Görsel ──────────────────────────────────────────────────────────────────
# ⚠️ Görsel YOKSA boş döner — placeholder kutusu basmaz, sayfa görselsiz de akar.
#    Türevler media.py ile images/w500|w900|w1600 altına üretilir.
GENISLIKLER = (500, 900, 1600)

def _turev_yolu(taban, g):
    return os.path.join(KOK, "images", f"w{g}", taban + ".webp")

def gorsel_var(taban):
    return (any(os.path.exists(_turev_yolu(taban, g)) for g in GENISLIKLER)
            or os.path.exists(os.path.join(KOK, "images", taban + ".webp")))

def olcu(taban):
    """Gerçek dosyadan en/boy okur; sabit oran yazmak yerleşim kayması yapıyordu."""
    for g in list(GENISLIKLER) + [None]:
        y = _turev_yolu(taban, g) if g else os.path.join(KOK, "images", taban + ".webp")
        if os.path.exists(y):
            try:
                from PIL import Image
                with Image.open(y) as im:
                    return im.size
            except Exception:
                return None
    return None

def gorsel(taban, alt, sinif="", boy="(min-width:1000px) 640px, 100vw", oncelik=False):
    if not gorsel_var(taban):
        return ""
    kaynak = []
    for g in GENISLIKLER:
        if os.path.exists(_turev_yolu(taban, g)):
            kaynak.append((f"images/w{g}/{taban}.webp", g))
    if kaynak:
        src = ic(kaynak[-1][0])
        srcset = ", ".join(f"{ic(y)} {g}w" for y, g in kaynak)
        ss = f' srcset="{srcset}" sizes="{boy}"'
    else:
        src, ss = ic(f"images/{taban}.webp"), ""
    o = olcu(taban)
    boyut = f' width="{o[0]}" height="{o[1]}"' if o else ""
    yukle = (' loading="eager" fetchpriority="high"' if oncelik
             else ' loading="lazy" decoding="async"')
    return (f'<picture class="{sinif}"><img src="{src}"{ss} alt="{e(alt)}"'
            f'{boyut}{yukle}></picture>')

# ── Varlık sürümleme ────────────────────────────────────────────────────────
# GitHub Pages CSS/JS'i max-age=600 ile servis ediyor; adres sabit kalırsa
# tarayıcı yeni HTML'i eski CSS'le birleştiriyor. ⛔ Kaldırma.
_surum_onbellek = {}
def surum(yol):
    if yol not in _surum_onbellek:
        t = os.path.join(KOK, yol.lstrip("/"))
        try:
            h = hashlib.md5(open(t, "rb").read()).hexdigest()[:8]
        except FileNotFoundError:
            h = "0"
        _surum_onbellek[yol] = f"{yol}?v={h}"
    return _surum_onbellek[yol]

def e(t):
    return html.escape(str(t), quote=True)

def kirp(metin, en_cok=165):
    """meta description'ı denetimin kabul ettiği aralığa çeker."""
    m = " ".join(str(metin).split())
    if len(m) > en_cok:
        kes = m[:en_cok]
        if " " in kes:
            kes = kes[:kes.rfind(" ")]
        m = kes.rstrip(" ,;:.") + "."
    return m

def kucuk(s):
    """⚠️ Türkçe küçük harf. Python'un .lower()'ı 'İ' harfini 'i̇' (i + birleşen
    nokta) yapıyor; anchor metinlerinde bozuk çıkıyor. ⛔ .lower()/.capitalize()
    doğrudan kullanma."""
    return s.replace("İ", "i").replace("I", "ı").lower()

# ── İlçe yardımcıları ───────────────────────────────────────────────────────
ILCE = {i["slug"]: i for i in D.ILCELER}
HIZMET = {h["slug"]: h for h in D.HIZMETLER}

def ek(i, hal="loc"):
    """i: ilçe dict'i veya slug. hal: loc(-de)/dat(-e)/gen(-in)/abl(-den)
    ⛔ Kod içinde elle "{ad}'da" YAZMA — Beşiktaş'ta / Fatih'te / Beylikdüzü'nde."""
    slug = i if isinstance(i, str) else i["slug"]
    l, d, g, a = D.ILCE_EK[slug]
    return ILCE[slug]["ad"] + {"loc": l, "dat": d, "gen": g, "abl": a}[hal]

def komsuluk_kur():
    """data.py'de bağlar tek yönlü yazılmış olabilir; iki yönlü hâle getiriliyor."""
    g = collections.defaultdict(set)
    for i in D.ILCELER:
        for k in i["komsu"]:
            if k in ILCE:
                g[i["slug"]].add(k)
                g[k].add(i["slug"])
    return {k: sorted(v) for k, v in g.items()}
KOMSU = komsuluk_kur()

def tohum(slug, tuz=""):
    """İlçeye özgü SABİT sayı — her derlemede aynı sonucu verir.
    ⚠️ random kullanılmıyor; build tekrarlanabilir olmalı."""
    h = hashlib.md5((slug + "|" + tuz).encode("utf-8")).hexdigest()
    return int(h[:8], 16)

def sec(liste, slug, tuz=""):
    return liste[tohum(slug, tuz) % len(liste)]

def ilce_yolu(i):
    return f"{i['slug']}-tikaniklik-acma/"

def hizmet_yolu(h):
    return f"{h['slug']}/"


# ── İkonlar (satır içi SVG — üçüncü parti ikon fontu YOK) ───────────────────
IK = {
 "tel":   '<path d="M2.5 4.5c0-1.1.9-2 2-2h2.2c.9 0 1.6.6 1.8 1.4l.7 2.8c.2.7-.1 1.4-.7 1.8l-1.3.9a12 12 0 0 0 5.4 5.4l.9-1.3c.4-.6 1.1-.9 1.8-.7l2.8.7c.8.2 1.4.9 1.4 1.8v2.2c0 1.1-.9 2-2 2C9.6 19.5 2.5 12.4 2.5 4.5Z"/>',
 "wa":    '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5 0-1 .2-3.3-.7-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.2.5-.3.6-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .6l-.4.5-.3.3c-.1.2-.2.3 0 .6.2.3.8 1.3 1.7 2.1 1.1 1 2 1.3 2.3 1.4.2.1.4.1.6-.1l.8-.9c.2-.2.4-.2.6-.1l1.9.9c.2.1.4.2.4.3.1.2.1.6 0 1Z"/>',
 "saat":  '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 10.6V6h-2v7.4l4.7 2.8 1-1.7-3.7-2Z"/>',
 "konum": '<path d="M12 2a7 7 0 0 0-7 7c0 5.1 6.3 12.3 6.6 12.6a.6.6 0 0 0 .9 0C12.7 21.3 19 14.1 19 9a7 7 0 0 0-7-7Zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2Z"/>',
 "posta": '<path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm9 8.1L4.4 7.3 4 7.9l8 6.1 8-6.1-.4-.6L12 13.1Z"/>',
 "kalkan":'<path d="M12 2 4 5.2v5.6c0 4.8 3.3 9.3 8 11.2 4.7-1.9 8-6.4 8-11.2V5.2L12 2Zm-1.2 13.6-3.2-3.2 1.4-1.4 1.8 1.8 4.6-4.6 1.4 1.4-6 6Z"/>',
 "dalga": '<path d="M2 9c2.2 0 2.2 2 4.4 2S8.6 9 10.8 9 13 11 15.2 11 17.4 9 19.6 9c1.3 0 1.8.7 2.4 1.2M2 14c2.2 0 2.2 2 4.4 2s2.2-2 4.4-2 2.2 2 4.4 2 2.2-2 4.4-2c1.3 0 1.8.7 2.4 1.2" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>',
 "gider": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm0 3.2a6.8 6.8 0 0 1 6.6 5.3H14a2 2 0 0 0-4 0H5.4A6.8 6.8 0 0 1 12 5.2ZM5.4 13.5H10a2 2 0 0 0 4 0h4.6A6.8 6.8 0 0 1 12 18.8a6.8 6.8 0 0 1-6.6-5.3Z"/>',
 "lavabo":'<path d="M4 11h16a1 1 0 0 1 1 1 7 7 0 0 1-7 7h-4a7 7 0 0 1-7-7 1 1 0 0 1 1-1Zm7-8h2v6h-2V3Zm-4 .5h2V5H7V3.5Z"/>',
 "tuvalet":'<path d="M6 3h2v8h9a1 1 0 0 1 1 1 7 7 0 0 1-4 6.3V21H8v-2.6A7 7 0 0 1 4 12V3h2Zm0 9a5 5 0 0 0 5 5h1a5 5 0 0 0 5-5H6Z"/>',
 "mutfak":'<path d="M7 2v7a3 3 0 0 0 2 2.8V22h2V11.8A3 3 0 0 0 13 9V2h-1.6v6H10V2H8.6v6H7V2Zm10 0c-1.7 0-3 2.7-3 6 0 2.6.8 4.8 2 5.6V22h2V2Z"/>',
 "banyo": '<path d="M6 2a3 3 0 0 0-3 3v7H2v2h1v2a4 4 0 0 0 3 3.9V21h2v-1h8v1h2v-1.1A4 4 0 0 0 21 16v-2h1v-2h-1V5a3 3 0 0 0-5.8-1.1l1.8.7A1 1 0 0 1 19 5v7H5V5a1 1 0 0 1 2 0v1h2V5a3 3 0 0 0-3-3Z"/>',
 "bina":  '<path d="M4 2h10v20H4V2Zm12 8h4v12h-4V10ZM6 5h2v2H6V5Zm4 0h2v2h-2V5ZM6 9h2v2H6V9Zm4 0h2v2h-2V9Zm-4 4h2v2H6v-2Zm4 0h2v2h-2v-2Zm-4 4h2v2H6v-2Zm4 0h2v2h-2v-2Zm8-4h2v2h-2v-2Z"/>',
 "rogar": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm0 2.2a7.8 7.8 0 1 1 0 15.6 7.8 7.8 0 0 1 0-15.6ZM7.5 8h9v1.6h-9V8Zm0 3.2h9v1.6h-9v-1.6Zm0 3.2h9V16h-9v-1.6Z"/>',
 "pimas": '<path d="M9 2h6v4h3a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h3V2Zm2 2v2h2V4h-2ZM7 8v12h10V8H7Zm2 2h6v2H9v-2Zm0 4h6v2H9v-2Z"/>',
 "kanal": '<path d="M2 6h6v2H4v8h4v2H2V6Zm14 0h6v12h-6v-2h4V8h-4V6Zm-6 1h4v10h-4V7Z"/>',
 "kamera":'<path d="M17 10.5V7a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1v-3.5l5 3.5V7l-5 3.5Z"/>',
 "robot": '<path d="M12 2a1.5 1.5 0 0 0-1 2.6V6H7a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V9a3 3 0 0 0-3-3h-4V4.6A1.5 1.5 0 0 0 12 2ZM8.5 11a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm7 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM8 16h8v1.5H8V16Z"/>',
 "simsek":'<path d="M13 2 4 13.5h6L9.5 22 20 9.5h-6.5L13 2Z"/>',
 "ok":    '<path d="M7 4.5 8.4 3.1 17.3 12l-8.9 8.9L7 19.5 14.5 12 7 4.5Z"/>',
 "menu":  '<path d="M3 6h18v2H3V6Zm0 5h18v2H3v-2Zm0 5h18v2H3v-2Z"/>',
 "kapat": '<path d="m5.3 3.9 14.8 14.8-1.4 1.4L3.9 5.3l1.4-1.4Zm14.8 1.4L5.3 20.1l-1.4-1.4L18.7 3.9l1.4 1.4Z"/>',
 "yildiz":'<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1L12 2Z"/>',
}

def svg(ad, sinif=""):
    s = f' class="{sinif}"' if sinif else ""
    return (f'<svg{s} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
            f'focusable="false">{IK[ad]}</svg>')

# ── Düğmeler ────────────────────────────────────────────────────────────────
def tel_btn(metin=None, sinif="dg dg-koyu"):
    return (f'<a class="{sinif}" href="tel:{S["tel_link"]}" '
            f'data-w4="ara">{svg("tel")}{e(metin or "Hemen Ara")}</a>')

def wa_btn(mesaj="Merhaba, tıkanıklık açma için bilgi almak istiyorum.", metin="WhatsApp",
           sinif="dg dg-wa"):
    from urllib.parse import quote
    return (f'<a class="{sinif}" href="https://wa.me/{S["wa"]}?text={quote(mesaj)}" '
            f'target="_blank" rel="noopener">{svg("wa")}{e(metin)}</a>')

def dock():
    """Yüzen eylem yığını — referans sitedeki desenin sadeleştirilmiş hâli."""
    return (
      '<div class="dock">'
      f'<a class="d-koyu" href="tel:{S["tel_link"]}">{svg("tel")}<span class="yz">Acil Tesisatçı</span></a>'
      f'<a class="d-koyu" href="tel:{S["tel_link"]}">{svg("gider")}<span class="yz">Gider Açma</span></a>'
      f'<a class="d-wa" href="https://wa.me/{S["wa"]}" target="_blank" rel="noopener">'
      f'{svg("wa")}<span class="yz">WhatsApp</span></a>'
      '</div>')


# ── Hero ızgarası ───────────────────────────────────────────────────────────
# ⚠️ Görsel henüz yüklenmemişse sağ sütun boş kalıyor ve üstündeki yüzen kart
#    havada duruyordu. Görsel yoksa hero TEK SÜTUNA düşüyor.
HERO_GORSEL = "tikaniklik-acma-servisi"

def hero_sag(alt, kart=True):
    g = gorsel(HERO_GORSEL, alt, oncelik=True)
    if not g:
        return "", " hero-tek"
    k = ('<div class="hero-kart"><span class="yv">' + svg("kalkan") + '</span>'
         '<span><b>Kırmadan, dökmeden</b>'
         '<span>Kameralı tespit ile kalıcı çözüm</span></span></div>') if kart else ""
    return f'<div class="hero-gorsel">{g}{k}</div>', ""

# ── Logo ────────────────────────────────────────────────────────────────────
def logo(koyu_zemin=False):
    """⏳ Gerçek marka logosu gelene kadar tipografik işaret + damla sembolü.
    Referans sitedeki logo 'TESSA' üstte, 'TESİSAT' altta harf aralıklı."""
    renk = "#fff" if koyu_zemin else "var(--metin)"
    return (
      f'<a class="logo" href="{ic()}" aria-label="{e(S["marka"])} ana sayfa">'
      f'<svg width="34" height="40" viewBox="0 0 34 40" aria-hidden="true" focusable="false">'
      f'<path d="M17 1C17 1 3 15.4 3 24.2A14 14 0 0 0 31 24.2C31 15.4 17 1 17 1Z" '
      f'fill="var(--altin)"/>'
      f'<path d="M17 9.5c0 0-7.4 8-7.4 13.1a7.4 7.4 0 0 0 14.8 0C24.4 17.5 17 9.5 17 9.5Z" '
      f'fill="{"#0E1D2E" if not koyu_zemin else "#16293D"}" opacity=".92"/></svg>'
      f'<span class="logo-yz"><b style="color:{renk}">TESSA</b><span>TESİSAT</span></span></a>')

# ── head ────────────────────────────────────────────────────────────────────
def head(baslik, aciklama, yol, sema="", tur="website"):
    """yol: site köküne göre ('' = anasayfa, 'esenler-tikaniklik-acma/')
    ⚠️ canonical / og:url / sitemap MUTLAK kalır — üretim adresini gösterirler."""
    kanonik = ALAN + "/" + yol
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(baslik)}</title>
<meta name="description" content="{e(kirp(aciklama))}">
<link rel="canonical" href="{e(kanonik)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta property="og:type" content="{tur}">
<meta property="og:site_name" content="{e(S["marka"])}">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{e(baslik)}">
<meta property="og:description" content="{e(kirp(aciklama))}">
<meta property="og:url" content="{e(kanonik)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E1D2E">
<link rel="icon" href="{ic("favicon.ico")}" sizes="any">
<link rel="icon" type="image/png" href="{ic("images/favicon-48.png")}" sizes="48x48">
<link rel="apple-touch-icon" href="{ic("images/apple-touch-icon.png")}">
<link rel="preload" as="font" type="font/woff2" href="{ic("assets/fonts/pjs-var-tr.woff2")}" crossorigin>
<link rel="stylesheet" href="{ic(surum("assets/css/site.css"))}">
{sema}</head>
<body>
<a class="sr" href="#ana">İçeriğe atla</a>
"""

# ── Üst başlık ──────────────────────────────────────────────────────────────
def ust_header(aktif=""):
    ogeler = [("", "Ana Sayfa", "anasayfa"), ("hakkimizda/", "Hakkımızda", "hakkimizda")]
    son = [("bolgeler/", "Bölgeler", "bolgeler"), ("iletisim/", "İletişim", "iletisim")]

    def bag(yol, ad, anahtar):
        gec = ' aria-current="page"' if aktif == anahtar else ""
        return f'<a href="{ic(yol)}"{gec}>{e(ad)}</a>'

    acilir = "".join(
        f'<a href="{ic(hizmet_yolu(HIZMET[s]))}">{e(HIZMET[s]["ad"])}</a>'
        for s in D.MENU_HIZMET)
    acilir += f'<a href="{ic("hizmetler/")}"><b>Tüm Hizmetler →</b></a>'

    return f"""<header class="ust">
<div class="kap ust-ic">
{logo()}
<nav class="menu" aria-label="Ana menü">
{bag(*ogeler[0])}
{bag(*ogeler[1])}
<div class="acilir"><button type="button" aria-expanded="false">Hizmetler{svg("ok")}</button>
<div class="acilir-liste">{acilir}</div></div>
{bag(*son[0])}
{bag(*son[1])}
</nav>
<div class="ust-sag">
<a class="tel-kart" href="tel:{S["tel_link"]}">
<span class="yv">{svg("tel")}</span>
<span class="yz"><small>Acil Tesisatçı</small><b>{e(S["tel_goster"])}</b></span></a>
{wa_btn(metin="WhatsApp", sinif="dg dg-wa dg-sm")}
<button class="mnu-ac" type="button" aria-expanded="false" aria-label="Menüyü aç">{svg("menu")}</button>
</div>
</div>
</header>
"""

# ── Kırıntı ─────────────────────────────────────────────────────────────────
def kirinti(parcalar):
    """parcalar: [(ad, yol veya None), ...] — sonuncusu bulunulan sayfa."""
    ic_html, ldj = [], []
    tam = [("Ana Sayfa", "")] + parcalar
    for n, (ad, yol) in enumerate(tam, 1):
        if n == len(tam):
            ic_html.append(f'<li><span aria-current="page">{e(ad)}</span></li>')
        else:
            ic_html.append(f'<li><a href="{ic(yol or "")}">{e(ad)}</a></li>')
        ldj.append({"@type": "ListItem", "position": n, "name": ad,
                    "item": ALAN + "/" + (yol or "")})
    sema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ldj}
    return (f'<nav class="kirinti" aria-label="Sayfa yolu"><div class="kap"><ol>'
            f'{"".join(ic_html)}</ol></div></nav>' + ldj_yaz(sema))

def ldj_yaz(nesne):
    return ('<script type="application/ld+json">'
            + json.dumps(nesne, ensure_ascii=False, separators=(",", ":"))
            + "</script>")


# ── Web4Medya imzası ────────────────────────────────────────────────────────
def w4_imza():
    """⚠️ Bağlantı YALNIZCA marka adını sarar; "Web Tasarım:" etiketi <a>'nın
    DIŞINDA kalır. Rozetin tamamı bağlantı olsaydı 60 sayfadan çıkan anahtar
    kelimeli tasarımcı linki Google'ın link şeması tarifine girerdi.
    ⛔ Rozeti <a> yapma, geri çevirme ([[reference_w4_tasarim_imzasi]])."""
    return ('<div class="w4"><span class="w4-bag">'
            '<span class="w4-etiket">Web Tasarım:</span>'
            '<a class="w4-ad" href="https://www.web4medya.com/" target="_blank" '
            'rel="noopener">Web<span class="w4-d">4</span>Medya</a>'
            '</span></div>')

# ── Alt bilgi ───────────────────────────────────────────────────────────────
def alt_bilgi():
    menu_bag = [("", "Ana Sayfa"), ("hakkimizda/", "Hakkımızda"), ("hizmetler/", "Hizmetlerimiz"),
                ("bolgeler/", "Hizmet Bölgeleri"), ("iletisim/", "İletişim"),
                ("gizlilik-politikasi/", "Gizlilik Politikası"), ("kullanim-sartlari/", "Kullanım Şartları")]
    hiz_bag = [(hizmet_yolu(HIZMET[s]), HIZMET[s]["ad"]) for s in D.MENU_HIZMET[:6]]

    def liste(ogeler):
        return "".join(f'<li><a href="{ic(y)}">{e(a)}</a></li>' for y, a in ogeler)

    return f"""
<section class="ft-serit"><div class="kap">
<b>{e(S["marka"])} — 7/24 tıkanıklık açma ve gider açma</b>
{wa_btn(metin="WhatsApp'tan yaz", sinif="dg dg-wa dg-sm")}
</div></section>
<footer class="ft">
<div class="kap">
<div class="ft-izgara">
<div>
<div class="ft-logo">{logo(koyu_zemin=True)}</div>
<p>Lavabo, tuvalet, mutfak ve ana gider tıkanıklıklarında kırmadan çalışıyoruz.
Tıkanıklığın yerini kamerayla bulup sebebini ortadan kaldırıyoruz — İstanbul'un
39 ilçesinde 7/24 hizmetinizdeyiz.</p>
<p><a class="dg dg-cizgi dg-sm" href="{ic("bolgeler/")}">{svg("konum")}Hizmet Bölgelerimiz</a></p>
</div>
<div><h4>Menü</h4><ul>{liste(menu_bag)}</ul></div>
<div><h4>Hizmetler</h4><ul>{liste(hiz_bag)}
<li><a href="{ic("hizmetler/")}">Tüm Hizmetler</a></li></ul></div>
<div><h4>İletişim</h4>
<div class="ft-ilet">
<div class="sr-k"><span class="yv">{svg("konum")}</span><span>
<small>Adres</small><span>{e(S["adres"])}</span></span></div>
<div class="sr-k"><span class="yv">{svg("tel")}</span><span>
<small>Telefon</small><a href="tel:{S["tel_link"]}">{e(S["tel_goster"])}</a></span></div>
<div class="sr-k"><span class="yv">{svg("posta")}</span><span>
<small>E-posta</small><a href="mailto:{S["eposta"]}">{e(S["eposta"])}</a></span></div>
<div class="sr-k"><span class="yv">{svg("saat")}</span><span>
<small>Çalışma Saatleri</small><span>{e(S["saat"])}</span></span></div>
</div></div>
</div>
<div class="ft-alt">
<span>© 2026 {e(S["marka"])}. Tüm hakları saklıdır.</span>
<a href="{ic("sitemap.xml")}">Site Haritası</a>
</div>
</div>
{w4_imza()}
</footer>
{dock()}
<script src="{ic(surum("assets/js/app.js"))}" defer></script>
</body>
</html>
"""

# ── Harita (facade) ─────────────────────────────────────────────────────────
def harita(baslik="Deponun konumu"):
    """⚠️ iframe tıklanana kadar DOM'a GİRMİYOR → ilk yükte 0 üçüncü parti istek.
    Referans sitede harita doğrudan gömülüydü; her sayfada Google'a istek çıkıyordu."""
    return (f'<div class="harita" data-src="{e(S["harita_embed"])}" '
            f'data-baslik="{e(S["harita_baslik"])}">'
            f'<button class="harita-ac" type="button">'
            f'<span class="pin">{svg("konum")}</span>'
            f'<b>{e(baslik)}</b>'
            f'<span>{e(S["adres"])} — haritayı açmak için tıklayın.</span>'
            f'</button></div>')

# ── Video ───────────────────────────────────────────────────────────────────
def video_var(dosya):
    return os.path.exists(os.path.join(KOK, "videos", dosya + ".mp4"))

def video_bolum(sayfa_anahtari, baslik="Çalışmalarımızdan"):
    """⚠️ Dosya yoksa bölüm HİÇ basılmaz — boş kutu çıkmaz."""
    v = [x for x in D.VIDEOLAR if sayfa_anahtari in x["sayfa"] and video_var(x["dosya"])]
    if not v:
        return ""
    kartlar = []
    for x in v:
        poster = f'videos/{x["dosya"]}.jpg'
        p = f' poster="{ic(poster)}"' if os.path.exists(os.path.join(KOK, poster)) else ""
        kartlar.append(
          f'<figure class="vid"><video controls preload="none"{p} '
          f'playsinline width="640" height="400">'
          f'<source src="{ic("videos/" + x["dosya"] + ".mp4")}" type="video/mp4">'
          f'Tarayıcınız videoyu desteklemiyor.</video>'
          f'<figcaption class="yz"><b>{e(x["baslik"])}</b>'
          f'<span>{e(x["alt"])}</span></figcaption></figure>')
    return (f'<section class="bolum bolum-ac"><div class="kap">'
            f'<div class="b-ust"><span class="b-etiket">Sahadan</span>'
            f'<h2>{e(baslik)}</h2></div>'
            f'<div class="vid-izgara">{"".join(kartlar)}</div></div></section>')


# ── İçerik üreticileri ──────────────────────────────────────────────────────
# Metin 1. şahıs usta sesiyle yazıldı. ⛔ UYDURMA vaka/rakam/süre YOK.
# İlçe farkı; yapı stoğu, hat karakteri, baskın tıkanma sebebi ve erişim
# koşulundan geliyor — kelime değiştirerek 39 kopya üretilmiyor.

def p(*paragraflar):
    return "".join(f"<p>{x}</p>" for x in paragraflar if x)

def mahalle_cumlesi(i, kac=3):
    m = i["mahalle"]
    b = tohum(i["slug"], "mah") % len(m)
    sec_m = [m[(b + n) % len(m)] for n in range(min(kac, len(m)))]
    if len(sec_m) == 1:
        return sec_m[0]
    return ", ".join(sec_m[:-1]) + " ve " + sec_m[-1]

def tel_vurgu():
    return (f'<a href="tel:{S["tel_link"]}"><b>{e(S["tel_goster"])}</b></a>')

def G(anahtar, i):
    """H2 gövdesi üretir. i: ilçe dict'i."""
    ad, loc, dat, gen, abl = i["ad"], ek(i, "loc"), ek(i, "dat"), ek(i, "gen"), ek(i, "abl")
    mah = mahalle_cumlesi(i)
    yapi, hat, risk, erisim = i["yapi"], i["hat"], i["risk"], i["erisim"]

    # ── Usta / servis ──
    if anahtar in ("usta", "usta_cagir", "servis", "usta_gider", "actirmak",
                   "servis_ara", "tesisatci_usta", "actirma_gider"):
        giris = {
          "usta":        f"{loc} tıkanıklık açma ustası ararken en çok sorulan şey şu: gelen kişi işi gerçekten çözecek mi, yoksa bir süre sonra aynı sorun tekrar mı edecek?",
          "usta_cagir":  f"{loc} tıkanıklık ustası çağırmadan önce bilmeniz gereken bir şey var: tıkanıklığın nerede olduğunu bilmeden çağırılan usta, işin yarısını tahminle yapar.",
          "servis":      f"{loc} tıkanıklık açma servisi olarak çalışırken önce şunu ayırıyoruz: sorun dairenin kendi hattında mı, yoksa binanın ortak kolonunda mı?",
          "usta_gider":  f"{loc} gider açma ustası aradığınızda, karşınızdakinin elindeki ekipman işin sonucunu doğrudan belirler.",
          "actirmak":    f"{loc} tıkanıklık açtırmak isteyenlerin çoğu bize zaten bir şeyler denedikten sonra ulaşıyor: pompa, tel, market kimyasalı..",
          "servis_ara":  f"{loc} tıkanıklık servisi ararken telefonda birkaç soru sormamız sizi şaşırtmasın — o sorular ekibin hangi makineyle geleceğini belirliyor.",
          "tesisatci_usta": f"{loc} su tesisatçısı ve tıkanıklık ustası çoğu zaman aynı kişi sanılır ama ekipman tarafında ciddi fark vardır.",
          "actirma_gider": f"{loc} gider açtırma işini iki şekilde yapabilirsiniz: tıkanıklığı iterek geçici olarak akıtmak, ya da tıkayan kütleyi hattan çıkarmak.",
        }[anahtar]
        return p(
          giris,
          f"Biz ikinci yolu seçiyoruz. Önce hangi giderlerin etkilendiğini dinliyoruz, sonra "
          f"gerekiyorsa kamerayla hattın içine bakıyoruz. Tıkanıklığın cinsini görmeden makine "
          f"seçilmez — saç ve sabun artığıyla donmuş yağ aynı uçla açılmaz.",
          f"{ad} tarafında {yapi} ağırlıkta. Bu da şu demek: {hat}. Ekibimiz {loc} çalışırken "
          f"bunu baştan hesaba katıyor, {erisim}.",
          f"{mah} ve çevresindeki mahallelerde günün her saati müdahale ediyoruz. "
          f"Tıkanıklık gece de olsa {tel_vurgu()} numarasından ulaşabilirsiniz.")

    # ── Telefon / numara ──
    if anahtar in ("numara", "telefon", "kimi_ara", "telefon_gider", "acil_numara"):
        giris = {
          "numara":       f"{ad} tıkanıklık açma servisi için aramanız gereken numara tek: {tel_vurgu()}.",
          "telefon":      f"{ad} tıkanıklık servisi telefonu {tel_vurgu()} — santral yok, doğrudan ekibe düşer.",
          "kimi_ara":     f"{loc} tıkanıklık olduğunda kimi arayacağınızı düşünmeden önce bir dakika durun: durumu doğru anlatmak, gelen ekibin doğru ekipmanla gelmesini sağlar.",
          "telefon_gider":f"{ad} gider açma servisi telefon numaramız {tel_vurgu()}. Aradığınızda ilk soracağımız şey adres değil, hangi giderlerin taştığı olacak.",
          "acil_numara":  f"{loc} acil tesisatçı numarası arıyorsanız {tel_vurgu()} numarasını kaydedin — su taştığında numara aramakla geçen dakika pahalıya mal oluyor.",
        }[anahtar]
        return p(
          giris,
          f"Telefonda size şunları soruyoruz: Hangi gider tıkalı — lavabo mu, klozet mi, yer "
          f"süzgeci mi? Evdeki başka giderler de yavaşladı mı? Alt kattaki komşuda aynı sorun "
          f"var mı? Bu üç sorunun cevabı, tıkanıklığın daire içinde mi bina kolonunda mı "
          f"olduğunu büyük ölçüde belli ediyor.",
          f"Cevaba göre ekip ya elde taşınan robot makineyle ya da basınçlı su ünitesiyle yola "
          f"çıkıyor. {ad} tarafında {erisim}.",
          f"Yazmayı tercih ederseniz WhatsApp'tan fotoğraf da gönderebilirsiniz; giderin ve "
          f"çevresinin fotoğrafı çoğu zaman uzun bir tariften daha açıklayıcı oluyor.")

    # ── Yakınlık / aciliyet ──
    if anahtar in ("yakin", "yakin_ekip", "hizli", "acil", "yedi24", "yakinimda"):
        giris = {
          "yakin":     f"{ad} en yakın tıkanıklık servisi denince akla haritadaki en kısa mesafe geliyor; oysa belirleyici olan o an {dat} en yakın olan ekibin nerede olduğu.",
          "yakin_ekip":f"{ad} en yakın tıkanıklık açma ekibini yönlendirirken mesafeye değil, o anda müsait olan ve doğru makineyi taşıyan araca bakıyoruz.",
          "hizli":     f"\"{loc} en hızlı tıkanıklık servisi hangisi?\" sorusunun dürüst cevabı şu: hız tek başına bir şey ifade etmiyor.",
          "acil":      f"{loc} acil tıkanıklık açma dediğimiz durum bellidir — su taşıyor, gider geri basıyor ya da koku evi almış durumda.",
          "yedi24":    f"{loc} 7/24 tıkanıklık açma veriyoruz; çünkü tıkanıklık mesai saatine göre olmuyor.",
          "yakinimda": f"Telefonunuza \"yakınımdaki tıkanıklık açma servisi\" yazdıysanız muhtemelen işiniz acele. {loc} o an sahada olan ekibe bağlanıyorsunuz.",
        }[anahtar]
        ikinci = ("Bir ekip doğru makineyle 40 dakikada gelip işi bitirir; yanlış ekipmanla gelen "
                  "ekip 15 dakikada kapınızda olur ama tıkanıklığı iterek geçiştirir, iki hafta "
                  "sonra aynı yerden yine ararsınız. Biz telefonda sorduğumuz sorularla doğru "
                  "aracı gönderip tek seferde bitirmeyi hedefliyoruz."
                  if anahtar == "hizli" else
                  "Ekiplerimiz İstanbul'un iki yakasında dağınık çalışıyor; deponun bulunduğu "
                  f"{S['merkez_ilce']} çıkışlı araç dışında, size yakın bölgede iş bitiren bir "
                  "ekip varsa yönlendirme oradan yapılıyor.")
        return p(
          giris, ikinci,
          f"{ad} özelinde dikkat ettiğimiz nokta şu: {erisim}. Bu yüzden telefonda adresi "
          f"alırken sokak ve bina girişini de netleştiriyoruz — araç yanaşamayan yerlerde "
          f"taşınabilir ekipmanla çıkıyoruz.",
          f"Su taşıyorsa ekibi beklerken yapabileceğiniz en faydalı şey, o hatta bağlı bütün "
          f"muslukları kapatıp gidere su vermeyi kesmek. Kimyasal dökmeyin — hem işe yaramıyor "
          f"hem de açma sırasında sıçrama riski yaratıyor.")

    return ""


def G2(anahtar, i):
    """H2 gövdesi — gider tipleri ve yöntemler."""
    ad, loc, dat, gen = i["ad"], ek(i, "loc"), ek(i, "dat"), ek(i, "gen")
    yapi, hat, risk, erisim = i["yapi"], i["hat"], i["risk"], i["erisim"]

    if anahtar == "mutfak":
        return p(
          f"{loc} açtığımız mutfak giderlerinin neredeyse tamamında aynı şeyi buluyoruz: "
          f"soğuyup boruya yapışmış yağ. Tavadaki yağ sıcakken akıcıdır, gider borusuna girip "
          f"soğuduğunda çepere yapışır. Üstüne çay posası, pirinç ve yemek artığı eklendikçe "
          f"boru içten içe daralır.",
          f"Bu yüzden mutfak tıkanıklığında tıkacı delip geçmek yetmiyor — çeperdeki tabakayı "
          f"da sökmek gerekiyor. Yoksa birkaç hafta içinde aynı noktadan tekrar kapanıyor.",
          f"{ad} tarafında {yapi} olduğu için mutfak pimaşları çoğunlukla ortak kolona bağlı. "
          f"Tek dairede başlayan yağ birikmesi zamanla alttaki komşuyu da etkileyebiliyor; "
          f"o yüzden kolonun durumunu da kontrol ediyoruz.")

    if anahtar == "lavabo":
        return p(
          f"Lavabo tıkanıklığında ilk baktığımız yer sifon — lavabonun altındaki U şeklindeki "
          f"parça. Kokuyu tutsun diye sürekli su barındırır, aynı sebeple tortu da orada birikir. "
          f"{loc} çıktığımız işlerin azımsanmayacak bir kısmı sifonu sökünce bitiyor.",
          f"Sifon temizse tıkanıklık daha ileridedir. O zaman ince çaplı spiralle gider hattına "
          f"giriyor, kütleyi parçalayıp dışarı alıyoruz. Banyo lavabosunda sebep genelde saç ve "
          f"sabun; mutfakta yağ ve yemek artığı. İkisi aynı uçla açılmaz.",
          f"Lavaboya kimyasal döktüyseniz lütfen söyleyin — açarken sıçrama riski oluyor, "
          f"koruyucu ekipmanla çalışmamız gerekiyor.")

    if anahtar in ("tuvalet", "klozet"):
        return p(
          f"Tuvalet ve klozet tıkanıklığı diğerlerinden bir yönüyle ayrılıyor: sebep genelde "
          f"birikme değil, gidere ait olmayan bir şeyin atılmasıdır. Islak mendil başı çekiyor — "
          f"ambalajında ne yazarsa yazsın tuvalet kâğıdı gibi dağılmıyor, boruda açılıp bir bez "
          f"gibi hattı kapatıyor.",
          f"Klozeti yerinden sökmeden, çelik yaylı robot makineyle klozet çıkışından hatta "
          f"giriyoruz. Makine tıkacı parçalıyor ya da yabancı cismi kavrayıp geri çekiyor. "
          f"Fayans kırmak gerekmiyor.",
          f"<b>Klozet taşıyorsa sifonu tekrar çekmeyin.</b> En sık yapılan hata bu: ikinci sifon "
          f"tıkanıklığı açmaz, sadece hazne dolusu suyu taşan klozete ekler. Rezervuarın ara "
          f"musluğunu kapatıp bizi arayın — {loc} gece de olsa geliyoruz.")

    if anahtar == "banyo":
        return p(
          f"Banyo gideri ve yer süzgeci tıkanıklığı neredeyse her zaman aynı iki maddeden "
          f"çıkıyor: saç ve sabun. Saç tek başına akıp gidebilir, sabun tek başına sorun "
          f"çıkarmaz — ama ikisi birleşince boruya yapışan, elle bile zor koparılan keçemsi "
          f"bir kütle oluşuyor.",
          f"Seramiği kırmadan çalışıyoruz: süzgeci ve varsa tıkaç düzeneğini söküp hazneyi "
          f"boşaltıyoruz, sonra gerekiyorsa yer süzgecinden spiralle hatta giriyoruz. Küvet ve "
          f"duş teknelerinde taşma deliğinden de erişim mümkün.",
          f"Yer süzgecinden <b>gri, köpüklü su geri geliyorsa</b> bu artık daire içi bir "
          f"tıkanıklık değil — bina hattına bakmak gerekiyor. {ad} özelinde {risk} sık "
          f"karşımıza çıktığı için bu ayrımı baştan yapıyoruz.")

    if anahtar in ("gider", "gider_nasil"):
        giris = (f"{loc} gider açma işini iki şekilde yapmak mümkün: tıkacın ortasında bir kanal "
                 f"açıp suyu akıtmak, ya da tıkayan kütleyi hattan tamamen çıkarmak."
                 if anahtar == "gider" else
                 f"\"{loc} gider açma nasıl yapılır?\" diye soruyorsanız, işin sırası şöyle "
                 f"işliyor:")
        return p(
          giris,
          f"Birincisi hızlıdır ve o gün sorunu çözmüş gibi görünür; ikincisi biraz daha uzun "
          f"sürer ama aynı yerden tekrar aramazsınız. Biz ikincisini yapıyoruz.",
          f"Önce hangi giderlerin etkilendiğini dinliyoruz — bu, tıkanıklığın daire içinde mi "
          f"bina kolonunda mı olduğunu büyük ölçüde belli ediyor. Sonra uygun makineyle "
          f"müdahale ediyor, gerekiyorsa kamerayla hattın içine bakıyoruz. "
          f"{ad} tarafında {hat}, bu yüzden {kucuk(risk)} sık görülüyor.",
          f"İş bittikten sonra hattı su vererek test ediyoruz; akış normale dönmeden ayrılmıyoruz.")

    if anahtar == "anagider":
        return p(
          f"Bina ana gideri tıkandığında belirti bellidir: evdeki birden fazla gider aynı anda "
          f"yavaşlar, en alttaki daire ya da bodrum kat su alır. Tek bir dairenin kendi hattını "
          f"açmak bu durumda hiçbir şey değiştirmez.",
          f"Ana kolon ve bina çıkış hattı için daire içi ekipman yetmiyor; endüstriyel robot "
          f"makine ve basınçlı su ünitesiyle, binanın temizleme kapağından ya da bahçedeki "
          f"rögardan çalışıyoruz.",
          f"{ad} tarafında {yapi} ağırlıkta ve {hat}. {gen} özellikle yoğun sokaklarında tek bir "
          f"ana hat tıkanınca birden fazla bina etkilenebiliyor — böyle durumlarda sorunun "
          f"binanın parseli içinde mi yoksa sokaktaki ana şebekede mi olduğunu ayırmak "
          f"gerekiyor. Bu ayrımı kamerayla yapıyoruz.")

    if anahtar == "logar":
        return p(
          f"Logar ve rögar, binanın pis su hattının yer altındaki buluşma noktası. Buradaki "
          f"tıkanıklık genelde daire içindekinden farklı bir sebepten oluyor: kök sarması, "
          f"çökme, ya da yıllar içinde biriken katı atık.",
          f"Kapağı açıp kamerayla hattı takip ediyoruz. Kök varsa kesici uçla temizliyor, tortu "
          f"varsa basınçlı su ile çeperi yıkıyoruz. Boruda kırık ya da ters eğim varsa bunu "
          f"da görüntüyle gösteriyoruz — çünkü o durumda açmak kalıcı çözüm değil.",
          f"{loc} {kucuk(erisim)}. Bahçeli parsellerde rögar kapağının yeri unutulmuş olabiliyor; "
          f"gerekirse hattı takip ederek yerini tespit ediyoruz.")

    if anahtar == "kirmadan":
        return p(
          f"\"Kırmak gerekir mi?\" {loc} en çok sorulan soru bu. Cevap: hayır, normal şartlarda "
          f"gerekmiyor. Çalışmanın tamamını mevcut giriş noktalarından yapıyoruz — gider ağzı, "
          f"yer süzgeci, klozet çıkışı, temizleme kapağı ya da rögar.",
          f"Kırma yalnızca boruda <b>çökme veya kırık</b> varsa gündeme geliyor. O durumda da "
          f"önce kamerayla tam noktayı gösteriyor, ne yapılacağını anlatıyor ve onayınızı "
          f"almadan hiçbir yere dokunmuyoruz.",
          f"{ad} tarafında {yapi} bulunduğu için bu özellikle önemli: eski yapıda gereksiz "
          f"kırım, tıkanıklıktan çok daha pahalı bir tamirata dönüşebiliyor.")

    if anahtar == "kamera":
        return p(
          f"Fiber optik kamera, tıkanıklık işinde tahmin etmeyi bırakıp görmeyi sağlıyor. "
          f"Kamerayı hatta sürüyor, ekrandan tıkanıklığın <b>kaç metre ileride</b> olduğunu ve "
          f"<b>neden</b> oluştuğunu birlikte izliyoruz.",
          f"Bu özellikle iki durumda fark yaratıyor: aynı gider kısa aralıklarla tekrar "
          f"tıkanıyorsa, ve tıkanıklığın daire içinde mi bina hattında mı olduğu belirsizse. "
          f"Görüntü olmadan bu ikisi ancak deneyerek anlaşılır — deneme de zaman ve para demek.",
          f"{loc} {kucuk(hat)} bulunduğu için kamerayla teşhis çoğu işte ilk adımımız oluyor.")

    if anahtar == "robot":
        return p(
          f"Robot dediğimiz şey, ucunda değişebilir kesici başlıklar olan çelik yaylı makine. "
          f"Yay hattın dirseklerini takip ederek ilerliyor, uç tıkacı parçalıyor ya da yabancı "
          f"cismi kavrayıp geri çekiyor.",
          f"Boru çapına ve tıkanıklığın cinsine göre farklı yay kalınlığı ve uç kullanılıyor. "
          f"Saç kütlesiyle sertleşmiş yağ aynı uçla açılmaz; kök sarması için ise kesici uç "
          f"gerekiyor. Yanlış uç seçimi hem işi çözmez hem boruyu yorar.",
          f"{ad} tarafında {kucuk(risk)} yaygın olduğu için ekip yola çıkarken buna uygun "
          f"başlıkları da alıyor.")

    if anahtar == "pimas":
        return p(
          f"Pimaş, binanın katları boyunca inen dikey pis su kolonu. İçinde yıllar boyunca "
          f"biriken yağ ve tortu tabakası boru çapını içten daraltıyor; bir noktadan sonra "
          f"normal kullanım bile tıkanmaya yetiyor.",
          f"Pimaş yıkamada tıkanıklığı açmakla yetinmiyoruz — yüksek basınçlı su ile çeperdeki "
          f"tabakayı da söküyoruz. İşlem öncesi ve sonrası kamerayla görüntü alınabiliyor, "
          f"yönetime rapor gerekiyorsa bu işe yarıyor.",
          f"{loc} {kucuk(yapi)} bulunan binalarda pimaş yıkama, tek tek daire müdahalelerinden "
          f"daha ekonomik çıkıyor; çünkü sorun tek dairede değil kolonun kendisinde oluyor.")

    if anahtar == "kanal":
        return p(
          f"Kanal ve kanalizasyon açma, bina çıkışından sonraki hattın işi. Burada tıkanıklığın "
          f"sebebi daire içindekinden farklı: ağaç kökü, çökme, zeminden giren toprak ya da "
          f"yıllarca biriken katı atık.",
          f"Endüstriyel makine ve basınçlı su ünitesiyle çalışıyoruz. Hattın durumunu kamerayla "
          f"görüntüleyip sorunun parsel içinde mi sokaktaki ana şebekede mi olduğunu net olarak "
          f"ortaya koyuyoruz — bu ayrım kimin ne yapacağını belirliyor.",
          f"{ad} tarafında {kucuk(hat)}; {kucuk(erisim)}.")

    if anahtar == "kapanis":
        return p(
          f"Özetle: {loc} tıkanıklık açma ve gider açma işini kırmadan, tıkanıklığın sebebini "
          f"ortadan kaldıracak şekilde yapıyoruz. Tıkacı delip geçmek yerine çıkarıyoruz; "
          f"gerekiyorsa kamerayla hattı görüntüleyip neden tıkandığını da gösteriyoruz.",
          f"Lavabo, klozet, banyo gideri, mutfak pimaşı, bina ana kolonu, logar ve bahçe hattı — "
          f"hepsinde aynı ekip ve aynı ekipmanla çalışıyoruz. {kucuk(erisim).capitalize() if False else erisim.capitalize()}.",
          f"Tıkanıklık saat gözetmiyor; biz de gözetmiyoruz. {tel_vurgu()} numarasından günün "
          f"her saati ulaşabilirsiniz.")
    return ""


# ── Belediye / İSKİ bölümü ──────────────────────────────────────────────────
def belediye_bolum(i):
    """⚠️ Kullanıcı isteği (2026-09-18): her ilçe sayfasında belediye/İSKİ
    sorumluluğu ve numaraları. Bilgi DOĞRU olacak ama asıl hedef bize ulaşmak.
    ⛔ 39 ilçe belediyesi numarası UYDURULMADI — İstanbul'da kanalizasyon yetkisi
       İSKİ'dedir, ilçe belediyesi zaten doğru adres değil. bel_tel dolu olan
       ilçede ek satır otomatik basılır."""
    K = D.KURUM
    ad, loc, gen = i["ad"], ek(i, "loc"), ek(i, "gen")
    satir = "".join(
      f"<tr><td>{e(n)}</td><td>{e(k)}</td><td>{e(b)}</td></tr>"
      for n, k, b in D.SORUMLULUK)

    bel = ""
    if i.get("bel_tel"):
        bel = (f'<li>{ad} Belediyesi çağrı merkezi: '
               f'<a href="tel:{i["bel_tel_link"]}"><b>{e(i["bel_tel"])}</b></a></li>')

    return f"""
<h2 id="belediye">{e(ad)} Tıkanıklık Açma Belediye mi Yapar, İSKİ mi Geliyor?</h2>
{p(f"{loc} tıkanıklık olduğunda ilk akla gelen sorulardan biri bu — hatta pek çok kişi önce "
   f"belediyeyi arıyor. Dürüst cevap şu: <b>İSKİ ve belediye, dairenizin ya da binanızın "
   f"içindeki tıkanıklığa gelmez.</b> Onların sorumluluğu sokaktaki ana kanalizasyon "
   f"şebekesinde biter.",
   f"Sınır şurada çiziliyor: bina çıkışından sokaktaki ana hatta bağlanan <b>parsel içi</b> "
   f"tesisat mülk sahibinin sorumluluğunda. Ana hattın kendisi ve sokaktaki rögar İSKİ'nin. "
   f"{loc} yaşanan tıkanıklıkların büyük kısmı ilk gruba giriyor — yani özel tesisatçının işi.")}
<div class="tbl"><table>
<thead><tr><th>Tıkanıklık nerede?</th><th>Kim sorumlu?</th><th>Nereye başvurulur?</th></tr></thead>
<tbody>{satir}</tbody></table></div>
<h3>{e(ad)} İçin Kurum İletişim Numaraları</h3>
<ul>
<li>{e(K["iski_ad"])} arıza hattı: <a href="tel:{K["iski_tel_link"]}"><b>ALO {e(K["iski_tel"])}</b></a>
 — 7/24, sokaktaki ana kanalizasyon arızası için.</li>
<li>İstanbul dışından İSKİ: <a href="tel:{K["iski_disari_link"]}">{e(K["iski_disari"])}</a></li>
<li>{e(K["ibb_ad"])}: <a href="tel:{K["ibb_tel_link"]}"><b>ALO {e(K["ibb_tel"])}</b></a>
 — yol üstü yağmur suyu ızgarası ve genel başvurular için.</li>
{bel}
</ul>
{p(f"185'i aradığınızda ekip gelip <b>sokaktaki hattı</b> kontrol eder. Sorun sizin parselinizin "
   f"içindeyse tutanak tutulur ve iş size bırakılır — bu tamamen usulüne uygundur, kurum kendi "
   f"yetki alanına bakmıştır.",
   f"Yani ana hat tıkanıklığından şüpheleniyorsanız 185'i aramak doğru adım. Ama lavabonuz, "
   f"klozetiniz, banyo gideriniz ya da binanızın kolonu tıkandıysa beklemenin bir faydası yok; "
   f"o iş baştan özel tesisatçının işi.")}
<div class="kutu"><p><b>Nereden şüpheleneceğinizi bilmiyorsanız:</b> Sadece sizin dairenizde mi
sorun var, yoksa alt kattaki komşuda ve sokaktaki başka binalarda da aynı şey mi oluyor?
Tek bina etkileniyorsa bina hattındadır. Sokaktaki birden fazla bina birden etkilendiyse
ana şebeke olabilir — o zaman 185.</p></div>
<h3>Hangisine Ulaşmalısınız — Belediye mi, Özel Tıkanıklık Açma Servisi mi?</h3>
{p(f"Bunu açıkça yazalım, çünkü çok vakit kaybettiriyor: <b>belediye, evinizdeki tuvalet "
   f"tıkanıklığı için ekip göndermez.</b> İlçe belediyesinin böyle bir hizmet kalemi yok; "
   f"İSKİ de yalnızca kendi şebekesine bakar. Sifonunuz taşıyor diye 185'i aradığınızda "
   f"kaydınız alınır, ekip gelirse sokaktaki rögara bakar ve sorun sizin hattınızdaysa geri döner.",
   f"Karar aslında tek soruya bakıyor: <b>tıkanıklık sizin mülkünüzün sınırları içinde mi?</b>")}
<div class="tbl"><table>
<thead><tr><th>Durum</th><th>Kimi aramalı?</th></tr></thead>
<tbody>
<tr><td>Lavabo, klozet, banyo gideri, mutfak — tek dairede</td><td><b>Özel servis</b> (biz)</td></tr>
<tr><td>Apartmanın kolonu tıkalı, birden fazla daire etkileniyor</td><td><b>Özel servis</b> (bina yönetimi adına)</td></tr>
<tr><td>Bahçedeki logar/rögar doldu, parsel içinde</td><td><b>Özel servis</b></td></tr>
<tr><td>Sokaktaki rögardan pis su taşıyor</td><td><b>İSKİ — ALO 185</b></td></tr>
<tr><td>Sokakta birden fazla bina aynı anda geri tepiyor</td><td><b>İSKİ — ALO 185</b></td></tr>
<tr><td>Yol üstü yağmur ızgarası tıkalı, su birikiyor</td><td><b>İBB — ALO 153</b></td></tr>
</tbody></table></div>
{p(f"Kısacası: kapınızın içi ve parselinizin içi sizin, sokak kurumun. {loc} yaşanan "
   f"tıkanıklıkların çoğu ilk sütuna düşüyor.",
   f"{ad} dahil İstanbul'un 39 ilçesinde {kucuk(D.ONAYLI['ayni_gun'])} veriyoruz ve "
   f"{D.ONAYLI['varis_kisa']} içinde adresinizde oluyoruz. Emin olamadığınız durumda arayın, "
   f"telefonda birlikte ayırt edelim — gerçekten İSKİ'nin işiyse sizi 185'e yönlendirmekten "
   f"de çekinmiyoruz. Boşuna servis çağırtmanın kimseye faydası yok.")}
"""


# ── İlçeye özel teknik bölüm ────────────────────────────────────────────────
def ilce_ozel(i):
    """39 sayfada birbirine EN AZ benzeyen bölüm — tamamen ilçe verisinden kurulur."""
    ad, loc, gen = i["ad"], ek(i, "loc"), ek(i, "gen")
    return (f'<h2>{e(loc)} Tıkanıklığın En Sık Sebebi Ne?</h2>' + p(
      f"Her ilçede aynı tıkanıklık çıkmıyor. {ad} tarafında baskın yapı stoğu "
      f"{i['yapi']}; bu da pis su hattının karakterini belirliyor: {i['hat']}.",
      f"Bunun pratikteki karşılığı şu: {loc} en sık karşılaştığımız sebep "
      f"<b>{kucuk(i['risk'])}</b>. Aynı arıza tarifiyle başka bir ilçeye gittiğimizde "
      f"sebep çoğu zaman bambaşka çıkıyor — bu yüzden telefonda adresi öğrenmek bizim "
      f"için sadece yol tarifi değil, teşhisin bir parçası.",
      f"Saha tarafında dikkat ettiğimiz nokta ise erişim: {i['erisim']}."))

# ── H2 seçimi ───────────────────────────────────────────────────────────────
# Her ilçe, slug'ından hesaplanan SABİT kaydırmayla farklı kombinasyon alır.
SIRA = ["usta", "numara", "yakin", "mutfak", "lavabo", "tuvalet", "banyo", "gider", "yontem"]

def ilce_h2_seti(i):
    """[(başlık, gövde_anahtarı), ...] döndürür."""
    s = i["slug"]
    out = []
    for slot in SIRA:
        havuz = D.H2_HAVUZ[slot]
        out.append(havuz[tohum(s, slot) % len(havuz)])
    return out

def h2_yaz(kalip, i):
    return (kalip.replace("{ad}", i["ad"])
                 .replace("{loc}", ek(i, "loc"))
                 .replace("{dat}", ek(i, "dat"))
                 .replace("{gen}", ek(i, "gen"))
                 .replace("{abl}", ek(i, "abl")))

def govde_uret(anahtar, i):
    return G(anahtar, i) or G2(anahtar, i)

# ── İç link ağı ─────────────────────────────────────────────────────────────
def ana_anchor(i):
    """⚠️ 39 sayfada tek tip tam eşleşme anchor aşırı optimizasyon sinyali olurdu."""
    return sec(D.ANA_ANCHOR, i["slug"], "ana")

def komsu_agi(i):
    """Örümcek ağı: her ilçe komşularına + rotasyonla uzak ilçelere bağlanır."""
    ks = list(KOMSU.get(i["slug"], []))
    hepsi = [x["slug"] for x in D.ILCELER if x["slug"] != i["slug"] and x["slug"] not in ks]
    b = tohum(i["slug"], "uzak")
    uzak = [hepsi[(b + n * 7) % len(hepsi)] for n in range(4)]
    secim, gorulen = [], set()
    for s in ks + uzak:
        if s not in gorulen:
            gorulen.add(s); secim.append(s)
    kalip = ["{ad} tıkanıklık açma", "{loc} gider açma", "{ad} tıkanıklık açma servisi",
             "{loc} tıkalı gider açma", "{ad} gider açma ustası"]
    ogeler = []
    for n, s in enumerate(secim[:8]):
        k = ILCE[s]
        metin = h2_yaz(kalip[(tohum(i["slug"], "k%d" % n)) % len(kalip)], k)
        ogeler.append(f'<li><a class="cip" href="{ic(ilce_yolu(k))}">{e(metin)}</a></li>')
    gen_, loc_ = ek(i, "gen"), ek(i, "loc")
    giris = p(f"Ekibimiz {loc_} çalışırken komşu ilçelerdeki işleri de aynı güzergâhta "
              f"planlıyor. Aşağıdaki ilçelerde de aynı hizmeti veriyoruz:")
    return (f'<h2>{e(gen_)} Çevresinde Hizmet Verdiğimiz İlçeler</h2>{giris}'
            f'<ul class="cipler">{"".join(ogeler)}</ul>')

def hizmet_agi(i):
    """İlçe sayfasından hizmet sayfalarına bağlantı."""
    ogeler = []
    for h in D.HIZMETLER:
        ogeler.append(f'<li><a class="cip" href="{ic(hizmet_yolu(h))}">'
                      f'{e(h["ad"])}</a></li>')
    loc_ = ek(i, "loc")
    return (f'<h2>{e(loc_)} Verdiğimiz Tüm Hizmetler</h2>'
            f'<ul class="cipler">{"".join(ogeler)}</ul>')


# ── Şema ────────────────────────────────────────────────────────────────────
def isletme_semasi(ilce=None):
    """⚠️ aggregateRating YOK — teyit edilmemiş puan/yorum sayısı yazılmaz."""
    n = {
      "@context": "https://schema.org",
      "@type": "Plumber",
      "@id": ALAN + "/#isletme",
      "name": S["marka"],
      "url": ALAN + "/",
      "telephone": S["tel_link"],
      "email": S["eposta"],
      "address": {"@type": "PostalAddress",
                  "streetAddress": S["adres_sokak"],
                  "addressLocality": S["adres_ilce"],
                  "addressRegion": S["adres_il"],
                  "postalCode": S["posta_kodu"],
                  "addressCountry": "TR"},
      "geo": {"@type": "GeoCoordinates", "latitude": S["enlem"], "longitude": S["boylam"]},
      "openingHoursSpecification": [{
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
          "opens": "00:00", "closes": "23:59"}],
      "areaServed": ([{"@type": "AdministrativeArea", "name": ilce["ad"] + ", İstanbul"}]
                     if ilce else
                     [{"@type": "AdministrativeArea", "name": x["ad"] + ", İstanbul"}
                      for x in D.ILCELER]),
      "makesOffer": [{"@type": "Offer", "itemOffered":
                      {"@type": "Service", "name": h["ad"], "url": ALAN + "/" + hizmet_yolu(h)}}
                     for h in D.HIZMETLER],
    }
    return ldj_yaz(n)

def sss_semasi(sorular):
    return ldj_yaz({"@context": "https://schema.org", "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": s,
        "acceptedAnswer": {"@type": "Answer", "text": c}} for s, c in sorular]})

def hizmet_semasi(h, ilce=None):
    return ldj_yaz({"@context": "https://schema.org", "@type": "Service",
      "serviceType": h["ad"], "name": h["ad"],
      "description": h["ozet"],
      "provider": {"@id": ALAN + "/#isletme"},
      "areaServed": {"@type": "City", "name": "İstanbul"},
      "url": ALAN + "/" + (ilce_yolu(ilce) if ilce else hizmet_yolu(h))})

# ── Ortak bölümler ──────────────────────────────────────────────────────────
def b_ust(etiket, baslik, vurgu="", alt=""):
    v = f' <span class="v">{e(vurgu)}</span>' if vurgu else ""
    a = f"<p>{e(alt)}</p>" if alt else ""
    return (f'<div class="b-ust"><span class="b-etiket">{e(etiket)}</span>'
            f'<h2>{e(baslik)}{v}</h2>{a}</div>')

def cta_band(baslik, metin):
    return (f'<section class="bolum"><div class="kap"><div class="cta">'
            f'<h2>{e(baslik)}</h2><p>{e(metin)}</p>'
            f'<div class="cta-dg">{tel_btn(S["tel_goster"], "dg dg-altin")}'
            f'{wa_btn()}</div></div></div></section>')

def sss_bolum(sorular, baslik="Sık Sorulan Sorular"):
    ogeler = "".join(
      f'<details><summary>{e(s)}</summary><div class="cvp"><p>{c}</p></div></details>'
      for s, c in sorular)
    return (f'<section class="bolum bolum-ac"><div class="kap">'
            f'{b_ust("Merak Edilenler", baslik)}'
            f'<div class="sss">{ogeler}</div></div></section>')

def blok_yaz(bloklar):
    """data.py'deki ('h2'|'h3'|'p'|'ul'|'kutu'|'uyari', içerik) listesini HTML'e çevirir."""
    out = []
    for tip, ic_ in bloklar:
        if tip in ("h2", "h3"):
            out.append(f"<{tip}>{ic_}</{tip}>")
        elif tip == "p":
            out.append(f"<p>{ic_}</p>")
        elif tip == "ul":
            li = "".join(f"<li><b>{a}:</b> {b}</li>" for a, b in ic_)
            out.append(f"<ul>{li}</ul>")
        elif tip == "kutu":
            out.append(f'<div class="kutu"><p>{ic_}</p></div>')
        elif tip == "uyari":
            out.append(f'<div class="kutu kutu-uyari"><p>{ic_}</p></div>')
    return "".join(out)


# ── İlçe sayfası ────────────────────────────────────────────────────────────
def ilce_sss(i):
    ad, loc, dat = i["ad"], ek(i, "loc"), ek(i, "dat")
    return [
      (f"{ad} tıkanıklık açma için ne kadar sürede gelirsiniz?",
       f"{D.ONAYLI['varis']} hedefliyoruz; {dat} de aynı şekilde. Ekip yola çıkmadan önce "
       f"telefonda birkaç soru sorup doğru makineyle gelmesini sağlıyoruz — yanlış ekipmanla "
       f"erken gelmenin bir faydası olmuyor."),
      (f"{loc} gece ve hafta sonu çalışıyor musunuz?",
       f"Evet, 7/24. Su taşması, geri tepme ve koku gibi bekleyemeyecek durumlarda saat "
       f"fark etmeksizin {S['tel_goster']} numarasından arayabilirsiniz."),
      (f"{loc} fayans veya seramik kırıyor musunuz?",
       f"Hayır. Çalışma mevcut giriş noktalarından yapılıyor. Kırma yalnızca boruda çökme "
       f"ya da kırık varsa gündeme gelir; o durumda da kamerayla tam noktayı gösterip "
       f"onayınızı almadan hiçbir yere dokunmuyoruz."),
      (f"{ad} tıkanıklık açma için belediye veya İSKİ gelir mi?",
       f"Daire içi ve bina içi tıkanıklığa gelmez. İSKİ yalnızca sokaktaki ana kanalizasyon "
       f"şebekesinden sorumlu; ana hatta arıza varsa ALO 185'i arayabilirsiniz. Parselinizin "
       f"içindeki hat ise mülk sahibinin sorumluluğunda, o iş özel tesisatçının işi."),
      (f"{loc} tıkanıklığın daire içinde mi binada mı olduğunu nasıl anlarım?",
       f"Tek bir gider mi etkilendi, yoksa evdeki birkaç gider aynı anda mı yavaşladı? "
       f"Tek nokta ise sorun o giderin kendi hattında. Birden fazla gider birlikte taşıyorsa "
       f"ya da alt kattaki komşuda da aynı sorun varsa bina kolonundan şüphelenmek gerekir."),
    ]

def ilce_sayfasi(i):
    ad, loc, gen, dat = i["ad"], ek(i, "loc"), ek(i, "gen"), ek(i, "dat")
    baslik = f"{ad} Tıkanıklık Açma ve Gider Açma | 7/24 {S['marka']}"
    aciklama = (f"{loc} tıkanıklık açma ve gider açma. Kırmadan, kameralı tespitle; "
                f"lavabo, klozet, mutfak ve ana gider. 7/24 {S['tel_goster']}.")
    sorular = ilce_sss(i)

    # Gövde: 9 rotasyonlu H2 + ilçeye özel + belediye + ağlar + kapanış
    govde = []
    for kalip, anahtar in ilce_h2_seti(i):
        govde.append(f"<h2>{e(h2_yaz(kalip, i))}</h2>" + govde_uret(anahtar, i))
    govde.append(ilce_ozel(i))
    govde.append(belediye_bolum(i))
    govde.append(hizmet_agi(i))
    govde.append(komsu_agi(i))
    kap_kalip, _ = sec(D.H2_KAPANIS, i["slug"], "kapanis")
    govde.append(f"<h2>{e(h2_yaz(kap_kalip, i))}</h2>" + govde_uret("kapanis", i))
    govde.append(p(f'Daha fazlası için <a href="{ic()}">{e(ana_anchor(i))}</a> sayfamıza '
                   f'göz atabilir, ev yöntemlerini merak ediyorsanız '
                   f'<a href="{ic("lavabo-acma-yontemleri/")}">lavabo ve gider açma '
                   f'yöntemleri</a> rehberimizi okuyabilirsiniz.'))

    depo_basligi = S["adres_ilce"] + " deposu"
    yan = (
      '<aside class="yan">'
      f'<div class="yan-kutu"><h3>{e(ad)} için hemen arayın</h3>'
      f'<p style="color:var(--gri);font-size:.95rem">{e(D.ONAYLI["ayni_gun"])}. '
      f'{e(D.ONAYLI["varis"])}.</p>'
      f'<div style="display:grid;gap:10px">{tel_btn(S["tel_goster"])}{wa_btn()}</div></div>'
      '<div class="yan-kutu"><h3>Hizmetlerimiz</h3><ul class="yan-liste">'
      + "".join(f'<li><a href="{ic(hizmet_yolu(h))}">{e(h["ad"])}</a></li>'
                for h in D.HIZMETLER[:8])
      + f'<li><a href="{ic("hizmetler/")}"><b>Tümü →</b></a></li></ul></div>'
      f'<div class="yan-kutu"><h3>Konumumuz</h3>{harita(depo_basligi)}</div>'
      '</aside>')

    hero_g, hero_sinif = hero_sag(f"{ad} tıkanıklık açma ekibi çalışırken", kart=False)
    return (
      head(baslik, aciklama, ilce_yolu(i),
           isletme_semasi(i) + sss_semasi(sorular) + hizmet_semasi(HIZMET["tikaniklik-acma"], i))
      + ust_header("bolgeler")
      + kirinti([("Hizmet Bölgeleri", "bolgeler/"), (f"{ad} Tıkanıklık Açma", None)])
      + f"""
<section class="hero"><div class="kap"><div class="hero-izgara{hero_sinif}">
<div>
<span class="rozet"><span class="nokta"></span>{e(S["saat"])}</span>
<h1>{e(ad)} Tıkanıklık Açma<br><span class="v">ve Gider Açma</span></h1>
<p class="hero-alt">{e(D.ONAYLI["yontem"])} tıkalı giderlerinizi açıyoruz.
{e(D.ONAYLI["ayni_gun"])} veriyor, {e(D.ONAYLI["varis_kisa"])} içinde {e(dat)} ulaşıyoruz.</p>
<div class="hero-dg">{tel_btn(S["tel_goster"], "dg dg-altin")}{wa_btn()}</div>
<div class="hero-ist">
<div class="ist-k"><b>7/24</b><span>Acil Servis</span></div>
<div class="ist-k"><b>39</b><span>İlçe</span></div>
<div class="ist-k"><b>Kameralı</b><span>Tespit</span></div>
</div>
</div>
{hero_g}
</div></div></section>
<main id="ana"><section class="bolum"><div class="kap"><div class="yan-izgara">
<article class="govde">{"".join(govde)}</article>
{yan}
</div></div></section>
{video_bolum("ilce")}
{sss_bolum(sorular, f"{ad} Tıkanıklık Açma — Sık Sorulan Sorular")}
{cta_band(f"{ad} tıkanıklık açma için bekleyen bir işiniz mi var?",
          "Telefonda durumu birlikte değerlendirelim, ekip doğru ekipmanla yola çıksın.")}
</main>
""" + alt_bilgi())


# ── Hizmet sayfası ──────────────────────────────────────────────────────────
def hizmet_ilce_agi(h):
    """Hizmet sayfasından 39 ilçeye ağ — örümcek ağının ikinci yönü."""
    kalip = ["{ad} tıkanıklık açma", "{loc} gider açma", "{ad} gider açma",
             "{loc} tıkanıklık açma servisi"]
    ogeler = []
    for n, i in enumerate(D.ILCELER):
        metin = h2_yaz(kalip[tohum(h["slug"], "i%d" % n) % len(kalip)], i)
        ogeler.append(f'<li><a class="cip" href="{ic(ilce_yolu(i))}">{e(metin)}</a></li>')
    return (f'<h2>{e(h["ad"])} Hizmeti Verdiğimiz İstanbul İlçeleri</h2>'
            + p(f"{e(h['ad'])} hizmetini İstanbul'un 39 ilçesinin tamamında veriyoruz. "
                f"{D.ONAYLI['ayni_gun']}, {D.ONAYLI['varis_kisa']} içinde adreste oluyoruz.")
            + f'<ul class="cipler">{"".join(ogeler)}</ul>')

def hizmet_sss(h):
    return [
      (f"{h['ad']} için fayans kırmak gerekir mi?",
       "Normal şartlarda hayır. Çalışma mevcut giriş noktalarından yapılıyor. Kırma yalnızca "
       "boruda çökme ya da kırık varsa gündeme gelir; o durumda da kamerayla tam noktayı "
       "gösterip onayınızı alıyoruz."),
      (f"{h['ad']} hizmetini hangi saatlerde veriyorsunuz?",
       f"7/24. {D.ONAYLI['ayni_gun']} veriyoruz; gece ve hafta sonu dahil "
       f"{S['tel_goster']} numarasından ulaşabilirsiniz."),
      ("Kimyasal kullanıyor musunuz?",
       "Tıkanıklığı açmak için kullanmıyoruz. Market çözücüleri tıkacı çoğu zaman geçici "
       "olarak deler, asıl kütle yerinde kalır ve boruya zarar verir. Biz mekanik yöntemle "
       "— robot makine ve basınçlı su — çalışıyoruz."),
      ("İstanbul'un hangi ilçelerine geliyorsunuz?",
       "39 ilçenin tamamına. Ekiplerimiz iki yakada dağınık çalışıyor; size en yakın "
       "müsait ekip yönlendiriliyor."),
    ]

def yan_hizmet_ogesi(x, aktif):
    gec = ' aria-current="page"' if x["slug"] == aktif["slug"] else ""
    return f'<li><a href="{ic(hizmet_yolu(x))}"{gec}>{e(x["ad"])}</a></li>'

def hizmet_sayfasi(h):
    baslik = f"{h['ad']} | İstanbul 7/24 {S['marka']}"
    aciklama = h["ozet"] + f" İstanbul'un 39 ilçesinde 7/24. {S['tel_goster']}."
    sorular = hizmet_sss(h)
    govde = []
    govde.append(f"<h2>İstanbul'da {e(h['ad'])}</h2>" + p(
      f"{e(h['ozet'])} {D.ONAYLI['yontem']} çalışıyoruz; "
      f"{kucuk(D.ONAYLI['ayni_gun'])} veriyor, {D.ONAYLI['varis_kisa']} içinde adreste oluyoruz.",
      "Tıkanıklığı delip geçmek yerine tıkayan kütleyi hattan çıkarıyoruz. Aradaki fark şu: "
      "birincisinde su o gün akar ama kısa sürede geri kapanır, ikincisinde aynı yerden "
      "tekrar aramazsınız."))
    if h["es"]:
        govde.append(p("Bu hizmet şu adlarla da aranıyor: "
                       + ", ".join(f"<b>{e(x)}</b>" for x in h["es"]) + "."))
    if h["slug"] in D.HIZMET_GOVDE:
        govde.append(blok_yaz(D.HIZMET_GOVDE[h["slug"]]))
    govde.append(hizmet_ilce_agi(h))
    digerleri = [x for x in D.HIZMETLER if x["slug"] != h["slug"]][:8]
    govde.append('<h2>Diğer Hizmetlerimiz</h2><ul class="cipler">'
      + "".join(f'<li><a class="cip" href="{ic(hizmet_yolu(x))}">{e(x["ad"])}</a></li>'
                for x in digerleri) + "</ul>")
    govde.append(p(f'Ev yöntemlerini denemeyi düşünüyorsanız önce '
                   f'<a href="{ic("lavabo-acma-yontemleri/")}">hangi yöntem gerçekten işe '
                   f'yarıyor</a> yazımıza bakın — bazıları zaman kaybı, bazıları zararlı.'))

    yan = ('<aside class="yan">'
      f'<div class="yan-kutu"><h3>{e(h["ad"])} için arayın</h3>'
      f'<div style="display:grid;gap:10px">{tel_btn(S["tel_goster"])}{wa_btn()}</div></div>'
      '<div class="yan-kutu"><h3>Tüm Hizmetler</h3><ul class="yan-liste">'
      + "".join(yan_hizmet_ogesi(x, h) for x in D.HIZMETLER)
      + '</ul></div></aside>')

    hero_g, hero_sinif = hero_sag(h["ad"] + " çalışması", kart=False)
    return (head(baslik, aciklama, hizmet_yolu(h),
                 isletme_semasi() + hizmet_semasi(h) + sss_semasi(sorular))
      + ust_header()
      + kirinti([("Hizmetler", "hizmetler/"), (h["ad"], None)])
      + f"""
<section class="hero"><div class="kap"><div class="hero-izgara{hero_sinif}">
<div>
<span class="rozet"><span class="nokta"></span>{e(S["saat"])}</span>
<h1>{e(h["ad"])}<br><span class="v">İstanbul 7/24</span></h1>
<p class="hero-alt">{e(h["ozet"])}</p>
<div class="hero-dg">{tel_btn(S["tel_goster"], "dg dg-altin")}{wa_btn()}</div>
</div>
{hero_g}
</div></div></section>
<main id="ana"><section class="bolum"><div class="kap"><div class="yan-izgara">
<article class="govde">{"".join(govde)}</article>
{yan}
</div></div></section>
{video_bolum(h["slug"])}
{sss_bolum(sorular, e(h["ad"]) + " — Sık Sorulan Sorular")}
{cta_band(f"{h['ad']} için hemen destek alın",
          "Telefonda durumu birlikte değerlendirelim, ekip doğru ekipmanla yola çıksın.")}
</main>
""" + alt_bilgi())


# ── Rehber sayfası ──────────────────────────────────────────────────────────
def rehber_sayfasi(r):
    sorular = [
      ("Bulaşık tableti lavabo açar mı?",
       "Yavaşlamış bir mutfak giderinde çeperdeki taze yağ filmine bir miktar etki edebilir. "
       "Yıllardır birikmiş, sertleşmiş kütleye hiçbir şey yapmaz. Tableti kuru atmayın, "
       "sıcak suda eritin."),
      ("Limon tuzu ya da kaya tuzu lavabo açar mı?",
       "Hayır. Limon tuzu kireç çözer; lavabo tıkanıklığı ise saç, sabun ve yağdan oluşan "
       "organik bir kütledir. Kaya tuzunun ise hiçbir çözücü etkisi yoktur."),
      ("Tuz ruhu veya kostik kullanmak zararlı mı?",
       "Evet. Tuz ruhu boruyu ve contaları aşındırır; çamaşır suyuyla temas ederse klor gazı "
       "açığa çıkarır. Kostik suyla tepkimeye girerken ısınır ve dar giderde geri püskürüp "
       "ciddi yanıklara yol açabilir. Gider açmak için kullanılacak maddeler değildir."),
      ("Lavabo açma aparatı (susta) işe yarar mı?",
       "Mekanik olduğu için listedeki yöntemler arasında gerçekten şansı olan tek yöntem. "
       "Giderin ilk dirseğindeki saç kütlesini çıkarabilir. Ama zorlayarak itmeyin — ucu "
       "boruyu çizebilir, koparsa içeride kalır."),
      ("Ne zaman usta çağırmalıyım?",
       "Su hiç gitmiyorsa, birden fazla gider aynı anda yavaşladıysa, alt kattaki komşuda da "
       "aynı sorun varsa, ya da aynı gider kısa aralıklarla tekrar tıkanıyorsa. Bu durumlarda "
       "ev yöntemleri vakit kaybıdır."),
    ]
    return (head(r["baslik"] + f" | {S['marka']}", r["ozet"], r["slug"] + "/",
                 isletme_semasi() + sss_semasi(sorular))
      + ust_header()
      + kirinti([(r["ad"], None)])
      + f"""
<main id="ana">
<section class="bolum"><div class="kap">
<div class="b-ust"><span class="b-etiket">Rehber</span><h1>{e(r["baslik"])}</h1>
<p>{e(r["ozet"])}</p></div>
<div class="yan-izgara">
<article class="govde">{blok_yaz(r["blok"])}
{p(f'Denediniz ve olmadıysa ya da yukarıdaki uyarı işaretlerinden biri varsa, '
   f'<a href="{ic("tikaniklik-acma/")}">tıkanıklık açma</a> ve '
   f'<a href="{ic("gider-acma/")}">gider açma</a> hizmetimizle İstanbul un 39 ilçesinde '
   f'7/24 yanınızdayız.')}
</article>
<aside class="yan"><div class="yan-kutu"><h3>Kendiniz açamadıysanız</h3>
<p style="color:var(--gri);font-size:.95rem">{e(D.ONAYLI["ayni_gun"])}. {e(D.ONAYLI["varis"])}.</p>
<div style="display:grid;gap:10px">{tel_btn(S["tel_goster"])}{wa_btn()}</div></div>
<div class="yan-kutu"><h3>İlgili Hizmetler</h3><ul class="yan-liste">"""
      + "".join(f'<li><a href="{ic(hizmet_yolu(HIZMET[x]))}">{e(HIZMET[x]["ad"])}</a></li>'
                for x in ["lavabo-tikanikligi-acma", "tuvalet-tikanikligi-acma",
                          "banyo-gideri-tikanikligi-acma", "mutfak-gideri-tikanikligi-acma",
                          "kirmadan-tikaniklik-acma", "robotla-tikaniklik-acma"])
      + f"""</ul></div></aside>
</div></div></section>
{sss_bolum(sorular)}
{cta_band("Denediniz, açılmadı mı?", "Zorlamayın — yanlış müdahale çoğu zaman asıl işten daha pahalıya mal oluyor.")}
</main>
""" + alt_bilgi())

# ── Anasayfa ────────────────────────────────────────────────────────────────
def anasayfa():
    hero_g, hero_sinif = hero_sag("Tıkanıklık açma servisi ekibi çalışırken")
    hizmet_kartlari = "".join(
      f'<a class="kart" href="{ic(hizmet_yolu(h))}">'
      f'<span class="ikon-yv">{svg(h["ikon"])}</span>'
      f'<h3>{e(h["ad"])}</h3><p>{e(h["ozet"])}</p>'
      f'<span class="devam">Detaylı bilgi</span></a>'
      for h in D.HIZMETLER)

    ilce_cipleri = "".join(
      f'<li><a class="cip" href="{ic(ilce_yolu(i))}">{e(i["ad"])}</a></li>'
      for i in sorted(D.ILCELER, key=lambda x: kucuk(x["ad"])))

    sorular = D.SSS_GENEL
    return (head(
        f"{S['marka']} | İstanbul Tıkanıklık Açma ve Gider Açma — 7/24",
        f"İstanbul'un 39 ilçesinde 7/24 tıkanıklık açma ve gider açma. Kırmadan, kameralı "
        f"tespitle. {D.ONAYLI['varis']}. {S['tel_goster']}.",
        "", isletme_semasi() + sss_semasi(sorular))
      + ust_header("anasayfa")
      + f"""
<section class="hero"><div class="kap"><div class="hero-izgara{hero_sinif}">
<div>
<span class="rozet"><span class="nokta"></span>{e(S["saat"])}</span>
<h1>İstanbul'da Tıkanıklık Açma<br><span class="v">ve Gider Açma</span></h1>
<p class="hero-alt">{e(D.ONAYLI["yontem"])} tıkalı giderlerinizi açıyoruz.
{e(D.ONAYLI["ayni_gun"])} veriyor, {e(D.ONAYLI["varis_kisa"])} içinde adresinizde oluyoruz.</p>
<div class="hero-dg">{tel_btn(S["tel_goster"], "dg dg-altin")}{wa_btn()}
<a class="dg dg-cizgi" href="{ic("hizmetler/")}">Hizmetlerimiz</a></div>
<div class="hero-ist">
<div class="ist-k"><b>7/24</b><span>Acil Servis</span></div>
<div class="ist-k"><b>39</b><span>İlçe</span></div>
<div class="ist-k"><b>Kameralı</b><span>Tespit</span></div>
</div>
</div>
{hero_g}
</div></div></section>
<main id="ana">
<section class="bolum"><div class="kap">
{b_ust("Uzmanlık Alanlarımız", "Profesyonel", "Hizmetlerimiz",
       "Tıkanıklık açma, gider açma ve kameralı tespit hizmetlerimiz.")}
<div class="izgara iz-3">{hizmet_kartlari}</div>
</div></section>
{video_bolum("")}
<section class="bolum bolum-ac"><div class="kap">
{b_ust("Servis Ağımız", "Hizmet", "Bölgelerimiz",
       "İstanbul'un 39 ilçesinin tamamında aynı gün hizmet veriyoruz.")}
<div class="cip-grup"><h3>İstanbul <small>39 ilçe</small></h3>
<ul class="cipler">{ilce_cipleri}</ul></div>
</div></section>
<section class="bolum"><div class="kap"><div class="yan-izgara">
<article class="govde">
<h2>İstanbul'da Tıkanıklık Açma ve Gider Açma</h2>
{p(f"{S['marka']} olarak İstanbul'un 39 ilçesinde tıkanıklık açma ve gider açma hizmeti "
   f"veriyoruz. Lavabo, klozet, banyo gideri, mutfak pimaşı, bina ana kolonu, logar ve "
   f"bahçe hattı — hepsinde aynı ekip ve aynı ekipmanla çalışıyoruz.",
   "Çalışma biçimimiz tek cümleyle şu: tıkacı delip geçmek yerine hattan çıkarmak. Aradaki "
   "fark, aynı yerden iki hafta sonra tekrar aranıp aranmamak.",
   f"{D.ONAYLI['ayni_gun']} veriyoruz. Gerektiğinde fiber optik kamerayla hattın içine bakıp "
   f"tıkanıklığın kaç metre ileride olduğunu ve neden oluştuğunu birlikte görüyoruz — "
   f"özellikle aynı gider tekrar tekrar tıkanıyorsa bu adım işin tamamını değiştiriyor.")}
<h2>Kırmadan Çalışıyoruz</h2>
{p("En sık gelen soru bu. Normal şartlarda fayans, seramik ya da duvar kırmak gerekmiyor; "
   "çalışmanın tamamı mevcut giriş noktalarından yapılıyor: gider ağzı, yer süzgeci, klozet "
   "çıkışı, temizleme kapağı ya da rögar.",
   "Kırma yalnızca boruda çökme veya kırık varsa gündeme geliyor. O durumda da önce kamerayla "
   "tam noktayı gösteriyor, ne yapılacağını anlatıyor ve onayınızı almadan hiçbir yere "
   "dokunmuyoruz.")}
<h2>Tıkanıklık Daire İçinde mi, Binada mı?</h2>
{p("Bu ayrım işin en önemli kısmı, çünkü yanlış yerden başlamak hem zaman hem para kaybı. "
   "Pratik kontrol şu: tek bir gider mi etkilendi, yoksa evdeki birkaç gider aynı anda mı "
   "yavaşladı? Tek nokta ise sorun o giderin kendi hattında. Birden fazla gider birlikte "
   "taşıyorsa ya da alt kattaki komşuda da aynı sorun varsa bina kolonundan şüphelenmek gerekir.",
   "Emin değilseniz telefonda birkaç soruyla birlikte ayırt ediyoruz. Belediye ve İSKİ’nin "
   "bu işteki sorumluluğunu, hangi durumda kimin arandığını ilçe sayfalarımızda tablo "
   "hâlinde anlattık.")}
{p(f'Ev yöntemlerini denemeyi düşünüyorsanız, hangisinin gerçekten işe yaradığını '
   f'<a href="{ic("lavabo-acma-yontemleri/")}">lavabo ve gider açma yöntemleri</a> '
   f'rehberimizde tesisatçı gözünden yazdık.')}
</article>
<aside class="yan">
<div class="yan-kutu"><h3>Hemen arayın</h3>
<p style="color:var(--gri);font-size:.95rem">{e(D.ONAYLI["varis"])}. 7/24 açığız.</p>
<div style="display:grid;gap:10px">{tel_btn(S["tel_goster"])}{wa_btn()}</div></div>
<div class="yan-kutu"><h3>Konumumuz</h3>{harita(S["adres_ilce"] + " deposu")}</div>
</aside>
</div></div></section>
{sss_bolum(sorular)}
{cta_band("Tıkanıklık beklemez", "Telefonda durumu birlikte değerlendirelim, ekip doğru ekipmanla yola çıksın.")}
</main>
""" + alt_bilgi())


# ── Liste ve kurumsal sayfalar ──────────────────────────────────────────────
def basit_sayfa(baslik, aciklama, yol, h1, giris, govde, kirinti_ad=None, sema=""):
    return (head(f"{baslik} | {S['marka']}", aciklama, yol, isletme_semasi() + sema)
      + ust_header()
      + kirinti([(kirinti_ad or baslik, None)])
      + f"""
<main id="ana"><section class="bolum"><div class="kap">
<div class="b-ust"><span class="b-etiket">{e(kirinti_ad or baslik)}</span><h1>{e(h1)}</h1>
<p>{e(giris)}</p></div>
{govde}
</div></section>
{cta_band("Tıkanıklık beklemez", "Telefonda durumu birlikte değerlendirelim.")}
</main>
""" + alt_bilgi())

def bolgeler_sayfasi():
    cip = "".join(f'<li><a class="cip" href="{ic(ilce_yolu(i))}">{e(i["ad"])}</a></li>'
                  for i in sorted(D.ILCELER, key=lambda x: kucuk(x["ad"])))
    av = [i for i in D.ILCELER if i["yaka"] == "Avrupa"]
    an = [i for i in D.ILCELER if i["yaka"] == "Anadolu"]
    def grup(ad, liste):
        c = "".join(f'<li><a class="cip" href="{ic(ilce_yolu(i))}">{e(i["ad"])}</a></li>'
                    for i in sorted(liste, key=lambda x: kucuk(x["ad"])))
        return (f'<div class="cip-grup"><h3>{e(ad)} <small>{len(liste)} ilçe</small></h3>'
                f'<ul class="cipler">{c}</ul></div>')
    govde = ('<div class="govde" style="max-width:none">'
             + grup("İstanbul — Avrupa Yakası", av) + grup("İstanbul — Anadolu Yakası", an)
             + p(f"Her ilçe sayfasında o ilçeye özgü yapı stoğunu, hattın karakterini ve en sık "
                 f"karşılaştığımız tıkanıklık sebebini anlattık. Ayrıca belediye ve İSKİ'nin "
                 f"sorumluluk sınırını, hangi durumda kimin aranacağını tablo hâlinde koyduk.")
             + "</div>")
    return basit_sayfa("Hizmet Bölgeleri",
      f"İstanbul'un 39 ilçesinde tıkanıklık açma ve gider açma. {D.ONAYLI['varis']}.",
      "bolgeler/", "Hizmet Bölgelerimiz",
      "İstanbul'un 39 ilçesinin tamamında aynı gün hizmet veriyoruz.", govde)

def hizmetler_sayfasi():
    kartlar = "".join(
      f'<a class="kart" href="{ic(hizmet_yolu(h))}">'
      f'<span class="ikon-yv">{svg(h["ikon"])}</span>'
      f'<h3>{e(h["ad"])}</h3><p>{e(h["ozet"])}</p>'
      f'<span class="devam">Detaylı bilgi</span></a>' for h in D.HIZMETLER)
    return basit_sayfa("Hizmetlerimiz",
      "Tıkanıklık açma, gider açma, kameralı tespit, pimaş yıkama ve kanalizasyon açma "
      "hizmetlerimiz. İstanbul'un 39 ilçesinde 7/24.",
      "hizmetler/", "Profesyonel Hizmetlerimiz",
      "Tıkanıklık açma ve gider açma hizmetlerimiz kategorilere ayrılmış şekilde listelenmiştir.",
      f'<div class="izgara iz-3">{kartlar}</div>')

def hakkimizda_sayfasi():
    govde = '<div class="govde">' + "".join([
      "<h2>Biz Kimiz?</h2>",
      p(f"{S['marka']} olarak İstanbul'da tıkanıklık açma ve gider açma işi yapıyoruz. "
        f"Merkezimiz {ek('esenler', 'loc')}; ekiplerimiz iki yakada dağınık çalışıyor ve "
        f"{kucuk(D.ONAYLI['ayni_gun'])} veriyoruz.",
        "İşimiz dar bir alanda uzmanlaşmak üzerine kurulu: tıkanıklık ve gider. Lavabo, "
        "klozet, banyo gideri, mutfak pimaşı, bina ana kolonu, logar ve bahçe hattı."),
      "<h2>Nasıl Çalışıyoruz?</h2>",
      p("Önce dinliyoruz. Hangi giderler etkilendi, ne zaman başladı, daha önce ne denendi — "
        "bu üç sorunun cevabı ekibin hangi makineyle geleceğini belirliyor.",
        "Sonra teşhis: gerekiyorsa fiber optik kamerayla hattın içine bakıyoruz. Tıkanıklığın "
        "kaç metre ileride olduğunu ve neden oluştuğunu ekranda birlikte görüyoruz.",
        "Sonra müdahale: robot makine ve basınçlı su. Tıkacı delip geçmiyor, hattan "
        "çıkarıyoruz. Bitince hattı su vererek test ediyoruz."),
      "<h2>Neyi Yapmıyoruz?</h2>",
      p("Tıkanıklık açmak için kimyasal kullanmıyoruz. Market çözücüleri tıkacın ortasında "
        "kanal açar, asıl kütle yerinde kalır; üstelik eski döküm ve PVC boruların iç "
        "yüzeyine zarar verir.",
        "Gereksiz kırım yapmıyoruz. Kırma yalnızca boruda çökme ya da kırık varsa gündeme "
        "gelir ve o durumda da önce kamerayla noktayı gösterip onayınızı alıyoruz."),
      "<h2>İletişim</h2>",
      p(f"<b>Adres:</b> {e(S['adres'])}<br>"
        f"<b>Telefon:</b> {tel_vurgu()}<br>"
        f"<b>E-posta:</b> <a href=\"mailto:{S['eposta']}\">{e(S['eposta'])}</a><br>"
        f"<b>Çalışma saatleri:</b> {e(S['saat'])}"),
      harita(S["adres_ilce"] + " deposu"),
    ]) + "</div>"
    return basit_sayfa("Hakkımızda",
      f"{S['marka']} — İstanbul'da tıkanıklık açma ve gider açma. Kırmadan, kameralı "
      f"tespitle, 7/24.", "hakkimizda/", f"{S['marka']} Hakkında",
      "Dar bir alanda uzmanlaşmayı seçtik: tıkanıklık ve gider.", govde)

def iletisim_sayfasi():
    govde = ('<div class="govde">'
      + p(f"Tıkanıklık saat gözetmiyor; biz de gözetmiyoruz. Günün her saati "
          f"{tel_vurgu()} numarasından ulaşabilirsiniz.",
          "Aradığınızda size üç şey soracağız: hangi gider tıkalı, evdeki başka giderler de "
          "yavaşladı mı, alt kattaki komşuda aynı sorun var mı. Bu üç cevap ekibin doğru "
          "makineyle gelmesini sağlıyor.")
      + f'<div class="hero-dg">{tel_btn(S["tel_goster"], "dg dg-koyu")}{wa_btn()}</div>'
      + "<h2>İletişim Bilgileri</h2>"
      + p(f"<b>Adres:</b> {e(S['adres'])}<br>"
          f"<b>Telefon:</b> {tel_vurgu()}<br>"
          f"<b>E-posta:</b> <a href=\"mailto:{S['eposta']}\">{e(S['eposta'])}</a><br>"
          f"<b>Çalışma saatleri:</b> {e(S['saat'])}")
      + harita(S["adres_ilce"] + " deposu")
      + "<h2>Belediye ve İSKİ İletişim</h2>"
      + p(f"Sokaktaki ana kanalizasyon arızası için {e(D.KURUM['iski_ad'])} "
          f"<b>ALO {D.KURUM['iski_tel']}</b> (7/24), İstanbul dışından "
          f"{e(D.KURUM['iski_disari'])}. Yol üstü yağmur suyu ızgarası ve genel başvurular "
          f"için {e(D.KURUM['ibb_ad'])} <b>ALO {D.KURUM['ibb_tel']}</b>.",
          "Daire içi ve bina içi tıkanıklığa bu kurumlar ekip göndermiyor — o iş özel "
          "tesisatçının işi.")
      + "</div>")
    return basit_sayfa("İletişim",
      f"{S['marka']} iletişim: {S['tel_goster']} — 7/24 tıkanıklık açma ve gider açma. "
      f"{S['adres']}.", "iletisim/", "İletişim",
      "7/24 açığız. Telefon, WhatsApp veya e-posta ile ulaşabilirsiniz.", govde)

def metin_sayfasi(slug, baslik, bloklar, aciklama=None):
    return basit_sayfa(baslik, aciklama or f"{baslik} — {S['marka']}", slug + "/", baslik, "",
                       '<div class="govde">' + "".join(f"<p>{x}</p>" for x in bloklar) + "</div>")


# ── 404 / sitemap / robots ──────────────────────────────────────────────────
def hata404():
    """⚠️ ONEK burada '/' kalır — GitHub 404'ü her derinlikteki uydurma URL için
    servis ettiği için göreli yol tutmaz ([[reference_pages_altyol_kok_goreli_yol]])."""
    cip = "".join(f'<li><a class="cip" href="/{ilce_yolu(i)}">{e(i["ad"])}</a></li>'
                  for i in sorted(D.ILCELER, key=lambda x: kucuk(x["ad"]))[:12])
    return (head("Sayfa bulunamadı (404)",
                 "Aradığınız sayfa bulunamadı; adres değişmiş olabilir. Tıkanıklık açma ve "
                 "gider açma hizmetlerimize ve 39 ilçe sayfamıza buradan ulaşabilirsiniz.",
                 "404.html")
      + ust_header()
      + f"""
<main id="ana"><section class="bolum"><div class="kap">
<div class="b-ust"><span class="b-etiket">404</span><h1>Aradığınız sayfa bulunamadı</h1>
<p>Adres değişmiş ya da sayfa kaldırılmış olabilir.</p></div>
<div class="orta"><div class="hero-dg" style="justify-content:center">
<a class="dg dg-koyu" href="/">Ana sayfa</a>
<a class="dg dg-cizgi" href="/hizmetler/">Hizmetler</a>
<a class="dg dg-cizgi" href="/bolgeler/">Bölgeler</a></div></div>
<div style="margin-top:34px"><h2 class="orta">Sık aranan ilçeler</h2>
<ul class="cipler" style="justify-content:center">{cip}</ul></div>
</div></section></main>
""" + alt_bilgi())

def sitemap(yollar):
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for y, oncelik in yollar:
        o.append(f"<url><loc>{ALAN}/{y}</loc><priority>{oncelik}</priority></url>")
    o.append("</urlset>")
    return "\n".join(o)

def robots():
    return (f"User-agent: *\nAllow: /\n\nSitemap: {ALAN}/sitemap.xml\n")

# ── Yazma ───────────────────────────────────────────────────────────────────
def yaz(yol, icerik):
    global ONEK
    tam = os.path.join(KOK, yol)
    os.makedirs(os.path.dirname(tam), exist_ok=True)
    with open(tam, "w", encoding="utf-8") as f:
        f.write(icerik)
    return len(icerik.encode("utf-8"))

def sayfa_yaz(yol, uretici):
    """yol: '' (anasayfa) / 'bolgeler/' / '404.html'"""
    global ONEK
    if yol == "404.html":
        ONEK = "/"
        dosya = "404.html"
    else:
        derinlik = yol.count("/")
        ONEK = "../" * derinlik
        dosya = (yol + "index.html") if yol else "index.html"
    n = yaz(dosya, uretici())
    ONEK = ""
    return dosya, n

def main():
    sayfalar, toplam = [], 0
    is_listesi = [("", anasayfa, "1.0")]
    for h in D.HIZMETLER:
        is_listesi.append((hizmet_yolu(h), (lambda x: lambda: hizmet_sayfasi(x))(h), "0.9"))
    for r in D.REHBERLER:
        is_listesi.append((r["slug"] + "/", (lambda x: lambda: rehber_sayfasi(x))(r), "0.8"))
    for i in D.ILCELER:
        is_listesi.append((ilce_yolu(i), (lambda x: lambda: ilce_sayfasi(x))(i), "0.8"))
    is_listesi += [
      ("hizmetler/", hizmetler_sayfasi, "0.7"),
      ("bolgeler/", bolgeler_sayfasi, "0.7"),
      ("hakkimizda/", hakkimizda_sayfasi, "0.6"),
      ("iletisim/", iletisim_sayfasi, "0.6"),
      ("gizlilik-politikasi/", lambda: metin_sayfasi("gizlilik-politikasi",
        "Gizlilik Politikası", [
        "Bu sitede ziyaretçilerden kişisel veri toplayan bir form bulunmamaktadır. "
        "İletişim yalnızca telefon, WhatsApp ve e-posta üzerinden kurulmaktadır.",
        "Site üzerinde üçüncü taraf reklam veya takip çerezi çalıştırılmamaktadır. "
        "Google Haritalar bileşeni yalnızca siz haritaya tıkladığınızda yüklenir; "
        "tıklamadığınız sürece Google'a herhangi bir istek gönderilmez.",
        "Telefon veya WhatsApp ile bize ulaştığınızda paylaştığınız bilgiler yalnızca "
        "talep ettiğiniz hizmetin yerine getirilmesi amacıyla kullanılır, üçüncü kişilerle "
        "paylaşılmaz.",
        f"Sorularınız için: <a href=\"mailto:{S['eposta']}\">{S['eposta']}</a>"],
        "Bu sitede form yok, üçüncü taraf takip çerezi çalışmıyor. Google Haritalar yalnızca "
        "siz tıklayınca yükleniyor. Kişisel veri işleme yaklaşımımız."), "0.3"),
      ("kullanim-sartlari/", lambda: metin_sayfasi("kullanim-sartlari",
        "Kullanım Şartları", [
        "Bu sitedeki bilgiler genel bilgilendirme amaçlıdır. Tesisat arızaları binadan "
        "binaya değiştiği için, sitedeki anlatımlar yerinde yapılacak bir incelemenin "
        "yerine geçmez.",
        "Sitede yer alan ev yöntemleri ve kimyasallarla ilgili uyarılar deneyime dayalı "
        "bilgilendirmedir. Bu yöntemleri kendiniz uygulamanız hâlinde doğabilecek "
        "sonuçlardan site sahibi sorumlu tutulamaz.",
        "Site içeriğinin izinsiz kopyalanması ve başka mecralarda yayımlanması yasaktır.",
        f"Sorularınız için: <a href=\"mailto:{S['eposta']}\">{S['eposta']}</a>"],
        "Sitedeki bilgiler genel bilgilendirme amaçlıdır ve yerinde incelemenin yerine geçmez. "
        "Ev yöntemleri uyarıları, sorumluluk sınırları ve içerik kullanım şartları."), "0.3"),
    ]

    for yol, uretici, oncelik in is_listesi:
        dosya, n = sayfa_yaz(yol, uretici)
        sayfalar.append((yol, oncelik))
        toplam += n

    dosya, n = sayfa_yaz("404.html", hata404)
    toplam += n

    yaz("sitemap.xml", sitemap(sayfalar))
    yaz("robots.txt", robots())
    yaz("CNAME", S["cname"] + "\n")
    yaz(".nojekyll", "")

    print(f"✓ {len(sayfalar)} sayfa + 404 · toplam {toplam/1024:.0f} KB HTML")
    print(f"  sitemap: {len(sayfalar)} URL · CNAME: {S['cname']}")
    return sayfalar

if __name__ == "__main__":
    main()
