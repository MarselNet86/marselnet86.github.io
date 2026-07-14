# Personal Portfolio Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a static, bilingual (ru/en), light/dark, minimalist one-page portfolio site for Marsel Shamsutdinov, modeled structurally on https://zarazaex.xyz/ but content-focused on job search (resume-driven).

**Architecture:** Single static page (`index.html` + `style.css` + `script.js`), no build step, no dependencies. Bilingual content is duplicated in the DOM (`.ru` / `.en` classes) and toggled via a `data-lang` attribute on `<html>`. Theme is toggled via a `data-theme` attribute on `<html>` driven by CSS custom properties. Both preferences persist in `localStorage`.

**Tech Stack:** Plain HTML5, CSS3 (custom properties), vanilla JavaScript (no frameworks, no bundler).

## Global Constraints

- No build tooling, no npm packages, no external JS/CSS frameworks — everything hand-written and self-contained.
- Font: monospace stack — `'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.
- Color: monochrome only (black/white/greys) — no accent colors, links underlined.
- Default language: Russian (`ru`). Default theme: system preference via `prefers-color-scheme`, overridable and persisted in `localStorage`.
- Every bilingual text node must exist in both `.ru` and `.en` variants — never leave one language incomplete.
- Bilingual toggle mechanism: any element with class `ru` is hidden when `html[data-lang="en"]`; any element with class `en` is hidden when `html[data-lang="ru"]`. This single CSS rule pair (defined once in Task 2) is the only mechanism used for translation — do not introduce a second one.
- Content source of truth: `Шамсутдинов_Марсель_Резюме.pdf` and the design spec at `docs/superpowers/specs/2026-07-14-portfolio-site-design.md`.
- Deploying to GitHub Pages (creating a repo, pushing) is explicitly OUT OF SCOPE for this plan — requires separate user confirmation later.

---

### Task 1: Project skeleton, base styles, font

**Files:**
- Create: `index.html`
- Create: `style.css`

**Interfaces:**
- Produces: HTML skeleton with empty `<header>` and `<main>` elements inside `<body>`, and an inline head script that sets `data-theme` / `data-lang` / `lang` attributes on `<html>` before first paint. Later tasks insert content into `<header>` and append `<section>` elements as the last children of `<main>` (anchored on the literal string `</main>`).
- Produces: `style.css` with `:root` CSS variables (`--bg`, `--fg`, `--muted`, `--border`, `--link`, `--font-mono`) and a `[data-theme="dark"]` override block. Later tasks add new rules to the end of this file; they must reuse these variable names, not invent new ones.

- [ ] **Step 1: Create `index.html`**

```html
<!DOCTYPE html>
<html lang="ru" data-theme="light" data-lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Марсель Шамсутдинов — Fullstack / Backend Developer (Python) · DevOps</title>
<meta name="description" content="Портфолио Марселя Шамсутдинова — Fullstack/Backend-разработчика на Python и DevOps-инженера">
<link rel="stylesheet" href="style.css">
<script>
  (function () {
    var theme = localStorage.getItem('theme');
    if (theme !== 'light' && theme !== 'dark') {
      theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    var lang = localStorage.getItem('lang') === 'en' ? 'en' : 'ru';
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.setAttribute('lang', lang);
  })();
</script>
</head>
<body>
<header></header>
<main>
</main>
<script src="script.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Create `style.css`**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --bg: #ffffff;
  --fg: #111111;
  --muted: #666666;
  --border: #dddddd;
  --link: #111111;
  --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}

[data-theme="dark"] {
  --bg: #0d0d0d;
  --fg: #f2f2f2;
  --muted: #999999;
  --border: #333333;
  --link: #f2f2f2;
}

html, body {
  background: var(--bg);
  color: var(--fg);
}

body {
  font-family: var(--font-mono);
  font-size: 16px;
  line-height: 1.5;
  max-width: 720px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}

a {
  color: var(--link);
  text-decoration: underline;
}

