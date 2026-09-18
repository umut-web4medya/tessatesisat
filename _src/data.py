# -*- coding: utf-8 -*-
"""
tessatesisat.online veri katmanı.

⛔ Üretilen HTML'i ELLE DÜZENLEME — build.py her çalıştığında üzerine yazar.
   Metin/veri değişikliği BURAYA yapılır.
"""

# ── Firma ───────────────────────────────────────────────────────────────────
# ⛔ Buradaki hiçbir bilgi uydurulmadı; tessatesisat.com.tr'den ve kullanıcıdan alındı.
SITE = {
    "marka":      "TESSA TESİSAT",
    "alan":       "https://www.tessatesisat.online",
    "cname":      "www.tessatesisat.online",
    "tel_goster": "0552 156 64 84",
    "tel_link":   "+905521566484",
    "wa":         "905521566484",
    "eposta":     "info@tessatesisat.com",
    "adres":      "Fevziçakmak Mah. Ferhatpaşa Cad. No:26/A Esenler / İstanbul",
    "adres_sokak":"Fevziçakmak Mah. Ferhatpaşa Cad. No:26/A",
    "adres_ilce": "Esenler",
    "adres_il":   "İstanbul",
    "posta_kodu": "34100",
    "merkez_ilce":"Esenler",
    "merkez_slug":"esenler",
    "saat":       "7/24 Acil Müdahale & Servis",
    # Google Haritalar — kullanıcının verdiği gömme bağlantısındaki kayıt
    "harita_baslik": "Esenler Su Tesisatçısı - Tessa Tesisat",
    "harita_embed": ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3009.3806266425017"
                     "!2d28.878719775950564!3d41.03880471754479!2m3!1f0!2f0!3f0!3m2!1i1024!2i768"
                     "!4f13.1!3m3!1m2!1s0x14cabb0e5b20fa59%3A0xdab018bea8ab273a"
                     "!2sEsenler%20Su%20Tesisat%C3%A7%C4%B1s%C4%B1%20-%20Tessa%20Tesisat"
                     "!5e0!3m2!1str!2str!4v1789684600574!5m2!1str!2str"),
    "enlem":      41.038804,
    "boylam":     28.878719,
}

# ⏳ TEYİT BEKLİYOR — kullanıcı onaylayana kadar sitede KULLANILMAZ.
#    (denetim.py bu listedeki bir ifadeyi HTML'de bulursa uyarı basar)
TEYITSIZ = [
    "yıl tecrübe", "15400", "2150", "4.9", "%99", "memnuniyet",
]

# ✅ ONAYLI İDDİALAR — kullanıcı 2026-09-18'de bizzat beyan etti, sitede kullanılır.
#    ⚠️ Ticari Reklam Yönetmeliği ispat istiyor; bunlar firmanın kendi beyanı.
#    Üstünlük iddiası DEĞİL (en hızlı/en iyi demiyor), hizmet tanımı.
ONAYLI = {
  "ayni_gun":  "Her ilçede aynı gün içinde kameralı gider açma hizmeti",
  "varis":     "İstanbul'un her noktasına ortalama 30 dakikada ulaşım",
  "varis_kisa":"ortalama 30 dakika",
  "yontem":    "Kırmadan, dökmeden; uzman ekiple",
}

# ⛔ ÜSTÜNLÜK İDDİASI YASAK — Ticari Reklam ve Haksız Ticari Uygulamalar
#    Yönetmeliği ispat istiyor. denetim.py bunları HATA sayar.
YASAK_IDDIA = [
    "en iyi", "en ucuz", "lider", "bir numara", "1 numara", "türkiye'nin en",
    "istanbul'un en iyi", "rakipsiz", "en kaliteli", "garanti ediyoruz ki",
]


# ── Türkçe ek tablosu ───────────────────────────────────────────────────────
# ⛔ Kod içinde "{ad}'da" gibi elle ek YAZMA — build.ek(i, "loc|dat|gen|abl") kullan.
#    Otomatik ünlü uyumu yetmiyor: Beşiktaş'TA, Fatih'TE, Beylikdüzü'NDE,
#    Zeytinburnu'NDA, Ümraniye'YE. (dehaiskele'de ilk üretimde "Ümraniye'da" çıkmıştı)
#                 loc(-de)  dat(-e)  gen(-in)  abl(-den)
ILCE_EK = {
    "adalar":        ("'da",  "'a",   "'ın",   "'dan"),
    "arnavutkoy":    ("'de",  "'e",   "'ün",   "'den"),
    "atasehir":      ("'de",  "'e",   "'in",   "'den"),
    "avcilar":       ("'da",  "'a",   "'ın",   "'dan"),
    "bagcilar":      ("'da",  "'a",   "'ın",   "'dan"),
    "bahcelievler":  ("'de",  "'e",   "'in",   "'den"),
    "bakirkoy":      ("'de",  "'e",   "'ün",   "'den"),
    "basaksehir":    ("'de",  "'e",   "'in",   "'den"),
    "bayrampasa":    ("'da",  "'ya",  "'nın",  "'dan"),
    "besiktas":      ("'ta",  "'a",   "'ın",   "'tan"),
    "beykoz":        ("'da",  "'a",   "'un",   "'dan"),
    "beylikduzu":    ("'nde", "'ne",  "'nün",  "'nden"),
    "beyoglu":       ("'nda", "'na",  "'nun",  "'ndan"),
    "buyukcekmece":  ("'de",  "'ye",  "'nin",  "'den"),
    "catalca":       ("'da",  "'ya",  "'nın",  "'dan"),
    "cekmekoy":      ("'de",  "'e",   "'ün",   "'den"),
    "esenler":       ("'de",  "'e",   "'in",   "'den"),
    "esenyurt":      ("'ta",  "'a",   "'un",   "'tan"),
    "eyupsultan":    ("'da",  "'a",   "'ın",   "'dan"),
    "fatih":         ("'te",  "'e",   "'in",   "'ten"),
    "gaziosmanpasa": ("'da",  "'ya",  "'nın",  "'dan"),
    "gungoren":      ("'de",  "'e",   "'in",   "'den"),
    "kadikoy":       ("'de",  "'e",   "'ün",   "'den"),
    "kagithane":     ("'de",  "'ye",  "'nin",  "'den"),
    "kartal":        ("'da",  "'a",   "'ın",   "'dan"),
    "kucukcekmece":  ("'de",  "'ye",  "'nin",  "'den"),
    "maltepe":       ("'de",  "'ye",  "'nin",  "'den"),
    "pendik":        ("'te",  "'e",   "'in",   "'ten"),
    "sancaktepe":    ("'de",  "'ye",  "'nin",  "'den"),
    "sariyer":       ("'de",  "'e",   "'in",   "'den"),
    "silivri":       ("'de",  "'ye",  "'nin",  "'den"),
    "sultanbeyli":   ("'de",  "'ye",  "'nin",  "'den"),
    "sultangazi":    ("'de",  "'ye",  "'nin",  "'den"),
    "sile":          ("'de",  "'ye",  "'nin",  "'den"),
    "sisli":         ("'de",  "'ye",  "'nin",  "'den"),
    "tuzla":         ("'da",  "'ya",  "'nın",  "'dan"),
    "umraniye":      ("'de",  "'ye",  "'nin",  "'den"),
    "uskudar":       ("'da",  "'a",   "'ın",   "'dan"),
    "zeytinburnu":   ("'nda", "'na",  "'nun",  "'ndan"),
}


