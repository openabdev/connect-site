#!/usr/bin/env python3
"""Shared page chrome for connect.openab.dev.

The head tags, nav and footer live here once. They were inlined in build.py while the
landing pages were the only pages; privacy and support would have meant a second copy,
and a second copy of a nav is a nav that will disagree with itself within a month.
"""
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://connect.openab.dev"
ORDER = ["zh", "ja", "ko", "en"]

# Per-language chrome only. Page content lives with the generator that owns the page.
CHROME = {
    "en": dict(dir="", base="/", htmllang="en", label="EN", og_locale="en_US",
               nav=("Features", "FAQ", "Support"), onemin="1-min tutorials", notes="Dev notes", releases="Releases",
               foot=("Privacy", "Support", "Runtime source")),
    "zh": dict(dir="zh", base="/zh/", htmllang="zh-Hant", label="中文", og_locale="zh_TW",
               nav=("特色", "常見問題", "支援"), onemin="一分鐘看懂", notes="開發筆記", releases="版本紀錄",
               foot=("隱私", "支援", "runtime 原始碼")),
    "ja": dict(dir="ja", base="/ja/", htmllang="ja", label="日本語", og_locale="ja_JP",
               nav=("特徴", "よくある質問", "サポート"), onemin="1分で分かる", notes="開発ノート", releases="リリース",
               foot=("プライバシー", "サポート", "ランタイムのソース")),
    "ko": dict(dir="ko", base="/ko/", htmllang="ko", label="한국어", og_locale="ko_KR",
               nav=("특징", "자주 묻는 질문", "지원"), onemin="1분 만에 보기", notes="개발 노트", releases="릴리스",
               foot=("개인정보", "지원", "런타임 소스")),
}
PTY = "https://github.com/openabdev/openab-pty"

# Runs in <head> so the redirect happens before the page paints. Only `/` is redirected.
# A language picked with the switcher is stored and then never overridden, so the
# English link (which is `/`) keeps working for someone who once chose Chinese.
LANG_SCRIPT = """<script>
// Browser language on the root page. navigator.languages is read in order; the first entry
// that is zh-Hant (script Hant, or region TW/HK/MO), ja, ko or en decides. Other entries
// (zh-Hans, zh-CN, fr, …) are skipped, so with none matching the page stays English.
// A language picked with the switcher is stored in localStorage and never overridden.
(function () {
  var KEY = "oab-lang";
  var PAGES = { en: "/", zh: "/zh/", ja: "/ja/", ko: "/ko/" };
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function pick(tag) {
    var p = String(tag).toLowerCase().split("-");
    if (p[0] === "en" || p[0] === "ja" || p[0] === "ko") return p[0];
    if (p[0] !== "zh" || p.indexOf("hans") >= 0) return null;
    var zhHant = p.some(function (s) { return s === "hant" || s === "tw" || s === "hk" || s === "mo"; });
    return zhHant ? "zh" : null;
  }
  if (location.pathname === "/" && !stored()) {
    var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
    var lang = null;
    for (var i = 0; i < langs.length && !lang; i++) lang = pick(langs[i]);
    if (lang && lang !== "en") location.replace(PAGES[lang] + location.search + location.hash);
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".lang a");
    if (!a) return;
    var code = (a.getAttribute("href") || "").split("/")[1] || "en";
    if (!PAGES[code]) return;
    try { localStorage.setItem(KEY, code); } catch (err) { /* storage unavailable: nothing to remember */ }
  });
})();
</script>"""


def rev(name):
    """An asset path with a content hash, so a change is never served stale.

    GitHub Pages sends cache-control: max-age=600. Without this a visitor who loaded the
    page minutes ago keeps the old stylesheet or image, which is indistinguishable from
    the change not having been deployed — and that produced one wrong diagnosis already.
    """
    f = ROOT / name
    h = hashlib.md5(f.read_bytes()).hexdigest()[:8] if f.exists() else "0"
    return f"/{name}?v={h}"


