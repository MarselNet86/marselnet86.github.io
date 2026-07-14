from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib import colors

ACCENT = colors.HexColor("#0f6f6f")
MUTED = colors.HexColor("#555555")
TEXT = colors.HexColor("#111111")

styles = getSampleStyleSheet()

name_style = ParagraphStyle(
    "Name", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=20, leading=24, textColor=TEXT, spaceAfter=4,
)
role_style = ParagraphStyle(
    "Role", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=12.5, leading=16, textColor=ACCENT, spaceAfter=6,
)
meta_style = ParagraphStyle(
    "Meta", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=2,
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=ACCENT, spaceBefore=12, spaceAfter=5,
    letterSpacing=0.5,
)
h3_style = ParagraphStyle(
    "H3", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=10.5, leading=13, textColor=TEXT, spaceBefore=7, spaceAfter=2,
)
h3sub_style = ParagraphStyle(
    "H3Sub", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=10, leading=13, textColor=TEXT, spaceBefore=5, spaceAfter=2,
)
meta_small = ParagraphStyle(
    "MetaSmall", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=9, leading=12, textColor=MUTED, spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9.5, textColor=TEXT, leading=13, spaceAfter=3,
)
bullet_style = ParagraphStyle(
    "Bullet", parent=body_style, leftIndent=10, bulletIndent=0, spaceAfter=2,
)
stack_style = ParagraphStyle(
    "Stack", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=8.5, leading=11, textColor=ACCENT, spaceAfter=7,
)
skill_label_style = ParagraphStyle(
    "SkillLabel", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=9.5, leading=13, textColor=TEXT,
)
skill_list_style = ParagraphStyle(
    "SkillList", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9.5, leading=13, textColor=MUTED,
)

doc = SimpleDocTemplate(
    "/Users/marsel.shamsutdinov/bio86/assets/resume-en.pdf",
    pagesize=A4,
    topMargin=16 * mm, bottomMargin=14 * mm,
    leftMargin=18 * mm, rightMargin=18 * mm,
    title="Marsel Shamsutdinov - Resume",
)

story = []

def hr():
    story.append(HRFlowable(width="100%", thickness=0.8, color=ACCENT, spaceBefore=4, spaceAfter=8))

def h2(text):
    story.append(Paragraph(text.upper(), h2_style))

def bullets(items):
    for it in items:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{it}", bullet_style))

story.append(Paragraph("Marsel Shamsutdinov", name_style))
story.append(Paragraph("Fullstack / Backend Developer (Python) &middot; DevOps", role_style))
story.append(Paragraph("Bashkortostan &middot; open to remote work", meta_style))
story.append(Paragraph(
    "Telegram: @marselnet &middot; marsel.shamsutdinov@icloud.com &middot; GitHub: github.com/MarselNet86",
    meta_style,
))
hr()

h2("About me")
story.append(Paragraph(
    "Fullstack/backend developer (Python) with commercial experience since 2024: from mobile "
    "development in Flutter to server systems in Django and FastAPI, and infrastructure solutions "
    "in Docker and nginx. Built an ERP system for work-permit automation, Telegram bots for internal "
    "processes, a trading bot for the Polymarket prediction market, and a client VPN service &mdash; "
    "from architecture to production. I quickly get up to speed on new stacks and take a product from "
    "idea to release on my own, without a dedicated team.",
    body_style,
))

