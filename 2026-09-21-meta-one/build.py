#!/usr/bin/env python3
# Carousel @konsultantugas: Meta One (2026-09-21)
# Dijalankan otomatis oleh GitHub Actions (.github/workflows/render.yml)
import glob, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
import tempfile
FONTS = os.environ.get("FONTS_DIR") or os.path.join(ROOT, "node_modules", "@fontsource")
OUT = ROOT  # PNG ditulis di folder yang sama dengan skrip ini
HTML = tempfile.mkdtemp(prefix="carousel_html_")
QA = tempfile.mkdtemp(prefix="carousel_qa_")

FACES = [
    ("GFS Didot", "gfs-didot", [400]),
    ("Inter", "inter", [400, 500, 700, 800]),
    ("Bebas Neue", "bebas-neue", [400]),
    ("Montserrat", "montserrat", [400, 500, 700, 800]),
    ("Poppins", "poppins", [600, 800]),
    ("DM Sans", "dm-sans", [400, 500, 700]),
    ("Archivo Black", "archivo-black", [400]),
    ("Space Grotesk", "space-grotesk", [400, 500, 700]),
]


def font_css():
    css = []
    for fam, pkg, weights in FACES:
        for w in weights:
            f = os.path.join(FONTS, pkg, "files", f"{pkg}-latin-{w}-normal.woff2")
            if os.path.exists(f):
                css.append(
                    "@font-face{font-family:'%s';font-weight:%d;font-style:normal;src:url('file://%s') format('woff2');}"
                    % (fam, w, f)
                )
            else:
                print("MISSING FONT", f, file=sys.stderr)
    return "\n".join(css)


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


def lock():
    return (
        '<svg width="40" height="40" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10.5" fill="#fff" stroke="#0A0A0A" stroke-width="2" stroke-dasharray="3 2.4"/>'
        '<text x="12" y="16.5" font-family="Inter" font-weight="800" font-size="12" text-anchor="middle" fill="#0A0A0A">$</text></svg>'
    )


# ---------------------------------------------------------------- slides
def s1():
    return "v4", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:14px;top:96px;width:960px;font-size:124px">Meta One:<br>%s atau<br>tidak?</div>
%s
<div class="abs b" style="left:0;top:520px;width:470px;font-size:34px;font-weight:500">4 fakta dari pengumuman resmi Meta yang jarang dibahas.</div>
<div class="abs" style="left:10px;top:800px;transform:rotate(-4deg);border:5px solid #0A0A0A;padding:14px 26px;background:#fff;box-shadow:8px 8px 0 #0A0A0A">
  <div class="b" style="font-size:22px;font-weight:700;letter-spacing:1px">DIUMUMKAN</div>
  <div class="d" style="font-size:52px;line-height:1.05">15 Sep 2026</div>
</div>
<!-- kartu belakang -->
<div class="abs card" style="left:500px;top:540px;width:410px;height:250px;transform:rotate(6deg);background:#1F3BFF;box-shadow:12px 12px 0 #0A0A0A">
  <div class="b" style="position:absolute;left:26px;top:22px;color:#fff;font-size:26px;font-weight:700">Core</div>
  <div class="d" style="position:absolute;left:26px;top:70px;color:#fff;font-size:92px">$7.99</div>
  <div class="b" style="position:absolute;left:26px;top:186px;color:#DDE4FF;font-size:24px;font-weight:500">per bulan</div>
</div>
<!-- kartu depan -->
<div class="abs card" style="left:390px;top:720px;width:430px;height:270px;transform:rotate(-3deg)">
  <div class="b" style="position:absolute;left:28px;top:24px;font-size:26px;font-weight:700">Meta AI, sehari-hari</div>
  <div class="d blue" style="position:absolute;left:28px;top:70px;font-size:120px">$0</div>
  <div class="b" style="position:absolute;left:28px;top:208px;font-size:24px;font-weight:500">kata Meta, tetap gratis</div>
