# tessatesisat.online

TESSA TESİSAT — İstanbul tıkanıklık açma ve gider açma sitesi.
Statik site, **GitHub Pages** üzerinden `www.tessatesisat.online` adresinde yayınlanır.

## ⛔ Üretilen HTML'i elle düzenleme

Kökteki bütün `index.html` dosyaları `_src/build.py` tarafından **üretilir**;
betik her çalıştığında üzerine yazar. Metin ve veri değişikliği `_src/data.py`'ye yapılır.

## Çalışma akışı

```bash
python3 _src/media.py     # images/ ve videos/ içine yeni dosya koyduysan (türev + poster)
python3 _src/build.py     # 62 sayfa + sitemap + robots + CNAME üretir
python3 _src/denetim.py   # commit ÖNCESİ — hata varsa 1 döner
```

## Dosyalar

| Dosya | İş |
|---|---|
| `_src/data.py` | Firma bilgisi, 39 ilçe, hizmetler, H2 havuzu, metinler, kurum numaraları |
| `_src/build.py` | Sayfa üreticisi |
| `_src/denetim.py` | Üstünlük iddiası, yinelenen title, kırık yol, imza denetimi |
| `_src/logo.py` | favicon.ico + 48/96/192 png + apple-touch-icon |
| `_src/media.py` | Görsel türevleri (w500/w900/w1600) + video posterleri |

## Sayfa yapısı (62 sayfa)

- 1 anasayfa
- 15 hizmet sayfası (`/tikaniklik-acma/`, `/gider-acma/`, `/lavabo-tikanikligi-acma/` …)
- 1 rehber (`/lavabo-acma-yontemleri/`)
- **39 ilçe sayfası** (`/esenyurt-tikaniklik-acma/` …) — her biri ~2.200 kelime
- 4 liste/kurumsal + 2 hukuki sayfa

⛔ **İlçe × hizmet matrisi açılmadı.** Her ilçe sayfası hem "tıkanıklık açma" hem
"gider açma" niyetini, 9 rotasyonlu H2 + ilçeye özel teknik bölüm + belediye/İSKİ
sorumluluk tablosuyla tek sayfada kapsıyor. Mahalle sayfası da yok.
Gerekçe: Google'ın "ölçeklendirilmiş içeriği kötüye kullanma" politikası.

## Kurallar

- Üstünlük iddiası yazılmaz ("en iyi", "en hızlı", "lider") — `denetim.py` hata sayar.
- Teyit edilmemiş rakam yazılmaz — `data.TEYITSIZ` listesi uyarı üretir.
- Üçüncü parti istek **sıfır**: font yerel, ikonlar satır içi SVG, harita facade.
- Tüm iç yollar sayfa derinliğine göre **göreli** (`ONEK`) — `404.html` istisna.
