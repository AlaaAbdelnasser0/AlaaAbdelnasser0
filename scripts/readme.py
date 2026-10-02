"""Point every asset URL in the READMEs at its current content (?v=<hash>),
so GitHub's image cache never keeps serving an old SVG after a refresh."""
import hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def version(m):
    f = ROOT / m.group(2)
    v = hashlib.sha1(f.read_bytes()).hexdigest()[:8] if f.is_file() else "0"
    return f"{m.group(1)}?v={v}"


if __name__ == "__main__":
    for name in ("README.md", "README.ar.md"):
        p = ROOT / name
        s = p.read_text()
        p.write_text(re.sub(r'(/main/(assets/[^?"\s]+))\?v=\w+', version, s))
