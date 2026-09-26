import re, colorsys
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
I = str(ROOT / "scripts" / "icons")
OUT = str(ROOT / "assets" / "tech-stack.svg")
SANS = "'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, monospace"
TILE = "#242938"

def sk(name, pfx):
    s = open(f"{I}/sk_{name}.svg").read()
    inner = re.search(r"<g transform=\"translate\(0, 0\)\">\s*(<svg.*</svg>)\s*</g>", s, re.S).group(1)
    ids = set(re.findall(r'id="([^"]+)"', inner))
    for i in ids:
        inner = inner.replace(f'id="{i}"', f'id="{pfx}{i}"').replace(f"url(#{i})", f"url(#{pfx}{i})").replace(f'href="#{i}"', f'href="#{pfx}{i}"')
    inner = inner.strip()
    head, rest = inner.split(">", 1)
    head = re.sub(r'\s(width|height)="[^"]*"', "", head)
    return head.replace("<svg", '<svg x="0" y="0" width="72" height="72"', 1) + ">" + rest

def si(name, color):
    d = re.search(r'<path d="([^"]+)"', open(f"{I}/si_{name}.svg").read()).group(1)
    return (f'<svg x="0" y="0" width="72" height="72" viewBox="0 0 256 256"><rect width="256" height="256" rx="60" fill="{TILE}"/>' +
            (f'<path transform="translate(22 22) scale(8.833)" fill="{color}" d="{d}"/></svg>' if name == "filament" else f'<path transform="translate(60 60) scale(5.667)" fill="{color}" d="{d}"/></svg>'))

def custom(kind):
    if kind == "riverpod":
        body = ('<path d="M58 150 q35 -40 70 0 t70 0" fill="none" stroke="#00B4AB" stroke-width="18" stroke-linecap="round"/>'
                '<path d="M58 190 q35 -40 70 0 t70 0" fill="none" stroke="#0E7C86" stroke-width="18" stroke-linecap="round"/>'
                '<circle cx="128" cy="86" r="26" fill="#5EEAD4"/>')
    else:
        body = f'<text x="128" y="150" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="58" fill="#4D8BFF">paymob</text>'
    return f'<svg x="0" y="0" width="72" height="72" viewBox="0 0 256 256"><rect width="256" height="256" rx="60" fill="{TILE}"/>{body}</svg>'

ROWS = [
 ("Backend", "⚙️", [("PHP","sk","php","#777BB4"),("Laravel","sk","laravel","#FF2D20"),("Livewire","si","livewire","#FB70A9"),
                    ("Filament","si","filament","#FDAE4B"),("Node.js","sk","nodejs","#5FA04E")]),
 ("Mobile", "📱", [("Flutter","sk","flutter","#44D1FD"),("Dart","sk","dart","#0175C2"),("Riverpod","cu","riverpod","#00B4AB"),
                   ("Android Studio","sk","androidstudio","#3DDC84")]),
 ("Frontend", "🎨", [("HTML","sk","html","#E34F26"),("CSS","sk","css","#1572B6"),("JavaScript","sk","js","#F0DB4F"),
                     ("Tailwind","sk","tailwind","#38BDF8"),("Bootstrap","sk","bootstrap","#7952B3"),("Alpine.js","sk","alpinejs","#8BC0D0"),("Vite","sk","vite","#BD34FE")]),
 ("Data", "🗄️", [("MySQL","sk","mysql","#4479A1"),("Redis","sk","redis","#FF4438"),("Meilisearch","si","meilisearch","#FF5CAA")]),
 ("Payments", "💳", [("Stripe","si","stripe","#635BFF"),("PayPal","si","paypal","#2997E6"),("Paymob","cu","paymob","#4D8BFF"),("Fawry","si","fawry","#FFD200")]),
 ("Tools", "🧰", [("Git","sk","git","#F05032"),("GitHub","sk","github","#E6EDF3"),("Postman","sk","postman","#FF6C37"),
                  ("VS Code","sk","vscode","#23A9F2"),("Linux","sk","linux","#FCC624")]),
]

