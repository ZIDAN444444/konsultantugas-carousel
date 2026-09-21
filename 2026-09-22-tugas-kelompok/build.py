#!/usr/bin/env python3
# Carousel @konsultantugas: kenapa satu orang selalu kerja sendiri di tugas kelompok (2026-09-22)
# 6 slide, slide 5 promosi jasa, slide 6 CTA WhatsApp. Font cover baru: Unbounded + Plus Jakarta Sans.
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import *  # noqa

EXTRA = [("Unbounded", "unbounded", [700, 800]), ("Plus Jakarta Sans", "plus-jakarta-sans", [400, 500, 700]),
         ("Syne", "syne", [700, 800]), ("Manrope", "manrope", [400, 500, 700])]
V6 = "<style>body.v6{--d:'Unbounded',sans-serif;--b:'Plus Jakarta Sans';--dw:800;--dt:none;--dl:-2px;--dlh:1.08}</style>"
WA = "+62 858-3212-8420"


def person(x, working, label):
    fill = "#1F3BFF" if working else "#fff"
    pill_bg = "#1F3BFF" if working else "#fff"
    pill_fg = "#fff" if working else "#0A0A0A"
    return (
        '<div class="abs" style="left:%dpx;top:60px;width:150px;text-align:center">'
        '<div style="display:inline-block;background:%s;color:%s;border:3px solid #0A0A0A;border-radius:999px;padding:4px 14px;'
        'font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;font-size:19px;white-space:nowrap">%s</div></div>'
        '<div class="abs" style="left:%dpx;top:140px;width:64px;height:64px;border-radius:50%%;background:%s;border:5px solid #0A0A0A"></div>'
        '<div class="abs" style="left:%dpx;top:214px;width:110px;height:120px;border-radius:55px 55px 12px 12px;background:%s;border:5px solid #0A0A0A"></div>'
        % (x - 75 + 55, pill_bg, pill_fg, label, x + 23, fill, x, fill)
    )


def s1():
    labels = ["ngerjain semua", "besok aja", "lagi sibuk", "sinyal jelek", "lagi kelas"]
    people = ""
    for i, lb in enumerate(labels):
        people += person(30 + i * 170, i == 0, lb)
    return "v6", V6 + """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:14px;top:96px;width:960px;font-size:84px">Kelompok 5 orang, yang kerja %s</div>
<div class="abs b" style="left:0;top:340px;width:620px;font-size:30px;font-weight:500">Itu bukan kebetulan. Psikologi punya namanya.</div>
<div class="abs card" style="left:12px;top:470px;width:900px;height:400px;transform:rotate(-1deg)">
  %s
</div>
""" % (hl("1."), people) + ARROW


def s2():
    dots = ""
    for i in range(78):
        r, c = divmod(i, 13)
        dots += '<div class="abs" style="left:%dpx;top:%dpx;width:34px;height:34px;border-radius:50%%;background:#1F3BFF;border:3px solid #0A0A0A"></div>' % (
            36 + c * 64, 88 + r * 50)
    return "v3", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:980px;font-size:96px">Namanya<br><span class="wavy">social loafing</span></div>
<div class="abs b" style="left:0;top:350px;width:880px;font-size:30px;font-weight:500">Orang cenderung mengurangi usaha saat kerja bareng dibanding kerja sendiri. Analisis gabungan 78 studi menemukan pola ini kuat di berbagai jenis tugas dan kelompok orang.</div>
<div class="abs card" style="left:12px;top:590px;width:880px;height:400px;transform:rotate(1deg)">
  <div class="b" style="position:absolute;left:30px;top:22px;font-size:24px;font-weight:800;letter-spacing:.5px">1 TITIK = 1 STUDI</div>
  %s
</div>
""" % dots + ARROW


def s3():
    return "v1", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:6px;top:96px;width:940px;font-size:100px">yang peduli,<br>yang <span class="marker">nutupin</span></div>
<div class="abs b" style="left:6px;top:400px;width:470px;font-size:28px;font-weight:500">Peneliti menyebutnya social compensation. Di 3 eksperimen, orang bekerja lebih keras saat menduga temannya lemah, asal tugasnya dianggap penting.<br><br>Kalau tugasnya dianggap remeh, mereka tidak menutupi.</div>
<div class="abs card" style="left:516px;top:400px;width:420px;height:230px;transform:rotate(1.5deg)">
  <div class="b blue" style="position:absolute;left:26px;top:20px;font-size:22px;font-weight:800;letter-spacing:.5px">TUGAS PENTING</div>
  <div class="b" style="position:absolute;left:26px;top:60px;width:360px;font-size:28px;font-weight:700;line-height:1.2">Teman diduga lemah, kamu kerja ekstra</div>
  <div class="d blue" style="position:absolute;right:24px;top:150px;font-size:56px;line-height:1">+</div>
</div>
<div class="abs card" style="left:516px;top:670px;width:420px;height:230px;transform:rotate(-1.5deg);background:#DDE4FF">
  <div class="b" style="position:absolute;left:26px;top:20px;font-size:22px;font-weight:800;letter-spacing:.5px">TUGAS REMEH</div>
  <div class="b" style="position:absolute;left:26px;top:60px;width:360px;font-size:28px;font-weight:700;line-height:1.2">Tidak ada yang menutupi</div>
  <div class="d" style="position:absolute;right:24px;top:150px;font-size:56px;line-height:1">0</div>
</div>
<div class="pill" style="left:6px;top:850px;transform:rotate(-2deg)">hasil eksperimen lab, bukan survei kelas</div>
""" + ARROW


