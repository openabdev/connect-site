#!/usr/bin/env python3
"""One-minute explainer videos ("1min"), English and Traditional Chinese.

    python3 scripts/build_1min.py

English lives at /1min/<slug>/, Chinese at /zh/1min/<slug>/, matching how notes
are laid out. Only en and zh exist for these, so the language switcher and the
hreflang alternates list just those two instead of chrome's four (ja/ko would 404).

The media sit next to the English page, one folder per video:
  1min/<slug>/video-{en,zh}.mp4   final render, burned-in subtitles, cover as first frame
  1min/<slug>/cover-{en,zh}.jpg   vertical poster shown before playback
  1min/<slug>/og-{en,zh}.jpg      1200x630 share card
GitHub Pages honours Range requests, so a plain <video> streams and seeks fine.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chrome

ROOT = chrome.ROOT
SITE = chrome.SITE
LANGS = ["zh", "en"]

INDEX = {
    "en": dict(title="1-minute explainers — OpenAB Connect",
               h1="1-minute explainers",
               lede="Short vertical videos, one idea each."),
    "zh": dict(title="1 分鐘看懂 — OpenAB Connect",
               h1="1 分鐘看懂",
               lede="直式短影片，一支只講一件事。"),
}

VIDEOS = [
    dict(
        slug="openab-acp-vs-pty",
        date_iso="2026-10-01",
        en=dict(
            date="October 1, 2026",
            title="ACP or PTY? Results, or control? — OpenAB in 1 minute",
            h1="ACP or PTY? Results, or control?",
            desc="OpenAB has two modes. ACP brokers any ACP coding CLI to Discord, Slack, "
                 "Telegram, Feishu and LINE and hands you the result. PTY attaches the "
                 "agent's terminal to OpenAB Connect so you see and steer every step.",
            og_alt="ACP or PTY? Results, or control?",
            label="Play the video",
            points=[
                ("ACP", "Classic mode. Any coding CLI that speaks the Agent Communication "
                        "Protocol talks to OpenAB, which brokers it to Discord, Slack, Telegram, "
                        "Feishu and LINE. You get the result in your team channel."),
                ("PTY", "New mode. The agent's terminal attaches to OpenAB Connect on your Mac. "
                        "Install, configure, even talk to it by voice, and watch every step. "
                        "The cost: it can be a lot of information."),
                ("PTY ecosystem", "OpenAB PTY is a runtime: OpenAB Connect (Mac), OpenAB Remote "
                                  "(iOS) and instance MCP as its hands. Only PTY mode has this."),
            ],
            download="Download MP4",
            back="All 1-minute explainers",
        ),
        zh=dict(
            date="2026 年 10 月 1 日",
            title="ACP 還是 PTY？要結果，還是要掌控｜OpenAB 1 分鐘看懂",
            h1="ACP 還是 PTY？要結果，還是要掌控",
            desc="OpenAB 有兩種模式：ACP 把任何支援 ACP 的 coding CLI 串到 Discord、Slack、"
                 "Telegram、飛書、LINE，只給你結果；PTY 把 Agent 的終端機直接掛到 OpenAB "
                 "Connect，全程可見、完整掌控。",
            og_alt="ACP 還是 PTY？要結果，還是要掌控",
            label="播放影片",
            points=[
                ("ACP", "經典模式。支援 Agent Communication Protocol 的 coding CLI 都能和 "
                        "OpenAB 溝通，由 OpenAB 當 broker 串到 Discord、Slack、Telegram、飛書、"
                        "LINE，結果直接貼在團隊頻道。"),
                ("PTY", "新模式。Agent 的終端機直接掛到你 Mac 上的 OpenAB Connect，可以遠端安裝、"
                        "配置，甚至用語音對話，每一步都看得到。代價是資訊可能太多。"),
                ("PTY 生態", "OpenAB PTY 是一個 runtime，延伸出 OpenAB Connect（Mac）、"
                             "OpenAB Remote（iOS），再加上當手腳的 instance MCP。只有 PTY 模式才有。"),
            ],
            download="下載 MP4",
            back="所有 1 分鐘影片",
        ),
    ),
    dict(
        slug="lending-your-computer-to-an-agent",
        date_iso="2026-10-01",
        en=dict(
            date="October 1, 2026",
            title="Your agent, your computer: access is your call — OpenAB Connect in 1 minute",
            h1="Your agent, your computer. Access is your call.",
            desc="Agents are splitting from the computers they act on. When an agent borrows your "
                 "Mac, OpenAB Connect gives it one of three profiles: observe looks only, desktop "
                 "controls the desktop (which is a shell), owner gets every tool.",
            og_alt="Your agent, your computer. Access is your call.",
            label="Play the video",
            points=[
                ("observe", "Look only: screenshots and system info, 2 tools. Not a shell. The default, "
                            "and enough for “tell me what's wrong here”."),
                ("desktop", "Control the desktop: fill in forms, run a build, 20 tools. Controlling the "
                            "desktop is a shell, so lend it a dedicated computer."),
                ("owner", "Every tool, including the shell, 42 tools. Keep it for your own CLI."),
            ],
            note=("Read the full dev note", "/notes/lending-your-computer-to-an-agent/"),
            download="Download MP4",
            back="All 1-minute explainers",
        ),
        zh=dict(
            date="2026 年 10 月 1 日",
            title="Agent 和電腦分開，權限由你決定｜OpenAB Connect 1 分鐘看懂",
            h1="Agent 和電腦分開，權限由你決定",
            desc="Agent 和它動手的電腦正在分開。Agent 跟你借 Mac 時，OpenAB Connect 給它三種 "
                 "profile 之一：observe 只給看、desktop 操作桌面（等同 shell）、owner 全部工具。",
            og_alt="Agent 和電腦分開，權限由你決定",
            label="播放影片",
            points=[
                ("observe", "只給看：截圖和系統資訊，共 2 個工具，不等同 shell。預設值，"
                            "「幫我看一下哪裡出錯」這樣就夠了。"),
                ("desktop", "操作桌面：能填表、跑 build，共 20 個工具。能操作桌面就等於有 shell，"
                            "請借它一台專用的電腦。"),
                ("owner", "全部工具，包括 shell，共 42 個工具。留給你自己的 CLI。"),
            ],
            note=("閱讀完整開發筆記", "/zh/notes/lending-your-computer-to-an-agent/"),
            download="下載 MP4",
            back="所有 1 分鐘影片",
        ),
    ),
]

STYLE = """<style>
.onemin{max-width:760px}
.onemin .when{color:var(--muted);font-size:.95rem;margin:.25rem 0 1.5rem}
.iphone{position:relative;width:min(380px,88vw,calc((100svh - 160px) * 9 / 19.5));aspect-ratio:9/19.5;margin:1rem auto 0;padding:12px;border-radius:60px;
  background:linear-gradient(145deg,#5b5f66 0%,#2b2e33 18%,#1a1c20 50%,#33363c 82%,#6a6e75 100%);
  box-shadow:0 0 0 2px #0d0e10,0 0 0 3px #45484e,0 40px 90px rgba(0,0,0,.45)}
.iphone::before{content:"";position:absolute;inset:5px;border-radius:55px;border:1px solid rgba(255,255,255,.12);pointer-events:none}
.iphone .hw{position:absolute;width:4px;border-radius:2px;background:linear-gradient(90deg,#2a2c30,#55585e)}
.iphone .act{left:-4px;top:16%;height:4%}.iphone .vu{left:-4px;top:24%;height:8%}.iphone .vd{left:-4px;top:34%;height:8%}
.iphone .pw{right:-4px;top:27%;height:12%;background:linear-gradient(270deg,#2a2c30,#55585e)}
.iphone .screen{position:relative;width:100%;height:100%;border-radius:48px;overflow:hidden;background:#000;display:flex;flex-direction:column;justify-content:center}
.iphone .status{position:absolute;top:0;left:0;right:0;height:8.5%;display:flex;align-items:center;justify-content:space-between;padding:0 9% 0 11%;
  color:#fff;font:600 15px/1 -apple-system,"SF Pro Text",sans-serif;z-index:2;pointer-events:none}
.iphone .island{position:absolute;left:50%;top:22%;transform:translateX(-50%);width:32%;height:44%;border-radius:999px;background:#000}
.iphone .icons{display:flex;gap:5px;align-items:center}
.iphone video{display:block;width:100%;aspect-ratio:9/16;background:#000}
.iphone .home{position:absolute;bottom:1.6%;left:50%;transform:translateX(-50%);width:36%;height:5px;border-radius:3px;background:rgba(255,255,255,.85);z-index:2;pointer-events:none}
.onemin .dl{text-align:center;margin:1.25rem 0 2rem}
.onemin .points{display:grid;gap:1rem;margin:0 0 2rem}
.onemin .points div{padding:1rem 1.25rem;border-radius:14px;border:1px solid rgba(127,127,127,.25)}
.onemin .points b{display:block;margin-bottom:.35rem}
.onemin-index .vid{display:flex;gap:1rem;align-items:center}
.onemin-index .vid img{width:96px;border-radius:10px;flex:none}
</style>"""

ICONS = ('<span class="icons" aria-hidden="true">'
         '<svg width="18" height="12" viewBox="0 0 18 12" fill="#fff"><rect y="8" width="3" height="4" rx="1"/>'
         '<rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/>'
         '<rect x="15" width="3" height="12" rx="1"/></svg>'
         '<svg width="27" height="13" viewBox="0 0 27 13" fill="none"><rect x=".5" y=".5" width="23" height="12" rx="3.5" '
         'stroke="#fff" opacity=".5"/><rect x="2" y="2" width="20" height="9" rx="2" fill="#fff"/></svg></span>')


def two_lang(html, code, filename):
    """chrome emits four languages; these pages exist in two."""
    keep = []
    for line in html.splitlines():
        if 'hreflang="ja"' in line or 'hreflang="ko"' in line:
            continue
        keep.append(line)
    html = "\n".join(keep)
    links = []
    for c in LANGS:
        cls = ' class="active"' if c == code else ""
        links.append(f'<a{cls} href="{chrome.CHROME[c]["base"]}{filename}">{chrome.CHROME[c]["label"]}</a>')
    start = html.find('<span class="lang">')
    if start != -1:
        end = html.find("</span>", start)
        html = html[:start] + '<span class="lang">' + "|".join(links) + html[end:]
    return html


def page(code, filename, title, desc, body, og_image=None, og_alt=None, og_type="website"):
    d = chrome.CHROME[code]
    head = chrome.head(code, filename, title, desc, og_image, og_alt, og_type)
    html = f"""<!DOCTYPE html>
<html lang="{d['htmllang']}" data-lang="{code}">
<head>
{head}
{STYLE}
</head>
<body>

{chrome.nav(code, filename)}

{body}

{chrome.footer(code)}
</body>
</html>
"""
    return two_lang(html, code, filename)


def video_page(v, code):
    t = v[code]
    slug = v["slug"]
    filename = f"1min/{slug}/"
    media = f"1min/{slug}"
    video = chrome.rev(f"{media}/video-{code}.mp4")
    cover = chrome.rev(f"{media}/cover-{code}.jpg")
    og = SITE + chrome.rev(f"{media}/og-{code}.jpg")
    points = "\n".join(f"  <div><b>{k}</b>{p}</div>" for k, p in t["points"])
    note = f'<p><a href="{t["note"][1]}">{t["note"][0]} →</a></p>\n' if t.get("note") else ""
    body = f"""<main class="wrap onemin">
<h1>{t['h1']}</h1>
<div class="when"><time datetime="{v['date_iso']}">{t['date']}</time></div>
<div class="iphone" role="region" aria-label="{t['label']}">
  <i class="hw act"></i><i class="hw vu"></i><i class="hw vd"></i><i class="hw pw"></i>
  <div class="screen">
    <div class="status"><span>9:41</span><span class="island"></span>{ICONS}</div>
    <video src="{video}" poster="{cover}" controls playsinline preload="metadata" aria-label="{t['label']}"></video>
    <div class="home"></div>
  </div>
</div>
<p class="dl"><a href="{video}" download>{t['download']}</a></p>
<div class="points">
{points}
</div>
{note}<p><a href="{chrome.prefix(code)}1min/">← {t['back']}</a></p>
</main>"""
    html = page(code, filename, t["title"], t["desc"], body, og, t["og_alt"], "video.other")
    # og:video lets chat apps that support it play inline; the card still falls back to og:image.
    abs_video = SITE + video
    html = html.replace('<meta name="twitter:card"',
                        f'<meta property="og:video" content="{abs_video}">\n'
                        '<meta property="og:video:type" content="video/mp4">\n'
                        '<meta property="og:video:width" content="1080">\n'
                        '<meta property="og:video:height" content="1920">\n'
                        '<meta name="twitter:card"', 1)
    out = chrome.out_path(code, f"{filename}index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return out


def index_page(code):
    t = INDEX[code]
    rows = []
    for v in VIDEOS:
        x = v[code]
        cover = chrome.rev(f"1min/{v['slug']}/cover-{code}.jpg")
        rows.append(f"""<a class="note-entry vid" href="{chrome.prefix(code)}1min/{v['slug']}/">
  <img src="{cover}" alt="" width="96" height="171" loading="lazy">
  <div><div class="when">{x['date']}</div>
  <div class="ntitle">{x['h1']}</div>
  <p>{x['desc']}</p></div>
</a>""")
    body = f"""<main class="wrap notes-index onemin-index">
<h1>{t['h1']}</h1>
<p class="lede">{t['lede']}</p>
{chr(10).join(rows)}
</main>"""
    og = SITE + chrome.rev(f"1min/og-{code}.png")
    html = page(code, "1min/", t["title"], t["lede"], body, og, t["h1"])
    out = chrome.out_path(code, "1min/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return out


if __name__ == "__main__":
    for code in LANGS:
        for v in VIDEOS:
            print(video_page(v, code).relative_to(ROOT))
        print(index_page(code).relative_to(ROOT))
