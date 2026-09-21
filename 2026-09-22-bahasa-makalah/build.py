#!/usr/bin/env python3
# Carousel @konsultantugas: makalahmu kedengaran kayak robot? (2026-09-22)
# 8 slide, slide 7 promosi jasa, slide 8 CTA + QR WhatsApp. Font cover baru: Fraunces + Sora.
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import *  # noqa

EXTRA = [("Fraunces", "fraunces", [700, 800, 900]), ("Sora", "sora", [400, 500, 600, 700]),
         ("Unbounded", "unbounded", [700, 800]), ("Plus Jakarta Sans", "plus-jakarta-sans", [400, 500, 700])]
V7 = "<style>body.v7{--d:'Fraunces',serif;--b:'Sora';--dw:900;--dt:none;--dl:-2px;--dlh:0.98}</style>"
V6 = "<style>body.v6{--d:'Unbounded',sans-serif;--b:'Plus Jakarta Sans';--dw:800;--dt:none;--dl:-2px;--dlh:1.08}</style>"
WA_DISPLAY = "+62 858-3212-8420"

# Matriks QR untuk https://wa.me/6285832128420 (dihitung sekali dengan qrcode lib, dipakai sebagai data statis;
# tidak butuh dependency qrcode saat render supaya tidak gagal kalau CI belum punya paket itu)
QR_ROWS = "0000000000000000000000000000000000000|0000000000000000000000000000000000000|0011111110001000010001100110111111100|0010000010111100011100111010100000100|0010111010001000110010011000101110100|0010111010010101000000101000101110100|0010111010000001111011111000101110100|0010000010100001001101100110100000100|0011111110101010101010101010111111100|0000000000101101101100111010000000000|0000001111011101100101110100110001000|0010011101111001111010001110010111000|0000111110000001101011111101111001000|0011100100011111011111110001001101100|0011011010010110101001100000110100100|0010000101011101100000111111000011000|0011110111001010101101000110001101000|0000010001000000111000110010111101100|0000100011001111010101010101111011000|0000011101010110000111000110000000000|0000011111111011110001101111100100000|0011011100110101110110011000111000100|0010000111101001100010010000001101100|0010001001001001010010101011110010000|0000101110110000101001010110010000000|0000011001010010110001011100000100000|0011111010110111010100010011111001000|0000000000101110111010011110001000000|0011111110100000011011100010101101000|0010000010100010110111001110001101100|0010111010101111011100101011111100000|0010111010010011011011010110111100100|0010111010001111001110000101101110000|0010000010001110010001010111011010000|0011111110000011001001011010110010100|0000000000000000000000000000000000000|0000000000000000000000000000000000000".split("|")

def qr_svg(size=360):
    n = len(QR_ROWS)
    cell = size / n
    rects = []
    for r, row in enumerate(QR_ROWS):
        for c, ch in enumerate(row):
            if ch == "1":
                rects.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>' % (c*cell, r*cell, cell+0.6, cell+0.6))
    return ('<svg width="%d" height="%d" viewBox="0 0 %d %d" fill="#0A0A0A">%s</svg>'
            % (size, size, size, size, "".join(rects)))



def s1():
    return "v7", V7 + """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:6px;top:110px;width:960px;font-size:112px">Makalahmu<br>kedengaran<br>kayak %s?</div>
<div class="abs b" style="left:0;top:640px;width:640px;font-size:31px;font-weight:500">Dosen dan sistem kampus sekarang makin gampang mengenalinya. Ini alasannya, dan cara memperbaikinya.</div>
<div class="abs card" style="left:600px;top:770px;width:260px;height:260px;transform:rotate(4deg);display:flex;align-items:center;justify-content:center">
  <span class="d" style="font-size:115px;line-height:1">🤖</span>
</div>
""" % hl("robot") + ARROW


def s2():
    item = lambda t: (
        '<div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:26px">'
        '<div class="d blue" style="font-size:40px;line-height:1">•</div>'
        '<div class="b" style="font-size:30px;font-weight:600;line-height:1.3">%s</div></div>' % t
    )
    return "v1", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:940px;font-size:92px">4 ciri yang<br>paling <span class="marker">gampang ketahuan</span></div>
