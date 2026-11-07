(function () {
  var loader = document.getElementById('loader');
  window.addEventListener('load', function () { setTimeout(function () { loader.classList.add('done'); }, 300); });
  setTimeout(function () { loader.classList.add('done'); }, 2500);

  var toTop = document.getElementById('toTop');
  window.addEventListener('scroll', function () { toTop.classList.toggle('show', window.scrollY > 600); }, { passive: true });
  toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  var video = document.querySelector('.hero-video');
  if (video) {
    video.addEventListener('error', function () { video.remove(); }, true);
    var src = video.querySelector('source');
    if (src) src.addEventListener('error', function () { video.remove(); });
  }

  var slider = document.getElementById('slider');
  if (slider) {
    var slides = slider.querySelectorAll('.slide'), dots = slider.querySelectorAll('.dot'), cur = 0, timer;
    function show(n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle('active', i === cur); });
      dots.forEach(function (d, i) { d.classList.toggle('active', i === cur); });
    }
    function auto() { clearInterval(timer); timer = setInterval(function () { show(cur + 1); }, 6000); }
    dots.forEach(function (d, i) { d.addEventListener('click', function () { show(i); auto(); }); });
    auto();
  }

  var nf = document.getElementById('newsForm');
  if (nf) nf.addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById('newsMsg').textContent = 'Thank you for subscribing.';
    nf.reset();
  });

  document.querySelectorAll('[data-count]').forEach(function (el) {
    var end = +el.dataset.count, done = false;
    new IntersectionObserver(function (en, o) {
      if (en[0].isIntersecting && !done) {
        done = true; var t0 = performance.now();
        (function step(t) { var p = Math.min((t - t0) / 1400, 1); el.textContent = Math.round(end * p); if (p < 1) requestAnimationFrame(step); })(t0);
        o.disconnect();
      }
    }).observe(el);
  });
})();
