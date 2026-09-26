"""Services and build-timeline SVGs, in the same 3D style as the cards and tech stack."""
import colorsys, html, pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "assets"
SANS = "'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'Courier New', monospace"
V, CY = "#7C5CFF", "#22D3EE"
e = html.escape


def dark(hexc, f):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(h, max(0, l * f), s)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


STYLE = """
  .fl { animation: fl 4s ease-in-out infinite; }
  @keyframes fl { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }
  .sh { animation: sh 4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
  @keyframes sh { 0%,100% { transform: scaleX(1); opacity: .45; } 50% { transform: scaleX(.8); opacity: .2; } }
  .fp { animation: fp 9s cubic-bezier(.45,0,.2,1) infinite; transform-box: fill-box; transform-origin: center; }
  @keyframes fp { 0%,78% { transform: scaleX(1) skewY(0); } 83% { transform: scaleX(.02) skewY(-12deg); } 88% { transform: scaleX(-1) skewY(0); }
                  93% { transform: scaleX(.02) skewY(12deg); } 98%,100% { transform: scaleX(1) skewY(0); } }
  .glow { animation: glow 6s ease-in-out infinite; }
  @keyframes glow { 0%,100% { opacity: .35; } 50% { opacity: .6; } }
"""

DEFS = f"""
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f1a"/><stop offset=".6" stop-color="#120d2b"/><stop offset="1" stop-color="#0b1a2b"/></linearGradient>
  <linearGradient id="face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#161d2e"/><stop offset="1" stop-color="#0f1420"/></linearGradient>
  <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".2"/><stop offset=".45" stop-color="#fff" stop-opacity=".03"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <radialGradient id="o1"><stop offset="0" stop-color="{V}" stop-opacity=".55"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></radialGradient>
  <radialGradient id="o2"><stop offset="0" stop-color="{CY}" stop-opacity=".35"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#fff" fill-opacity=".06"/></pattern>
  <filter id="bl" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="4"/></filter>
"""


