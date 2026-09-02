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
# Per-storefront, matching each landing page's CTA. OpenAB Connect is a Mac app
# (?mt=12); OpenAB Remote is the iPhone companion, a separate App Store listing.
CONNECT_STORE = {
    "en": "https://apps.apple.com/app/openab-connect/id6803728097?mt=12",
    "zh": "https://apps.apple.com/tw/app/openab-connect/id6803728097?mt=12",
    "ja": "https://apps.apple.com/jp/app/openab-connect/id6803728097?mt=12",
    "ko": "https://apps.apple.com/kr/app/openab-connect/id6803728097?mt=12",
}
REMOTE_STORE = {
    "en": "https://apps.apple.com/us/app/openab-remote/id6805733009",
    "zh": "https://apps.apple.com/tw/app/openab-remote/id6805733009",
    "ja": "https://apps.apple.com/jp/app/openab-remote/id6805733009",
    "ko": "https://apps.apple.com/kr/app/openab-remote/id6805733009",
}

# ------------------------------------------------------------------ OpenAB Connect (Mac)
# Newest first. status: "review" | "latest" | ""
CONNECT_RELEASES = [
 dict(v="1.3.0", status="latest", date=dict(
   en="September 2, 2026", zh="2026 年 9 月 2 日",
   ja="2026 年 9 月 2 日", ko="2026년 9월 2일"),
  body=dict(
   en="<ul>"
      "<li>A dark, unified window chrome with Ghostty-style session tabs. "
      "Press Command-T or use the trailing + to open a new session on the "
      "selected connection.</li>"
      "<li>Redesigned connection cards group each host and show Kubernetes or "
      "ECS platform marks at a glance.</li>"
      "<li>The tab context menu can detach and close, rename, or colour a tab; "
      "the inactive pane now dims when a split is focused.</li>"
      "<li>More reliable recovery from dropped attaches, Devin TUI support, "
      "and an ephemeral-workspace disclosure that fades after eight seconds.</li></ul>",
   zh="<ul>"
      "<li>全新的深色一致介面，加入 Ghostty 風格的 session 分頁。按 Command-T 或分頁列末端的 "
      "+，即可在目前選取的連線開啟新 session。</li>"
      "<li>重新設計連線卡片，將每台 host 清楚分組，並以 Kubernetes 或 ECS 圖示標示平台。</li>"
      "<li>分頁右鍵選單可中斷連線並關閉、重新命名或加上顏色；聚焦分割畫面時，非作用中的窗格會變暗。</li>"
      "<li>更可靠地從 attach 連線中斷恢復，支援 Devin TUI，並加入暫時性 workspace 提示，"
      "顯示八秒後自動淡出。</li></ul>",
   ja="<ul>"
      "<li>ダークで統一されたウインドウに、Ghostty 風のセッションタブを追加。Command-T "
      "またはタブ列末尾の + で、選択中の接続に新しいセッションを開けます。</li>"
      "<li>接続カードを刷新し、ホストごとにまとめて Kubernetes または ECS のマークを表示します。</li>"
      "<li>タブのコンテキストメニューから切断して閉じる、名前を変更する、色を付ける操作が可能に。"
      "分割表示ではフォーカスされていないペインが暗くなります。</li>"
      "<li>切断されたアタッチからの復旧を改善し、Devin TUI に対応。エフェメラルなワークスペースの"
      "案内は 8 秒後にフェードアウトします。</li></ul>",
   ko="<ul>"
      "<li>어둡고 통일된 창에 Ghostty 스타일 세션 탭을 추가했습니다. Command-T 또는 탭 막대 "
      "끝의 +로 선택한 연결에서 새 세션을 열 수 있습니다.</li>"
      "<li>연결 카드를 새롭게 디자인해 호스트별로 묶고 Kubernetes 또는 ECS 플랫폼 표시를 보여 줍니다.</li>"
      "<li>탭 컨텍스트 메뉴에서 연결을 해제하고 닫기, 이름 변경, 색상 지정이 가능하며 분할 화면에서 "
      "포커스되지 않은 창은 어두워집니다.</li>"
      "<li>끊어진 연결의 복구를 개선하고 Devin TUI를 지원하며, 임시 워크스페이스 안내는 "
      "8초 후 사라집니다.</li></ul>"),
 ),
 dict(v="1.2.0", status="", date=dict(
   en="August 31, 2026", zh="2026 年 8 月 31 日",
   ja="2026 年 8 月 31 日", ko="2026년 8월 31일"),
  body=dict(
   en="<ul>"
      "<li>Copy on select: releasing a text selection in the terminal copies "
      "it to the clipboard automatically, iTerm-style.</li>"
      "<li>Dictation language: choose English or Traditional Chinese (台灣) "
      "for Press to Speak.</li>"
      "<li>Dictation is now fully on-device — the Groq Cloud option was "
      "removed and audio never leaves your Mac.</li>"
      "<li>Dictation setup problems now explain themselves in a dialog with "
      "the exact System Settings switch to flip.</li></ul>",
   zh="<ul>"
      "<li>選取即複製：在終端機放開選取的瞬間自動複製到剪貼簿，和 iTerm 一樣。</li>"
      "<li>聽寫語言：Press to Speak 可選英文或繁體中文（台灣）。</li>"
      "<li>聽寫全面改為裝置端處理 —— 移除 Groq Cloud 選項，語音永不離開你的 Mac。</li>"
      "<li>聽寫設定問題（未開啟聽寫、缺語言模型、權限被拒）現在會以對話框說明，"
      "並指出要開啟的系統設定。</li></ul>",
   ja="<ul>"
      "<li>選択でコピー：ターミナルで選択を離した瞬間、iTerm と同様に自動で"
      "クリップボードへコピーします。</li>"
      "<li>音声入力の言語：Press to Speak で英語または繁体字中国語（台湾）を選べます。</li>"
      "<li>音声入力は完全にオンデバイスに — Groq Cloud オプションを削除し、"
      "音声が Mac の外に出ることはありません。</li>"
      "<li>音声入力の設定問題はダイアログで、開くべきシステム設定とともに表示されます。</li></ul>",
   ko="<ul>"
      "<li>선택 시 복사: 터미널에서 선택을 놓는 순간 iTerm 처럼 자동으로 "
      "클립보드에 복사됩니다.</li>"
      "<li>받아쓰기 언어: Press to Speak 에서 영어 또는 번체 중국어(대만)를 선택할 수 있습니다.</li>"
      "<li>받아쓰기가 완전히 온디바이스로 — Groq Cloud 옵션이 제거되어 오디오가 "
      "Mac 을 떠나지 않습니다.</li>"
      "<li>받아쓰기 설정 문제는 열어야 할 시스템 설정과 함께 대화 상자로 안내됩니다.</li></ul>"),
 ),
 dict(v="1.1.0", status="", date=dict(
   en="August 30, 2026", zh="2026 年 8 月 30 日",
   ja="2026 年 8 月 30 日", ko="2026년 8월 30일"),
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
 dict(v="1.0.1", status="", date=dict(
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

# ------------------------------------------------------------------ OpenAB Remote (iPhone)
# The iPhone companion: attach to your Mac's sessions, and push-to-talk dictation.
# Newest first. status: "review" | "latest" | ""
REMOTE_RELEASES = [
 dict(v="0.2.1", status="review", date=dict(
   en="Submitted September 2, 2026", zh="2026 年 9 月 2 日送審",
   ja="2026 年 9 月 2 日申請", ko="2026년 9월 2일 심사 제출"),
  body=dict(
   en="<ul>"
      "<li>Importing connections from your Mac now mirrors the Mac exactly — "
      "connections you removed there no longer linger here.</li>"
      "<li>Fixed stray characters that could appear when attaching to a "
      "session another device had already opened.</li></ul>",
   zh="<ul>"
      "<li>從 Mac 匯入連線時，會完全對齊 Mac 目前的連線 —— 你在 Mac 移除的連線，"
      "這裡也不再殘留。</li>"
      "<li>修正接手其他裝置已開啟的 session 時，畫面可能出現的亂碼字元。</li></ul>",
   ja="<ul>"
      "<li>Mac から接続をインポートすると、Mac の現在の接続と完全に一致します —— "
      "Mac で削除した接続がこちらに残ることはありません。</li>"
      "<li>他のデバイスがすでに開いていたセッションにアタッチした際に、文字化けが"
      "表示されることがある問題を修正しました。</li></ul>",
   ko="<ul>"
      "<li>Mac 에서 연결을 가져오면 Mac 의 현재 연결과 정확히 일치합니다 —— "
      "Mac 에서 제거한 연결이 여기에 더 이상 남지 않습니다.</li>"
      "<li>다른 기기가 이미 열어 둔 세션에 연결할 때 깨진 문자가 나타날 수 있던 "
      "문제를 수정했습니다.</li></ul>"),
 ),
 dict(v="0.2.0", status="latest", date=dict(
   en="September 2, 2026", zh="2026 年 9 月 2 日",
   ja="2026 年 9 月 2 日", ko="2026년 9월 2일"),
  body=dict(
   en="<p>First release on the App Store. Pair with your Mac running OpenAB "
      "Connect and attach to any running session from your iPhone — the "
      "transcript replays and you can type or dictate. Press to Speak turns "
      "your voice into text on-device, and an offline demo lets you try every "
      "screen without pairing.</p>",
   zh="<p>首度在 App Store 上架。與執行 OpenAB Connect 的 Mac 配對，就能從 iPhone "
      "接手任何進行中的 session —— 內容會重播，你可以打字或口述。Press to Speak 在"
      "裝置端把語音轉成文字，離線 demo 則讓你不必配對就能試用每個畫面。</p>",
   ja="<p>App Store で初公開。OpenAB Connect を実行している Mac とペアリングすれば、"
      "iPhone から実行中のセッションにアタッチできます —— トランスクリプトが再生され、"
      "入力や音声入力ができます。Press to Speak は音声をオンデバイスでテキストに変換し、"
      "オフラインデモではペアリングなしですべての画面を試せます。</p>",
   ko="<p>App Store 첫 출시. OpenAB Connect 를 실행하는 Mac 과 페어링하면 iPhone 에서 "
      "실행 중인 세션에 연결할 수 있습니다 —— 기록이 재생되고 입력하거나 받아쓸 수 "
      "있습니다. Press to Speak 는 음성을 온디바이스로 텍스트로 변환하며, 오프라인 "
      "데모로 페어링 없이 모든 화면을 사용해 볼 수 있습니다.</p>"),
 ),
]

T = {
 "en": dict(title="OpenAB Connect — Releases",
   desc="What each OpenAB Connect and OpenAB Remote release brought, newest "
        "first — including the versions currently in App Review.",
   h1="Releases", lede="What each version brought, newest first. A version "
   "that has been submitted but not yet approved is listed here too.",
   connect_h="OpenAB Connect for Mac", remote_h="OpenAB Remote for iPhone",
   connect_store="Mac App Store ↗", remote_store="App Store ↗",
   badge_review="In review", badge_latest="Latest",
   plat_mac="Mac", plat_iphone="iPhone"),
 "zh": dict(title="OpenAB Connect — 版本紀錄",
   desc="OpenAB Connect 與 OpenAB Remote 每個版本帶來了什麼，由新到舊 —— 包含目前正在送審的版本。",
   h1="版本紀錄", lede="每個版本帶來了什麼，由新到舊。已送審、尚未通過的版本也會先列在這裡。",
   connect_h="OpenAB Connect for Mac", remote_h="OpenAB Remote for iPhone",
   connect_store="Mac App Store ↗", remote_store="App Store ↗",
   badge_review="審核中", badge_latest="最新",
   plat_mac="Mac", plat_iphone="iPhone"),
 "ja": dict(title="OpenAB Connect — リリース",
   desc="OpenAB Connect と OpenAB Remote の各リリースの内容を新しい順に。現在審査中のバージョンも掲載。",
   h1="リリース", lede="各バージョンの内容を新しい順に。提出済みでまだ承認されていない"
   "バージョンもここに掲載されます。",
   connect_h="OpenAB Connect for Mac", remote_h="OpenAB Remote for iPhone",
   connect_store="Mac App Store ↗", remote_store="App Store ↗",
   badge_review="審査中", badge_latest="最新",
   plat_mac="Mac", plat_iphone="iPhone"),
 "ko": dict(title="OpenAB Connect — 릴리스",
   desc="OpenAB Connect 와 OpenAB Remote 각 릴리스의 내용을 최신순으로 — 현재 심사 중인 버전 포함.",
   h1="릴리스", lede="각 버전의 내용을 최신순으로 정리했습니다. 제출되어 아직 승인되지 "
   "않은 버전도 함께 표시됩니다.",
   connect_h="OpenAB Connect for Mac", remote_h="OpenAB Remote for iPhone",
   connect_store="Mac App Store ↗", remote_store="App Store ↗",
   badge_review="심사 중", badge_latest="최신",
   plat_mac="Mac", plat_iphone="iPhone"),
}

PAGE = """<!DOCTYPE html>
<html lang="{htmllang}" data-lang="{code}">
<head>
{head}
</head>
<body>
{nav}
<main class="wrap notes-index">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
{sections}
</main>
{footer}
</body>
</html>
"""


def entry(code, r, t, plat):
    badge = ""
    if r["status"] == "review":
        badge = f'<span class="relbadge review">{t["badge_review"]}</span>'
    elif r["status"] == "latest":
        badge = f'<span class="relbadge latest">{t["badge_latest"]}</span>'
    return f"""<article class="rel">
  <div class="rhead"><span class="ver">{r["v"]}</span>{badge}<span class="plat">{plat}</span><span class="when">{r["date"][code]}</span></div>
  {r["body"][code]}
</article>"""


def section(code, t, heading, store_label, store_url, releases, plat):
    entries = "\n".join(entry(code, r, t, plat) for r in releases)
    return f"""<section class="relgroup">
  <h2 class="relgroup-h">{heading} <a href="{store_url}">{store_label}</a></h2>
{entries}
</section>"""


def main():
    for code in chrome.ORDER:
        t = T[code]
        d = chrome.CHROME[code]
        sections = "\n".join([
            section(code, t, t["connect_h"], t["connect_store"],
                    CONNECT_STORE[code], CONNECT_RELEASES, t["plat_mac"]),
            section(code, t, t["remote_h"], t["remote_store"],
                    REMOTE_STORE[code], REMOTE_RELEASES, t["plat_iphone"]),
        ])
        html = PAGE.format(
            htmllang=d["htmllang"], code=code,
            head=chrome.head(code, "releases/", t["title"], t["desc"]),
            nav=chrome.nav(code, "releases/"),
            h1=t["h1"], lede=t["lede"], sections=sections,
            footer=chrome.footer(code),
        )
        out = chrome.out_path(code, "releases/index.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
