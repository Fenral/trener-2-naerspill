"""Build a single-file shareable HTML where CSS and the logo are inlined and
videos stream from the live Vercel URL so the file works when emailed."""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "index.html"
CSS = ROOT / "theme.css"
LOGO = ROOT / "ngf-logo.png"
OUT = ROOT / "trener-2-naerspill-fil.html"
BASE_URL = "https://trener-2-naerspill.vercel.app"

html = SRC.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
logo_b64 = base64.b64encode(LOGO.read_bytes()).decode("ascii")

html = html.replace(
    '<link rel="stylesheet" href="theme.css">',
    f"<style>\n{css}\n</style>",
)
html = re.sub(r'\s*<script src="gate\.js"></script>\s*\n', "\n", html)
html = html.replace(
    '<img src="ngf-logo.png"',
    f'<img src="data:image/png;base64,{logo_b64}"',
)
html = re.sub(r'(?<=["\'])videos/(media\d+\.mp4)', rf"{BASE_URL}/videos/\1", html)

OUT.write_text(html, encoding="utf-8")
size_kb = OUT.stat().st_size / 1024
print(f"Wrote {OUT.name} ({size_kb:.1f} KB)")
