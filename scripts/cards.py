import textwrap, os, html
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
R = str(ROOT / "assets")
os.makedirs(R + "/projects", exist_ok=True)
SANS = "'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'Courier New', monospace"
V, CY = "#7C5CFF", "#22D3EE"
e = html.escape

# ---------------- animated header ----------------
header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340">
<style>
  .orb {{ animation: float 9s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  .o2 {{ animation-duration: 12s; animation-delay: -4s; }}
  .o3 {{ animation-duration: 15s; animation-delay: -7s; }}
  @keyframes float {{ 0%,100% {{ transform: translate(0,0) scale(1); }} 50% {{ transform: translate(-30px,18px) scale(1.12); }} }}
  .up {{ animation: up .9s cubic-bezier(.2,.7,.2,1) backwards; }}
  .d1 {{ animation-delay: .15s; }} .d2 {{ animation-delay: .45s; }} .d3 {{ animation-delay: .75s; }} .d4 {{ animation-delay: 1.05s; }}
  @keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .bar {{ animation: grow 1.2s .6s cubic-bezier(.2,.7,.2,1) both; transform-origin: left; transform-box: fill-box; }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  .cur {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .shine {{ animation: shine 6s linear infinite; }}
  @keyframes shine {{ from {{ transform: translateX(-400px); }} to {{ transform: translateX(1600px); }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f1a"/><stop offset=".6" stop-color="#120d2b"/><stop offset="1" stop-color="#0b1a2b"/></linearGradient>
  <linearGradient id="ac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{CY}"/></linearGradient>
  <linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#fff" fill-opacity=".07"/></pattern>
  <clipPath id="c"><rect width="1200" height="340" rx="22"/></clipPath>
</defs>
<g clip-path="url(#c)">
  <rect width="1200" height="340" fill="url(#bg)"/>
  <rect width="1200" height="340" fill="url(#dots)"/>
  <circle class="orb" cx="980" cy="90" r="150" fill="{V}" opacity=".55" filter="url(#blur)"/>
  <circle class="orb o2" cx="1120" cy="280" r="110" fill="{CY}" opacity=".35" filter="url(#blur)"/>
  <circle class="orb o3" cx="760" cy="330" r="90" fill="#FF2D20" opacity=".18" filter="url(#blur)"/>
  <rect class="shine" x="0" y="0" width="300" height="340" fill="url(#sh)" transform="skewX(-20)"/>

  <!-- floating code window -->
  <g transform="translate(820,70)" class="up d4">
    <rect width="310" height="200" rx="14" fill="#0d1117" fill-opacity=".82" stroke="#ffffff" stroke-opacity=".1"/>
    <circle cx="22" cy="22" r="6" fill="#ff5f57"/><circle cx="42" cy="22" r="6" fill="#febc2e"/><circle cx="62" cy="22" r="6" fill="#28c840"/>
    <text x="290" y="27" text-anchor="end" font-family="{MONO}" font-size="12" fill="#6b7280">routes/web.php</text>
    <g font-family="{MONO}" font-size="14">
      <text x="22" y="66"><tspan fill="#c678dd">Route</tspan><tspan fill="#e5e7eb">::</tspan><tspan fill="#61afef">get</tspan><tspan fill="#e5e7eb">(</tspan><tspan fill="#98c379">'/idea'</tspan><tspan fill="#e5e7eb">,</tspan></text>
      <text x="38" y="90"><tspan fill="#c678dd">fn</tspan><tspan fill="#e5e7eb">() =&gt; </tspan><tspan fill="#61afef">ship</tspan><tspan fill="#e5e7eb">(</tspan></text>
      <text x="54" y="114"><tspan fill="#e5c07b">web</tspan><tspan fill="#e5e7eb">: </tspan><tspan fill="#FF6B5B">Laravel</tspan><tspan fill="#e5e7eb">,</tspan></text>
      <text x="54" y="138"><tspan fill="#e5c07b">app</tspan><tspan fill="#e5e7eb">: </tspan><tspan fill="#54C5F8">Flutter</tspan><tspan fill="#e5e7eb">,</tspan></text>
      <text x="38" y="162" fill="#e5e7eb">));<tspan class="cur" fill="{CY}"> ▍</tspan></text>
    </g>
  </g>

  <text class="up d1" x="72" y="100" font-family="{MONO}" font-size="18" fill="{CY}">// hello world, I'm</text>
  <text class="up d2" x="70" y="172" font-family="{SANS}" font-size="64" font-weight="800" fill="#f4f7fb" letter-spacing="-1">Alaa Abdelnasser</text>
  <rect class="bar" x="73" y="192" width="180" height="6" rx="3" fill="url(#ac)"/>
  <text class="up d3" x="72" y="242" font-family="{SANS}" font-size="27" font-weight="600" fill="#d7dcf0">Full-Stack <tspan fill="#FF6B5B">Laravel</tspan> &amp; <tspan fill="#54C5F8">Flutter</tspan> Developer</text>
  <g class="up d4" font-family="{SANS}" font-size="16" fill="#aab3c8">
    <rect x="72" y="266" width="186" height="34" rx="17" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".12"/>
    <text x="165" y="288" text-anchor="middle">💼  predev. Solutions</text>
    <rect x="270" y="266" width="160" height="34" rx="17" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".12"/>
    <text x="350" y="288" text-anchor="middle">📍  Cairo, Egypt</text>
    <rect x="442" y="266" width="210" height="34" rx="17" fill="{V}" fill-opacity=".18" stroke="{V}" stroke-opacity=".6"/>
    <text x="547" y="288" text-anchor="middle" fill="#e4dcff">🚀  16+ products built</text>
  </g>
</g>
</svg>'''
open(R + "/header.svg", "w").write(header)

# ---------------- project cards ----------------
P = [
 ("shado", "🛒", "SHADO Online Trading", "Multi-Vendor Marketplace", "#10B981",
  "Many shops, one basket, one checkout — the buyer's money is held in escrow until the parcel arrives. Guest checkout, multi-currency, per-seller shipping.",
  ["Laravel 13", "Meilisearch", "Escrow", "455 tests"]),
 ("crm", "📈", "Motigraph CRM", "Business CRM", "#F59E0B",
  "Bilingual AR/EN CRM for a creative studio — drag-and-drop deals pipeline, client health scores, client portal and real-time notifications.",
  ["Laravel 13", "Bootstrap RTL", "PWA", "Kanban"]),
 ("lms", "🎓", "Moti-Graph Academy", "Learning Platform", "#8B5CF6",
  "Full LMS with courses, quizzes, exams, certificates, wallets & instructor payouts, coupons, bundles and a built-in AI assistant.",
  ["Livewire 3", "Stripe", "Paymob", "Fawry"]),
 ("school", "🏫", "NSIS International School", "Multi-Tenant Platform", "#3B82F6",
  "One codebase and one admin panel running two independent schools — American 🇺🇸 and British 🇬🇧 — each with its own content and branding.",
  ["Laravel 12", "Multi-tenant", "CMS", "i18n"]),
 ("saas", "🧭", "SaaS PM Platform", "Project Management SaaS", "#EC4899",
  "Multi-tenant project management with workspaces, AI assistance, real-time collaboration and enterprise-grade security.",
  ["Laravel 12", "Livewire 4", "Tailwind v4", "AI"]),
 ("aura", "🧘", "Aura Wellness", "Mobile App + API", "#22D3EE",
  "Meditation & wellness app — a 22-screen Flutter client with audio playback, backed by a Laravel API and admin dashboard.",
  ["Flutter", "Riverpod", "Sanctum API", "just_audio"]),
 ("saloon", "💈", "MS Saloon", "Business Website", "#EAB308",
  "Arabic RTL barbershop site with bookings, branch maps, barbers, offers & memberships — every word editable from a custom dashboard.",
  ["Laravel 13", "RTL", "Bookings", "CMS"]),
 ("stockpro", "📦", "StockPro", "Inventory & Sales", "#F43F5E",
  "Inventory and sales management for small businesses — products, stock movements, invoices, reports and a REST API.",
  ["Laravel 11", "Livewire 3", "REST API", "Reports"]),
]
import colorsys
def dark(hexc, f):
    r, g, b = (int(hexc[i:i+2], 16) / 255 for i in (1, 3, 5))
    h, l, s_ = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(h, max(0, l * f), s_)
    return "#%02x%02x%02x" % (int(r*255), int(g*255), int(b*255))

W, H = 440, 230          # card face
PAD, EDGE = 10, 9        # headroom for float, 3D edge depth
CW, CH = W, H + PAD + EDGE + 16
for n, (slug, icon, name, kind, col, desc, tags) in enumerate(P):
    dl_ = -(n * 0.55)
    lines = textwrap.wrap(desc, 58)[:4]
    dl = "".join(f'<text x="26" y="{112+i*22}">{e(l)}</text>' for i, l in enumerate(lines))
    x, tg = 26, ""
    for t in tags:
        w = int(len(t) * 7.4 + 22)
        tg += f'<rect x="{x}" y="{H-44}" width="{w}" height="24" rx="12" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".45"/><text x="{x+w/2}" y="{H-27.5}" text-anchor="middle">{e(t)}</text>'
        x += w + 8
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">
<style>
  .fl {{ animation: fl 4.2s ease-in-out infinite; animation-delay: {dl_:.2f}s; }}
  @keyframes fl {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-{PAD}px); }} }}
  .sh {{ animation: sh 4.2s ease-in-out infinite; animation-delay: {dl_:.2f}s; transform-box: fill-box; transform-origin: center; }}
  @keyframes sh {{ 0%,100% {{ transform: scaleX(1); opacity: .45; }} 50% {{ transform: scaleX(.86); opacity: .2; }} }}
  .if {{ animation: if 3.2s ease-in-out infinite; animation-delay: {dl_*1.3:.2f}s; }}
  @keyframes if {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-4px); }} }}
  .fp {{ animation: fp 9s cubic-bezier(.45,0,.2,1) infinite; animation-delay: {n*0.7:.2f}s; transform-box: fill-box; transform-origin: center; }}
  @keyframes fp {{ 0%,78% {{ transform: scaleX(1) skewY(0); }} 83% {{ transform: scaleX(.02) skewY(-12deg); }} 88% {{ transform: scaleX(-1) skewY(0); }}
                   93% {{ transform: scaleX(.02) skewY(12deg); }} 98%,100% {{ transform: scaleX(1) skewY(0); }} }}
  .g {{ animation: pulse 4s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: .6; }} }}
  .sw {{ animation: sw 7s ease-in-out infinite; animation-delay: {n*0.9:.2f}s; }}
  @keyframes sw {{ 0%,70% {{ transform: translateX(-260px); }} 100% {{ transform: translateX({W+260}px); }} }}
</style>
<defs>
  <linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#131a2a"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
  <radialGradient id="r" cx="1" cy="0" r="1"><stop offset="0" stop-color="{col}" stop-opacity=".5"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>
  <linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".45" stop-color="#fff" stop-opacity=".04"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="swg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="ed" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{dark(col, .35)}"/><stop offset=".5" stop-color="{dark(col, .55)}"/><stop offset="1" stop-color="{dark(col, .3)}"/></linearGradient>
  <clipPath id="c"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16"/></clipPath>
  <filter id="bl" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<ellipse class="sh" filter="url(#bl)" cx="{W/2}" cy="{CH-9}" rx="{W/2-30}" ry="7" fill="{col}" opacity=".4"/>
<g class="fl"><g transform="translate(0 {PAD})">
  <rect x="0" y="{EDGE}" width="{W}" height="{H}" rx="16" fill="url(#ed)"/>
  <rect x="0" y="{EDGE/2}" width="{W}" height="{H}" rx="16" fill="{dark(col, .45)}"/>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="url(#b)"/>
    <rect class="g" width="{W}" height="{H}" fill="url(#r)"/>
    <rect width="{W}" height="4" fill="{col}"/>
    <rect class="sw" x="0" y="0" width="180" height="{H}" fill="url(#swg)" transform="skewX(-20)"/>
  </g>
  <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="#ffffff" stroke-opacity=".12"/>
  <g transform="translate(26 22)"><g class="if"><g class="fp">
    <rect x="0" y="6" width="48" height="48" rx="12" fill="{dark(col, .4)}"/>
    <rect x="0" y="3" width="48" height="48" rx="12" fill="{dark(col, .65)}"/>
    <rect width="48" height="48" rx="12" fill="#1c2233"/>
    <rect width="48" height="48" rx="12" fill="{col}" fill-opacity=".16"/>
    <text x="24" y="32" text-anchor="middle" font-size="23">{icon}</text>
    <rect width="48" height="48" rx="12" fill="url(#gl)"/>
    <rect x=".5" y=".5" width="47" height="47" rx="11.5" fill="none" stroke="{col}" stroke-opacity=".6"/>
  </g></g></g>
  <text x="88" y="46" font-family="{SANS}" font-size="19" font-weight="700" fill="#f4f7fb">{e(name)}</text>
  <text x="88" y="67" font-family="{MONO}" font-size="12" fill="{col}" letter-spacing=".5">{e(kind.upper())}</text>
  <g font-family="{SANS}" font-size="14" fill="#a9b3c9">{dl}</g>
  <g font-family="{SANS}" font-size="11.5" font-weight="600" fill="#e5e7eb">{tg}</g>
</g></g>
</svg>"""
    open(f"{R}/projects/{slug}.svg", "w").write(svg)

# ---------------- about code card ----------------
rows = [
 [("#c678dd","class "),("#e5c07b","Alaa "),("#c678dd","extends "),("#e5c07b","Developer"),("#e5e7eb"," {")],
 [("#e5e7eb","")],
 [("#c678dd","    public "),("#e06c75","$role"),("#e5e7eb"," = "),("#98c379","'Full-Stack Laravel & Flutter'"),("#e5e7eb",";")],
 [("#c678dd","    public "),("#e06c75","$company"),("#e5e7eb"," = "),("#98c379","'predev. Solutions'"),("#e5e7eb",";")],
 [("#c678dd","    public "),("#e06c75","$location"),("#e5e7eb"," = "),("#98c379","'Cairo, Egypt 🇪🇬'"),("#e5e7eb",";")],
 [("#c678dd","    public "),("#e06c75","$shipped"),("#e5e7eb"," = "),("#d19a66","16"),("#e5e7eb","; "),("#6b7280","// and counting")],
 [("#e5e7eb","")],
 [("#c678dd","    public "),("#c678dd","function "),("#61afef","stack"),("#e5e7eb","(): "),("#e5c07b","array"),("#e5e7eb","  {")],
 [("#c678dd","        return "),("#e5e7eb","["),("#98c379","'backend'"),("#e5e7eb"," => ["),("#98c379","'Laravel'"),("#e5e7eb",", "),("#98c379","'Livewire'"),("#e5e7eb","],")],
 [("#98c379","                "),("#98c379","'mobile'"),("#e5e7eb","  => ["),("#98c379","'Flutter'"),("#e5e7eb",", "),("#98c379","'Dart'"),("#e5e7eb","],")],
 [("#98c379","                "),("#98c379","'focus'"),("#e5e7eb","   => ["),("#98c379","'SaaS'"),("#e5e7eb",", "),("#98c379","'Payments'"),("#e5e7eb",", "),("#98c379","'RTL'"),("#e5e7eb","]];")],
 [("#e5e7eb","    }")],
 [("#e5e7eb","}")],
]
body = ""
for i, r in enumerate(rows):
    y = 72 + i * 22
    ts = "".join(f'<tspan fill="{c}">{e(t)}</tspan>' for c, t in r)
    body += f'<text x="52" y="{y}" xml:space="preserve" class="l" style="animation-delay:{.12*i:.2f}s"><tspan fill="#4b5563">{i+1:>2}  </tspan>{ts}</text>'
aw, ah = 560, 72 + len(rows) * 22 + 12
about = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{aw}" height="{ah}" viewBox="0 0 {aw} {ah}">
<style>.l{{animation:in .5s ease backwards}}@keyframes in{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}</style>
<rect x=".5" y=".5" width="{aw-1}" height="{ah-1}" rx="14" fill="#0d1117" stroke="#ffffff" stroke-opacity=".12"/>
<path d="M.5 14.5a14 14 0 0 1 14-14h{aw-29}a14 14 0 0 1 14 14V40H.5z" fill="#161b26"/>
<circle cx="22" cy="20" r="6" fill="#ff5f57"/><circle cx="42" cy="20" r="6" fill="#febc2e"/><circle cx="62" cy="20" r="6" fill="#28c840"/>
<text x="{aw/2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="#8b95ab">app/Models/Alaa.php</text>
<g font-family="{MONO}" font-size="13.5" transform="translate(-36,0)">{body}</g>
</svg>'''
open(R + "/about.svg", "w").write(about)

# ---------------- section divider ----------------
open(R + "/divider.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="6" viewBox="0 0 1200 6">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{V}" stop-opacity="0"/><stop offset=".5" stop-color="{V}"/><stop offset=".75" stop-color="{CY}"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></linearGradient></defs>
<rect width="1200" height="6" rx="3" fill="url(#g)"/></svg>''')
