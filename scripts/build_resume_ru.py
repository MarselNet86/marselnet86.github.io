from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, HRFlowable
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", "/System/Library/Fonts/Supplemental/Arial Italic.ttf"))

ACCENT = colors.HexColor("#0f6f6f")
MUTED = colors.HexColor("#555555")
TEXT = colors.HexColor("#111111")

styles = getSampleStyleSheet()

name_style = ParagraphStyle(
    "Name", parent=styles["Normal"], fontName="Arial-Bold",
    fontSize=20, leading=24, textColor=TEXT, spaceAfter=4,
)
role_style = ParagraphStyle(
    "Role", parent=styles["Normal"], fontName="Arial-Bold",
    fontSize=12.5, leading=16, textColor=ACCENT, spaceAfter=6,
)
meta_style = ParagraphStyle(
    "Meta", parent=styles["Normal"], fontName="Arial",
    fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=2,
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Normal"], fontName="Arial-Bold",
    fontSize=12, leading=15, textColor=ACCENT, spaceBefore=12, spaceAfter=5,
)
h3_style = ParagraphStyle(
    "H3", parent=styles["Normal"], fontName="Arial-Bold",
    fontSize=10.5, leading=13, textColor=TEXT, spaceBefore=7, spaceAfter=2,
)
h3sub_style = ParagraphStyle(
    "H3Sub", parent=styles["Normal"], fontName="Arial-Bold",
    fontSize=10, leading=13, textColor=TEXT, spaceBefore=5, spaceAfter=2,
)
meta_small = ParagraphStyle(
    "MetaSmall", parent=styles["Normal"], fontName="Arial-Italic",
    fontSize=9, leading=12, textColor=MUTED, spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"], fontName="Arial",
    fontSize=9.5, leading=13, textColor=TEXT, spaceAfter=3,
)
bullet_style = ParagraphStyle(
    "Bullet", parent=body_style, leftIndent=10, spaceAfter=2,
)
stack_style = ParagraphStyle(
    "Stack", parent=styles["Normal"], fontName="Arial-Italic",
    fontSize=8.5, leading=11, textColor=ACCENT, spaceAfter=7,
)
skill_label_style = ParagraphStyle(
    "SkillLabel", parent=styles["Normal"], fontName="Arial-Bold",
    fontSize=9.5, leading=13, textColor=TEXT,
)
skill_list_style = ParagraphStyle(
    "SkillList", parent=styles["Normal"], fontName="Arial",
    fontSize=9.5, leading=13, textColor=MUTED,
)

doc = SimpleDocTemplate(
    "/Users/marsel.shamsutdinov/bio86/assets/resume.pdf",
    pagesize=A4,
    topMargin=16 * mm, bottomMargin=14 * mm,
    leftMargin=18 * mm, rightMargin=18 * mm,
    title="Шамсутдинов Марсель - Резюме",
)

story = []

def hr():
    story.append(HRFlowable(width="100%", thickness=0.8, color=ACCENT, spaceBefore=4, spaceAfter=8))

def h2(text):
    story.append(Paragraph(text.upper(), h2_style))

def bullets(items):
    for it in items:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{it}", bullet_style))

story.append(Paragraph("Шамсутдинов Марсель Русланович", name_style))
story.append(Paragraph("Fullstack / Backend Developer (Python) &middot; DevOps", role_style))
story.append(Paragraph("Башкортостан &middot; открыт к удалённой работе", meta_style))
story.append(Paragraph(
    "Telegram: @marselnet &middot; marsel.shamsutdinov@icloud.com &middot; GitHub: github.com/MarselNet86",
    meta_style,
))
hr()

h2("Обо мне")
story.append(Paragraph(
    "Fullstack/Backend-разработчик (Python) с коммерческим опытом с 2024 года: от мобильной "
    "разработки на Flutter до серверных систем на Django и FastAPI и инфраструктурных решений на "
    "Docker и nginx. Разрабатывал ERP-систему автоматизации нарядов-допусков, Telegram-ботов для "
    "внутренних процессов, торгового бота для предикт-биржи Polymarket и клиентский VPN-сервис — "
    "от архитектуры до продакшена. Быстро вникаю в новый стек и довожу продукт от идеи до релиза "
    "самостоятельно, без выделенной команды.",
    body_style,
))