<div class="abs card" style="left:12px;top:460px;width:900px;height:520px;transform:rotate(-1deg)">
  <div class="abs" style="left:36px;top:36px;width:820px">
    %s%s%s%s
  </div>
</div>
""" % (
        item("Pembuka klise: \u201cdalam era globalisasi ini\u2026\u201d"),
        item("Kalimat rapi terus, panjangnya mirip semua"),
        item("Tidak ada contoh atau pengalaman yang spesifik"),
        item("Kata yang diulang-ulang: \u201chal ini menunjukkan bahwa\u2026\u201d"),
    ) + ARROW


def bar(label, before, after, y, maxw=560):
    wb = int(before / 137 * maxw)
    wa = int(after / 137 * maxw)
    return (
        '<div class="abs b" style="left:0;top:%dpx;width:220px;font-size:26px;font-weight:700">%s</div>'
        '<div class="abs" style="left:230px;top:%dpx;width:%dpx;height:22px;background:#DDE4FF;border:3px solid #0A0A0A"></div>'
        '<div class="abs" style="left:230px;top:%dpx;width:%dpx;height:22px;background:#1F3BFF;border:3px solid #0A0A0A"></div>'
        '<div class="abs d blue" style="left:%dpx;top:%dpx;font-size:30px">+%d%%</div>'
        % (y + 4, label, y, wb, y + 34, wa, 230 + wa + 16, y + 24, after)
    )


def s3():
    return "v3", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:980px;font-size:88px">Kata tertentu<br>tiba-tiba <span class="stamp">melonjak</span></div>
<div class="abs b" style="left:0;top:330px;width:860px;font-size:29px;font-weight:500">Peneliti UCL mengecek jutaan artikel ilmiah. Beberapa kata mendadak jadi jauh lebih sering dipakai persis di tahun ChatGPT populer.</div>
<div class="abs card" style="left:12px;top:530px;width:900px;height:360px;transform:rotate(1deg)">
  <div class="b" style="position:absolute;left:30px;top:20px;font-size:22px;font-weight:800;letter-spacing:.5px">KENAIKAN PEMAKAIAN KATA, 2022 KE 2023</div>
  %s%s%s
</div>
<div class="pill" style="left:6px;top:940px;transform:rotate(-2deg)">studi bahasa Inggris, ilustrasi pola yang sama</div>
""" % (
        bar("intricate", 30, 117, 90),
        bar("meticulously", 20, 137, 175),
        bar("commendable", 25, 83, 260),
    ) + ARROW


def s4():
    return "v2", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:980px;font-size:100px">Sistem kampus<br>makin <span class="pillk">tajam</span></div>
<div class="abs d blue" style="left:0;top:400px;font-size:200px;line-height:1">14,8%</div>
<div class="abs b" style="left:0;top:610px;width:820px;font-size:30px;font-weight:500">Menurut Turnitin, di periode Oktober 2025 sampai Februari 2026, segini persen esai yang diperiksa isinya lebih dari 80% tulisan AI. Naik dari cuma 3,3% waktu alat ini baru rilis pertengahan 2023.</div>
<div class="abs b" style="left:0;top:900px;width:820px;font-size:24px;font-weight:600">Alat deteksi tidak sempurna, tapi makin sering dipakai kampus.</div>
""" + ARROW


def s5():
    return "v1", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:6px;top:96px;width:940px;font-size:104px">kalau <span class="marker">ketahuan</span>,<br>bukan cuma malu</div>
<div class="abs card" style="left:12px;top:470px;width:900px;height:440px;transform:rotate(-1deg)">
  <div class="abs" style="left:36px;top:36px;width:820px">
    <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:30px"><div class="d blue" style="font-size:40px;line-height:1">•</div><div class="b" style="font-size:30px;font-weight:600;line-height:1.3">Diminta revisi ulang, tenggat makin mepet</div></div>
    <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:30px"><div class="d blue" style="font-size:40px;line-height:1">•</div><div class="b" style="font-size:30px;font-weight:600;line-height:1.3">Dipanggil buat menjelaskan ke dosen</div></div>
    <div style="display:flex;gap:16px;align-items:flex-start"><div class="d blue" style="font-size:40px;line-height:1">•</div><div class="b" style="font-size:30px;font-weight:600;line-height:1.3">Nilai ditahan sampai masalahnya jelas</div></div>
  </div>
</div>
<div class="pill" style="left:6px;top:960px;transform:rotate(-2deg)">konsekuensi beda-beda tiap kampus</div>
""" + ARROW


