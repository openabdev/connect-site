#!/usr/bin/env python3
"""Dev notes, four languages each.

    python3 scripts/build_notes.py

Same shape as build_docs.py: structure lives here once, languages are data.
English lives at /notes/<slug>/, the others at /zh/notes/<slug>/ etc., which is
what chrome.head/alternates/switcher already produce when handed the filename
"notes/<slug>/". A per-language notes index sits at /notes/ (and /zh/notes/ …).

Not translated line by line. The note argues one thesis — three products on one
trust spectrum — and each language carries that argument the way it says it.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chrome

ROOT = chrome.ROOT
SITE = chrome.SITE

SLUG = "terminal-trust-spectrum"
DATE_ISO = "2026-08-30"

HERDR = "https://github.com/ogulcancelik/herdr"
SL = "https://superlogical.com/"
SL_POST = "https://mitchellh.com/writing/superlogical"
PTY = chrome.PTY

# Column heads are product names, identical in every language.
COLS = ("Herdr", "Superlogical", "OpenAB Connect")


def table(rows):
    """The comparison table. Dimension per row, both sides named, so a reader
    draws the conclusion line by line instead of being handed a verdict —
    except in the last two rows, which are the verdict, on purpose."""
    out = ['<div class="tablewrap"><table class="cmp">',
           "<thead><tr><th></th>" +
           "".join(f"<th>{c}</th>" for c in COLS) + "</tr></thead>", "<tbody>"]
    for label, a, b, c in rows:
        out.append(f"<tr><th>{label}</th><td>{a}</td><td>{b}</td><td>{c}</td></tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


# N[lang] = dict(title, desc, og_alt, date, notes_label, notes_lede, lede,
#                rows, body)  — body is HTML with {table} left to format in.
N = {}

N["zh"] = dict(
 title="Hashimoto 的 Superlogical、Herdr、與我們：終端信任光譜的三個賭注",
 desc="Hashimoto 的 Superlogical、本機端的 Herdr、我們的 OpenAB Connect——三個終端產品"
      "在同一條信任光譜上押了三個不同的賭注。一張表格橫向對比。",
 og_alt="Herdr、Superlogical、OpenAB Connect——終端信任光譜的三個賭注",
 date="2026 年 8 月 30 日",
 notes_label="開發筆記",
 notes_lede="關於 OpenAB Connect 的設計取捨，以及它所在的市場。",
 lede="2026 年 7 月底，HashiCorp 共同創辦人、Ghostty 作者 Mitchell Hashimoto "
      f'<a href="{SL_POST}">宣布成立新公司 Superlogical</a>，第一個產品是 server-side '
      "terminal multiplexer。同一個夏天，Herdr 在本機終端這一端快速竄紅，我們的 "
      "OpenAB Connect 則在另一端上線。三個產品都在回答同一個問題——當 AI agent 成為"
      "終端的常駐使用者，session 應該住在哪裡、又該被信任到什麼程度？——而它們押了"
      "三個不同的答案。",
 rows=[
  ("Session 住在哪",
   "本機 daemon（另有 SSH remote mode）",
   "server-side daemon，目標橫跨本機／遠端／production",
   "遠端沙箱容器（k8s pod／ECS task）"),
  ("信任假設",
   "完全信任——以你的身份跑你的 process",
   "尚未公布——auth、權限分離、audit 均待定",
   "零信任——假設 session 內容不可信"),
  ("隔離",
   "無（保留你的環境正是賣點）",
   "無（daemon 直接持有你的權限）",
   "uid 1000、無 sudo、read-only rootfs、無 SA token"),
  ("憑證模型",
   "無（本機 socket API）",
   "未公布",
   "第一天就有：管理面／連線面分離，per-session token 有 TTL、不帶 signing key"),
  ("Agent 狀態語意",
   "一等物件：blocked／working／done，socket API 供 agent 互相編排",
   "規劃中（三階段願景的第三階）",
   "無——刻意不碰，agent 語意屬於 openab 本體"),
  ("斷線重連",
   "跨斷線存活（非跨主機關機）",
   "畫面快照＋raw stream 續流，含完整終端狀態",
   "ring buffer 重播，狀態語意較薄"),
  ("感知延遲",
   "本機，無此問題",
   "client 端 libghostty 自行 render，設計上與 server 脫鉤（未量測）",
   "由 client 決定；runtime 自測 1.0 ms，WiFi 筆電 78–82 ms"),
  ("成熟度",
   "已可用，開源",
   "pre-beta，僅 waitlist，無 benchmark、無規格",
   "Phase 1，已在 k3s 與 ECS Fargate 上實際使用"),
  ("它押的是", "編排", "持久", "信任"),
  ("它放掉的是", "隔離與跨主機持久", "信任模型（目前）", "環境自由度與終端狀態語意"),
 ],
 body=f"""
