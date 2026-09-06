#!/usr/bin/env python3
"""Sharing cards for the terminal-trust-spectrum note, one per language.

Same canvas, gradient, watermark, fonts and fit-by-measurement as the landing
cards — the layout constants and helpers are imported from og_cards.py rather
than re-derived. Only the text and the destination differ: the headline is the
note's argument compressed to two lines, and the domain line carries the
per-language notes path so a timeline reader knows it is an article.

    python3 scripts/og_note_cards.py
"""
import pathlib
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import og_cards as base

ROOT = base.ROOT

# One entry per note: slug + per-language (two headline lines, subline). Line
# lengths are fitted at draw time; keep headlines to ~2 short lines.
NOTES = [
    ("shareable-state-for-stateless-agents", {
        "en": (["Durable · Shared · Portable", "Shareable state for stateless agents"],
               "Sandboxes are disposable; data should outlive any one session."),
        "zh": (["持久、共享、可攜", "stateless agent 的可共享狀態，我們怎麼設計"],
               "沙箱用完即棄，資料該活得比任何單一 session 更久。"),
        "ja": (["持続・共有・可搬", "ステートレスなエージェントの共有可能な状態"],
               "サンドボックスは使い捨てでも、データはセッションより長生きすべきだ。"),
        "ko": (["지속 · 공유 · 이동", "스테이트리스 에이전트의 공유 가능한 상태"],
               "샌드박스는 일회용이어도, 데이터는 세션보다 오래 살아남아야 한다."),
    }),
    ("terminal-trust-spectrum", {
        "en": (["Herdr · Superlogical · OpenAB Connect", "Three bets on terminal trust"],
               "Where should a session live, and how far should it be trusted?"),
        "zh": (["Herdr、Superlogical、OpenAB Connect", "終端信任光譜的三個賭注"],
               "Session 該住在哪裡，又該被信任到什麼程度？"),
        "ja": (["Herdr・Superlogical・OpenAB Connect", "ターミナル信頼スペクトラム、三つの賭け"],
               "セッションはどこに住み、どこまで信頼されるべきか"),
        "ko": (["Herdr · Superlogical · OpenAB Connect", "터미널 신뢰 스펙트럼의 세 가지 베팅"],
               "세션은 어디에 살고, 어디까지 신뢰해야 하는가"),
    }),
]

DOMAIN = {
    "en": "connect.openab.dev/notes",
    "zh": "connect.openab.dev/zh/notes",
    "ja": "connect.openab.dev/ja/notes",
    "ko": "connect.openab.dev/ko/notes",
}


def build(lang, text, dest_dir):
    im = base.gradient()
    icon = Image.open(ROOT / "icon.png").convert("RGBA")

    wm = Image.open(base.WATERMARK).convert("RGBA")
    wm_h = 520
    wm = wm.resize((round(wm.width * wm_h / wm.height), wm_h), Image.LANCZOS)
    wm.putalpha(wm.split()[3].point(lambda a: int(a * 0.16)))
    im.paste(wm, (base.W - wm.width + 150, (base.H - wm_h) // 2), wm)

    d = ImageDraw.Draw(im)
    mark = icon.resize((base.ICON_PX, base.ICON_PX), Image.LANCZOS)
    im.paste(mark, base.ICON_XY, mark)

    wf = base.font(base.LATIN, 31, bold=True)
    wy = (base.ICON_XY[1] + base.ICON_PX // 2
          - d.textbbox((0, 0), base.WORDMARK, font=wf)[3] // 2 - 3)
    d.text((base.ICON_XY[0] + base.ICON_PX + 18, wy), base.WORDMARK,
           font=wf, fill=base.INK)

    lines, sub = text
    hpath = base.HEAD_FACE.get(lang, base.FACE[lang])
    # The product-name line is long, so start lower than the landing cards and
    # let fit() take it down until it clears the watermark boundary.
    hf, hsize = base.fit(d, lines, hpath, 48, 30, base.TEXT_R)
    d.text((base.MARGIN, base.HEAD_Y1), lines[0], font=hf, fill=base.INK)
    d.text((base.MARGIN, base.HEAD_Y2 if hsize > 44 else base.HEAD_Y1 + hsize + 22),
           lines[1], font=hf, fill=base.INK)

    sf_size = 27 if lang == "en" else 25
    sf = base.font(base.FACE[lang], sf_size)
    while base.MARGIN + base.width(d, sub, sf) > base.TEXT_R and sf_size > 17:
        sf_size -= 1
        sf = base.font(base.FACE[lang], sf_size)
    d.text((base.MARGIN, base.SUB_Y), sub, font=sf, fill=base.MUTED)
    d.text((base.MARGIN, base.DOMAIN_Y), DOMAIN[lang],
           font=base.font(base.MONO, 26), fill=base.ACCENT)

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"og-{lang}.png"
    im.save(dest, optimize=True)

    # Measure each line with the font it is drawn in — a check that can disagree
    # with the code it checks proves nothing.
    over = [l for l in lines if base.MARGIN + base.width(d, l, hf) > base.TEXT_R]
    if base.MARGIN + base.width(d, sub, sf) > base.TEXT_R:
        over.append(sub)
    return dest, hsize, sf_size, "/".join(hf.getname()), over


if __name__ == "__main__":
    base.derive_watermark()
    for slug, text_by_lang in NOTES:
      for lang in ("en", "zh", "ja", "ko"):
        dest, hs, ss, name, over = build(lang, text_by_lang[lang], ROOT / "notes" / slug)
        im = Image.open(dest)
        print(f"  {lang:3} {dest.relative_to(ROOT)}  {im.size[0]}x{im.size[1]} "
              f"{im.mode:4} head={hs}px sub={ss}px  {name}"
              + ("  OVERFLOW: %s" % over if over else ""))
