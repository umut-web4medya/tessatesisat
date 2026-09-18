/* TESSA TESİSAT — app.js  (üçüncü parti kütüphane YOK) */
(function () {
  "use strict";

  var azHareket = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── Mobil menü ─────────────────────────────────────────────────────── */
  var ac = document.querySelector(".mnu-ac");
  var menu = document.querySelector(".menu");
  if (ac && menu) {
    ac.addEventListener("click", function () {
      var acik = menu.classList.toggle("acik");
      ac.setAttribute("aria-expanded", acik ? "true" : "false");
      document.documentElement.style.overflow = acik ? "hidden" : "";
    });
  }

  /* ── Hizmetler açılır listesi ───────────────────────────────────────── */
  document.querySelectorAll(".acilir").forEach(function (k) {
    var dg = k.querySelector("button");
    if (!dg) return;
    dg.addEventListener("click", function (o) {
      o.stopPropagation();
      var acik = k.hasAttribute("data-ac");
      document.querySelectorAll(".acilir[data-ac]").forEach(function (d) {
        d.removeAttribute("data-ac");
        var b = d.querySelector("button");
        if (b) b.setAttribute("aria-expanded", "false");
      });
      if (!acik) { k.setAttribute("data-ac", ""); dg.setAttribute("aria-expanded", "true"); }
    });
  });
  document.addEventListener("click", function () {
    document.querySelectorAll(".acilir[data-ac]").forEach(function (d) {
      d.removeAttribute("data-ac");
      var b = d.querySelector("button");
      if (b) b.setAttribute("aria-expanded", "false");
    });
  });
  document.addEventListener("keydown", function (o) {
    if (o.key === "Escape") {
      document.querySelectorAll(".acilir[data-ac]").forEach(function (d) { d.removeAttribute("data-ac"); });
      if (menu && menu.classList.contains("acik")) {
        menu.classList.remove("acik");
        document.documentElement.style.overflow = "";
        if (ac) ac.setAttribute("aria-expanded", "false");
      }
    }
  });

  /* ── Harita facade ──────────────────────────────────────────────────── */
  /* iframe tıklanana kadar DOM'a girmiyor → ilk yükte 0 üçüncü parti istek. */
  document.querySelectorAll(".harita-ac").forEach(function (dg) {
    dg.addEventListener("click", function () {
      var kap = dg.parentNode, src = kap.getAttribute("data-src");
      if (!src) return;
      var f = document.createElement("iframe");
      f.src = src;
      f.loading = "lazy";
      f.title = kap.getAttribute("data-baslik") || "Harita";
      f.referrerPolicy = "strict-origin-when-cross-origin";
      f.allowFullscreen = true;
      kap.appendChild(f);
      dg.remove();
    });
  });

  /* ── Video facade ───────────────────────────────────────────────────── */
  /* ⚠️ 4 video ~11 MB. <video> DOM'a tıklanana kadar GİRMİYOR; poster
     görünür, tıklanınca gerçek oynatıcı takılıyor. ⛔ preload açma. */
  document.querySelectorAll(".reel-ac").forEach(function (dg) {
    dg.addEventListener("click", function () {
      var src = dg.getAttribute("data-video");
      if (!src) return;
      var poster = dg.querySelector("img");
      var v = document.createElement("video");
      v.src = src;
      v.controls = true;
      v.autoplay = true;
      v.playsInline = true;
      v.setAttribute("playsinline", "");
      v.preload = "auto";
      if (poster) v.poster = poster.getAttribute("src");
      dg.parentNode.insertBefore(v, dg);
      dg.remove();
      var o = v.play();
      if (o && o.catch) o.catch(function () { /* otomatik oynatma engellenebilir */ });
    });
  });

  /* ── Üst başlık yoğunlaşması ────────────────────────────────────────── */
  var ust = document.querySelector(".ust");

  /* ── Yüzen yığın ────────────────────────────────────────────────────── */
  /* ⚠️ Sayfa dibine yaklaşınca gizlenir. Sabit kalırsa mobilde Web4Medya
     imzasının tam üstüne oturuyor ve imza tıklanamaz hâle geliyor. */
  var dock = document.querySelector(".dock");

  /* ── Kaydırma açılışı ───────────────────────────────────────────────── */
  /* ⚠️ Başlangıç durumunu CSS/HTML DEĞİL, bu betik kuruyor. JS çalışmazsa
     içerik olduğu gibi görünür. ⛔ .rv'yi HTML'e yazma.
     ⚠️ IntersectionObserver ile denendi ve 20 öğe hiç açılmadan kaldı
        (Playwright ile yakalandı) — görünmez içerik demekti. Artık açılma
        kaydırma döngüsünün İÇİNDE, düz dikdörtgen kontrolüyle yapılıyor:
        gözcü geri çağırması kaçsa bile her karede yeniden denenir.
     ⛔ Buradaki güvenlik ağını (bekleyenler listesi) kaldırma. */
  var bekleyen = [];
  if (!azHareket) {
    [".b-ust", ".kart", ".fk", ".fs-k", ".reel", ".ist-k", ".yan-kutu",
     ".sss details", ".cta", ".cip-grup", ".fiyat-gorsel", ".tbl"].forEach(function (sec) {
      document.querySelectorAll(sec).forEach(function (el) {
        /* İlk ekranda zaten görünen öğeyi gizleyip geri açmak titreme yapıyor */
        if (el.getBoundingClientRect().top < window.innerHeight * 0.92) return;
        el.classList.add("rv");
        bekleyen.push(el);
      });
    });
    bekleyen.forEach(function (el, i) {
      el.style.transitionDelay = (Math.min(i % 4, 3) * 70) + "ms";
    });
  }

  var bekle = false;
  var tazele = function () {
    var y = window.scrollY || window.pageYOffset;
    var gorunen = window.innerHeight;

    if (ust) ust.classList.toggle("kucuk", y > 12);
    if (dock) {
      var toplam = document.documentElement.scrollHeight;
      dock.classList.toggle("gizli", (toplam - (y + gorunen)) < 280);
    }
    if (bekleyen.length) {
      var kalan = [];
      for (var i = 0; i < bekleyen.length; i++) {
        var el = bekleyen[i];
        var k = el.getBoundingClientRect();
        /* Görüş alanına girdiyse VEYA yukarıda kaldıysa (hızlı kaydırma) aç */
        if (k.top < gorunen * 0.94) { el.classList.add("gor"); }
        else { kalan.push(el); }
      }
      bekleyen = kalan;
    }
    bekle = false;
  };
  window.addEventListener("scroll", function () {
    if (!bekle) { bekle = true; requestAnimationFrame(tazele); }
  }, { passive: true });
  window.addEventListener("resize", tazele, { passive: true });
  /* Son güvenlik ağı: 6 sn sonra hâlâ kapalı kalan varsa koşulsuz aç.
     Görünmez içerik bırakmaktansa efekti kaybetmek yeğdir. */
  setTimeout(function () {
    bekleyen.forEach(function (el) { el.classList.add("gor"); });
    bekleyen = [];
  }, 6000);
  tazele();
})();