a:hover {
  opacity: 0.7;
}
```

- [ ] **Step 3: Verify the skeleton renders**

Run:
```bash
grep -q 'data-theme="light"' /Users/marsel.shamsutdinov/bio86/index.html && grep -q 'font-mono' /Users/marsel.shamsutdinov/bio86/style.css && echo OK
```
Expected: `OK`

Then open `index.html` in the Browser pane (navigate to `file:///Users/marsel.shamsutdinov/bio86/index.html`) and confirm the page loads with a white background and no console errors.

- [ ] **Step 4: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add index.html style.css
git commit -m "Add site skeleton with theme CSS variables"
```

---

### Task 2: Header with theme/language toggles

**Files:**
- Modify: `index.html` (fill `<header></header>`)
- Modify: `style.css` (append header + toggle + `.ru`/`.en` rules)
- Create: `script.js`

**Interfaces:**
- Consumes: `data-theme` / `data-lang` attributes and CSS variables from Task 1.
- Produces: the site-wide bilingual toggle CSS rule (`[data-lang="ru"] .en { display: none; }` / `[data-lang="en"] .ru { display: none; }`) that every later content task relies on. Produces two DOM ids, `theme-toggle` and `lang-toggle`, that `script.js` binds to — later tasks must not reuse these ids.

- [ ] **Step 1: Replace `<header></header>` in `index.html`**

```html
<header class="site-header">
  <div class="header-top">
    <div class="controls">
      <button id="theme-toggle" class="toggle-btn" type="button" aria-label="Toggle theme">
        <span class="ru">тема</span><span class="en">theme</span>
      </button>
      <button id="lang-toggle" class="toggle-btn" type="button" aria-label="Toggle language">
        <span class="ru">en</span><span class="en">ru</span>
      </button>
    </div>
  </div>
  <h1><span class="ru">Привет, я Марсель</span><span class="en">Hi, I'm Marsel</span></h1>
  <p class="role">Fullstack / Backend Developer (Python) · DevOps</p>
  <p class="location">
    <span class="ru">Сургут, Россия · открыт к удалённой работе</span>
    <span class="en">Surgut, Russia · open to remote work</span>
  </p>
  <p class="resume-download">
    <a href="assets/resume.pdf" download>
      <span class="ru">Скачать резюме (PDF)</span><span class="en">Download resume (PDF)</span>
    </a>
  </p>
</header>
```

- [ ] **Step 2: Create `script.js`**

```javascript
(function () {
  var root = document.documentElement;
  var THEME_KEY = 'theme';
  var LANG_KEY = 'lang';

  document.addEventListener('DOMContentLoaded', function () {
    var themeToggle = document.getElementById('theme-toggle');
    var langToggle = document.getElementById('lang-toggle');

    themeToggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem(THEME_KEY, next);
    });

    langToggle.addEventListener('click', function () {
      var next = root.getAttribute('data-lang') === 'ru' ? 'en' : 'ru';
      root.setAttribute('data-lang', next);
      root.setAttribute('lang', next);
      localStorage.setItem(LANG_KEY, next);
    });
  });
})();
```

- [ ] **Step 3: Append header + toggle + i18n rules to `style.css`**

```css
[data-lang="ru"] .en { display: none; }
[data-lang="en"] .ru { display: none; }

.site-header {
  border-bottom: 1px solid var(--border);
  padding-bottom: 24px;
  margin-bottom: 32px;
}

.header-top {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 16px;
}

.toggle-btn {
  font-family: var(--font-mono);
  font-size: 14px;
  background: none;
  border: 1px solid var(--border);
  color: var(--fg);
  padding: 4px 10px;
  cursor: pointer;
  border-radius: 4px;
}

.toggle-btn:hover {
  opacity: 0.7;
}

.site-header h1 {
  font-size: 28px;
  margin-bottom: 8px;
}

.role {
  color: var(--fg);
  margin-bottom: 4px;
}