def s6():
    row = lambda n, t: (
        '<div style="display:flex;align-items:flex-start;gap:22px;margin-bottom:32px">'
        '<div class="d blue" style="font-size:88px;width:66px;line-height:.9">%s</div>'
        '<div class="b" style="font-size:31px;font-weight:700;line-height:1.25">%s</div></div>' % (n, t)
    )
    return "v6", V6 + """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:14px;top:96px;width:960px;font-size:100px">3 cara bikin<br>bunyinya <span class="hl">manusia</span></div>
<div class="abs card" style="left:12px;top:460px;width:900px;height:520px;transform:rotate(1deg)">
  <div class="abs" style="left:40px;top:44px;width:820px">
    %s%s%s
  </div>
</div>
""" % (
        row("1", "Ganti kalimat pembuka yang umum jadi fakta atau angka spesifik"),
        row("2", "Selipkan contoh dari kasus nyata, bukan cuma teori"),
        row("3", "Baca ulang keras-keras, potong kalimat yang kepanjangan"),
    ) + ARROW


def s7():
    item = lambda t: (
        '<div style="display:flex;gap:16px;align-items:center;margin-bottom:22px">%s'
        '<div class="b" style="font-size:30px;font-weight:700;line-height:1.2">%s</div></div>' % (check(), t)
    )
    return "v5", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:14px;top:96px;width:950px;font-size:76px">Males benerin sendiri? %s aja.</div>
<div class="abs card" style="left:12px;top:400px;width:900px;height:380px;transform:rotate(-1deg)">
  <div class="b blue" style="position:absolute;left:34px;top:26px;font-size:24px;font-weight:800;letter-spacing:1px">KONSULTAN TUGAS BANTU</div>
  <div class="abs" style="left:34px;top:84px;width:820px">
    %s%s%s
  </div>
</div>
<div class="abs b" style="left:0;top:830px;width:800px;font-size:29px;font-weight:600">Makalahmu jadi enak dibaca dosen, bukan cuma lolos cek AI.</div>
""" % (
        hl("serahin"),
        item("Bahasanya dirapikan biar terdengar natural"),
        item("Struktur dan alur tulisan disusun ulang"),
        item("Referensi jurnal dicek, bukan asal tempel"),
    ) + ARROW


def s8():
    return "v4", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:14px;top:80px;width:960px;font-size:80px">Scan buat<br>chat %s</div>
<div class="abs card" style="left:340px;top:360px;width:400px;height:400px;transform:rotate(-1deg);display:flex;align-items:center;justify-content:center">
  %s
</div>
<div class="abs d blue" style="left:0;top:790px;width:1080px;text-align:center;font-size:52px;letter-spacing:0">%s</div>
<div class="abs b" style="left:110px;top:870px;width:760px;text-align:center;font-size:28px;font-weight:600">Ceritakan makalahmu dan tenggatnya.</div>
<div class="abs" style="left:190px;top:960px;width:700px;height:88px;border-radius:999px;background:#0A0A0A;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:8px 8px 0 #1F3BFF"><span class="d" style="font-size:42px;letter-spacing:0">follow @konsultantugas</span></div>
""" % (hl("WhatsApp"), qr_svg(360), WA_DISPLAY)


SLIDES = [s1, s2, s3, s4, s5, s6, s7, s8]

if __name__ == "__main__":
    run(SLIDES, HERE, extra_faces=EXTRA)
