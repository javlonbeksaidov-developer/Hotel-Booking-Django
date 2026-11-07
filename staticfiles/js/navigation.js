(function () {
  var header = document.getElementById("header");
  var burger = document.getElementById("burger");
  var menu = document.getElementById("menu");
  function onScroll() {
    header.classList.toggle("scrolled", window.scrollY > 60);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  function setMenu(open) {
    menu.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.style.overflow = open ? "hidden" : "";
  }
  burger.addEventListener("click", function () {
    setMenu(!menu.classList.contains("open"));
  });
  menu.addEventListener("click", function (e) {
    if (e.target.tagName === "A") setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setMenu(false);
  });
})();
