#!/usr/bin/env python3
"""Пересобирает README и картинки в docs/ — карточки в стиле iOS, как в olymp.

Две версии: английская (README.md, картинки в docs/en) открывается на GitHub по умолчанию,
русская — README.ru.md, картинки в docs. Сверху у обеих — ссылка-переключатель.

Запуск: python3 scripts/build_readme.py

docs/phones.png (сайт в айфонах) этот скрипт не трогает — это скриншот, его обновляют руками.
"""
import html
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
SITE = 'https://dr-isana.vercel.app'
REPO_URL = 'https://github.com/a1tvv'
LANG = 'ru'


def tr(ru, en=None):
    """Текст на языке, который сейчас собирается: tr('рус', 'eng') или tr(('рус', 'eng')).
    Просто строка — одна на оба языка."""
    if en is None:
        if isinstance(ru, str):
            return ru
        ru, en = ru
    return en if LANG == 'en' else ru


FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"
GRAD = {
    'green': ('#4ade80', '#1e9e47'), 'orange': ('#ffb340', '#d26a00'), 'gray': ('#7c7c80', '#3a3a3c'),
    'blue': ('#64d2ff', '#0a84ff'), 'violet': ('#d48cff', '#7d3bd1'),
    'django': ('#2ba977', '#0c4b33'), 'postgres': ('#6c9bd8', '#336791'), 'spaces': ('#4da3ff', '#0069ff'),
    'vercel': ('#48484a', '#1c1c1e'),
}
AI_STOPS = ('<stop offset="0" stop-color="#ff9f0a"/><stop offset="0.35" stop-color="#ff375f"/>'
            '<stop offset="0.7" stop-color="#bf5af2"/><stop offset="1" stop-color="#0a84ff"/>')
TILE = ('<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#161618"/><stop offset="1" stop-color="#000000"/></linearGradient>')
TITANIUM = ('<linearGradient id="titanium" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0.2" stop-color="#ffffff"/><stop offset="1" stop-color="#8e8e93"/></linearGradient>')