h2("Навыки")
skills = [
    ("Backend", "Python, Django, FastAPI, Celery, Aiogram, SQLAlchemy, LDAP"),
    ("Базы данных", "PostgreSQL, Redis, OracleSQL"),
    ("Frontend / Mobile", "Flutter, Dart, React, JavaScript, HTMX, Tailwind CSS, Bootstrap"),
    ("DevOps / Инфраструктура", "Docker, Git, Nginx, Caddy, VLESS, XRAY, Marzban API, Remnawave API, CDN-fronting"),
    ("Данные и Web3", "Pandas, NumPy, Dash, Plotly, web3.py, eth-account, EIP-712, py-clob-client"),
    ("Интеграции и API", "REST API, Telegram Bot API, YooKassa API, LDAP"),
]
skill_table_data = [[Paragraph(label, skill_label_style), Paragraph(items, skill_list_style)] for label, items in skills]
skill_table = Table(skill_table_data, colWidths=[45 * mm, 122 * mm])
skill_table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
]))
story.append(skill_table)

h2("Опыт работы")

story.append(Paragraph("Daimon Group", h3_style))
story.append(Paragraph("Основатель &middot; Python / DevOps &nbsp;&nbsp;|&nbsp;&nbsp; Янв 2026 &ndash; н.в. &middot; Удалённо", meta_small))

story.append(Paragraph("Trojan VPN &mdash; сервис для обхода блокировок в РФ", h3sub_style))
story.append(Paragraph("Мар 2026 &ndash; н.в.", meta_small))
bullets([
    "Разработал VPN-сервис на протоколе VLESS с использованием XRAY и Marzban / Remnawave API "
    "для управления пользователями и конфигурациями — 3 сервера, до 1000 клиентов",
    "Настроил каскадную маскировку трафика через XHTTP и CDN-fronting: западный трафик "
    "маскируется под легитимный российский, что обеспечивает обход блокировок ТСПУ и DPI",
    "Реализовал приём платежей через YooKassa API и Telegram-бота на Aiogram для оформления "
    "подписок и выдачи доступа",
    "Разработал веб-интерфейс личного кабинета на React",
])
story.append(Paragraph(
    "Стек: Remnawave API, XRAY, Docker, Git, VLESS, Marzban API, Caddy, Nginx, React, Aiogram, "
    "YooKassa API, CDN-fronting, FastAPI", stack_style,
))

story.append(Paragraph("Бот для поиска неэффективностей на предикт-бирже Polymarket", h3sub_style))
story.append(Paragraph("Янв 2026 &ndash; Мар 2026", meta_small))
bullets([
    "Разработал дашборд на Dash / Plotly для анализа рынков SOL, BTC, ETH, XRP: сравнение "
    "расхождений графиков между Polymarket и Binance, отслеживание объёмов и анализ "
    "исторических данных",
    "Настроил постоянный сбор данных по стаканам Polymarket через WebSocket с автоматическим "
    "переключением на REST API при обрыве соединения — до восстановления WebSocket-сессии",
    "Реализовал Django-приложение для мониторинга крупных игроков рынка и управления "
    "proxy-кошельками",
    "Построил торговую модель на базе py-clob-client и web3.py с подписанием ордеров по "
    "стандарту EIP-712, реализовал скрипт автоматического скальпинга на 15-минутных опционах",
])
story.append(Paragraph(
    "Стек: Python, py-clob-client (Polymarket CLOB API), web3.py, eth-account, EIP-712, Django, "
    "Dash, Plotly, Pandas, NumPy, Pydantic, httpx", stack_style,
))

