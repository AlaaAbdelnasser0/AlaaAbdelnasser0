"""Skills, detected from what my repos actually use.

Scans every repo I own (private included) for composer.json, package.json,
pubspec.yaml, languages and tell-tale files, then redraws:
  assets/tech-stack.svg  bento grid of the main technologies
  assets/toolkit.svg     packages and practices, grouped by job
  the SKILLS block in README.md and README.ar.md

Needs STATS_TOKEN (or GH_TOKEN) that can read private repos. Only skill names
and how many repos use them are written out, never repo names or code.
New tech shows up on its own once it is listed in STACK or TOOLKIT below and a repo uses it.
"""
import base64, json, pathlib, re, urllib.error
from collections import namedtuple
from fnmatch import fnmatch

from sections import A, ROOT, SANS, MONO, V, CY, dark, e, frame
from stats import USER, TOKEN, api

ICONS = ROOT / "scripts" / "icons"
TILE = "#242938"

# icon: "sk:<file>" (skillicons tile), "si:<file>" (simple-icons path on a dark tile) or "cu:<name>".
# always=True keeps a skill even when no repo shows it (Postman, VS Code and the like leave no trace).
Skill = namedtuple("Skill", "name icon col dets always", defaults=((), False))
Chip = namedtuple("Chip", "name dets always", defaults=((), False))