.location {
  color: var(--muted);
  font-size: 14px;
  margin-bottom: 16px;
}
```

- [ ] **Step 4: Verify toggles work**

Run:
```bash
grep -q 'id="theme-toggle"' /Users/marsel.shamsutdinov/bio86/index.html && grep -q 'id="lang-toggle"' /Users/marsel.shamsutdinov/bio86/index.html && echo OK
```
Expected: `OK`

Then in the Browser pane, navigate to `file:///Users/marsel.shamsutdinov/bio86/index.html`:
- Click the theme button — background/text colors should invert. Reload the page — the chosen theme must persist.
- Click the language button — "Привет, я Марсель" must swap to "Hi, I'm Marsel" (and vice versa). Reload — the chosen language must persist.
- Check the browser console (`read_console_messages`) — no errors.

- [ ] **Step 5: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add index.html style.css script.js
git commit -m "Add header with theme and language toggles"
```

---

### Task 3: About me section

**Files:**
- Modify: `index.html` (insert new `<section>` immediately before `</main>`)
- Modify: `style.css` (append shared section/typography rules)

**Interfaces:**
- Consumes: `.ru` / `.en` toggle rule from Task 2.
- Produces: shared `.section` / `.section h2` rules in `style.css` that Tasks 4–7 reuse verbatim (do not redefine).

- [ ] **Step 1: Insert the About section**

In `index.html`, replace:
```html
</main>
```
with:
```html
  <section class="section" id="about">
    <h2><span class="ru">Обо мне</span><span class="en">About me</span></h2>
    <p class="ru">Fullstack/backend-разработчик на Python с коммерческим опытом с 2024 года: от мобильной разработки на Flutter до серверных систем на Django и FastAPI и инфраструктурных решений на Docker и nginx. Разрабатывал ERP-систему автоматизации нарядов-допусков, Telegram-ботов для внутренних процессов, торгового бота для предикт-биржи Polymarket и клиентский VPN-сервис — от архитектуры до продакшена. Быстро вникаю в новый стек и довожу продукт от идеи до релиза самостоятельно, без выделенной команды.</p>
    <p class="en">Fullstack/backend developer in Python with commercial experience since 2024: from mobile development in Flutter to server systems in Django and FastAPI and infrastructure solutions in Docker and nginx. Built an ERP system for work-permit automation, Telegram bots for internal processes, a trading bot for the Polymarket prediction market, and a client VPN service — from architecture to production. I get up to speed on new stacks quickly and take a product from idea to release on my own, without a dedicated team.</p>
  </section>
</main>
```

- [ ] **Step 2: Append shared section styles to `style.css`**

```css
.section {
  margin-bottom: 40px;
}

.section h2 {
  font-size: 20px;
  margin-bottom: 12px;
}

.section p {
  margin-bottom: 12px;
}
```

- [ ] **Step 3: Verify content and toggle**

Run:
```bash
grep -q 'id="about"' /Users/marsel.shamsutdinov/bio86/index.html && echo OK
```
Expected: `OK`

In the Browser pane, reload `index.html`, confirm the "Обо мне" / "About me" section renders under the header, and that the language toggle swaps its text along with the header.

- [ ] **Step 4: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add index.html style.css
git commit -m "Add About me section"
```

---

### Task 4: Skills section

**Files:**
- Modify: `index.html` (insert new `<section>` immediately before `</main>`)
- Modify: `style.css` (append skills-row rules)

**Interfaces:**
- Consumes: `.section` / `.section h2` rules from Task 3, `.ru`/`.en` toggle from Task 2.
- Produces: `.skill-row` / `.skill-label` / `.skill-list` classes (not reused elsewhere).

- [ ] **Step 1: Insert the Skills section**

