(function () {
  var today = new Date().toISOString().split('T')[0];
  var ins = document.querySelectorAll('input#checkin'), outs = document.querySelectorAll('input#checkout');
  function nextDay(v) { var d = new Date(v); d.setDate(d.getDate() + 1); return d.toISOString().split('T')[0]; }
  ins.forEach(function (inp, i) {
    var out = outs[i]; inp.min = today;
    function sync() {
      if (!inp.value) return;
      out.min = nextDay(inp.value);
      if (!out.value || out.value <= inp.value) out.value = nextDay(inp.value);
      total();
    }
    inp.addEventListener('change', sync);
    if (out) out.addEventListener('change', total);
    out.min = today;
  });

  var room = document.getElementById('broom'), totalEl = document.getElementById('total');
  function total() {
    if (!room || !totalEl) return;
    var a = document.getElementById('checkin').value, b = document.getElementById('checkout').value;
    if (!a || !b) return;
    var nights = Math.round((new Date(b) - new Date(a)) / 864e5);
    if (nights < 1) { totalEl.textContent = 'Check-out must be after check-in.'; return; }
    var price = +room.options[room.selectedIndex].dataset.price;
    totalEl.textContent = nights + (nights > 1 ? ' nights' : ' night') + ' x $' + price + ' = $' + nights * price;
  }
  if (room) { room.addEventListener('change', total); total(); }

  /* Rooms page filters */
  var grid = document.getElementById('roomGrid');
  if (!grid) return;
  var f = { cat: fCat, price: fPrice, guests: fGuests, sort: fSort, avail: fAvail };
  var cards = Array.prototype.slice.call(grid.children);
  function apply() {
    fPriceOut.textContent = f.price.value;
    var shown = 0;
    cards.forEach(function (c) {
      var ok = (f.cat.value === 'all' || c.dataset.category === f.cat.value) && +c.dataset.price <= +f.price.value &&
               +c.dataset.guests >= +f.guests.value && (!f.avail.checked || c.dataset.available === '1');
      c.hidden = !ok; if (ok) shown++;
    });
    var sorted = cards.slice();
    if (f.sort.value !== 'none') sorted.sort(function (a, b) { return (a.dataset.price - b.dataset.price) * (f.sort.value === 'asc' ? 1 : -1); });
    sorted.forEach(function (c) { grid.appendChild(c); });
    document.getElementById('noRooms').hidden = shown > 0;
  }
  ['change', 'input'].forEach(function (ev) { document.getElementById('filters').addEventListener(ev, apply); });
  apply();
})();

/* Frontend-only: prefill booking form from URL and handle demo forms */
(function () {
  var q = new URLSearchParams(location.search), bf = document.getElementById('bookingForm');
  if (bf) {
    ['checkin', 'checkout', 'adults', 'children'].forEach(function (k) { var el = bf.elements[k]; if (el && q.get(k)) el.value = q.get(k); });
    var room = bf.elements.room; if (room && q.get('room')) room.value = q.get('room');
    if (room) room.dispatchEvent(new Event('change'));
  }
  document.querySelectorAll('form[data-demo]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var t = document.createElement('div'); t.className = 'toast'; t.setAttribute('role', 'status');
      t.textContent = f.id === 'bookingForm' ? 'Your reservation request has been received. A confirmation will be sent to your email.' : 'Thank you. Your message has been sent and we will reply within one business day.';
      document.body.appendChild(t); setTimeout(function () { t.remove(); }, 6000); f.reset();
    });
  });
})();
