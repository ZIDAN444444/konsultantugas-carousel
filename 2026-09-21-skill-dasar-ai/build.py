#!/usr/bin/env python3
# Carousel @konsultantugas: skill dasar dan kreativitas mahasiswa di era AI (2026-09-21)
# 5 slide. Font cover baru: Syne + Manrope. Dirender otomatis oleh GitHub Actions.
import os, sys, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import *  # noqa

EXTRA = [("Syne", "syne", [700, 800]), ("Manrope", "manrope", [400, 500, 700])]


def s1():
    return "v5", """
<div class="brand">@konsultantugas</div>
<div class="abs card" style="left:20px;top:64px;width:900px;height:470px;transform:rotate(-1deg)">
  <div class="b" style="position:absolute;left:28px;top:22px;font-size:23px;font-weight:700;letter-spacing:.5px">NILAI DIBANDING SISWA TANPA AI</div>
  <div class="pill" style="right:24px;top:18px;font-size:20px;padding:3px 14px">studi siswa SMA</div>
  <div class="abs" style="left:300px;top:84px;width:0;height:350px;border-left:4px solid #0A0A0A"></div>
  <div class="b" style="position:absolute;left:28px;top:104px;font-size:26px;font-weight:700">Saat latihan, boleh pakai GPT-4</div>
  <div class="abs" style="left:304px;top:150px;width:250px;height:76px;background:#1F3BFF;border:4px solid #0A0A0A;box-shadow:6px 6px 0 #0A0A0A"></div>
  <div class="d blue" style="position:absolute;left:576px;top:156px;font-size:56px">+48%%</div>
  <div class="b" style="position:absolute;left:28px;top:270px;font-size:26px;font-weight:700">Saat ujian, tanpa AI</div>
  <div class="abs" style="left:212px;top:316px;width:88px;height:76px;background:#0A0A0A;border:4px solid #0A0A0A;box-shadow:6px 6px 0 #1F3BFF"></div>
  <div class="d" style="position:absolute;left:24px;top:322px;width:176px;text-align:right;font-size:56px">-17%%</div>
</div>
<div class="abs d" style="left:14px;top:575px;width:960px;font-size:78px">Dibantu AI, nilai naik. Tanpa AI, %s.</div>
<div class="abs b" style="left:0;top:945px;width:700px;font-size:30px;font-weight:500">3 temuan riset soal skill dasar dan kreativitas.</div>
""" % hl("malah turun") + ARROW


def s2():
    cells = ""
    for r in range(2):
        for c in range(5):
            idx = r * 5 + c
            bg = "#1F3BFF" if idx < 2 else "#fff"
            cells += '<div class="abs" style="left:%dpx;top:%dpx;width:56px;height:56px;background:%s;border:4px solid #0A0A0A"></div>' % (
                30 + c * 70, 90 + r * 70, bg)
    return "v1", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:6px;top:96px;width:940px;font-size:104px">jago tiktok,<br>belum tentu<br>jago <span class="marker">word</span></div>
<div class="abs b" style="left:6px;top:470px;width:460px;font-size:28px;font-weight:500">Survei 2021 di kampus 4 tahun AS: 20%% mahasiswa kesulitan belajar alat edtech baru.<br><br>Beberapa dosen bilang mahasiswa bingung pakai Word dan Excel. Itu cerita dosen, bukan ukuran nasional.</div>
<div class="abs card" style="left:516px;top:460px;width:420px;height:440px;transform:rotate(1.5deg)">
  <div class="b" style="position:absolute;left:30px;top:24px;font-size:26px;font-weight:800;letter-spacing:1px">2 DARI 10 MAHASISWA</div>
  %s
  <div class="b" style="position:absolute;left:30px;top:246px;width:340px;font-size:26px;font-weight:600;line-height:1.25">kesulitan belajar alat edtech baru</div>
  <div class="abs" style="left:30px;top:340px;width:360px;border-top:4px dashed #0A0A0A"></div>
  <div class="b blue" style="position:absolute;left:30px;top:362px;width:340px;font-size:24px;font-weight:700;line-height:1.25">survei mahasiswa, bukan tes langsung</div>