In `index.html`, replace:
```html
</main>
```
with:
```html
  <section class="section" id="skills">
    <h2><span class="ru">Навыки</span><span class="en">Skills</span></h2>
    <div class="skill-row">
      <span class="skill-label">Backend</span>
      <span class="skill-list">Python, Django, FastAPI, Celery, Aiogram, SQLAlchemy, LDAP</span>
    </div>
    <div class="skill-row">
      <span class="skill-label"><span class="ru">Базы данных</span><span class="en">Databases</span></span>
      <span class="skill-list">PostgreSQL, Redis, OracleSQL</span>
    </div>
    <div class="skill-row">
      <span class="skill-label">Frontend / Mobile</span>
      <span class="skill-list">Flutter, Dart, React, JavaScript, HTMX, Tailwind CSS, Bootstrap</span>
    </div>
    <div class="skill-row">
      <span class="skill-label"><span class="ru">DevOps / Инфраструктура</span><span class="en">DevOps / Infrastructure</span></span>
      <span class="skill-list">Docker, Git, Nginx, Caddy, VLESS, XRAY, Marzban API, Remnawave API, CDN-fronting</span>
    </div>
    <div class="skill-row">
      <span class="skill-label"><span class="ru">Данные и Web3</span><span class="en">Data &amp; Web3</span></span>
      <span class="skill-list">Pandas, NumPy, Dash, Plotly, web3.py, eth-account, EIP-712, py-clob-client</span>
    </div>
    <div class="skill-row">
      <span class="skill-label"><span class="ru">Интеграции и API</span><span class="en">Integrations &amp; APIs</span></span>
      <span class="skill-list">REST API, Telegram Bot API, YooKassa API, LDAP</span>
    </div>
  </section>
</main>
```

- [ ] **Step 2: Append skills styles to `style.css`**

```css
.skill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 15px;
}

.skill-label {
  font-weight: bold;
  min-width: 160px;
}

.skill-list {
  color: var(--muted);
}
```

- [ ] **Step 3: Verify content and toggle**

Run:
```bash
grep -q 'id="skills"' /Users/marsel.shamsutdinov/bio86/index.html && grep -q 'py-clob-client' /Users/marsel.shamsutdinov/bio86/index.html && echo OK
```
Expected: `OK`

In the Browser pane, reload, confirm all six skill categories render and the "Базы данных"/"Databases" label toggles with the language switch.