story.append(Paragraph("ПАО «Ростелеком»", h3_style))
story.append(Paragraph("Python / Web Developer &nbsp;&nbsp;|&nbsp;&nbsp; Дек 2024 &ndash; Дек 2025 &middot; Сургут", meta_small))
story.append(Paragraph(
    "Разработчик внутренней ERM-системы и Telegram-ботов для автоматизации процессов и "
    "уведомлений по заявкам.", body_style,
))
bullets([
    "Разработал B2C Telegram-бота (XRT) с мини-приложением для контроля заявок: сроки, "
    "уведомления об упущенных, статистика по дому. Использовался всем Сургутским районом (до "
    "30 заявок в день) вместо громоздкой CRM ARGUS, недоступной мастеру в поле без ноутбука — "
    "Python, Aiogram, LDAP, Celery",
    "Разрабатывал ERP-систему автоматизации нарядов-допусков для Сургутского района, "
    "реализовал ключевые модули — Python, Django, Celery, LDAP, Redis, PostgreSQL, JS, Docker, "
    "Git, Tailwind CSS",
    "Создал Telegram-бота для уведомления о новых нарядах WFM — Python, Aiogram, LDAP, "
    "SQLAlchemy, PostgreSQL, OracleSQL, Git",
    "Разработал внутренние инструменты для сотрудников: скрипт анализа эффективности "
    "работников по участкам, бот для получения данных из БД компании при сбоях основной "
    "системы, геокодер для перевода координат из xlsx в точки на карте — Python, Django, "
    "Flask, LDAP, OracleSQL",
])

story.append(Paragraph("Фриланс-проекты", h3_style))
story.append(Paragraph("Веб-разработка вне основной занятости &nbsp;&nbsp;|&nbsp;&nbsp; 2025 &middot; Сургут", meta_small))

story.append(Paragraph("Сайт-меню кафе «ЯЕсть»", h3sub_style))
story.append(Paragraph(
    "Проект по рекомендации директора филиала ПАО «Ростелеком» в г. Сургут — разработка "
    "веб-сайта для отображения меню кафе.", body_style,
))
story.append(Paragraph("Стек: Python, Django, PostgreSQL, JavaScript, HTMX, Docker, Git, Bootstrap", stack_style))

story.append(Paragraph("Образовательная платформа для СурГПУ", h3sub_style))
story.append(Paragraph(
    "Разработана совместно с преподавателем для конкурса — образовательная платформа для "
    "студентов.", body_style,
))
story.append(Paragraph("Стек: Python, Django, PostgreSQL, Pillow, Gunicorn, Docker, Nginx, JavaScript", stack_style))

story.append(Paragraph("Лендинг для логистической компании «БашАвтоСпец»", h3sub_style))
story.append(Paragraph("Разработка landing-страницы для логистической компании.", body_style))
story.append(Paragraph("Стек: Python, Django, Tailwind CSS, DaisyUI, JavaScript", stack_style))

story.append(Paragraph("ООО «Сытый самурай»", h3_style))
story.append(Paragraph("Мобильный разработчик &middot; Flutter Developer &nbsp;&nbsp;|&nbsp;&nbsp; Фев 2024 &ndash; Май 2024 &middot; Сургут", meta_small))
story.append(Paragraph("Разработка мобильного приложения для системы заказов еды на Flutter и Dart.", body_style))
bullets([
    "Реализовал функционал авторизации и регистрации по номеру телефона, интеграцию с API "
    "(аутентификация, БД, хранение изображений)",
    "Спроектировал архитектуру клиентского приложения, внедрил поддержку тёмной темы, экраны "
    "корзины, товаров, профиля и заказов",
    "Разработал приложение для Android TV — отображение статусов заказов и оставшегося "
    "времени на их выполнение",
    "Разработал приложение для планшетов — отслеживание заказов на кухне в режиме реального "
    "времени",
])
story.append(Paragraph("Стек: Flutter, Dart, REST API", stack_style))

h2("Образование")
story.append(Paragraph("СурГУ", h3sub_style))
story.append(Paragraph("Высшее образование &middot; Программная инженерия &middot; 1 курс (обучение продолжается)", body_style))
story.append(Paragraph("АУ «Сургутский политехнический колледж», г. Сургут", h3sub_style))
story.append(Paragraph("Среднее профессиональное образование &middot; 09.02.07 &mdash; Информационные системы и программирование", body_style))

h2("Языки")
story.append(Paragraph("Русский &mdash; родной &middot; Английский &mdash; начальный", body_style))

doc.build(story)
print("done")
