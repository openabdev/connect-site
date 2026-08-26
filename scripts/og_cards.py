#!/usr/bin/env python3
"""Sharing cards, one per language: og-<lang>.png at 1200x630.

The layout is measured from deepsrt.com's card rather than eyeballed — margin x=75,
icon 78px at y=63, headline lines at y=255 and y=328, subtitle at y=424, domain at
y=557, and a vertical gradient whose luminance runs from about #1E3A5F to #0B1726.
The hue is ours: the same deep navy and warm peach used by the shipping icon, so the
card is recognisably from this site while keeping the reference's proportions.

Headline size is measured and reduced until the longest line fits, rather than chosen
by eye — a card is only ever seen at final size, so an overflow is invisible until it
is on somebody's timeline.

    python3 scripts/og_cards.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent

W, H = 1200, 630
MARGIN = 75
TEXT_R = 820          # the watermark begins after this; nothing may cross it
ICON_XY, ICON_PX = (75, 63), 78
HEAD_Y1, HEAD_Y2 = 250, 326
SUB_Y, DOMAIN_Y = 424, 557

# Ours, in the reference's luminance range.
GRAD_TOP, GRAD_BOTTOM = (0x20, 0x30, 0x40), (0x08, 0x10, 0x18)
INK = (0xFF, 0xFF, 0xFF)
MUTED = (0xB8, 0xC3, 0xCC)
ACCENT = (0xF8, 0xC0, 0x90)

LATIN = "/System/Library/Fonts/HelveticaNeue.ttc"
MONO = "/System/Library/Fonts/SFNSMono.ttf"
GB = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FACE = {
    "en": LATIN,
    "zh": GB,
    "ja": "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "ko": "/System/Library/Fonts/AppleSDGothicNeo.ttc",
}
# Face index of the bold cut inside each collection, verified on this machine:
# Helvetica Neue/Bold, Hiragino Sans GB/W6, Apple SD Gothic Neo/Bold.
BOLD = {LATIN: 1, GB: 2, "/System/Library/Fonts/AppleSDGothicNeo.ttc": 6}
# ヒラギノ角ゴシック W3 has no bold cut installed, so the Japanese headline borrows
# Hiragino Sans GB W6 — the headline is kana and Latin, where the families agree.
HEAD_FACE = {"ja": GB}

TEXT = {
    "en": (["Agents from every major vendor.", "One client, each sandboxed."],
           "Encrypted and distributed across your own private infrastructure."),
    "zh": (["所有頂尖廠商的 Agent，", "一個客戶端，各自沙箱。"],
           "加密分散運行在你的私有基礎架構"),
    "ja": (["主要ベンダーのエージェントを、", "ひとつのクライアントに。"],
           "暗号化されたまま、自分のプライベート環境に分散"),
    "ko": (["주요 벤더의 모든 에이전트.", "클라이언트 하나, 각자 샌드박스."],
           "암호화된 채로 여러분의 사설 인프라에 분산"),
}
DOMAIN = "connect.openab.dev"
WORDMARK = "OpenAB Connect"


ICON_SOURCE = ROOT / "icon.png"
WATERMARK = ROOT / "assets/watermark.png"


def derive_watermark():
    """Build assets/watermark.png from the app icon, if it is not already there.

    Kept in this file so the method is reproducible rather than a remembered one-off.
    Three things had to be true and only the third attempt got there:

    - Pasting the icon shows its squircle, which at any opacity reads as a rounded box
      rather than a watermark.
    - Colour-keying the squircle away would keep the textured navy background.
      Saturation separates the warm jellyfish from that field without assuming one
      exact background colour.
    - Feathering with a blurred rectangle leaves a Gaussian tail of 2-5 at the border,
      measured as a 3-unit step at the paste seam; clamping the tail did not remove it.
      A linear ramp on distance-from-edge is zero at the border by construction.
    """
    if not ICON_SOURCE.exists():
        raise SystemExit(f"need {ICON_SOURCE} to derive the watermark")
    # Always rebuild: icon.png is versioned content, and a committed watermark
    # must never silently remain from the previous icon family.
    im = Image.open(ICON_SOURCE).convert("RGBA")
    px = im.load()
    w0, h0 = im.size
    xs, ys = [], []
    for x in range(0, w0, 2):
        for y in range(0, h0, 2):
            r, g, b, a = px[x, y]
            if a > 200 and max(r, g, b) - min(r, g, b) > 34:
                xs.append(x)
                ys.append(y)
    pad = 26
    crop = im.crop((max(0, min(xs) - pad), max(0, min(ys) - pad),
                    min(w0, max(xs) + pad), min(h0, max(ys) + pad)))
    w, h = crop.size
    feather = int(min(w, h) * 0.22)
    src, out = crop.split()[3], Image.new("L", (w, h))
    sp, op = src.load(), out.load()
    for x in range(w):
        dx = min(x, w - 1 - x)
        for y in range(h):
            d = min(dx, y, h - 1 - y)
            op[x, y] = sp[x, y] * min(255, d * 255 // feather) // 255
    crop.putalpha(out)
    WATERMARK.parent.mkdir(parents=True, exist_ok=True)
    crop.save(WATERMARK)
    print(f"  derived {WATERMARK.relative_to(ROOT)} {crop.size}, feather {feather}px")


def font(path, size, bold=False):
    idx = BOLD.get(path, 0) if bold else 0
    try:
        return ImageFont.truetype(path, size, index=idx)
    except OSError:
        return ImageFont.truetype(path, size)


def width(draw, text, f):
    return draw.textbbox((0, 0), text, font=f)[2]


def fit(draw, lines, path, start, floor, limit):
    """Largest size at or below `start` where every line fits inside `limit`."""
    for size in range(start, floor - 1, -1):
        f = font(path, size, bold=True)
        if all(MARGIN + width(draw, l, f) <= limit for l in lines):
            return f, size
    return font(path, floor, bold=True), floor


def gradient():
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(round(GRAD_TOP[i] + (GRAD_BOTTOM[i] - GRAD_TOP[i]) * t)
                          for i in range(3)))
    return im


def build(lang):
    im = gradient()
    icon = Image.open(ROOT / "icon.png").convert("RGBA")

    # Watermark first, so text sits over it rather than under. It is a pre-feathered
    # crop of the jellyfish (assets/watermark.png), not the app icon: pasting the icon
    # showed its squircle, and at any alpha that reads as a rounded box instead of a
    # watermark. The asset is cropped to the saturated peach region and its edges
    # are feathered, which removes the dark squircle boundary regardless of what
    # the artwork does.
    wm = Image.open(WATERMARK).convert("RGBA")
    wm_h = 520
    wm = wm.resize((round(wm.width * wm_h / wm.height), wm_h), Image.LANCZOS)
    wm.putalpha(wm.split()[3].point(lambda a: int(a * 0.16)))
    im.paste(wm, (W - wm.width + 150, (H - wm_h) // 2), wm)

    d = ImageDraw.Draw(im)
    mark = icon.resize((ICON_PX, ICON_PX), Image.LANCZOS)
    im.paste(mark, ICON_XY, mark)

    # The wordmark is optically centred on the icon, not on its line box.
    wf = font(LATIN, 31, bold=True)
    wy = ICON_XY[1] + ICON_PX // 2 - d.textbbox((0, 0), WORDMARK, font=wf)[3] // 2 - 3
    d.text((ICON_XY[0] + ICON_PX + 18, wy), WORDMARK, font=wf, fill=INK)

    lines, sub = TEXT[lang]
    hpath = HEAD_FACE.get(lang, FACE[lang])
    hf, hsize = fit(d, lines, hpath, 54 if lang == "en" else 52, 34, TEXT_R)
    d.text((MARGIN, HEAD_Y1), lines[0], font=hf, fill=INK)
    d.text((MARGIN, HEAD_Y2 if hsize > 44 else HEAD_Y1 + hsize + 22),
           lines[1], font=hf, fill=INK)

    sf_size = 27 if lang == "en" else 25
    sf = font(FACE[lang], sf_size)
    while MARGIN + width(d, sub, sf) > TEXT_R and sf_size > 17:
        sf_size -= 1
        sf = font(FACE[lang], sf_size)
    d.text((MARGIN, SUB_Y), sub, font=sf, fill=MUTED)
    d.text((MARGIN, DOMAIN_Y), DOMAIN, font=font(MONO, 26), fill=ACCENT)

    dest = ROOT / f"og-{lang}.png"
    im.save(dest, optimize=True)

    # Measure each line with the font it is actually drawn in. Measuring the
    # subtitle with the headline font reported an overflow that was not there, and a
    # check that can disagree with the code proves nothing.
    over = [l for l in lines if MARGIN + width(d, l, hf) > TEXT_R]
    if MARGIN + width(d, sub, sf) > TEXT_R:
        over.append(sub)
    return dest, hsize, sf_size, "/".join(hf.getname()), over


if __name__ == "__main__":
    derive_watermark()
    for lang in ("en", "zh", "ja", "ko"):
        dest, hs, ss, name, over = build(lang)
        im = Image.open(dest)
        print(f"  {lang:3} {dest.name:10} {im.size[0]}x{im.size[1]} {im.mode:4} "
              f"head={hs}px sub={ss}px  {name}"
              + ("  OVERFLOW: %s" % over if over else ""))
