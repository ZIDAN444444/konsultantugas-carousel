#!/usr/bin/env python3
# Carousel @konsultantugas: skill dasar kampus yang jarang diajarkan (2026-09-23)
# Gaya diadaptasi dari referensi editorial (serif tinggi-kontras, kertas krem bergaris,
# coretan tangan) dengan warna aksen biru brand, bukan oranye. 8 slide.
# Font cover baru: Playfair Display + Work Sans.
import os, sys, subprocess
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BLUE = "#1F3BFF"

FONT_SPECS = [
    ("Playfair Display", "playfair-display", 700, "normal"),
    ("Playfair Display", "playfair-display", 800, "normal"),
    ("Playfair Display", "playfair-display", 900, "normal"),
    ("Playfair Display Italic", "playfair-display", 700, "italic"),
    ("Playfair Display Italic", "playfair-display", 800, "italic"),
    ("Playfair Display Italic", "playfair-display", 900, "italic"),
    ("Work Sans", "work-sans", 500, "normal"),
    ("Work Sans", "work-sans", 600, "normal"),
    ("Work Sans", "work-sans", 700, "normal"),
    ("Work Sans", "work-sans", 800, "normal"),
]


def ensure_fonts():
    fd = os.environ.get("FONTS_DIR") or os.path.join(HERE, "..", "node_modules", "@fontsource")
    prefix = os.path.dirname(os.path.dirname(fd))
    pkgs = sorted({pkg for _, pkg, _, _ in FONT_SPECS})
    missing = [pkg for pkg in pkgs if not os.path.isdir(os.path.join(fd, pkg))]
    if missing:
        print("npm install " + " ".join("@fontsource/" + p for p in missing), file=sys.stderr)
        subprocess.run(["npm", "i", "--prefix", prefix] + ["@fontsource/" + p for p in missing], check=True)