</div>
%s
""" % (hl("bayar"), '', cursor(770, 930, -6)) + ARROW


def s2():
    return "v1", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:480px;font-size:96px">yang gratis<br>tetap <span class="marker">gratis</span></div>
<div class="abs b" style="left:0;top:450px;width:470px;font-size:29px;font-weight:500">15 September 2026, Meta meluncurkan Meta One, langganan berbayar untuk Instagram, Facebook, WhatsApp, dan Meta AI.<br><br>Menurut Meta, pengalaman inti dan Meta AI untuk pemakaian sehari-hari tidak berubah.</div>
<div class="abs d blue" style="left:0;top:815px;font-size:170px;line-height:1">50+</div>
<div class="abs b" style="left:315px;top:840px;width:195px;font-size:24px;font-weight:700;line-height:1.25">fitur berbayar di hari peluncuran</div>

<div class="abs card" style="left:516px;top:70px;width:428px;height:880px;transform:rotate(1.5deg)">
  <div class="b" style="position:absolute;left:34px;top:30px;font-size:28px;font-weight:800;letter-spacing:1px">TETAP GRATIS</div>
  <div class="abs" style="left:30px;top:88px;width:380px">
    <div style="display:flex;gap:16px;align-items:center;margin-bottom:26px">%s<div class="b" style="font-size:29px;font-weight:600;line-height:1.2">Pengalaman inti di semua aplikasi</div></div>
    <div style="display:flex;gap:16px;align-items:center">%s<div class="b" style="font-size:29px;font-weight:600;line-height:1.2">Meta AI untuk pemakaian sehari-hari</div></div>
  </div>
  <div class="abs" style="left:30px;top:340px;width:390px;border-top:4px dashed #0A0A0A"></div>
  <div class="b" style="position:absolute;left:34px;top:376px;font-size:28px;font-weight:800;letter-spacing:1px;color:#1F3BFF">BERBAYAR (META ONE)</div>
  <div class="abs" style="left:30px;top:436px;width:380px">
    <div style="display:flex;gap:16px;align-items:center;margin-bottom:26px">%s<div class="b" style="font-size:29px;font-weight:600;line-height:1.2">Fitur gaya dan personalisasi</div></div>
    <div style="display:flex;gap:16px;align-items:center;margin-bottom:26px">%s<div class="b" style="font-size:29px;font-weight:600;line-height:1.2">Pemakaian AI lebih besar</div></div>
    <div style="display:flex;gap:16px;align-items:center">%s<div class="b" style="font-size:29px;font-weight:600;line-height:1.2">Alat untuk kreator dan bisnis</div></div>
  </div>
</div>
<div class="sticker" style="left:740px;top:820px;transform:rotate(-6deg)">dari Meta</div>
""" % (check("#0A0A0A"), check("#0A0A0A"), lock(), lock(), lock()) + ARROW


def plan(name, price, x, y, rot, dark=False):
    bg = "#0A0A0A" if dark else "#fff"
    fg = "#fff" if dark else "#0A0A0A"
    return (
        '<div class="abs card" style="left:%dpx;top:%dpx;width:290px;height:330px;transform:rotate(%sdeg);background:%s;color:%s">'
        '<div class="b" style="position:absolute;left:24px;top:24px;font-size:30px;font-weight:700;line-height:1.1">%s</div>'
        '<div class="d" style="position:absolute;left:24px;top:120px;font-size:96px;color:%s">%s</div>'
        '<div class="b" style="position:absolute;left:24px;top:250px;font-size:26px;font-weight:500">per bulan</div>'
        "</div>" % (x, y, rot, bg, fg, name, "#8FA3FF" if dark else "#1F3BFF", price)
    )