# ── İlçeler ─────────────────────────────────────────────────────────────────
# Her ilçenin metni BU alanlardan türetilir. Amaç kelime değiştirerek 39 kopya
# üretmek değil; ilçenin yapı stoğu / hat tipi / baskın tıkanma sebebi / erişim
# koşulu gerçekten farklı olduğu için metin de farklı çıkıyor.
#   yapi   : baskın yapı stoğu
#   hat    : pis su hattının karakteri
#   risk   : o ilçede en sık karşılaşılan tıkanma sebebi
#   erisim : ekip/araç erişimi ve müdahale koşulu
#   mahalle: gerçek mahalle adları (SAYFA AÇILMAZ — sadece metinde geçer)
ILCELER = [
 {"ad":"Adalar","slug":"adalar","yaka":"Anadolu",
  "komsu":["maltepe","kartal"],
  "mahalle":["Büyükada","Heybeliada","Burgazada","Kınalıada","Nizam","Maden"],
  "yapi":"ahşap köşkler ve yüzyıllık yazlık konutlar",
  "hat":"eğimi düşük, bir kısmı hâlâ fosseptiğe bağlı eski hatlar",
  "risk":"yaz nüfusuyla birlikte katlanan kullanım ve ağaç kökü",
  "erisim":"ekip ve ekipman vapurla geçtiği için iş planı bir gün önceden kuruluyor"},

 {"ad":"Arnavutköy","slug":"arnavutkoy","yaka":"Avrupa",
  "komsu":["basaksehir","eyupsultan","sultangazi","catalca","buyukcekmece","esenyurt"],
  "mahalle":["Hadımköy","Taşoluk","Bolluca","Haraççı","Boğazköy","Ömerli"],
  "yapi":"köy dokusundan kalma müstakil evlerle yeni toplu konutların iç içe olduğu karma stok",
  "hat":"şebeke hattı ile fosseptiğin yan yana bulunduğu geçiş bölgesi",
  "risk":"bahçeli evlerde uzun bahçe hattı ve kök sarması",
  "erisim":"ilçe çok geniş olduğu için adres tarifi telefonda netleştiriliyor"},

 {"ad":"Ataşehir","slug":"atasehir","yaka":"Anadolu",
  "komsu":["kadikoy","umraniye","maltepe","uskudar"],
  "mahalle":["Barbaros","Küçükbakkalköy","İçerenköy","Ferhatpaşa","Yenisahra","Örnek"],
  "yapi":"yüksek katlı rezidans ve site blokları",
  "hat":"çok katı tek kolona bağlayan ortak iniş hatları",
  "risk":"üst katlardan atılan ıslak mendilin kolon dibinde toplanması",
  "erisim":"site yönetimiyle önceden haberleşilip otopark giriş izni alınıyor"},

 {"ad":"Avcılar","slug":"avcilar","yaka":"Avrupa",
  "komsu":["kucukcekmece","esenyurt","beylikduzu","buyukcekmece"],
  "mahalle":["Ambarlı","Denizköşkler","Merkez","Üniversite","Cihangir","Tahtakale"],
  "yapi":"1980–2000 arası yapılmış orta katlı apartmanlar",
  "hat":"gevşek alüvyon zeminde oturma yapmış, ek yerleri açılmaya müsait hatlar",
  "risk":"zemin oturmasıyla kayan boru ekinde biriken tortu",
  "erisim":"öğrenci yoğunluğu nedeniyle akşam saatlerinde de servis veriliyor"},

 {"ad":"Bağcılar","slug":"bagcilar","yaka":"Avrupa",
  "komsu":["bahcelievler","gungoren","esenler","kucukcekmece","basaksehir"],
  "mahalle":["Güneşli","Kirazlı","Yıldıztepe","Demirkapı","Mahmutbey","Yenimahalle"],
  "yapi":"zemin katları atölyeye çevrilmiş yoğun apartman dokusu",
  "hat":"konut ve imalathanenin aynı kolonu paylaştığı hatlar",
  "risk":"atölye artığı, boya ve tekstil lifinin gidere dökülmesi",
  "erisim":"sanayi yoğunluğu nedeniyle mesai dışı ve hafta sonu müdahale sık"},

 {"ad":"Bahçelievler","slug":"bahcelievler","yaka":"Avrupa",
  "komsu":["bagcilar","gungoren","bakirkoy","kucukcekmece"],
  "mahalle":["Şirinevler","Yenibosna","Soğanlı","Kocasinan","Siyavuşpaşa","Zafer"],
  "yapi":"1985–2005 arası sıkışık apartman adaları",
  "hat":"sokak boyunca uzayan, rögara kadar uzun yatay hatlar",
  "risk":"bodrum kat dairelerinde geri tepme ve kokunun birlikte gelmesi",
  "erisim":"apartman görevlisiyle ortak çalışıp bina ana hattı baştan kontrol ediliyor"},

 {"ad":"Bakırköy","slug":"bakirkoy","yaka":"Avrupa",
  "komsu":["bahcelievler","zeytinburnu","kucukcekmece"],
  "mahalle":["Ataköy","Yeşilköy","Florya","Yeşilyurt","Zeytinlik","Cevizlik"],
  "yapi":"Ataköy blokları ve sahil şeridindeki köklü siteler",
  "hat":"deniz seviyesine yakın, eğimi az çalışan tahliye hatları",
  "risk":"düşük eğimde ilerleyemeyip çöken katı atık birikintisi",
  "erisim":"site blokları arasında ekipmanı taşımak için kısa mesafe el arabası kullanılıyor"},

 {"ad":"Başakşehir","slug":"basaksehir","yaka":"Avrupa",
  "komsu":["arnavutkoy","esenyurt","kucukcekmece","bagcilar","sultangazi","esenler"],
  "mahalle":["İkitelli","Kayaşehir","Ziya Gökalp","Başak","Altınşehir","Bahçeşehir"],
  "yapi":"İkitelli sanayi sitesiyle yeni toplu konutların bir arada olduğu karma yapı",
  "hat":"yeni döşenmiş ama blok sayısı yüzünden çok uzun yatay PVC hatlar",
  "risk":"sanayi tarafında yağ, tiner ve boya artığının hattı kaplaması",
  "erisim":"kapalı site girişlerinde ziyaretçi kaydı için kimlik ve plaka önceden bildiriliyor"},

 {"ad":"Bayrampaşa","slug":"bayrampasa","yaka":"Avrupa",
  "komsu":["esenler","gaziosmanpasa","eyupsultan","zeytinburnu","fatih"],
  "mahalle":["Yıldırım","Kartaltepe","Altıntepsi","Muratpaşa","Terazidere","Vatan"],
  "yapi":"hal ve toptancı çevresinde yoğunlaşan iş yeri + konut karışımı",
  "hat":"gıda toptancılığının yükünü taşıyan, yağ yükü yüksek hatlar",
  "risk":"donmuş yağ tabakasının boru çapını daraltması",
  "erisim":"hal bölgesinde iş akışını durdurmamak için gece vardiyasında da çalışılıyor"},

 {"ad":"Beşiktaş","slug":"besiktas","yaka":"Avrupa",
  "komsu":["sisli","sariyer","kagithane","beyoglu"],
  "mahalle":["Ortaköy","Bebek","Etiler","Levent","Arnavutköy","Gayrettepe"],
  "yapi":"dik yamaca oturan eski apartmanlarla Levent tarafındaki ofis blokları",
  "hat":"yüksek eğimli, hızlı akan ama dirsek sayısı fazla hatlar",
  "risk":"sahil şeridindeki yoğun mutfak kullanımından gelen yağ",
  "erisim":"dar ve eğimli sokaklarda araç park yeri önceden ayarlanıyor"},

 {"ad":"Beykoz","slug":"beykoz","yaka":"Anadolu",
  "komsu":["uskudar","umraniye","cekmekoy","sile","sariyer"],
  "mahalle":["Kavacık","Paşabahçe","Anadolu Hisarı","Çubuklu","Acarkent","Riva"],
  "yapi":"orman sınırındaki müstakil evler, villalar ve köy dokusu",
  "hat":"bahçe içinden geçen uzun hatlar ve yaygın fosseptik kullanımı",
  "risk":"ağaç kökünün boru ekine girip hattı sarması",
  "erisim":"villa bahçelerinde rögar kapağının yeri kamerayla tespit ediliyor"},

 {"ad":"Beylikdüzü","slug":"beylikduzu","yaka":"Avrupa",
  "komsu":["avcilar","buyukcekmece","esenyurt"],
  "mahalle":["Cumhuriyet","Barış","Gürpınar","Yakuplu","Adnan Kahveci","Marmara"],
  "yapi":"2005 sonrası planlı site ve rezidans yerleşimi",
  "hat":"blok çıkışından site rögarına kadar uzanan uzun ortak hatlar",
  "risk":"ıslak mendil ve temizlik bezinin klozetten atılması",
  "erisim":"site yönetimiyle ortak hat mı daire hattı mı olduğu baştan ayrıştırılıyor"},

 {"ad":"Beyoğlu","slug":"beyoglu","yaka":"Avrupa",
  "komsu":["sisli","besiktas","kagithane","eyupsultan","fatih"],
  "mahalle":["Cihangir","Galata","Tarlabaşı","Kasımpaşa","Şişhane","Hacımimi"],
  "yapi":"yüz yılı aşkın taş ve kâgir binalar",
  "hat":"font (pik) döküm boruların hâlâ kullanımda olduğu tarihî hatlar",
  "risk":"döküm borunun iç yüzeyinde kabuklaşma ve kireç birikmesi",
  "erisim":"dar sokak ve merdivenli girişlerde ekipman elle taşınıyor"},

 {"ad":"Büyükçekmece","slug":"buyukcekmece","yaka":"Avrupa",
  "komsu":["beylikduzu","esenyurt","arnavutkoy","catalca","silivri"],
  "mahalle":["Mimarsinan","Kumburgaz","Celaliye","Kamiloba","Atatürk","Türkoba"],
  "yapi":"sahil yazlıkları ve yıl boyu oturulan sitelerin karışımı",
  "hat":"yazlık dönem dışında az kullanılan, uzun süre durunca tıkanan hatlar",
  "risk":"sezon açılışında uzun süre kullanılmayan hatta oturan tortu",
  "erisim":"yazlık sitelerde sezon öncesi toplu hat kontrolü yapılıyor"},

 {"ad":"Çatalca","slug":"catalca","yaka":"Avrupa",
  "komsu":["arnavutkoy","buyukcekmece","silivri"],
  "mahalle":["Ferhatpaşa","Kaleiçi","Ovayenice","Çanakça","İzzettin","Elbasan"],
  "yapi":"köy yerleşimleri ve tarım işletmeleriyle müstakil konutlar",
  "hat":"şebeke yerine ağırlıklı olarak fosseptik ve sızdırma kuyusu",
  "risk":"fosseptiğin dolması ve tahliye hattının geri basması",
  "erisim":"mesafe uzun olduğu için ekip günü baştan planlayarak yola çıkıyor"},

 {"ad":"Çekmeköy","slug":"cekmekoy","yaka":"Anadolu",
  "komsu":["umraniye","sancaktepe","beykoz","sile"],
  "mahalle":["Taşdelen","Alemdağ","Ömerli","Soğukpınar","Mimarsinan","Hamidiye"],
  "yapi":"köy dokusunun üzerine kurulmuş yeni siteler ve müstakil evler",
  "hat":"orman sınırına yakın, bahçe içinden geçen hatlar",
  "risk":"kök sarması ve yağmurla hatta giren toprak",
  "erisim":"bahçeli parsellerde hattın güzergâhı kamerayla çıkarılıyor"},

 {"ad":"Esenler","slug":"esenler","yaka":"Avrupa",
  "komsu":["bagcilar","bayrampasa","gaziosmanpasa","sultangazi","basaksehir","gungoren"],
  "mahalle":["Fevziçakmak","Menderes","Oruçreis","Havaalanı","Çifte Havuzlar","Nine Hatun"],
  "yapi":"1990'ların yoğun apartman dokusu ve otogar çevresindeki iş yerleri",
  "hat":"birbirine çok yakın binaların aynı sokak hattına bağlandığı yoğun şebeke",
  "risk":"bina yoğunluğu nedeniyle tek bir ana hat tıkanınca birkaç binanın birden etkilenmesi",
  "erisim":"deponun bulunduğu ilçe; ekip ve ekipman aynı noktadan çıkıyor"},

 {"ad":"Esenyurt","slug":"esenyurt","yaka":"Avrupa",
  "komsu":["avcilar","beylikduzu","buyukcekmece","arnavutkoy","basaksehir","kucukcekmece"],
  "mahalle":["Örnek","Yenikent","Saadetdere","Balıkyolu","İnönü","Namık Kemal"],
  "yapi":"kısa sürede yükselmiş çok bloklu yeni konut alanları",
  "hat":"hızlı yapılaşmada eğimi yeterince verilmemiş uzun bağlantı hatları",
  "risk":"inşaat artığı kireç ve harcın hatta oturup sertleşmesi",
  "erisim":"nüfus yoğunluğu yüksek olduğu için gün içinde birden çok ekip dolaşıyor"},

 {"ad":"Eyüpsultan","slug":"eyupsultan","yaka":"Avrupa",
  "komsu":["gaziosmanpasa","kagithane","sisli","beyoglu","bayrampasa","sultangazi","arnavutkoy","sariyer"],
  "mahalle":["Alibeyköy","Göktürk","Rami","Nişanca","Silahtarağa","Kemerburgaz"],
  "yapi":"tarihî Eyüp dokusu, Alibeyköy vadisi ve Göktürk tarafındaki yeni siteler",
  "hat":"vadi tabanında toplanan, yağışta yükü artan hatlar",
  "risk":"sağanak sonrası hatta dolan çamur ve yaprak",
  "erisim":"vadi ile sırt arasındaki kot farkına göre ekipman seçiliyor"},

 {"ad":"Fatih","slug":"fatih","yaka":"Avrupa",
  "komsu":["zeytinburnu","bayrampasa","eyupsultan","beyoglu"],
  "mahalle":["Aksaray","Balat","Fener","Çapa","Sultanahmet","Kocamustafapaşa"],
  "yapi":"tarihî yarımadanın yüzyıllık binaları ve otel–lokanta yoğunluğu",
  "hat":"şehrin en eski kanalizasyon güzergâhları, yer yer tuğla kanal",
  "risk":"eski döküm hatta kabuklaşma ve lokanta kaynaklı yağ birikmesi",
  "erisim":"dar sokaklarda ve sit alanında kırmadan çalışmak zorunlu"},

 {"ad":"Gaziosmanpaşa","slug":"gaziosmanpasa","yaka":"Avrupa",
  "komsu":["eyupsultan","sultangazi","esenler","bayrampasa"],
  "mahalle":["Karayolları","Yenidoğan","Merkez","Sarıgöl","Hürriyet","Barbaros Hayrettin"],
  "yapi":"kentsel dönüşümün sürdüğü, eski ve yeni bloğun yan yana durduğu doku",
  "hat":"yeni binaların eski sokak hattına bağlandığı karma şebeke",
  "risk":"inşaat molozunun ve kesilmiş boru parçasının hatta kalması",
  "erisim":"şantiye trafiği nedeniyle araç yaklaşım noktası önceden konuşuluyor"},

 {"ad":"Güngören","slug":"gungoren","yaka":"Avrupa",
  "komsu":["bagcilar","bahcelievler","esenler","zeytinburnu"],
  "mahalle":["Merter","Tozkoparan","Haznedar","Gençosman","Sanayi","Akıncılar"],
  "yapi":"Merter çevresinde tekstil atölyeleriyle iç içe geçmiş yoğun yapı",
  "hat":"konfeksiyon atölyelerinin yükünü taşıyan dar çaplı hatlar",
  "risk":"kumaş lifi, iplik ve boya suyu artığının hattı keçeleştirmesi",
  "erisim":"atölye yoğun sokaklarda üretimi aksatmamak için mesai sonrası çalışılıyor"},

 {"ad":"Kadıköy","slug":"kadikoy","yaka":"Anadolu",
  "komsu":["uskudar","atasehir","maltepe"],
  "mahalle":["Moda","Caferağa","Fenerbahçe","Göztepe","Bostancı","Kozyatağı"],
  "yapi":"Moda ve çarşı çevresindeki köklü apartmanlarla sahil siteleri",
  "hat":"eski stokta hâlâ döküm boru bulunan, sahilde eğimi düşen hatlar",
  "risk":"çarşıdaki yoğun yeme-içme işletmelerinden gelen yağ yükü",
  "erisim":"çarşı içinde araç kısıtı olduğundan ekipman yakın noktadan taşınıyor"},

 {"ad":"Kağıthane","slug":"kagithane","yaka":"Avrupa",
  "komsu":["sisli","besiktas","eyupsultan","beyoglu","sariyer"],
  "mahalle":["Merkez","Çağlayan","Seyrantepe","Gültepe","Hamidiye","Nurtepe"],
  "yapi":"vadi tabanındaki ofis dönüşümleriyle yamaçtaki eski konut stoğu",
  "hat":"dere kotuna inen, yağışta yükü hızla artan hatlar",
  "risk":"yamaçtan inen çamur ve kumun hatta çökmesi",
  "erisim":"kot farkı yüksek olduğu için uzun spiral ve basınçlı araç birlikte kullanılıyor"},

 {"ad":"Kartal","slug":"kartal","yaka":"Anadolu",
  "komsu":["maltepe","pendik","sancaktepe","sultanbeyli","adalar"],
  "mahalle":["Soğanlık","Yakacık","Cevizli","Orhantepe","Esentepe","Uğur Mumcu"],
  "yapi":"dönüşümle yenilenen sahil şeridi ve yamaçtaki eski apartmanlar",
  "hat":"yeni kulelerin eski sokak hattına bağlandığı geçiş dönemi şebekesi",
  "risk":"yıkım ve inşaat döneminde hatta giren moloz",
  "erisim":"şantiye yoğunluğuna göre giriş noktası gün içinde değişebiliyor"},

 {"ad":"Küçükçekmece","slug":"kucukcekmece","yaka":"Avrupa",
  "komsu":["avcilar","esenyurt","basaksehir","bagcilar","bahcelievler","bakirkoy"],
  "mahalle":["Sefaköy","Halkalı","Atakent","İnönü","Cennet","Kanarya"],
  "yapi":"eski Sefaköy dokusuyla Halkalı tarafındaki yeni sitelerin karışımı",
  "hat":"göl kenarındaki düşük kotta tahliyesi zorlaşan hatlar",
  "risk":"düşük kotta geri tepme ve bodrum katlarda su yükselmesi",
  "erisim":"bodrum müdahalelerinde önce geri tepmenin kaynağı ayrıştırılıyor"},

 {"ad":"Maltepe","slug":"maltepe","yaka":"Anadolu",
  "komsu":["kadikoy","atasehir","kartal","sancaktepe","adalar"],
  "mahalle":["Bağlarbaşı","Cevizli","Küçükyalı","Altayçeşme","Zümrütevler","Gülsuyu"],
  "yapi":"sahil siteleriyle yamaçtaki eski konut stoğunun bir arada olduğu doku",
  "hat":"sahilde eğimi azalan, yamaçta hızlanan iki karakterli hatlar",
  "risk":"eğim değişiminin olduğu noktada katı atığın takılması",
  "erisim":"kot farkı nedeniyle müdahale noktası bina girişinden değil rögardan seçiliyor"},

 {"ad":"Pendik","slug":"pendik","yaka":"Anadolu",
  "komsu":["kartal","sultanbeyli","sancaktepe","tuzla","cekmekoy"],
  "mahalle":["Kaynarca","Yenişehir","Çamçeşme","Batı","Kurtköy","Güllübağlar"],
  "yapi":"sahil şeridi, tersane çevresi ve Kurtköy tarafındaki yeni siteler",
  "hat":"ilçenin genişliği nedeniyle birbirinden çok farklı karakterde hatlar",
  "risk":"sanayi çevresinde yağ ve talaş, konut tarafında ıslak mendil",
  "erisim":"ilçe uzun olduğu için ekip sabah güzergâhını kuzey–güney ayırarak planlıyor"},

 {"ad":"Sancaktepe","slug":"sancaktepe","yaka":"Anadolu",
  "komsu":["umraniye","cekmekoy","sultanbeyli","kartal","maltepe","pendik"],
  "mahalle":["Sarıgazi","Samandıra","Abdurrahmangazi","Yenidoğan","Osmangazi","Eyüpsultan"],
  "yapi":"köy yerleşiminden dönüşen, hızla apartmanlaşan doku",
  "hat":"eski müstakil ev hattına bağlanmış yeni apartman kolonları",
  "risk":"eski çapın yeni bina yükünü kaldıramaması",
  "erisim":"bina hattı mı sokak hattı mı olduğu kamerayla ayrıştırılıyor"},

 {"ad":"Sarıyer","slug":"sariyer","yaka":"Avrupa",
  "komsu":["besiktas","sisli","kagithane","eyupsultan","beykoz"],
  "mahalle":["Maslak","Tarabya","Yeniköy","Kilyos","Bahçeköy","Rumelifeneri"],
  "yapi":"boğaz yalıları, bahçeli konutlar ve kuzeyde köy dokusu",
  "hat":"orman ve bahçe içinden geçen uzun, dik eğimli hatlar",
  "risk":"ağaç kökü ve yaprak birikmesi",
  "erisim":"dik rampalarda araç yanaşamıyorsa taşınabilir ekipman kullanılıyor"},

 {"ad":"Silivri","slug":"silivri","yaka":"Avrupa",
  "komsu":["catalca","buyukcekmece"],
  "mahalle":["Selimpaşa","Gümüşyaka","Ortaköy","Alipaşa","Değirmenköy","Kavaklı"],
  "yapi":"sahil yazlıkları, köy evleri ve yıl boyu oturulan siteler",
  "hat":"köylerde fosseptik, sahilde şebeke olmak üzere iki ayrı düzen",
  "risk":"sezon dışında uzun süre kullanılmayan hatta çöken tortu",
  "erisim":"mesafe uzun olduğu için aynı bölgedeki işler tek güzergâhta toplanıyor"},

 {"ad":"Sultanbeyli","slug":"sultanbeyli","yaka":"Anadolu",
  "komsu":["sancaktepe","kartal","pendik"],
  "mahalle":["Abdurrahmangazi","Mehmet Akif","Hasanpaşa","Turgutreis","Fatih","Battalgazi"],
  "yapi":"kendi imkânıyla yapılmış yapıların üzerine eklenen katlarla büyümüş doku",
  "hat":"sonradan eklenen katlara göre genişletilmemiş dar çaplı hatlar",
  "risk":"kat sayısı artınca yetersiz kalan boru çapı",
  "erisim":"dar sokaklarda araç yaklaşamadığında taşınabilir makineyle çalışılıyor"},

 {"ad":"Sultangazi","slug":"sultangazi","yaka":"Avrupa",
  "komsu":["gaziosmanpasa","eyupsultan","arnavutkoy","basaksehir","esenler"],
  "mahalle":["Cebeci","Habibler","Uğur Mumcu","Esentepe","Gazi","50. Yıl"],
  "yapi":"dönüşüm süreci devam eden yoğun konut alanları",
  "hat":"eski hattın üzerine yeni bina bağlantılarının eklendiği şebeke",
  "risk":"bağlantı noktalarında kaçak ve çökme",
  "erisim":"hat güzergâhı belirsiz olduğunda önce kamerayla haritalanıyor"},

 {"ad":"Şile","slug":"sile","yaka":"Anadolu",
  "komsu":["beykoz","cekmekoy"],
  "mahalle":["Ağva","Çayırbaşı","Kumbaba","Balibey","Doğancılı","Teke"],
  "yapi":"yazlık siteler, pansiyonlar ve köy evleri",
  "hat":"ağırlıklı olarak fosseptik ve sızdırma kuyusu düzeni",
  "risk":"yaz sezonunda kapasitesini aşan fosseptik ve kumlu zeminde tıkanma",
  "erisim":"sezonda yoğunluk arttığı için randevu gün içinde bloklanarak veriliyor"},

 {"ad":"Şişli","slug":"sisli","yaka":"Avrupa",
  "komsu":["besiktas","kagithane","beyoglu","eyupsultan","sariyer"],
  "mahalle":["Nişantaşı","Mecidiyeköy","Kurtuluş","Fulya","Bomonti","Esentepe"],
  "yapi":"plaza ve iş merkezleriyle Kurtuluş–Nişantaşı tarafındaki eski apartmanlar",
  "hat":"derin bodrumlardan pompayla basılan ve eski kolonlara bağlanan hatlar",
  "risk":"iş yeri mutfaklarından gelen yağın eski kolonda katılaşması",
  "erisim":"plazalarda teknik müdürlükten çalışma izni alınarak giriliyor"},

 {"ad":"Tuzla","slug":"tuzla","yaka":"Anadolu",
  "komsu":["pendik"],
  "mahalle":["Aydınlı","İçmeler","Postane","Şifa","Orhanlı","Cami"],
  "yapi":"tersane ve organize sanayi çevresiyle yeni konut siteleri",
  "hat":"sanayi debisiyle konut hattının ayrıştığı iki ayrı düzen",
  "risk":"sanayi tarafında yağ, tortu ve metal talaşı",
  "erisim":"tesis içi çalışmalarda iş güvenliği prosedürüne uyularak giriliyor"},

 {"ad":"Ümraniye","slug":"umraniye","yaka":"Anadolu",
  "komsu":["uskudar","atasehir","cekmekoy","sancaktepe","beykoz"],
  "mahalle":["Çakmak","Atatürk","Tepeüstü","İnkılap","Armağanevler","Dudullu"],
  "yapi":"1990–2010 arası hızla apartmanlaşan yoğun konut dokusu ve Dudullu sanayi",
  "hat":"kısa sürede genişleyen şebekede çap farkı bulunan hatlar",
  "risk":"çap değişimi olan noktada katı atığın takılması",
  "erisim":"sanayi ve konut bölgeleri için ayrı ekipman hazırlığı yapılıyor"},

 {"ad":"Üsküdar","slug":"uskudar","yaka":"Anadolu",
  "komsu":["kadikoy","atasehir","umraniye","beykoz"],
  "mahalle":["Kuzguncuk","Çengelköy","Acıbadem","Bulgurlu","Altunizade","Ünalan"],
  "yapi":"sahildeki tarihî doku ile yamaçtaki eski ve yeni konut karışımı",
  "hat":"dik yamaçtan sahile inen, eğimi ani değişen hatlar",
  "risk":"eski stokta döküm boru kabuklaşması, sahilde eğim kaybı",
  "erisim":"dar ve eğimli sokaklarda küçük araçla yaklaşılıyor"},

 {"ad":"Zeytinburnu","slug":"zeytinburnu","yaka":"Avrupa",
  "komsu":["bakirkoy","bahcelievler","gungoren","bayrampasa","fatih"],
  "mahalle":["Merkezefendi","Telsiz","Seyitnizam","Kazlıçeşme","Yenidoğan","Veliefendi"],
  "yapi":"deri ve tekstil sanayisinden dönüşen, yoğun konut ve iş yeri karışımı",
  "hat":"sanayi döneminden kalma geniş çaplı ama yıpranmış hatlar",
  "risk":"eski sanayi hattında tortu ve kimyasal artık kalıntısı",
  "erisim":"sahil ve sanayi tarafı için farklı ekipman planlanıyor"},
]