BASE = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1440px}
body{position:relative;overflow:hidden;background-color:#F2F0E8;
 background-image:repeating-linear-gradient(90deg,transparent,transparent 78px,rgba(10,10,10,0.07) 78px,rgba(10,10,10,0.07) 79px);
 color:#0A0A0A;font-family:'Work Sans',sans-serif}
.safe{position:absolute;left:56px;top:150px;width:968px;height:1140px}
.abs{position:absolute}
.brand{position:absolute;left:0;right:0;top:56px;text-align:center;font-family:'Work Sans',sans-serif;font-weight:700;font-size:26px;letter-spacing:.5px;color:#0A0A0A}
.pf{font-family:'Playfair Display',serif;font-weight:900;letter-spacing:-1.5px;line-height:0.98;white-space:nowrap}
.pfi{font-family:'Playfair Display Italic',serif;font-weight:900;font-style:italic;letter-spacing:-1.5px;line-height:0.98;white-space:nowrap}
.blue{color:%s}
.lbl{font-family:'Work Sans',sans-serif;font-weight:800;font-size:22px;letter-spacing:1.5px;text-transform:uppercase}
.body{font-family:'Work Sans',sans-serif;font-weight:500;line-height:1.55}
.footer{position:absolute;left:56px;right:56px;bottom:60px;display:flex;align-items:center;justify-content:space-between}
.arrowbtn{width:74px;height:74px;border-radius:50%%;background:%s;display:flex;align-items:center;justify-content:center}
.bignum{position:absolute;font-family:'Playfair Display',serif;font-weight:900;font-size:420px;color:rgba(10,10,10,0.05);line-height:1;right:-20px;top:60px}
.guide{position:absolute;left:56px;top:150px;width:968px;height:1140px;border:3px dashed #ff00cc;z-index:99;pointer-events:none}
""" % (BLUE, BLUE)

ARROW_BTN = (
    '<div class="footer"><div class="lbl" style="color:%s">Skill kampus</div>'
    '<div class="arrowbtn"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 5l7 7-7 7"/></svg></div></div>'
) % BLUE


def circle(x, y, w, h, rot=-3):
    return (
        '<svg class="abs" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;transform:rotate(%ddeg)" viewBox="0 0 300 140">'
        '<path d="M60 18 C 20 26, 6 60, 14 88 C 24 118, 70 132, 140 130 C 210 128, 280 110, 288 74 '
        'C 294 46, 250 16, 180 10 C 165 8, 172 2, 190 6" '
        'fill="none" stroke="%s" stroke-width="9" stroke-linecap="round"/></svg>'
        % (x, y, w, h, rot, BLUE)
    )


def underline(x, y, w, rot=-1):
    return (
        '<svg class="abs" style="left:%dpx;top:%dpx;width:%dpx;height:36px;transform:rotate(%ddeg)" viewBox="0 0 400 36">'
        '<path d="M6 20 C 100 6, 300 32, 394 12" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round"/></svg>'
        % (x, y, w, rot, BLUE)
    )


def arrow_curl(x, y, w=140, h=170, rot=0):
    return (
        '<svg class="abs" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;transform:rotate(%ddeg)" viewBox="0 0 140 170">'
        '<path d="M30 4 C 54 4, 58 26, 36 30 C 16 32, 14 10, 36 6 C 76 -2, 118 50, 96 130" '
        'fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/>'
        '<path d="M74 120 L98 138 L116 110" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>' % (x, y, w, h, rot, BLUE, BLUE)
    )


# ---------------------------------------------------------------- slides
def s1():
    return """
<div class="brand">@konsultantugas</div>
<div class="abs pf" style="left:2px;top:150px;font-size:108px">Kamu jago</div>
<div class="abs pf" style="left:2px;top:270px;font-size:108px">Canva.</div>
%s
<div class="abs pfi blue" style="left:2px;top:470px;font-size:100px">Tapi daftar isi</div>
<div class="abs pfi blue" style="left:2px;top:582px;font-size:100px">otomatis?</div>
%s
<div class="abs body" style="left:290px;top:830px;font-size:36px;font-weight:700">Belum tentu.</div>
""" % (
        circle(-30, 240, 400, 160, -3),
        arrow_curl(60, 700, 150, 150, 8),
    ) + ARROW_BTN


def item_card(no, line1, line2, body_txt):
    return """
<div class="bignum">%s</div>
<div class="abs pf" style="left:2px;top:140px;font-size:90px">%s</div>
<div class="abs pfi blue" style="left:2px;top:250px;font-size:90px">%s</div>
%s
<div class="abs body" style="left:4px;top:470px;width:800px;font-size:33px">%s</div>
""" % (no, line1, line2, underline(0, 350, 340, -2), body_txt)


def s2():
    return item_card(
        "1", "Bikin daftar isi", "otomatis",
        'Pakai Heading 1, 2, 3 di Word buat tiap bab dan sub-bab. Nanti daftar isi tinggal <b>References &gt; Table of Contents</b>, bukan ngetik manual satu-satu.',
    ) + ARROW_BTN


def s3():
    return item_card(
        "2", "Rapikan sitasi", "otomatis",
        'Simpan sumber di Zotero atau Mendeley, lalu masukkan kutipan langsung dari situ. Daftar pustaka ikut tersusun sendiri, formatnya konsisten.',
    ) + ARROW_BTN


def s4():
    return item_card(
        "3", "Kirim email", "yang dibalas",
        'Subjek jelas, sapaan formal, langsung ke inti, tutup dengan satu permintaan spesifik. Dosen sibuk, email panjang tanpa poin sering kelewat.',
    ) + ARROW_BTN


def s5():
    return item_card(
        "4", "Cari jurnal asli", "bukan blog",
        'Mulai dari Google Scholar atau situs jurnal resmi kampus, bukan hasil googling biasa. Cek nama penulis dan tahun terbit sebelum dikutip.',
    ) + ARROW_BTN


def s6():
    return item_card(
        "5", "Kasih nama file", "yang jelas",
        '"Tugas_SIM_Bab2_Revisi2.docx", bukan "dokumen baru (3).docx". Dosen dan tim kelompokmu jadi gampang nyari versi yang benar.',
    ) + ARROW_BTN


def s7():
    return """
<div class="brand">@konsultantugas</div>
<div class="abs pf" style="left:2px;top:180px;font-size:100px">Bukan gaptek.</div>
<div class="abs pfi blue" style="left:2px;top:480px;font-size:100px">Cuma nggak</div>
<div class="abs pfi blue" style="left:2px;top:592px;font-size:100px">pernah diajarin.</div>
%s
<div class="abs body" style="left:2px;top:850px;width:820px;font-size:34px;font-weight:600">5 hal ini nggak diajarkan formal, tapi dipakai terus sampai skripsi.</div>
""" % underline(0, 300, 480, -2) + ARROW_BTN


def s8():
    return """
<div class="brand">@konsultantugas</div>
<div class="abs pf" style="left:2px;top:220px;font-size:110px">Simpan ini.</div>
%s
<div class="abs pfi blue" style="left:2px;top:540px;font-size:110px">Biar nggak</div>
<div class="abs pfi blue" style="left:2px;top:652px;font-size:110px">lupa.</div>
<div class="abs body" style="left:2px;top:900px;width:800px;font-size:33px;font-weight:600">Kirim ke temanmu yang masih ngetik daftar isi manual.</div>
""" % circle(388, 190, 200, 150, -6) + ARROW_BTN


SLIDES = [s1, s2, s3, s4, s5, s6, s7, s8]


def font_css():
    ensure_fonts()
    fd = os.environ.get("FONTS_DIR") or os.path.join(HERE, "..", "node_modules", "@fontsource")
    css = []
    for fam, pkg, w, style in FONT_SPECS:
        f = os.path.join(fd, pkg, "files", f"{pkg}-latin-{w}-{style}.woff2")
        if os.path.exists(f):
            css.append(
                "@font-face{font-family:'%s';font-weight:%d;font-style:%s;src:url('file://%s') format('woff2');}"
                % (fam, w, style, f)
            )
        else:
            print("MISSING FONT", f, file=sys.stderr)
    return "\n".join(css)


def build_page(inner, guides=False):
    g = '<div class="guide"></div>' if guides else ""
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>%s\n%s</style></head>"
        "<body><div class='safe'>%s</div>%s</body></html>" % (font_css(), BASE, inner, g)
    )


def main():
    argv = sys.argv[1:]
    guides_only = "--guides" in argv
    only = [int(a) for a in argv if a.isdigit()]
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1440})
        for i, fn in enumerate(SLIDES, 1):
            if only and i not in only:
                continue
            for guides in ([True] if guides_only else [False]):
                html = build_page(fn(), guides)
                path = os.path.join(HERE, f"_tmp_{i}.html")
                open(path, "w").write(html)
                pg.goto("file://" + path)
                pg.wait_for_timeout(500)
                name = f"slide_{i:02d}" + ("_guides" if guides else "")
                dest = os.path.join(HERE, f"{name}.png")
                pg.screenshot(path=dest, clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
                os.remove(path)
                print("ok", dest)
        br.close()


if __name__ == "__main__":
    main()