def s3():
    return "v3", """
<div class="brand">@konsultantugas</div>
%s%s%s
%s
<div class="abs d" style="left:0;top:560px;width:960px;font-size:84px">Paket satuan itu<br>soal <span class="wavy">gaya</span></div>
<div class="abs b" style="left:0;top:790px;width:760px;font-size:32px;font-weight:500">Isinya font DM dan Story kustom, tema WhatsApp, dan pin lebih banyak chat.<br>Enak dipakai, tapi bukan kebutuhan kuliah.</div>
<div class="pill" style="left:650px;top:880px;transform:rotate(3deg)">harga dalam dolar AS</div>
""" % (
        plan("Instagram Plus", "$3.99", 10, 70, -3),
        plan("Facebook Plus", "$3.99", 345, 120, 2),
        plan("WhatsApp Plus", "$2.99", 655, 60, -2, True),
        cursor(860, 330, -10),
    ) + ARROW


def bar(label, w, color, y, note):
    return (
        '<div class="abs b" style="left:0;top:%dpx;width:190px;font-size:26px;font-weight:700">%s</div>'
        '<div class="abs" style="left:200px;top:%dpx;width:%dpx;height:50px;background:%s;border:4px solid #0A0A0A;box-shadow:6px 6px 0 #0A0A0A"></div>'
        '<div class="abs b" style="left:%dpx;top:%dpx;font-size:24px;font-weight:600">%s</div>'
        % (y + 6, label, y, w, color, 200 + w + 22, y + 8, note)
    )


def s4():
    return "v2", """
<div class="brand">@konsultantugas</div>
<div class="abs d blue" style="left:-6px;top:50px;font-size:300px;line-height:1">$7.99</div>
<div class="abs b" style="left:6px;top:330px;font-size:26px;font-weight:700">Core, per bulan</div>
<div class="abs d" style="left:560px;top:96px;width:420px;font-size:112px">Paket AI:<br>bayar buat<br><span class="stamp">kuota</span></div>
<div class="abs card" style="left:0;top:430px;width:900px;height:290px;box-shadow:12px 12px 0 #0A0A0A">
  <div class="b" style="position:absolute;left:28px;top:16px;font-size:24px;font-weight:700">Jatah bikin gambar dan video di Meta AI</div>
  <div class="pill" style="right:24px;top:14px;font-size:20px;padding:3px 14px">ilustrasi</div>
  <div class="abs" style="left:28px;top:70px;width:830px;height:200px">
    %s
  </div>
</div>
<div class="abs b" style="left:0;top:790px;width:800px;font-size:31px;font-weight:500">Core $7.99 dan Premium $19.99 per bulan menambah jatah bikin gambar dan video di Meta AI.<br>Buat pemakaian sehari-hari, Meta AI tetap gratis.</div>
""" % (
        bar("Gratis", 150, "#fff", 0, "")
        + bar("Core", 330, "#BFCBFF", 65, "")
        + bar("Premium", 520, "#1F3BFF", 130, "")
    ) + ARROW


def rung(name, price, y, w, color, fg="#0A0A0A"):
    return (
        '<div class="abs" style="left:%dpx;top:%dpx;width:372px;height:96px;background:%s;color:%s;border:4px solid #0A0A0A;box-shadow:6px 6px 0 #0A0A0A">'
        '<div class="b" style="position:absolute;left:18px;top:26px;font-size:28px;font-weight:800">%s</div>'
        '<div class="d" style="position:absolute;right:18px;top:18px;font-size:42px;line-height:1">%s</div></div>'
        % (w, y, color, fg, name, price)
    )


def s5():
    return "v1", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="right:36px;top:96px;width:760px;text-align:right;font-size:92px">kalau kamu jualan<br>atau <span style="position:relative;display:inline-block;padding:0 .12em">ngonten<svg class="abs" style="left:-20px;top:-16px;width:calc(100%% + 40px);height:calc(100%% + 30px)" viewBox="0 0 300 120" preserveAspectRatio="none"><path d="M150 8 C 250 2, 296 40, 285 70 C 270 108, 170 116, 110 112 C 30 108, 4 80, 14 46 C 26 16, 90 6, 168 6" fill="none" stroke="#1F3BFF" stroke-width="6" stroke-linecap="round"/></svg></span></div>
