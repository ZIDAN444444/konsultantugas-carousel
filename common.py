#!/usr/bin/env python3
# Modul bersama carousel @konsultantugas: font, CSS dasar, helper visual, renderer.
# Dipakai oleh <tanggal-topik>/build.py, dijalankan otomatis oleh GitHub Actions.
import os, sys, subprocess, tempfile
from playwright.sync_api import sync_playwright

# (nama keluarga, paket @fontsource, bobot)
BASE_FACES = [
    ("GFS Didot", "gfs-didot", [400]),
    ("Inter", "inter", [400, 500, 700, 800]),
    ("Bebas Neue", "bebas-neue", [400]),
    ("Montserrat", "montserrat", [400, 500, 700, 800]),
    ("Poppins", "poppins", [600, 800]),
    ("DM Sans", "dm-sans", [400, 500, 700]),
    ("Archivo Black", "archivo-black", [400]),
    ("Space Grotesk", "space-grotesk", [400, 500, 700]),
]

BASE = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1440px}
body{position:relative;overflow:hidden;background-color:#fff;
 background-image:radial-gradient(#dcdfe8 2px,transparent 2.6px);background-size:80px 80px;
 color:#0A0A0A;font-family:var(--b),sans-serif}
body.v1{--d:'GFS Didot',serif;--b:'Inter';--dw:700;--dt:lowercase;--dl:-1px;--dlh:1.04}
body.v2{--d:'Bebas Neue',sans-serif;--b:'Montserrat';--dw:400;--dt:uppercase;--dl:1px;--dlh:0.94}
body.v3{--d:'Poppins',sans-serif;--b:'DM Sans';--dw:800;--dt:none;--dl:-1.5px;--dlh:1.1}
body.v4{--d:'Archivo Black',sans-serif;--b:'Space Grotesk';--dw:400;--dt:none;--dl:-3px;--dlh:1.0}
body.v5{--d:'Syne',sans-serif;--b:'Manrope';--dw:800;--dt:none;--dl:-2px;--dlh:1.02}
.safe{position:absolute;left:50px;top:180px;width:980px;height:1080px}
.abs{position:absolute}
.brand{position:absolute;left:0;right:0;top:0;text-align:center;font-family:'Inter',sans-serif;font-weight:800;font-size:30px;letter-spacing:.2px}
.d{font-family:var(--d),serif;font-weight:var(--dw);text-transform:var(--dt);letter-spacing:var(--dl);line-height:var(--dlh)}
.b{font-family:var(--b),sans-serif;line-height:1.36;text-wrap:balance}
.card{background:#fff;border:5px solid #0A0A0A;box-shadow:12px 12px 0 #0A0A0A}
.blue{color:#1F3BFF}
.hl{position:relative;display:inline-block;white-space:nowrap;background:#DDE4FF;border:4px solid #1F3BFF;padding:0 .16em;margin:0 .04em}
.hl i{position:absolute;width:15px;height:15px;background:#fff;border:3px solid #1F3BFF}
.hl i:nth-child(1){left:-11px;top:-11px}.hl i:nth-child(2){right:-11px;top:-11px}
.hl i:nth-child(3){left:-11px;bottom:-11px}.hl i:nth-child(4){right:-11px;bottom:-11px}
.pill{position:absolute;background:#fff;border:3px solid #1F3BFF;border-radius:999px;color:#1F3BFF;font-family:'Inter',sans-serif;font-weight:700;font-size:22px;padding:5px 18px;white-space:nowrap}
.pillk{background:#0A0A0A;color:#fff;border-radius:999px;padding:4px 22px;display:inline-block;white-space:nowrap}
.wavy{text-decoration:underline wavy #1F3BFF;text-decoration-thickness:6px;text-underline-offset:12px}
.stamp{display:inline-block;border:6px solid #1F3BFF;color:#1F3BFF;padding:0 .2em;transform:rotate(-4deg);white-space:nowrap}
.marker{background:linear-gradient(transparent 12%,#BFCBFF 12%,#BFCBFF 92%,transparent 92%);padding:0 .1em;transform:rotate(-1deg);display:inline-block;white-space:nowrap}
.sticker{position:absolute;background:#1F3BFF;color:#fff;font-family:'Inter',sans-serif;font-weight:800;font-size:26px;padding:8px 20px;border:4px solid #0A0A0A;white-space:nowrap}
.next{position:absolute;right:8px;bottom:8px;width:84px;height:84px;border-radius:50%;background:#1F3BFF;border:4px solid #0A0A0A;box-shadow:5px 5px 0 #0A0A0A;display:flex;align-items:center;justify-content:center}
.guide{position:absolute;left:50px;top:180px;width:980px;height:1080px;border:3px dashed #ff00cc;z-index:99;pointer-events:none}
"""

CURSOR = (
    '<svg class="abs" style="left:%dpx;top:%dpx;width:54px;height:54px;transform:rotate(%ddeg)" viewBox="0 0 24 24">'
    '<path d="M3 2 L3 19 L8 14.5 L11.5 22 L14.5 20.6 L11 13.2 L18 13 Z" fill="#fff" stroke="#0A0A0A" stroke-width="1.6" stroke-linejoin="round"/></svg>'
)
ARROW = (
    '<div class="next"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.2" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 5l7 7-7 7"/></svg></div>'
)


def hl(t):
    return '<span class="hl">%s<i></i><i></i><i></i><i></i></span>' % t


def cursor(x, y, r=-8):
    return CURSOR % (x, y, r)


def check(color="#1F3BFF"):
    return (
        '<svg width="40" height="40" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="%s"/>'
        '<path d="M6.5 12.5l3.5 3.5 7.5-8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        % color
    )


def fonts_dir():
    return os.environ.get("FONTS_DIR") or os.path.join(os.getcwd(), "node_modules", "@fontsource")


def ensure_fonts(faces):
    fd = fonts_dir()
    prefix = os.path.dirname(os.path.dirname(fd))
    for _, pkg, _ in faces:
        if not os.path.isdir(os.path.join(fd, pkg)):
            print("npm install @fontsource/" + pkg, file=sys.stderr)
            subprocess.run(["npm", "i", "--prefix", prefix, "@fontsource/" + pkg], check=True)


def font_css(faces):
    fd = fonts_dir()
    css = []
    for fam, pkg, weights in faces:
        for w in weights:
            f = os.path.join(fd, pkg, "files", f"{pkg}-latin-{w}-normal.woff2")
            if os.path.exists(f):
                css.append(
                    "@font-face{font-family:'%s';font-weight:%d;font-style:normal;src:url('file://%s') format('woff2');}"
                    % (fam, w, f)
                )
            else:
                print("MISSING FONT", f, file=sys.stderr)
    return "\n".join(css)


def run(slides, out_dir, extra_faces=None, argv=None):
    """slides: daftar fungsi yang mengembalikan (kelas_font, html_isi)."""
    argv = sys.argv[1:] if argv is None else argv
    faces = BASE_FACES + (extra_faces or [])
    ensure_fonts(faces)
    fcss = font_css(faces)
    guides = "--guides" in argv
    only = [int(a) for a in argv if a.isdigit()]
    tmp = tempfile.mkdtemp(prefix="carousel_")
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1440})
        for i, fn in enumerate(slides, 1):
            if only and i not in only:
                continue
            fclass, inner = fn()
            g = '<div class="guide"></div>' if guides else ""
            html = (
                "<!doctype html><html><head><meta charset='utf-8'><style>%s\n%s</style></head>"
                "<body class='%s'><div class='safe'>%s</div>%s</body></html>" % (fcss, BASE, fclass, inner, g)
            )
            name = f"slide_{i:02d}" + ("_guides" if guides else "")
            path = os.path.join(tmp, name + ".html")
            open(path, "w").write(html)
            pg.goto("file://" + path)
            pg.wait_for_timeout(500)
            dest = os.path.join(out_dir if not guides else tmp, name + ".png")
            pg.screenshot(path=dest, clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            print("ok", dest)
        br.close()