# ── H2 kelime havuzu ────────────────────────────────────────────────────────
# Kullanıcının verdiği örnek başlıklardan türetildi. Her ilçe, slug'ından
# hesaplanan sabit bir kaydırma ile FARKLI kombinasyon alır → 39 sayfa aynı
# 10 başlığı tekrarlamaz.
#
# Şablon anahtarları:  {ad}=Esenyurt  {loc}=Esenyurt'ta  {dat}=Esenyurt'a
#                      {gen}=Esenyurt'un  {abl}=Esenyurt'tan
#
# ⚠️ "en hızlı / en iyi / en uygun" gibi İSPAT GEREKTİREN üstünlük iddiaları
#    doğrudan başlık yapılmadı (Ticari Reklam ve Haksız Ticari Uygulamalar
#    Yönetmeliği). Kullanıcının listesindeki "en hızlı tıkanıklık servisi"
#    arama niyeti korunarak SORU kalıbına çevrildi — kelime yine sayfada geçiyor,
#    ama firma kendisi için iddia etmiş olmuyor. ⛔ Geri çevirme.
#
# (başlık şablonu, gövde üreticisi anahtarı)
H2_HAVUZ = {
 # ── Usta / servis çağırma niyeti ──
 "usta": [
  ("{ad} Tıkanıklık Açma Ustası", "usta"),
  ("{ad} Tıkanıklık Ustası Çağır", "usta_cagir"),
  ("{ad} Tıkanıklık Açma Servisi", "servis"),
  ("{ad} Gider Açma Ustası", "usta_gider"),
  ("{loc} Tıkanıklık Açtırmak İsteyenler İçin", "actirmak"),
  ("{ad} Tıkanıklık Servisi Ara", "servis_ara"),
  ("{ad} Su Tesisatçısı ve Tıkanıklık Ustası", "tesisatci_usta"),
  ("{loc} Gider Açtırma Hizmeti", "actirma_gider"),
 ],
 # ── Telefon / numara niyeti ──
 "numara": [
  ("{ad} Tıkanıklık Açma Servisi İçin Hangi Numarayı Aramalısınız?", "numara"),
  ("{ad} Tıkanıklık Servisi Telefonu", "telefon"),
  ("{loc} Tıkanıklık İçin Kimi Aramalı?", "kimi_ara"),
  ("{ad} Gider Açma Servisi Telefon Numarası", "telefon_gider"),
  ("{loc} Acil Tesisatçı Numarası", "acil_numara"),
 ],
 # ── Yakınlık / varış süresi niyeti ──
 "yakin": [
  ("{ad} En Yakın Tıkanıklık Servisi", "yakin"),
  ("{ad} En Yakın Tıkanıklık Açma Ekibi", "yakin_ekip"),
  ("{loc} En Hızlı Tıkanıklık Servisi Nasıl Bulunur?", "hizli"),
  ("{ad} Acil Tıkanıklık Açma", "acil"),
  ("{loc} 7/24 Tıkanıklık Açma", "yedi24"),
  ("{ad} Yakınımdaki Tıkanıklık Açma Servisi", "yakinimda"),
 ],
 # ── Mutfak ──
 "mutfak": [
  ("{ad} Mutfak Tıkanıklığı Açma", "mutfak"),
  ("{ad} Mutfak Gideri Tıkanıklığı Açma", "mutfak"),
  ("{loc} Tıkalı Mutfak Gideri Açma", "mutfak"),
  ("{ad} Mutfak Lavabosu Tıkanıklığı Açtırma", "mutfak"),
 ],
 # ── Lavabo ──
 "lavabo": [
  ("{ad} Lavabo Tıkanıklığı Açma", "lavabo"),
  ("{loc} Tıkalı Lavabo Gideri Açtırma", "lavabo"),
  ("{ad} Lavabo Gideri Açma", "lavabo"),
  ("{ad} Banyo Lavabosu Tıkanıklığı Açma", "lavabo"),
 ],
 # ── Tuvalet / klozet ──
 "tuvalet": [
  ("{ad} Tuvalet Tıkanıklığı Açma", "tuvalet"),
  ("{ad} Klozet Tıkanıklığı Açma", "klozet"),
  ("{loc} Tıkalı Tuvalet Gideri Açma", "tuvalet"),
  ("{ad} Klozet ve Tuvalet Tıkanıklığı Açtırma", "klozet"),
 ],
 # ── Banyo / yer süzgeci ──
 "banyo": [
  ("{ad} Banyo Tıkanıklığı ve Gideri Açma", "banyo"),
  ("{ad} Banyo Gideri Tıkanıklığı Açma", "banyo"),
  ("{loc} Tıkalı Banyo Gideri Açtırma Ustası", "banyo"),
  ("{ad} Duş ve Küvet Gideri Açma", "banyo"),
 ],
 # ── Gider açma odaklı ──
 "gider": [
  ("{ad} Tıkalı Gider Açma", "gider"),
  ("{ad} Gider Açma Hizmeti", "gider"),
  ("{loc} Gider Açma Nasıl Yapılır?", "gider_nasil"),
  ("{ad} Ana Gider Tıkanıklığı Açma", "anagider"),
  ("{ad} Bina Ana Gideri ve Kolon Açma", "anagider"),
  ("{loc} Logar ve Rögar Tıkanıklığı Açma", "logar"),
 ],
 # ── Yöntem / ekipman ──
 "yontem": [
  ("{loc} Kırmadan Tıkanıklık Açma", "kirmadan"),
  ("{ad} Kameralı Tıkanıklık Tespiti", "kamera"),
  ("{loc} Robotla Tıkanıklık Açma", "robot"),
  ("{ad} Pimaş Yıkama ve Görüntüleme", "pimas"),
  ("{loc} Kanal ve Kanalizasyon Açma", "kanal"),
]}