<div class="abs card" style="left:12px;top:420px;width:466px;height:540px;transform:rotate(-1.5deg)">
  <div class="b" style="position:absolute;left:24px;top:18px;font-size:22px;font-weight:800;letter-spacing:1px">HARGA MULAI DARI, PER BULAN</div>
  <div class="abs" style="left:24px;top:64px;width:420px">
    %s%s%s%s
  </div>
</div>
<div class="abs b" style="left:530px;top:440px;width:450px;font-size:31px;font-weight:500">Essential dari $14.99: badge verifikasi dan agen bisnis di WhatsApp.<br><br>Jadwal Story sampai 30 hari baru mulai dari Advanced.<br><br>Badge tetap harus lolos pengecekan.</div>
<div class="pill" style="left:560px;top:930px;transform:rotate(-2deg);display:none">x</div>
""" % (
        rung("Essential", "$14.99+", 0, 0, "#fff"),
        rung("Advanced", "$49.99+", 112, 12, "#DDE4FF"),
        rung("Expert", "$149+", 224, 24, "#BFCBFF"),
        rung("Max", "$499+", 336, 36, "#1F3BFF", "#fff"),
    ) + ARROW


def s6():
    return "v3", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:980px;font-size:90px;white-space:nowrap">Kamu yang <span class="pillk">mana?</span></div>
<div class="abs card" style="left:16px;top:330px;width:440px;height:470px;transform:rotate(-2deg)">
  <div class="b" style="position:absolute;left:26px;top:24px;font-size:26px;font-weight:800;letter-spacing:.5px" >PEMAKAIAN BIASA</div>
  <div class="b" style="position:absolute;left:26px;top:80px;width:390px;font-size:32px;font-weight:500">Tanya-tanya, edit foto sesekali, chat sama teman.</div>
  <div class="d blue" style="position:absolute;left:26px;top:330px;font-size:58px;line-height:1">Tetap gratis</div>
</div>
<div class="abs card" style="left:500px;top:450px;width:450px;height:470px;transform:rotate(2deg);background:#DDE4FF">
  <div class="b" style="position:absolute;left:26px;top:24px;font-size:26px;font-weight:800;letter-spacing:.5px">PEMAKAIAN BERAT</div>
  <div class="b" style="position:absolute;left:26px;top:80px;width:390px;font-size:32px;font-weight:500">Bikin gambar dan video tiap hari buat konten.</div>
  <div class="d blue" style="position:absolute;left:26px;top:330px;width:400px;font-size:52px;line-height:1.05">Bandingkan paket</div>
</div>
<div class="abs" style="left:415px;top:520px;width:110px;height:110px;border-radius:50%;background:#0A0A0A;color:#fff;display:flex;align-items:center;justify-content:center;border:5px solid #fff;z-index:5"><span class="d" style="font-size:44px">VS</span></div>
<div class="abs b" style="left:0;top:940px;width:800px;font-size:26px;font-weight:600">Meta tidak menyebut angka batas pemakaian gratisnya.</div>
""" + ARROW


def s7():
    row = lambda n, t: (
        '<div style="display:flex;align-items:center;gap:22px;margin-bottom:30px">'
        '<div class="d blue" style="font-size:88px;width:70px;line-height:1">%s</div>'
        '<div class="b" style="font-size:36px;font-weight:700;line-height:1.15">%s</div></div>' % (n, t)
    )
    return "v1", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;font-size:130px">catat <span class="wavy">ini</span></div>
<div class="abs card" style="left:120px;top:340px;width:760px;height:560px;transform:rotate(1.5deg)">
  <div class="abs" style="left:44px;top:56px;width:680px">
    %s%s%s%s
  </div>
