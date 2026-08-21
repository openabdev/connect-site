#!/usr/bin/env python3
"""Emit the four language landing pages from one template.

Four near-identical HTML files drift: a fix lands in two of them and nobody
notices for a month. The structure lives here once and the languages are data.

    python3 scripts/build.py     # writes index.html, zh/, ja/, ko/

Page shape, following foldic.app: hero, screenshot, six feature cards, FAQ,
footer. The prose that used to sit between the cards and the footer is now FAQ
entries — a visitor who wants the argument opens it, and one who wants to know
whether it runs on their cluster does not have to read past it.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

ORDER = ["zh", "ja", "ko", "en"]

ICONS = [
    # stacked layers — many vendors, one surface
    '<path d="M12 2 2 7l10 5 10-5z"/><path d="M2 12l10 5 10-5"/><path d="M2 17l10 5 10-5"/>',
    # cycle — the session comes back
    '<path d="M21 12a9 9 0 1 1-2.64-6.36M21 3v6h-6"/>',
    # padlock — nothing exposed
    '<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    # stacked racks — any cluster
    '<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01"/>',
    # angle brackets — open source
    '<path d="M8 6 3 12l5 6M16 6l5 6-5 6"/>',
    # microphone — say it
    '<path d="M12 3a3 3 0 0 1 3 3v5a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3z"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
]

PTY = "https://github.com/openabdev/openab-pty"
CONTRACT = PTY + "/blob/main/runtime/CLIENT-CONTRACT.md"

# Not translations of each other. Each carries the same argument in the way that
# language makes it: 聚合 has no direct equivalent, so Japanese gathers into one
# (ひとつのクライアント) and Korean uses 하나 rather than 集約/집약, which read like
# procurement documents.
L = {
 "en": dict(
  dir="", base="/", htmllang="en", label="EN",
  title="OpenAB Connect — agents from every major vendor, one client",
  desc="Agents from every major vendor in one macOS client. Encrypted and distributed "
       "across your own private infrastructure, each in its own sandbox.",
  hero_h1='Agents from every major vendor.<br><span class="mark">One client</span>, each sandboxed.',
  hero_sub="Encrypted and distributed across your own private infrastructure.<br>"
           "<strong>Quit the app and they keep running.</strong>",
  nav=("Features", "FAQ", "Support"),
  shot_alt="OpenAB Connect with seven agent connections in the sidebar and four terminal "
           "panes attached to different coding CLIs",
  soon_label="coming soon",
  feats=[
   ("Every major vendor",
    "Thirteen agent CLIs, one image each — Claude Code, Codex, Cursor, Kiro, Gemini, "
    "Copilot and more. Chosen per session. The <code>native</code> variant carries no "
    "agent at all."),
   ("Sessions outlive the client",
    "The shell runs in the container, not on your Mac. Quit the app and it keeps going; "
    "reopen and you are in the same split layout, output resuming from the byte where "
    "it stopped."),
   ("Nothing is exposed",
    "No ports opened, no ingress, no public endpoint. A Tailscale sidecar is the only "
    "thing with a network identity; the runtime binds loopback only."),
   ("Any Kubernetes, or ECS",
    "It deploys a plain pod, so any conformant cluster works — k3s on a spare box, EKS, "
    "GKE. Or AWS ECS Fargate, where there is no cluster to run at all."),
   ("The runtime is open source",
    f'MIT licensed at <a href="{PTY}">openabdev/openab-pty</a>. Read exactly what you '
    "are about to run, or write your own client against the published contract."),
   ("Just say it",
    "Talk to the agent instead of typing at it — the same session, driven by chat or "
    "voice through openab.", True),
  ],
  faq_title="Questions",
  faq=[
   ("why-not-ssh", "How is this different from <code>kubectl exec</code> or SSH?",
    "Both give you a shell; neither gives you a session that survives. Quit your "
    "terminal mid-<code>exec</code> and the process dies with the connection. Here the "
    "session lives in the container, so closing the app closes a WebSocket and nothing "
    "else — the next launch re-attaches from the byte where output stopped and restores "
    "the same split layout. The deployment model differs too: no kubeconfig on the "
    "client, no port-forward, and a credential that authorises one session rather than "
    "your whole cluster."),
   ("vs-herdr", "How is this different from Herdr?",
    "<p>Herdr is an agent multiplexer — tmux for coding agents. It gives each agent a real "
    "PTY, keeps them alive across disconnects, classifies every pane as working, blocked "
    "or idle, and exposes a CLI and a socket API. The persistence and the fleet view "
    "overlap with this app almost exactly. What differs is where the agents run:"
    "</p><ul>"
    "<li><strong>Herdr</strong> runs them on the machine you invoke it on, sharing your "
    "user, your filesystem and your credentials — so the blast radius is that machine and everything your account can reach. "
    "Its persistence is across disconnects, not across the host powering off, so on a "
    "laptop, closing the lid ends everything. (Its SSH remote mode avoids that, at the "
    "cost of moving the blast radius to the remote host.)</li>"
    "<li><strong>OpenAB Connect</strong> gives each session its own container in your "
    "cluster — <code>uid 1000</code>, no <code>sudo</code>, no host credentials, "
    "read-only root, ephemeral workspace — reached over a WireGuard tailnet with no port "
    "exposed.</li>"
    "</ul>"
    "<p>The difference is sandboxing, not multiplexing. Herdr also does things OpenAB "
    "Connect does not: pane state classification, a scriptable local API, and running "
    "with no infrastructure at all. If you want nothing to deploy, Herdr is the better "
    "answer.</p>"),
   ("vs-local", "How is this different from just running Claude Code or Codex on my Mac?",
    "An agent on your Mac runs as you. It can reach your SSH keys, your cloud credentials, "
    "your npm and GitHub tokens, and every repository on the disk — so a wrong command is a "
    "wrong command on your machine. Here the shell has none of that, the workspace is "
    "discarded with the session, and several agents can work at once without competing for "
    "the same working tree or the same ports. Your laptop can sleep or close without "
    "stopping anything. The cost is real: the agent cannot see your local files, so work "
    "arrives by git; the first pull of an image takes a few minutes; and you need a cluster "
    "or an AWS account. For a quick edit in a repo you already have open, running locally "
    "is simpler and this adds nothing."),
   ("what-can-the-shell-do", "How much can the shell actually do?",
    "Deliberately little. It opens as <code>uid 1000</code> with no <code>sudo</code>, "
    "no service-account token and no host credentials, on a read-only root filesystem "
    "with an ephemeral workspace. A session shell can reach the runtime over loopback, "
    "which is why the admin credential is never inside the container: an attach token "
    "authorises exactly one session and expires."),
   ("open-ports", "Do I have to open a port or set up ingress?",
    "No. The runtime binds <code>127.0.0.1</code> and holds no TLS key. A Tailscale "
    "sidecar in the same pod is the only thing with a network identity, and the two "
    "talk over loopback inside the pod's network namespace. Traffic reaches you over "
    "the WireGuard tailnet, which is what carries the encryption."),
   ("do-you-see-my-data", "What do you receive?",
    "Nothing. There is no service here — every server the app talks to is one you "
    "deployed, in your own cluster or your own AWS account. No account, no sign-up, no "
    "analytics, no telemetry. Credentials you supply stay in the macOS Keychain and go "
    "nowhere except your own runtime."),
   ("inspect-first", "Can I see what I am deploying before I deploy it?",
    f'Yes. The runtime is MIT licensed at <a href="{PTY}">openabdev/openab-pty</a>, and '
    f'the <a href="{CONTRACT}">client contract</a> is published, so you can write your '
    "own client instead of using this one. This app is one implementation of that "
    "contract and is not open source."),
   ("try-without-cluster", "Can I try it without a cluster?",
    "Yes. <strong>Demo Mode</strong> in the app menu runs two sample connections and a "
    "recorded terminal with no network connection of any kind. It exists so the app can "
    "be evaluated before you deploy anything."),
   ("what-deploy-does", "What happens when I deploy?",
    "Three clicks, then eight steps: a credential is minted into your Keychain, the "
    "namespace is ensured, the secret and volume are created, the pod is applied, and "
    "the app waits for it to run, waits for it to join your tailnet, and verifies the "
    "admin plane. No manifests to write. The first deploy of an image can take a couple "
    "of minutes because the cluster is pulling it."),
   ("teardown", "Is anything left behind when I delete a session?",
    "<p><strong>The workspace is discarded.</strong> That part is certain: it exists only "
    "for that session, and deleting the session deletes it.</p>"
    "<p>What is not certain is processes. Deleting a session terminates that session's "
    "process group, but a process that deliberately leaves that group — a background job "
    "started with <code>nohup</code> or <code>setsid</code> — can outlive it until the pod "
    "or task is replaced. It is still confined to the same sandbox and gains no new reach, "
    "but it keeps consuming that pod's CPU and memory.</p>"
    "<p>So this is labelled best-effort in the app rather than claimed as a clean kill. To "
    "be certain nothing remains, delete the pod or task.</p>"),
  ],
  f=("Privacy", "Support", "Runtime source"),
 ),

 "zh": dict(
  dir="zh", base="/zh/", htmllang="zh-Hant", label="中文",
  title="OpenAB Connect — 所有頂尖廠商的 Agent，一個客戶端",
  desc="所有頂尖廠商的 Agent，一個客戶端，各自沙箱。加密分散運行在你的私有基礎架構。",
  hero_h1='所有頂尖廠商的 Agent，<br><span class="mark">一個客戶端</span>，各自沙箱。',
  hero_sub="加密分散運行在你的私有基礎架構，關掉 app，<br>"
           "<strong>它們繼續運行。</strong>",
  nav=("特色", "常見問題", "支援"),
  shot_alt="OpenAB Connect 側邊欄有七個 agent 連線，四個終端分割視窗分別接著不同的 coding CLI",
  soon_label="即將推出",
  feats=[
   ("涵蓋所有頂尖廠商",
    "13 種 agent CLI，各自一個映像 —— Claude Code、Codex、Cursor、Kiro、Gemini、"
    "Copilot 等，每個 session 分別選擇。<code>native</code> 版本不含任何 agent。"),
   ("Session 活得比客戶端久",
    "shell 跑在容器裡，不在你的 Mac 上。關掉 app 它繼續跑；再開啟就回到原本的分割版面，"
    "輸出從中斷的那個位元組接續。"),
   ("什麼都不對外開放",
    "不開連接埠、沒有 ingress、沒有公開端點。只有 Tailscale sidecar 擁有網路身分，"
    "runtime 只綁 loopback。"),
   ("任何 Kubernetes 或 ECS",
    "它部署的是一個單純的 pod，所以任何符合規範的叢集都能跑 —— 閒置機器上的 k3s、EKS、"
    "GKE。或是 AWS ECS Fargate，那裡連叢集都不必維護。"),
   ("核心 runtime 開放原始碼",
    f'MIT 授權，位於 <a href="{PTY}">openabdev/openab-pty</a>。你可以先確認自己要跑的'
    "到底是什麼，也可以照公開的契約寫自己的客戶端。"),
   ("用說的也可以通",
    "不只打字 —— 透過 openab 用聊天或語音對同一個 session 下指令。", True),
  ],
  faq_title="常見問題",
  faq=[
   ("why-not-ssh", "這和 <code>kubectl exec</code> 或 SSH 有什麼不同?",
    "兩者都給你一個 shell，但都不給你一個活得下去的 session。<code>exec</code> 進行中"
    "關掉終端，程序就跟著連線一起死。這裡的 session 活在容器裡，關掉 app 只是關掉一條 "
    "WebSocket，其他什麼都沒發生 —— 下次啟動從輸出中斷的那個位元組接回來，並還原同一個"
    "分割版面。部署模型也不同:客戶端上沒有 kubeconfig、不需要 port-forward，"
    "而且憑證授權的是一個 session，不是你的整個叢集。此外你要的往往不是「一個 shell」，"
    "而是「那個運行環境」裡的 shell —— 同一個映像、同一個 workspace、同一批檔案，"
    "不是在筆電上重現一次。"),
   ("vs-herdr", "這跟 Herdr 有什麼不同?",
    "<p>Herdr 是 agent multiplexer —— coding agent 版的 tmux。它給每個 agent 一個真實 PTY、"
    "斷線後仍活著、把每個窗格分類成 working／blocked／idle，還有 CLI 和 socket API。"
    "持久性和艦隊視圖這兩點和這個 app 幾乎完全重疊。不同的是 agent 跑在哪裡:"
    "</p><ul>"
    "<li><strong>Herdr</strong> 把它們跑在你叫它的那台機器上，共用你的使用者、"
    "你的檔案系統、你的憑證 —— 風險與爆炸半徑就是那台機器，以及你的帳號碰得到的一切。"
    "它的持久性是針對斷線而非主機關機，所以跑在筆電上時，筆電關了就什麼都沒了。"
    "（SSH 遠端模式可以避開這點，代價是爆炸半徑換成那台遠端主機。）</li>"
    "<li><strong>OpenAB Connect</strong> 每個 session 是你叢集裡自己的容器 —— "
    "<code>uid 1000</code>、沒有 <code>sudo</code>、沒有主機憑證、根檔案系統唯讀、"
    "workspace 用完即棄 —— 經 WireGuard tailnet 連上，不開任何連接埠。</li>"
    "</ul>"
    "<p>分野是沙箱化，不是多工。Herdr 也做得到一些 OpenAB Connect 做不到的事:"
    "窗格狀態判定、可腳本化的本機 API，以及完全不需要任何基礎架構。"
    "如果你希望什麼都不用部署，Herdr 是更好的答案。</p>"),
   ("vs-local", "這跟只在我的電腦上跑 Claude Code 或 Codex Desktop 有什麼不同?",
    "在你 Mac 上的 agent 是以你的身分執行的。它碰得到你的 SSH 金鑰、你的雲端憑證、"
    "你的 npm 和 GitHub token，以及磁碟上每一個 repository —— 所以一個下錯的指令，"
    "是在你的機器上下錯。這裡的 shell 什麼都沒有，workspace 隨 session 一起丟掉，"
    "而且好幾個 agent 可以同時工作而不必爭同一個 working tree 或同一組連接埠。"
    "你的筆電也可以睡眠或闔上，什麼都不會停。"
    "代價是真的:agent 看不到你本機的檔案，工作要透過 git 送過去;某個映像第一次拉取"
    "要幾分鐘;而且你需要一個叢集或一個 AWS 帳號。如果只是在一個已經開著的 repo 裡改一行，"
    "在本機跑更簡單，這個東西沒有任何幫助。"),
   ("what-can-the-shell-do", "這個 shell 到底能做多少事?",
    "刻意很少。它以 <code>uid 1000</code> 開啟，沒有 <code>sudo</code>、沒有 "
    "service-account token、沒有主機憑證，根檔案系統唯讀，workspace 用完即棄。"
    "session 的 shell 可以經 loopback 連到 runtime —— 這正是管理憑證從不放進容器的原因:"
    "attach token 只授權一個 session，而且會過期。"),
   ("open-ports", "我需要開連接埠或設定 ingress 嗎?",
    "不需要。runtime 綁在 <code>127.0.0.1</code>，本身不持有 TLS 金鑰。"
    "同一個 pod 裡的 Tailscale sidecar 是唯一擁有網路身分的東西，兩者在 pod 的網路"
    "命名空間內經 loopback 通訊。流量走 WireGuard tailnet 到你手上，加密由它承擔。"),
   ("do-you-see-my-data", "你們會收到什麼?",
    "什麼都沒有。這裡沒有任何服務 —— app 連上的每一台伺服器都是你自己部署的，"
    "在你自己的叢集或你自己的 AWS 帳號裡。不需要帳號、不需要註冊、沒有分析、沒有遙測。"
    "你輸入的憑證留在 macOS Keychain，除了你自己的 runtime 之外不會送到任何地方。"),
   ("inspect-first", "我可以在部署前先確認要部署什麼嗎?",
    f'可以。runtime 是 MIT 授權的 <a href="{PTY}">openabdev/openab-pty</a>，'
    f'而且 <a href="{CONTRACT}">客戶端契約</a>是公開的，'
    "所以你可以不用這個 app、自己寫一個客戶端。這個 app 只是那份契約的一種實作，"
    "它不是開源的。"),
   ("try-without-cluster", "沒有叢集可以先試嗎?",
    "可以。應用程式選單裡的 <strong>Demo Mode</strong> 會跑兩個範例連線和一個預錄的終端，"
    "完全不建立任何網路連線。它的存在就是為了讓你在部署任何東西之前先評估這個 app。"),
   ("what-deploy-does", "按下部署之後發生什麼事?",
    "你點三下，然後是八個步驟:產生憑證存進你的 Keychain、確認 namespace、"
    "建立 secret 與儲存、套用 pod，然後 app 等它就緒、等它加入你的 tailnet、驗證管理端。"
    "不必寫 manifest。某個映像第一次部署可能要幾分鐘,因為叢集正在拉取它。"),
   ("teardown", "刪掉 session 之後會留下東西嗎?",
    "<p><strong>workspace 會被丟掉</strong>，這部分是確定的:它只存在於那個 session，"
    "刪除就沒了。</p>"
    "<p>不確定的是程序。刪除 session 時，runtime 會終止這個 session 的 process group，"
    "但一個刻意脫離那個 group 的程序 —— 例如用 <code>nohup</code> 或 <code>setsid</code> "
    "啟動的背景工作 —— 可能活下來，直到那個 pod 或 task 被替換。它仍然關在同一個沙箱裡，"
    "不會因此碰到任何新的東西，但它會繼續佔用那個 pod 的 CPU 和記憶體。</p>"
    "<p>所以這件事在 app 裡標示為 best-effort，而不是聲稱乾淨結束。"
    "要確定什麼都不剩，刪掉那個 pod 或 task。</p>"),
  ],
  f=("隱私", "支援", "runtime 原始碼"),
 ),

 "ja": dict(
  dir="ja", base="/ja/", htmllang="ja", label="日本語",
  title="OpenAB Connect — すべての主要ベンダーのエージェントを、ひとつのクライアントに",
  desc="すべての主要ベンダーのエージェントをひとつのクライアントに。暗号化されたまま、"
       "自分のプライベート環境に分散し、それぞれのサンドボックスで動きます。",
  hero_h1='すべての主要ベンダーのエージェント。<br>'
          '<span class="mark">ひとつのクライアント</span>、それぞれサンドボックス。',
  hero_sub="暗号化されたまま、自分のプライベート環境に分散して動きます。<br>"
           "<strong>アプリを閉じても、動き続けます。</strong>",
  nav=("特徴", "よくある質問", "サポート"),
  shot_alt="サイドバーに 7 つのエージェント接続、4 つのターミナルペインがそれぞれ別の "
           "coding CLI に接続している OpenAB Connect",
  soon_label="近日公開",
  feats=[
   ("主要ベンダーを網羅",
    "13 種類のエージェント CLI に、それぞれのイメージ — Claude Code、Codex、Cursor、"
    "Kiro、Gemini、Copilot など。セッションごとに選べます。<code>native</code> は"
    "エージェントを含みません。"),
   ("セッションはアプリより長生き",
    "シェルはコンテナの中で動きます。アプリを閉じても動き続け、次に開くと同じ分割"
    "レイアウトに戻り、出力は止まったバイト位置から続きます。"),
   ("外部には何も公開しない",
    "ポートを開けず、ingress も公開エンドポイントもありません。ネットワーク上の識別を"
    "持つのは Tailscale サイドカーだけで、ランタイムは loopback だけを listen します。"),
   ("Kubernetes でも ECS でも",
    "デプロイするのはごく普通の pod なので、準拠したクラスタなら何でも動きます — "
    "空いているマシンの k3s、EKS、GKE。あるいは AWS ECS Fargate なら、クラスタ自体を"
    "運用する必要がありません。"),
   ("ランタイムはオープンソース",
    f'MIT ライセンスで <a href="{PTY}">openabdev/openab-pty</a> にあります。'
    "何を動かすのかを先に確認できますし、公開された契約に沿って自分のクライアントも"
    "書けます。"),
   ("話しかけて動かす",
    "打ち込むだけでなく — openab を通じて、同じセッションをチャットや音声で動かせます。",
    True),
  ],
  faq_title="よくある質問",
  faq=[
   ("why-not-ssh", "<code>kubectl exec</code> や SSH と何が違うのですか?",
    "どちらもシェルは得られますが、生き残るセッションは得られません。"
    "<code>exec</code> の途中でターミナルを閉じれば、プロセスは接続と一緒に死にます。"
    "ここではセッションがコンテナの中で生きているので、アプリを閉じても閉じるのは "
    "WebSocket ひとつだけです。次の起動で出力が止まったバイト位置から接続し直し、"
    "同じ分割レイアウトを復元します。デプロイの形も違います。クライアントに kubeconfig "
    "は不要、port-forward も不要で、資格情報が許可するのはクラスタ全体ではなく"
    "セッション 1 つです。"),
   ("vs-herdr", "Herdr とは何が違うのですか?",
    "<p>Herdr はエージェントマルチプレクサ — コーディングエージェント版の tmux です。"
    "各エージェントに本物の PTY を与え、切断されても生かし続け、各ペインを working／"
    "blocked／idle に分類し、CLI と socket API を備えています。永続性と一覧性という点は、"
    "このアプリとほぼそのまま重なります。違うのはエージェントがどこで動くかです:"
    "</p><ul>"
    "<li><strong>Herdr</strong> は起動したマシンの上で動かすので、ユーザー、"
    "ファイルシステム、資格情報を共有します — つまり影響範囲はそのマシンと、"
    "あなたのアカウントが到達できるすべてです。永続するのは切断に対してで、"
    "ホストの電源が落ちることに対してではないため、ノート PC 上で動かしていれば"
    "閉じた時点ですべて終わります。（SSH リモートモードはこれを避けられますが、"
    "影響範囲がそのリモートホストに移ります。）</li>"
    "<li><strong>OpenAB Connect</strong> は各セッションをクラスタ内の独立したコンテナで"
    "動かします — <code>uid 1000</code>、<code>sudo</code> なし、ホストの資格情報なし、"
    "ルートは読み取り専用、ワークスペースは使い捨て — WireGuard の tailnet 経由で、"
    "ポートは一切開けません。</li>"
    "</ul>"
    "<p>違いはサンドボックス化であって、マルチプレクスではありません。Herdr にできて "
    "OpenAB Connect にできないこともあります。ペインの状態判定、スクリプト可能な"
    "ローカル API、そしてインフラを一切必要としない点です。何もデプロイしたくないなら、"
    "Herdr のほうが適した答えです。</p>"),
   ("vs-local", "自分の Mac で Claude Code や Codex Desktop を動かすのと何が違うのですか?",
    "Mac 上のエージェントは、あなたとして動きます。SSH 鍵、クラウドの資格情報、npm や "
    "GitHub のトークン、ディスク上のすべてのリポジトリに手が届くので、間違ったコマンドは"
    "あなたのマシンでの間違ったコマンドになります。こちらのシェルはそれらを一切持たず、"
    "ワークスペースはセッションとともに破棄され、複数のエージェントが同じ作業ツリーや"
    "同じポートを奪い合わずに同時に働けます。ノートを閉じてもスリープさせても、"
    "何も止まりません。"
    "代償は実在します。エージェントはローカルのファイルを見られないので作業は git 経由に"
    "なり、イメージの初回取得には数分かかり、クラスタか AWS アカウントが必要です。"
    "すでに開いているリポジトリを一行直すだけなら、ローカルで動かすほうが簡単で、"
    "これは何の足しにもなりません。"),
   ("what-can-the-shell-do", "このシェルはどこまでできるのですか?",
    "意図的にほとんど何もできません。<code>uid 1000</code> で開き、<code>sudo</code> "
    "なし、サービスアカウントトークンなし、ホストの資格情報なし、ルートファイルシステムは"
    "読み取り専用、ワークスペースは使い捨てです。セッションのシェルは loopback で"
    "ランタイムに到達できます。だからこそ管理用の資格情報はコンテナの中に置きません。"
    "アタッチトークンが許可するのは 1 セッションだけで、期限もあります。"),
   ("open-ports", "ポートを開けたり ingress を用意する必要はありますか?",
    "ありません。ランタイムは <code>127.0.0.1</code> にバインドし、TLS 鍵を持ちません。"
    "同じ pod の Tailscale サイドカーだけがネットワーク上の識別を持ち、両者は pod の"
    "ネットワーク名前空間の中で loopback を通して会話します。通信は WireGuard の "
    "tailnet を通って届き、暗号化はそこが担います。"),
   ("do-you-see-my-data", "そちらには何が届くのですか?",
    "何も届きません。ここにサービスはありません。アプリが接続する先はすべて、"
    "あなたが自分のクラスタか自分の AWS アカウントにデプロイしたものです。"
    "アカウント登録も、解析も、テレメトリもありません。入力した資格情報は macOS の"
    "キーチェーンに留まり、あなた自身のランタイム以外へは送信されません。"),
   ("inspect-first", "デプロイする前に中身を確認できますか?",
    f'できます。ランタイムは MIT ライセンスで <a href="{PTY}">openabdev/openab-pty</a> '
    f'にあり、<a href="{CONTRACT}">クライアント契約</a>も公開しているので、'
    "このアプリを使わずに自分のクライアントを書くこともできます。このアプリはその契約の"
    "一実装で、オープンソースではありません。"),
   ("try-without-cluster", "クラスタなしで試せますか?",
    "試せます。アプリメニューの <strong>Demo Mode</strong> は、サンプル接続 2 つと"
    "収録済みのターミナルだけで動き、ネットワーク接続は一切行いません。"
    "何もデプロイする前に評価できるようにするためのものです。"),
   ("what-deploy-does", "デプロイを押すと何が起きますか?",
    "3 クリックのあと、8 つの手順が走ります。資格情報を生成してキーチェーンに保存し、"
    "namespace を確認し、secret とボリュームを作成し、pod を適用し、起動を待ち、"
    "tailnet への参加を待ち、管理プレーンを検証します。マニフェストを書く必要は"
    "ありません。あるイメージの初回デプロイは、クラスタがそれを取得するため数分かかる"
    "ことがあります。"),
   ("teardown", "セッションを削除したあと、何か残りますか?",
    "<p><strong>ワークスペースは破棄されます。</strong>ここは確実です。そのセッションのため"
    "だけに存在し、セッションを削除すれば消えます。</p>"
    "<p>確実でないのはプロセスです。セッションを削除するとそのセッションのプロセスグループ"
    "は終了しますが、意図的にそのグループを離れたプロセス — <code>nohup</code> や "
    "<code>setsid</code> で起動したバックグラウンドジョブなど — は、pod や task が"
    "置き換わるまで生き残ることがあります。同じサンドボックスの中に閉じたままで、"
    "新たに何かへ手が届くわけではありませんが、その pod の CPU とメモリを使い続けます。</p>"
    "<p>そのためアプリでは、きれいに終了したとは言わず best-effort と明示しています。"
    "何も残らないことを確実にするなら、pod か task を削除してください。</p>"),
  ],
  f=("プライバシー", "サポート", "ランタイムのソース"),
 ),

 "ko": dict(
  dir="ko", base="/ko/", htmllang="ko", label="한국어",
  title="OpenAB Connect — 주요 벤더의 모든 에이전트를 클라이언트 하나로",
  desc="주요 벤더의 모든 에이전트를 클라이언트 하나로. 암호화된 채로 여러분의 사설 "
       "인프라에 분산되어 각자 샌드박스에서 실행됩니다.",
  hero_h1='주요 벤더의 모든 에이전트.<br>'
          '<span class="mark">클라이언트 하나</span>, 각자 샌드박스.',
  hero_sub="암호화된 채로 여러분의 사설 인프라에 분산되어 실행됩니다.<br>"
           "<strong>앱을 닫아도 계속 실행됩니다.</strong>",
  nav=("특징", "자주 묻는 질문", "지원"),
  shot_alt="사이드바에 에이전트 연결 7개, 서로 다른 coding CLI에 연결된 터미널 패널 4개가 "
           "열려 있는 OpenAB Connect",
  soon_label="출시 예정",
  feats=[
   ("주요 벤더를 모두",
    "에이전트 CLI 13종, 각각 별도의 이미지 — Claude Code, Codex, Cursor, Kiro, Gemini, "
    "Copilot 등. 세션마다 선택합니다. <code>native</code>는 에이전트를 포함하지 않습니다."),
   ("세션이 앱보다 오래 삽니다",
    "셸은 컨테이너 안에서 실행됩니다. 앱을 닫아도 계속 돌아가고, 다시 열면 같은 분할 "
    "레이아웃으로 돌아와 출력이 멈춘 바이트에서 이어집니다."),
   ("외부로 아무것도 열지 않습니다",
    "포트를 열지 않고 ingress도 공개 엔드포인트도 없습니다. 네트워크 신원을 가진 것은 "
    "Tailscale 사이드카뿐이며 런타임은 loopback만 수신합니다."),
   ("어떤 Kubernetes든, ECS든",
    "배포하는 것은 평범한 pod이므로 표준을 따르는 클러스터면 모두 동작합니다 — 남는 "
    "장비의 k3s, EKS, GKE. 또는 AWS ECS Fargate라면 운영할 클러스터 자체가 없습니다."),
   ("런타임은 오픈소스",
    f'MIT 라이선스로 <a href="{PTY}">openabdev/openab-pty</a>에 있습니다. 무엇을 '
    "실행할지 먼저 확인할 수 있고, 공개된 계약에 맞춰 자신의 클라이언트도 만들 수 있습니다."),
   ("말로도 됩니다",
    "타이핑만이 아니라 — openab을 통해 같은 세션을 채팅이나 음성으로 움직입니다.", True),
  ],
  faq_title="자주 묻는 질문",
  faq=[
   ("why-not-ssh", "<code>kubectl exec</code>이나 SSH와 무엇이 다릅니까?",
    "둘 다 셸은 주지만, 살아남는 세션은 주지 않습니다. <code>exec</code> 도중에 터미널을 "
    "닫으면 프로세스는 연결과 함께 죽습니다. 여기서는 세션이 컨테이너 안에 살아 있어서 "
    "앱을 닫는 것은 WebSocket 하나를 닫는 일에 그칩니다. 다음 실행에서 출력이 멈춘 "
    "바이트부터 다시 붙고 같은 분할 레이아웃을 복원합니다. 배포 방식도 다릅니다. "
    "클라이언트에 kubeconfig가 없고 port-forward도 없으며, 자격 증명이 허용하는 범위는 "
    "클러스터 전체가 아니라 세션 하나입니다."),
   ("vs-herdr", "Herdr와는 무엇이 다릅니까?",
    "<p>Herdr는 에이전트 멀티플렉서 — 코딩 에이전트를 위한 tmux입니다. 각 에이전트에 실제 "
    "PTY를 주고, 연결이 끊겨도 계속 살려 두며, 각 패널을 working／blocked／idle로 "
    "분류하고, CLI와 socket API를 제공합니다. 지속성과 전체 조망이라는 점은 이 앱과 거의 "
    "그대로 겹칩니다. 다른 것은 에이전트가 어디서 실행되는가입니다:"
    "</p><ul>"
    "<li><strong>Herdr</strong>는 실행한 그 머신 위에서 돌리므로 사용자, 파일시스템, "
    "자격 증명을 공유합니다 — 즉 영향 범위는 그 머신과 여러분 계정이 닿을 수 있는 모든 "
    "것입니다. 지속성은 연결 끊김에 대한 것이지 호스트 전원이 꺼지는 것에 대한 것이 "
    "아니므로, 노트북에서 돌린다면 덮는 순간 전부 끝납니다. (SSH 원격 모드는 이를 피할 "
    "수 있지만 영향 범위가 그 원격 호스트로 옮겨갑니다.)</li>"
    "<li><strong>OpenAB Connect</strong>는 각 세션을 클러스터 안의 독립된 컨테이너에서 "
    "실행합니다 — <code>uid 1000</code>, <code>sudo</code> 없음, 호스트 자격 증명 없음, "
    "루트는 읽기 전용, 워크스페이스는 일회용 — WireGuard tailnet으로 닿고 포트는 전혀 "
    "열지 않습니다.</li>"
    "</ul>"
    "<p>차이는 샌드박싱이며 멀티플렉싱이 아닙니다. Herdr가 할 수 있고 OpenAB Connect가 "
    "못 하는 일도 있습니다. 패널 상태 판정, 스크립트 가능한 로컬 API, 그리고 인프라가 전혀 "
    "필요 없다는 점입니다. 아무것도 배포하고 싶지 않다면 Herdr가 더 나은 답입니다.</p>"),
   ("vs-local", "제 Mac에서 Claude Code나 Codex Desktop을 그냥 쓰는 것과 무엇이 다릅니까?",
    "Mac 위의 에이전트는 여러분 자신으로 실행됩니다. SSH 키, 클라우드 자격 증명, npm과 "
    "GitHub 토큰, 디스크의 모든 리포지터리에 닿을 수 있으므로 잘못된 명령은 여러분의 "
    "기계에서의 잘못된 명령이 됩니다. 이쪽 셸은 그런 것을 하나도 갖지 않고, 워크스페이스는 "
    "세션과 함께 버려지며, 여러 에이전트가 같은 작업 트리나 같은 포트를 두고 다투지 않고 "
    "동시에 일할 수 있습니다. 노트북을 닫거나 잠자기로 두어도 아무것도 멈추지 않습니다."
    "대가는 실재합니다. 에이전트는 로컬 파일을 볼 수 없어 작업은 git으로 오가고, 이미지의 "
    "첫 내려받기는 몇 분이 걸리며, 클러스터나 AWS 계정이 필요합니다. 이미 열어 둔 "
    "리포지터리에서 한 줄 고치는 정도라면 로컬 실행이 더 간단하고 이것은 아무 도움이 "
    "되지 않습니다."),
   ("what-can-the-shell-do", "이 셸은 실제로 무엇을 할 수 있습니까?",
    "의도적으로 거의 못 합니다. <code>uid 1000</code>으로 열리며 <code>sudo</code>도, "
    "서비스 어카운트 토큰도, 호스트 자격 증명도 없습니다. 루트 파일시스템은 읽기 전용이고 "
    "워크스페이스는 일회용입니다. 세션 셸은 loopback으로 런타임에 닿을 수 있는데, 바로 "
    "그래서 관리 자격 증명은 컨테이너 안에 두지 않습니다. 어태치 토큰은 세션 하나만 "
    "허용하고 만료됩니다."),
   ("open-ports", "포트를 열거나 ingress를 설정해야 합니까?",
    "아닙니다. 런타임은 <code>127.0.0.1</code>에 바인드하고 TLS 키를 갖지 않습니다. 같은 "
    "pod의 Tailscale 사이드카만 네트워크 신원을 가지며, 둘은 pod의 네트워크 네임스페이스 "
    "안에서 loopback으로 통신합니다. 트래픽은 WireGuard tailnet을 통해 도달하고 암호화는 "
    "그쪽이 담당합니다."),
   ("do-you-see-my-data", "그쪽에는 무엇이 전달됩니까?",
    "아무것도 전달되지 않습니다. 여기에 서비스가 없습니다. 앱이 연결하는 서버는 모두 "
    "여러분이 자신의 클러스터나 자신의 AWS 계정에 배포한 것입니다. 계정도, 가입도, "
    "분석도, 텔레메트리도 없습니다. 입력한 자격 증명은 macOS 키체인에 남고 여러분 자신의 "
    "런타임 외에는 어디로도 전송되지 않습니다."),
   ("inspect-first", "배포하기 전에 무엇을 배포하는지 확인할 수 있습니까?",
    f'가능합니다. 런타임은 MIT 라이선스로 <a href="{PTY}">openabdev/openab-pty</a>에 있고 '
    f'<a href="{CONTRACT}">클라이언트 계약</a>도 공개되어 있어, 이 앱을 쓰지 않고 자신의 '
    "클라이언트를 만들 수도 있습니다. 이 앱은 그 계약의 한 구현이며 오픈소스가 아닙니다."),
   ("try-without-cluster", "클러스터 없이 사용해 볼 수 있습니까?",
    "가능합니다. 앱 메뉴의 <strong>Demo Mode</strong>는 샘플 연결 두 개와 미리 녹화된 "
    "터미널만으로 동작하며 어떤 네트워크 연결도 하지 않습니다. 아무것도 배포하기 전에 앱을 "
    "평가할 수 있도록 넣었습니다."),
   ("what-deploy-does", "배포를 누르면 무슨 일이 일어납니까?",
    "세 번의 클릭 뒤에 여덟 단계가 진행됩니다. 자격 증명을 만들어 키체인에 저장하고, "
    "namespace를 확인하고, secret과 볼륨을 만들고, pod을 적용한 뒤, 실행을 기다리고, "
    "tailnet 참여를 기다리고, 관리 평면을 검증합니다. 매니페스트를 쓸 필요가 없습니다. "
    "어떤 이미지의 첫 배포는 클러스터가 이미지를 받아오는 동안 몇 분이 걸릴 수 있습니다."),
   ("teardown", "세션을 삭제한 뒤에 남는 것이 있습니까?",
    "<p><strong>워크스페이스는 버려집니다.</strong> 이 부분은 확실합니다. 그 세션을 위해서만 "
    "존재하며, 세션을 삭제하면 함께 사라집니다.</p>"
    "<p>확실하지 않은 것은 프로세스입니다. 세션을 삭제하면 해당 세션의 프로세스 그룹이 "
    "종료되지만, 그 그룹을 의도적으로 벗어난 프로세스 — <code>nohup</code>이나 "
    "<code>setsid</code>로 띄운 백그라운드 작업 — 는 pod이나 task가 교체될 때까지 살아남을 "
    "수 있습니다. 여전히 같은 샌드박스 안에 갇혀 있어 새로 닿을 수 있는 것은 없지만, 그 pod의 "
    "CPU와 메모리를 계속 씁니다.</p>"
    "<p>그래서 앱에서는 깔끔하게 종료된다고 말하지 않고 best-effort라고 밝힙니다. 아무것도 "
    "남지 않게 하려면 pod이나 task를 삭제하십시오.</p>"),
  ],
  f=("개인정보", "지원", "런타임 소스"),
 ),
}


def switcher(current):
    out = []
    for c in ORDER:
        cls = ' class="active"' if c == current else ""
        out.append('<a' + cls + ' href="' + L[c]["base"] + '">' + L[c]["label"] + '</a>')
    return "|".join(out)


def alternates():
    rows = [f'<link rel="alternate" hreflang="{L[c]["htmllang"]}" '
            f'href="https://connect.openab.dev{L[c]["base"]}">' for c in ORDER]
    # x-default is what a search engine serves when it matches no listed language.
    rows.append('<link rel="alternate" hreflang="x-default" href="https://connect.openab.dev/">')
    return "\n".join(rows)


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
    <a href="#features">{nav0}</a>
    <a href="#faq">{nav1}</a>
    <a href="/support.html">{nav2}</a>
    <span class="lang">{switcher}</span>
  </div>
</nav>

<header>
  <img class="appicon" src="/icon.png" alt="OpenAB Connect">
  <h1>{hero_h1}</h1>
  <p class="tag">{hero_sub}</p>
</header>

<div class="shotwrap">
<figure><img src="/screenshot.png" alt="{shot_alt}"></figure>
</div>

<section class="features" id="features">
<div class="features-grid">
{features}
</div>
</section>

<section class="faq" id="faq">
<h2>{faq_title}</h2>
{faqs}
</section>

<footer>
  <a href="/privacy.html">{f0}</a>
  <a href="/support.html">{f1}</a>
  <a href="{pty}">{f2}</a>
  <span class="dim">© 2026 openabdev</span>
</footer>

<script>
// Give every question a copyable anchor, so an answer can be linked to directly
// rather than described. Added in script because the markup should stay readable.
(function () {{
  var items = document.querySelectorAll(".faq details[id]");
  Array.prototype.forEach.call(items, function (d) {{
    var a = document.createElement("a");
    a.className = "faq-anchor";
    a.href = "#" + d.id;
    a.textContent = "#";
    a.setAttribute("aria-label", "Link to this question");
    d.querySelector("summary").appendChild(a);
  }});
  // A linked question should already be open when it is arrived at. Looked up by id
  // rather than built into a selector: location.hash needs escaping to be a valid
  // selector, and getElementById needs none.
  if (location.hash) {{
    var t = document.getElementById(location.hash.slice(1));
    if (t && t.tagName === "DETAILS") {{ t.open = true; }}
  }}
}})();
</script>

</body>
</html>
"""