# İlçe sayfasının kapanış H2'si — ters kelime sırası (kullanıcının
# "Tıkanıklık açma servisi Esenyurt" örneği).
H2_KAPANIS = [
  ("Tıkanıklık Açma Servisi {ad}", "kapanis"),
  ("Gider Açma Servisi {ad}", "kapanis"),
  ("Tıkanıklık Açma {ad} — Çalışma Şeklimiz", "kapanis"),
  ("Su Tesisatçısı {ad}", "kapanis"),
]

# İlçe sayfasının teknik bölümü — başlık ilçenin KARAKTERİNDEN kuruluyor,
# şablondan değil. Bu bölüm 39 sayfada birbirine benzemeyen tek bölüm.
H2_ILCE_OZEL = "{loc} Tıkanıklığın En Sık Sebebi Ne?"


# ── Hizmetler ───────────────────────────────────────────────────────────────
# ⛔ Sayfa sayısı bilinçli DAR tutuldu. Referans sitedeki 28 hizmet sayfasının
#    bir kısmı aynı işin eşanlamlısıydı ("kanal açma" / "boru açma" /
#    "tıkalı gider açma" / "gider açma"). Google'ın rehberi: varyasyon için
#    değil, AYRI NİYET için sayfa aç. Eşanlamlılar ilgili sayfanın İÇİNDE geçiyor.
#
#   tip: "pillar" = ana küme sayfası · "hizmet" = alt hizmet
#   es  : sayfa içinde geçecek eşanlamlı/varyant kelimeler (ayrı sayfa AÇILMAZ)
HIZMETLER = [
 {"slug":"tikaniklik-acma","ad":"Tıkanıklık Açma","tip":"pillar","ikon":"dalga",
  "ozet":"Lavabo, tuvalet, mutfak ve ana gider tıkanıklıklarında kırmadan, kameralı teşhisle kalıcı çözüm.",
  "es":["tıkanıklık açma servisi","tıkanıklık açtırma","tıkanıklık açtırmak","tıkanıklık ustası","tıkanıklık giderme"]},

 {"slug":"gider-acma","ad":"Gider Açma","tip":"pillar","ikon":"gider",
  "ozet":"Tıkalı gideri, hangi noktada tıkandığını bulup boruya zarar vermeden açıyoruz.",
  "es":["tıkalı gider açma","gider açtırma","boru açma","kanal açma","pis su gideri açma"]},

 {"slug":"lavabo-tikanikligi-acma","ad":"Lavabo Tıkanıklığı Açma","tip":"hizmet","ikon":"lavabo",
  "ozet":"Saç, sabun ve yağ artığıyla dolan lavabo giderini sifon sökmeden açıyoruz.",
  "es":["lavabo gideri açma","tıkalı lavabo açma","lavabo açtırma"]},

 {"slug":"tuvalet-tikanikligi-acma","ad":"Tuvalet Tıkanıklığı Açma","tip":"hizmet","ikon":"tuvalet",
  "ozet":"Taşan tuvalet ve klozet giderlerini fayans kırmadan, çelik yaylı robotla açıyoruz.",
  "es":["klozet tıkanıklığı açma","tıkalı tuvalet açma","hela taşı açma","tuvalet açtırma"]},

 {"slug":"mutfak-gideri-tikanikligi-acma","ad":"Mutfak Gideri Tıkanıklığı Açma","tip":"hizmet","ikon":"mutfak",
  "ozet":"Donmuş yağ ve yemek artığıyla kapanan mutfak pimaşını basınç ve robotla temizliyoruz.",
  "es":["mutfak tıkanıklığı açma","mutfak lavabosu açma","tıkalı mutfak gideri"]},

 {"slug":"banyo-gideri-tikanikligi-acma","ad":"Banyo Gideri Tıkanıklığı Açma","tip":"hizmet","ikon":"banyo",
  "ozet":"Duş, küvet ve yer süzgeci tıkanıklıklarını seramiği kırmadan çözüyoruz.",
  "es":["banyo tıkanıklığı açma","duş gideri açma","yer süzgeci açma","küvet gideri açma"]},

 {"slug":"ana-gider-tikanikligi-acma","ad":"Ana Gider Tıkanıklığı Açma","tip":"hizmet","ikon":"bina",
  "ozet":"Tüm binayı etkileyen ana kolon ve bina çıkış hattı tıkanıklıklarında endüstriyel müdahale.",
  "es":["bina ana gideri açma","kolon açma","ana hat tıkanıklığı","apartman gideri açma"]},

 {"slug":"logar-tikanikligi-acma","ad":"Logar ve Rögar Açma","tip":"hizmet","ikon":"rogar",
  "ozet":"Logar, rögar ve bahçe hattı tıkanıklıklarında kök kesme ve basınçlı yıkama.",
  "es":["rögar açma","logar temizliği","bahçe gideri açma","kanalizasyon rögarı"]},

 {"slug":"pimas-yikama","ad":"Pimaş Yıkama","tip":"hizmet","ikon":"pimas",
  "ozet":"Bina pimaş hattını yüksek basınçlı su ile yıkayıp iç yüzeydeki tortu tabakasını söküyoruz.",
  "es":["pimaş temizliği","pimaş görüntüleme","pimaş tıkanıklığı açma","kolon yıkama"]},

 {"slug":"kanalizasyon-acma","ad":"Kanalizasyon Açma","tip":"hizmet","ikon":"kanal",
  "ozet":"Kök sarması, çökme ve katı atık kaynaklı ana hat tıkanıklıklarında kanal açma.",
  "es":["kanal açma","kanalizasyon tıkanıklığı","pis su hattı açma","vidanjor"]},

 {"slug":"kamerali-tikaniklik-tespiti","ad":"Kameralı Tıkanıklık Tespiti","tip":"hizmet","ikon":"kamera",
  "ozet":"Fiber optik kamerayla tıkanıklığın yerini ve sebebini görerek tespit ediyoruz.",
  "es":["kameralı tespit","boru içi görüntüleme","kameralı gider açma","arıza tespiti"]},

 {"slug":"robotla-tikaniklik-acma","ad":"Robotla Tıkanıklık Açma","tip":"hizmet","ikon":"robot",
  "ozet":"Çelik yaylı robot makineyle boruyu zorlamadan tıkanıklığı parçalayıp temizliyoruz.",
  "es":["makineyle tıkanıklık açma","spiral makine","cihazla tıkanıklık açma"]},

 {"slug":"kirmadan-tikaniklik-acma","ad":"Kırmadan Tıkanıklık Açma","tip":"hizmet","ikon":"kalkan",
  "ozet":"Fayans, seramik ve duvar kırmadan; mevcut giriş noktalarından çalışıyoruz.",
  "es":["kırmadan gider açma","kırmadan açma","hasarsız tıkanıklık açma"]},

 {"slug":"su-kacagi-tespiti","ad":"Kameralı Su Kaçağı Tespiti","tip":"hizmet","ikon":"kamera",
  "ozet":"Duvar ve zemini kırmadan, cihazla su kaçağının tam yerini tespit ediyoruz.",
  "es":["kamerayla su kaçağı tespiti","su kaçağı bulma","kaçak tespiti","noktasal tespit"]},

 {"slug":"acil-tikaniklik-acma","ad":"Acil Tıkanıklık Açma","tip":"hizmet","ikon":"simsek",
  "ozet":"Su taşması ve geri tepme gibi bekleyemeyecek durumlarda 7/24 acil müdahale.",
  "es":["acil tesisatçı","7/24 tesisatçı","gece tesisatçı","acil gider açma"]},
]