</div>
<div class="sticker" style="left:560px;top:880px;transform:rotate(-4deg)">buat kamu simpan</div>
<div class="abs b" style="left:0;top:975px;width:800px;font-size:24px;font-weight:600;line-height:1.3">Kata Meta, plan, harga, dan ketersediaan bisa beda per wilayah, aplikasi, dan akun.</div>
""" % (
        row("1", "Cek dulu apa yang kamu pakai"),
        row("2", "Pakai versi gratis dulu"),
        row("3", "Lihat harga di akunmu sendiri"),
        row("4", "Baca syarat uji coba"),
    ) + ARROW


def s8():
    return "v2", """
<div class="brand">@konsultantugas</div>
<div class="abs card" style="left:250px;top:60px;width:480px;height:400px;transform:rotate(-2deg)">
  <div class="abs" style="left:20px;top:18px;width:44px;height:44px;border-radius:50%%;background:#1F3BFF;border:3px solid #0A0A0A"></div>
  <div class="abs b" style="left:78px;top:26px;font-size:22px;font-weight:700">konsultantugas</div>
  <div class="abs" style="left:20px;top:80px;width:436px;height:210px;background:#DDE4FF;border:3px solid #0A0A0A;display:flex;align-items:center;justify-content:center"><span class="d blue" style="font-size:90px;line-height:1">Meta One</span></div>
  <div class="abs" style="left:20px;top:312px;display:flex;gap:26px;align-items:center">
    <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#0A0A0A" stroke-width="2"><path d="M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z"/></svg>
    <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#0A0A0A" stroke-width="2"><path d="M4 5h16v11H9l-5 4z"/></svg>
    <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#0A0A0A" stroke-width="2"><path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/></svg>
  </div>
  <div class="abs" style="right:26px;top:304px;width:62px;height:62px;border-radius:50%%;background:#1F3BFF;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 8px #BFCBFF">
    <svg width="34" height="34" viewBox="0 0 24 24" fill="#fff" stroke="#fff" stroke-width="2" stroke-linejoin="round"><path d="M6 3h12v18l-6-4.5L6 21z"/></svg>
  </div>
</div>
%s
<div class="abs d" style="left:0;top:520px;width:980px;text-align:center;font-size:102px">Simpan <span class="hl">biar tidak lupa</span></div>
<div class="abs b" style="left:110px;top:790px;width:760px;text-align:center;font-size:34px;font-weight:600">Kirim ke temanmu yang mau langganan tanpa baca isinya dulu.</div>
<div class="abs" style="left:150px;top:930px;width:680px;height:96px;border-radius:999px;background:#0A0A0A;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:8px 8px 0 #1F3BFF"><span class="d" style="font-size:58px;letter-spacing:1.5px">Follow @konsultantugas</span></div>
""" % cursor(672, 394, -8)


SLIDES = [s1, s2, s3, s4, s5, s6, s7, s8]


def page(fclass, inner, guides=False):
    g = '<div class="guide"></div>' if guides else ""
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>%s\n%s</style></head>"
        "<body class='%s'><div class='safe'>%s</div>%s</body></html>" % (font_css(), BASE, fclass, inner, g)
    )


def main():
    guides_only = "--guides" in sys.argv
    only = [int(a) for a in sys.argv[1:] if a.isdigit()]
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1440})
        for i, fn in enumerate(SLIDES, 1):
            if only and i not in only:
                continue
            fclass, inner = fn()
            for guides in ([True] if guides_only else [False]):
                name = f"slide_{i:02d}" + ("_guides" if guides else "")
                path = os.path.join(HTML, name + ".html")
                open(path, "w").write(page(fclass, inner, guides))
                pg.goto("file://" + path)
                pg.wait_for_timeout(500)
                dest = os.path.join(OUT if not guides else QA, name + ".png")
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                pg.screenshot(path=dest, clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
        br.close()


if __name__ == "__main__":
    main()
