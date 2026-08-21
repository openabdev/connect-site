#!/usr/bin/env python3
"""Emit the four language landing pages from one template.

Four near-identical HTML files drift: a fix lands in two of them and nobody
notices for a month. The structure lives here once and the languages are data.

    python3 scripts/build.py     # writes index.html, zh/, ja/, ko/
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Not translations of each other. Each carries the same argument in the way that
# language makes it: 聚合 has no direct equivalent, so Japanese uses まとめる
# ("gather into one") and Korean 한곳에서 ("in one place") rather than 集約/집약,
# which read like procurement documents.
L = {
    "en": dict(
        dir="", base="/", htmllang="en", label="EN",
        title="OpenAB Connect — agents from every major vendor, one client",
        desc="Agents from every major vendor in one macOS client, running distributed "
             "across your own private infrastructure, each in its own sandbox.",
        hero_h1='Agents from every major vendor,<br>one client',
        hero_sub="Running distributed across your own private infrastructure, each in its "
                 "own sandbox. <strong>Quit the app and they keep running.</strong>",
        nav=("What it is", "You own both ends", "Deploy", "Support"),
        shot_alt="OpenAB Connect with seven agent connections in the sidebar and four "
                 "terminal panes attached to different coding CLIs",
        shot_cap="Seven agents deployed, four attached at once. Every header states the two "
                 "things the runtime states about itself: the workspace is ephemeral, and "
                 "teardown is best-effort.",
        h_what="What it is",
        p_what="Your agent runs somewhere. When it leaves something half-finished you want a "
               "shell <em>there</em> — same image, same workspace, same files — not a "
               "reproduction of it on your laptop.",
        panel_1="<strong>The shell is deliberately powerless.</strong> It opens as "
                "<code>uid 1000</code> with no <code>sudo</code>, no service-account token, "
                "no host credentials, a read-only root filesystem and an ephemeral workspace.",
        panel_2="The runtime never listens on a routable address. A Tailscale sidecar is the "
                "only thing with a network identity, and the two talk over loopback inside "
                "the pod.",
        h_own="You own both ends",
        li_1="<strong>There is no service here.</strong> Every server the app talks to is one "
             "you deployed, in your own Kubernetes cluster or your own AWS account.",
        li_2="<strong>No account, no sign-up, no telemetry.</strong> Credentials you supply "
             "stay in your macOS Keychain and go nowhere except your own runtime.",
        li_3="<strong>The runtime is open source</strong> under MIT: "
             '<a href="https://github.com/openabdev/openab-pty">openabdev/openab-pty</a>. '
             "Read exactly what you are deploying, or write your own client against "
             '<a href="https://github.com/openabdev/openab-pty/blob/main/runtime/CLIENT-CONTRACT.md">'
             "the client contract</a>. This app is one implementation of it, and is not open source.",
        h_deploy="Deploy it",
        p_deploy="Three clicks, and the app does eight things: mints a credential into your "
                 "Keychain, ensures the namespace, creates the secret and the volume, applies "
                 "the pod, waits for it to run, waits for it to join your tailnet, and "
                 "verifies the admin plane. No manifests to write, no ports to open.",
        p_variants="One image per agent CLI — Claude Code, Codex, Cursor, Kiro, Gemini, "
                   "Copilot and more. The <code>native</code> variant carries no agent at all.",
        h_demo="Trying it without a cluster",
        p_demo="The app ships an offline <strong>Demo Mode</strong> in its app menu: two "
               "sample connections and a canned terminal, with no network connection of any "
               "kind. It is there so the app can be evaluated before you deploy anything.",
        f=("Privacy", "Support", "Runtime source"),
    ),
    "zh": dict(
        dir="zh", base="/zh/", htmllang="zh-Hant", label="中文",
        title="OpenAB Connect — 所有頂尖廠商的 Agent,一個客戶端",
        desc="所有頂尖廠商的 Agent,一個客戶端,分散運行在你的私有基礎架構,各自沙箱。",
        hero_h1="所有頂尖廠商的 Agent,<br>一個客戶端",
        hero_sub="分散運行在你的私有基礎架構,各自沙箱。<strong>關掉 app,它們繼續跑。</strong>",
        nav=("這是什麼", "兩端都是你的", "部署", "支援"),
        shot_alt="OpenAB Connect 側邊欄有七個 agent 連線,四個終端分割視窗分別接著不同的 coding CLI",
        shot_cap="七個 agent 已部署,四個同時接上。每一條標題列都寫著 runtime 對自己的兩項聲明:"
                 "workspace 是暫存的,teardown 是 best-effort。",
        h_what="這是什麼",
        p_what="你的 agent 跑在某處。它把事情做到一半時,你想要的是**那裡**的一個 shell —— "
               "同一個映像、同一個 workspace、同一批檔案,而不是在筆電上重現一次。",
        panel_1="<strong>這個 shell 刻意沒有權限。</strong>它以 <code>uid 1000</code> 開啟,"
                "沒有 <code>sudo</code>、沒有 service-account token、沒有主機憑證,"
                "根檔案系統唯讀,workspace 用完即棄。",
        panel_2="runtime 從不監聽可路由的位址。只有 Tailscale sidecar 擁有網路身分,"
                "兩者在 pod 內經 loopback 通訊。",
        h_own="兩端都是你的",
        li_1="<strong>這裡沒有任何服務。</strong>app 連上的每一台伺服器都是你自己部署的 —— "
             "在你自己的 Kubernetes 叢集,或你自己的 AWS 帳號裡。",
        li_2="<strong>不需要帳號、不需要註冊、沒有遙測。</strong>你輸入的憑證留在 macOS Keychain,"
             "除了你自己的 runtime 之外不會送到任何地方。",
        li_3="<strong>runtime 是 MIT 開源的</strong>:"
             '<a href="https://github.com/openabdev/openab-pty">openabdev/openab-pty</a>。'
             "你可以確認自己到底部署了什麼,也可以照 "
             '<a href="https://github.com/openabdev/openab-pty/blob/main/runtime/CLIENT-CONTRACT.md">'
             "客戶端契約</a>寫自己的客戶端。這個 app 只是其中一種實作,它不是開源的。",
        h_deploy="部署",
        p_deploy="你點三下,它做八件事:產生憑證存進 Keychain、確認 namespace、建立 secret 與儲存、"
                 "套用 pod、等它就緒、等它加入你的 tailnet、驗證管理端。"
                 "不必寫 manifest,也不必開任何對外連接埠。",
        p_variants="每個 agent CLI 一個映像 —— Claude Code、Codex、Cursor、Kiro、Gemini、Copilot 等。"
                   "<code>native</code> 版本不含任何 agent。",
        h_demo="沒有叢集也能試",
        p_demo="app 的應用程式選單裡有離線的 <strong>Demo Mode</strong>:兩個範例連線和一個預錄的終端,"
               "完全不建立任何網路連線。它的存在就是為了讓你在部署任何東西之前先評估這個 app。",
        f=("隱私", "支援", "runtime 原始碼"),
    ),
    "ja": dict(
        dir="ja", base="/ja/", htmllang="ja", label="日本語",
        title="OpenAB Connect — 主要ベンダーのエージェントを、ひとつのクライアントに",
        desc="主要ベンダーのエージェントをひとつのクライアントにまとめ、"
             "自分のプライベート環境に分散して、それぞれのサンドボックスで動かします。",
        hero_h1="主要ベンダーのエージェントを、<br>ひとつのクライアントに",
        hero_sub="自分のプライベート環境に分散して、それぞれのサンドボックスで動きます。"
                 "<strong>アプリを閉じても、動き続けます。</strong>",
        nav=("これは何か", "両端はあなたのもの", "デプロイ", "サポート"),
        shot_alt="サイドバーに 7 つのエージェント接続、4 つのターミナルペインがそれぞれ別の "
                 "coding CLI に接続している OpenAB Connect",
        shot_cap="7 つデプロイし、4 つを同時に接続。各ヘッダーはランタイム自身が明言している 2 点を"
                 "そのまま表示します。ワークスペースは一時的であること、そして終了処理は "
                 "best-effort であること。",
        h_what="これは何か",
        p_what="エージェントはどこかで動いています。作業が途中で止まったとき、必要なのは"
               "<em>その場所</em>のシェルです。同じイメージ、同じワークスペース、同じファイル。"
               "手元で再現したものではありません。",
        panel_1="<strong>このシェルには意図的に権限がありません。</strong><code>uid 1000</code> "
                "で開き、<code>sudo</code> なし、サービスアカウントトークンなし、ホストの資格情報"
                "なし、ルートファイルシステムは読み取り専用、ワークスペースは使い捨てです。",
        panel_2="ランタイムはルーティング可能なアドレスを一切リッスンしません。ネットワーク上の"
                "識別を持つのは Tailscale サイドカーだけで、両者は pod 内の loopback で会話します。",
        h_own="両端はあなたのもの",
        li_1="<strong>ここにサービスはありません。</strong>アプリが接続する先はすべて、"
             "あなたが自分の Kubernetes クラスタか AWS アカウントにデプロイしたものです。",
        li_2="<strong>アカウント登録なし、テレメトリなし。</strong>入力した資格情報は macOS の"
             "キーチェーンに留まり、あなた自身のランタイム以外へは送信されません。",
        li_3="<strong>ランタイムは MIT ライセンスのオープンソースです</strong>:"
             '<a href="https://github.com/openabdev/openab-pty">openabdev/openab-pty</a>。'
             "何をデプロイしているかを自分で確認できますし、"
             '<a href="https://github.com/openabdev/openab-pty/blob/main/runtime/CLIENT-CONTRACT.md">'
             "クライアント契約</a>に沿って自分のクライアントを書くこともできます。"
             "このアプリはその一実装で、オープンソースではありません。",
        h_deploy="デプロイ",
        p_deploy="3 クリックで、アプリが 8 つの作業を行います。資格情報の生成とキーチェーンへの保存、"
                 "namespace の確認、secret とボリュームの作成、pod の適用、起動待ち、"
                 "tailnet への参加待ち、管理プレーンの検証。マニフェストを書く必要も、"
                 "ポートを開ける必要もありません。",
        p_variants="エージェント CLI ごとに 1 つのイメージ — Claude Code、Codex、Cursor、Kiro、"
                   "Gemini、Copilot など。<code>native</code> はエージェントを含みません。",
        h_demo="クラスタなしで試す",
        p_demo="アプリメニューにオフラインの <strong>Demo Mode</strong> があります。"
               "サンプル接続 2 つと収録済みのターミナルだけで、ネットワーク接続は一切行いません。"
               "何もデプロイする前に評価できるようにするためのものです。",
        f=("プライバシー", "サポート", "ランタイムのソース"),
    ),
    "ko": dict(
        dir="ko", base="/ko/", htmllang="ko", label="한국어",
        title="OpenAB Connect — 주요 벤더의 에이전트를 클라이언트 하나로",
        desc="주요 벤더의 에이전트를 클라이언트 한곳에서. 여러분의 사설 인프라에 분산되어 "
             "각자 샌드박스에서 실행됩니다.",
        hero_h1="주요 벤더의 에이전트를,<br>클라이언트 하나로",
        hero_sub="여러분의 사설 인프라에 분산되어, 각자 샌드박스에서 실행됩니다. "
                 "<strong>앱을 닫아도 계속 실행됩니다.</strong>",
        nav=("무엇인가", "양쪽 모두 내 것", "배포", "지원"),
        shot_alt="사이드바에 에이전트 연결 7개, 서로 다른 coding CLI에 연결된 터미널 패널 4개가 "
                 "열려 있는 OpenAB Connect",
        shot_cap="7개를 배포하고 4개를 동시에 연결한 화면. 각 헤더는 런타임이 스스로 밝히는 두 "
                 "가지를 그대로 보여줍니다. 워크스페이스는 임시이며, 종료 처리는 best-effort입니다.",
        h_what="무엇인가",
        p_what="에이전트는 어딘가에서 돌아갑니다. 작업이 중간에 멈췄을 때 필요한 것은 "
               "<em>그곳</em>의 셸입니다. 같은 이미지, 같은 워크스페이스, 같은 파일. "
               "노트북에서 재현한 것이 아닙니다.",
        panel_1="<strong>이 셸은 의도적으로 권한이 없습니다.</strong><code>uid 1000</code>으로 "
                "열리며 <code>sudo</code>도, 서비스 어카운트 토큰도, 호스트 자격 증명도 없습니다. "
                "루트 파일시스템은 읽기 전용이고 워크스페이스는 일회용입니다.",
        panel_2="런타임은 라우팅 가능한 주소를 전혀 수신하지 않습니다. 네트워크 신원을 가진 것은 "
                "Tailscale 사이드카뿐이며, 둘은 pod 내부 loopback으로 통신합니다.",
        h_own="양쪽 모두 내 것",
        li_1="<strong>여기에 서비스는 없습니다.</strong> 앱이 연결하는 서버는 모두 여러분이 자신의 "
             "Kubernetes 클러스터나 AWS 계정에 배포한 것입니다.",
        li_2="<strong>계정도, 가입도, 텔레메트리도 없습니다.</strong> 입력한 자격 증명은 macOS "
             "키체인에 남고, 여러분 자신의 런타임 외에는 어디로도 전송되지 않습니다.",
        li_3="<strong>런타임은 MIT 오픈소스입니다</strong>: "
             '<a href="https://github.com/openabdev/openab-pty">openabdev/openab-pty</a>. '
             "무엇을 배포하는지 직접 확인할 수 있고, "
             '<a href="https://github.com/openabdev/openab-pty/blob/main/runtime/CLIENT-CONTRACT.md">'
             "클라이언트 계약</a>에 맞춰 자신의 클라이언트를 만들 수도 있습니다. "
             "이 앱은 그 구현 중 하나이며 오픈소스가 아닙니다.",
        h_deploy="배포",
        p_deploy="세 번의 클릭으로 앱이 여덟 가지를 처리합니다. 자격 증명 생성과 키체인 저장, "
                 "namespace 확인, secret과 볼륨 생성, pod 적용, 실행 대기, tailnet 참여 대기, "
                 "관리 평면 검증. 매니페스트를 쓸 필요도, 포트를 열 필요도 없습니다.",
        p_variants="에이전트 CLI마다 이미지 하나 — Claude Code, Codex, Cursor, Kiro, Gemini, "
                   "Copilot 등. <code>native</code>는 에이전트를 포함하지 않습니다.",
        h_demo="클러스터 없이 사용해 보기",
        p_demo="앱 메뉴에 오프라인 <strong>Demo Mode</strong>가 있습니다. 샘플 연결 두 개와 "
               "미리 녹화된 터미널만 있고 어떤 네트워크 연결도 하지 않습니다. 아무것도 배포하기 "
               "전에 앱을 평가할 수 있도록 넣었습니다.",
        f=("개인정보", "지원", "런타임 소스"),
    ),
}

ORDER = ["zh", "ja", "ko", "en"]

def switcher(current):
    parts = []
    for code in ORDER:
        d = L[code]
        cls = ' class="active"' if code == current else ""
        parts.append(f'<a{cls} href="{d["base"]}">{d["label"]}</a>')
    return "|".join(parts)

TEMPLATE = """<!DOCTYPE html>
<html lang="{htmllang}" data-lang="{code}" data-base="{base}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://connect.openab.dev{base}">
<link rel="icon" href="/icon.png">
<link rel="stylesheet" href="/style.css">
{alternates}
<script src="/lang.js"></script>
</head>
<body>