STACK = [
    ("Backend", "⚙️", "#FF2D20", [
        Skill("PHP", "sk:php", "#777BB4", ("composer:php", "lang:PHP"), True),
        Skill("Laravel", "sk:laravel", "#FF2D20", ("composer:laravel/framework",), True),
        Skill("Livewire", "si:livewire", "#FB70A9", ("composer:livewire/*",), True),
        Skill("Filament", "si:filament", "#FDAE4B", ("composer:filament/*",), True),
        Skill("Node.js", "sk:nodejs", "#5FA04E", ("npm:express", "npm:nest*"), True),
        Skill("Python", "sk:python", "#3776AB", ("lang:Python",)),
        Skill("GraphQL", "sk:graphql", "#E10098", ("composer:nuwave/lighthouse", "npm:graphql", "pub:graphql*")),
        Skill("WordPress", "sk:wordpress", "#21759B", (r"path:(^|/)wp-config(-sample)?\.php$",)),
    ]),
    ("Frontend", "🎨", "#38BDF8", [
        Skill("HTML", "sk:html", "#E34F26", ("lang:HTML", "lang:Blade"), True),
        Skill("CSS", "sk:css", "#1572B6", ("lang:CSS",), True),
        Skill("JavaScript", "sk:js", "#F0DB4F", ("lang:JavaScript",), True),
        Skill("TypeScript", "sk:ts", "#3178C6", ("lang:TypeScript", "npm:typescript")),
        Skill("Tailwind", "sk:tailwind", "#38BDF8", ("npm:tailwindcss",), True),
        Skill("Bootstrap", "sk:bootstrap", "#7952B3", ("npm:bootstrap",), True),
        Skill("Alpine.js", "sk:alpinejs", "#8BC0D0", ("npm:alpinejs", "composer:livewire/livewire"), True),
        Skill("jQuery", "sk:jquery", "#0769AD", ("npm:jquery",)),
        Skill("React", "sk:react", "#61DAFB", ("npm:react",)),
        Skill("Next.js", "sk:nextjs", "#E6EDF3", ("npm:next",)),
        Skill("Vue", "sk:vue", "#42B883", ("npm:vue",)),
        Skill("Nuxt", "sk:nuxtjs", "#00DC82", ("npm:nuxt",)),
        Skill("Svelte", "sk:svelte", "#FF3E00", ("npm:svelte",)),
        Skill("Inertia", "sk:inertia", "#9553E9", ("composer:inertiajs/*", "npm:@inertiajs/*")),
        Skill("Sass", "sk:sass", "#CC6699", ("npm:sass",)),
    ]),
    ("Mobile", "📱", "#22D3EE", [
        Skill("Flutter", "sk:flutter", "#44D1FD", ("pub:flutter",), True),
        Skill("Dart", "sk:dart", "#0175C2", ("lang:Dart",), True),
        Skill("Riverpod", "cu:riverpod", "#00B4AB", ("pub:*riverpod",), True),
        Skill("iOS", "sk:apple", "#E6EDF3", (r"path:(^|/)ios/Runner/",)),
        Skill("Android", "sk:androidstudio", "#3DDC84", (r"path:(^|/)android/app/",), True),
        Skill("Kotlin", "sk:kotlin", "#A97BFF", ("lang:Kotlin",)),
        Skill("Swift", "sk:swift", "#F05138", ("lang:Swift",)),
        Skill("Firebase", "sk:firebase", "#FFCA28", ("pub:firebase_*", "npm:firebase", "composer:kreait/*")),
    ]),
    ("Data & Cloud", "🗄️", "#10B981", [
        Skill("MySQL", "sk:mysql", "#4479A1", (), True),
        Skill("PostgreSQL", "sk:postgres", "#4169E1", ("npm:pg",)),
        Skill("MongoDB", "sk:mongodb", "#47A248", ("composer:mongodb/*", "npm:mongoose", "npm:mongodb")),
        Skill("Redis", "sk:redis", "#FF4438", ("composer:predis/predis", "composer:laravel/horizon", "npm:ioredis"), True),
        Skill("Meilisearch", "si:meilisearch", "#FF5CAA", ("composer:meilisearch/*", "npm:meilisearch")),
        Skill("Supabase", "sk:supabase", "#3ECF8E", ("npm:@supabase/*", "pub:supabase*")),
        Skill("AWS S3", "sk:aws", "#FF9900", ("composer:league/flysystem-aws-s3*", "composer:aws/*")),
        Skill("Pusher", "si:pusher", "#8A7CFF", ("composer:pusher/*", "npm:pusher-js")),
        Skill("Twilio", "si:twilio", "#F22F46", ("composer:twilio/*",)),
    ]),
    ("Payments", "💳", "#8B5CF6", [
        Skill("Stripe", "si:stripe", "#635BFF", ("composer:stripe/*", "composer:laravel/cashier*", "pub:flutter_stripe", "npm:@stripe/*"), True),
        Skill("PayPal", "si:paypal", "#2997E6", ("composer:srmklive/paypal", "composer:paypal/*"), True),
        Skill("Paymob", "cu:paymob", "#4D8BFF", ("composer:*paymob*",), True),
        Skill("Fawry", "si:fawry", "#FFD200", ("composer:*fawry*",), True),
    ]),
    ("DevOps & Build", "🚀", "#F59E0B", [
        Skill("Docker", "sk:docker", "#2396ED", (r"path:(^|/)(Dockerfile|docker-compose\.ya?ml)$",)),
        Skill("GitHub Actions", "sk:githubactions", "#2088FF", (r"path:^\.github/workflows/.+\.ya?ml$",)),
        Skill("Codemagic", "si:codemagic", "#F45E3F", (r"path:(^|/)codemagic\.ya?ml$",)),
        Skill("Nginx", "sk:nginx", "#009639", (r"path:(^|/)nginx[^/]*\.conf$", r"path:(^|/)nginx/")),
        Skill("Vite", "sk:vite", "#BD34FE", ("npm:vite",), True),
        Skill("Linux", "sk:linux", "#FCC624", (), True),
    ]),
    ("Tools", "🧰", "#EC4899", [
        Skill("Git", "sk:git", "#F05032", (), True),
        Skill("GitHub", "sk:github", "#E6EDF3", (), True),
        Skill("Postman", "sk:postman", "#FF6C37", (), True),
        Skill("VS Code", "sk:vscode", "#23A9F2", (), True),
        Skill("Figma", "sk:figma", "#A259FF", ()),
    ]),
]