<h2>一條光譜，兩條軸</h2>
<p>用「session 住在哪」排序：<a href="{HERDR}">Herdr</a> 在你的終端裡；<a href="{SL}">Superlogical</a>
在一個跨環境的 server-side daemon；OpenAB Connect 在 WireGuard tailnet 之後的遠端沙箱容器。
換用「信任假設」排序，順序一模一樣：Herdr 完全信任（session 裡的就是你）；Superlogical 的信任模型
尚未公布；OpenAB Connect 從第一天就假設 session 內容不可信。兩條軸給出同一條光譜——Herdr 和
OpenAB Connect 站在兩個極端，Superlogical 剛好在中間。</p>
<figure class="cmp-shot">
  <img src="{chrome.rev("notes/terminal-trust-spectrum/session-architecture-comparison.png")}"
       width="2560" height="1600"
       alt="三種 Session 架構的十維度對照圖：Herdr 是本機 daemon，完全信任、零隔離，押注編排；Superlogical 是 server-side daemon，信任模型尚未公布，押注持久；OpenAB Connect 是遠端沙箱容器，零信任、day 1 憑證模型，押注信任">
</figure>
<h2>Herdr：編排做到極致，隔離為零</h2>
<p>Herdr 是跑在你現有終端裡的 agent multiplexer（Rust + Ratatui，開源）。它把 agent 當成 runtime
的一等物件：sidebar 即時顯示每個 agent 是 blocked、working 還是 done；socket API 讓 agent 自己
spawn pane、讀取彼此的輸出、互相等待。session 在 daemon 裡跨斷線存活——但不跨主機關機——另有
SSH remote mode 可以管到遠端主機。</p>
<p>一切以你的身份、在你的機器上跑。隔離為零是它的賣點而不是缺陷：保留你的 shell、SSH 設定、字型和
keybinds。它賭的是<strong>編排</strong>：agent 狀態的即時可見性，是多 agent 時代最值錢的東西。</p>
<h2>Superlogical：持久做到極致，信任留白</h2>
<p>Superlogical 把 session 從終端抽出來，放進 server-side daemon。daemon 持有 PTY，用 libghostty
把輸出 parse 成 authoritative state，同時把同一份 raw bytes 原樣分發給每個 client——client 內建
同一套 libghostty，自己 parse、自己 render。重連時 daemon 暫停 PTY、送出畫面快照，client 就緒後
續流 raw bytes。願景是橫跨本機、遠端主機、沙箱與 production 的「multiplexer for all work」。</p>
<p>它賭的是<strong>持久</strong>：session 本身作為一個獨立於任何 client 的持久層，是最值錢的抽象——
這跟當年 Terraform 賭 state 層是同一種賭法。但要把現況說清楚：截至本文寫作，它只有 waitlist，沒有
benchmark、沒有協定規格，而 auth、權限分離、audit 這些 production 的必需品，一項都尚未公布。
持久性被推到最遠，信任整個留白。</p>
<h2>OpenAB Connect：信任做到極致，環境被規定死</h2>
<p>我們押相反的一端。Connect 連上的 shell 住在一個刻意無權限的容器裡：uid 1000、沒有 sudo、
read-only rootfs、沒有 service-account token，workspace 是暫時的。憑證模型從第一天就在：管理面與
連線面分離，per-session token 有 TTL、不帶 signing key——一個被入侵的 shell 就算從 loopback 打
管理 API，拿到的也只是 401，這是對抗測試裡明確驗證的不變量。整條路徑走 WireGuard tailnet，runtime
從不監聽可路由位址（<a href="{PTY}">runtime 是 MIT 開源</a>）。</p>
<p>我們賭的是<strong>信任</strong>：agent 會失控、shell 會被騙，所以環境必須假設其中的東西不可信。
代價也直說：環境被規定死，而 raw byte pipe 的架構讓感知延遲幾乎全由 client 決定——runtime 在自己
主機上量到 1.0 ms 的 echo latency，從 WiFi 筆電量到 78–82 ms。Superlogical 那套 client 端 state
rendering，正面解的就是我們自己在 README 裡承認的最大缺口。</p>
<h2>三個賭注，三層問題</h2>
<p>有意思的是三者並不互斥：Herdr 式的 agent 狀態介面，跑在 Superlogical 式的持久 session 上，而
session 住在 OpenAB 式的沙箱裡——編排、持久、信任，各解一層。現在只是三個產品各自從光譜的一端
往中間長。</p>
<p>站在中間也意味著兩頭夾擊：本機編排的即時性比不過 Herdr，零信任沙箱的安全模型還沒亮出來。
Hashimoto 賭的是 durable session 層本身贏者全拿；我們賭的是，在 agent 真正被放出去亂跑的那天，
大家最先問的是——它能碰到什麼。</p>
""",
)

N["en"] = dict(
 title="Hashimoto's Superlogical, Herdr, and us: three bets on the terminal trust spectrum",
 desc="Hashimoto's Superlogical, Herdr at the local end, our OpenAB Connect at the other — "
      "three terminal products placing three different bets on one trust spectrum. "
      "With a side-by-side table.",
 og_alt="Herdr, Superlogical, OpenAB Connect — three bets on the terminal trust spectrum",
 date="30 August 2026",
 notes_label="Dev notes",
 notes_lede="Design trade-offs behind OpenAB Connect, and the market it sits in.",
 lede="In late July 2026, Mitchell Hashimoto — HashiCorp co-founder and the author of "
      f'Ghostty — <a href="{SL_POST}">announced his new company, Superlogical</a>, whose '
      "first product is a server-side terminal multiplexer. The same summer, Herdr was "
      "gathering momentum at the local end of the terminal, and our OpenAB Connect "
      "shipped at the other. All three answer the same question — when AI agents become "
      "permanent residents of the terminal, where should a session live, and how far "
      "should it be trusted? — and each placed a different bet.",
 rows=[
  ("Where the session lives",
   "a local daemon (plus an SSH remote mode)",
   "a server-side daemon, aiming to span local, remote and production",
   "a remote sandboxed container (k8s pod or ECS task)"),
  ("Trust assumption",
   "full trust — runs your processes as you",
   "unpublished — auth, permission separation and audit all pending",
   "zero trust — assumes what is inside cannot be trusted"),
  ("Isolation",
   "none (keeping your environment is the point)",
   "none (the daemon holds your privileges)",
   "uid 1000, no sudo, read-only rootfs, no SA token"),
  ("Credential model",
   "none (a local socket API)",
   "unannounced",
   "day one: admin and attach planes split; per-session tokens with a TTL and no signing key"),
  ("Agent state semantics",
   "first-class: blocked / working / done, and a socket API for agents to orchestrate each other",
   "planned (stage three of the vision)",
   "none — deliberately out of scope; agent semantics belong to openab"),
  ("Reconnect",
   "survives disconnects (not the host powering off)",
   "screen snapshot, then the raw stream resumes — full terminal state",
   "ring-buffer replay; thinner state semantics"),
  ("Perceived latency",
   "local, so not a question",
   "each client renders with embedded libghostty, decoupled from the server by design (unmeasured)",
   "set by the client; the runtime measures 1.0 ms, 78–82 ms from a laptop over WiFi"),
  ("Maturity",
   "usable today, open source",
   "pre-beta: a waitlist, no benchmarks, no spec",
   "Phase 1, in real use on k3s and ECS Fargate"),
  ("Its bet", "orchestration", "durability", "trust"),
  ("What it gives up",
   "isolation, and persistence beyond the host",
   "the trust model (for now)",
   "environment freedom, and terminal state semantics"),
 ],
 body=f"""