def row(n, t, s):
    return (
        '<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:34px">'
        '<div class="d blue" style="font-size:110px;width:70px;line-height:.9">%s</div>'
        '<div><div class="b" style="font-size:34px;font-weight:800;line-height:1.15">%s</div>'
        '<div class="b" style="font-size:24px;font-weight:500;margin-top:8px">%s</div></div></div>' % (n, t, s)
    )


def s4():
    return "v2", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:980px;font-size:126px">3 cara <span class="stamp">memecahnya</span></div>
<div class="abs card" style="left:12px;top:330px;width:900px;height:540px;transform:rotate(-1deg)">
  <div class="abs" style="left:40px;top:44px;width:820px">
    %s%s%s
  </div>
</div>
<div class="abs b" style="left:0;top:930px;width:800px;font-size:24px;font-weight:600">Temuan dari studi mahasiswa di AS dan analisis 78 studi, bukan jaminan untuk kelompokmu.</div>
""" % (
        row("1", "Tulis nama pemilik tiap bagian", "Kontribusi yang kelihatan menekan malas-malasan."),
        row("2", "Usul kelompok kecil, cakupan sempit", "Makin besar kelompok dan proyek, makin sering terjadi."),
        row("3", "Usul penilaian teman berkali-kali", "Penilaian antaranggota di tengah proyek menurunkannya."),
    ) + ARROW


def s5():
    item = lambda t: (
        '<div style="display:flex;gap:16px;align-items:center;margin-bottom:22px">%s'
        '<div class="b" style="font-size:31px;font-weight:700;line-height:1.2">%s</div></div>' % (check(), t)
    )
    return "v5", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:14px;top:96px;width:950px;font-size:66px">Kelompokmu macet? %s dulu.</div>
<div class="abs card" style="left:12px;top:400px;width:900px;height:360px;transform:rotate(1deg)">
  <div class="b blue" style="position:absolute;left:34px;top:26px;font-size:24px;font-weight:800;letter-spacing:1px">KONSULTAN TUGAS BANTU</div>
  <div class="abs" style="left:34px;top:84px;width:820px">
    %s%s%s
  </div>
</div>
<div class="abs b" style="left:0;top:810px;width:760px;font-size:28px;font-weight:600">Tanya kebutuhanmu lewat WhatsApp, ceritakan tugas dan tenggatnya.</div>
""" % (
        hl("Konsultasi"),
        item("Format tugas rapi sesuai pedoman kampus"),
        item("Struktur dan alur tulisan"),
        item("Referensi jurnal yang dicek nyata"),
    ) + ARROW


def s6():
    return "v4", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:14px;top:96px;width:960px;font-size:104px">Hubungi lewat %s</div>
<div class="abs card" style="left:12px;top:420px;width:900px;height:300px;transform:rotate(-1.5deg);background:#1F3BFF;box-shadow:12px 12px 0 #0A0A0A">
  <div class="b" style="position:absolute;left:34px;top:30px;color:#DDE4FF;font-size:26px;font-weight:700">Chat via WhatsApp</div>
  <div class="d" style="position:absolute;left:34px;top:100px;color:#fff;font-size:70px;white-space:nowrap;letter-spacing:-2px">%s</div>
  <div class="b" style="position:absolute;left:34px;top:220px;color:#DDE4FF;font-size:26px;font-weight:500">ceritakan tugas dan tenggatmu</div>
</div>
<div class="abs b" style="left:0;top:790px;width:860px;font-size:32px;font-weight:600">Simpan biar tidak lupa. Kirim ke temanmu yang lagi kena kelompok begini.</div>
<div class="abs" style="left:0;top:960px;width:640px;height:92px;border-radius:999px;background:#0A0A0A;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:8px 8px 0 #1F3BFF"><span class="d" style="font-size:44px;letter-spacing:0">follow @konsultantugas</span></div>
""" % (hl("WhatsApp"), WA)


SLIDES = [s1, s2, s3, s4, s5, s6]

if __name__ == "__main__":
    run(SLIDES, HERE, extra_faces=EXTRA)
