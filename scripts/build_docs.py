#!/usr/bin/env python3
"""Privacy policy and support pages, four languages each.

    python3 scripts/build_docs.py

English stays at /privacy.html and /support.html: Apple has those two URLs on file for
this app, so they must not move. The other languages sit under /zh/, /ja/, /ko/.

Not translated line by line. The support page is a list of real failures, and what makes
each one recognisable differs by language.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chrome

UPDATED = "21 August 2026"
PTY = chrome.PTY
ADVISORY = PTY + "/security/advisories/new"
ISSUES = PTY + "/issues"
HISTORY = "https://github.com/openabdev/connect-site/commits/main/privacy.html"
MAIL = "support@openab.dev"

PRIVACY = {
 "en": dict(
  title="Privacy Policy — OpenAB Connect",
  desc="OpenAB Connect collects nothing: no account, no analytics, no telemetry, and no "
       "server of ours that the app contacts.",
  h1="Privacy Policy", updated=f"OpenAB Connect · last updated {UPDATED}",
  lead="<strong>OpenAB Connect collects nothing.</strong> There is no account, no "
       "analytics, no crash reporting, no advertising and no telemetry of any kind. We "
       "operate no server that the app contacts.",
  intro="That is the whole policy. The rest of this page explains what the app does with "
        "the data it necessarily handles, because “collects nothing” is worth "
        "substantiating rather than asserting.",
  sections=[
   ("What the app handles, and where it goes", None, [
    "<strong>Server addresses you enter.</strong> Stored in the app's own preferences on "
    "your Mac, so it can reconnect. They describe machines you deployed.",
    "<strong>Credentials you enter.</strong> Stored in the macOS Keychain. They are sent "
    "only to the server you entered them for, as an <code>Authorization</code> header, "
    "and never anywhere else. The app does not transmit, back up or sync them.",
    "<strong>Terminal contents.</strong> Streamed between your Mac and your own server "
    "for as long as a session is attached. Nothing is written to disk by the app and "
    "nothing passes through us.",
    "<strong>AWS credentials, if you deploy to ECS.</strong> Read from your existing AWS "
    "configuration or a sign-in you perform, used to call your own account, and held "
    "only in memory for the duration.",
   ]),
   ("Network connections",
    "Outbound only, and only to endpoints you configure: your own runtime, and — if you "
    "use the ECS deployment path — Amazon's APIs on your behalf. The app contacts no "
    "other host. It has no update service, no licence check and no beacon.", []),
   ("What we receive",
    "Nothing. We have no servers, no database and no logs relating to your use of the "
    "app. If you email us for support, we receive what is in your email and nothing "
    'else; see <a href="{p}support.html">Support</a>.', []),
   ("Third parties",
    "The app bundles the <code>kubectl</code> and <code>ecsctl</code> command-line tools "
    "so it can deploy into infrastructure you already own. They run inside the app's "
    "sandbox and talk only to the cluster or account you point them at.<br><br>"
    f'The container images the app deploys are built from <a href="{PTY}">'
    "openabdev/openab-pty</a> and, for every variant except <code>native</code>, include "
    "a third-party coding CLI whose terms and privacy practices are set by its vendor, "
    "not by us. What that agent does with your code or prompts is between you and that "
    "vendor.", []),
   ("Children", "The app is a developer tool and is not directed at children.", []),
   ("Changes",
    "If this policy changes, the date above changes with it, and earlier versions remain "
    f'in the page\'s <a href="{HISTORY}">git history</a> rather than being quietly '
    "replaced.", []),
   ("Contact", f'<a href="mailto:{MAIL}">{MAIL}</a>', []),
  ]),

 "zh": dict(
  title="隱私政策 — OpenAB Connect",
  desc="OpenAB Connect 什麼都不收集:沒有帳號、沒有分析、沒有遙測,也沒有任何屬於我們的伺服器會被這個 app 連上。",
  h1="隱私政策", updated=f"OpenAB Connect · 最後更新 {UPDATED}",
  lead="<strong>OpenAB Connect 什麼都不收集。</strong>沒有帳號、沒有分析、沒有崩潰回報、"
       "沒有廣告,也沒有任何形式的遙測。我們沒有營運任何會被這個 app 連上的伺服器。",
  intro="這就是整份政策。以下的內容解釋這個 app 對它必然會處理到的資料做了什麼 —— "
        "因為「什麼都不收集」值得被證實,而不只是被宣稱。",
  sections=[
   ("app 會處理什麼,以及那些東西去了哪裡", None, [
    "<strong>你輸入的伺服器位址。</strong>存在 app 自己的偏好設定裡,在你的 Mac 上,"
    "用來重新連線。它們描述的是你自己部署的機器。",
    "<strong>你輸入的憑證。</strong>存在 macOS Keychain。它們只會以 "
    "<code>Authorization</code> 標頭送到你為它輸入的那台伺服器,不會送到任何其他地方。"
    "app 不會傳輸、備份或同步它們。",
    "<strong>終端機的內容。</strong>在 session 附加期間,於你的 Mac 和你自己的伺服器之間"
    "串流。app 不會把它寫到磁碟,也不會經過我們。",
    "<strong>AWS 憑證(如果你部署到 ECS)。</strong>從你既有的 AWS 設定或你自己執行的登入"
    "讀取,用來呼叫你自己的帳號,而且只在當次操作期間留在記憶體裡。",
   ]),
   ("網路連線",
    "只有對外,而且只連到你設定的端點:你自己的 runtime,以及 —— 如果你走 ECS 部署路徑 —— "
    "代表你呼叫的 Amazon API。app 不會連到其他任何主機。它沒有更新服務、沒有授權檢查、"
    "也沒有任何回報信標。", []),
   ("我們收到什麼",
    "什麼都沒有。我們沒有伺服器、沒有資料庫,也沒有任何與你使用這個 app 有關的紀錄。"
    "如果你寄信來詢問,我們收到的就是你信裡的內容,除此之外沒有別的;參見"
    '<a href="{p}support.html">支援</a>。', []),
   ("第三方",
    "app 內附 <code>kubectl</code> 和 <code>ecsctl</code> 兩個命令列工具,"
    "以便部署到你已經擁有的基礎架構。它們在 app 的沙箱內執行,只和你指定的叢集或帳號通訊。"
    "<br><br>"
    f'app 部署的容器映像建置自 <a href="{PTY}">openabdev/openab-pty</a>,'
    "而除了 <code>native</code> 之外的每一個版本都包含一個第三方 coding CLI —— "
    "它的條款與隱私做法由它的廠商決定,不是由我們決定。那個 agent 對你的程式碼或提示詞"
    "做了什麼,是你和那家廠商之間的事。", []),
   ("兒童", "這個 app 是開發者工具,並非針對兒童設計。", []),
   ("變更",
    "如果這份政策有變動,上方的日期會跟著改,而先前的版本會留在這個頁面的"
    f'<a href="{HISTORY}">git 歷史</a>裡,而不是被安靜地取代掉。', []),
   ("聯絡", f'<a href="mailto:{MAIL}">{MAIL}</a>', []),
  ]),

 "ja": dict(
  title="プライバシーポリシー — OpenAB Connect",
  desc="OpenAB Connect は何も収集しません。アカウントも解析もテレメトリもなく、"
       "アプリが接続する当方のサーバーも存在しません。",
  h1="プライバシーポリシー", updated=f"OpenAB Connect · 最終更新 {UPDATED}",
  lead="<strong>OpenAB Connect は何も収集しません。</strong>アカウント登録、解析、"
       "クラッシュレポート、広告、いかなる形のテレメトリもありません。"
       "このアプリが接続する当方のサーバーは存在しません。",
  intro="ポリシーとしてはこれで全部です。以下は、アプリが必然的に扱うデータをどう扱って"
        "いるかの説明です。「何も収集しない」は主張するより裏づける価値があるからです。",
  sections=[
   ("アプリが扱うもの、そしてその行き先", None, [
    "<strong>入力したサーバーアドレス。</strong>再接続のために、お使いの Mac 上の"
    "アプリ自身の設定に保存されます。それはあなたがデプロイしたマシンを指すものです。",
    "<strong>入力した資格情報。</strong>macOS のキーチェーンに保存されます。"
    "<code>Authorization</code> ヘッダーとして、その資格情報を入力した先のサーバーへだけ"
    "送られ、それ以外のどこへも送られません。アプリが送信・バックアップ・同期することは"
    "ありません。",
    "<strong>ターミナルの内容。</strong>セッションが接続されている間、お使いの Mac と"
    "あなた自身のサーバーの間でストリームされます。アプリがディスクへ書き出すことはなく、"
    "当方を経由することもありません。",
    "<strong>ECS にデプロイする場合の AWS 資格情報。</strong>既存の AWS 設定または"
    "ご自身で行うサインインから読み取り、あなた自身のアカウントを呼び出すために使い、"
    "その処理の間だけメモリに保持します。",
   ]),
   ("ネットワーク接続",
    "送信方向のみ、しかもあなたが設定したエンドポイントだけです。あなた自身のランタイムと、"
    "ECS のデプロイ経路を使う場合はあなたの代理として呼び出す Amazon の API です。"
    "他のホストへは接続しません。更新サービスもライセンス確認もビーコンもありません。", []),
   ("当方が受け取るもの",
    "何もありません。あなたのアプリ利用に関するサーバー、データベース、ログを当方は"
    "持っていません。サポートのためにメールをいただいた場合、受け取るのはそのメールの"
    '内容だけです。<a href="{p}support.html">サポート</a>をご覧ください。', []),
   ("第三者",
    "アプリは、あなたがすでに所有するインフラへデプロイできるように <code>kubectl</code> と "
    "<code>ecsctl</code> のコマンドラインツールを同梱しています。これらはアプリの"
    "サンドボックス内で動き、あなたが指定したクラスタまたはアカウントとだけ通信します。"
    "<br><br>"
    f'アプリがデプロイするコンテナイメージは <a href="{PTY}">openabdev/openab-pty</a> から'
    "ビルドされ、<code>native</code> 以外のすべての variant にはサードパーティの "
    "coding CLI が含まれます。その規約とプライバシーの扱いは当方ではなくそのベンダーが"
    "定めるものです。そのエージェントがあなたのコードやプロンプトに対して何をするかは、"
    "あなたとそのベンダーの間の問題です。", []),
   ("子ども", "このアプリは開発者向けのツールで、子どもを対象としていません。", []),
   ("変更",
    "このポリシーが変わるときは上の日付も変わり、以前の版はこのページの"
    f'<a href="{HISTORY}">git 履歴</a>に残ります。黙って差し替えることはしません。', []),
   ("連絡先", f'<a href="mailto:{MAIL}">{MAIL}</a>', []),
  ]),

 "ko": dict(
  title="개인정보 처리방침 — OpenAB Connect",
  desc="OpenAB Connect는 아무것도 수집하지 않습니다. 계정도, 분석도, 텔레메트리도 없고 "
       "앱이 접속하는 우리 쪽 서버도 없습니다.",
  h1="개인정보 처리방침", updated=f"OpenAB Connect · 마지막 업데이트 {UPDATED}",
  lead="<strong>OpenAB Connect는 아무것도 수집하지 않습니다.</strong> 계정도, 분석도, "
       "크래시 리포트도, 광고도, 어떤 형태의 텔레메트리도 없습니다. 이 앱이 접속하는 우리 "
       "쪽 서버는 존재하지 않습니다.",
  intro="방침 자체는 이것으로 전부입니다. 아래는 앱이 필연적으로 다루게 되는 데이터를 어떻게 "
        "다루는지에 대한 설명입니다. “아무것도 수집하지 않는다”는 주장하기보다 뒷받침할 "
        "가치가 있기 때문입니다.",
  sections=[
   ("앱이 다루는 것, 그리고 그것이 가는 곳", None, [
    "<strong>입력한 서버 주소.</strong> 재접속을 위해 여러분 Mac에 있는 앱 자체의 설정에 "
    "저장됩니다. 그 주소는 여러분이 배포한 기계를 가리킵니다.",
    "<strong>입력한 자격 증명.</strong> macOS 키체인에 저장됩니다. <code>Authorization</code> "
    "헤더로, 그 자격 증명을 입력한 대상 서버에만 전송되며 다른 어디로도 가지 않습니다. 앱이 "
    "전송하거나 백업하거나 동기화하지 않습니다.",
    "<strong>터미널 내용.</strong> 세션이 연결되어 있는 동안 여러분의 Mac과 여러분 자신의 "
    "서버 사이에서 스트리밍됩니다. 앱이 디스크에 기록하지 않고, 우리를 거치지도 않습니다.",
    "<strong>ECS에 배포하는 경우의 AWS 자격 증명.</strong> 기존 AWS 설정이나 직접 수행한 "
    "로그인에서 읽어, 여러분 자신의 계정을 호출하는 데 쓰이며, 그 작업 동안만 메모리에 "
    "남습니다.",
   ]),
   ("네트워크 연결",
    "바깥으로 나가는 방향만이며, 그것도 여러분이 설정한 엔드포인트로만 갑니다. 여러분 자신의 "
    "런타임과, ECS 배포 경로를 쓰는 경우 여러분을 대신해 호출하는 Amazon의 API입니다. 다른 "
    "호스트에는 접속하지 않습니다. 업데이트 서비스도, 라이선스 확인도, 비콘도 없습니다.", []),
   ("우리가 받는 것",
    "없습니다. 여러분의 앱 사용과 관련된 서버도, 데이터베이스도, 로그도 우리에게 없습니다. "
    "지원을 위해 메일을 보내시면 받는 것은 그 메일의 내용뿐입니다. "
    '<a href="{p}support.html">지원</a>을 참고하십시오.', []),
   ("제3자",
    "앱은 여러분이 이미 소유한 인프라에 배포할 수 있도록 <code>kubectl</code>과 "
    "<code>ecsctl</code> 명령줄 도구를 포함합니다. 이들은 앱의 샌드박스 안에서 실행되며 "
    "여러분이 지정한 클러스터나 계정과만 통신합니다.<br><br>"
    f'앱이 배포하는 컨테이너 이미지는 <a href="{PTY}">openabdev/openab-pty</a>에서 '
    "빌드되며, <code>native</code>를 제외한 모든 variant에는 서드파티 coding CLI가 "
    "포함됩니다. 그 약관과 개인정보 처리 방식은 우리가 아니라 해당 벤더가 정합니다. 그 "
    "에이전트가 여러분의 코드나 프롬프트로 무엇을 하는지는 여러분과 그 벤더 사이의 "
    "문제입니다.", []),
   ("아동", "이 앱은 개발자 도구이며 아동을 대상으로 하지 않습니다.", []),
   ("변경",
    "이 방침이 바뀌면 위의 날짜도 함께 바뀌고, 이전 판은 이 페이지의 "
    f'<a href="{HISTORY}">git 이력</a>에 남습니다. 조용히 교체하지 않습니다.', []),
   ("연락처", f'<a href="mailto:{MAIL}">{MAIL}</a>', []),
  ]),
}

SUPPORT = {
 "en": dict(
  title="Support — OpenAB Connect",
  desc="How to try OpenAB Connect without deploying anything, and the failures worth "
       "knowing about in advance.",
  h1="Support",
  lead=f'<a href="mailto:{MAIL}">{MAIL}</a> — or open an issue at '
       f'<a href="{ISSUES}">openabdev/openab-pty</a> for anything about the runtime '
       "itself.",
  lead2=f'Security issues: please use <a href="{ADVISORY}">a private advisory</a> rather '
        "than a public issue or email.",
  demo_h="Trying the app without deploying anything",
  demo="Open the <strong>OpenAB Connect</strong> menu and choose <strong>Demo Mode</strong>. "
       "Two sample connections appear; double-click a session under either one to open a "
       "terminal. It is a canned transcript with local echo — no network connection is "
       "made and nothing is executed. Choose Demo Mode again to remove the samples.",
  wrong_h="Things that go wrong, and why",
  wrong=[
   ("The first deployment takes a long time",
    "It is pulling a container image, and the first pull of any agent variant is the slow "
    "part — measured at over two minutes for 156 MB on an ordinary connection. The app "
    "reports what it is waiting on. Nothing is wrong until it says so."),
   ("“No tailnet node appeared”",
    "Registration normally takes seconds, so this almost never means slowness. In order of "
    "likelihood: this Mac is signed out of the tailnet, or on a different one; the auth "
    "key was rejected — expired, already consumed, or not marked reusable; or a node of "
    "that name already exists, so the new one registered as <code>name-1</code>, which a "
    "non-ephemeral key does on every deploy.<br><br>Use a key that is both "
    "<strong>Reusable</strong> and <strong>Ephemeral</strong>. Ephemeral is what lets a "
    "deleted pod's node leave the tailnet instead of accumulating dead entries."),
   ("A session says it expired, or was taken over",
    "Sessions are single-attach by design: a second device attaching takes the keyboard. "
    "TTLs are set when you deploy. Both are reported with a specific reason rather than a "
    "generic disconnect."),
   ("The workspace lost my work",
    "The workspace is ephemeral unless you chose a persistent one at deploy time. It does "
    "not survive the pod being replaced. Push your work; lifecycle hooks are a backup, not "
    "a primary mechanism. The app says so in every session's header for this reason."),
   ("A process kept running after I killed a session",
    "Teardown is best-effort and labelled as such throughout. Only one kill domain is "
    "implemented, and a process that leaves its process group may outlive its session "
    "until the pod or task is replaced. This is documented behaviour, not a fault. To be "
    "certain nothing remains, delete the pod or task."),
  ],
  req_h="Requirements",
  req=["macOS 13 or later.",
       "A Kubernetes cluster or an AWS account you can deploy into.",
       "A Tailscale tailnet, and an auth key for it."],
  where_h="Where things live on your Mac",
  where_note="Removing the app leaves those; delete them if you want it gone entirely.",
 ),
 "zh": dict(
  title="支援 — OpenAB Connect",
  desc="如何在不部署任何東西的情況下試用 OpenAB Connect,以及值得事先知道的那些失敗情況。",
  h1="支援",
  lead=f'<a href="mailto:{MAIL}">{MAIL}</a> —— 或者,任何關於 runtime 本身的問題,'
       f'請在 <a href="{ISSUES}">openabdev/openab-pty</a> 開 issue。',
  lead2=f'安全性問題:請使用<a href="{ADVISORY}">私密 advisory</a>,'
        "不要開公開 issue 或寄信。",
  demo_h="不部署任何東西也能試用",
  demo="打開<strong>應用程式選單</strong>並選擇 <strong>Demo Mode</strong>。"
       "側邊欄會出現兩個範例連線;在其中任一個底下雙擊一個 session 就會開啟終端機。"
       "那是預錄的內容加上本機回顯 —— 不會建立任何網路連線,也不會執行任何東西。"
       "再選一次 Demo Mode 就會移除範例。",
  wrong_h="會出錯的事,以及為什麼",
  wrong=[
   ("第一次部署很久",
    "它在拉取容器映像,而任何 agent 版本的第一次拉取就是慢的那一段 —— 實測在普通連線下,"
    "156 MB 要超過兩分鐘。app 會回報它正在等什麼。在它說有問題之前,都不是有問題。"),
   ("「沒有出現 tailnet 節點」",
    "註冊正常只要幾秒,所以這幾乎不是「慢」。依可能性排序:這台 Mac 登出了 tailnet,"
    "或在另一個 tailnet 上;auth key 被拒絕 —— 過期、已被用掉,或沒有標記為可重複使用;"
    "或者同名節點已經存在,所以新的註冊成了 <code>name-1</code> —— "
    "非 ephemeral 的 key 每次部署都會這樣。<br><br>"
    "請使用同時是 <strong>Reusable</strong> 和 <strong>Ephemeral</strong> 的 key。"
    "Ephemeral 才能讓被刪掉的 pod 的節點離開 tailnet,而不是累積成一堆死掉的項目。"),
   ("session 說它過期了,或被接手了",
    "session 的設計是單一附加:第二台裝置接上就拿走鍵盤。TTL 在你部署時設定。"
    "這兩種情況都會回報具體原因,而不是一個籠統的斷線。"),
   ("workspace 把我的工作弄丟了",
    "除非你在部署時選了持久性的,workspace 是暫存的。它不會在 pod 被替換後存活。"
    "請把工作 push 出去;lifecycle hook 是備援,不是主要機制。"
    "app 在每個 session 的標題列都寫著這件事,原因就是這個。"),
   ("我殺掉 session 之後還有程序在跑",
    "teardown 是 best-effort,而且在每個地方都這樣標示。目前只實作了一層 kill domain,"
    "而離開自己 process group 的程序可能活得比它的 session 久,直到 pod 或 task 被替換。"
    "這是有記錄的行為,不是故障。要確定什麼都不剩,刪掉那個 pod 或 task。"),
  ],
  req_h="需求",
  req=["macOS 13 或以上。",
       "一個你能部署進去的 Kubernetes 叢集,或一個 AWS 帳號。",
       "一個 Tailscale tailnet,以及它的 auth key。"],
  where_h="東西在你 Mac 上的位置",
  where_note="移除 app 不會刪掉這些;如果你想完全清除,請自行刪除。",
 ),
 "ja": dict(
  title="サポート — OpenAB Connect",
  desc="何もデプロイせずに OpenAB Connect を試す方法と、"
       "前もって知っておく価値のある失敗の一覧。",
  h1="サポート",
  lead=f'<a href="mailto:{MAIL}">{MAIL}</a> — ランタイム自体に関することは '
       f'<a href="{ISSUES}">openabdev/openab-pty</a> に issue を立ててください。',
  lead2=f'セキュリティに関する問題は、公開 issue やメールではなく'
        f'<a href="{ADVISORY}">非公開のアドバイザリ</a>をお使いください。',
  demo_h="何もデプロイせずに試す",
  demo="<strong>アプリメニュー</strong>から <strong>Demo Mode</strong> を選びます。"
       "サンプル接続が 2 つ現れるので、どちらかのセッションをダブルクリックすると"
       "ターミナルが開きます。収録済みの内容とローカルエコーだけで、"
       "ネットワーク接続は行われず、何も実行されません。"
       "もう一度 Demo Mode を選ぶとサンプルは消えます。",
  wrong_h="うまくいかないこと、その理由",
  wrong=[
   ("最初のデプロイに時間がかかる",
    "コンテナイメージを取得しているところで、どの variant でも初回の取得が遅い部分です — "
    "通常の回線で 156 MB に 2 分以上かかることを実測しています。"
    "アプリは何を待っているかを表示します。そう表示されるまでは、異常ではありません。"),
   ("「tailnet ノードが現れません」",
    "登録は通常数秒なので、これが遅さを意味することはほぼありません。可能性の高い順に、"
    "この Mac が tailnet からサインアウトしている、または別の tailnet にいる。"
    "auth key が拒否された — 期限切れ、使用済み、または再利用可と設定されていない。"
    "あるいは同名のノードが既にあり、新しいものが <code>name-1</code> として登録された — "
    "ephemeral でない key は毎回これを起こします。<br><br>"
    "<strong>Reusable</strong> かつ <strong>Ephemeral</strong> の key を使ってください。"
    "Ephemeral であることが、削除された pod のノードを tailnet から離脱させ、"
    "死んだ項目が溜まるのを防ぎます。"),
   ("セッションが期限切れ、または引き継がれたと表示される",
    "セッションは設計上シングルアタッチで、2 台目が接続するとキーボードを持っていきます。"
    "TTL はデプロイ時に設定されます。どちらも一般的な切断ではなく、"
    "具体的な理由とともに表示されます。"),
   ("ワークスペースの作業が失われた",
    "デプロイ時に永続的なものを選んでいない限り、ワークスペースは一時的です。"
    "pod が置き換わると残りません。作業は push してください。"
    "ライフサイクルフックはバックアップであって主たる仕組みではありません。"
    "そのためアプリは各セッションのヘッダーで毎回そう明示しています。"),
   ("セッションを終了した後もプロセスが動き続けた",
    "終了処理は best-effort で、随所にそう明示しています。実装されている kill domain は"
    "1 つだけで、自分のプロセスグループを離れたプロセスは pod や task が置き換わるまで"
    "セッションより長く残ることがあります。これは仕様として記載された挙動で、"
    "不具合ではありません。何も残らないことを確実にするなら pod か task を削除してください。"),
  ],
  req_h="必要なもの",
  req=["macOS 13 以降。",
       "デプロイ先にできる Kubernetes クラスタ、または AWS アカウント。",
       "Tailscale の tailnet と、その auth key。"],
  where_h="Mac 上のどこに保存されるか",
  where_note="アプリを削除してもこれらは残ります。完全に消すなら手で削除してください。",
 ),
 "ko": dict(
  title="지원 — OpenAB Connect",
  desc="아무것도 배포하지 않고 OpenAB Connect를 사용해 보는 방법과, 미리 알아 둘 만한 "
       "실패 사례들.",
  h1="지원",
  lead=f'<a href="mailto:{MAIL}">{MAIL}</a> — 런타임 자체에 관한 것은 '
       f'<a href="{ISSUES}">openabdev/openab-pty</a>에 이슈를 남겨 주십시오.',
  lead2=f'보안 문제는 공개 이슈나 메일이 아니라 '
        f'<a href="{ADVISORY}">비공개 어드바이저리</a>를 이용해 주십시오.',
  demo_h="아무것도 배포하지 않고 사용해 보기",
  demo="<strong>앱 메뉴</strong>에서 <strong>Demo Mode</strong>를 선택합니다. 샘플 연결 두 "
       "개가 나타나고, 그중 하나의 세션을 두 번 클릭하면 터미널이 열립니다. 미리 녹화된 "
       "내용과 로컬 에코뿐이며 네트워크 연결도 하지 않고 아무것도 실행하지 않습니다. Demo "
       "Mode를 다시 선택하면 샘플이 사라집니다.",
  wrong_h="잘 안 되는 것들, 그리고 그 이유",
  wrong=[
   ("첫 배포가 오래 걸립니다",
    "컨테이너 이미지를 받아오는 중이며, 어떤 variant든 첫 내려받기가 느린 부분입니다 — "
    "일반 회선에서 156 MB에 2분 이상 걸리는 것을 측정했습니다. 앱은 무엇을 기다리는지 "
    "알려 줍니다. 그렇게 말하기 전까지는 문제가 아닙니다."),
   ("“tailnet 노드가 나타나지 않았습니다”",
    "등록은 보통 몇 초면 끝나므로 이것이 느림을 뜻하는 경우는 거의 없습니다. 가능성이 높은 "
    "순서대로, 이 Mac이 tailnet에서 로그아웃되어 있거나 다른 tailnet에 있습니다. auth key가 "
    "거부되었습니다 — 만료, 이미 사용됨, 또는 재사용 가능으로 표시되지 않음. 또는 같은 이름의 "
    "노드가 이미 있어 새 노드가 <code>name-1</code>로 등록되었습니다 — ephemeral이 아닌 키는 "
    "배포마다 이렇게 됩니다.<br><br><strong>Reusable</strong>이면서 "
    "<strong>Ephemeral</strong>인 키를 쓰십시오. Ephemeral이어야 삭제된 pod의 노드가 "
    "tailnet에서 빠져나가고, 죽은 항목이 쌓이지 않습니다."),
   ("세션이 만료되었다거나 다른 곳에서 가져갔다고 나옵니다",
    "세션은 설계상 단일 접속이며, 두 번째 기기가 붙으면 키보드를 가져갑니다. TTL은 배포할 때 "
    "설정됩니다. 두 경우 모두 일반적인 연결 끊김이 아니라 구체적인 이유와 함께 표시됩니다."),
   ("워크스페이스가 작업을 잃었습니다",
    "배포 시 영구 워크스페이스를 고르지 않았다면 워크스페이스는 임시입니다. pod이 교체되면 "
    "남지 않습니다. 작업은 push하십시오. 라이프사이클 훅은 백업이며 주된 수단이 아닙니다. "
    "그래서 앱이 모든 세션 헤더에 그렇게 적어 둡니다."),
   ("세션을 종료한 뒤에도 프로세스가 계속 돌았습니다",
    "종료 처리는 best-effort이며 곳곳에 그렇게 명시합니다. 구현된 kill domain은 하나뿐이고, "
    "자신의 프로세스 그룹을 벗어난 프로세스는 pod이나 task가 교체될 때까지 세션보다 오래 "
    "남을 수 있습니다. 이는 문서화된 동작이며 결함이 아닙니다. 아무것도 남지 않게 하려면 "
    "pod이나 task를 삭제하십시오."),
  ],
  req_h="요구 사항",
  req=["macOS 13 이상.",
       "배포할 수 있는 Kubernetes 클러스터 또는 AWS 계정.",
       "Tailscale tailnet과 그 auth key."],
  where_h="Mac에서 어디에 저장되는지",
  where_note="앱을 지워도 이것들은 남습니다. 완전히 없애려면 직접 삭제하십시오.",
 ),
}

PATHS = """~/Library/Containers/dev.openab.connect/     app data, sandboxed
Keychain (login)                             credentials, per connection"""


def doc(code, filename, title, desc, body):
    return f"""<!DOCTYPE html>