def frame(w, h, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{STYLE}</style>
<defs>{DEFS}<clipPath id="c"><rect width="{w}" height="{h}" rx="20"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" fill="url(#dots)"/>
  <circle class="glow" cx="{w - 60}" cy="50" r="260" fill="url(#o1)"/>
  <circle class="glow" style="animation-delay:-3s" cx="70" cy="{h - 30}" r="230" fill="url(#o2)"/>
  {body}
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="19.5" fill="none" stroke="#fff" stroke-opacity=".1"/>
</svg>"""


def icon_tile(emoji, col, size, delay):
    r = size * .25
    return f"""<g class="fp" style="animation-delay:{delay:.2f}s">
    <rect y="{size * .12:.1f}" width="{size}" height="{size}" rx="{r}" fill="{dark(col, .4)}"/>
    <rect y="{size * .06:.1f}" width="{size}" height="{size}" rx="{r}" fill="{dark(col, .65)}"/>
    <rect width="{size}" height="{size}" rx="{r}" fill="#1c2233"/>
    <rect width="{size}" height="{size}" rx="{r}" fill="{col}" fill-opacity=".18"/>
    <text x="{size / 2}" y="{size * .68:.1f}" text-anchor="middle" font-size="{size * .48:.0f}">{emoji}</text>
    <rect width="{size}" height="{size}" rx="{r}" fill="url(#gloss)"/>
    <rect x=".5" y=".5" width="{size - 1}" height="{size - 1}" rx="{r - .5}" fill="none" stroke="{col}" stroke-opacity=".6"/>
  </g>"""


# ---------------- services ----------------
SERVICES = [
    ("🛍️", "Web Platforms", "#10B981", "Marketplaces, e-commerce and multi-tenant SaaS — from database schema to checkout."),
    ("🧩", "Dashboards & CMS", "#F59E0B", "Custom admin panels where every text, image and setting is editable without code."),
    ("📱", "Flutter Mobile Apps", "#22D3EE", "iOS & Android apps with clean state management, backed by a Laravel API."),
    ("💳", "Payment Integration", "#8B5CF6", "Stripe, PayPal, Paymob & Fawry — wallets, payouts, escrow and invoicing."),
    ("🔌", "APIs & Backends", "#FF2D20", "Secure REST APIs with Sanctum, queues, search and real-time notifications."),
    ("🌐", "Arabic-first & RTL", "#EC4899", "Bilingual AR / EN interfaces that feel native in both directions, dark mode included."),
]


def services():
    W, cols, cw, ch, gx, gy, x0, y0 = 920, 3, 272, 150, 22, 34, 25, 28
    rows = (len(SERVICES) + cols - 1) // cols
    H = y0 + rows * (ch + gy) + 6
    out = []
    for i, (emo, title, col, desc) in enumerate(SERVICES):
        r, c = divmod(i, cols)
        x, y, d = x0 + c * (cw + gx), y0 + r * (ch + gy), -(r * .5 + c * .35)
        lines = "".join(f'<text x="22" y="{96 + k * 19}">{e(l)}</text>' for k, l in enumerate(textwrap.wrap(desc, 36)[:3]))
        out.append(f"""<g transform="translate({x} {y})">
  <ellipse class="sh" style="animation-delay:{d:.2f}s" cx="{cw / 2}" cy="{ch + 16}" rx="{cw / 2 - 26}" ry="5" fill="{col}" filter="url(#bl)"/>
  <g class="fl" style="animation-delay:{d:.2f}s">
    <rect y="7" width="{cw}" height="{ch}" rx="16" fill="{dark(col, .35)}"/>
    <rect y="3.5" width="{cw}" height="{ch}" rx="16" fill="{dark(col, .5)}"/>
    <rect width="{cw}" height="{ch}" rx="16" fill="url(#face)"/>
    <rect width="{cw}" height="{ch}" rx="16" fill="{col}" fill-opacity=".06"/>
    <rect x=".5" y=".5" width="{cw - 1}" height="{ch - 1}" rx="15.5" fill="none" stroke="{col}" stroke-opacity=".35"/>
    <g transform="translate(22 18)">{icon_tile(emo, col, 44, i * .8)}</g>
    <text x="80" y="47" font-family="{SANS}" font-size="17" font-weight="700" fill="#f4f7fb">{e(title)}</text>
    <g font-family="{SANS}" font-size="13" fill="#a9b3c9">{lines}</g>
  </g>
</g>""")
    (A / "services.svg").write_text(frame(W, H, "".join(out)))


# ---------------- build timeline ----------------
# Month the repo was started (from GitHub repo creation dates).
TIMELINE = [
    ("May 2026", [("📦", "StockPro"), ("🛍️", "E-commerce Platform"), ("🧭", "SaaS PM Platform")]),
    ("Jun 2026", [("🏫", "NSIS School Platform"), ("🏛️", "Architecture Portfolio"), ("🧱", "GIO Supplies"),
                  ("🎨", "MotiGraph Agency"), ("📈", "Motigraph CRM"), ("🪙", "Coin Tycoon"),
                  ("🌸", "Anemone Cosmetics"), ("🍔", "Wasel (Flutter)")]),
    ("Jul 2026", [("💈", "MS Saloon"), ("🧘", "Aura Wellness"), ("🎓", "Moti-Graph Academy")]),
    ("Sep 2026", [("🛒", "SHADO Marketplace")]),
]
MONTH_COL = ["#FF2D20", "#F59E0B", "#22D3EE", "#10B981"]


def timeline():
    W, x0, colw, top = 920, 30, 215, 96
    most = max(len(p) for _, p in TIMELINE)
    H = top + most * 44 + 30
    out = [f'<line x1="40" x2="{W - 40}" y1="52" y2="52" stroke="#fff" stroke-opacity=".12" stroke-width="3" stroke-linecap="round"/>',
           f'<line class="run" x1="40" x2="{W - 40}" y1="52" y2="52" stroke="url(#run)" stroke-width="3" stroke-linecap="round"/>']
    for m, (month, projects) in enumerate(TIMELINE):
        col, cx = MONTH_COL[m], x0 + m * colw + colw / 2
        out.append(f"""<g transform="translate({cx} 52)">
  <circle class="pl" style="animation-delay:{m * .6:.1f}s" r="16" fill="{col}" fill-opacity=".25"/>
  <circle r="9" fill="{dark(col, .5)}"/><circle r="7" cy="-1.5" fill="{col}"/>
</g>
<text x="{cx}" y="28" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{col}">{month.upper()}</text>
<text x="{cx}" y="84" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#8b95ab">{len(projects)} project{"s" if len(projects) > 1 else ""} started</text>""")
        for k, (emo, name) in enumerate(projects):
            x, y, w = x0 + m * colw + 10, top + k * 44, colw - 20
            d = -(m * .4 + k * .25)
            out.append(f"""<g transform="translate({x} {y})"><g class="fl" style="animation-delay:{d:.2f}s">
  <rect y="5" width="{w}" height="34" rx="10" fill="{dark(col, .35)}"/>
  <rect width="{w}" height="34" rx="10" fill="url(#face)"/>
  <rect x=".5" y=".5" width="{w - 1}" height="33" rx="9.5" fill="none" stroke="{col}" stroke-opacity=".45"/>
  <rect width="{w}" height="34" rx="10" fill="url(#gloss)"/>
  <text x="14" y="22.5" font-size="14">{emo}</text>
  <text x="40" y="22" font-family="{SANS}" font-size="13" font-weight="600" fill="#e5e7eb">{e(name)}</text>
</g></g>""")
    body = "".join(out)
    svg = frame(W, H, body).replace("</style>", """
  .run { stroke-dasharray: 140 2000; animation: run 5s linear infinite; }
  @keyframes run { from { stroke-dashoffset: 140; } to { stroke-dashoffset: -900; } }
  .pl { animation: pl 2.4s ease-out infinite; transform-box: fill-box; transform-origin: center; }
  @keyframes pl { 0% { transform: scale(.6); opacity: .9; } 100% { transform: scale(1.8); opacity: 0; } }
</style>""").replace("</defs>", f"""<linearGradient id="run" gradientUnits="userSpaceOnUse" x1="40" x2="880"><stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{CY}"/></linearGradient></defs>""")
    (A / "timeline.svg").write_text(svg)


if __name__ == "__main__":
    services()
    timeline()
