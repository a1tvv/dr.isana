(function () {
  'use strict';

  var WHATSAPP_NUMBER = '996502259797';
  var CART_KEY = 'dr_isana_cart';

  /* ================= Корзина ================= */

  function getCart() {
    try { return JSON.parse(localStorage.getItem(CART_KEY)) || {}; }
    catch (e) { return {}; }
  }

  function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    renderCart();
  }

  function fmt(n) { return Number(n).toLocaleString('ru-RU') + ' сом'; }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function addToCart(id, name, price, image) {
    var cart = getCart();
    if (cart[id]) cart[id].qty += 1;
    else cart[id] = { id: id, name: name, price: Number(price), qty: 1, image: image || '' };
    saveCart(cart);
    openCart();
  }

  function incQty(id) { var c = getCart(); if (c[id]) { c[id].qty += 1; saveCart(c); } }

  function decQty(id) {
    var c = getCart();
    if (c[id]) { c[id].qty -= 1; if (c[id].qty <= 0) delete c[id]; saveCart(c); }
  }

  function removeItem(id) { var c = getCart(); delete c[id]; saveCart(c); }

  function cartTotal(cart) {
    var t = 0;
    Object.keys(cart).forEach(function (id) { t += cart[id].price * cart[id].qty; });
    return t;
  }

  function cartCount(cart) {
    var n = 0;
    Object.keys(cart).forEach(function (id) { n += cart[id].qty; });
    return n;
  }

  function renderCart() {
    var cart = getCart();
    var body = document.querySelector('[data-cart-body]');
    var badge = document.querySelector('[data-cart-count]');
    var totalEl = document.querySelector('[data-cart-total]');
    if (!body) return;

    var count = cartCount(cart);
    if (badge) {
      badge.textContent = count;
      badge.classList.toggle('is-hidden', count === 0);
    }
    if (totalEl) totalEl.textContent = fmt(cartTotal(cart));

    var ids = Object.keys(cart);
    if (ids.length === 0) {
      body.innerHTML = '<div class="cart-empty">Корзина пуста</div>';
      return;
    }

    body.innerHTML = ids.map(function (id) {
      var it = cart[id];
      var imgHtml = it.image
        ? '<img class="cart-line-img" src="' + escapeHtml(it.image) + '" alt="">'
        : '';
      return '<div class="cart-line">' +
        imgHtml +
        '<div class="cart-line-info">' +
          '<div class="cart-line-name">' + escapeHtml(it.name) + '</div>' +
          '<div class="cart-line-price">' + fmt(it.price) + ' × ' + it.qty + '</div>' +
          '<div class="cart-line-controls">' +
            '<button type="button" class="qty-btn" data-dec="' + id + '">\u2212</button>' +
            '<span>' + it.qty + '</span>' +
            '<button type="button" class="qty-btn" data-inc="' + id + '">+</button>' +
            '<button type="button" class="cart-line-remove" data-remove="' + id + '">Удалить</button>' +
          '</div>' +
        '</div>' +
        '<div class="cart-line-total">' + fmt(it.price * it.qty) + '</div>' +
      '</div>';
    }).join('');
  }

  function openCart() {
    var o = document.querySelector('[data-cart-overlay]');
    var d = document.querySelector('[data-cart-drawer]');
    if (o) o.classList.add('is-open');
    if (d) d.classList.add('is-open');
  }

  function closeCart() {
    var o = document.querySelector('[data-cart-overlay]');
    var d = document.querySelector('[data-cart-drawer]');
    if (o) o.classList.remove('is-open');
    if (d) d.classList.remove('is-open');
  }

  function openCheckout() {
    closeCart();
    var o = document.querySelector('[data-checkout-overlay]');
    if (o) o.classList.add('is-open');
  }

  function closeCheckout() {
    var o = document.querySelector('[data-checkout-overlay]');
    if (o) o.classList.remove('is-open');
  }

  function submitOrder() {
    var cart = getCart();
    var ids = Object.keys(cart);
    if (ids.length === 0) return;

    var nameEl = document.querySelector('[data-checkout-name]');
    var phoneEl = document.querySelector('[data-checkout-phone]');
    var name = nameEl ? nameEl.value.trim() : '';
    var phone = phoneEl ? phoneEl.value.trim() : '';

    var lines = ids.map(function (id) {
      var it = cart[id];
      return '• ' + it.name + ' × ' + it.qty + ' — ' + fmt(it.price * it.qty);
    });

    var text = 'Здравствуйте! Хочу оформить заказ:\n' + lines.join('\n') +
      '\n\nИтого: ' + fmt(cartTotal(cart)) +
      '\n\nИмя: ' + (name || '-') +
      '\nТелефон: ' + (phone || '-');

    window.open('https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(text), '_blank');

    localStorage.removeItem(CART_KEY);
    renderCart();
    closeCheckout();
    if (nameEl) nameEl.value = '';
    if (phoneEl) phoneEl.value = '';
  }

  /* ================= Поиск по товарам ================= */

  function initSearch() {
    var input = document.querySelector('[data-product-search]');
    var grid = document.querySelector('[data-product-grid]');
    if (!input || !grid) return;

    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      var cards = grid.querySelectorAll('.product-card');
      var visible = 0;

      for (var i = 0; i < cards.length; i++) {
        var nameEl = cards[i].querySelector('.product-name');
        var descEl = cards[i].querySelector('.product-desc');
        var hay = ((nameEl ? nameEl.textContent : '') + ' ' + (descEl ? descEl.textContent : '')).toLowerCase();
        var match = !q || hay.indexOf(q) !== -1;
        cards[i].style.display = match ? '' : 'none';
        if (match) visible++;
      }

      var noRes = grid.querySelector('[data-no-results]');
      if (visible === 0 && q) {
        if (!noRes) {
          noRes = document.createElement('div');
          noRes.className = 'empty-state';
          noRes.setAttribute('data-no-results', '');
          noRes.textContent = 'Ничего не найдено. Попробуйте изменить запрос.';
          grid.appendChild(noRes);
        }
      } else if (noRes) {
        noRes.remove();
      }
    });
  }

  /* ================= Init ================= */

  document.addEventListener('DOMContentLoaded', function () {
    renderCart();
    initSearch();

    document.addEventListener('click', function (e) {
      var addBtn = e.target.closest('[data-add-to-cart]');
      if (addBtn) {
        e.preventDefault();
        addToCart(addBtn.dataset.id, addBtn.dataset.name, addBtn.dataset.price, addBtn.dataset.image);
        return;
      }
      if (e.target.closest('[data-open-cart]')) { e.preventDefault(); openCart(); return; }
      if (e.target.closest('[data-close-cart]')) { e.preventDefault(); closeCart(); return; }
      if (e.target.closest('[data-open-checkout]')) { e.preventDefault(); openCheckout(); return; }
      if (e.target.closest('[data-close-checkout]')) { e.preventDefault(); closeCheckout(); return; }
      if (e.target.closest('[data-submit-order]')) { e.preventDefault(); submitOrder(); return; }

      var inc = e.target.closest('[data-inc]');
      if (inc) { incQty(inc.dataset.inc); return; }
      var dec = e.target.closest('[data-dec]');
      if (dec) { decQty(dec.dataset.dec); return; }
      var rm = e.target.closest('[data-remove]');
      if (rm) { removeItem(rm.dataset.remove); return; }

      var descToggle = e.target.closest('[data-desc-toggle]');
      if (descToggle) {
        var desc = descToggle.previousElementSibling;
        var expanded = desc.classList.toggle('is-expanded');
        descToggle.textContent = expanded ? 'Свернуть' : 'Далее';
        return;
      }

      var burger = e.target.closest('[data-burger-toggle]');
      if (burger) {
        var mobileNav = document.querySelector('[data-mobile-nav]');
        var isOpen = mobileNav.classList.toggle('is-open');
        burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        return;
      }

      var card = e.target.closest('[data-card-link]');
      if (card && !e.target.closest('[data-add-to-cart]') && !e.target.closest('a')) {
        window.location.href = card.dataset.cardLink;
        return;
      }
    });

    document.querySelectorAll('[data-desc]').forEach(function (desc) {
      if (desc.scrollHeight > desc.clientHeight + 1) {
        var toggle = desc.nextElementSibling;
        if (toggle && toggle.hasAttribute('data-desc-toggle')) toggle.style.display = 'inline-block';
      }
    });

    var checkoutOverlayEl = document.querySelector('[data-checkout-overlay]');
    if (checkoutOverlayEl) {
      checkoutOverlayEl.addEventListener('click', function (e) {
        if (e.target === checkoutOverlayEl) closeCheckout();
      });
    }

    var revealEls = document.querySelectorAll('.reveal');
    if (revealEls.length) {
      if ('IntersectionObserver' in window) {
        var revealObserver = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible');
              revealObserver.unobserve(entry.target);
            }
          });
        }, { threshold: 0.15 });
        revealEls.forEach(function (el) { revealObserver.observe(el); });
      } else {
        revealEls.forEach(function (el) { el.classList.add('is-visible'); });
      }
    }
  });
})();