def out_path(code, filename):
    """Where a page for this language lives.

    English stays at the root: Apple has /privacy.html and /support.html on file for this
    app, so those two URLs must not move.
    """
    d = CHROME[code]["dir"]
    return ROOT / d / filename if d else ROOT / filename


def prefix(code):
    """Path prefix for same-language links."""
    return CHROME[code]["base"]


def switcher(current, filename="index.html"):
    """Plain links. A click on one is recorded by LANG_SCRIPT, then the browser follows it.

    `/` is English. The root page may redirect a first-time visitor by browser language
    (see LANG_SCRIPT), but not once a choice has been stored here.
    """
    out = []
    for c in ORDER:
        cls = ' class="active"' if c == current else ""
        target = CHROME[c]["base"] + ("" if filename == "index.html" else filename)
        out.append(f'<a{cls} href="{target}">{CHROME[c]["label"]}</a>')
    return "|".join(out)


def alternates(filename="index.html"):
    suffix = "" if filename == "index.html" else filename
    rows = [f'<link rel="alternate" hreflang="{CHROME[c]["htmllang"]}" '
            f'href="{SITE}{CHROME[c]["base"]}{suffix}">' for c in ORDER]
    # x-default is what a search engine serves when it matches no listed language.
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{suffix}">')
    return "\n".join(rows)


def head(code, filename, title, desc, og_image=None, og_alt=None, og_type="website"):
    d = CHROME[code]
    suffix = "" if filename == "index.html" else filename
    url = f"{SITE}{d['base']}{suffix}"
    tags = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        LANG_SCRIPT,
        f"<title>{title}</title>",
        f'<meta name="description" content="{desc}">',
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:type" content="{og_type}">',
        '<meta property="og:site_name" content="OpenAB Connect">',
        f'<meta property="og:locale" content="{d["og_locale"]}">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{url}">',
    ]
    if og_image:
        tags += [
            f'<meta property="og:image" content="{og_image}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{og_alt or title}">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{title}">',
            f'<meta name="twitter:description" content="{desc}">',
            f'<meta name="twitter:image" content="{og_image}">',
        ]
    tags += [
        f'<link rel="icon" href="{rev("icon.png")}">',
        f'<link rel="apple-touch-icon" href="{rev("icon.png")}">',
        f'<link rel="stylesheet" href="{rev("style.css")}">',
        alternates(filename),
    ]
    return "\n".join(tags)


def nav(code, filename="index.html"):
    d = CHROME[code]
    p = d["base"]
    # On a document page the section anchors belong to the landing page, so they are
    # absolute links back to it rather than fragments that would resolve to nothing.
    home = p if filename == "index.html" else p
    icon = rev("icon.png")
    # The videos exist in en and zh only; ja and ko readers get the English page.
    onemin = f"{p}1min/" if code in ("en", "zh") else "/1min/"
    return f"""<nav>
  <a class="brand" href="{home}"><img src="{icon}" alt="" width="28" height="28">OpenAB Connect</a>
  <div class="links">
    <a href="{p}#features">{d["nav"][0]}</a>
    <a href="{p}#faq">{d["nav"][1]}</a>
    <a href="{onemin}">{d["onemin"]}</a>
    <a href="{p}notes/">{d["notes"]}</a>
    <a href="{p}releases/">{d["releases"]}</a>
    <a href="{p}support.html">{d["nav"][2]}</a>
    <span class="lang">{switcher(code, filename)}</span>
  </div>
</nav>"""


def footer(code):
    d = CHROME[code]
    p = d["base"]
    return f"""<footer>
  <a href="{p}privacy.html">{d["foot"][0]}</a>
  <a href="{p}support.html">{d["foot"][1]}</a>
  <a href="{PTY}">{d["foot"][2]}</a>
  <span class="dim">© 2026 openabdev</span>
</footer>"""