h2("Skills")
skills = [
    ("Backend", "Python, Django, FastAPI, Celery, Aiogram, SQLAlchemy, LDAP"),
    ("Databases", "PostgreSQL, Redis, OracleSQL"),
    ("Frontend / Mobile", "Flutter, Dart, React, JavaScript, HTMX, Tailwind CSS, Bootstrap"),
    ("DevOps / Infrastructure", "Docker, Git, Nginx, Caddy, VLESS, XRAY, Marzban API, Remnawave API, CDN-fronting"),
    ("Data & Web3", "Pandas, NumPy, Dash, Plotly, web3.py, eth-account, EIP-712, py-clob-client"),
    ("Integrations & APIs", "REST API, Telegram Bot API, YooKassa API, LDAP"),
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

h2("Work experience")

story.append(Paragraph("Daimon Group", h3_style))
story.append(Paragraph("Founder &middot; Python / DevOps &nbsp;&nbsp;|&nbsp;&nbsp; Jan 2026 &ndash; present &middot; Remote", meta_small))

story.append(Paragraph("Trojan VPN &mdash; a censorship-circumvention VPN service for Russia", h3sub_style))
story.append(Paragraph("Mar 2026 &ndash; present", meta_small))
bullets([
    "Built a VPN service on the VLESS protocol using XRAY and the Marzban/Remnawave API for user and "
    "configuration management &mdash; 3 servers, up to 1000 clients",
    "Configured cascading traffic masking via XHTTP and CDN-fronting: Western traffic is disguised as "
    "legitimate Russian traffic, bypassing TSPU and DPI blocking",
    "Implemented payments via the YooKassa API and a Telegram bot on Aiogram for subscription "
    "management and access provisioning",
    "Built a React web dashboard for the personal account area",
])
story.append(Paragraph(
    "Stack: Remnawave API, XRAY, Docker, Git, VLESS, Marzban API, Caddy, Nginx, React, Aiogram, "
    "YooKassa API, CDN-fronting, FastAPI", stack_style,
))

story.append(Paragraph("Bot for finding inefficiencies on the Polymarket prediction exchange", h3sub_style))
story.append(Paragraph("Jan 2026 &ndash; Mar 2026", meta_small))
bullets([
    "Built a Dash/Plotly dashboard for analyzing SOL, BTC, ETH, XRP markets: comparing chart "
    "discrepancies between Polymarket and Binance, tracking volumes, and analyzing historical data",
    "Set up continuous Polymarket order-book data collection via WebSocket with automatic fallback to "
    "REST API on disconnect &mdash; until the WebSocket session is restored",
    "Built a Django app for monitoring large market players and managing proxy wallets",
    "Built a trading model on py-clob-client and web3.py with EIP-712 order signing; implemented an "
    "automated scalping script on 15-minute options",
])
story.append(Paragraph(
    "Stack: Python, py-clob-client (Polymarket CLOB API), web3.py, eth-account, EIP-712, Django, Dash, "
    "Plotly, Pandas, NumPy, Pydantic, httpx", stack_style,
))

story.append(Paragraph("PJSC Rostelecom", h3_style))
story.append(Paragraph("Python / Web Developer &nbsp;&nbsp;|&nbsp;&nbsp; Dec 2024 &ndash; Dec 2025 &middot; Surgut", meta_small))
story.append(Paragraph(
    "Developer of an internal ERM system and Telegram bots for automating processes and request "
    "notifications.", body_style,
))
bullets([
    "Built a B2C Telegram bot (XRT) with a mini-app for tracking service requests: deadlines, "
    "missed-request alerts, per-building statistics. Used across the whole Surgut district (up to 30 "
    "requests/day) in place of the cumbersome ARGUS CRM, which field technicians couldn't access "
    "without a laptop &mdash; Python, Aiogram, LDAP, Celery",
    "Developed an ERP system automating work permits for the Surgut district, built key modules &mdash; "
    "Python, Django, Celery, LDAP, Redis, PostgreSQL, JS, Docker, Git, Tailwind CSS",
    "Built a Telegram bot notifying staff of new WFM work orders &mdash; Python, Aiogram, LDAP, "
    "SQLAlchemy, PostgreSQL, OracleSQL, Git",
    "Built internal tools for employees: a script analyzing staff efficiency by district, a bot for "
    "retrieving company database data during main-system outages, a geocoder converting coordinates "
    "from xlsx into map points &mdash; Python, Django, Flask, LDAP, OracleSQL",
])

story.append(Paragraph("Freelance Projects", h3_style))
story.append(Paragraph("Web development outside primary employment &nbsp;&nbsp;|&nbsp;&nbsp; 2025 &middot; Surgut", meta_small))

story.append(Paragraph('Caf&eacute; menu website &ldquo;YaYest&rdquo;', h3sub_style))
story.append(Paragraph(
    "A project referred by the branch director of PJSC Rostelecom in Surgut &mdash; building a website "
    "to display a caf&eacute;'s menu.", body_style,
))
story.append(Paragraph("Stack: Python, Django, PostgreSQL, JavaScript, HTMX, Docker, Git, Bootstrap", stack_style))

story.append(Paragraph("Education platform for SurSPU", h3sub_style))
story.append(Paragraph(
    "Built together with a lecturer for a competition &mdash; an education platform for students.",
    body_style,
))
story.append(Paragraph("Stack: Python, Django, PostgreSQL, Pillow, Gunicorn, Docker, Nginx, JavaScript", stack_style))

story.append(Paragraph('Landing page for logistics company &ldquo;BashAvtoSpec&rdquo;', h3sub_style))
story.append(Paragraph("Built a landing page for a logistics company.", body_style))
story.append(Paragraph("Stack: Python, Django, Tailwind CSS, DaisyUI, JavaScript", stack_style))

story.append(Paragraph('LLC &ldquo;Sytiy Samurai&rdquo;', h3_style))
story.append(Paragraph("Mobile Developer &middot; Flutter Developer &nbsp;&nbsp;|&nbsp;&nbsp; Feb 2024 &ndash; May 2024 &middot; Surgut", meta_small))
story.append(Paragraph("Development of a mobile app for a food-ordering system in Flutter and Dart.", body_style))
bullets([
    "Implemented phone-number authentication and registration, API integration (auth, database, image "
    "storage)",
    "Designed the client app architecture, added dark theme support, cart/product/profile/order "
    "screens",
    "Built an Android TV app &mdash; displaying order statuses and remaining preparation time",
    "Built a tablet app &mdash; real-time kitchen order tracking",
])
story.append(Paragraph("Stack: Flutter, Dart, REST API", stack_style))

h2("Education")
story.append(Paragraph("Surgut State University", h3sub_style))
story.append(Paragraph("Higher education &middot; Software Engineering &middot; 1st year (ongoing)", body_style))
story.append(Paragraph("Surgut Polytechnic College", h3sub_style))
story.append(Paragraph("Vocational education &middot; 09.02.07 &mdash; Information Systems and Programming", body_style))

h2("Languages")
story.append(Paragraph("Russian &mdash; native &middot; English &mdash; beginner", body_style))

doc.build(story)
print("done")