</div>
<div class="sticker" style="left:600px;top:935px;transform:rotate(-4deg)">cek dulu, jangan panik</div>
""" % cells + ARROW


def s3():
    return "v3", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:980px;font-size:96px">AI jadi %s</div>
<div class="abs b" style="left:0;top:330px;width:500px;font-size:30px;font-weight:500">Hampir 1.000 siswa SMA belajar matematika. Yang pakai GPT&#8209;4 biasa saat latihan malah lebih rendah di ujian tanpa AI.</div>
<div class="abs d blue" style="left:540px;top:300px;font-size:170px;line-height:1">-17%%</div>
<div class="abs b" style="left:548px;top:480px;width:380px;font-size:24px;font-weight:700;line-height:1.25">nilai ujian dibanding siswa yang tidak pakai AI</div>
<div class="abs card" style="left:0;top:610px;width:900px;height:290px">
  <div class="abs" style="left:440px;top:24px;width:0;height:240px;border-left:4px dashed #0A0A0A"></div>
  <div class="b" style="position:absolute;left:28px;top:24px;font-size:24px;font-weight:800;letter-spacing:.5px">AI KASIH JAWABAN</div>
  <div class="d" style="position:absolute;left:28px;top:84px;font-size:86px;line-height:1">-17%%</div>
  <div class="b" style="position:absolute;left:28px;top:176px;width:380px;font-size:26px;font-weight:500">nilai ujian tanpa AI</div>
  <div class="b blue" style="position:absolute;left:472px;top:24px;font-size:24px;font-weight:800;letter-spacing:.5px">AI KASIH PETUNJUK</div>
  <div class="d blue" style="position:absolute;left:472px;top:92px;font-size:50px;line-height:1.05">hampir sama</div>
  <div class="b" style="position:absolute;left:472px;top:176px;width:400px;font-size:26px;font-weight:500">efek buruknya sebagian besar hilang</div>
</div>
<div class="abs b" style="left:0;top:950px;width:800px;font-size:26px;font-weight:600">Ini siswa SMA dan matematika, bukan mahasiswa.</div>
""" % hl("tongkat") + ARROW


def dots(seed, n, cx, cy, spread_x, spread_y, color, r=12):
    rnd = random.Random(seed)
    out = ""
    placed = []
    tries = 0
    while len(placed) < n and tries < 4000:
        tries += 1
        x = cx + rnd.uniform(-spread_x, spread_x)
        y = cy + rnd.uniform(-spread_y, spread_y)
        if all((x - px) ** 2 + (y - py) ** 2 > (2 * r + 6) ** 2 for px, py in placed):
            placed.append((x, y))
    for x, y in placed:
        out += '<div class="abs" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:50%%;background:%s;border:3px solid #0A0A0A"></div>' % (
            x - r, y - r, 2 * r, 2 * r, color)
    return out


def s4():
    left = dots(3, 16, 210, 200, 170, 120, "#fff")
    right = dots(5, 16, 210, 200, 62, 58, "#1F3BFF")
    return "v2", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;width:980px;font-size:124px">Lebih kreatif,<br>tapi makin <span class="stamp">seragam</span></div>
<div class="abs card" style="left:12px;top:400px;width:426px;height:330px;transform:rotate(-1.5deg)">
  <div class="b" style="position:absolute;left:24px;top:16px;font-size:24px;font-weight:800;letter-spacing:.5px">TANPA AI</div>
  %s
</div>
<div class="abs card" style="left:470px;top:420px;width:430px;height:330px;transform:rotate(1.5deg)">
  <div class="b blue" style="position:absolute;left:24px;top:16px;font-size:24px;font-weight:800;letter-spacing:.5px">DIBANTU IDE AI</div>
  %s
</div>
<div class="pill" style="left:370px;top:782px;transform:rotate(-3deg)">ilustrasi</div>
<div class="abs b" style="left:0;top:850px;width:820px;font-size:28px;font-weight:600">Eksperimen 293 penulis dewasa di Inggris, bukan mahasiswa: cerita dengan ide dari AI dinilai 6,7%% lebih baru. Tapi cerita-cerita itu lebih mirip satu sama lain.</div>
""" % (left, right) + ARROW


def s5():
    row = lambda n, t: (
        '<div style="display:flex;align-items:center;gap:22px;margin-bottom:26px">'
        '<div class="d blue" style="font-size:84px;width:64px;line-height:1">%s</div>'
        '<div class="b" style="font-size:34px;font-weight:700;line-height:1.15">%s</div></div>' % (n, t)
    )
    return "v1", """
<div class="brand">@konsultantugas</div>
<div class="abs d" style="left:0;top:96px;font-size:118px">coba sendiri <span class="marker">dulu</span></div>
<div class="abs card" style="left:12px;top:340px;width:870px;height:390px;transform:rotate(-1.2deg)">
  <div class="abs" style="left:40px;top:44px;width:800px">
    %s%s%s
  </div>
</div>
<div class="sticker" style="left:600px;top:712px;transform:rotate(-4deg)">riset, bukan vonis</div>
<div class="abs b" style="left:0;top:810px;width:860px;font-size:32px;font-weight:600">Simpan biar tidak lupa. Kirim ke temanmu yang tugasnya selalu dikerjain AI.</div>
<div class="abs" style="left:0;top:960px;width:640px;height:92px;border-radius:999px;background:#0A0A0A;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:8px 8px 0 #1F3BFF"><span class="d" style="font-size:48px;letter-spacing:0">follow @konsultantugas</span></div>
""" % (
        row("1", "Kerjakan dulu, baru tanya AI"),
        row("2", "Minta petunjuk, bukan jawaban"),
        row("3", "Tulis draf awalmu sendiri"),
    )


SLIDES = [s1, s2, s3, s4, s5]

if __name__ == "__main__":
    run(SLIDES, HERE, extra_faces=EXTRA)