for code in ORDER:
    d = L[code]
    cards = []
    for i, item in enumerate(d["feats"]):
        soon = len(item) > 2 and item[2]
        ribbon = f'    <span class="ribbon">{d["soon_label"]}</span>\n' if soon else ""
        cards.append(f'  <div class="feature{" soon" if soon else ""}">\n{ribbon}'
                     f'    <div class="icon"><svg viewBox="0 0 24 24">{ICONS[i]}</svg></div>\n'
                     f'    <h3>{item[0]}</h3>\n    <p>{item[1]}</p>\n  </div>')
    entries = []
    for qid, q, a in d["faq"]:
        body = a if "<ul>" in a or "<p>" in a else f"<p>{a}</p>"
        entries.append(f'<details id="faq-{qid}">\n  <summary><span class="q">{q}</span>'
                       f'</summary>\n  <div class="a">{body}</div>\n</details>')
    faqs = "\n".join(entries)

    out = ROOT / d["dir"] / "index.html" if d["dir"] else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE.format(
        code=code, alternates=alternates(), switcher=switcher(code),
        features="\n".join(cards), faqs=faqs, pty=PTY,
        nav0=d["nav"][0], nav1=d["nav"][1], nav2=d["nav"][2],
        f0=d["f"][0], f1=d["f"][1], f2=d["f"][2],
        **{k: v for k, v in d.items()
           if k not in ("nav", "f", "feats", "faq", "soon_label", "dir", "label")}),
        encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)}  ({len(cards)} cards, {len(d['faq'])} questions)")