- [ ] **Step 4: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add index.html style.css
git commit -m "Add Skills section"
```

---

### Task 5: Experience section

**Files:**
- Modify: `index.html` (insert new `<section>` immediately before `</main>`)
- Modify: `style.css` (append experience-entry rules)

**Interfaces:**
- Consumes: `.section` rules from Task 3, `.ru`/`.en` toggle from Task 2.
- Produces: `.job` / `.job-title` / `.job-meta` / `.job-stack` classes (not reused elsewhere).

- [ ] **Step 1: Insert the Experience section**

In `index.html`, replace:
```html
</main>
```
with:
```html
  <section class="section" id="experience">
    <h2><span class="ru">Опыт работы</span><span class="en">Experience</span></h2>

    <div class="job">
      <div class="job-title">
        Daimon Group — <span class="ru">Основатель · Python / DevOps</span><span class="en">Founder · Python / DevOps</span>
      </div>
      <div class="job-meta"><span class="ru">Янв 2026 — н.в. · Удалённо</span><span class="en">Jan 2026 — present · Remote</span></div>
      <p class="ru"><strong>Trojan VPN</strong> — сервис для обхода блокировок в РФ (закрытый код). VPN на протоколе VLESS (XRAY, Marzban/Remnawave API) — 3 сервера, до 1000 клиентов. Каскадная маскировка трафика через XHTTP и CDN-fronting для обхода ТСПУ и DPI. Приём платежей через YooKassa API, Telegram-бот на Aiogram, веб-интерфейс на React.</p>
      <p class="en"><strong>Trojan VPN</strong> — a censorship-circumvention VPN service (closed source). Built on the VLESS protocol (XRAY, Marzban/Remnawave API) — 3 servers, up to 1000 clients. Cascading traffic masking via XHTTP and CDN-fronting to bypass DPI-based blocking. Payments via YooKassa API, a Telegram bot on Aiogram, and a React web dashboard.</p>
      <p class="job-stack">Стек: Remnawave API, XRAY, Docker, VLESS, Marzban API, Caddy, Nginx, React, Aiogram, YooKassa API, FastAPI</p>

      <p class="ru"><strong>Бот для Polymarket</strong> — дашборд на Dash/Plotly для анализа рынков SOL, BTC, ETH, XRP; сбор данных по стаканам через WebSocket с fallback на REST API; Django-приложение для мониторинга крупных игроков и proxy-кошельков; торговая модель на py-clob-client и web3.py (EIP-712), автоскальпинг на 15-минутных опционах.</p>
      <p class="en"><strong>Polymarket inefficiency bot</strong> — a Dash/Plotly dashboard analyzing SOL, BTC, ETH, XRP markets; continuous Polymarket order-book collection over WebSocket with REST API fallback; a Django app for tracking large market players and proxy wallets; a trading model on py-clob-client and web3.py (EIP-712 order signing) with automated scalping on 15-minute options.</p>
      <p class="job-stack">Стек: Python, py-clob-client, web3.py, eth-account, EIP-712, Django, Dash, Plotly, Pandas, NumPy</p>
    </div>

    <div class="job">
      <div class="job-title">ПАО «Ростелеком» — <span class="ru">Python / Web Developer</span><span class="en">Python / Web Developer</span></div>
      <div class="job-meta"><span class="ru">Дек 2024 — Дек 2025 · Сургут</span><span class="en">Dec 2024 — Dec 2025 · Surgut</span></div>
      <p class="ru">B2C Telegram-бот (XRT) с мини-приложением для контроля заявок — использовался всем Сургутским районом (до 30 заявок в день) вместо громоздкой CRM. ERP-система автоматизации нарядов-допусков — реализовал ключевые модули. Telegram-бот для уведомлений о нарядах WFM. Внутренние инструменты: анализ эффективности сотрудников, геокодер, бот для аварийного доступа к БД.</p>
      <p class="en">A B2C Telegram bot (XRT) with a mini-app for tracking service requests — used across the whole Surgut district (up to 30 requests/day) instead of a cumbersome CRM. An ERP system automating work permits — built key modules. A Telegram bot for WFM work-order notifications. Internal tools: employee efficiency analysis, a geocoder, and an emergency database-access bot.</p>
      <p class="job-stack">Стек: Python, Django, Celery, Aiogram, LDAP, SQLAlchemy, PostgreSQL, OracleSQL, Redis, Docker</p>
    </div>

    <div class="job">
      <div class="job-title"><span class="ru">Фриланс-проекты</span><span class="en">Freelance projects</span></div>
      <div class="job-meta"><span class="ru">2025 · Сургут</span><span class="en">2025 · Surgut</span></div>
      <p class="ru">Сайт-меню кафе «ЯЕсть» (Python, Django, PostgreSQL, JavaScript, HTMX, Docker). Образовательная платформа для СурГПУ (Python, Django, PostgreSQL, Pillow, Docker, Nginx). Лендинг для логистической компании «БашАвтоСпец» (Python, Django, Tailwind CSS, DaisyUI).</p>
      <p class="en">A menu website for the "YaYest" café (Python, Django, PostgreSQL, JavaScript, HTMX, Docker). An education platform for SurSPU (Python, Django, PostgreSQL, Pillow, Docker, Nginx). A landing page for the "BashAvtoSpec" logistics company (Python, Django, Tailwind CSS, DaisyUI).</p>
    </div>

    <div class="job">
      <div class="job-title">ООО «Сытый самурай» — <span class="ru">Flutter Developer</span><span class="en">Flutter Developer</span></div>
      <div class="job-meta"><span class="ru">Фев 2024 — Май 2024 · Сургут</span><span class="en">Feb 2024 — May 2024 · Surgut</span></div>
      <p class="ru">Мобильное приложение заказов еды: авторизация по телефону, корзина, профиль, тёмная тема. Приложение для Android TV (статусы заказов) и планшетов (кухня в реальном времени).</p>
      <p class="en">A food-ordering mobile app: phone-number auth, cart, profile, dark theme. An Android TV app (order status display) and a tablet app (real-time kitchen order tracking).</p>
      <p class="job-stack">Стек: Flutter, Dart, REST API</p>
    </div>
  </section>
