(function () {
  var items = Array.prototype.slice.call(document.querySelectorAll(".g-item"));
  if (!items.length) return;
  var lb = document.createElement("div");
  lb.className = "lightbox";
  lb.setAttribute("role", "dialog");
  lb.setAttribute("aria-modal", "true");
  lb.setAttribute("aria-label", "Image viewer");
  lb.innerHTML =
    '<button class="lb-btn lb-close" aria-label="Close">&times;</button><button class="lb-btn lb-prev" aria-label="Previous">&lsaquo;</button><img alt=""><button class="lb-btn lb-next" aria-label="Next">&rsaquo;</button>';
  document.body.appendChild(lb);
  var img = lb.querySelector("img"),
    cur = 0,
    last;
  function show(n) {
    cur = (n + items.length) % items.length;
    img.src = items[cur].dataset.full;
    img.alt = items[cur].querySelector("img").alt;
  }
  function open(n) {
    last = document.activeElement;
    show(n);
    lb.classList.add("open");
    document.body.style.overflow = "hidden";
    lb.querySelector(".lb-close").focus();
  }
  function close() {
    lb.classList.remove("open");
    document.body.style.overflow = "";
    if (last) last.focus();
  }
  items.forEach(function (el, i) {
    el.addEventListener("click", function () {
      open(i);
    });
  });
  lb.querySelector(".lb-close").onclick = close;
  lb.querySelector(".lb-prev").onclick = function () {
    show(cur - 1);
  };
  lb.querySelector(".lb-next").onclick = function () {
    show(cur + 1);
  };
  lb.addEventListener("click", function (e) {
    if (e.target === lb) close();
  });
  document.addEventListener("keydown", function (e) {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") show(cur - 1);
    if (e.key === "ArrowRight") show(cur + 1);
  });
})();