TOOLKIT = [
    ("Auth & Security", "🔐", "#F43F5E", [
        Chip("Sanctum API tokens", ("composer:laravel/sanctum",)),
        Chip("Passport OAuth2", ("composer:laravel/passport",)),
        Chip("Socialite logins", ("composer:laravel/socialite",)),
        Chip("Sign in with Apple", ("composer:socialiteproviders/apple", "pub:sign_in_with_apple")),
        Chip("Google Sign-In", ("pub:google_sign_in",)),
        Chip("Roles & permissions", ("composer:spatie/laravel-permission",)),
        Chip("Two-factor auth", ("composer:pragmarx/google2fa*", "composer:laravel/fortify")),
        Chip("Audit logs", ("composer:spatie/laravel-activitylog",)),
        Chip("Breeze starter", ("composer:laravel/breeze",)),
    ]),
    ("Payments & Billing", "💳", "#8B5CF6", [
        Chip("Stripe", ("composer:stripe/*", "pub:flutter_stripe"), True),
        Chip("Cashier subscriptions", ("composer:laravel/cashier*",)),
        Chip("PayPal", ("composer:srmklive/paypal", "composer:paypal/*"), True),
        Chip("Paymob", ("composer:*paymob*",), True),
        Chip("Fawry", ("composer:*fawry*",), True),
        Chip("Escrow checkout", (), True),
        Chip("Wallets & payouts", (), True),
    ]),
    ("Real-time & Alerts", "⚡", "#22D3EE", [
        Chip("Laravel Reverb", ("composer:laravel/reverb",)),
        Chip("Pusher", ("composer:pusher/*", "npm:pusher-js")),
        Chip("Laravel Echo", ("npm:laravel-echo",)),
        Chip("Web push", ("composer:laravel-notification-channels/webpush",)),
        Chip("Twilio SMS", ("composer:twilio/*",)),
        Chip("Queues & jobs", (), True),
        Chip("Horizon", ("composer:laravel/horizon",)),
    ]),
    ("Search, Data & Storage", "🔎", "#10B981", [
        Chip("Laravel Scout", ("composer:laravel/scout",)),
        Chip("Meilisearch", ("composer:meilisearch/*",)),
        Chip("Redis cache", ("composer:predis/predis", "composer:laravel/horizon")),
        Chip("Multi-tenancy", ("composer:stancl/tenancy", "composer:spatie/laravel-multitenancy")),
        Chip("Media library", ("composer:spatie/laravel-medialibrary",)),
        Chip("S3 storage", ("composer:league/flysystem-aws-s3*",)),
        Chip("Backups", ("composer:spatie/laravel-backup",)),
        Chip("Eloquent ORM", ("composer:laravel/framework",), True),
    ]),
    ("Files, Reports & Docs", "📄", "#F59E0B", [
        Chip("PDF (DomPDF)", ("composer:barryvdh/laravel-dompdf",)),
        Chip("Arabic PDF (mPDF)", ("composer:mpdf/mpdf",)),
        Chip("Excel import/export", ("composer:maatwebsite/excel",)),
        Chip("QR codes", ("composer:bacon/bacon-qr-code", "composer:simplesoftwareio/simple-qrcode")),
        Chip("Image processing", ("composer:intervention/image*",)),
        Chip("API docs (Scribe)", ("composer:knuckleswtf/scribe",)),
        Chip("ApexCharts", ("npm:apexcharts",)),
        Chip("Drag & drop", ("npm:sortablejs",)),
    ]),
    ("Testing & Quality", "🧪", "#84CC16", [
        Chip("Pest", ("composer:pestphp/pest",)),
        Chip("PHPUnit", ("composer:phpunit/phpunit",)),
        Chip("Larastan", ("composer:larastan/larastan", "composer:nunomaduro/larastan")),
        Chip("Laravel Pint", ("composer:laravel/pint",)),
        Chip("Telescope", ("composer:laravel/telescope",)),
        Chip("Mockery", ("composer:mockery/mockery",)),
        Chip("Flutter lints", ("pub:flutter_lints",)),
    ]),
    ("Flutter Toolkit", "📱", "#44D1FD", [
        Chip("Riverpod", ("pub:*riverpod",)),
        Chip("GoRouter", ("pub:go_router",)),
        Chip("Dio", ("pub:dio",)),
        Chip("Secure storage", ("pub:flutter_secure_storage",)),
        Chip("Stripe SDK", ("pub:flutter_stripe",)),
        Chip("ML Kit face detection", ("pub:google_mlkit_*",)),
        Chip("Camera", ("pub:camera",)),
        Chip("Audio playback", ("pub:just_audio",)),
        Chip("fl_chart", ("pub:fl_chart",)),
    ]),
    ("DevOps & Delivery", "🚀", "#FB923C", [
        Chip("Docker Compose", (r"path:(^|/)docker-compose\.ya?ml$",)),
        Chip("GitHub Actions CI", (r"path:^\.github/workflows/.+\.ya?ml$",)),
        Chip("Codemagic", (r"path:(^|/)codemagic\.ya?ml$",)),
        Chip("TestFlight releases", (r"path:(^|/)codemagic\.ya?ml$",)),
        Chip("Laravel Sail", ("composer:laravel/sail",)),
        Chip("Vite builds", ("npm:vite",)),
        Chip("Git flow", (), True),
    ]),
    ("Product & UX", "🌐", "#EC4899", [
        Chip("Arabic-first RTL", (), True),
        Chip("AR / EN localization", (), True),
        Chip("Dark mode", (), True),
        Chip("PWAs", (), True),
        Chip("Responsive UI", (), True),
        Chip("REST API design", (), True),
        Chip("Admin dashboards", (), True),
    ]),
]