</main>
```

- [ ] **Step 2: Append experience styles to `style.css`**

```css
.job {
  margin-bottom: 28px;
  padding-bottom: 4px;
}

.job-title {
  font-weight: bold;
  font-size: 16px;
}

.job-meta {
  color: var(--muted);
  font-size: 14px;
  margin-bottom: 8px;
}

.job p {
  margin-bottom: 8px;
}

.job-stack {
  color: var(--muted);
  font-size: 13px;
}
```

- [ ] **Step 3: Verify content and toggle**

Run:
```bash
grep -q 'id="experience"' /Users/marsel.shamsutdinov/bio86/index.html && grep -q 'Ростелеком' /Users/marsel.shamsutdinov/bio86/index.html && grep -q 'Сытый самурай' /Users/marsel.shamsutdinov/bio86/index.html && echo OK
```
Expected: `OK`

In the Browser pane, reload, confirm all four experience entries render in order (Daimon Group, Ростелеком, Фриланс-проекты, Сытый самурай) and toggle correctly between ru/en.

- [ ] **Step 4: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add index.html style.css
git commit -m "Add Experience section"
```

---

### Task 6: Projects section

**Files:**
- Modify: `index.html` (insert new `<section>` immediately before `</main>`)
- Modify: `style.css` (append project-row rules)

**Interfaces:**
- Consumes: `.section` rules from Task 3, `.ru`/`.en` toggle from Task 2.
- Produces: `.project-row` / `.project-name` / `.project-link` / `.project-private` classes (not reused elsewhere).

- [ ] **Step 1: Insert the Projects section**

In `index.html`, replace:
```html
</main>
```
with:
```html
  <section class="section" id="projects">
    <h2><span class="ru">Проекты</span><span class="en">Projects</span></h2>

    <div class="project-row">
      <span class="project-name">poly_fast_scan(polymarket-scanner):</span>
      <a class="project-link" href="https://github.com/MarselNet86/poly_fast_scan">https://github.com/MarselNet86/poly_fast_scan</a>
    </div>
    <div class="project-row">
      <span class="project-name">poly_start(polymarket-bot-starter):</span>
      <a class="project-link" href="https://github.com/MarselNet86/poly_start">https://github.com/MarselNet86/poly_start</a>
    </div>
    <div class="project-row">
      <span class="project-name">clever(surgpu-education-platform):</span>
      <a class="project-link" href="https://github.com/MarselNet86/Clever">https://github.com/MarselNet86/Clever</a>
    </div>
    <div class="project-row">
      <span class="project-name">trojan-vpn(vless-vpn-service):</span>
      <span class="project-private"><span class="ru">закрытый код</span><span class="en">private</span></span>
    </div>
    <div class="project-row">
      <span class="project-name">bashavtospec(logistics-landing):</span>
      <span class="project-private"><span class="ru">закрытый код</span><span class="en">private</span></span>
    </div>
    <div class="project-row">
      <span class="project-name">yaeast(cafe-menu-site):</span>
      <span class="project-private"><span class="ru">закрытый код</span><span class="en">private</span></span>
    </div>
    <div class="project-row">
      <span class="project-name">ssamurai(food-order-app):</span>
      <a class="project-link" href="https://surgut.ssamurai.ru/">https://surgut.ssamurai.ru/</a>
    </div>
  </section>
</main>
```