# Menüde öne çıkacak hizmetler (slug)
MENU_HIZMET = ["tikaniklik-acma","gider-acma","lavabo-tikanikligi-acma",
               "tuvalet-tikanikligi-acma","mutfak-gideri-tikanikligi-acma",
               "ana-gider-tikanikligi-acma","kamerali-tikaniklik-tespiti",
               "acil-tikaniklik-acma"]

# Anasayfadan ilçe sayfalarına dağıtılan anchor metinleri.
# ⚠️ Tek tip tam eşleşme anchor aşırı optimizasyon sinyali — rotasyonla dağıtılıyor.
ANA_ANCHOR = [
  "İstanbul tıkanıklık açma",
  "tıkanıklık açma servisi",
  "İstanbul gider açma",
  "tıkalı gider açma",
  "İstanbul tıkanıklık açma ustası",
  "7/24 tıkanıklık açma",
]


# ── Fiyat listesi ───────────────────────────────────────────────────────────
# ⚠️ TEK KAYNAK: fiyat değişince SADECE burası düzenlenir; sayfa, şema, kartlar
#    ve SSS hepsi buradan üretilir. ⛔ HTML'e elle rakam yazma.
# ✅ Rakamlar kullanıcının 2026-09-18'de bizzat verdiği gerçek fiyat listesi.
#    ⛔ Buraya UYDURMA kalem/rakam ekleme — "yerinde tespit" diyen satırlar
#    bilerek rakamsız; olmayan bir fiyatı yazmak Ticari Reklam Yönetmeliği'nde
#    yanıltıcı ticari uygulama sayılır.
# ⚠️ Hedef kelimeler (kullanıcı verdi): tıkanıklık açma fiyatları · gider açma
#    fiyatları · tıkanıklık açma ücreti · gider açma ücreti. Dördü de TEK
#    sayfada toplanıyor — ayrı "ücret" sayfası açmak kannibalizasyon olurdu.
FIYAT = {
    "slug":  "tikaniklik-acma-fiyatlari",
    "ad":    "Tıkanıklık Açma Fiyatları",
    "h1":    "Tıkanıklık Açma ve Gider Açma Fiyatları",
    "ozet":  "Tuvalet, lavabo ve banyo gideri tıkanıklıklarında güncel fiyat aralıklarımız, "
             "fiyatı değiştiren durumlar ve ücretin nasıl belirlendiği.",
    "giris": "Tessa Tesisat'ta gider açma hizmetlerinde fiyatlandırma, tıkanıklığın bulunduğu "
             "bölgeye, tıkanıklığın seviyesine ve kullanılacak ekipmana göre belirlenmektedir. "
             "Aşağıdaki fiyatlar standart tıkanıklıklar için temel fiyat aralıklarını "
             "göstermektedir.",
    "not":   "Fiyatlar hizmetin kapsamına ve tıkanıklığın durumuna göre değişebilir. Kesin "
             "ücret, gerekli müdahale belirlendikten sonra netleştirilir.",
    "para":  "TRY",
}
FIYAT_SLUG_YER = FIYAT["slug"]

# Kalemler — kart olarak basılır. "hizmet": ilgili hizmet sayfasının slug'ı (iç link).
FIYAT_KALEM = [
 {"ad":"Tuvalet Tıkanıklığı", "ikon":"tuvalet", "hizmet":"tuvalet-tikanikligi-acma",
  "aralik":"2.500 TL – 3.000 TL", "alt":2500, "ust":3000,
  "ozet":"Standart tuvalet gideri tıkanıklıklarının açılması için uygulanan fiyat aralığıdır.",
  "durum":[
    ("Hafif ve yüzeysel tıkanıklık",   "2.500 TL'den başlayan fiyatlarla"),
    ("Orta seviyeli tıkanıklık",       "2.750 TL civarı"),
    ("Zor ve derin tıkanıklık",        "3.000 TL'ye kadar"),
    ("Yabancı cisim kaynaklı tıkanıklık", "Tıkanıklığın durumuna göre fiyatlandırılır"),
    ("Ana gider hattı problemi",       "Yerinde tespit sonrası ayrıca fiyatlandırılır"),
    ("Kamera ile gider kontrolü",      "İhtiyaç halinde ayrıca değerlendirilir"),
  ]},

 {"ad":"Lavabo Tıkanıklığı", "ikon":"lavabo", "hizmet":"lavabo-tikanikligi-acma",
  "aralik":"2.000 TL – 2.500 TL", "alt":2000, "ust":2500,
  "ozet":"Mutfak ve lavabo giderlerinde oluşan standart tıkanıklıklar için temel fiyat aralığıdır.",
  "durum":[
    ("Hafif lavabo tıkanıklığı",       "2.000 TL'den başlayan fiyatlarla"),
    ("Orta seviyeli tıkanıklık",       "2.250 TL civarı"),
    ("Yoğun veya derin tıkanıklık",    "2.500 TL'ye kadar"),
    ("Yağ ve yemek artığı kaynaklı tıkanıklık", "Tıkanıklığın seviyesine göre"),
    ("Sifon ve gider bağlantısı problemi", "Yerinde kontrol sonrası belirlenir"),
    ("Ana gider hattı tıkanıklığı",    "Ayrı değerlendirme yapılır"),
    ("Kamera ile tesisat kontrolü",    "Gerektiğinde ayrıca fiyatlandırılır"),
  ]},

 {"ad":"Banyo Gideri Tıkanıklığı", "ikon":"banyo", "hizmet":"banyo-gideri-tikanikligi-acma",
  "aralik":"2.000 TL – 2.500 TL", "alt":2000, "ust":2500,
  "ozet":"Banyo, duş ve zemin giderlerinde oluşan standart tıkanıklıklar için uygulanabilecek "
         "fiyat aralığıdır.",
  "durum":[
    ("Hafif saç ve kıl birikmesi",     "2.000 TL'den başlayan fiyatlarla"),
    ("Orta seviyeli gider tıkanıklığı","2.250 TL civarı"),
    ("Derin ve yoğun tıkanıklık",      "2.500 TL'ye kadar"),
    ("Sabun ve tortu birikmesi",       "Tıkanıklığın durumuna göre"),
    ("Gider borusunun derin bölümündeki tıkanıklık", "Yerinde kontrol edilir"),
    ("Ana gider hattı tıkanıklığı",    "Ayrı fiyatlandırılır"),
    ("Kamera ile gider görüntüleme",   "İhtiyaç halinde ayrıca değerlendirilir"),
  ]},
]

# "Fiyatı Belirleyen Ek Unsurlar" tablosu — (işlem/durum, fiyatlandırma)
FIYAT_TABLO = [
 ("Standart lavabo tıkanıklığı",          "2.000 – 2.500 TL"),
 ("Standart banyo gideri tıkanıklığı",    "2.000 – 2.500 TL"),
 ("Standart tuvalet tıkanıklığı",         "2.500 – 3.000 TL"),
 ("Derin gider tıkanıklığı",              "Ana fiyat aralığı içinde / durumuna göre"),
 ("Yoğun yağ ve tortu birikmesi",         "Ana fiyat aralığı içinde / durumuna göre"),
 ("Yabancı cisim kaynaklı tıkanıklık",    "Yerinde tespit"),
 ("Ana gider hattı tıkanıklığı",          "Yerinde tespit"),
 ("Kamera ile tesisat görüntüleme",       "İhtiyaç halinde ayrıca fiyatlandırılır"),
 ("Tesisat kaynaklı yapısal problem",     "Tespit sonrası ayrıca fiyatlandırılır"),
]


# Fiyat sayfası gövdesi.
# ⚠️ Kullanıcının verdiği metin AYNEN korundu (giriş, "Fiyatlandırma Nasıl
#    Yapılır?", not). Etrafındaki bölümler kullanıcının ağzından ghostwrite —
#    kullanıcı "içerikler zengin olmalı" dedi.
# ⛔ Bu bölümlerde YENİ RAKAM YOK. Fiyat yalnızca FIYAT_KALEM / FIYAT_TABLO'dan
#    gelir; anlatıma rakam sızdırmak ikinci bir "fiyat kaynağı" yaratır.
FIYAT_GOVDE_UST = [
 ("h2","Fiyatı Belirleyen Ek Unsurlar"),
 ("p","Bazı tıkanıklıklarda standart gider açma işleminin dışında ek işlem veya ekipman "
      "gerekebilir. Bu nedenle kesin fiyat, tıkanıklığın durumuna göre belirlenir."),
]

