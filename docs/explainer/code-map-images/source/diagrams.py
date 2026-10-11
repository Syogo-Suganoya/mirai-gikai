from svg import Svg


def system():
    s = Svg(1080, 610, "システム構成図")
    # 利用者
    s.group(14, 14, 186, 540, "使う人・外部")
    s.box(30, 60, 154, 60, "市民", ["ブラウザ・スマホ"], kind="gray")
    s.box(30, 170, 154, 60, "外部の開発者", ["オープンデータ"], kind="gray")
    s.box(30, 340, 154, 60, "運営メンバー", ["管理画面"], kind="gray")
    s.box(30, 450, 154, 60, "AIエージェント", ["Claude など（MCP）"], kind="gray")
    # アプリ（Vercel）
    s.group(222, 14, 300, 540, "Vercel（Next.js 15 / React 19）", kind="teal")
    s.lbox(240, 44, 264, 206, "web（公開サイト）", [
        "議案・会期・インタビュー・レポート",
        "`/api/chat",
        "`/api/interview/chat · complete",
        "`/api/open-data/*",
        "`/api/revalidate",
        "`/preview/* （トークン付き）",
    ], kind="teal")
    s.lbox(240, 316, 264, 220, "admin（管理画面 :3001）", [
        "議案・解説・賛否・会期・タグ",
        "インタビュー設定・レポート公開",
        "シミュレーション・採点",
        "`/api/mcp （MCPサーバー）",
        "`/api/user-topic-analysis/*",
        "`middleware.ts → roles: admin",
    ], kind="blue")
    s.arrow([(184, 90), (240, 90)])
    s.arrow([(184, 200), (240, 200)], "JSON", at=(212, 192), lsize=10.5)
    s.arrow([(184, 370), (240, 370)])
    s.arrow([(184, 480), (240, 480)], "MCP", at=(212, 472), lsize=10.5)
    # admin -> web revalidate
    s.arrow([(440, 316), (440, 250)], "`POST /api/revalidate", at=(430, 278), anchor="end", kind="blue")
    s.text(430, 296, "保存したらキャッシュを消す", size=11, anchor="end")
    # 中央列
    s.group(560, 14, 270, 540, "データ・AI", kind="amber")
    s.lbox(578, 44, 234, 96, "Vercel AI Gateway", ["OpenAI / Anthropic / Google", "`shared/src/ai/models.ts"], kind="violet", sub_size=11.5)
    s.box(578, 158, 234, 44, "Langfuse", ["LLM のトレース・一部のプロンプト"], kind="gray", size=13.5, sub_size=11)
    s.lbox(578, 236, 234, 196, "Supabase", [
        "PostgreSQL",
        "  RLS は有効・ポリシーなし",
        "  サーバーが Secret Key で読み書き",
        "Auth：市民は匿名ログイン",
        "  admin はメール / Google",
        "Storage：議案のサムネイル",
    ], kind="amber", sub_size=12)
    s.arrow([(504, 80), (578, 80)], kind="violet")
    s.arrow([(504, 180), (578, 180)], dashed=True)
    s.arrow([(504, 236), (540, 236), (540, 300), (578, 300)])
    s.arrow([(504, 400), (578, 400)])
    s.arrow([(504, 340), (548, 340), (548, 124), (578, 124)], kind="violet", dashed=True)
    # 右列
    s.group(866, 14, 200, 540, "Google Cloud", kind="blue")
    s.lbox(882, 236, 168, 132, "Cloud Run Job", ["`worker/src/main.ts", "トピック分析", "意見の再抽出", "タグの付け直し"], kind="blue", sub_size=12)
    s.box(882, 430, 168, 56, "Cloud Scheduler", ["毎日 6:00 analyze-all"], kind="gray", size=13.5, sub_size=11.5)
    s.arrow([(966, 430), (966, 368)])
    s.arrow([(882, 330), (812, 330)])
    s.arrow([(900, 236), (812, 110)], kind="violet")
    s.arrow([(504, 512), (848, 512), (848, 350), (882, 350)], "`jobs:run （GCP_SA_KEY）", at=(676, 504), kind="blue")
    # CI
    s.lbox(14, 566, 1052, 36, "GitHub Actions：", [], kind="gray", size=13)
    s.text(150, 594, "code_check（Biome・型・build・test）→ develop/main で DB マイグレーション → Vercel Deploy Hook ／ worker イメージ → Cloud Run Job", size=12.5)
    return s.render()


