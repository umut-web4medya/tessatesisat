/* TESSA TESİSAT — app.js  (üçüncü parti kütüphane YOK) */
(function () {
  "use strict";

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

  /* ── Yüzen yığın ────────────────────────────────────────────────────── */
  /* ⚠️ Sayfa dibine yaklaşınca gizlenir. Sabit kalırsa mobilde Web4Medya
     imzasının tam üstüne oturuyor ve imza tıklanamaz hâle geliyor. */
  var dock = document.querySelector(".dock");
  if (dock) {
    var bekle = false;
    var tazele = function () {
      var y = window.scrollY || window.pageYOffset;
      var toplam = document.documentElement.scrollHeight;
      var gorunen = window.innerHeight;
      var dipte = (toplam - (y + gorunen)) < 280;
      dock.classList.toggle("gizli", dipte);
      bekle = false;
    };
    window.addEventListener("scroll", function () {
      if (!bekle) { bekle = true; requestAnimationFrame(tazele); }
    }, { passive: true });
    tazele();
  }
})();