FIYAT_GOVDE_ALT = [
 ("h2","Fiyatlandırma Nasıl Yapılır?"),
 ("p","Tessa Tesisat'ta fiyat belirlenirken öncelikle tıkanıklığın hangi giderde olduğu, "
      "ne kadar ileride bulunduğu, tıkanıklığa neden olan madde ve kullanılacak müdahale "
      "yöntemi değerlendirilir."),
 ("p","Standart tıkanıklıklarda fiyatlar yukarıdaki aralıklar içerisindedir. Daha kapsamlı bir "
      "işlem gerektiğinde, yapılacak ek işlem ve varsa ekipman kullanımı müşteriye belirtilerek "
      "fiyatlandırma yapılır."),

 ("h2","Tıkanıklık Açma Ücreti Neye Göre Değişiyor?"),
 ("p","Aynı işe iki farklı ücret çıkmasının sebebi keyfîlik değil; giderin kendisi. Fiyatı "
      "yukarı ya da aşağı çeken şeyler pratikte şunlar:"),
 ("ul",[
   ("Tıkanıklığın yeri","Sifonun hemen altındaki bir tıkaçla, kolona bağlanan noktadaki tıkaç "
    "aynı iş değil. Hat uzadıkça makine değişiyor, süre uzuyor."),
   ("Tıkanıklığın cinsi","Saç ve sabun tortusu mekanik olarak kolay çıkar. Donmuş yağ, kireç "
    "kabuğu, inşaat harcı veya kök sarması aynı kolaylıkta çıkmaz."),
   ("Kullanılan ekipman","Elde açılan bir gider ile çelik yaylı robot makine ya da yüksek "
    "basınçlı yıkama gereken bir hat arasında fark var."),
   ("Erişim noktası","Temizleme kapağı açıktaysa iş kısa sürer. Kapak yoksa, dolabın içinden "
    "ya da rögardan çalışmak gerekiyorsa süre uzar."),
   ("Daire içi mi, bina hattı mı","Fiyatı en çok değiştiren ayrım bu. Aşağıda ayrı başlık "
    "altında anlattık."),
 ]),

 ("h2","Telefonda Neden Kesin Rakam Söylemiyoruz?"),
 ("p","Söyleyebilseydik söylerdik. Ama telefonda duyduğumuz şey çoğu zaman \u201clavabo "
      "gitmiyor\u201d oluyor; giderin içinde ne olduğunu ne siz görüyorsunuz ne biz. "
      "Sahada aynı cümleyle gittiğimiz iki adresten birinde iş on beş dakikada bitiyor, "
      "diğerinde kolonda kireç kabuğu çıkıyor."),
 ("p","Bu yüzden telefonda size <b>aralık</b> söylüyoruz: yukarıdaki tablo, standart bir işin "
      "hangi bandın içinde kalacağını baştan gösteriyor. Ekip yerinde gördükten sonra, işe "
      "başlamadan önce net rakamı söylüyor. Onaylamazsanız iş yapılmıyor."),
 ("uyari","<b>Şuna dikkat edin:</b> telefonda tereddütsüz \u201cçok ucuz\u201d bir rakam "
          "veren kimse o rakamı görmüyor. Kapıya gelince \u201cbu başka iş\u201d denip "
          "fiyat katlanıyor. Biz de kapıda sürpriz sevmediğimiz için aralığı buraya, "
          "herkesin görebileceği bir sayfaya yazdık."),

 ("h2","Gider Açma Ücretinde Nelere Dikkat Etmelisiniz?"),
 ("ul",[
   ("Fiyat işe başlamadan konuşulsun","Makine gidere girdikten sonra pazarlık yapılmaz. "
    "Net rakamı duymadan onay vermeyin — bu bizim için de geçerli."),
   ("Neyin dahil olduğu net olsun","Açma işlemi mi, kamerayla kontrol mü, ikisi birden mi? "
    "Kamera her işte gerekmiyor; gerekmediği yerde ücret de çıkmamalı."),
   ("Kırma konusu baştan sorulsun","Standart bir tıkanıklıkta fayans kırılması gerekmiyor. "
    "Kırma teklif eden biri varsa önce sebebini kamerayla göstermesini isteyin."),
   ("Tekrarlayan tıkanıklıkta ısrar etmeyin","Aynı gider kısa aralıklarla tekrar tıkanıyorsa "
    "sorun tıkaçta değil hattın kendisinde. Üst üste açtırmak, bir kez doğru teşhisten "
    "pahalıya geliyor."),
 ]),

 ("h2","Daire İçi Tıkanıklık mı, Bina Ana Gideri mi?"),
 ("p","Fiyatı en çok değiştiren ayrım bu. Tek bir gider yavaşladıysa iş büyük ihtimalle o "
      "giderin kendi hattında; yukarıdaki standart aralıklar geçerli. Evdeki birkaç gider "
      "aynı anda taşıyorsa ya da alt kattaki komşuda da aynı sorun varsa bina kolonundan "
      "şüpheleniyoruz; orası ayrı bir iş ve yerinde görülmeden fiyatlanmıyor."),
 ("p","Bina hattı söz konusuysa masrafın ortak alana mı daireye mi ait olduğu da ayrı bir "
      "konu. Sokaktaki ana kanalizasyon şebekesi ise zaten İSKİ'nin işi — parsel içi ile "
      "sokak arasındaki sınırı ilçe sayfalarımızda tablo hâlinde anlattık."),

 ("h2","Kamera Her İşte Gerekiyor mu?"),
 ("p","Hayır. Standart bir lavabo ya da banyo gideri tıkanıklığında kamera gerekmiyor; iş "
      "açılır, biter. Kamerayı şu üç durumda öneriyoruz: aynı gider kısa sürede tekrar "
      "tıkanıyorsa, tıkanıklık makineyle açılmıyorsa, ya da hattın çökmüş/kırılmış olduğundan "
      "şüpheleniyorsak."),
 ("p","Kamera gerekmeyen bir işte kamera ücreti çıkarmıyoruz. Gerektiğinde de neden "
      "gerektiğini ekranda birlikte görüyorsunuz."),

 ("h2","Fiyatlar İlçeye Göre Değişiyor mu?"),
 ("p","Hayır. Yukarıdaki aralıklar İstanbul'un 39 ilçesinin tamamında aynı. Adres uzak diye "
      "fiyat yükseltmiyoruz; ekip hangi ilçeye giderse gitsin standart iş standart bandın "
      "içinde kalıyor."),

 ("h2","Ev Yöntemlerini Denemek Ücreti Düşürür mü?"),
 ("p","Gider sadece <b>yavaşladıysa</b> denemeye değer — bazı yöntemlerin gerçekten bir "
      "etkisi var ve iş bize hiç düşmeyebilir. Ama su hiç gitmiyorsa ya da geri geliyorsa "
      "tıkaç oturmuş demektir; o aşamada dökülen kimyasal tıkanıklığı çıkarmıyor, sadece "
      "hattın içinde bekliyor ve biz geldiğimizde işi zorlaştırıyor."),
]

# ── Videolar ────────────────────────────────────────────────────────────────
# ⚠️ Kullanıcı 2026-09-18'de 4 dosya yükledi. 5. dosya (tikaniklik-acma.mp4)
#    GELMEDİ — o kayıt listeden çıkarıldı, yoksa anasayfa videosuz kalıyordu.
# ⚠️ Videolar DİKEY (9:16 reels, 464×832 / 576×1024) — yatay 16/10 kutuda
#    kırpılıyorlardı. Bölüm dikey şerit olarak kuruldu.
# ⚠️ Başlık/alt metinler videonun GERÇEK karesinden yazıldı; poster
#    `videos/<ad>.jpg` olarak media.py üretir (postersiz <video> mobilde
#    siyah kutu gösteriyor).
VIDEOLAR = [
 {"dosya":"gider-acma",
  "baslik":"Yer süzgeci gideri açılırken",
  "alt":"Tıkalı yer süzgeci giderine spiral makine ve çelik yayla müdahale",
  "sayfa":["", "gider-acma", "banyo-gideri-tikanikligi-acma", "robotla-tikaniklik-acma",
           "acil-tikaniklik-acma", FIYAT_SLUG_YER]},

 {"dosya":"lavabo-gideri-acma",
  "baslik":"Mutfak lavabosu gideri açılırken",
  "alt":"Mutfak dolabının altındaki gider ağzından basınçlı hortumla çalışma",
  "sayfa":["", "lavabo-tikanikligi-acma", "mutfak-gideri-tikanikligi-acma",
           "kirmadan-tikaniklik-acma", "lavabo-acma-yontemleri", FIYAT_SLUG_YER]},

 {"dosya":"tikali-gider-acma",
  "baslik":"Tıkalı giderden çıkan tortu",
  "alt":"Gider borusu sökülüp hattaki tortulu suyun kovaya alınması",
  "sayfa":["", "tikaniklik-acma", "ana-gider-tikanikligi-acma", "pimas-yikama",
           "kanalizasyon-acma", FIYAT_SLUG_YER]},

 {"dosya":"tuvalet-tikanikligi-acma",
  "baslik":"Banyo giderinden çıkan saç kütlesi",
  "alt":"Banyo ve tuvalet giderinden çıkarılan saç ve tortu birikintisi",
  "sayfa":["tuvalet-tikanikligi-acma", "banyo-gideri-tikanikligi-acma",
           "kamerali-tikaniklik-tespiti", FIYAT_SLUG_YER]},
]

# ── Sık sorulan sorular ─────────────────────────────────────────────────────
# ⚠️ Cevaplarda süre/fiyat TAAHHÜDÜ yok — teyit edilmemiş rakam yazılmıyor.
SSS_GENEL = [
 ("Tıkanıklık açma ne kadar sürer?",
  "Lavabo, klozet ve banyo gideri gibi daire içi tıkanıklıklar çoğunlukla tek ziyarette çözülür. "
  "Bina ana kolonu veya bahçe hattı söz konusuysa önce kamerayla tıkanıklığın yeri bulunur; "
  "süre, tıkanıklığın cinsine ve hattın uzunluğuna göre değişir. Ekip yerinde gördükten sonra "
  "size net bir süre söyler."),
 ("Fayans veya seramik kırmanız gerekir mi?",
  "Hayır. Çalışmanın tamamı mevcut giriş noktalarından — gider ağzı, rögar, temizleme kapağı veya "
  "klozet çıkışından — yapılır. Kırma yalnızca boruda çökme ya da kırılma varsa gündeme gelir; "
  "o durumda da kamerayla tam noktayı gösterip sizin onayınızı almadan hiçbir yere dokunmayız."),
 ("Kimyasal döküyor musunuz?",
  "Tıkanıklığı açmak için kimyasal kullanmıyoruz. Piyasadaki güçlü çözücüler tıkanıklığı çoğu zaman "
  "geçici olarak deler, asıl kütle yerinde kalır; üstelik eski döküm ve PVC boruların iç yüzeyine "
  "zarar verir. Biz mekanik yöntemle — robot makine ve basınçlı su — tıkanıklığı parçalayıp "
  "hattan uzaklaştırıyoruz."),
 ("Gece veya hafta sonu geliyor musunuz?",
  "Evet, 7/24 acil müdahale veriyoruz. Su taşması, geri tepme ve koku gibi bekleyemeyecek "
  "durumlarda saat fark etmeksizin arayabilirsiniz."),
 ("Tıkanıklığın daire içinde mi binada mı olduğunu nasıl anlarım?",
  "Pratik bir kontrol: tıkanıklık yalnızca bir musluk ya da bir gidere mi ait, yoksa evdeki birden "
  "fazla gider aynı anda mı yavaşladı? Tek nokta ise sorun büyük ihtimalle o giderin kendi hattında. "
  "Birden fazla gider birlikte taşıyorsa ya da alt kattaki komşuda da aynı sorun varsa bina "
  "kolonundan şüphelenmek gerekir. Emin değilseniz telefonda birkaç soruyla birlikte ayırt ederiz."),
 ("Aynı tıkanıklık tekrar ederse ne oluyor?",
  "Aynı noktada kısa süre içinde tekrar eden tıkanıklık, genelde tıkanıklığın değil hattın kendisinin "
  "sorunlu olduğunu gösterir: çökme, ters eğim, kök sarması veya kırık. Bu yüzden tekrar eden "
  "işlerde hattı kamerayla görüntüleyip sebebi net olarak ortaya koyuyoruz — sürekli açtırmak "
  "yerine bir kez doğru işi yapmak daha ucuza geliyor."),
]