<nav>
  <a class="brand" href="{base}"><img src="/icon.png" alt="" width="28" height="28">OpenAB Connect</a>
  <div class="links">
    <a href="#what">{nav0}</a>
    <a href="#own">{nav1}</a>
    <a href="#deploy">{nav2}</a>
    <a href="/support.html">{nav3}</a>
    <span class="lang">{switcher}</span>
  </div>
</nav>

<div class="wrap">

<header>
  <img class="appicon" src="/icon.png" alt="OpenAB Connect">
  <h1>{hero_h1}</h1>
  <p class="tag">{hero_sub}</p>
</header>

<figure>
  <img src="/screenshot.png" alt="{shot_alt}">
  <figcaption>{shot_cap}</figcaption>
</figure>

<h2 id="what">{h_what}</h2>
<p>{p_what}</p>

<div class="panel">
<p style="margin-top:0">{panel_1}</p>
<p style="margin-bottom:0" class="dim">{panel_2}</p>
</div>

<h2 id="own">{h_own}</h2>
<ul>
  <li>{li_1}</li>
  <li>{li_2}</li>
  <li>{li_3}</li>
</ul>

<h2 id="deploy">{h_deploy}</h2>
<p>{p_deploy}</p>
<p class="dim">{p_variants}</p>

<h2 id="demo">{h_demo}</h2>
<p class="note">{p_demo}</p>

<footer>
  <a href="/privacy.html">{f0}</a>
  <a href="/support.html">{f1}</a>
  <a href="https://github.com/openabdev/openab-pty">{f2}</a>
  <span class="dim">© 2026 openabdev</span>
</footer>

</div>
</body>
</html>
"""

def alternates():
    rows = [f'<link rel="alternate" hreflang="{L[c]["htmllang"]}" '
            f'href="https://connect.openab.dev{L[c]["base"]}">' for c in ORDER]
    # x-default is what a search engine serves when it matches no listed language.
    rows.append('<link rel="alternate" hreflang="x-default" href="https://connect.openab.dev/">')
    return "\n".join(rows)

for code in ORDER:
    d = L[code]
    out = ROOT / d["dir"] / "index.html" if d["dir"] else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = TEMPLATE.format(
        code=code, alternates=alternates(), switcher=switcher(code),
        nav0=d["nav"][0], nav1=d["nav"][1], nav2=d["nav"][2], nav3=d["nav"][3],
        f0=d["f"][0], f1=d["f"][1], f2=d["f"][2],
        **{k: v for k, v in d.items() if k not in ("nav", "f", "dir", "label")})
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)}")