<h2>One spectrum, two axes</h2>
<p>Sort by where the session lives: <a href="{HERDR}">Herdr</a> is inside your terminal;
<a href="{SL}">Superlogical</a> is a server-side daemon meant to span environments; OpenAB
Connect is a remote sandboxed container behind a WireGuard tailnet. Sort by trust assumption
instead and the order does not change: Herdr trusts the session fully (it is you); Superlogical
has not published a trust model; OpenAB Connect assumes from day one that what is inside cannot
be trusted. Two axes, one spectrum — Herdr and OpenAB Connect at the two ends, Superlogical in
the middle.</p>
{{table}}
<h2>Herdr: orchestration at full depth, zero isolation</h2>
<p>Herdr is an agent multiplexer that runs inside your existing terminal (Rust + Ratatui, open
source). Agents are first-class runtime objects: a sidebar shows each one as blocked, working
or done; a socket API lets agents spawn panes, read each other's output and wait on one
another. Sessions survive disconnects in a daemon — though not the host powering off — and an
SSH remote mode reaches other machines.</p>
<p>Everything runs as you, on your machine. Zero isolation is the selling point, not a defect:
you keep your shell, your SSH setup, your fonts and keybinds. Its bet is
<strong>orchestration</strong>: real-time visibility of agent state is the most valuable thing
in a multi-agent world.</p>
<h2>Superlogical: durability at full depth, trust left blank</h2>
<p>Superlogical pulls the session out of the terminal and into a server-side daemon. The daemon
owns the PTY and parses its output into authoritative state with libghostty, while distributing
the same raw bytes to every client — each client embeds the same libghostty and parses and
renders on its own. On reconnect the daemon pauses the PTY, ships a snapshot of the screen, and
resumes the raw stream once the client signals ready. The vision is a “multiplexer for all
work” spanning local machines, remote hosts, sandboxes and production.</p>
<p>Its bet is <strong>durability</strong>: the session itself, as a layer independent of any
client, is the most valuable abstraction — the same kind of bet Terraform placed on the state
layer. To be plain about what exists: as of this writing there is a waitlist, no benchmark, no
protocol spec, and auth, permission separation and audit — the things production requires —
are all unannounced. Durability is pushed as far as it goes; trust is left blank.</p>
<h2>OpenAB Connect: trust at full depth, the environment pinned down</h2>
<p>We bet on the opposite end. The shell Connect attaches to lives in a deliberately
unprivileged container: uid 1000, no sudo, a read-only rootfs, no service-account token, and a
workspace that is discarded with the session. The credential model is there from day one: the
admin plane and the attach plane are separate, and per-session tokens carry a TTL and no
signing key — a compromised shell hitting the admin API over loopback gets a 401, an invariant
the adversary test asserts explicitly. The whole path runs over a WireGuard tailnet, and the
runtime never listens on a routable address (<a href="{PTY}">the runtime is MIT-licensed open
source</a>).</p>
<p>Our bet is <strong>trust</strong>: agents will run away and shells will be tricked, so the
environment must assume what is inside is hostile. The costs are stated too: the environment is
pinned down, and a raw byte pipe leaves perceived latency almost entirely to the client — the
runtime measures 1.0 ms of echo latency from its own host, against 78–82 ms from a laptop over
WiFi. Superlogical's client-side state rendering attacks exactly the gap our README names as
our largest.</p>
<h2>Three bets, three layers</h2>
<p>The interesting part is that the three do not exclude each other: a Herdr-style agent-state
interface, on a Superlogical-style durable session, living in an OpenAB-style sandbox —
orchestration, durability and trust each solve one layer. For now, three products are growing
toward the middle from their own ends.</p>
<p>The middle also means being squeezed from both sides: for local orchestration it will not
match Herdr's immediacy, and its zero-trust story is not yet on the table. Hashimoto is betting
the durable-session layer wins outright. We are betting that on the day agents are truly let
loose, the first question anyone asks is — what can it reach?</p>
""",
)

N["ja"] = dict(
 title="Hashimoto の Superlogical、Herdr、そして私たち——ターミナル信頼スペクトラム、三つの賭け",
 desc="Hashimoto の Superlogical、ローカル側の Herdr、反対側の OpenAB Connect——三つの"
      "ターミナルプロダクトが、同じ信頼スペクトラムの上で三つの異なる賭けをしている。"
      "横並びの比較表つき。",
 og_alt="Herdr・Superlogical・OpenAB Connect——ターミナル信頼スペクトラム、三つの賭け",
 date="2026年8月30日",
 notes_label="開発ノート",
 notes_lede="OpenAB Connect の設計上のトレードオフと、それが立つ市場について。",
 lede="2026 年 7 月末、HashiCorp 共同創業者で Ghostty の作者でもある Mitchell Hashimoto が"
      f'<a href="{SL_POST}">新会社 Superlogical の設立を発表した</a>。最初のプロダクトは '
      "server-side のターミナルマルチプレクサだ。同じ夏、ローカルターミナルの側では Herdr "
      "が勢いを増し、私たちの OpenAB Connect は反対側でリリースされた。三つとも同じ問いに"
      "答えている——AI エージェントがターミナルの常駐者になったとき、セッションはどこに住み、"
      "どこまで信頼されるべきか？——そして、それぞれ違う答えに賭けた。",
 rows=[
  ("セッションの住処",
   "ローカルの daemon（SSH リモートモードあり）",
   "server-side の daemon。ローカル／リモート／production を横断する構想",
   "リモートのサンドボックスコンテナ（k8s pod／ECS task）"),
  ("信頼の前提",
   "全面的に信頼——あなたの身分であなたのプロセスを実行",
   "未公表——認証・権限分離・監査はすべて未定",
   "ゼロトラスト——中身を信頼しない前提"),
  ("隔離",
   "なし（あなたの環境をそのまま保つことが売り）",
   "なし（daemon があなたの権限をそのまま持つ）",
   "uid 1000、sudo なし、read-only rootfs、SA トークンなし"),
  ("クレデンシャルモデル",
   "なし（ローカルの socket API）",
   "未発表",
   "初日から：管理面と接続面を分離。セッション毎トークンは TTL 付き、署名鍵なし"),
  ("エージェント状態のセマンティクス",
   "一級市民：blocked／working／done、socket API でエージェント同士が編成",
   "構想段階（三段階ビジョンの第三段）",
   "なし——意図的に扱わない。エージェントのセマンティクスは openab 本体の領分"),
  ("再接続",
   "切断をまたいで存続（ホストの電源断はまたがない）",
   "画面スナップショット＋raw stream の続行。完全な端末状態",
   "リングバッファの再生。状態のセマンティクスは薄い"),
  ("体感レイテンシ",
   "ローカルなので問題にならない",
   "クライアント内蔵の libghostty が自前で描画し、設計上サーバーと分離（未計測）",
   "クライアント次第。runtime 自測 1.0 ms、WiFi のラップトップから 78–82 ms"),
  ("成熟度",
   "現在利用可能、オープンソース",
   "pre-beta。waitlist のみ、ベンチマークも仕様もなし",
   "Phase 1。k3s と ECS Fargate で実運用中"),
  ("賭けているもの", "オーケストレーション", "永続性", "信頼"),
  ("手放しているもの",
   "隔離と、ホストを越えた永続性",
   "信頼モデル（今のところ）",
   "環境の自由度と、端末状態のセマンティクス"),
 ],
 body=f"""