# ── Hizmet sayfası gövdeleri ────────────────────────────────────────────────
# Kullanıcı 2026-09-18'de "neden tıkanır" anlatımlarını gönderdi ve
# "%100 bana ait değil, benim dilimle çevirip ekleme yapabilirsin" dedi.
# ⚠️ Bu yüzden metinler AYNEN kullanılmadı — kaynak metin başka sitelerde de
#    duruyor olabilir; birebir kopyalamak yinelenen içerik demekti.
#    Yapı (sebep listesi + belirti paragrafı) korunup ifade baştan yazıldı,
#    üzerine sahadan gerçek ayrım ve dürüst uyarı eklendi.
#
# Blok biçimi: ("h2"|"h3"|"p", metin) · ("ul", [(kalın_etiket, açıklama), ...])
#              ("kutu", metin) · ("uyari", metin)
HIZMET_GOVDE = {

"lavabo-tikanikligi-acma": [
 ("h2", "Lavabo Neden Tıkanır?"),
 ("p", "Lavabo tıkanıklığı bir anda olmuyor. Gidere her gün kaçan küçük şeyler borunun iç çeperinde "
       "ince bir tabaka bırakıyor; o tabaka kalınlaştıkça su geçecek yer daralıyor. Bir sabah "
       "\"dün akıyordu, bugün akmıyor\" dediğiniz an aslında aylardır süren birikmenin son günü."),
 ("p", "Açtığımız lavabo giderlerinde en sık şunları buluyoruz:"),
 ("ul", [
  ("Yağ", "Mutfak lavabosunda en sık bulduğumuz şey. Tavadaki yağ sıcakken sıvı, boruya girip "
          "soğuyunca çepere yapışıyor. Üstüne çay posası, pirinç, makarna artığı geldikçe "
          "bir tıkaç hâline geliyor."),
  ("Çay posası", "Türkiye'ye özgü bir sorun.. Demliği lavaboya boşaltmak zararsız görünür ama "
                 "posa yağın üstüne tutunur ve tabakayı hızla kalınlaştırır."),
  ("Saç ve sabun", "Banyo lavabosunda yağın yerini bunlar alıyor. Saç tel tel gider, sabun "
                   "kalıntısı onları birbirine yapıştırıp keçe gibi bir kütle oluşturur."),
  ("Bez, süngerden kopan parça, kapak", "Temizlik sırasında farkında olmadan gidere kaçan bu "
                                        "cisimler tek başına suyu tamamen kesebilir."),
  ("Sifonun hiç sökülmemesi", "Lavabonun altındaki U şeklindeki sifon, kokuyu tutsun diye "
                              "sürekli su barındırır — ama aynı sebeple tortu da orada birikir."),
  ("Tesisatın kendisi", "Borunun eğimi yetersizse, bir yerde çökme ya da ters eğim varsa gider "
                        "temiz olsa bile su ilerlemez. Bunu ancak kamerayla görerek anlarsınız."),
 ]),
 ("p", "Suyun yavaşlaması, giderden koku gelmesi, lavaboda su göllenmesi ya da suyun geri "
       "tepmesi tıkanıklığın habercisidir. Aynı lavabo kısa aralıklarla tekrar tıkanıyorsa "
       "sorun lavaboda değil, hattın ilerisinde demektir."),
 ("uyari", "<b>Market kimyasalı dökmeyin.</b> Güçlü çözücüler tıkacın ortasında ince bir delik "
           "açar; su akmaya başlayınca sorun çözüldü sanırsınız, oysa kütle yerinde durur ve "
           "birkaç gün içinde geri kapanır. Üstelik o kimyasal hattın içinde bekler — biz "
           "açmaya geldiğimizde sıçrama riski yaratır. Döktüyseniz mutlaka söyleyin."),
 ("h3", "Lavabo Gideri Nasıl Açılır?"),
 ("p", "Önce sifonu söküp içini boşaltıyoruz; tıkanıklıkların azımsanmayacak bir kısmı orada "
       "bitiyor. Sifon temizse tıkanıklık daha ileride demektir: ince çaplı spiralle gider "
       "hattına giriyor, kütleyi parçalayıp dışarı alıyoruz. Gerekirse kamerayla hattın içine "
       "bakıp tıkanıklığın kaç metre ileride olduğunu ve boruda çökme olup olmadığını görüyoruz."),
],

"banyo-gideri-tikanikligi-acma": [
 ("h2", "Banyo Gideri Neden Tıkanır?"),
 ("p", "Banyo gideri tıkanıklığı neredeyse her zaman aynı iki maddeden çıkıyor: saç ve sabun. "
       "Saç tek başına akıp gidebilir, sabun tek başına da sorun çıkarmaz — ama ikisi birleşince "
       "boruya yapışan, elle bile zor koparılan keçemsi bir kütle oluşuyor."),
 ("ul", [
  ("Saç ve kıl", "Süzgeçten geçip borunun ilk dirseğinde takılır. Zamanla geçen her şeyi tutan "
                 "bir ağ hâline gelir."),
  ("Sabun, şampuan, duş jeli kalıntısı", "Boru çeperinde yağımsı bir film bırakır; saç bu filme "
                                          "tutunur. Kütlenin yapıştırıcısı budur."),
  ("Süzgecin hiç kaldırılmaması", "Süzgeç altındaki hazne çoğu evde yıllarca hiç açılmaz. "
                                  "Oysa tıkanıklığın büyük kısmı ilk 20 santimde durur."),
  ("Küvet ve duş teknesi giderindeki tıkaç mekanizması", "Açma-kapama düzeneğinin altı saç "
                                                         "toplamak için ideal bir yerdir."),
  ("Yabancı cisim", "Şampuan kapağı, jilet başlığı, çocuk oyuncağı.. Banyoda gidere düşen şey "
                    "genelde geri alınmaz ve orada kalır."),
  ("Boru eğimi ve çökme", "Özellikle zemin altındaki yatay hatta eğim kaybı varsa su gitmekte "
                          "zorlanır. Tıkanıklık temizlense de sorun tekrar eder."),
  ("Ana kolon", "Banyoyla birlikte mutfak ve tuvalet de yavaşladıysa ya da alt komşuda aynı "
                "sorun varsa, arıza dairede değil bina kolonundadır."),
 ]),
 ("p", "Duş alırken suyun ayağınızın altında birikmesi, giderden koku gelmesi ya da yer "
       "süzgecinden suyun geri çıkması tıkanıklığın belirtisidir. Yer süzgecinden <b>gri, köpüklü "
       "su geri geliyorsa</b> bu artık daire içi bir tıkanıklık değildir — bina hattına bakmak gerekir."),
 ("h3", "Banyo Gideri Açma Nasıl Yapılır?"),
 ("p", "Seramiği kırmadan çalışıyoruz. Süzgeci ve varsa tıkaç düzeneğini söküp hazneyi "
       "boşaltıyoruz; sorun devam ediyorsa yer süzgecinden spiralle hatta giriyoruz. Küvet ve "
       "duş teknelerinde taşma deliğinden de erişim mümkün oluyor. Tıkanıklık yatay hatta "
       "ilerideyse kamerayla yerini bulup basınçlı su ile çeperdeki tabakayı da söküyoruz — "
       "sadece delik açmak kısa ömürlü bir çözüm."),
],

"tuvalet-tikanikligi-acma": [
 ("h2", "Tuvalet ve Klozet Neden Tıkanır?"),
 ("p", "Tuvalet tıkanıklığı diğerlerinden bir yönüyle ayrılıyor: burada sebep çoğunlukla "
       "birikme değil, <b>gidere ait olmayan bir şeyin atılması</b>. Yani tek seferde oluyor ve "
       "genelde ne olduğunu ev sahibi biliyor.. Söylemekten çekinmeyin, işimizi kolaylaştırır."),
 ("ul", [
  ("Islak mendil", "Bugün açtığımız tuvalet tıkanıklıklarının başında bu geliyor. Ambalajında "
                   "\"suda çözünür\" yazsa bile tuvalet kâğıdı gibi dağılmıyor; boruda açılıp "
                   "bir bez gibi hattı kapatıyor."),
  ("Ped, tampon, bebek bezi", "Suyla temas edince kat kat şişmek üzere üretilmiş ürünler. "
                              "Boruda da aynısını yapıyorlar."),
  ("Kâğıt havlu ve peçete", "Tuvalet kâğıdı suda dağılsın diye üretilir, kâğıt havlu ise tam "
                            "tersi — ıslanınca dağılmasın diye. Gidere atılınca çözünmüyor."),
  ("Fazla tuvalet kâğıdı", "Tek seferde çok miktarda kâğıt, özellikle dar çaplı ve dirsekli "
                           "hatlarda topaklanıp sıkışabiliyor."),
  ("Düşen cisim", "Cep telefonu, oyuncak, temizlik ürünü kapağı, koku bloğu.. Sifonu "
                  "çektiğinizde bunlar gözden kaybolur ama hattın ilk dirseğinde durur."),
  ("Kireç ve tortu", "Eski binalarda boru çeperinde yıllar içinde biriken tabaka iç çapı "
                     "daraltır; o daralmış çapta artık normal kullanım bile tıkanmaya yeter."),
  ("Kırık, çökme, ters eğim", "Hattın kendisi bozuksa tıkanıklık sürekli tekrar eder. "
                              "Böyle durumlarda açmak yetmez, hattı görmek gerekir."),
  ("Ana gider hattı", "Evdeki birden fazla gider aynı anda geri tepiyorsa sorun klozette değil, "
                      "binanın ana hattındadır."),
 ]),
 ("uyari", "<b>Klozet taşıyorsa sifonu tekrar çekmeyin.</b> En sık yapılan hata bu. İkinci "
           "sifon, tıkanıklığı açmaz ama hazne dolusu suyu taşan klozete ekler — zemine yayılan "
           "suyun çoğu bu şekilde oluşuyor. Sifonu çekmeyi bırakın, rezervuarın ara musluğunu "
           "kapatın ve bizi arayın."),
 ("h3", "Tuvalet Tıkanıklığı Nasıl Açılır?"),
 ("p", "Klozeti sökmeden, çelik yaylı robot makineyle klozet çıkışından hatta giriyoruz. Makinenin "
       "ucu tıkacı parçalıyor ya da yabancı cismi kavrayıp geri çekiyor. Fayans veya seramik "
       "kırmak gerekmiyor; kırma yalnızca boruda çökme ya da kırık varsa gündeme geliyor ve o "
       "durumda da önce kamerayla tam noktayı gösterip onayınızı alıyoruz."),
],
}


