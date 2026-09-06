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

SLUG_TRUST = "terminal-trust-spectrum"
SLUG_SHARE = "shareable-state-for-stateless-agents"
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


# NOTE_<x>[lang] = dict(title, desc, og_alt, date, notes_label, notes_lede,
#                       lede, rows, body) — body is HTML with {table} left to
#                       format in (notes without a table use rows=[] and never
#                       reference {table}).
NOTE_TRUST = {}

NOTE_TRUST["zh"] = dict(
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

NOTE_TRUST["en"] = dict(
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

NOTE_TRUST["ja"] = dict(
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

NOTE_TRUST["ko"] = dict(
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


def _panel_fig(alt):
    """The management-panel screenshot, once per language so the alt is native."""
    src = chrome.rev(f"notes/{SLUG_SHARE}/management-panel.png")
    return (f'<figure class="cmp-shot">'
            f'<img src="{src}" width="1504" height="1328" alt="{alt}"></figure>')


NOTE_SHARE = {}

NOTE_SHARE["zh"] = dict(
 title="持久、共享、可攜：stateless agent 的可共享狀態，我們怎麼設計",
 desc="agent 的執行環境刻意 stateless、用完即棄，但真實工作需要狀態。這篇談我們如何讓"
      "狀態持久、可跨 session 共享、可攜——以及為了不刪別人的資料所做的取捨。",
 og_alt="持久、共享、可攜——stateless agent 的可共享狀態",
 date="2026 年 9 月 6 日",
 notes_label="開發筆記",
 notes_lede="關於 OpenAB Connect 的設計取捨，以及它所在的市場。",
 lede="OpenAB Connect 從第一天就把 agent 的執行環境設計成 stateless：uid 1000、沒有 sudo、"
      "root 檔案系統唯讀、workspace 用完即棄。這是刻意的——agent 會失控、shell 會被騙，"
      "環境必須假設裡面的東西不可信。但一個矛盾很快浮現：真實的工作需要狀態。一個跑了半天"
      "的 workspace、一把多個 agent 共用的 API key、一份想搬去新環境重跑的資料——這些都"
      "不該跟著 session 一起生死。這次更新，講的就是我們怎麼在「執行環境無狀態」和"
      "「工作需要有狀態」之間，設計出一層可共享的狀態。",
 rows=[],
 body=f"""
<h2>先分清楚：哪些是 stateless，哪些不該是</h2>
<p>agent 的執行環境該是 stateless 的——每個 session 是一個可拋棄的沙箱，壞了就丟、重開一個
乾淨的。但 /workspace 裡的資料是另一回事。把這兩者綁在一起，是最容易犯、也最痛的錯：你關掉
一個連線，只是想收掉那個 agent，結果連它三小時的產出一起沒了。</p>
<p>所以第一個決定：workspace 的生命週期，要能獨立於 session 的生命週期。這一版讓你在部署時
三選一——用完即棄（emptyDir）、新建一顆持久磁碟（PVC）、或掛一顆既有的。前兩個是舊有的，
第三個是這次的重點，因為它把「資料」變成一個可以被多個 session 輪流使用的一等公民。</p>
<h2>「借用」不是「擁有」：一條防誤刪的紅線</h2>
<p>一旦允許掛既有的磁碟，一個危險立刻出現：移除連線時，該不該刪那顆磁碟？</p>
<p>我們的答案是一條硬規則：這個 app 建的，才由這個 app 刪；你指定給它掛的，一律不刪。一顆你
事先建好、或別的 agent 正在共用的磁碟，對這個連線來說是「借用」，不是「擁有」——移除連線只
收掉 pod，磁碟原封不動。</p>
<p>這聽起來理所當然，但要做對，關鍵在於所有權必須有證據，不能用猜的。我們踩過的洞是：早期的
清理邏輯只要看到「記錄裡有磁碟名字」就刪。這在「只有自己建的磁碟才會被記錄」的年代是安全的
——但一旦開放掛既有磁碟，同樣的邏輯就會去刪一顆使用者根本沒授權刪的磁碟。修正的原則是：
所有權由部署當下的實際證據決定（這顆真的是我這次建的嗎？），而不是由名字碰巧對得上來推斷。
用慣例猜出來的名字，是未經證實的所有權；未經證實，就不刪。</p>
<h2>共享：狀態不只跨 session，也跨 agent</h2>
{_panel_fig("OpenAB Connect 的 Kubernetes 管理面板：context macmini-orbstack、namespace openab-pty；共享 volume claims 列出 kiro-shared-pvc 與 kiroshared-pvc2（Bound、10Gi、local-path），下方有 New PVC / Delete / Copy 按鈕；共享 secrets 列出 oab-kiro-shared-secrets（key KIRO_API_KEY）")}
<p>持久還不夠。一把 OpenAI key、一份多個 agent 都要讀的設定，不該每開一個 agent 就重打一次、
各存一份。所以這一版加了一個 Kubernetes 管理面板：在這裡建立的 PVC 與 Secret 是共享的、獨立
於任何連線的——它們不屬於某一條連線，移除任何連線都不會動到它們，只有在面板裡才會被手動刪除。</p>
<p>Secret 的部分特別講究一個原則：明文不該經過這個 app。部署時你可以把共享 Secret 的某個 key
直接指定成 agent 的環境變數——用的是 Kubernetes 的 secretKeyRef，值從頭到尾留在叢集裡，app
只搬名字，不碰內容。這跟「把 key 貼進一個輸入框」是兩種安全等級。</p>
<h2>可攜：複製，而不是污染</h2>
<p>有了共享狀態，下一個需求很自然：我想拿一顆現有磁碟當起點，複製一份出來給新的 agent 玩，
但不動到原本那顆。</p>
<p>這裡我們刻意沒用 Kubernetes 的 CSI clone——因為那需要底層儲存驅動支援，而很多環境（包括
開發常用的 local-path）根本沒有。我們用的是一個更樸素、但到處都能跑的做法：起一個極短命的
job，同時掛來源（唯讀）和目的，cp -a 把內容複製過去，然後自己消失。這個 job 被嚴格 harden
（非 root、丟掉所有 capability、唯讀 root fs、不掛 service-account token、來源唯讀），因為它
是一段會碰到你資料的程式，就該用對待不可信程式的方式對待它。</p>
<p>一個誠實的邊界：這條路只能複製閒置的磁碟。一顆正被某個 pod 用著的磁碟（RWO，一次只能一個
掛載者），我們的做法是不讓你選、清楚標示「使用中」，而不是讓 job 卡在那裡等到逾時。要複製
「使用中」的磁碟而不打擾它，那才真的需要 CSI 快照——那是我們留給未來的一步。</p>
<h2>回到那個矛盾</h2>
<p>「stateless agent」和「可共享的狀態」聽起來衝突，其實不是。stateless 的是執行環境——那層
我們要它可拋棄、不可信、隨時能丟。有狀態的是工作本身——那層我們要它持久、可共享、可搬。這次
更新做的，就是把這兩層乾淨地分開：讓沙箱繼續用完即棄，同時給資料一個能活得比任何單一 session
更久、被明確擁有或明確借用、能被複製搬移的家。</p>
<p>關掉 app，agent 繼續跑。移除連線，資料還在。這是同一個信念的兩面：該短暫的東西讓它短暫，
該持久的東西，值得一個經得起推敲的所有權模型。</p>
""",
)

NOTE_SHARE["en"] = dict(
 title="Durable, shared, portable: how we designed shareable state for stateless agents",
 desc="The agent's execution environment is deliberately stateless and disposable — but real "
      "work needs state. How we made state durable, shareable across sessions, and portable — "
      "and the trade-offs we accepted so we never delete someone else's data.",
 og_alt="Durable, shared, portable — shareable state for stateless agents",
 date="September 6, 2026",
 notes_label="Dev notes",
 notes_lede="Design trade-offs behind OpenAB Connect, and the market it sits in.",
 lede="OpenAB Connect has kept the agent's execution environment stateless from day one: "
      "uid 1000, no sudo, a read-only root filesystem, a workspace discarded with the session. "
      "That is deliberate — agents run away and shells get tricked, so the environment must "
      "assume nothing inside it can be trusted. But a contradiction surfaced quickly: real work "
      "needs state. A workspace half a day in the making, an API key several agents share, data "
      "you want to carry into a fresh environment and rerun — none of it should live and die "
      "with a session. This update is about the layer of shareable state we designed between "
      "a stateless environment and stateful work.",
 rows=[],
 body=f"""
<h2>First, draw the line: what is stateless, and what must not be</h2>
<p>The agent's execution environment should be stateless — each session a disposable sandbox:
if it breaks, throw it away and start a clean one. But the data in /workspace is a different
matter. Tying the two together is the easiest mistake to make and the most painful one: you
close a connection meaning only to retire that agent, and three hours of its output go with
it.</p>
<p>So the first decision: a workspace's lifecycle must be able to run independently of the
session's. This release gives you three choices at deploy time — disposable (emptyDir), a
freshly created persistent disk (a PVC), or an existing one mounted in. The first two existed
before; the third is the point of this release, because it turns data into a first-class
citizen that successive sessions can take turns using.</p>
<h2>Borrowed is not owned: a hard line against deleting other people's data</h2>
<p>The moment you allow mounting an existing disk, a danger appears: when a connection is
removed, should that disk be deleted?</p>
<p>Our answer is one hard rule: this app deletes only what this app created; anything you told
it to mount is never touched. A disk you provisioned beforehand, or one other agents are
sharing, is borrowed by this connection, not owned — removing the connection tears down the
pod and leaves the disk exactly as it was.</p>
<p>That sounds obvious, but getting it right hinges on ownership being evidenced, never
guessed. The hole we fell into: our early cleanup logic deleted any disk whose name appeared
in its records. That was safe in the era when only self-created disks were ever recorded —
but the moment existing disks could be mounted, the same logic would delete a disk the user
never authorized it to touch. The corrected principle: ownership is decided by actual evidence
at deploy time (did I really create this one, this time?), not inferred from a name that
happens to match. A name guessed from convention is unproven ownership; unproven means not
deleted.</p>
<h2>Shared: state across agents, not just across sessions</h2>
{_panel_fig("OpenAB Connect's Kubernetes management panel: context macmini-orbstack, namespace openab-pty; shared volume claims list kiro-shared-pvc and kiroshared-pvc2 (Bound, 10Gi, local-path) with New PVC / Delete / Copy buttons below; shared secrets list oab-kiro-shared-secrets (key KIRO_API_KEY)")}
<p>Durable is not enough. An OpenAI key, a config several agents all read — these should not
be retyped and stored once per agent. So this release adds a Kubernetes management panel: PVCs
and Secrets created there are shared and independent of any connection — they belong to no
connection, removing any connection leaves them untouched, and only a manual action in the
panel deletes them.</p>
<p>The Secret side is strict about one principle: plaintext should never pass through this
app. At deploy time you can bind a key of a shared Secret directly to an agent's environment
variable — via Kubernetes's secretKeyRef, so the value stays inside the cluster end to end;
the app moves names, never contents. That is a different security class from pasting a key
into a text field.</p>
<h2>Portable: copy, don't contaminate</h2>
<p>Once state is shared, the next need follows naturally: take an existing disk as a starting
point, copy it for a new agent to play with, and leave the original alone.</p>
<p>Here we deliberately did not use Kubernetes CSI cloning — it needs support from the
underlying storage driver, which many environments (including local-path, the usual choice in
development) simply lack. We use something plainer that runs everywhere: a very short-lived
job that mounts the source (read-only) and the destination side by side, copies the contents
across with cp -a, and then disappears. The job is strictly hardened (non-root, all
capabilities dropped, read-only root filesystem, no service-account token, source mounted
read-only), because it is a piece of code that touches your data, and such code deserves to
be treated the way untrusted code is treated.</p>
<p>An honest boundary: this path can only copy an idle disk. For a disk currently in use by a
pod (RWO — one mounter at a time), our choice is to make it unselectable and label it clearly
as in use, rather than let the job hang until it times out. Copying a live disk without
disturbing it genuinely requires CSI snapshots — a step we have left for the future.</p>
<h2>Back to the contradiction</h2>
<p>“Stateless agent” and “shareable state” sound like a conflict. They are not. What is
stateless is the execution environment — the layer we want disposable, untrusted, discardable
at any moment. What is stateful is the work itself — the layer we want durable, shareable,
movable. What this update does is separate the two layers cleanly: the sandbox stays
disposable, while the data gets a home that outlives any single session, is explicitly owned
or explicitly borrowed, and can be copied and moved.</p>
<p>Close the app, and the agent keeps running. Remove the connection, and the data is still
there. Two faces of the same conviction: let what should be ephemeral be ephemeral — and what
should persist deserves an ownership model that stands up to scrutiny.</p>
""",
)

NOTE_SHARE["ja"] = dict(
 title="永続・共有・可搬——stateless エージェントの「共有できる状態」を、こう設計した",
 desc="エージェントの実行環境は意図的に stateless で使い捨て。だが実際の仕事には状態が要る。"
      "状態を永続化し、セッションを越えて共有し、持ち運べるようにした方法——そして他人の"
      "データを消さないために引き受けたトレードオフの話。",
 og_alt="永続・共有・可搬——stateless エージェントの共有できる状態",
 date="2026 年 9 月 6 日",
 notes_label="開発ノート",
 notes_lede="OpenAB Connect の設計上のトレードオフと、それが立つ市場について。",
 lede="OpenAB Connect は初日から、エージェントの実行環境を stateless に設計してきた。"
      "uid 1000、sudo なし、root ファイルシステムは読み取り専用、ワークスペースはセッション"
      "とともに破棄。これは意図的だ——エージェントは暴走するし、シェルは騙される。環境は"
      "中身を信頼できないものとして扱わなければならない。だが矛盾はすぐに現れた。実際の"
      "仕事には状態が要る。半日かけて育てたワークスペース、複数のエージェントで共用する "
      "API キー、新しい環境に持ち込んで再実行したいデータ——どれもセッションと生死をともに"
      "すべきものではない。今回のアップデートは、「実行環境は無状態」と「仕事には状態が要る」"
      "のあいだに、共有できる状態の層をどう設計したかという話だ。",
 rows=[],
 body=f"""
<h2>まず切り分ける——何が stateless で、何がそうであってはならないか</h2>
<p>エージェントの実行環境は stateless であるべきだ。各セッションは使い捨てのサンドボックスで、
壊れたら捨てて、きれいなものを立ち上げ直せばいい。だが /workspace の中のデータは別の話だ。
この二つを縛り付けてしまうのは、いちばん犯しやすく、いちばん痛い間違いでもある。接続を閉じて
そのエージェントを片付けたかっただけなのに、三時間ぶんの成果が一緒に消える。</p>
<p>そこで最初の決定：ワークスペースのライフサイクルは、セッションのライフサイクルから独立
できなければならない。今回のリリースでは、デプロイ時に三つから選べる——使い捨て（emptyDir）、
新しい永続ディスクの作成（PVC）、既存ディスクのマウント。前の二つは以前からあった。要は三つ目
で、これによって「データ」は、複数のセッションが代わる代わる使える一級市民になる。</p>
<h2>「借り物」は「持ち物」ではない——誤削除を防ぐ一線</h2>
<p>既存ディスクのマウントを許した瞬間、危険が一つ現れる。接続を削除するとき、そのディスクを
消していいのか？</p>
<p>私たちの答えは一つの固い規則だ。この app が作ったものだけを、この app が消す。あなたが
マウントするよう指定したものは、一切消さない。事前に作っておいたディスクや、ほかのエージェント
が共用しているディスクは、この接続にとって「借り物」であって「持ち物」ではない——接続を削除
すれば pod は片付くが、ディスクは元のまま残る。</p>
<p>当たり前に聞こえるが、正しくやるには、所有権が証拠に基づかなければならない。推測では
だめだ。私たちが踏んだ穴はこうだった。初期のクリーンアップロジックは、「記録にディスク名が
ある」だけで削除していた。自分が作ったディスクしか記録されない時代には安全だった——だが既存
ディスクのマウントを開放した瞬間、同じロジックが、ユーザーが削除を許可した覚えのないディスク
を消しに行く。修正後の原則はこうだ。所有権は、デプロイ時点の実際の証拠で決める（これは本当に、
今回、私が作ったものか？）。名前がたまたま一致することから推論しない。慣習から推測した名前は
証明されていない所有権であり、証明されていないなら、消さない。</p>
<h2>共有——セッションだけでなく、エージェントも越える</h2>
{_panel_fig("OpenAB Connect の Kubernetes 管理パネル：context は macmini-orbstack、namespace は openab-pty。共有 volume claims に kiro-shared-pvc と kiroshared-pvc2（Bound・10Gi・local-path）が並び、下に New PVC / Delete / Copy ボタン。共有 secrets には oab-kiro-shared-secrets（key は KIRO_API_KEY）")}
<p>永続化だけでは足りない。一つの OpenAI キー、複数のエージェントが読む設定——エージェントを
立ち上げるたびに打ち直し、それぞれに保存するようなものではない。そこで今回、Kubernetes の管理
パネルを追加した。ここで作った PVC と Secret は共有で、どの接続からも独立している——特定の
接続に属さず、どの接続を削除しても影響を受けず、消えるのはパネルで手動で削除したときだけだ。</p>
<p>Secret については、一つの原則にこだわった。平文はこの app を通らない。デプロイ時に、共有
Secret の特定の key をエージェントの環境変数として直接指定できる——使うのは Kubernetes の
secretKeyRef で、値は最初から最後までクラスタの中に留まる。app が運ぶのは名前だけで、中身には
触れない。「キーを入力欄に貼り付ける」のとは、セキュリティの等級が違う。</p>
<h2>可搬——汚染ではなく、複製</h2>
<p>状態が共有できるようになると、次の要求は自然に出てくる。既存のディスクを起点に、複製を
一つ作って新しいエージェントに遊ばせたい。ただし元のディスクには触れずに。</p>
<p>ここで私たちは、Kubernetes の CSI clone をあえて使わなかった。下層のストレージドライバの
対応が必要で、多くの環境（開発でよく使う local-path を含む）にはそれがないからだ。使ったのは、
もっと素朴だが、どこでも動くやり方だ。ごく短命の job を立ち上げ、コピー元（読み取り専用）と
コピー先を同時にマウントし、cp -a で中身を写して、自分で消える。この job は厳格に harden して
ある（非 root、全 capability の破棄、読み取り専用の root fs、service-account トークンなし、
コピー元は読み取り専用）。あなたのデータに触れるコードなのだから、信頼できないコードを扱う
やり方で扱うべきだ。</p>
<p>正直な境界を一つ。この方法で複製できるのは、遊んでいるディスクだけだ。いまどこかの pod に
使われているディスク（RWO——マウントできるのは一度に一つ）については、選べないようにして
「使用中」と明示する。job をタイムアウトまで待たせたりはしない。「使用中」のディスクを邪魔
せずに複製するには、本当に CSI スナップショットが要る——それは未来に残した一歩だ。</p>
<h2>あの矛盾に戻る</h2>
<p>「stateless なエージェント」と「共有できる状態」は、衝突しているように聞こえて、実は
していない。stateless なのは実行環境だ——その層は使い捨てで、信頼せず、いつでも捨てられて
ほしい。状態を持つのは仕事そのものだ——その層は永続し、共有でき、持ち運べてほしい。今回の
アップデートがやったのは、この二つの層をきれいに分けることだ。サンドボックスは使い捨ての
ままに、データには、どのセッションよりも長く生き、明示的に所有されるか明示的に借りられ、複製
して運べる住処を与える。</p>
<p>app を閉じても、エージェントは走り続ける。接続を削除しても、データは残る。同じ信念の
両面だ。短命であるべきものは短命に。永続すべきものには、吟味に耐える所有権のモデルを。</p>
""",
)

NOTE_SHARE["ko"] = dict(
 title="지속·공유·이동 — stateless 에이전트의 공유 가능한 상태, 우리는 이렇게 설계했다",
 desc="에이전트의 실행 환경은 의도적으로 stateless하고 일회용입니다. 하지만 실제 작업에는 "
      "상태가 필요합니다. 상태를 지속시키고, 세션을 넘어 공유하고, 옮길 수 있게 만든 방법 — "
      "그리고 남의 데이터를 지우지 않기 위해 받아들인 트레이드오프에 대하여.",
 og_alt="지속·공유·이동 — stateless 에이전트의 공유 가능한 상태",
 date="2026년 9월 6일",
 notes_label="개발 노트",
 notes_lede="OpenAB Connect의 설계 트레이드오프, 그리고 이 제품이 서 있는 시장에 대하여.",
 lede="OpenAB Connect는 첫날부터 에이전트의 실행 환경을 stateless로 설계했습니다. uid 1000, "
      "sudo 없음, 읽기 전용 root 파일 시스템, 세션과 함께 버려지는 워크스페이스 — 이것은 "
      "의도적입니다. 에이전트는 폭주하고 셸은 속아 넘어가므로, 환경은 그 안의 것을 신뢰할 수 "
      "없다고 가정해야 합니다. 하지만 모순은 금방 드러났습니다. 실제 작업에는 상태가 "
      "필요합니다. 한나절을 들여 키운 워크스페이스, 여러 에이전트가 함께 쓰는 API 키, 새 "
      "환경으로 옮겨 다시 돌리고 싶은 데이터 — 어느 것도 세션과 생사를 같이해서는 안 됩니다. "
      "이번 업데이트는 '실행 환경은 무상태'와 '작업에는 상태가 필요하다' 사이에, 공유 가능한 "
      "상태라는 층을 어떻게 설계했는가에 대한 이야기입니다.",
 rows=[],
 body=f"""
<h2>먼저 선을 긋자 — 무엇이 stateless여야 하고, 무엇은 아니어야 하는가</h2>
<p>에이전트의 실행 환경은 stateless여야 합니다. 각 세션은 버릴 수 있는 샌드박스이고, 망가지면
버리고 깨끗한 것을 새로 열면 됩니다. 하지만 /workspace 안의 데이터는 다른 이야기입니다. 이 둘을
묶어 버리는 것은 가장 저지르기 쉽고 가장 아픈 실수입니다. 그 에이전트 하나를 정리하려고 연결을
닫았을 뿐인데, 세 시간치 산출물이 함께 사라집니다.</p>
<p>그래서 첫 번째 결정: 워크스페이스의 수명 주기는 세션의 수명 주기와 독립적이어야 합니다. 이번
버전에서는 배포 시 셋 중 하나를 고를 수 있습니다 — 일회용(emptyDir), 새 지속 디스크 생성(PVC),
기존 디스크 마운트. 앞의 둘은 원래 있었고, 핵심은 세 번째입니다. 이것이 '데이터'를 여러 세션이
번갈아 쓸 수 있는 일급 객체로 만들기 때문입니다.</p>
<h2>'빌린 것'은 '가진 것'이 아니다 — 오삭제를 막는 한 줄의 선</h2>
<p>기존 디스크의 마운트를 허용하는 순간, 위험이 하나 나타납니다. 연결을 제거할 때, 그 디스크를
지워도 되는가?</p>
<p>우리의 답은 하나의 단단한 규칙입니다. 이 앱이 만든 것만 이 앱이 지운다. 여러분이 마운트하라고
지정한 것은 절대 지우지 않는다. 미리 만들어 둔 디스크, 혹은 다른 에이전트가 함께 쓰고 있는
디스크는 이 연결에게 '빌린 것'이지 '가진 것'이 아닙니다 — 연결을 제거하면 pod만 정리되고,
디스크는 원래 그대로 남습니다.</p>
<p>당연하게 들리지만, 제대로 하려면 소유권이 증거에 근거해야 합니다. 추측으로는 안 됩니다.
우리가 빠졌던 구멍은 이렇습니다. 초기의 정리 로직은 '기록에 디스크 이름이 있다'는 것만으로
지웠습니다. 스스로 만든 디스크만 기록되던 시절에는 안전했지만 — 기존 디스크의 마운트를 여는
순간, 같은 로직이 사용자가 지우라고 허락한 적 없는 디스크를 지우러 갑니다. 수정된 원칙은
이렇습니다. 소유권은 배포 시점의 실제 증거로 결정한다(이건 정말로, 이번에, 내가 만든 것인가?).
이름이 우연히 맞아떨어진다고 추론하지 않는다. 관례로 짐작한 이름은 증명되지 않은 소유권이고,
증명되지 않았으면 지우지 않습니다.</p>
<h2>공유 — 세션만이 아니라 에이전트도 넘어서</h2>
{_panel_fig("OpenAB Connect의 Kubernetes 관리 패널: context macmini-orbstack, namespace openab-pty. 공유 volume claims에 kiro-shared-pvc와 kiroshared-pvc2(Bound, 10Gi, local-path)가 나열되고 아래에 New PVC / Delete / Copy 버튼, 공유 secrets에는 oab-kiro-shared-secrets(key KIRO_API_KEY)")}
<p>지속만으로는 부족합니다. OpenAI 키 하나, 여러 에이전트가 모두 읽는 설정 하나 — 에이전트를
열 때마다 다시 입력하고 각자 따로 저장할 것이 아닙니다. 그래서 이번 버전에는 Kubernetes 관리
패널을 추가했습니다. 여기서 만든 PVC와 Secret은 공유이며 어떤 연결로부터도 독립입니다 — 특정
연결에 속하지 않고, 어느 연결을 제거해도 건드려지지 않으며, 오직 패널에서 수동으로 지울 때만
사라집니다.</p>
<p>Secret 쪽은 한 가지 원칙을 특히 지켰습니다. 평문은 이 앱을 거치지 않는다. 배포 시 공유
Secret의 특정 key를 에이전트의 환경 변수로 직접 지정할 수 있는데 — 여기에 쓰는 것은 Kubernetes의
secretKeyRef라서, 값은 처음부터 끝까지 클러스터 안에 머뭅니다. 앱은 이름만 옮기고 내용은 만지지
않습니다. '키를 입력란에 붙여 넣는 것'과는 보안 등급이 다릅니다.</p>
<h2>이동 — 오염이 아니라 복사</h2>
<p>상태를 공유할 수 있게 되면 다음 요구는 자연스럽게 따라옵니다. 기존 디스크를 출발점 삼아
복사본을 하나 만들어 새 에이전트에게 주고 싶다, 단 원본은 건드리지 않고.</p>
<p>여기서 우리는 Kubernetes의 CSI clone을 일부러 쓰지 않았습니다. 하부 스토리지 드라이버의
지원이 필요한데, 많은 환경(개발에서 흔히 쓰는 local-path 포함)에는 그것이 아예 없기 때문입니다.
우리가 쓴 것은 더 소박하지만 어디서나 도는 방법입니다. 아주 짧게 사는 job을 하나 띄워, 원본(읽기
전용)과 대상을 동시에 마운트하고, cp -a로 내용을 복사한 뒤, 스스로 사라집니다. 이 job은 엄격하게
하드닝되어 있습니다(비 root, 모든 capability 제거, 읽기 전용 root fs, service-account 토큰 없음,
원본은 읽기 전용). 여러분의 데이터를 만지는 코드이므로, 신뢰할 수 없는 코드를 다루는 방식으로
다뤄야 하기 때문입니다.</p>
<p>정직한 경계 하나. 이 길로는 놀고 있는 디스크만 복사할 수 있습니다. 지금 어떤 pod가 쓰고 있는
디스크(RWO — 한 번에 하나만 마운트 가능)는, job이 타임아웃까지 매달리게 두는 대신 선택할 수
없게 하고 '사용 중'이라고 분명히 표시하는 쪽을 택했습니다. '사용 중'인 디스크를 방해하지 않고
복사하려면 정말로 CSI 스냅숏이 필요합니다 — 그것은 미래에 남겨 둔 한 걸음입니다.</p>
<h2>그 모순으로 돌아가서</h2>
<p>'stateless 에이전트'와 '공유 가능한 상태'는 충돌하는 것처럼 들리지만, 사실 그렇지 않습니다.
stateless인 것은 실행 환경입니다 — 그 층은 버릴 수 있고, 신뢰하지 않고, 언제든 폐기할 수 있기를
바랍니다. 상태를 갖는 것은 작업 그 자체입니다 — 그 층은 지속되고, 공유되고, 옮겨질 수 있기를
바랍니다. 이번 업데이트가 한 일은 이 두 층을 깨끗하게 분리한 것입니다. 샌드박스는 계속
일회용으로 두면서, 데이터에는 어떤 단일 세션보다 오래 살고, 명시적으로 소유되거나 명시적으로
빌려지며, 복사해 옮길 수 있는 집을 줍니다.</p>
<p>앱을 닫아도 에이전트는 계속 돕니다. 연결을 제거해도 데이터는 남습니다. 같은 신념의 두
얼굴입니다. 짧아야 할 것은 짧게 — 그리고 지속되어야 할 것에는, 따져 물어도 견디는 소유권 모델을.</p>
""",
)

# Newest first.
NOTES = [
    (SLUG_SHARE, NOTE_SHARE),
    (SLUG_TRUST, NOTE_TRUST),
]


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

# Note pages: one per (note, language). og:image is that note's own card for
# that language, content-hashed so a corrected card is never served stale by a
# scraper that caches by URL.
for slug, N in NOTES:
    for code in chrome.ORDER:
        d = N[code]
        c = chrome.CHROME[code]
        note_file = f"notes/{slug}/"

        og = SITE + chrome.rev(f"notes/{slug}/og-{code}.png")
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

# The notes index: all notes, newest first. The landing card is fine as its
# og:image — an index is not the shared artifact.
for code in chrome.ORDER:
    c = chrome.CHROME[code]
    index_file = "notes/"
    d = NOTES[0][1][code]  # notes_label / notes_lede are the same in every note

    entries = "\n".join(
        f'<a class="note-entry" href="{c["base"]}notes/{slug}/">\n'
        f'  <div class="when">{N[code]["date"]}</div>\n'
        f'  <div class="ntitle">{N[code]["title"]}</div>\n'
        f'  <p>{N[code]["desc"]}</p>\n</a>'
        for slug, N in NOTES)
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
        entries=entries),
        encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)}")
