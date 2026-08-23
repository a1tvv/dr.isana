# ART SOFFIO — Django templates

Готовая адаптивная вёрстка под Django, собранная по присланному макету.

## Куда положить

```text
project/
├─ templates/
│  └─ store/
│     ├─ base.html
│     ├─ home.html
│     ├─ catalog.html
│     ├─ product_detail.html
│     ├─ cart.html
│     └─ partials/
│        └─ product_card.html
└─ static/
   └─ store/
      ├─ css/style.css
      ├─ js/store.js
      └─ img/...
```

## Контекст для главной страницы

Шаблон ожидает:

- `bestsellers` — queryset популярных товаров;
- `new_products` — queryset новинок;
- `demo_products` — запасной список товаров, если queryset пуст;
- `cart_count` — количество товаров в корзине;
- `active_page` — например `home` или `catalog`.

У товара используются поля `id`, `name`, `price`, `old_price`, `discount`, `image`, `description`, а также `get_absolute_url()`.

## URL-пути, которые предполагает шаблон

- `/`
- `/catalog/`
- `/cart/`
- `/cart/add/<id>/`
- `/checkout/`
- `/callback/`

Названия и адреса можно поменять под твой `urls.py`.
# dr.isana
