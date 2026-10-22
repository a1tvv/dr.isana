<!-- Этот файл собирается скриптом: python3 scripts/build_readme.py. Правки вручную перезапишутся. -->
<p align="center"><a href="README.md">English</a> &nbsp;|&nbsp; <b>Русский</b></p>

<a href="https://dr-isana.vercel.app"><img src="docs/banner.svg" alt="Dr. Isana — препараты для косметологов" width="100%"></a>

<p align="center">
  <a href="#site">Сайт&nbsp;›</a>&emsp;
  <a href="#features">Возможности&nbsp;›</a>&emsp;
  <a href="#stack">Под капотом&nbsp;›</a>&emsp;
  <a href="#structure">Структура&nbsp;›</a>&emsp;
  <a href="#run">Запуск&nbsp;›</a>&emsp;
  <a href="#deploy">Деплой&nbsp;›</a>
</p>

<br>

<img src="docs/stats.svg" alt="Оригинальные препараты, доставка по Бишкеку день в день" width="100%">

<br>
<br>

<p align="center">
  <i>«Simplicity is the ultimate sophistication.»</i><br>
  <sub>— первая брошюра Apple, 1977</sub>
</p>

<br>

<a name="site"></a>
<img src="docs/titles/site.svg" alt="Сайт" width="100%">

<a href="https://dr-isana.vercel.app"><img src="docs/phones.png" alt="Сайт на iPhone: главная, каталог и страница товара" width="100%"></a>

<br>
<br>

<a name="features"></a>
<img src="docs/titles/features.svg" alt="Возможности" width="100%">

<a href="https://dr-isana.vercel.app/catalog/"><img src="docs/rows/catalog.svg" alt="Каталог — PDRN, PLLA и филлеры — фильтр по категориям и поиск" width="100%"></a>
<a href="https://dr-isana.vercel.app"><img src="docs/rows/order.svg" alt="Корзина и заказ — Без регистрации — заказ уходит менеджеру в WhatsApp" width="100%"></a>
<a href="https://dr-isana.vercel.app/reviews/"><img src="docs/rows/reviews.svg" alt="Отзывы — Отзывы коллег и фото до/после — добавляются из админки" width="100%"></a>
<a href="https://dr-isana.vercel.app/about/"><img src="docs/rows/about.svg" alt="О враче — Кто такая Dr. Isana и как с ней связаться" width="100%"></a>
<a href="store/admin.py"><img src="docs/rows/admin.svg" alt="Админка — Своё оформление: товары, отзывы и фото без программиста" width="100%"></a>

<br>
<br>

<a name="stack"></a>
<img src="docs/titles/stack.svg" alt="Под капотом" width="100%">

<img src="docs/stack.svg" alt="Django 6.1, PostgreSQL, DigitalOcean Spaces, Vercel" width="100%">

<br>
<br>

<a name="structure"></a>
<img src="docs/titles/structure.svg" alt="Структура" width="100%">

<img src="docs/structure.svg" alt="Структура репозитория" width="100%">

<br>
<br>

<a name="run"></a>
<img src="docs/titles/run.svg" alt="Запуск" width="100%">

<img src="docs/run.svg" alt="Запуск сайта в терминале" width="100%">

<details>
<summary>Скопировать команды</summary>
<br>

```bash
# Установка
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Первый запуск
echo "DEBUG=True" > .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Тесты
python manage.py test

# Пересобрать README
python3 scripts/build_readme.py
```

</details>

<br>
<br>

<a name="deploy"></a>
<img src="docs/titles/deploy.svg" alt="Деплой" width="100%">

<img src="docs/deploy.svg" alt="Как выкатить изменения" width="100%">

<br>

<img src="docs/env.svg" alt="Переменные окружения" width="100%">

<br>

<img src="docs/footer.svg" alt="Stay hungry. Stay foolish. — Steve Jobs, 1955–2011" width="100%">

<p align="center">
  <sub>Dr. Isana · Бишкек &nbsp;·&nbsp; <a href="https://instagram.com/dr.isana">@dr.isana</a> &nbsp;·&nbsp; <a href="https://wa.me/996502259797">WhatsApp</a></sub><br>
  <sub>Сделано с ☕ и Django &nbsp;·&nbsp; <a href="https://github.com/a1tvv">@a1tvv</a></sub>
</p>
