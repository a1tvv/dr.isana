<!-- This file is built by a script: python3 scripts/build_readme.py. Edits by hand will be lost. -->
<p align="center"><b>English</b> &nbsp;|&nbsp; <a href="README.ru.md">Русский</a></p>

<a href="https://dr-isana.vercel.app"><img src="docs/en/banner.svg" alt="Dr. Isana — products for cosmetologists" width="100%"></a>

<p align="center">
  <a href="#site">Website&nbsp;›</a>&emsp;
  <a href="#features">Features&nbsp;›</a>&emsp;
  <a href="#stack">Under the hood&nbsp;›</a>&emsp;
  <a href="#structure">Structure&nbsp;›</a>&emsp;
  <a href="#run">Run&nbsp;›</a>&emsp;
  <a href="#deploy">Deploy&nbsp;›</a>
</p>

<br>

<img src="docs/en/stats.svg" alt="Original products, same-day delivery in Bishkek" width="100%">

<br>
<br>

<p align="center">
  <i>«Simplicity is the ultimate sophistication.»</i><br>
  <sub>— the first Apple brochure, 1977</sub>
</p>

<br>

<a name="site"></a>
<img src="docs/en/titles/site.svg" alt="Website" width="100%">

<a href="https://dr-isana.vercel.app"><img src="docs/phones.png" alt="The website on iPhone: home, catalog and product page" width="100%"></a>

<br>
<br>

<a name="features"></a>
<img src="docs/en/titles/features.svg" alt="Features" width="100%">

<a href="https://dr-isana.vercel.app/catalog/"><img src="docs/en/rows/catalog.svg" alt="Catalog — PDRN, PLLA and fillers — filter by category and search" width="100%"></a>
<a href="https://dr-isana.vercel.app"><img src="docs/en/rows/order.svg" alt="Cart and order — No sign-up — the order goes to a manager in WhatsApp" width="100%"></a>
<a href="https://dr-isana.vercel.app/reviews/"><img src="docs/en/rows/reviews.svg" alt="Reviews — Reviews from colleagues and before/after photos — added in the admin panel" width="100%"></a>
<a href="https://dr-isana.vercel.app/about/"><img src="docs/en/rows/about.svg" alt="About the doctor — Who Dr. Isana is and how to contact her" width="100%"></a>
<a href="store/admin.py"><img src="docs/en/rows/admin.svg" alt="Admin panel — Custom design: products, reviews and photos without a programmer" width="100%"></a>

<br>
<br>

<a name="stack"></a>
<img src="docs/en/titles/stack.svg" alt="Under the hood" width="100%">

<img src="docs/en/stack.svg" alt="Django 6.1, PostgreSQL, DigitalOcean Spaces, Vercel" width="100%">

<br>
<br>

<a name="structure"></a>
<img src="docs/en/titles/structure.svg" alt="Structure" width="100%">

<img src="docs/en/structure.svg" alt="Repository structure" width="100%">

<br>
<br>

<a name="run"></a>
<img src="docs/en/titles/run.svg" alt="Run" width="100%">

<img src="docs/en/run.svg" alt="Running the site in the terminal" width="100%">

<details>
<summary>Copy the commands</summary>
<br>

```bash
# Install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# First run
echo "DEBUG=True" > .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Tests
python manage.py test

# Rebuild README
python3 scripts/build_readme.py
```

</details>

<br>
<br>

<a name="deploy"></a>
<img src="docs/en/titles/deploy.svg" alt="Deploy" width="100%">

<img src="docs/en/deploy.svg" alt="How to put changes online" width="100%">

<br>

<img src="docs/en/env.svg" alt="Environment variables" width="100%">

<br>

<img src="docs/footer.svg" alt="Stay hungry. Stay foolish. — Steve Jobs, 1955–2011" width="100%">

<p align="center">
  <sub>Dr. Isana · Bishkek &nbsp;·&nbsp; <a href="https://instagram.com/dr.isana">@dr.isana</a> &nbsp;·&nbsp; <a href="https://wa.me/996502259797">WhatsApp</a></sub><br>
  <sub>Made with ☕ and Django &nbsp;·&nbsp; <a href="https://github.com/a1tvv">@a1tvv</a></sub>
</p>