AR_NAMES = {"Backend": "الخلفية", "Frontend": "الواجهات", "Mobile": "الموبايل", "Data & Cloud": "البيانات والسحابة",
            "Payments": "المدفوعات", "DevOps & Build": "النشر والبناء", "Tools": "الأدوات",
            "Auth & Security": "المصادقة والأمان", "Payments & Billing": "الدفع والفواتير",
            "Real-time & Alerts": "الوقت الحقيقي والإشعارات", "Search, Data & Storage": "البحث والبيانات والتخزين",
            "Files, Reports & Docs": "الملفات والتقارير والتوثيق", "Testing & Quality": "الاختبار والجودة",
            "Flutter Toolkit": "أدوات Flutter", "DevOps & Delivery": "النشر والتسليم", "Product & UX": "المنتج وتجربة المستخدم"}

SKIP = re.compile(r"(^|/)(vendor|node_modules|build|\.dart_tool|Pods|storage|public/build)/")
MANIFESTS = ("composer.json", "package.json", "pubspec.yaml")


# ---------------- scanning ----------------
def raw(repo, path):
    data = api(f"repos/{USER}/{repo}/contents/{path}")
    return base64.b64decode(data["content"]).decode("utf-8", "replace")


def pub_deps(text):
    deps, section = set(), None
    for line in text.splitlines():
        if re.match(r"^\S", line):
            section = line.split(":")[0].strip()
        elif section in ("dependencies", "dev_dependencies"):
            m = re.match(r"^  ([a-z0-9_]+):", line)
            if m:
                deps.add(m.group(1))
    return deps


def repo_tokens(r):
    toks, paths = set(), []
    try:
        tree = api(f"repos/{USER}/{r['name']}/git/trees/{r['default_branch']}?recursive=1")["tree"]
    except urllib.error.HTTPError:  # empty repo
        return toks, paths
    paths = [t["path"] for t in tree if t["type"] == "blob" and not SKIP.search(t["path"])]
    for p in paths:
        name = p.rsplit("/", 1)[-1]
        if name not in MANIFESTS or p.count("/") > 2:
            continue
        try:
            text = raw(r["name"], p)
        except urllib.error.HTTPError:
            continue
        if name == "pubspec.yaml":
            toks |= {f"pub:{d}" for d in pub_deps(text)}
            continue
        try:
            js = json.loads(text)
        except ValueError:
            continue
        kind, keys = ("composer", ("require", "require-dev")) if name == "composer.json" else ("npm", ("dependencies", "devDependencies"))
        for k in keys:
            toks |= {f"{kind}:{d}" for d in (js.get(k) or {})}
    langs = api(f"repos/{USER}/{r['name']}/languages")
    total = sum(langs.values()) or 1
    # a tiny share is usually generated code (Flutter's Kotlin/Swift runners), not something I wrote
    toks |= {f"lang:{k}" for k, v in langs.items() if v >= 5000 and v / total >= .02}
    return toks, paths


def matches(dets, toks, paths):
    for d in dets:
        if d.startswith("path:"):
            if any(re.search(d[5:], p) for p in paths):
                return True
        elif any(fnmatch(t, d) for t in toks):
            return True
    return False


def scan():
    repos = [r for r in api("user/repos?affiliation=owner&per_page=100") if r["name"] != USER and not r["fork"]]
    scanned = [repo_tokens(r) for r in repos]
    count = {}
    for *_, items in STACK + TOOLKIT:
        for it in items:
            count[(it.name, it.dets)] = sum(matches(it.dets, t, p) for t, p in scanned)
    return len(repos), count