<h2>一本のスペクトラム、二本の軸</h2>
<p>「セッションがどこに住むか」で並べると、<a href="{HERDR}">Herdr</a> はあなたのターミナルの中、
<a href="{SL}">Superlogical</a> は環境を横断する server-side の daemon、OpenAB Connect は
WireGuard tailnet の向こうのリモートのサンドボックスコンテナになる。「信頼の前提」で並べ直しても
順序は変わらない。Herdr はセッションを全面的に信頼し（中身はあなた自身だ）、Superlogical は信頼
モデルを未公表のままにし、OpenAB Connect は初日から中身を信頼しない前提に立つ。二本の軸が同じ
一本のスペクトラムを描く——Herdr と OpenAB Connect が両極、Superlogical がちょうど中間だ。</p>
{{table}}
<h2>Herdr——オーケストレーションを極め、隔離はゼロ</h2>
<p>Herdr は、いま使っているターミナルの中で動くエージェントマルチプレクサだ（Rust + Ratatui、
オープンソース）。エージェントはランタイムの一級市民で、サイドバーには各エージェントが blocked か
working か done かがリアルタイムに並ぶ。socket API を通じて、エージェント自身が pane を開き、
互いの出力を読み、互いを待てる。セッションは daemon の中で切断をまたいで生き続けるが、ホストの
電源断はまたがない。SSH リモートモードで他のマシンにも届く。</p>
<p>すべてはあなたの身分で、あなたのマシンの上で動く。隔離ゼロは欠陥ではなく売りだ——シェルも
SSH 設定もフォントもキーバインドも、そのまま使える。Herdr の賭けは<strong>オーケストレーション</strong>：
マルチエージェント時代に一番価値があるのは、エージェント状態のリアルタイムな可視性だという賭けだ。</p>
<h2>Superlogical——永続性を極め、信頼は空欄</h2>
<p>Superlogical はセッションをターミナルから引き剥がし、server-side の daemon に移す。daemon が
PTY を持ち、libghostty で出力を権威ある状態（authoritative state）にパースしながら、同じ raw bytes
をそのまま各クライアントに配る。クライアントは同じ libghostty を内蔵し、自分でパースし自分で描画
する。再接続時は daemon が PTY を一時停止して画面のスナップショットを送り、クライアントの準備が
できてから raw stream を再開する。構想は、ローカルもリモートもサンドボックスも production も横断
する「multiplexer for all work」だ。</p>
<p>Superlogical の賭けは<strong>永続性</strong>：どのクライアントからも独立したセッションという
持続層こそ、いちばん価値のある抽象だという賭けだ——かつて Terraform が state 層に賭けたのと同じ
種類の賭けである。ただし現状は正確に言っておく。本稿の時点であるのは waitlist だけで、ベンチマーク
も、プロトコル仕様もない。そして認証・権限分離・監査という production の必需品は、一つも発表されて
いない。永続性は極限まで押し込み、信頼はまるごと空欄だ。</p>
<h2>OpenAB Connect——信頼を極め、環境は固定</h2>
<p>私たちは反対側の極に賭けた。Connect がつなぐシェルは、意図的に無権限にしたコンテナに住む。
uid 1000、sudo なし、read-only rootfs、service-account トークンなし、ワークスペースはセッションと
ともに破棄される。クレデンシャルモデルは初日からある。管理面と接続面は分離され、セッション毎の
トークンは TTL 付きで署名鍵を持たない——乗っ取られたシェルが loopback から管理 API を叩いても
返るのは 401 で、これは敵対テストが明示的に検証している不変条件だ。経路全体は WireGuard tailnet
の上を通り、runtime はルーティング可能なアドレスでは決して待ち受けない
（<a href="{PTY}">runtime は MIT ライセンスのオープンソース</a>）。</p>
<p>私たちの賭けは<strong>信頼</strong>：エージェントは暴走するし、シェルは騙される。だから環境は、
中身を信頼できないものとして扱わなければならない、という賭けだ。コストも率直に言う。環境は固定され、
raw byte pipe のアーキテクチャでは体感レイテンシがほぼクライアント側で決まる——runtime は自分の
ホストからのエコーレイテンシを 1.0 ms、WiFi のラップトップからは 78–82 ms と計測している。
Superlogical のクライアント側 state rendering が正面から解こうとしているのは、まさに私たちが README
で最大のギャップだと認めている部分だ。</p>
<h2>三つの賭け、三つの層</h2>
<p>面白いのは、三つが互いを排除しないことだ。Herdr 式のエージェント状態インターフェースが、
Superlogical 式の永続セッションの上で動き、そのセッションが OpenAB 式のサンドボックスに住む——
オーケストレーション、永続性、信頼は、それぞれ別の層を解いている。いまは三つのプロダクトが、
それぞれの端から中間に向かって伸びている途中にすぎない。</p>
<p>中間に立つことは、両側から挟まれることでもある。ローカルの編成では Herdr の即時性に敵わず、
ゼロトラストのサンドボックスについては安全モデルがまだ卓上にない。Hashimoto は durable session
という層そのものが総取りすると賭けている。私たちは、エージェントが本当に野に放たれた日に、
誰もが最初に問うのは——それは何に届くのか？——だと賭けている。</p>
""",
)

N["ko"] = dict(
 title="Hashimoto의 Superlogical, Herdr, 그리고 우리 — 터미널 신뢰 스펙트럼의 세 가지 베팅",
 desc="Hashimoto의 Superlogical, 로컬 쪽의 Herdr, 반대쪽 끝의 OpenAB Connect — 세 터미널 "
      "제품이 같은 신뢰 스펙트럼 위에서 서로 다른 베팅을 하고 있습니다. 나란히 비교한 표와 함께.",
 og_alt="Herdr · Superlogical · OpenAB Connect — 터미널 신뢰 스펙트럼의 세 가지 베팅",
 date="2026년 8월 30일",
 notes_label="개발 노트",
 notes_lede="OpenAB Connect의 설계 트레이드오프, 그리고 이 제품이 서 있는 시장에 대하여.",
 lede="2026년 7월 말, HashiCorp 공동 창업자이자 Ghostty의 작자인 Mitchell Hashimoto가 "
      f'<a href="{SL_POST}">새 회사 Superlogical의 설립을 발표했습니다</a>. 첫 제품은 '
      "server-side 터미널 멀티플렉서입니다. 같은 여름, 로컬 터미널 쪽에서는 Herdr가 "
      "빠르게 주목받았고, 우리의 OpenAB Connect는 반대쪽 끝에서 출시되었습니다. 셋 다 "
      "같은 질문에 답하고 있습니다 — AI 에이전트가 터미널의 상주자가 될 때, 세션은 어디에 "
      "살아야 하고 어디까지 신뢰받아야 하는가? — 그리고 각자 다른 답에 베팅했습니다.",
 rows=[
  ("세션이 사는 곳",
   "로컬 데몬(SSH 원격 모드 있음)",
   "서버 사이드 데몬. 로컬/원격/프로덕션을 아우르는 구상",
   "원격 샌드박스 컨테이너(k8s pod/ECS task)"),
  ("신뢰 가정",
   "전적으로 신뢰 — 여러분의 신원으로 여러분의 프로세스를 실행",
   "미공개 — 인증·권한 분리·감사 모두 미정",
   "제로 트러스트 — 내용물을 신뢰하지 않는다는 전제"),
  ("격리",
   "없음(여러분의 환경을 그대로 두는 것이 장점)",
   "없음(데몬이 여러분의 권한을 그대로 가짐)",
   "uid 1000, sudo 없음, read-only rootfs, SA 토큰 없음"),
  ("자격 증명 모델",
   "없음(로컬 socket API)",
   "미발표",
   "첫날부터: 관리 평면과 연결 평면 분리. 세션별 토큰은 TTL이 있고 서명 키가 없음"),
  ("에이전트 상태 시맨틱",
   "일급 객체: blocked/working/done, 에이전트끼리 편성하는 socket API",
   "계획 단계(3단계 비전의 세 번째)",
   "없음 — 의도적으로 다루지 않음. 에이전트 시맨틱은 openab 본체의 몫"),
  ("재접속",
   "접속 끊김은 견딤(호스트 전원이 꺼지는 것은 못 견딤)",
   "화면 스냅숏 + raw 스트림 이어받기. 완전한 터미널 상태",
   "링 버퍼 재생. 상태 시맨틱은 얇음"),
  ("체감 지연",
   "로컬이라 문제가 되지 않음",
   "클라이언트 내장 libghostty가 직접 렌더링, 설계상 서버와 분리(미측정)",
   "클라이언트가 좌우. 런타임 자체 측정 1.0 ms, WiFi 노트북에서 78–82 ms"),
  ("성숙도",
   "지금 사용 가능, 오픈 소스",
   "pre-beta. waitlist뿐, 벤치마크도 스펙도 없음",
   "Phase 1. k3s와 ECS Fargate에서 실사용 중"),
  ("베팅한 것", "오케스트레이션", "지속성", "신뢰"),
  ("포기한 것",
   "격리, 그리고 호스트 너머의 지속성",
   "신뢰 모델(아직은)",
   "환경의 자유도와 터미널 상태 시맨틱"),
 ],
 body=f"""