def features():
    s = Svg(1080, 560, "フィーチャーとパッケージの依存図")
    s.group(14, 14, 1052, 150, "web/src/features/（公開サイト・10）", kind="teal")
    web = ["bills", "bill-difficulty", "diet-sessions", "chat", "interview-config", "interview-session",
           "interview-report", "report-reaction", "user-topic-analysis", "open-data"]
    x, y = 32, 48
    for name in web:
        w = len(name) * 7.8 + 22
        if x + w > 1050:
            x, y = 32, y + 36
        s.chip(x, y, name, kind="teal", w=w)
        x += w + 10
    s.text(32, 140, "app/ の page.tsx と route.ts から呼ばれる。web と admin はおたがいを import しない", size=12)

    s.group(14, 184, 1052, 186, "admin/src/features/（管理画面・17）", kind="blue")
    adm = ["auth", "admins", "bills", "bills-edit", "mirai-stance", "diet-sessions", "tags", "interview-config",
           "interviews", "interview-reports", "interview-simulation", "experts", "topic-analysis",
           "user-topic-analysis", "analysis-viewer", "interview-opinion-backfill", "mcp"]
    x, y = 32, 218
    for name in adm:
        w = len(name) * 7.8 + 22
        if x + w > 1050:
            x, y = 32, y + 36
        s.chip(x, y, name, kind="blue", w=w)
        x += w + 10
    s.text(32, 352, "mcp は他の feature の repository / service を呼んで、ツールとして公開する", size=12)

    s.group(14, 400, 830, 146, "packages/（web・admin・worker から import する共有パッケージ）", kind="amber")
    s.box(32, 434, 150, 96, "@mirai-gikai/seed", ["ローカル用の", "テストデータ投入"], kind="gray", mono=True, size=12.5)
    s.box(200, 434, 186, 96, "@mirai-gikai/supabase", ["`createAdminClient()", "生成した DB の型"], kind="amber", mono=True, size=13)
    s.box(404, 434, 186, 96, "@mirai-gikai/shared", ["AIモデル名・プロンプト部品", "モデレーション・意見の保存"], kind="amber", mono=True, size=13)
    s.box(608, 434, 210, 96, "topic-analysis-core", ["トピック分析の本体", "公開用の読み出しも提供"], kind="amber", mono=True, size=13)
    s.box(870, 434, 180, 96, "worker/", ["Cloud Run Job の", "エントリポイント"], kind="blue", mono=True, size=13)
    s.arrow([(870, 482), (818, 482)])
    s.arrow([(608, 482), (590, 482)])
    s.arrow([(404, 482), (386, 482)])
    s.arrow([(182, 482), (200, 482)])
    return s.render()


def layers():
    s = Svg(1080, 470, "feature 内のレイヤー構成")
    s.box(20, 40, 170, 78, "app/…/page.tsx", ["params を受け取って", "feature に渡すだけ"], kind="gray", mono=True, size=13.5)
    s.box(20, 160, 170, 78, "app/api/…/route.ts", ["API の入口", "認証・入力チェック"], kind="gray", mono=True, size=13.5)
    s.box(230, 40, 170, 78, "server/components", ["Server Component", "画面を組み立てる"], kind="violet", mono=True, size=13.5)
    s.box(440, 20, 180, 66, "server/loaders", ["読む・unstable_cache"], kind="teal", mono=True, size=13.5)
    s.box(440, 104, 180, 66, "server/actions", ['"use server"・書く'], kind="blue", mono=True, size=13.5)
    s.box(660, 60, 180, 78, "server/services", ["ビジネスロジック", "AI 呼び出し・副作用"], kind="amber", mono=True, size=13.5)
    s.box(880, 60, 180, 78, "server/repositories", ["Supabase 呼び出しだけ", "find* / create* / update*"], kind="amber", mono=True, size=13)
    s.box(880, 190, 180, 50, "Supabase", ["`createAdminClient()"], kind="ink", size=13.5)
    s.arrow([(190, 79), (230, 79)])
    s.arrow([(400, 66), (440, 56)])
    s.arrow([(400, 92), (440, 130)])
    s.arrow([(620, 52), (650, 52), (650, 84), (660, 84)])
    s.arrow([(620, 137), (650, 137), (650, 114), (660, 114)])
    s.arrow([(840, 99), (880, 99)])
    s.arrow([(970, 138), (970, 190)])
    s.arrow([(190, 199), (640, 199), (640, 130), (660, 130)], "route.ts から services を直接呼ぶ", at=(420, 192))
    s.arrow([(620, 40), (860, 40), (860, 80), (880, 80)], "簡単な読み取りは loader → repository", at=(740, 34), dashed=True)
    # client
    s.box(230, 290, 200, 78, "client/components", ['"use client"', "操作・状態を持つ部品"], kind="violet", mono=True, size=13.5)
    s.box(470, 290, 170, 78, "client/hooks", ["fetch・ストリーム受信", "楽観的更新"], kind="violet", mono=True, size=13.5)
    s.arrow([(330, 290), (330, 250), (520, 250), (520, 170)], "Server Action を呼ぶ", at=(420, 244), kind="blue")
    s.arrow([(555, 368), (555, 400), (105, 400), (105, 238)], "fetch で /api を呼ぶ（チャットは ストリーム）", at=(330, 394), kind="violet")
    s.arrow([(430, 329), (470, 329)])
    s.box(690, 290, 370, 90, "shared/types · shared/utils", ["サーバーとブラウザの両方で使える純粋関数", "DB や API に触らない → *.test.ts を同じ場所に置く"], kind="teal", mono=True, size=13.5)
    s.text(20, 450, "server 側のファイルは先頭に import \"server-only\"。共通ロジックを web と admin の両方で使うときは packages/ に切り出す（同じコードを2か所に置かない）", size=12.5)
    return s.render()