def shown(items, count):
    return [(it, count[(it.name, it.dets)]) for it in items if it.always or count[(it.name, it.dets)]]


# ---------------- icons ----------------
def icon(spec, col, pfx, s):
    kind, key = spec.split(":")
    if kind == "sk":
        src = (ICONS / f"sk_{key}.svg").read_text()
        inner = re.search(r'<g transform="translate\(0, 0\)">\s*(<svg.*</svg>)\s*</g>', src, re.S).group(1).strip()
        for i in set(re.findall(r'id="([^"]+)"', inner)):
            inner = inner.replace(f'id="{i}"', f'id="{pfx}{i}"').replace(f"url(#{i})", f"url(#{pfx}{i})").replace(f'href="#{i}"', f'href="#{pfx}{i}"')
        head, rest = inner.split(">", 1)
        head = re.sub(r'\s(width|height)="[^"]*"', "", head)
        return head.replace("<svg", f'<svg width="{s}" height="{s}"', 1) + ">" + rest
    if kind == "si":
        d = re.search(r'<path d="([^"]+)"', (ICONS / f"si_{key}.svg").read_text()).group(1)
        fit = "translate(22 22) scale(8.833)" if key == "filament" else "translate(60 60) scale(5.667)"
        body = f'<path transform="{fit}" fill="{col}" d="{d}"/>'
    elif key == "riverpod":
        body = ('<path d="M58 150 q35 -40 70 0 t70 0" fill="none" stroke="#00B4AB" stroke-width="18" stroke-linecap="round"/>'
                '<path d="M58 190 q35 -40 70 0 t70 0" fill="none" stroke="#0E7C86" stroke-width="18" stroke-linecap="round"/>'
                '<circle cx="128" cy="86" r="26" fill="#5EEAD4"/>')
    else:  # paymob
        body = f'<text x="128" y="150" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="58" fill="#4D8BFF">paymob</text>'
    return f'<svg width="{s}" height="{s}" viewBox="0 0 256 256"><rect width="256" height="256" rx="60" fill="{TILE}"/>{body}</svg>'


# ---------------- shared card chrome ----------------
STYLE = """
  .pz { animation: pz 7s ease-in-out infinite; opacity: 0; }
  @keyframes pz { 0%,70%,100% { opacity: 0; } 80% { opacity: .9; } }
  .sw { animation: sw 7s ease-in-out infinite; }
  @keyframes sw { 0% { transform: translateX(-160px); } 60%,100% { transform: translateX(1000px); } }
"""


def card(x, y, w, h, col, emo, title, sub, body, k):
    return f"""<g transform="translate({x} {y})">
  <rect y="5" width="{w}" height="{h}" rx="18" fill="{dark(col, .3)}" fill-opacity=".7"/>
  <rect width="{w}" height="{h}" rx="18" fill="url(#face)"/>
  <rect width="{w}" height="{h}" rx="18" fill="{col}" fill-opacity=".05"/>
  <rect width="{w}" height="58" rx="18" fill="url(#hd{k})"/>
  <g clip-path="url(#cc{k})"><rect class="sw" style="animation-delay:{k * .6:.1f}s" width="160" height="2" fill="url(#swg)"/></g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="17.5" fill="none" stroke="{col}" stroke-opacity=".35"/>
  <g transform="translate(18 15)">
    <rect width="30" height="30" rx="9" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-opacity=".55"/>
    <text x="15" y="21" text-anchor="middle" font-size="15">{emo}</text>
  </g>
  {label(60, 36, title, 16, "#f4f7fb", weight=700)}
  <text x="{w - 18}" y="35" text-anchor="end" font-family="{MONO}" font-size="11" fill="{col}" fill-opacity=".9">{sub}</text>
  <line x1="18" x2="{w - 18}" y1="58" y2="58" stroke="#fff" stroke-opacity=".07"/>
  {body}
</g>"""


def card_defs(k, w, col):
    return (f'<linearGradient id="hd{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="cc{k}"><rect x="18" width="{w - 36}" height="2"/></clipPath>')