<h2>하나의 스펙트럼, 두 개의 축</h2>
<p>“세션이 어디에 사는가”로 줄을 세우면 <a href="{HERDR}">Herdr</a>는 여러분의 터미널 안,
<a href="{SL}">Superlogical</a>은 환경을 가로지르는 서버 사이드 데몬, OpenAB Connect는 WireGuard
tailnet 너머의 원격 샌드박스 컨테이너입니다. “신뢰 가정”으로 다시 줄을 세워도 순서는 같습니다.
Herdr는 세션을 전적으로 신뢰하고(그 안은 곧 여러분입니다), Superlogical은 신뢰 모델을 아직
공개하지 않았으며, OpenAB Connect는 첫날부터 내용물을 신뢰하지 않는다는 전제에 서 있습니다.
두 축이 같은 스펙트럼 하나를 그립니다 — Herdr와 OpenAB Connect가 양 극단, Superlogical이 딱
중간입니다.</p>
{{table}}
<h2>Herdr — 오케스트레이션의 극단, 격리는 제로</h2>
<p>Herdr는 지금 쓰는 터미널 안에서 도는 에이전트 멀티플렉서입니다(Rust + Ratatui, 오픈 소스).
에이전트는 런타임의 일급 객체입니다. 사이드바에 각 에이전트가 blocked인지 working인지 done인지
실시간으로 표시되고, socket API로 에이전트가 스스로 pane을 열고, 서로의 출력을 읽고, 서로를
기다릴 수 있습니다. 세션은 데몬 안에서 접속 끊김을 넘어 살아남지만 — 호스트 전원이 꺼지는 것은
넘지 못합니다 — SSH 원격 모드로 다른 머신에도 닿습니다.</p>
<p>모든 것이 여러분의 신원으로, 여러분의 머신 위에서 돕니다. 격리 제로는 결함이 아니라 장점입니다.
셸, SSH 설정, 폰트, 키바인딩을 그대로 쓸 수 있으니까요. Herdr의 베팅은
<strong>오케스트레이션</strong>입니다. 멀티 에이전트 시대에 가장 값진 것은 에이전트 상태의 실시간
가시성이라는 베팅입니다.</p>
<h2>Superlogical — 지속성의 극단, 신뢰는 공란</h2>
<p>Superlogical은 세션을 터미널에서 떼어내 서버 사이드 데몬으로 옮깁니다. 데몬이 PTY를 쥐고
libghostty로 출력을 권위 있는 상태(authoritative state)로 파싱하는 동시에, 같은 raw bytes를
그대로 각 클라이언트에 나눠 줍니다. 클라이언트는 같은 libghostty를 내장해 스스로 파싱하고 스스로
렌더링합니다. 재접속 때는 데몬이 PTY를 잠시 멈추고 화면 스냅숏을 보낸 뒤, 클라이언트가 준비되면
raw 스트림을 이어 갑니다. 비전은 로컬·원격·샌드박스·프로덕션을 모두 아우르는 “multiplexer for
all work”입니다.</p>
<p>Superlogical의 베팅은 <strong>지속성</strong>입니다. 어떤 클라이언트와도 무관하게 살아 있는
세션이라는 지속 계층이야말로 가장 값진 추상이라는 베팅 — Terraform이 state 계층에 걸었던 것과
같은 종류의 베팅입니다. 다만 현재 상태는 정확히 말해 두겠습니다. 이 글을 쓰는 시점에 있는 것은
waitlist뿐이고, 벤치마크도 프로토콜 스펙도 없으며, 인증·권한 분리·감사라는 프로덕션 필수 요소는
하나도 발표되지 않았습니다. 지속성은 끝까지 밀어붙였고, 신뢰는 통째로 공란입니다.</p>
<h2>OpenAB Connect — 신뢰의 극단, 환경은 고정</h2>
<p>우리는 반대쪽 극단에 베팅했습니다. Connect가 붙는 셸은 의도적으로 무권한으로 만든 컨테이너에
삽니다. uid 1000, sudo 없음, read-only rootfs, service-account 토큰 없음, 워크스페이스는 세션과
함께 버려집니다. 자격 증명 모델은 첫날부터 있습니다. 관리 평면과 연결 평면이 분리되어 있고,
세션별 토큰은 TTL이 있으며 서명 키를 갖지 않습니다 — 탈취된 셸이 loopback으로 관리 API를 때려도
돌아오는 것은 401이고, 이는 적대 테스트가 명시적으로 검증하는 불변 조건입니다. 경로 전체는
WireGuard tailnet 위를 지나며, 런타임은 라우팅 가능한 주소에서 절대 수신 대기하지 않습니다
(<a href="{PTY}">런타임은 MIT 라이선스 오픈 소스</a>).</p>
<p>우리의 베팅은 <strong>신뢰</strong>입니다. 에이전트는 폭주하고 셸은 속아 넘어가므로, 환경은
그 안의 것을 신뢰할 수 없다고 가정해야 한다는 베팅입니다. 대가도 솔직히 말하겠습니다. 환경은
고정되어 있고, raw byte pipe 아키텍처에서는 체감 지연이 거의 전부 클라이언트 쪽에서 결정됩니다 —
런타임은 자기 호스트에서 에코 지연 1.0 ms를, WiFi 노트북에서는 78–82 ms를 측정했습니다.
Superlogical의 클라이언트 사이드 state rendering이 정면으로 풀려는 것이 바로, 우리가 README에서
가장 큰 공백이라고 인정한 그 부분입니다.</p>
<h2>세 가지 베팅, 세 개의 층</h2>
<p>흥미로운 점은 셋이 서로를 배제하지 않는다는 것입니다. Herdr식 에이전트 상태 인터페이스가
Superlogical식 지속 세션 위에서 돌고, 그 세션이 OpenAB식 샌드박스 안에 사는 그림 —
오케스트레이션, 지속성, 신뢰는 각자 다른 층을 풉니다. 지금은 세 제품이 각자의 끝에서 중간을 향해
자라고 있는 중일 뿐입니다.</p>
<p>중간에 선다는 것은 양쪽에서 협공당한다는 뜻이기도 합니다. 로컬 편성의 즉시성은 Herdr를 못
따라가고, 제로 트러스트 샌드박스의 보안 모델은 아직 테이블 위에 없습니다. Hashimoto는 durable
session 계층 자체가 승자독식한다는 데 베팅했습니다. 우리는 에이전트가 정말로 풀려나는 날, 모두가
가장 먼저 묻는 것은 — 그것이 무엇에 닿을 수 있는가? — 라는 데 베팅했습니다.</p>
""",
)


NOTE_TEMPLATE = """<!DOCTYPE html>
<html lang="{htmllang}" data-lang="{code}">
<head>
{head}
</head>
<body>