<html lang="{chrome.CHROME[code]["htmllang"]}" data-lang="{code}">
<head>
{chrome.head(code, filename, title, desc, og_type="article")}
</head>
<body>

{chrome.nav(code, filename)}

<div class="wrap doc">
{body}
</div>

{chrome.footer(code)}

</body>
</html>
"""


def privacy(code):
    d = PRIVACY[code]
    p = chrome.prefix(code)
    parts = [f'<h1>{d["h1"]}</h1>', f'<p class="date dim">{d["updated"]}</p>',
             f'<div class="panel"><p style="margin:0">{d["lead"]}</p></div>',
             f'<p>{d["intro"]}</p>']
    for head_, prose, items in d["sections"]:
        parts.append(f"<h2>{head_}</h2>")
        if prose:
            parts.append(f"<p>{prose.format(p=p)}</p>")
        if items:
            parts.append("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
    return doc(code, "privacy.html", d["title"], d["desc"], "\n".join(parts))


def support(code):
    d = SUPPORT[code]
    parts = [f'<h1>{d["h1"]}</h1>',
             f'<div class="panel"><p style="margin:0">{d["lead"]}</p>'
             f'<p style="margin:10px 0 0" class="dim">{d["lead2"]}</p></div>',
             f'<h2>{d["demo_h"]}</h2>', f'<p>{d["demo"]}</p>',
             f'<h2>{d["wrong_h"]}</h2>']
    for head_, prose in d["wrong"]:
        parts.append(f"<h3>{head_}</h3><p>{prose}</p>")
    parts.append(f'<h2>{d["req_h"]}</h2><ul>'
                 + "".join(f"<li>{i}</li>" for i in d["req"]) + "</ul>")
    parts.append(f'<h2>{d["where_h"]}</h2><pre>{PATHS}</pre>'
                 f'<p class="dim">{d["where_note"]}</p>')
    return doc(code, "support.html", d["title"], d["desc"], "\n".join(parts))


if __name__ == "__main__":
    for code in chrome.ORDER:
        for name, fn in (("privacy.html", privacy), ("support.html", support)):
            out = chrome.out_path(code, name)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(fn(code), encoding="utf-8")
            print(f"  wrote {out.relative_to(chrome.ROOT)}")