def wrap(body, W, H, defs, foot):
    svg = frame(W, H, body + f'<text x="{W - 22}" y="{H - 14}" text-anchor="end" font-family="{MONO}" font-size="11" fill="#5b6478">{foot}</text>')
    return svg.replace("</style>", STYLE + "</style>").replace("</defs>", (
        f'<linearGradient id="swg" x1="0" x2="1"><stop offset="0" stop-color="{CY}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></linearGradient>'
        + "".join(defs) + "</defs>"), 1)


# ---------------- layout helpers ----------------
# Helvetica/Arial advance widths per 1000 em. Viewers get different fonts per OS, so every
# label also carries textLength: the estimate below decides the box, the browser fits the text to it.
_W = {**dict.fromkeys("ijl'|", 222), **dict.fromkeys(" ft./,:;I!", 278), **dict.fromkeys("r()-", 333),
      **dict.fromkeys("cksvxyzJ", 500), **dict.fromkeys("FTZL", 611), "m": 833, "w": 722, "M": 833, "W": 944,
      **dict.fromkeys("CDHNRU", 722), **dict.fromkeys("GOQ", 778), "&": 667, "+": 584}


def tw(text, size, weight=1.06):
    return sum(_W.get(ch, 667 if ch.isupper() else 556) for ch in text) * size / 1000 * weight


def label(x, y, text, size, fill, anchor="start", weight=600, max_w=None):
    w = tw(text, size)
    fit = f' textLength="{min(w, max_w) if max_w else w:.1f}" lengthAdjust="spacingAndGlyphs"'
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{SANS}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{fit}>{e(text)}</text>')


def bento(groups, W=920, X0=20, GAP=16):
    """Two cards per row, the last one full width when the count is odd. Yields (group, x, width, pair)."""
    half = (W - 2 * X0 - GAP) // 2
    for i in range(0, len(groups), 2):
        pair = groups[i:i + 2]
        w = half if len(pair) == 2 else W - 2 * X0
        yield [(g, X0 + j * (half + GAP), w) for j, g in enumerate(pair)]


# ---------------- tech stack ----------------
TS, STEP, ROW = 48, 72, 88


def tiles(items, per_row, x0, k0):
    out = []
    for i, (sk, n) in enumerate(items):
        r, c = divmod(i, per_row)
        x, y, k = x0 + c * STEP, 76 + r * ROW, k0 + i
        badge = (f'<g transform="translate({TS - 4} -4)"><circle r="9.5" fill="#0b0f1a" stroke="{sk.col}" stroke-opacity=".9"/>'
                 f'<text y="3.6" text-anchor="middle" font-family="{SANS}" font-size="10" font-weight="700" fill="#f4f7fb">{n}</text></g>') if n else ""
        out.append(f"""<g transform="translate({x} {y})">
    <rect class="pz" style="animation-delay:{k * .18:.2f}s" x="-5" y="-5" width="{TS + 10}" height="{TS + 10}" rx="17" fill="none" stroke="{sk.col}" stroke-width="2"/>
    <rect y="4" width="{TS}" height="{TS}" rx="13" fill="{dark(sk.col, .4)}"/>
    {icon(sk.icon, sk.col, f"i{k}_", TS)}
    <rect width="{TS}" height="{TS}" rx="13" fill="url(#gloss)"/>
    <rect x=".5" y=".5" width="{TS - 1}" height="{TS - 1}" rx="12.5" fill="none" stroke="{sk.col}" stroke-opacity=".5"/>
    {badge}
    {label(TS / 2, TS + 22, sk.name, 11, "#b6bfd3", "middle", max_w=STEP - 6)}
  </g>""")
    return "".join(out)