def requests():
    s = Svg(1080, 640, "リクエストの流れ")
    # A 読み取り
    s.group(14, 14, 1052, 170, "A. 読み取り：議案の詳細ページ /bills/[id]", kind="teal")
    st = [
        ("page.tsx", ["`bills/[id]/page.tsx", "params を await"]),
        ("getBillById()", ["`loaders/get-bill-by-id.ts", "unstable_cache 600秒", "tag: bills"]),
        ("bill-repository", ["議案・賛否・本文・タグ", "を Promise.all で並列"]),
        ("hideUnpublishedStance", ["キャッシュの外で", "予約公開の時刻を判定"]),
        ("BillDetailLayout", ["Server Component", "→ client の部品へ"]),
    ]
    x = 30
    for i, (t, ls) in enumerate(st):
        s.box(x, 52, 190, 112, t, ls, kind="teal" if i != 2 else "amber", size=13.5, sub_size=11.5, mono=True)
        if i < len(st) - 1:
            s.arrow([(x + 190, 108), (x + 206, 108)])
        x += 206
    # B 書きこみ
    s.group(14, 200, 1052, 190, "B. 書きこみ：admin でチームみらいの賛否を保存 → web に反映", kind="blue")
    st = [
        ("stance-form", ['"use client"', "react-hook-form"]),
        ("create-stance", ["Server Action", "zod で入力チェック"]),
        ("mirai-stance-repository", ["`mirai_stances に insert"]),
        ("cache-invalidation", ["`POST {web}/api/revalidate", "Bearer REVALIDATE_SECRET"]),
        ("web: revalidateTag", ['"bills" タグを無効化', "次のアクセスで取り直す"]),
    ]
    x = 30
    for i, (t, ls) in enumerate(st):
        s.box(x, 238, 190, 112, t, ls, kind="blue" if i < 4 else "teal", size=13 if len(t) > 18 else 13.5, sub_size=11.5, mono=True)
        if i < len(st) - 1:
            s.arrow([(x + 190, 294), (x + 206, 294)])
        x += 206
    s.text(30, 376, "議案の保存（update-bill）では、状態によってインタビューの自動クローズなどの副作用もまとめて services/update-bill-with-side-effects.ts で行う", size=12)
    # C AI
    s.group(14, 406, 1052, 222, "C. AI ストリーミング：インタビューのチャット", kind="violet")
    st = [
        ("use-interview-chat", ["ブラウザ", "匿名ユーザーで fetch"]),
        ("/api/interview/chat", ["日次・月次のコスト上限", "をチェック"]),
        ("handleInterview…", ["設定・議案・セッション", "を並列取得 → 発言保存", "モード別に次の質問"]),
        ("streamText()", ["AI Gateway 経由", "Langfuse にトレース", "利用額を記録"]),
        ("/api/interview/complete", ["レポート抽出", "モデレーション採点", "report + opinion 保存"]),
    ]
    x = 30
    for i, (t, ls) in enumerate(st):
        s.box(x, 444, 190, 120, t, ls, kind="violet" if i != 4 else "amber", size=13, sub_size=11.5, mono=True)
        if i < len(st) - 1:
            s.arrow([(x + 190, 504), (x + 206, 504)])
        x += 206
    s.arrow([(442 + 190 + 16 + 95, 564), (742, 594), (125, 594), (125, 564)], "回答はストリームで少しずつ返る（next_stage もいっしょに出力）", at=(430, 588), dashed=True, kind="violet")
    return s.render()