- [ ] **Step 2: Append project styles to `style.css`**

```css
.project-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 15px;
  margin-bottom: 6px;
}

.project-name {
  white-space: nowrap;
}

.project-private {
  color: var(--muted);
  font-style: italic;
}
```

- [ ] **Step 3: Verify content and toggle**

Run:
```bash
grep -q 'id="projects"' /Users/marsel.shamsutdinov/bio86/index.html && grep -q 'poly_fast_scan' /Users/marsel.shamsutdinov/bio86/index.html && grep -q 'surgut.ssamurai.ru' /Users/marsel.shamsutdinov/bio86/index.html && echo OK
```
Expected: `OK`

In the Browser pane, reload, confirm all 7 project rows render, the 3 links are clickable (check `href` via `read_page`), and "закрытый код"/"private" toggles with language.

- [ ] **Step 4: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add index.html style.css
git commit -m "Add Projects section"
```

---

### Task 7: Contacts section and footer

**Files:**
- Modify: `index.html` (insert new `<section>` and `<footer>` immediately before `</main>` / after `</main>`)
- Modify: `style.css` (append contacts/footer rules)

**Interfaces:**
- Consumes: `.section` rules from Task 3, `.ru`/`.en` toggle from Task 2.
- Produces: `.contact-row`, `.site-footer` classes (not reused elsewhere). This is the last content task — after this, `index.html`'s full section order is: header, about, skills, experience, projects, contacts, footer.

- [ ] **Step 1: Insert the Contacts section**

In `index.html`, replace:
```html
</main>
```
with:
```html
  <section class="section" id="contacts">
    <h2><span class="ru">Контакты</span><span class="en">Contacts</span></h2>
    <div class="contact-row">Telegram: <a href="https://t.me/marselnet">@marselnet</a></div>
    <div class="contact-row">Email: <a href="mailto:marsel.shamsutdinov@icloud.com">marsel.shamsutdinov@icloud.com</a></div>
    <div class="contact-row">GitHub: <a href="https://github.com/MarselNet86">github.com/MarselNet86</a></div>
  </section>
</main>
```

- [ ] **Step 2: Insert the footer**

In `index.html`, replace:
```html
<script src="script.js" defer></script>
```
with:
```html
<footer class="site-footer">© 2026 Марсель Шамсутдинов</footer>
<script src="script.js" defer></script>
```

- [ ] **Step 3: Append contacts/footer styles to `style.css`**

```css
.contact-row {
  margin-bottom: 6px;
  font-size: 15px;
}

.site-footer {
  margin-top: 40px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 13px;
  text-align: center;
}
```

- [ ] **Step 4: Verify content**

Run:
```bash
grep -q 'id="contacts"' /Users/marsel.shamsutdinov/bio86/index.html && grep -q 'site-footer' /Users/marsel.shamsutdinov/bio86/index.html && grep -q '@marselnet' /Users/marsel.shamsutdinov/bio86/index.html && echo OK
```
Expected: `OK`

In the Browser pane, reload, confirm Contacts section and footer render at the bottom of the page, all three contact links have correct `href`s.

- [ ] **Step 5: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add index.html style.css
git commit -m "Add Contacts section and footer"
```

---

### Task 8: Resume PDF asset

**Files:**
- Create: `assets/resume.pdf` (copy of the source resume)

**Interfaces:**
- Consumes: the `href="assets/resume.pdf"` download link created in Task 2's header markup.
- Produces: nothing consumed by later tasks — this is a leaf task.

- [ ] **Step 1: Copy the resume PDF into the project**

```bash
mkdir -p /Users/marsel.shamsutdinov/bio86/assets
cp "/Users/marsel.shamsutdinov/Desktop/Резюме/Шамсутдинов_Марсель_Резюме.pdf" /Users/marsel.shamsutdinov/bio86/assets/resume.pdf
```

- [ ] **Step 2: Verify the download link resolves**

