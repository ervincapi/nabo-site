/* Nabo site — small, dependency-free. Everything degrades without JS. */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Sticky nav: frosted once the page scrolls. */
  var nav = document.getElementById("nav");
  function onScroll() { nav.classList.toggle("is-scrolled", window.scrollY > 8); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Mobile menu. */
  var toggle = document.getElementById("navToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    nav.querySelectorAll(".nav-links a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); });
    });
  }

  /* Language menu closes on outside click or Escape. */
  var lang = document.getElementById("lang");
  if (lang) {
    document.addEventListener("click", function (e) { if (!lang.contains(e.target)) lang.removeAttribute("open"); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") lang.removeAttribute("open"); });
  }

  /* Reveal on scroll: a cheap position check on rAF, so it never depends on observer timing. */
  var items = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (reduce) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var pending = false;
    function check() {
      pending = false;
      var limit = window.innerHeight * 0.94;
      items = items.filter(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < limit && r.bottom > 0) { el.classList.add("in"); return false; }
        return true;
      });
      if (!items.length) {
        window.removeEventListener("scroll", queue);
        window.removeEventListener("resize", queue);
      }
    }
    function queue() { if (!pending) { pending = true; requestAnimationFrame(check); } }
    check();
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue);
    window.addEventListener("load", queue);
    setTimeout(queue, 300);
  }

  /* Gentle parallax on the hero visual (pointer devices only). */
  var stage = document.getElementById("heroVisual");
  if (stage && !reduce && window.matchMedia("(pointer: fine)").matches) {
    var layers = stage.querySelectorAll("[data-depth]");
    var raf = 0, tx = 0, ty = 0;
    function paint() {
      raf = 0;
      layers.forEach(function (el) {
        var d = parseFloat(el.getAttribute("data-depth")) || 0;
        el.style.transform = (el.classList.contains("phone") ? "rotate(-3deg) " : "") +
          "translate3d(" + (tx * d).toFixed(1) + "px," + (ty * d).toFixed(1) + "px,0)";
      });
    }
    stage.addEventListener("pointermove", function (e) {
      var r = stage.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width - 0.5);
      ty = ((e.clientY - r.top) / r.height - 0.5);
      if (!raf) raf = requestAnimationFrame(paint);
    });
    stage.addEventListener("pointerleave", function () {
      tx = 0; ty = 0;
      layers.forEach(function (el) { el.style.transform = ""; });
    });
  }

  /* Theme: light / dark / follow system. */
  var root = document.documentElement;
  document.querySelectorAll("[data-theme-set]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var mode = btn.getAttribute("data-theme-set");
      try {
        if (mode === "auto") { localStorage.removeItem("nabo-theme"); root.removeAttribute("data-theme"); }
        else { localStorage.setItem("nabo-theme", mode); root.setAttribute("data-theme", mode); }
      } catch (e) {
        if (mode === "auto") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", mode);
      }
    });
  });

  /* One FAQ open at a time. */
  var faqs = document.querySelectorAll(".faq");
  faqs.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) faqs.forEach(function (o) { if (o !== d) o.removeAttribute("open"); });
    });
  });
})();