def data():
    s = Svg(1080, 600, "データモデル（主なテーブル）")
    def t(x, y, name, sub=None, kind="gray", w=200, h=None):
        h = h or (48 if sub else 34)
        s.box(x, y, w, h, name, [sub] if sub else [], kind=kind, mono=True, size=13, sub_size=11)
    s.group(14, 14, 316, 300, "議案まわり", kind="teal")
    t(436, 28, "bills", "publish_status・status・slug", kind="teal", w=230, h=52)
    t(40, 44, "diet_sessions", "会期・is_active")
    t(40, 102, "bill_contents", "normal / hard の本文")
    t(40, 160, "tags", "bills_tags で多対多")
    t(40, 218, "mirai_stances", "賛否・理由・publish_at")
    t(40, 276 - 6, "preview_tokens", None)
    s.arrow([(240, 62), (436, 46)], kind="teal")
    s.add('<path class="ar a-teal" d="M436,66 L300,66 L300,287"/>')
    for y in (126, 184, 242, 287):
        s.arrow([(300, y), (240, y)], kind="teal")
    s.group(350, 104, 490, 340, "インタビュー", kind="violet")
    t(380, 140, "interview_configs", "mode・chat_model・status", kind="violet", w=212)
    t(612, 140, "interview_questions", "順番・追加質問の方針", w=212)
    t(380, 218, "interview_sessions", "user_id・開始/完了", kind="violet", w=212)
    t(612, 210, "interview_messages", None, w=212)
    t(612, 254, "interview_rating_feedbacks", None, w=212)
    t(380, 300, "interview_report", "要約・立場・公開フラグ", kind="violet", w=212)
    t(612, 304, "report_reactions", "参考になった", w=212)
    t(380, 380, "interview_opinion", "意見1件=1行・タグ", kind="amber", w=212)
    s.arrow([(520, 80), (520, 104), (486, 104), (486, 140)], kind="violet")
    s.arrow([(592, 164), (612, 164)])
    s.arrow([(486, 188), (486, 218)])
    s.arrow([(592, 236), (602, 236), (602, 227), (612, 227)])
    s.arrow([(592, 250), (602, 250), (602, 271), (612, 271)])
    s.arrow([(486, 266), (486, 300)])
    s.arrow([(592, 324), (612, 324)])
    s.arrow([(486, 348), (486, 380)])
    s.group(860, 14, 206, 430, "トピック分析（新）", kind="amber")
    t(874, 140, "topic_analysis_version", "status・is_published", kind="amber", w=180)
    t(874, 230, "topic", "parent_topic_id で2階層", w=180)
    t(874, 320, "topic_opinion", "topic × 意見", w=180)
    s.arrow([(666, 54), (964, 54), (964, 140)], kind="amber")
    s.arrow([(964, 188), (964, 230)])
    s.arrow([(964, 278), (964, 320)])
    s.arrow([(592, 404), (850, 404), (850, 344), (874, 344)], kind="amber")
    s.group(14, 334, 316, 252, "利用者・記録", kind="gray")
    t(40, 370, "auth.users", "匿名ユーザーもここ", kind="ink")
    s.text(40, 440, "user_id で参照される:", size=11.5)
    s.text(40, 458, "`interview_sessions · report_reactions", size=11)
    s.text(40, 476, "`chat_usage_events · expert_registrations", size=11)
    t(40, 494, "chat_usage_events", "トークン数・利用額(USD)")
    t(40, 548, "api_rate_limits", None)
    s.group(350, 464, 716, 122, "旧トピック分析（インタビュー設定ごと・admin の5ステップ版）", kind="gray")
    for x, n in ((366, "topic_analysis_versions"), (596, "topic_analysis_topics"), (826, "topic_analysis_classifications")):
        s.box(x, 504, 226, 34, n, [], kind="gray", mono=True, size=12)
    s.text(366, 568, "新しい分析は topic_analysis_version（単数形）側。名前が似ているので注意", size=12)
    return s.render()


ALL = [
    ("system", "システム構成", "web・admin・Supabase・AI・Cloud Run のつながり", system),
    ("features", "フィーチャーマップ", "features/ の分け方と packages/ への依存", features),
    ("layers", "レイヤー構成", "1つの feature の中の server / client / shared", layers),
    ("requests", "リクエストの流れ", "読み取り・書きこみ・AI ストリーミングで通るファイル", requests),
    ("data", "データモデル", "supabase/migrations で作られる主なテーブル", data),
]