Run:
```bash
test -f /Users/marsel.shamsutdinov/bio86/assets/resume.pdf && echo OK
```
Expected: `OK`

In the Browser pane, reload `index.html`, click "Скачать резюме (PDF)" and confirm the PDF downloads/opens without a 404.

- [ ] **Step 3: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add assets/resume.pdf
git commit -m "Add downloadable resume PDF"
```

---

### Task 9: Responsive layout polish

**Files:**
- Modify: `style.css` (append a mobile media query at the end of the file)

**Interfaces:**
- Consumes: all classes defined in Tasks 1–7.
- Produces: nothing consumed by later tasks — this is the last styling task.

- [ ] **Step 1: Append mobile styles to the end of `style.css`**

```css
@media (max-width: 480px) {
  body {
    padding: 24px 16px 60px;
    font-size: 15px;
  }

  .site-header h1 {
    font-size: 22px;
  }

  .skill-row {
    flex-direction: column;
    gap: 2px;
  }

  .skill-label {
    min-width: unset;
  }

  .project-row {
    flex-direction: column;
    gap: 2px;
  }
}
```

- [ ] **Step 2: Verify at mobile width**

In the Browser pane, use `resize_window` with `preset: "mobile"` (375×812), reload `index.html`, and confirm:
- No horizontal scrollbar appears.
- The header, skill rows, and project rows stack legibly without overlapping text.
- Take a screenshot to visually confirm.

Then resize back to `preset: "desktop"`.

- [ ] **Step 3: Commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add style.css
git commit -m "Add responsive mobile layout"
```

---

### Task 10: Full-site verification pass

**Files:**
- None created or modified — verification only. If any check fails, fix the relevant file from Tasks 1–9 and re-run this task's checks before committing.

**Interfaces:**
- Consumes: the complete site from Tasks 1–9.
- Produces: nothing — terminal task.

- [ ] **Step 1: Run the full grep-based content checklist**

```bash
cd /Users/marsel.shamsutdinov/bio86
grep -q 'Привет, я Марсель' index.html
grep -q "Hi, I'm Marsel" index.html
grep -q 'id="about"' index.html
grep -q 'id="skills"' index.html
grep -q 'id="experience"' index.html
grep -q 'id="projects"' index.html
grep -q 'id="contacts"' index.html
grep -q 'site-footer' index.html
test -f assets/resume.pdf
echo ALL_CHECKS_PASSED
```
Expected: `ALL_CHECKS_PASSED` with no grep failures above it.

- [ ] **Step 2: Manual browser walkthrough**

In the Browser pane, navigate to `file:///Users/marsel.shamsutdinov/bio86/index.html` and verify, in order:
1. Page loads with no console errors (`read_console_messages`, `onlyErrors: true` should return empty).
2. Theme toggle switches light ↔ dark and persists across a reload.
3. Language toggle switches ru ↔ en for every section (header, about, skills, experience, projects, contacts) and persists across a reload.
4. All project links (`poly_fast_scan`, `poly_start`, `Clever`, `ssamurai`) and contact links (Telegram, email, GitHub) have correct, non-empty `href` attributes (`read_page` with `filter: "interactive"`).
5. Resume PDF download link resolves to `assets/resume.pdf`.
6. At `375px` width (`resize_window`, `preset: "mobile"`), no horizontal overflow and all text remains legible.

- [ ] **Step 3: Fix any failures found**

If any check in Step 1 or Step 2 fails, edit the relevant file (`index.html`, `style.css`, or `script.js`) to fix it, then re-run both Step 1 and Step 2 before proceeding.

- [ ] **Step 4: Final commit**

```bash
cd /Users/marsel.shamsutdinov/bio86
git add -A
git status
```
If `git status` shows anything staged (fixes from Step 3), commit:
```bash
git commit -m "Fix issues found in full-site verification pass"
```
If nothing is staged, no commit is needed — the site is complete.