def dark(hexc, f):
    r, g, b = (int(hexc[i:i+2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(h, max(0, l * f), s)
    return "#%02x%02x%02x" % (int(r*255), int(g*255), int(b*255))

W, LBL, X0, STEP, ROWH, TOP = 920, 170, 200, 100, 128, 30
H = TOP + ROWH * len(ROWS) + 10
out = []
for r, (cat, emo, items) in enumerate(ROWS):
    y = TOP + r * ROWH
    if r:
        out.append(f'<line x1="24" x2="{W-24}" y1="{y-10}" y2="{y-10}" stroke="#fff" stroke-opacity=".06"/>')
    out.append(f'<g transform="translate(24 {y+20})"><rect width="{LBL-20}" height="40" rx="20" fill="#7C5CFF" fill-opacity=".12" stroke="#7C5CFF" stroke-opacity=".45"/>'
               f'<text x="{(LBL-20)/2}" y="26" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="#e6e1ff">{emo} {cat}</text></g>')
    for c, (name, src, key, col) in enumerate(items):
        x = X0 + c * STEP
        pfx = f"t{r}{c}_"
        icon = sk(key, pfx) if src == "sk" else si(key, col) if src == "si" else custom(key)
        d = (r * 0.35 + c * 0.22)
        out.append(f'''<g transform="translate({x} {y})">
  <ellipse class="sh" style="animation-delay:-{d:.2f}s" cx="36" cy="92" rx="30" ry="5" fill="{col}" opacity=".35"/>
  <g class="fl" style="animation-delay:-{d:.2f}s"><g class="fp" style="animation-delay:{d*1.6:.2f}s">
    <rect x="0" y="7" width="72" height="72" rx="17" fill="{dark(col, .45)}"/>
    <rect x="0" y="3.5" width="72" height="72" rx="17" fill="{dark(col, .7)}"/>
    {icon}
    <rect width="72" height="72" rx="17" fill="url(#gloss)"/>
    <rect x=".5" y=".5" width="71" height="71" rx="16.5" fill="none" stroke="{col}" stroke-opacity=".55"/>
  </g></g>
  <text x="36" y="112" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="600" fill="#9aa4bb">{name}</text>
</g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .fl {{ animation: fl 3.2s ease-in-out infinite; }}
  @keyframes fl {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
  .sh {{ animation: sh 3.2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes sh {{ 0%,100% {{ transform: scale(1); opacity: .4; }} 50% {{ transform: scale(.7); opacity: .18; }} }}
  .fp {{ animation: fp 9s cubic-bezier(.45,0,.2,1) infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes fp {{ 0%,78% {{ transform: scaleX(1) skewY(0); }} 83% {{ transform: scaleX(.02) skewY(-12deg); }} 88% {{ transform: scaleX(-1) skewY(0); }}
                   93% {{ transform: scaleX(.02) skewY(12deg); }} 98%,100% {{ transform: scaleX(1) skewY(0); }} }}
  .glow {{ animation: glow 6s ease-in-out infinite; }}
  @keyframes glow {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: .6; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f1a"/><stop offset=".6" stop-color="#120d2b"/><stop offset="1" stop-color="#0b1a2b"/></linearGradient>
  <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".45" stop-color="#fff" stop-opacity=".04"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <radialGradient id="o1"><stop offset="0" stop-color="#7C5CFF" stop-opacity=".55"/><stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></radialGradient>
  <radialGradient id="o2"><stop offset="0" stop-color="#22D3EE" stop-opacity=".35"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#fff" fill-opacity=".06"/></pattern>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <circle class="glow" cx="{W-60}" cy="60" r="260" fill="url(#o1)"/>
  <circle class="glow" style="animation-delay:-3s" cx="80" cy="{H-40}" r="240" fill="url(#o2)"/>
  {"".join(out)}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="19.5" fill="none" stroke="#fff" stroke-opacity=".1"/>
</svg>'''
open(OUT, "w").write(svg)
print(len(svg))