# ── Rehber sayfaları ────────────────────────────────────────────────────────
# ⚠️ Kullanıcının Google Ads arama terimi raporundan (2026-09-18) doğdu:
#    "bulaşık tableti ile lavabo açma", "limon tuzu lavabo açar mı",
#    "kaya tuzu lavabo açar mı", "lavabo açma aparatı", "gider açma sustası",
#    "gider temizleyici", "lavabo açıcısı", "klozet açma aparatı",
#    "pis su gideri açma aparatı" — yani ücretli trafiğin ciddi bir kısmı
#    "kendim açayım" niyetinde. Bu sorulara DÜRÜST cevap veren tek bir güçlü
#    sayfa, o trafiği organik karşılıyor ve deneyip başaramayanı müşteriye
#    çeviriyor.
# ⛔ Her ev yöntemi için AYRI sayfa AÇMA — hepsi tek niyet ("kendim açabilir
#    miyim?"). Varyasyon için sayfa açmak ölçeklendirilmiş içerik sayılır.
REHBERLER = [
{
 "slug":"lavabo-acma-yontemleri",
 "ad":"Lavabo ve Gider Açma Yöntemleri",
 "baslik":"Lavabo ve Gider Açma Yöntemleri: Hangisi İşe Yarıyor?",
 "ozet":"Bulaşık tableti, limon tuzu, kaya tuzu, karbonat, açma aparatı ve kimyasal açıcı — "
        "tesisatçı gözünden hangisi ne işe yarıyor, hangisi zaman kaybı?",
 "blok":[
 ("p","Tıkanıklık açmaya gelmeden önce insanların ne denediğini artık tahmin edebiliyoruz. "
      "Çoğu zaman aynı liste: karbonatla sirke, bulaşık tableti, kaya tuzu, marketten alınan "
      "gider açıcı.. Bir kısmı zararsız, bir kısmı işi büyütüyor. Hangisinin ne yaptığını "
      "olduğu gibi yazıyorum — işimize gelsin diye \"hiçbiri olmaz, bizi arayın\" demeyeceğim."),
 ("kutu","<b>Önce şunu ayırın:</b> Gider <b>yavaşladı</b> mı, yoksa <b>tamamen kapandı</b> mı? "
         "Yavaşlamış bir giderde ev yöntemlerinin bir şansı var — çeperdeki film tabakası "
         "henüz incedir. Su hiç gitmiyorsa ya da geri geliyorsa tıkaç oturmuş demektir; "
         "aşağıdakilerin hiçbiri onu çıkarmaz, sadece vakit kaybettirir."),

 ("h2","Bulaşık Tableti ile Lavabo Açma"),
 ("p","Bulaşık tableti alkali ve enzim içerir, yani <b>yağ çözme</b> tarafında gerçekten bir "
      "etkisi vardır. Sıcak suda eritip yavaşlamış bir mutfak giderine dökerseniz çeperdeki "
      "taze yağ filmini bir miktar inceltebilir ve kokuyu azaltır."),
 ("p","Ama sınırı şurası: tablet <b>yumuşak ve yeni</b> yağ tabakasına etki eder. Yıllardır "
      "birikmiş, içine çay posası ve yemek artığı girmiş sertleşmiş kütleye hiçbir şey yapmaz. "
      "Bir de tableti kuru kuru gidere atmayın — dibe oturup kendisi tıkaca eklenir."),

 ("h2","Limon Tuzu Lavabo Açar mı?"),
 ("p","Limon tuzu (sitrik asit) <b>kireç</b> çözer. Musluk ucundaki, duş başlığındaki beyaz "
      "kalıntı için iyidir. Lavabo giderindeki tıkanıklık ise kireç değil; saç, sabun ve yağdan "
      "oluşan <b>organik</b> bir kütledir. Sitrik asit ona etki etmez."),
 ("p","Kısa cevap: limon tuzu lavabo açmaz. Çok eski binalarda boru çeperinde kireç birikmesi "
      "varsa bile o tabakayı ev tipi bir çözeltiyle sökemezsiniz, o iş basınçlı yıkamanın konusu."),

 ("h2","Kaya Tuzu Lavabo Açar mı?"),
 ("p","Hayır. Kaya tuzu suda çözünür, bitti. Yağı çözmez, saçı parçalamaz, kireci sökmez. "
      "İnternette dolaşan \"kaya tuzu + sıcak su\" tarifinde işi yapan şey varsa o da sıcak "
      "sudur, tuz değil. Bu yöntemi denemenizin tek zararı zaman kaybı."),

 ("h2","Karbonat ve Sirke Karışımı"),
 ("p","En yaygın tarif bu ve görsel olarak en etkileyici olanı — köpürme insanı bir şeyler "
      "oluyor sanısına sokuyor. Oysa o köpük karbondioksit; borunun içinde tıkacı itecek bir "
      "basınç oluşturmuyor. Üstelik <b>asit ile bazı birbirine karıştırdığınız an ikisi de "
      "nötrleşiyor</b>, yani temizleme gücü olan iki maddeyi birbirine harcamış oluyorsunuz."),
 ("p","Giderde koku varsa faydası olabilir. Tıkanıklık açma yöntemi olarak sayılmaz."),

 ("h2","Gider Temizleyici ve Lavabo Açıcı Kimyasallar"),
 ("uyari","Marketten alınan güçlü gider açıcılar (sodyum hidroksit ya da sülfürik asit bazlı) "
          "işin en riskli tarafı. Tıkacın ortasında ince bir kanal açarlar; su akmaya başlar ve "
          "sorunun çözüldüğünü sanırsınız. Kütle yerinde durduğu için birkaç gün içinde geri kapanır."),
 ("p","Asıl mesele şu: o kimyasal boruda bekler. Eski döküm hatlarda ve conta bölgelerinde "
      "aşınma yapar; PVC'de sıcaklık yükselince deformasyona yol açabilir. Bir de bizim "
      "açısından: dökülen kimyasal hattın içinde dururken makineyle müdahale edildiğinde "
      "sıçrama riski oluşuyor."),
 ("kutu","<b>Kimyasal döktüyseniz mutlaka söyleyin.</b> Kızmak için sormuyoruz — koruyucu "
         "ekipmanla ve farklı bir sırayla çalışmamız gerekiyor. Saklanan tek bilgi bu ve "
         "gerçekten önemli."),

 ("h2","Tuz Ruhu, Kostik ve Kireç Sökücü — Buraya Dikkat"),
 ("uyari","Bu üçü diğerlerinden ayrı bir başlıkta, çünkü diğerleri işe yaramazken bunlar "
          "<b>zarar verebiliyor.</b> Tuz ruhu (hidroklorik asit) ve kostik (sodyum hidroksit) "
          "ciddi kimyasallar; evde gider açmak için kullanılacak maddeler değil."),
 ("ul",[
  ("Tuz ruhu lavaboyu açar mı","Açmaz. Organik tıkacı çözmez ama metal boruyu, contayı ve "
                               "eklerdeki yalıtımı aşındırır. Asıl tehlike şu: tuz ruhu, "
                               "çamaşır suyuyla temas ederse <b>klor gazı</b> açığa çıkarır. "
                               "Gidere önce biri sonra diğeri döküldüğünde bu kapalı banyoda olur."),
  ("Kostikle banyo gideri açma","Kostik suyla tepkimeye girerken ısınır. Dar bir giderde "
                                "kaynayıp <b>geri püskürebilir</b>; gözü ve cildi kalıcı olarak "
                                "yakar. PVC boruyu yumuşatır, döküm boruda aşınma yapar."),
  ("Kireç sökücü lavabo açar mı","Hayır. Kireç sökücü kirece çalışır; lavabo tıkanıklığı "
                                 "saç, sabun ve yağdan oluşur. Yanlış sorun için doğru ürün."),
  ("Market açıcıları ve dök-boşalt ürünleri","Etki mekanizmaları yukarıdakilerle aynı ailede. "
                                             "Yavaşlamış giderde bir miktar işe yarayabilir; "
                                             "oturmuş tıkaçta kanal açıp sorunu erteler."),
 ]),
 ("p","Bir de şu var: bu maddelerden biri gidere döküldükten sonra tıkanıklık açılmazsa, o "
      "kimyasal boruda bekliyor demektir. Biz makineyle müdahale ettiğimizde sıçrama olabilir. "
      "<b>Ne döktüğünüzü söyleyin</b> — koruyucu ekipmanla ve farklı bir sırayla çalışırız."),

 ("h2","Lavabo Açma Aparatı, Susta ve Spiral"),
 ("p","\"Lavabo açma sustası\", \"gider açma sustası\", \"pis su gideri açma aparatı\" diye "
      "aranan şey genelde 2–3 metrelik el spirali. Bu, listedeki yöntemler arasında <b>gerçekten "
      "işe yarayabilecek</b> olanı — çünkü mekanik. Giderin ilk dirseğinde duran saç kütlesini "
      "kavrayıp çıkarabilir."),
 ("p","Dikkat edilecek yerler var: aparatı zorlayarak itmeyin. Dirsekte takıldığında güç "
      "uygularsanız ucu boru çeperini çizebilir, ince PVC'de delebilir. Ucu koparsa içeride "
      "kalır ve o noktadan sonra iş kesinlikle bize kalır. Bir de el spirali sadece ilk birkaç "
      "metreye ulaşır; tıkanıklık yatay hatta ilerideyse fark etmezsiniz bile."),

 ("h2","Klozet Açma Aparatı ve Pompa"),
 ("p","Klozette lastik pompa mantıklı bir ilk adımdır — kâğıt kaynaklı hafif tıkanıklığı "
      "açabilir. Ama <b>yabancı cisim</b> düştüyse pompa işi büyütür: cismi daha ileri iter ve "
      "kolay erişilen bir noktadan erişilmesi zor bir noktaya taşır."),
 ("p","Klozet taşmışsa pompa kullanmayın, önce suyu azaltın. Ve sifonu tekrar tekrar çekmeyin — "
      "zemine yayılan suyun çoğu bu yüzden oluyor."),

 ("h2","Kaynar Su Dökmek"),
 ("p","Yağ kaynaklı mutfak tıkanıklığında sıcak suyun kısmi faydası vardır. Ama kaynar su "
      "PVC gider borusunda, özellikle ek yerlerinde ve contalarda yumuşamaya yol açabiliyor. "
      "Sıcak kullanacaksanız kaynar değil <b>çok sıcak musluk suyu</b> tercih edin. Klozette "
      "ise hiç yapmayın; seramik ani ısı farkıyla çatlayabilir."),

 ("h2","Ne Zaman Denemeyi Bırakıp Usta Çağırmalı?"),
 ("ul",[
  ("Su hiç gitmiyor ya da geri geliyor","Tıkaç oturmuş demektir. Ev yöntemleri bu aşamada "
                                        "vakit kaybı."),
  ("Birden fazla gider aynı anda yavaşladı","Sorun daire içinde değil, bina kolonunda. "
                                            "Daireden yapılan hiçbir müdahale çözmez."),
  ("Alt kattaki komşuda da aynı sorun var","Ana hat tıkanıklığının en net işareti."),
  ("Aynı gider kısa aralıklarla tekrar tıkanıyor","Tıkanıklık değil hattın kendisi sorunlu "
                                                 "olabilir: çökme, ters eğim, kök sarması. "
                                                 "Kamerayla bakmak gerekir."),
  ("Yer süzgecinden gri, köpüklü su çıkıyor","Pis su geri basıyor demektir; beklemeyin."),
  ("Gidere bir cisim düştü","İtmeyin. İttikçe erişimi zorlaşır."),
 ]),
 ("p","Bu durumların hiçbiri yoksa ve gider sadece yavaşladıysa, yukarıdakilerden mekanik "
      "olanı (el spirali) ve sıcak su denenebilir. Sonuç alamazsanız zorlamayın — "
      "yanlış müdahale çoğu zaman asıl işten daha pahalıya mal oluyor."),
 ],
},
]


# ── Kurum bilgileri (belediye / İSKİ) ───────────────────────────────────────
# ⚠️ Numaralar 2026-09-18'de İSKİ'nin resmî sayfasından DOĞRULANDI:
#    https://iski.istanbul/iletisim/alo-185/  → ALO 185, 7/24, şehir dışından
#    0212 185 00 00. İBB Beyaz Masa 153.
# ⛔ 39 ilçe belediyesinin çağrı merkezi numarası UYDURULMADI. İstanbul'da
#    kanalizasyon yetkisi ilçe belediyesinde değil İSKİ'dedir; ilçe belediyesini
#    aramak zaten doğru adres değil. Kullanıcı teyit edilmiş numara verirse
#    ILCELER içindeki "bel_tel" alanına eklenir ve metin otomatik gösterir.
KURUM = {
  "iski_ad":    "İSKİ (İstanbul Su ve Kanalizasyon İdaresi)",
  "iski_tel":   "185",
  "iski_tel_link": "185",
  "iski_disari":"0212 185 00 00",
  "iski_disari_link":"+902121850000",
  "ibb_ad":     "İBB Beyaz Masa",
  "ibb_tel":    "153",
  "ibb_tel_link":"153",
  "kaynak":     "https://iski.istanbul/iletisim/alo-185/",
}

# Sorumluluk tablosu — her ilçe sayfasında basılır.
# (nerede, kim sorumlu, nereye başvurulur)
SORUMLULUK = [
 ("Daire içi giderler — lavabo, klozet, banyo, mutfak",
  "Mal sahibi veya kiracı", "Özel tesisatçı"),
 ("Bina içi kolon ve apartman ana gideri",
  "Bina yönetimi / kat malikleri", "Özel tesisatçı"),
 ("Parsel içi hat — bina çıkışından sokak bağlantısına kadar",
  "Mülk sahibi (abone)", "Özel tesisatçı"),
 ("Sokaktaki ana kanalizasyon hattı ve rögarı",
  "İSKİ", "ALO 185"),
 ("Yol üstü yağmur suyu ızgarası",
  "İBB / İSKİ", "ALO 153 veya 185"),
]