def tech_stack(count, n_repos):
    groups = [(cat, emo, col, shown(items, count)) for cat, emo, col, items in STACK]
    out, defs, y, k, tile_k = [], [], 22, 0, 0
    for row in bento(groups):
        w = row[0][2]
        per = (w - 24 - TS) // STEP + 1
        h = 70 + max(-(-len(g[3]) // per) for g, *_ in row) * ROW
        for (cat, emo, col, items), x, w in row:
            n = min(len(items), per)
            x0 = (w - ((n - 1) * STEP + TS)) / 2
            out.append(card(x, y, w, h, col, emo, cat, f"{len(items)} skills", tiles(items, per, x0, tile_k), k))
            defs.append(card_defs(k, w, col))
            k, tile_k = k + 1, tile_k + len(items)
        y += h + 20
    foot = f"auto-detected from {n_repos} repos · badge = projects using it"
    (A / "tech-stack.svg").write_text(wrap("".join(out), 920, y + 18, defs, foot))
    return groups


# ---------------- toolkit (chips) ----------------
CH, CF = 28, 12.5  # chip height, font size


def chips(items, inner, col):
    x, y, out = 0, 0, []
    for it, n in items:
        w = tw(it.name, CF) + 28 + (tw(str(n), 11) + 16 if n else 0)
        if x and x + w > inner:
            x, y = 0, y + CH + 9
        num = (f'<rect x="{w - tw(str(n), 11) - 22:.1f}" y="6" width="{tw(str(n), 11) + 12:.1f}" height="16" rx="8" fill="{col}" fill-opacity=".22"/>'
               + label(f"{w - 16:.1f}", 18.5, str(n), 11, col, "end", 700)) if n else ""
        out.append(f'<g transform="translate({x:.1f} {y})">'
                   f'<rect width="{w:.1f}" height="{CH}" rx="{CH / 2}" fill="{col}" fill-opacity=".09" stroke="{col}" stroke-opacity=".4"/>'
                   + label(14, 18.5, it.name, CF, "#dbe2f0") + num + "</g>")
        x += w + 8
    return "".join(out), y + CH


def toolkit(count, n_repos):
    groups = [(cat, emo, col, sorted(shown(items, count), key=lambda c: -c[1])) for cat, emo, col, items in TOOLKIT]
    out, defs, y, k = [], [], 22, 0
    for row in bento(groups):
        laid = [(g, x, w, *chips(g[3], w - 40, g[2])) for g, x, w in row]
        h = 92 + max(ch for *_, ch in laid)
        for (cat, emo, col, items), x, w, body, _ in laid:
            out.append(card(x, y, w, h, col, emo, cat, f"{len(items)} items", f'<g transform="translate(20 76)">{body}</g>', k))
            defs.append(card_defs(k, w, col))
            k += 1
        y += h + 20
    foot = f"packages found across {n_repos} repos · number = projects using it"
    (A / "toolkit.svg").write_text(wrap("".join(out), 920, y + 18, defs, foot))
    return groups


# ---------------- README block ----------------
RAW = f"https://raw.githubusercontent.com/{USER}/{USER}/main/assets"


def block(stack, kit, n_repos, ar):
    names = lambda groups: ", ".join(it.name for *_, items in groups for it, _ in items)
    text = "\n\n".join(f"**{emo} {AR_NAMES[cat] if ar else cat}:** " + " · ".join(it.name for it, _ in items)
                       for cat, emo, _, items in stack + kit)
    summary = "كل المهارات كنص" if ar else "All skills as plain text"
    note = (f"🤖 تُستخرج تلقائيًا من حزم مستودعاتي الـ {n_repos} وتُحدَّث يوميًا عبر GitHub Actions."
            if ar else f"🤖 Detected automatically from the packages in my {n_repos} repositories, refreshed daily by GitHub Actions.")
    return f"""<!-- SKILLS:START (generated by scripts/skills.py, edits here are overwritten) -->
<p align="center">
  <img src="{RAW}/tech-stack.svg?v=0" width="100%" alt="Tech stack: {e(names(stack))}" />
</p>

<p align="center">
  <img src="{RAW}/toolkit.svg?v=0" width="100%" alt="Toolkit: {e(names(kit))}" />
</p>

<details>
<summary><b>{summary}</b></summary>

{text}

</details>

<p align="center"><sub>{note}</sub></p>
<!-- SKILLS:END -->"""


def write_readmes(stack, kit, n_repos):
    for name, ar in (("README.md", False), ("README.ar.md", True)):
        p = ROOT / name
        s = p.read_text()
        new = re.sub(r"<!-- SKILLS:START.*?<!-- SKILLS:END -->", lambda _: block(stack, kit, n_repos, ar), s, flags=re.S)
        if new == s and "SKILLS:START" not in s:
            raise SystemExit(f"{name}: no SKILLS:START / SKILLS:END markers")
        p.write_text(new)


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Set STATS_TOKEN (a token that can read your private repos).")
    n, count = scan()
    write_readmes(tech_stack(count, n), toolkit(count, n), n)
