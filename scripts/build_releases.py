#!/usr/bin/env python3
"""Release history, four languages.

    python3 scripts/build_releases.py

Same shape as build_notes.py: structure lives here once, languages are data.
English lives at /releases/, the others at /zh/releases/ etc. A version that is
submitted but not yet approved is listed at the top with a "in review" badge —
the page exists to answer "what changed and what is coming", and hiding the
queued version would answer only half.

Dates are the App Store's own (iTunes lookup releaseDate/currentVersionReleaseDate),
not our submission times. The in-review entry carries its submission date and
must be re-labelled when Apple approves it.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chrome

ROOT = chrome.ROOT
APP_STORE = "https://apps.apple.com/app/openab-connect/id6803728097?mt=12"

# Newest first. status: "review" | "latest" | ""
RELEASES = [
 dict(v="1.1.0", status="review", date=dict(
   en="Submitted August 30, 2026", zh="2026 年 8 月 30 日送審",
   ja="2026 年 8 月 30 日申請", ko="2026년 8월 30일 심사 제출"),
  body=dict(
   en="<ul>"
      "<li>Links in terminal output are clickable: hold Command to highlight a "
      "URL, Command-click to open it in your browser. Only http/https links "
      "open; everything else is refused for safety.</li>"
      "<li>New session hosts let you choose how long a detached session is "
      "kept — 1 to 168 hours, default 72. Every session ends after one week "
      "at most.</li>"
      "<li>Fixed the sidebar losing your selection every few seconds while it "
      "refreshed session state in the background.</li></ul>",
   zh="<ul>"
      "<li>終端輸出裡的連結可以點了：按住 Command 高亮 URL，Command-點擊在瀏覽器開啟。"
      "基於安全考量只開 http/https，其他一律拒絕。</li>"
      "<li>新的 session host 可以自訂中斷連線後 session 保留多久 —— 1 到 168 小時，"
      "預設 72 小時。每個 session 最長存活一週。</li>"
      "<li>修正側邊欄的選取每隔幾秒被背景重新整理清掉的問題。</li></ul>",
   ja="<ul>"
      "<li>ターミナル出力内のリンクをクリックできるようになりました。Command を押しながら "
      "URL をハイライトし、Command クリックでブラウザで開きます。安全のため http/https "
      "以外は開きません。</li>"
      "<li>新しいセッションホストでは、切断後にセッションを保持する時間を 1〜168 時間"
      "（既定 72 時間）で選べます。どのセッションも最長 1 週間で終了します。</li>"
      "<li>バックグラウンド更新のたびにサイドバーの選択が数秒で消える問題を修正しました。</li></ul>",
   ko="<ul>"
      "<li>터미널 출력의 링크를 클릭할 수 있습니다. Command 를 누른 채 URL 을 강조하고 "
      "Command-클릭으로 브라우저에서 엽니다. 안전을 위해 http/https 만 열립니다.</li>"
      "<li>새 세션 호스트에서 연결 해제 후 세션 보존 시간을 1–168시간(기본 72시간)으로 "
      "설정할 수 있습니다. 모든 세션은 최대 1주일 후 종료됩니다.</li>"
      "<li>백그라운드 새로 고침 때마다 사이드바 선택이 사라지던 문제를 수정했습니다.</li></ul>"),
 ),
 dict(v="1.0.1", status="latest", date=dict(
   en="August 28, 2026", zh="2026 年 8 月 28 日",
   ja="2026 年 8 月 28 日", ko="2026년 8월 28일"),
  body=dict(
   en="<p>Updates the OpenAB Connect app icon.</p>",
   zh="<p>更新 OpenAB Connect 的 App 圖示。</p>",
   ja="<p>OpenAB Connect のアプリアイコンを更新しました。</p>",
   ko="<p>OpenAB Connect 앱 아이콘을 업데이트했습니다.</p>"),
 ),
 dict(v="1.0", status="", date=dict(
   en="August 27, 2026", zh="2026 年 8 月 27 日",
   ja="2026 年 8 月 27 日", ko="2026년 8월 27일"),
  body=dict(
   en="<p>First release on the Mac App Store. Agents from every major vendor "
      "in one client, each in its own sandboxed container on your Kubernetes "
      "cluster or AWS ECS Fargate — sessions outlive the app, nothing is "
      "exposed to the network, and your iPhone works as a push-to-talk "
      "remote.</p>",
   zh="<p>首度在 Mac App Store 上架。所有頂尖廠商的 agent，一個客戶端，各自在你的 "
      "Kubernetes 叢集或 AWS ECS Fargate 上的沙箱容器裡運行 —— session 活得比 app 久、"
      "什麼都不對外開放，iPhone 還能當按住說話的遙控器。</p>",
   ja="<p>Mac App Store で初公開。主要ベンダーすべてのエージェントをひとつのクライアントに。"
      "各エージェントは自分の Kubernetes クラスタや AWS ECS Fargate 上のサンドボックス化"
      "されたコンテナで動き、セッションはアプリより長生きし、外部には何も公開されません。"
      "iPhone はプッシュ・トゥ・トークのリモコンになります。</p>",
   ko="<p>Mac App Store 첫 출시. 모든 주요 벤더의 에이전트를 하나의 클라이언트로 — "
      "각 에이전트는 사용자의 Kubernetes 클러스터 또는 AWS ECS Fargate 의 샌드박스 "
      "컨테이너에서 실행되고, 세션은 앱보다 오래 살아남으며, 네트워크에 아무것도 "
      "노출하지 않습니다. iPhone 은 푸시 투 토크 리모컨이 됩니다.</p>"),
 ),
]

T = {
 "en": dict(title="OpenAB Connect — Releases",
   desc="What each OpenAB Connect release brought, newest first — including the "
        "version currently in App Review.",
   h1="Releases", lede="What each version brought, newest first. A version "
   "that has been submitted but not yet approved is listed here too.",
   store="Mac App Store ↗", badge_review="In review", badge_latest="Latest",
   plat="Mac"),
 "zh": dict(title="OpenAB Connect — 版本紀錄",
   desc="OpenAB Connect 每個版本帶來了什麼，由新到舊 —— 包含目前正在送審的版本。",
   h1="版本紀錄", lede="每個版本帶來了什麼，由新到舊。已送審、尚未通過的版本也會先列在這裡。",
   store="Mac App Store ↗", badge_review="審核中", badge_latest="最新",
   plat="Mac"),
 "ja": dict(title="OpenAB Connect — リリース",
   desc="OpenAB Connect の各リリースの内容を新しい順に。現在審査中のバージョンも掲載。",
   h1="リリース", lede="各バージョンの内容を新しい順に。提出済みでまだ承認されていない"
   "バージョンもここに掲載されます。",
   store="Mac App Store ↗", badge_review="審査中", badge_latest="最新",
   plat="Mac"),
 "ko": dict(title="OpenAB Connect — 릴리스",
   desc="OpenAB Connect 각 릴리스의 내용을 최신순으로 — 현재 심사 중인 버전 포함.",
   h1="릴리스", lede="각 버전의 내용을 최신순으로 정리했습니다. 제출되어 아직 승인되지 "
   "않은 버전도 함께 표시됩니다.",
   store="Mac App Store ↗", badge_review="심사 중", badge_latest="최신",
   plat="Mac"),
}

PAGE = """<!DOCTYPE html>
<html lang="{htmllang}" data-lang="{code}">
<head>
{head}
</head>
<body>
{nav}
<main class="notes-index">
  <h1>{h1}</h1>
  <p class="lede">{lede} <a href="{store_url}">{store}</a></p>
{entries}
</main>
{footer}
</body>
</html>
"""


def entry(code, r, t):
    badge = ""
    if r["status"] == "review":
        badge = f'<span class="relbadge review">{t["badge_review"]}</span>'
    elif r["status"] == "latest":
        badge = f'<span class="relbadge latest">{t["badge_latest"]}</span>'
    return f"""<article class="rel">
  <div class="rhead"><span class="ver">{r["v"]}</span>{badge}<span class="plat">{t["plat"]}</span><span class="when">{r["date"][code]}</span></div>
  {r["body"][code]}
</article>"""


def main():
    for code in chrome.ORDER:
        t = T[code]
        d = chrome.CHROME[code]
        entries = "\n".join(entry(code, r, t) for r in RELEASES)
        html = PAGE.format(
            htmllang=d["htmllang"], code=code,
            head=chrome.head(code, "releases/", t["title"], t["desc"]),
            nav=chrome.nav(code, "releases/"),
            h1=t["h1"], lede=t["lede"], store=t["store"], store_url=APP_STORE,
            entries=entries, footer=chrome.footer(code),
        )
        out = chrome.out_path(code, "releases/index.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