# Иконки те же, что в мобильном меню сайта (templates/store/base.html), сетка 24×24
ICONS = {
    'grid': ('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>'
             '<rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
    'cart': ('<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>'
             '<path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>'),
    'star': '<path d="M12 3l2.6 5.9 6.4.6-4.8 4.3 1.4 6.2L12 16.9 6.4 20l1.4-6.2L3 9.5l6.4-.6z"/>',
    'person': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/>',
    'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
}

# (имя файла, иконка, цвет, заголовок, описание, плашка справа, куда ведёт строка)
FEATURES = [
    ('catalog', 'grid', 'blue', ('Каталог', 'Catalog'),
     ('PDRN, PLLA и филлеры — фильтр по категориям и поиск', 'PDRN, PLLA and fillers — filter by category and search'),
     '/catalog/', f'{SITE}/catalog/'),
    ('order', 'cart', 'green', ('Корзина и заказ', 'Cart and order'),
     ('Без регистрации — заказ уходит менеджеру в WhatsApp', 'No sign-up — the order goes to a manager in WhatsApp'),
     'WhatsApp', SITE),
    ('reviews', 'star', 'orange', ('Отзывы', 'Reviews'),
     ('Отзывы коллег и фото до/после — добавляются из админки',
      'Reviews from colleagues and before/after photos — added in the admin panel'),
     '/reviews/', f'{SITE}/reviews/'),
    ('about', 'person', 'violet', ('О враче', 'About the doctor'),
     ('Кто такая Dr. Isana и как с ней связаться', 'Who Dr. Isana is and how to contact her'),
     '/about/', f'{SITE}/about/'),
    ('admin', 'lock', 'gray', ('Админка', 'Admin panel'),
     ('Своё оформление: товары, отзывы и фото без программиста',
      'Custom design: products, reviews and photos without a programmer'),
     'Django', 'store/admin.py'),
]

# (цвет иконки, надпись на иконке, название, подпись)
STACK = [
    ('django', 'dj', 'Django 6.1', 'Python 3.12'),
    ('postgres', 'PG', 'PostgreSQL', ('база на проде', 'production database')),
    ('spaces', 'DO', 'DO Spaces', ('фото товаров', 'product photos')),
    ('vercel', None, 'Vercel', ('хостинг и деплой', 'hosting and deploy')),
]

ENV = [
    ('SECRET_KEY', ('без неё сайт не запустится', 'the site will not start without it'),
     (('обязательно', 'required'), '#ff9f0a')),
    ('DEBUG', ('True — только на своём компьютере', 'True — only on your own computer'),
     (('только локально', 'local only'), '#64d2ff')),
    ('ALLOWED_HOSTS', ('домены через запятую', 'domains, separated by commas'), None),
    ('DATABASE_URL', ('PostgreSQL, без неё — локальная SQLite', 'PostgreSQL; without it — local SQLite'), None),
    ('USE_SPACES', ('True — фото хранятся в DigitalOcean Spaces', 'True — photos are kept in DigitalOcean Spaces'), None),
    ('DO_SPACES_*', ('ключ, секрет, бакет и адрес Spaces', 'Spaces key, secret, bucket and address'), None),
]

DEPLOY = [
    ('Пуш в `main` — Vercel сам выкатит новую версию', 'Push to `main` — Vercel puts the new version online by itself'),
    ('Правили CSS, JS или картинки — `collectstatic` и закоммитить `staticfiles/`',
     'Changed CSS, JS or images — run `collectstatic` and commit `staticfiles/`'),
    ('Новая миграция — `migrate` с `DATABASE_URL` продовой базы',
     'New migration — run `migrate` with the `DATABASE_URL` of the production database'),
]

RUN_COMMANDS = '''# {install}
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# {first}
echo "DEBUG=True" > .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# {tests}
python manage.py test

# {rebuild}
python3 scripts/build_readme.py'''


# ───────────────────────── помощники ─────────────────────────

def esc(s):
    return html.escape(str(s), quote=False)


def grad_def(gid, name):
    a, b = GRAD[name]
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')


def write_svg(path, w, h, label, defs, body):
    full = os.path.join(DOCS, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
                f'role="img" aria-label="{html.escape(label)}">\n<defs>{defs}</defs>\n'
                f'<g font-family="{FONT}">\n{body}\n</g>\n</svg>\n')


def app_icon(x, y, size, gid, inner):
    r = size * 0.26
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" fill="url(#{gid})"/>'
            f'<rect x="{x + .5}" y="{y + .5}" width="{size - 1}" height="{size - 1}" rx="{r}" fill="none" '
            f'stroke="#ffffff" stroke-opacity="0.18"/>' + inner)


def icon_glyph(x, y, size, name):
    """Иконка из ICONS по центру квадрата: обводка белым, как в меню сайта."""
    scale = size * 0.55 / 24
    offset = size * 0.225
    return (f'<g transform="translate({x + offset} {y + offset}) scale({scale:.3f})" fill="none" stroke="#ffffff" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def icon_text(x, y, size, text, fs):
    return (f'<text x="{x + size / 2}" y="{y + size / 2 + fs * 0.36}" font-size="{fs}" font-weight="700" '
            f'fill="#ffffff" text-anchor="middle">{esc(text)}</text>')


def rich(x, y, line, fs=21):
    """Строка, где `текст в обратных кавычках` выделяется моноширинным голубым."""
    out = f'<text x="{x}" y="{y}" font-size="{fs}" font-weight="500" fill="#d1d1d6">'
    for i, part in enumerate(line.split('`')):
        if not part:
            continue
        if i % 2:
            out += (f'<tspan font-family="{MONO}" font-size="{fs - 2}" font-weight="600" '
                    f'fill="#64d2ff">{esc(part)}</tspan>')
        else:
            out += f'<tspan>{esc(part)}</tspan>'
    return out + '</text>'


def tile(w, h, rx=31.5):
    return (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="url(#tile)" '
            'stroke="#ffffff" stroke-opacity="0.1"/>')


CHEVRON = ('<path d="M1160 53l12 13-12 13" fill="none" stroke="#636366" stroke-width="3.5" '
           'stroke-linecap="round" stroke-linejoin="round"/>')


# ───────────────────────── карточки ─────────────────────────

def banner():
    # Dynamic Island раскрывается, как Live Activity нового заказа
    island = (
        '<rect x="530" y="30" width="140" height="46" rx="23" fill="#000000" stroke="#ffffff" stroke-opacity="0.16">'
        '<animate attributeName="width" values="140;140;480;480;140" keyTimes="0;0.1;0.2;0.86;1" dur="7s" '
        'repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.3 0.9 0.2 1;0 0 1 1;0.5 0 0.2 1"/>'
        '<animate attributeName="x" values="530;530;360;360;530" keyTimes="0;0.1;0.2;0.86;1" dur="7s" '
        'repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.3 0.9 0.2 1;0 0 1 1;0.5 0 0.2 1"/></rect>'
        '<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.18;0.24;0.82;0.86;1" '
        'dur="7s" repeatCount="indefinite"/>'
        '<circle cx="393" cy="53" r="12" fill="#30d158"/>'
        '<path d="M387 53.5l4 4 7.5-8" fill="none" stroke="#000000" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<text x="416" y="59.5" font-size="18" font-weight="600" fill="#ffffff">{tr("Новый заказ", "New order")}</text>'
        f'<text x="816" y="59.5" font-size="18" font-weight="600" fill="#30d158" text-anchor="end">{tr("4 230 сом", "4 230 som")}</text></g>'
    )
    defs = (f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="1">{AI_STOPS}'
            '<animateTransform attributeName="gradientTransform" type="rotate" from="0 0.5 0.5" to="360 0.5 0.5" '
            'dur="9s" repeatCount="indefinite"/></linearGradient>'
            f'<linearGradient id="aiText" x1="0" y1="0" x2="1" y2="0">{AI_STOPS}</linearGradient>' + TITANIUM +
            '<radialGradient id="spot" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity="0.07"/>'
            '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>'
            '<filter id="edgeGlow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="20"/></filter>'
            '<clipPath id="card"><rect width="1200" height="600" rx="32"/></clipPath>')
    body = (
        '<g clip-path="url(#card)"><rect width="1200" height="600" fill="#000000"/>'
        '<ellipse cx="600" cy="320" rx="560" ry="260" fill="url(#spot)"/>'
        '<rect width="1200" height="600" rx="32" fill="none" stroke="url(#ai)" stroke-width="40" filter="url(#edgeGlow)" opacity="0.85"/>'
        '<rect x="1.5" y="1.5" width="1197" height="597" rx="30.5" fill="none" stroke="url(#ai)" stroke-width="3"/></g>'
        + island +
        f'<text x="600" y="206" text-anchor="middle" font-size="28" font-weight="600" fill="url(#aiText)">{tr("Препараты для косметологов", "Products for cosmetologists")}</text>'
        '<text x="600" y="318" text-anchor="middle" font-size="104" font-weight="700" letter-spacing="-3" fill="url(#titanium)">Dr. Isana</text>'
        f'<text x="600" y="392" text-anchor="middle" font-size="36" font-weight="600" fill="#86868b">{tr("PDRN. PLLA. Филлеры.", "PDRN. PLLA. Fillers.")}</text>'
        f'<text x="600" y="466" text-anchor="middle" font-size="26" font-weight="500" fill="#2997ff">{tr("Открыть сайт ›", "Open the website ›")}</text>'
    )
    write_svg('banner.svg', 1200, 600, tr('Dr. Isana — препараты для косметологов', 'Dr. Isana — products for cosmetologists'),
              defs, body)


def stats():
    # «100%» набирается по четвертям, как счётчик в olymp
    steps = ['25%', '50%', '75%', '100%']
    frames = ''
    for i, value in enumerate(steps):
        start, end = i / len(steps), (i + 1) / len(steps)
        if value == steps[-1]:
            anim = f'<animate attributeName="opacity" values="0;1" keyTimes="0;{start:.3f}" calcMode="discrete" dur="0.8s" fill="freeze"/>'
            frames += f'<text x="34" y="400">{value}{anim}</text>'
        else:
            anim = (f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{start:.3f};{end:.3f}" '
                    'calcMode="discrete" dur="0.8s" fill="freeze"/>')
            frames += f'<text x="34" y="400" opacity="0">{value}{anim}</text>'

    defs = (f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="1">{AI_STOPS}</linearGradient>'
            + grad_def('blue', 'blue') + grad_def('green', 'green') + TITANIUM + TILE +
            '<filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="60"/></filter>'
            '<clipPath id="t1"><rect width="590" height="540" rx="32"/></clipPath>')
    body = (
        '<g font-weight="600">'
        # большая плитка слева
        '<g clip-path="url(#t1)"><rect width="590" height="540" fill="url(#tile)"/>'
        '<circle cx="470" cy="470" r="150" fill="url(#ai)" opacity="0.35" filter="url(#blur)"/></g>'
        '<rect x="0.5" y="0.5" width="589" height="539" rx="31.5" fill="none" stroke="#ffffff" stroke-opacity="0.1"/>'
        f'<text x="48" y="86" font-size="24" fill="#86868b">{tr("Оригинальные препараты", "Original products")}</text>'
        f'<g font-size="190" font-weight="700" letter-spacing="-6" fill="url(#ai)">{frames}</g>'
        f'<text x="48" y="490" font-size="22" fill="#86868b">{tr("напрямую от поставщика  ·  без посредников", "directly from the supplier  ·  no resellers")}</text>'
        # доставка
        '<rect x="610.5" y="0.5" width="589" height="259" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
        f'<text x="658" y="86" font-size="24" fill="#86868b">{tr("Доставка по Бишкеку", "Delivery in Bishkek")}</text>'
        f'<text x="652" y="200" font-size="80" font-weight="700" letter-spacing="-2" fill="url(#blue)">{tr("день в день", "same day")}</text>'
        # категории
        '<rect x="610.5" y="280.5" width="284" height="259" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
        f'<text x="646" y="344" font-size="24" fill="#86868b">{tr("Категории", "Categories")}</text>'
        '<text x="644" y="440" font-size="58" font-weight="700" letter-spacing="-1" fill="url(#titanium)">PDRN</text>'
        f'<text x="646" y="490" font-size="26" fill="#86868b">{tr("PLLA · филлеры", "PLLA · fillers")}</text>'
        # подделки
        '<rect x="915.5" y="280.5" width="284" height="259" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
        f'<text x="951" y="344" font-size="24" fill="#86868b">{tr("Подделок", "Fakes")}</text>'
        '<text x="946" y="448" font-size="110" font-weight="700" letter-spacing="-3" fill="url(#green)">0</text>'
        f'<text x="951" y="490" font-size="26" fill="#86868b">{tr("ни одной", "not a single one")}</text>'
        '</g>'
    )
    label = tr('Оригинальные препараты — 100%. Доставка по Бишкеку день в день. Категории: PDRN, PLLA, филлеры. Подделок: 0.',
               'Original products — 100%. Same-day delivery in Bishkek. Categories: PDRN, PLLA, fillers. Fakes: 0.')
    write_svg('stats.svg', 1200, 540, label, defs, body)


def title(name, heading, subs):
    defs = f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="0">{AI_STOPS}</linearGradient>'
    body = f'<text x="2" y="62" font-size="54" font-weight="700" letter-spacing="-1.2" fill="url(#ai)">{esc(heading)}</text>'
    for i, sub in enumerate(subs):
        body += f'<text x="3" y="{104 + 34 * i}" font-size="25" font-weight="500" fill="#8e8e93">{esc(sub)}</text>'
    write_svg(f'titles/{name}.svg', 1200, 92 + 34 * len(subs), heading, defs, body)


def feature_row(name, icon, color, heading, about, pill):
    w = 30 + 12 * len(pill)
    body = ('<rect x="0.5" y="6.5" width="1199" height="119" rx="26" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
            + app_icon(22, 24, 84, 'ic', icon_glyph(22, 24, 84, icon)) +
            f'<text x="128" y="61" font-size="30" font-weight="600" fill="#f5f5f7">{esc(heading)}</text>'
            f'<text x="128" y="99" font-size="21" font-weight="500" fill="#86868b">{esc(about)}</text>'
            f'<rect x="{1128 - w}" y="48" width="{w}" height="36" rx="18" fill="#ffffff" fill-opacity="0.08"/>'
            f'<text x="{1128 - w / 2}" y="72" font-family="{MONO}" font-size="19" font-weight="600" fill="#f5f5f7" '
            f'text-anchor="middle">{esc(pill)}</text>' + CHEVRON)
    write_svg(f'rows/{name}.svg', 1200, 132, f'{heading} — {about}', TILE + grad_def('ic', color), body)


def stack():
    size, col = 84, 300
    defs = TILE + ''.join(grad_def(f'ic{i}', color) for i, (color, *_) in enumerate(STACK))
    body = tile(1200, 260)
    for i, (_, glyph, name, caption) in enumerate(STACK):
        cx = col * i + col / 2
        x, y = cx - size / 2, 44
        if glyph:
            inner = icon_text(x, y, size, glyph, 32)
        else:  # треугольник Vercel
            inner = f'<path d="M{cx} {y + 24}L{cx + 22} {y + 62}H{cx - 22}z" fill="#ffffff"/>'
        body += app_icon(x, y, size, f'ic{i}', inner)
        body += (f'<text x="{cx}" y="174" font-size="26" font-weight="600" fill="#f5f5f7" text-anchor="middle">{esc(name)}</text>'
                 f'<text x="{cx}" y="208" font-size="20" font-weight="500" fill="#86868b" text-anchor="middle">{esc(tr(caption))}</text>')
        if i:
            body += f'<line x1="{col * i}" y1="48" x2="{col * i}" y2="212" stroke="#ffffff" stroke-opacity="0.08"/>'
    label = tr('Стек: ', 'Stack: ') + ', '.join(f'{name} — {tr(caption)}' for _, _, name, caption in STACK)
    write_svg('stack.svg', 1200, 260, label, defs, body)


def structure():
    tree = [
        (0, 'dr.isana/', ''),
        (1, 'config/', tr('настройки Django и адреса', 'Django settings and URLs')),
        (1, 'store/', tr('модели, вьюхи, админка', 'models, views, admin')),
        (2, 'migrations/', tr('изменения базы', 'database changes')),
        (2, 'tests.py', tr('тесты', 'tests')),
        (1, 'templates/', tr('шаблоны сайта и админки', 'site and admin templates')),
        (1, 'static/', tr('исходные CSS, JS и картинки', 'source CSS, JS and images')),
        (1, 'staticfiles/', tr('собранная статика для Vercel', 'built static files for Vercel')),
        (1, 'scripts/', tr('сборка README', 'README build')),
        (1, 'docs/', tr('картинки для README', 'pictures for README')),
    ]
    row, top, x0, ind = 46, 74, 48, 44
    h = top + row * len(tree) + 130
    defs = TILE + grad_def('folder', 'blue') + grad_def('root', 'violet') + grad_def('file', 'gray')
    lines, items = '', ''
    for i, (d, name, desc) in enumerate(tree):
        y, x = top + i * row, x0 + d * ind
        if d:
            p = max(k for k in range(i) if tree[k][0] == d - 1)
            px, py = x0 + (d - 1) * ind + 15, top + p * row
            lines += f'<path d="M{px} {py + 8}V{y - 8}H{x - 8}" fill="none" stroke="#3a3a3c" stroke-width="2"/>'
        if name.endswith('/'):
            fill = 'root' if d == 0 else 'folder'
            items += (f'<path transform="translate({x} {y - 19})" d="M0 4a3 3 0 0 1 3-3h7.5l3 3.5H27a3 3 0 0 1 3 3V19a3 3 0 0 1-3 3H3a3 3 0 0 1-3-3z" '
                      f'fill="url(#{fill})"/>')
        else:
            items += f'<path transform="translate({x + 5} {y - 22})" d="M0 3a3 3 0 0 1 3-3h10l7 7v15a3 3 0 0 1-3 3H3a3 3 0 0 1-3-3z" fill="url(#file)"/>'
        items += f'<text x="{x + 42}" y="{y}" font-family="{MONO}" font-size="21" font-weight="600" fill="#f5f5f7">{esc(name)}</text>'
        if desc:
            items += f'<text x="560" y="{y}" font-size="21" font-weight="500" fill="#86868b">{esc(desc)}</text>'
    ny = h - 78
    body = (tile(1200, h) + lines + items +
            f'<line x1="48" y1="{ny - 42}" x2="1152" y2="{ny - 42}" stroke="#ffffff" stroke-opacity="0.08"/>'
            + rich(48, ny, tr('Новая страница — вьюха в `store/views.py` и шаблон в `templates/store/`',
                              'New page — a view in `store/views.py` and a template in `templates/store/`'), fs=20)
            + rich(48, ny + 36, tr('Правили CSS или картинки — `collectstatic`, потом закоммитить `staticfiles/`',
                                   'Changed CSS or images — run `collectstatic`, then commit `staticfiles/`'), fs=20))
    write_svg('structure.svg', 1200, h, tr('Структура репозитория', 'Repository structure'), defs, body)


def terminal():
    p, t, op, s, com, out = '#30d158', '#f5f5f7', '#ff375f', '#ffd60a', '#636366', '#64d2ff'
    lines = [
        [(tr('# Установка', '# Install'), com)],
        [('$ ', p), ('python3 -m venv .venv ', t), ('&&', op), (' source .venv/bin/activate', t)],
        [('$ ', p), ('pip install -r requirements.txt', t)],
        [],
        [(tr('# Первый запуск', '# First run'), com)],
        [('$ ', p), ('echo ', t), ('"DEBUG=True"', s), (' > ', op), ('.env', t)],
        [('$ ', p), ('python manage.py migrate', t)],
        [('$ ', p), ('python manage.py runserver', t)],
        [('Starting development server at http://127.0.0.1:8000/', out)],
        [],
        [(tr('# Тесты', '# Tests'), com)],
        [('$ ', p), ('python manage.py test', t)],
        [('OK', out)],
    ]
    lh, top = 36, 122
    h = top + lh * (len(lines) - 1) + 56
    body = (tile(1200, h, rx=23.5) +
            '<rect x="1" y="1" width="1198" height="59" rx="23" fill="#ffffff" fill-opacity="0.04"/>'
            '<line x1="1" y1="60.5" x2="1199" y2="60.5" stroke="#ffffff" stroke-opacity="0.08"/>'
            + ''.join(f'<circle cx="{34 + 24 * k}" cy="30" r="7" fill="{col}"/>' for k, col in enumerate(('#ff5f57', '#febc2e', '#28c840')))
            + f'<text x="600" y="36" font-family="{MONO}" font-size="16" fill="#8e8e93" text-anchor="middle">zsh — dr.isana</text>')
    for i, segs in enumerate(lines):
        if segs:
            body += (f'<text x="48" y="{top + i * lh}" font-family="{MONO}" font-size="20" xml:space="preserve" style="white-space:pre">'
                     + ''.join(f'<tspan fill="{col}">{esc(txt)}</tspan>' for txt, col in segs) + '</text>')
    write_svg('run.svg', 1200, h, tr('Запуск сайта в терминале', 'Running the site in the terminal'), TILE, body)


def deploy():
    row, top = 64, 66
    h = top + row * len(DEPLOY) - 6
    defs = TILE + grad_def('num', 'blue')
    body = tile(1200, h)
    for i, line in enumerate(DEPLOY):
        y = top + i * row
        body += (f'<circle cx="66" cy="{y - 7}" r="18" fill="url(#num)"/>'
                 f'<text x="66" y="{y}" font-size="20" font-weight="700" fill="#ffffff" text-anchor="middle">{i + 1}</text>'
                 + rich(104, y, tr(line)))
        if i:
            body += f'<line x1="104" y1="{y - 39}" x2="1152" y2="{y - 39}" stroke="#ffffff" stroke-opacity="0.08"/>'
    write_svg('deploy.svg', 1200, h, tr('Деплой: ', 'Deploy: ') + '; '.join(tr(l).replace('`', '') for l in DEPLOY),
              defs, body)


def env():
    # Список как в «Настройках» iOS: имя слева, пояснение рядом, плашка справа
    row, top = 66, 54
    h = top + row * len(ENV) - 20
    body = tile(1200, h)
    for i, (name, about, pill) in enumerate(ENV):
        y = top + i * row
        body += (f'<text x="48" y="{y}" font-family="{MONO}" font-size="21" font-weight="600" fill="#f5f5f7">{esc(name)}</text>'
                 f'<text x="330" y="{y}" font-size="21" font-weight="500" fill="#86868b">{esc(tr(about))}</text>')
        if pill:
            text, color = pill
            text = tr(text)
            w = 28 + 11 * len(text)
            body += (f'<rect x="{1152 - w}" y="{y - 25}" width="{w}" height="34" rx="17" fill="{color}" fill-opacity="0.15"/>'
                     f'<text x="{1152 - w / 2}" y="{y - 2}" font-size="17" font-weight="600" fill="{color}" text-anchor="middle">{esc(text)}</text>')
        if i:
            body += f'<line x1="48" y1="{y - 41}" x2="1152" y2="{y - 41}" stroke="#ffffff" stroke-opacity="0.08"/>'
    label = tr('Переменные окружения: ', 'Environment variables: ') + '; '.join(f'{name} — {tr(about)}' for name, about, _ in ENV)
    write_svg('env.svg', 1200, h, label, TILE, body)


def footer():
    defs = (TITANIUM + f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="0">{AI_STOPS}'
            '<animateTransform attributeName="gradientTransform" type="translate" values="-0.3 0;0.3 0;-0.3 0" dur="8s" repeatCount="indefinite"/>'
            '</linearGradient><radialGradient id="spot" cx="0.5" cy="1" r="0.7"><stop offset="0" stop-color="#bf5af2" stop-opacity="0.22"/>'
            '<stop offset="1" stop-color="#bf5af2" stop-opacity="0"/></radialGradient>'
            '<clipPath id="card"><rect width="1200" height="380" rx="32"/></clipPath>')
    body = ('<g clip-path="url(#card)"><rect width="1200" height="380" fill="#000000"/><rect width="1200" height="380" fill="url(#spot)"/></g>'
            '<rect x="0.5" y="0.5" width="1199" height="379" rx="31.5" fill="none" stroke="#ffffff" stroke-opacity="0.1"/>'
            '<g font-weight="700" text-anchor="middle">'
            '<text x="600" y="160" font-size="96" letter-spacing="-3" fill="url(#titanium)">Stay hungry.</text>'
            '<text x="600" y="262" font-size="96" letter-spacing="-3" fill="url(#ai)">Stay foolish.</text>'
            '<text x="600" y="326" font-size="22" font-weight="600" fill="#86868b">Steve Jobs · 1955–2011</text></g>')
    write_svg('footer.svg', 1200, 380, 'Stay hungry. Stay foolish. — Steve Jobs, 1955–2011', defs, body)


# ───────────────────────── README ─────────────────────────

def section_title(anchor, name, alt, img):
    return f'<a name="{anchor}"></a>\n<img src="{img}/titles/{name}.svg" alt="{alt}" width="100%">\n'


def readme():
    img = 'docs' if LANG == 'ru' else 'docs/en'  # футер и фото айфонов — общие, лежат в docs
    switch = ('<p align="center"><a href="README.md">English</a> &nbsp;|&nbsp; <b>Русский</b></p>' if LANG == 'ru' else
              '<p align="center"><b>English</b> &nbsp;|&nbsp; <a href="README.ru.md">Русский</a></p>')
    rows = [f'<a href="{link}"><img src="{img}/rows/{name}.svg" alt="{esc(tr(heading))} — {esc(tr(about))}" width="100%"></a>'
            for name, _, _, heading, about, _, link in FEATURES]
    commands = RUN_COMMANDS.format(install=tr('Установка', 'Install'), first=tr('Первый запуск', 'First run'),
                                   tests=tr('Тесты', 'Tests'), rebuild=tr('Пересобрать README', 'Rebuild README'))
    out = [
        tr('<!-- Этот файл собирается скриптом: python3 scripts/build_readme.py. Правки вручную перезапишутся. -->',
           '<!-- This file is built by a script: python3 scripts/build_readme.py. Edits by hand will be lost. -->'),
        switch,
        '',
        f'<a href="{SITE}"><img src="{img}/banner.svg" alt="{tr("Dr. Isana — препараты для косметологов", "Dr. Isana — products for cosmetologists")}" width="100%"></a>',
        '',
        '<p align="center">\n'
        f'  <a href="#site">{tr("Сайт", "Website")}&nbsp;›</a>&emsp;\n'
        f'  <a href="#features">{tr("Возможности", "Features")}&nbsp;›</a>&emsp;\n'
        f'  <a href="#stack">{tr("Под капотом", "Under the hood")}&nbsp;›</a>&emsp;\n'
        f'  <a href="#structure">{tr("Структура", "Structure")}&nbsp;›</a>&emsp;\n'
        f'  <a href="#run">{tr("Запуск", "Run")}&nbsp;›</a>&emsp;\n'
        f'  <a href="#deploy">{tr("Деплой", "Deploy")}&nbsp;›</a>\n</p>',
        '', '<br>', '',
        f'<img src="{img}/stats.svg" alt="{tr("Оригинальные препараты, доставка по Бишкеку день в день", "Original products, same-day delivery in Bishkek")}" width="100%">',
        '', '<br>\n<br>', '',
        '<p align="center">\n  <i>«Simplicity is the ultimate sophistication.»</i><br>\n'
        f'  <sub>— {tr("первая брошюра Apple, 1977", "the first Apple brochure, 1977")}</sub>\n</p>',
        '', '<br>', '',
        section_title('site', 'site', tr('Сайт', 'Website'), img),
        f'<a href="{SITE}"><img src="docs/phones.png" alt="{tr("Сайт на iPhone: главная, каталог и страница товара", "The website on iPhone: home, catalog and product page")}" width="100%"></a>',
        '', '<br>\n<br>', '',
        section_title('features', 'features', tr('Возможности', 'Features'), img),
        '\n'.join(rows),
        '', '<br>\n<br>', '',
        section_title('stack', 'stack', tr('Под капотом', 'Under the hood'), img),
        f'<img src="{img}/stack.svg" alt="Django 6.1, PostgreSQL, DigitalOcean Spaces, Vercel" width="100%">',
        '', '<br>\n<br>', '',
        section_title('structure', 'structure', tr('Структура', 'Structure'), img),
        f'<img src="{img}/structure.svg" alt="{tr("Структура репозитория", "Repository structure")}" width="100%">',
        '', '<br>\n<br>', '',
        section_title('run', 'run', tr('Запуск', 'Run'), img),
        f'<img src="{img}/run.svg" alt="{tr("Запуск сайта в терминале", "Running the site in the terminal")}" width="100%">',
        '',
        f'<details>\n<summary>{tr("Скопировать команды", "Copy the commands")}</summary>\n<br>\n\n```bash\n{commands}\n```\n\n</details>',
        '', '<br>\n<br>', '',
        section_title('deploy', 'deploy', tr('Деплой', 'Deploy'), img),
        f'<img src="{img}/deploy.svg" alt="{tr("Как выкатить изменения", "How to put changes online")}" width="100%">',
        '', '<br>', '',
        f'<img src="{img}/env.svg" alt="{tr("Переменные окружения", "Environment variables")}" width="100%">',
        '', '<br>', '',
        '<img src="docs/footer.svg" alt="Stay hungry. Stay foolish. — Steve Jobs, 1955–2011" width="100%">',
        '',
        '<p align="center">\n'
        f'  <sub>Dr. Isana · {tr("Бишкек", "Bishkek")} &nbsp;·&nbsp; <a href="https://instagram.com/dr.isana">@dr.isana</a>'
        ' &nbsp;·&nbsp; <a href="https://wa.me/996502259797">WhatsApp</a></sub><br>\n'
        f'  <sub>{tr("Сделано с ☕ и Django", "Made with ☕ and Django")} &nbsp;·&nbsp; <a href="{REPO_URL}">@a1tvv</a></sub>\n</p>',
        '',
    ]
    with open(os.path.join(ROOT, 'README.ru.md' if LANG == 'ru' else 'README.md'), 'w') as f:
        f.write('\n'.join(out))


def build(lang):
    """Собирает картинки и README на одном языке: 'ru' — docs и README.ru.md, 'en' — docs/en и README.md."""
    global LANG, DOCS
    LANG = lang
    DOCS = os.path.join(ROOT, 'docs') if lang == 'ru' else os.path.join(ROOT, 'docs', 'en')

    for sub in ('rows', 'titles'):  # сгенерированные папки пересоздаём, чтобы не копился мусор
        shutil.rmtree(os.path.join(DOCS, sub), ignore_errors=True)

    banner()
    stats()
    title('site', tr('Сайт', 'Website'),
          [tr('Живая версия — dr-isana.vercel.app. Так он выглядит на iPhone.',
              'Live version — dr-isana.vercel.app. This is how it looks on iPhone.')])
    title('features', tr('Возможности', 'Features'),
          [tr('Нажми на строку — откроется эта страница на сайте.', 'Click a row to open this page on the website.')])
    for name, icon, color, heading, about, pill, _ in FEATURES:
        feature_row(name, icon, color, tr(heading), tr(about), pill)
    title('stack', tr('Под капотом', 'Under the hood'),
          [tr('Чистый Django: шаблоны, CSS и немного JS — без фронтенд-фреймворков.',
              'Plain Django: templates, CSS and a little JS — no frontend frameworks.')])
    stack()
    title('structure', tr('Структура', 'Structure'),
          [tr('Обычный Django-проект: одно приложение store и общие шаблоны.',
              'A normal Django project: one app called store and shared templates.')])
    structure()
    title('run', tr('Запуск', 'Run'),
          [tr('Нужен Python 3.12+. Локально база — SQLite, ставить ничего не надо.',
              'You need Python 3.12+. Locally the database is SQLite, so you do not need to install anything.')])
    terminal()
    title('deploy', tr('Деплой', 'Deploy'),
          [tr('Сайт на Vercel, база — PostgreSQL, фото — DigitalOcean Spaces.',
              'The site is on Vercel, the database is PostgreSQL, photos are in DigitalOcean Spaces.')])
    deploy()
    env()
    if lang == 'ru':  # в футере нет русского текста — он общий для обеих версий
        footer()
    readme()


def main():
    build('ru')
    build('en')
    print('README.md, README.ru.md и docs/ пересобраны')


if __name__ == '__main__':
    main()
