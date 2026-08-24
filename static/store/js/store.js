(function () {
  'use strict';

  var WHATSAPP_NUMBER = '996502259797'; // TODO: заменить на актуальный номер клиента
  var CART_KEY = 'dr_isana_cart';

  function getCart() {
    try {
      return JSON.parse(localStorage.getItem(CART_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    renderCart();
  }

  function fmt(n) {
    return Number(n).toLocaleString('ru-RU') + ' сом';
  }

  function addToCart(id, name, price) {
    var cart = getCart();
    if (cart[id]) {
      cart[id].qty += 1;
    } else {
      cart[id] = { id: id, name: name, price: Number(price), qty: 1 };
    }
    saveCart(cart);
    openCart();
  }

  function incQty(id) {
    var cart = getCart();
    if (cart[id]) { cart[id].qty += 1; saveCart(cart); }
  }

  function decQty(id) {
    var cart = getCart();
    if (cart[id]) {
      cart[id].qty -= 1;
      if (cart[id].qty <= 0) delete cart[id];
      saveCart(cart);
    }
  }

  function removeItem(id) {
    var cart = getCart();
    delete cart[id];
    saveCart(cart);
  }

  function cartTotal(cart) {
    var total = 0;
    Object.keys(cart).forEach(function (id) { total += cart[id].price * cart[id].qty; });
    return total;
  }

  function cartCount(cart) {
    var count = 0;
    Object.keys(cart).forEach(function (id) { count += cart[id].qty; });
    return count;
  }

  function renderCart() {
    var cart = getCart();
    var body = document.querySelector('[data-cart-body]');
    var countBadge = document.querySelector('[data-cart-count]');
    var totalLabel = document.querySelector('[data-cart-total]');
    if (!body) return;

    var count = cartCount(cart);
    if (countBadge) {
      countBadge.textContent = count;
      countBadge.classList.toggle('is-hidden', count === 0);
    }
    if (totalLabel) totalLabel.textContent = fmt(cartTotal(cart));

    var ids = Object.keys(cart);
    if (ids.length === 0) {
      body.innerHTML = '<div class="cart-empty">Корзина пуста</div>';
      return;
    }

    body.innerHTML = ids.map(function (id) {
      var item = cart[id];
      var lineTotal = item.price * item.qty;
      return (
        '<div class="cart-line">' +
          '<div class="cart-line-info">' +
            '<div class="cart-line-name">' + escapeHtml(item.name) + '</div>' +
            '<div class="cart-line-price">' + fmt(item.price) + ' × ' + item.qty + '</div>' +
            '<div class="cart-line-controls">' +
              '<button type="button" class="qty-btn" data-dec="' + id + '">\u2212</button>' +
              '<span>' + item.qty + '</span>' +
              '<button type="button" class="qty-btn" data-inc="' + id + '">+</button>' +
              '<button type="button" class="cart-line-remove" data-remove="' + id + '">Удалить</button>' +
            '</div>' +
          '</div>' +
          '<div class="cart-line-total">' + fmt(lineTotal) + '</div>' +
        '</div>'
      );
    }).join('');
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function openCart() {
    var overlay = document.querySelector('[data-cart-overlay]');
    var drawer = document.querySelector('[data-cart-drawer]');
    if (overlay) overlay.classList.add('is-open');
    if (drawer) drawer.classList.add('is-open');
  }

  function closeCart() {
    var overlay = document.querySelector('[data-cart-overlay]');
    var drawer = document.querySelector('[data-cart-drawer]');
    if (overlay) overlay.classList.remove('is-open');
    if (drawer) drawer.classList.remove('is-open');
  }

  function openCheckout() {
    closeCart();
    var overlay = document.querySelector('[data-checkout-overlay]');
    if (overlay) overlay.classList.add('is-open');
  }

  function closeCheckout() {
    var overlay = document.querySelector('[data-checkout-overlay]');
    if (overlay) overlay.classList.remove('is-open');
  }

  function submitOrder() {
    var cart = getCart();
    var ids = Object.keys(cart);
    if (ids.length === 0) return;

    var nameInput = document.querySelector('[data-checkout-name]');
    var phoneInput = document.querySelector('[data-checkout-phone]');
    var name = nameInput ? nameInput.value.trim() : '';
    var phone = phoneInput ? phoneInput.value.trim() : '';

    var lines = ids.map(function (id) {
      var item = cart[id];
      return '• ' + item.name + ' × ' + item.qty + ' — ' + fmt(item.price * item.qty);
    });

    var text = 'Здравствуйте! Хочу оформить заказ:\n' + lines.join('\n') +
      '\n\nИтого: ' + fmt(cartTotal(cart)) +
      '\n\nИмя: ' + (name || '-') +
      '\nТелефон: ' + (phone || '-');

    window.open('https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(text), '_blank');

    localStorage.removeItem(CART_KEY);
    renderCart();
    closeCheckout();
    if (nameInput) nameInput.value = '';
    if (phoneInput) phoneInput.value = '';
  }

  document.addEventListener('DOMContentLoaded', function () {
    renderCart();

    document.addEventListener('click', function (e) {
      var addBtn = e.target.closest('[data-add-to-cart]');
      if (addBtn) {
        e.preventDefault();
        addToCart(addBtn.dataset.id, addBtn.dataset.name, addBtn.dataset.price);
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
    });

    // Не закрывать модалку чекаута при клике внутри неё
    var checkoutModal = document.querySelector('[data-checkout-modal]');
    if (checkoutModal) {
      checkoutModal.addEventListener('click', function (e) { e.stopPropagation(); });
    }
  });
})();