{nav}

<main class="wrap note">
<article>
  <p class="crumbs"><a href="{base}notes/">{notes_label}</a></p>
  <h1>{title}</h1>
  <p class="byline">OpenAB Connect · {date}</p>
  <p class="lede">{lede}</p>
{body}
</article>
</main>

{footer}

</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="{htmllang}" data-lang="{code}">
<head>
{head}
</head>
<body>

{nav}

<main class="wrap notes-index">
<h1>{notes_label}</h1>
<p class="lede">{notes_lede}</p>
{entries}
</main>

{footer}

</body>
</html>
"""

for code in chrome.ORDER:
    d = N[code]
    c = chrome.CHROME[code]
    note_file = f"notes/{SLUG}/"
    index_file = "notes/"

    # The note page. og:image is this language's own card, content-hashed so a
    # corrected card is never served stale by a scraper that caches by URL.
    og = SITE + chrome.rev(f"notes/{SLUG}/og-{code}.png")
    out = chrome.out_path(code, note_file + "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(NOTE_TEMPLATE.format(
        code=code, htmllang=c["htmllang"], base=c["base"],
        head=chrome.head(code, note_file, f'{d["title"]} — OpenAB Connect',
                         d["desc"], og_image=og, og_alt=d["og_alt"],
                         og_type="article"),
        nav=chrome.nav(code, note_file), footer=chrome.footer(code),
        notes_label=d["notes_label"], title=d["title"], date=d["date"],
        lede=d["lede"], body=d["body"].format(table=table(d["rows"]))),
        encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)}  ({len(d['rows'])} rows)")

    # The notes index: newest first, and there is exactly one entry today. The
    # landing card is fine as its og:image — an index is not the shared artifact.
    entry = (f'<a class="note-entry" href="{c["base"]}{note_file}">\n'
             f'  <div class="when">{d["date"]}</div>\n'
             f'  <div class="ntitle">{d["title"]}</div>\n'
             f'  <p>{d["desc"]}</p>\n</a>')
    out = chrome.out_path(code, index_file + "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(INDEX_TEMPLATE.format(
        code=code, htmllang=c["htmllang"], base=c["base"],
        head=chrome.head(code, index_file,
                         f'{d["notes_label"]} — OpenAB Connect', d["notes_lede"],
                         og_image=SITE + chrome.rev(f"og-{code}.png"),
                         og_alt=d["notes_label"]),
        nav=chrome.nav(code, index_file), footer=chrome.footer(code),
        notes_label=d["notes_label"], notes_lede=d["notes_lede"],
        entries=entry),
        encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)}")
