"""AIインタビューの仕様書（HTML）を作る。コード逆引きと同じ見た目・図のヘルパーを使う。"""
from svg import Svg, SVG_CSS
from build_codemap import BASE_CSS, COMMIT


def flow_svg():
    s = Svg(1080, 400, "インタビューの全体フロー")
    s.group(14, 14, 1052, 170, "公開サイト（市民）", kind="teal")
    steps = [
        ("入口（LP）", ["説明・同意", "/interview"], "teal"),
        ("chat", ["AI が質問", "回答を保存"], "violet"),
        ("summary", ["レポート案を作成", "修正の要望を反映"], "violet"),
        ("提出", ["公開するか選ぶ", "/api/interview/complete"], "amber"),
        ("完了画面", ["公開設定の変更", "専門家登録"], "teal"),
    ]
    x = 34
    for i, (t, ls, k) in enumerate(steps):
        s.box(x, 60, 176, 96, t, ls, kind=k, size=15, sub_size=12, mono=t in ("chat", "summary"))
        if i < 4:
            s.arrow([(x + 176, 108), (x + 208, 108)])
        x += 208
    s.group(14, 206, 1052, 180, "サーバーと管理画面", kind="blue")
    s.box(450, 240, 210, 66, "モデレーション", ["0〜100 点で不適切さを採点"], kind="amber", size=14.5, sub_size=12)
    s.box(450, 316, 210, 56, "interview_report", ["＋ interview_opinion"], kind="amber", mono=True, size=13.5, sub_size=12)
    s.box(700, 240, 170, 66, "自動公開の判定", ["本人同意・29点以下", "充実度50以上"], kind="blue", size=14, sub_size=11.5)
    s.box(890, 240, 160, 66, "管理者の確認", ["公開／非公開", "一括公開・再採点"], kind="blue", size=14, sub_size=11.5)
    s.box(890, 316, 160, 56, "公開レポート", ["/report/[id]"], kind="teal", size=14, sub_size=12)
    s.box(40, 240, 200, 66, "インタビュー設定", ["モード・質問・AIモデル", "目安時間"], kind="blue", size=14.5, sub_size=11.5)
    s.box(260, 316, 170, 56, "トピック分析", ["公開・ok の意見だけ"], kind="gray", size=14, sub_size=11.5)
    s.arrow([(140, 240), (140, 200), (330, 200), (330, 156)], "設定を読む", at=(236, 194), kind="blue", dashed=True)
    s.arrow([(658, 156), (658, 200), (555, 200), (555, 240)])
    s.arrow([(555, 306), (555, 316)])
    s.arrow([(660, 273), (700, 273)])
    s.arrow([(870, 273), (890, 273)])
    s.arrow([(970, 306), (970, 316)])
    s.arrow([(450, 344), (430, 344)], dashed=True)
    return s.render()


def stage_svg():
    s = Svg(1080, 380, "ステージ遷移")
    s.box(60, 120, 200, 80, "chat", ["インタビュー中"], kind="violet", mono=True, size=17, sub_size=12.5)
    s.box(440, 120, 200, 80, "summary", ["レポート案の作成・修正"], kind="violet", mono=True, size=17, sub_size=12.5)
    s.box(820, 120, 200, 80, "summary_complete", ["本人が内容に同意"], kind="amber", mono=True, size=15, sub_size=12.5)
    s.arrow([(260, 145), (440, 145)], "LLM が next_stage=summary\n（質問を終えた・本人が終了を希望）", at=(350, 108), kind="violet")
    s.arrow([(440, 182), (260, 182)], "本人が再開を希望（LLM 判定）\nまたは「インタビューを続ける」ボタン", at=(350, 222))
    s.arrow([(640, 160), (820, 160)], "next_stage=summary_complete", at=(730, 150), kind="amber")
    s.arrow([(500, 120), (500, 84), (580, 84), (580, 120)], kind="violet")
    s.text(540, 74, "修正の要望 → summary のまま", size=12, anchor="middle")
    s.box(820, 248, 200, 56, "提出（complete API）", ["公開同意を選んで送信"], kind="teal", size=13.5, sub_size=11.5)
    s.arrow([(920, 200), (920, 248)])
    s.arrow([(110, 120), (110, 84), (210, 84), (210, 120)])
    s.text(160, 74, "回答ごとに次の質問", size=12, anchor="middle")
    s.text(60, 342, "chat→summary に変わった瞬間、ブラウザが自動で summary リクエストを1回送る（summary 中に summary が返っても再送しない）", size=12.5)
    s.text(60, 364, "レポートを作れなかった（report=null）ときは「インタビューを続ける」か「インタビューを終了する」（セッションをアーカイブ）を選ぶ", size=12.5)
    return s.render()


CSS = """
.spec-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }
.kv { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; display: grid; gap: 4px; }
.kv .k { font-size: 12px; color: var(--ink-soft); font-weight: 700; }
.kv .v { font-size: 15px; font-weight: 700; }
.kv .d { font-size: 13px; color: var(--ink-soft); }
.callout { background: var(--amber-wash); border: 1px dashed var(--amber); border-radius: 10px; padding: 12px 16px; font-size: 14px; max-width: 60em; }
.callout b { color: var(--amber); }
td code, li code { font-size: 12px; }
td.n { white-space: nowrap; font-weight: 700; }
ul.rules { margin: 0; padding-left: 1.3em; display: grid; gap: 4px; font-size: 14.5px; max-width: 60em; }
ol.qs { margin: 0; padding-left: 1.6em; display: grid; gap: 6px; font-size: 14.5px; }
ol.qs .qr { display: block; font-size: 12.5px; color: var(--ink-soft); }
.chap h3 { font-size: 17px; font-weight: 700; margin-top: 6px; }
"""


def table(head, rows, widths=None):
    th = "".join(f'<th{f" style=\"width:{w}\"" if w else ""}>{h}</th>' for h, w in zip(head, widths or [None] * len(head)))
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def chap(i, cid, title, lead, body):
    return f'''<section class="chap" id="{cid}">
  <div class="eyebrow">{i:02d}</div>
  <h2>{title}</h2>
  {f"<p>{lead}</p>" if lead else ""}
  {body}
</section>'''


def page():
    C = []
    C.append(("overview", "概要", "議案ごとに AI がインタビュアーになり、市民の経験や意見を聞き取って、レポート（要約・賛否・立場・意見）にまとめる機能です。集まった意見は、本人と運営の両方が公開を認めたものだけが公開され、トピック分析やオープンデータにも使われます。", f'''
  <div class="spec-grid">
    <div class="kv"><span class="k">対象</span><span class="v">議案ごとに1つの公開設定</span><span class="d">公開中の設定（status=public）は議案につき最大1つ</span></div>
    <div class="kv"><span class="k">回答者</span><span class="v">匿名ユーザー</span><span class="d">Supabase の匿名ログイン。メール登録なし</span></div>
    <div class="kv"><span class="k">AI</span><span class="v">既定は Claude Haiku 4.5</span><span class="d">設定ごとに変更可。AI Gateway 経由</span></div>
    <div class="kv"><span class="k">質問の進め方</span><span class="v">3モード</span><span class="d">bulk / loop / targeted</span></div>
    <div class="kv"><span class="k">成果物</span><span class="v">レポート＋意見（最大3件）</span><span class="d">interview_report と interview_opinion に保存</span></div>
    <div class="kv"><span class="k">公開条件</span><span class="v">本人の同意 × 管理者の公開</span><span class="d">条件を満たせば管理者公開は自動</span></div>
  </div>
  <figure><div class="diagram">{flow_svg()}</div></figure>'''))

    C.append(("screens", "画面と API", "公開サイト側の入口はすべて <code>/bills/[id]/interview</code> 配下と <code>/report/[reportId]</code> 配下です。プレビュー用には先頭に <code>/preview</code> が付いた同じ構成のページがあり、admin が発行したトークンが有効なときだけ非公開の議案・設定を使えます。", table(
        ["URL", "役割", "主な処理"],
        [
            ["<code>/bills/[id]/interview</code>", "入口（LP）", "説明、目安時間、開始前の同意。前回のセッションの状態でボタンが変わる（下表）"],
            ["<code>/bills/[id]/interview/disclosure</code>", "質問内容の開示", "AI に渡しているテーマ・質問・プロンプトの方針を公開"],
            ["<code>/bills/[id]/interview/chat</code>", "チャット", "セッションを取得または作成。メッセージが0件なら最初の質問をサーバーで生成して保存"],
            ["<code>POST /api/interview/chat</code>", "1往復の会話", "コスト上限チェック → 回答を保存 → 次の発言をストリーミングで返す"],
            ["<code>POST /api/interview/complete</code>", "提出", "持ち主チェック → レポート抽出 → モデレーション → 保存"],
            ["<code>/report/[reportId]/complete</code>", "完了画面", "公開設定の変更、専門家登録、リアクション"],
            ["<code>/report/[reportId]</code>", "公開レポート", "本人同意と管理者公開の両方がある場合だけ表示"],
            ["<code>/bills/[id]/opinions</code> ・ <code>/topics</code>", "みんなの意見", "公開レポートの回答者一覧とトピック分析"],
            ["<code>GET /api/open-data/interviews</code>", "オープンデータ", "二次利用の同意も条件に加えて配布（12章）"],
        ],
        ["30%", "16%", None],
    ) + table(
        ["前回のセッション", "入口のボタン", "動き"],
        [
            ["なし", "AIインタビューをはじめる", "同意モーダル → チャットへ"],
            ["進行中（active）", "AIインタビューを再開する", "同じセッションのチャットへ戻る"],
            ["完了（completed）", "もう一度新たに回答する", "確認なしで前のセッションをアーカイブし、新しいセッションのチャットへ。過去のレポートは入口ページの一覧から見られる"],
        ],
        ["22%", "34%", None],
    )))

    C.append(("config", "インタビュー設定（管理画面）", "設定は <code>interview_configs</code>、質問は <code>interview_questions</code> に保存します。管理画面の <code>/bills/[id]/interview</code> から作成・編集します。", table(
        ["項目", "値・制約", "説明"],
        [
            ["name", "1〜100文字", "設定名。1つの議案に複数の設定を作れる"],
            ["status", "<code>public</code> / <code>closed</code>", "public にすると、同じ議案の他の公開中の設定は自動で closed になる。議案が成立（enacted）に変わると公開中の設定は自動で closed"],
            ["mode", "<code>bulk</code> / <code>loop</code> / <code>targeted</code>", "質問の進め方（5章）"],
            ["chat_model", "選択肢から1つ、または未設定", "未設定なら Claude Haiku 4.5。summary フェーズも同じモデルを使う"],
            ["estimated_duration", "1〜180（分）、または未設定", "目安時間。未設定ならタイムマネジメントをしない"],
            ["themes", "文字列の配列", "インタビューのテーマ。プロンプトに入る"],
            ["prompt_overrides", "モードごと・節ごとに最大2000文字", "差し替えられるのは「話し方の注意事項（cautions）」と「深掘りの打ち切り基準（stopCriteria）」の2節だけ。空欄は既定文を使う"],
            ["deleted_at", "論理削除", "削除すると status=closed になり、その設定のレポートは一括で非公開（admin_unpublished_at を記録）"],
        ],
        ["18%", "28%", None],
    ) + "<h3>質問（interview_questions）</h3>" + table(
        ["項目", "値・制約", "説明"],
        [
            ["question", "1〜1000文字", "質問文"],
            ["follow_up_guide", "最大2000文字", "回答を受けた後の深掘りの指針。bulk モードではプロンプトに入れない"],
            ["quick_replies", "文字列の配列", "回答の選択肢ボタン。その質問をするときに AI が出力する"],
            ["target_audience", "最大500文字", "対象者の条件。targeted モードだけで使い、該当しない人にはスキップ"],
            ["question_order", "整数", "並び順。管理画面でドラッグして並べ替え"],
        ],
        ["18%", "22%", None],
    ) + '''<h3>設定づくりの補助</h3>
  <ul class="rules">
    <li><b>既定テンプレート（7問）</b>：Q1 関心のあるテーマ → Q2 立場・関わり方 → Q3 法案の認知度 → Q4 全体の評価 → Q5 Q1のテーマについて気になる点 → Q6 運用上のハードルと考慮の十分さ → Q7 制度を設計する人に伝えたいこと。Q1・Q2 の選択肢だけを議案ごとに AI が作り、末尾に「その他（自由記述）」を必ず付ける</li>
    <li><b>AI と対話して作る</b>（<code>POST /api/interview-config/generate</code>）：既定の質問 → 質問の提案 → 質問の確定 → テーマの提案 → テーマの確定、の順に進む</li>
    <li><b>複製</b>：同じ議案内、または別の議案へ質問ごとコピー。複製は必ず closed で作られる</li>
    <li><b>プレビュー</b>：トークン付きの URL を発行し、公開前の設定で実際にインタビューを試せる</li>
    <li><b>シミュレーション</b>（14章）：AI の回答者役で本番前に試運転できる</li>
  </ul>'''))

    C.append(("session", "セッションと会話の保存", "セッションは「インタビュー設定 × 匿名ユーザー」ごとに、進行中のものが1つになるように扱います。", table(
        ["状態", "条件", "主な遷移"],
        [
            ["active（進行中）", "archived_at も completed_at も空", "チャットページを開くと再開。メッセージ0件なら最初の質問を生成"],
            ["completed（完了）", "completed_at あり", "提出（complete API）の最後に記録"],
            ["archived（取り下げ）", "archived_at あり", "「やり直す」「もう一度新たに回答する」「インタビューを終了する（レポートなし）」で記録。以後は使われない"],
        ],
        ["20%", "30%", None],
    ) + '''<h3>1往復の処理（POST /api/interview/chat）</h3>
  <ol class="qs">
    <li>匿名ユーザーを確認（いなければ 401）。システム全体の日次・月次のコスト上限を確認</li>
    <li>プレビュートークンが有効なら管理用のローダー、それ以外は公開中の議案・設定だけを読むローダーを使う</li>
    <li>本人の日次コスト上限・設定・議案を並列で取得（上限チェックは失敗したら止める fail-closed）</li>
    <li>セッションを取得（なければ作成）→ <b>ユーザーの発言を先に保存</b> → 保存済みの全メッセージを取得</li>
    <li>保存済みの会話から「すでに聞いた質問ID」を集め、モードごとに次の質問を決める。目安時間があれば残り時間を計算</li>
    <li>システムプロンプトを組み立てて <code>streamText</code>（構造化出力）で生成し、テキストのストリームで返す</li>
    <li>生成し終わったら <b>AI の発言を保存</b>し、トークン数と利用額を <code>chat_usage_events</code> に記録（プロンプト名 <code>interview-chat</code> / <code>interview-summary</code>）</li>
  </ol>
  <div class="callout"><b>メモ</b>　Anthropic 系のモデルは会話が user の発言で終わる必要があるため、末尾が AI の発言のときは「続けて」などの合成メッセージを足してから渡します（DB には保存しません）。summary フェーズは会話の全文をシステムプロンプトに埋め込むので、モデルには末尾の1件だけを渡します。</div>'''))

    C.append(("modes", "3つのモード", "モードによって「次にどの質問をするか」を誰が決めるかと、深掘りのタイミングが変わります。", table(
        ["", "bulk（一括回答優先）", "loop（都度深掘り）", "targeted（対象者指定）"],
        [
            ["<b>次の質問</b>", "サーバーが「未回答の最初の質問」を決めて、プロンプトで<b>必ずその質問をする</b>よう指示", "AI に任せる（サーバーは指定しない）", "AI に任せる"],
            ["<b>深掘り</b>", "全問を聞き終えてから、まとめて深掘り", "回答のたびに2〜3問の追加質問", "loop と同じ"],
            ["<b>follow_up_guide</b>", "プロンプトに入れない", "入れる", "入れる"],
            ["<b>target_audience</b>", "使わない", "使わない", "会話から該当するか判定し、該当しなければスキップ"],
            ["<b>summary への移行</b>", "未回答の質問が残っていれば必ず chat のまま", "概ね聞き終えて十分に深掘りしたら", "対象者に該当する質問を終えたら"],
        ],
        ["14%", None, None, None],
    ) + '''<h3>プロンプトに入るもの（全モード共通）</h3>
  <ul class="rules">
    <li>役割（半構造化デプスインタビューの熟練インタビュアー）、責任、話し方の注意事項、専門知識レベルの見きわめ、深掘りテクニック、打ち切り基準、事前定義質問の使い方</li>
    <li>議案の名前・タイトル・要約・本文、ナレッジソース、テーマ、事前定義質問（ID・質問文・クイックリプライ）</li>
    <li><b>誤認の補足</b>：回答が法案の実際の内容と違う前提なら、否定せずに短く補足してから意見を聞き直す</li>
    <li><b>タイムマネジメント</b>：残り目安時間と残り質問数。時間を超えたら、本人が望めばすぐ summary へ</li>
    <li><b>ステージ遷移の指示</b>と、聞き終えた質問・未回答の質問の一覧</li>
    <li>最初の質問だけは「温かい挨拶を2文程度 → 法案名を伝える → すぐに1問目（クイックリプライと question_id も出す）」という追加指示を付ける</li>
  </ul>'''))

    C.append(("stages", "ステージ遷移", "ステージは <code>chat</code> → <code>summary</code> → <code>summary_complete</code> の3つです。遷移は AI が毎回の出力の <code>next_stage</code> で判断し、ブラウザがそれに従います。", f'<figure><div class="diagram">{stage_svg()}</div></figure>'))

    C.append(("output", "AI の出力形式", "どちらのフェーズも zod スキーマによる構造化出力（JSON）で生成し、そのままストリーミングで返します。", table(
        ["フェーズ", "フィールド", "内容"],
        [
            ["chat", "<code>text</code>", "AI の発言"],
            ["", "<code>quick_replies</code>", "選択肢ボタン。選ばせる聞き方のときは必ず出す"],
            ["", "<code>question_id</code>", "事前定義質問をするときだけ、その ID。進捗と「聞いた質問」の判定に使う"],
            ["", "<code>topic_title</code>", "事前定義質問のテーマ（20文字以内）。画面上部に表示"],
            ["", "<code>next_stage</code>", "<code>chat</code> または <code>summary</code>"],
            ["summary", "<code>text</code>", "AI の発言（質問はしない。再開するときだけ次の質問を1つ）"],
            ["", "<code>report</code>", "レポート案（下表）。chat に戻すときは null"],
            ["", "<code>next_stage</code>", "<code>summary</code> / <code>summary_complete</code> / <code>chat</code>"],
        ],
        ["14%", "22%", None],
    ) + "<h3>レポート（report）</h3>" + table(
        ["フィールド", "形式", "ルール"],
        [
            ["summary", "100文字程度", "本人の主張を、かぎかっこで書けるような話し言葉で。「〜すべき」などの強い表現は使わない"],
            ["stance", "<code>for</code> / <code>against</code> / <code>neutral</code>", "neutral は期待と懸念の両方がある場合"],
            ["role", "4種類から1つ", "<code>subject_expert</code> 専門的な有識者 ／ <code>work_related</code> 業務に関係 ／ <code>daily_life_affected</code> 暮らしに影響 ／ <code>general_citizen</code> 一般的な関心"],
            ["role_title", "10文字以内", "例：物流業者、主婦、教師。過去の職歴なら「元〜」"],
            ["role_description", "文章", "本人の発言だけを根拠に経歴・専門性を書く"],
            ["opinions", "最大3件", "議案を検討する人にとって有益な順。本人の発言だけを根拠にし、言っていない要望や賛成に格上げしない"],
            ["content_richness", "0〜100 ×5", "総合（total）・論点の明確さ・具体性・影響への言及・提案の広がり と根拠。<b>本人には表示しない</b>"],
        ],
        ["18%", "24%", None],
    ) + "<h3>意見（opinions の1件）</h3>" + table(
        ["フィールド", "内容"],
        [
            ["title ・ content", "40文字以内 ・ 120文字以内"],
            ["source_message_id", "根拠になった本人の発言の ID（会話ログに <code>[msg_id:…]</code> として渡す）"],
            ["contextual_quote", "その発言からの逐語引用だけ。要約・結合・補完をしない。個人名などは含めない。切り出せなければ null"],
            ["bill_sentiment", "「期待」「懸念」または null"],
            ["richness", "この意見単体の情報充実度（0〜100）。引用の具体性も含めて評価"],
            ["concern ・ proposal", "懸念の要点 ・ 本人が明示した要望の要点（各20〜50字、なければ null）"],
            ["reasoning_types", "根拠の種類（自分の体験・身近な人の観察・職業上の知見・研究や統計・海外事例・直感・なし）"],
        ],
        ["24%", None],
    )))

    C.append(("ui", "チャット画面の補助機能", None, table(
        ["機能", "仕様"],
        [
            ["クイックリプライ", "AI が出した選択肢をボタンで表示。押すとその文言を送信"],
            ["進捗バー", "chat 中は「聞き終えた事前定義質問 ÷ 全質問 × 80%」、summary は 90%、summary_complete は 100%。上に現在のトピック名"],
            ["スキップメニュー", "chat 中だけ表示。「次の質問に進む」「他に言いたいことがある」「インタビューを終了する」を選ぶと、その文言を送信"],
            ["タイマー", "目安時間があるときだけ。開始時刻から残り分数を10秒ごとに再計算"],
            ["時間超過の案内", "「目安時間を超過しましたが、インタビューを続けてもよいですか？」→「インタビューを続ける」／「終了してレポートを作成」"],
            ["エラー時", "自動で1回だけ再送。それでも失敗したら「もう一度お試しください」と手動の再送ボタン"],
            ["やり直す", "確認ダイアログの後、セッションをアーカイブして新しいチャットへ"],
            ["レポートを作れなかったとき", "「お話しいただいた内容が短く…」と表示し、「インタビューを続ける」か「インタビューを終了する」を選ぶ"],
            ["評価", "星1〜5。3以下なら理由タグ（質問が的外れ／話が噛み合わない／言いたいことと違う／質問が多い／その他）を選べる"],
        ],
        ["22%", None],
    )))

    C.append(("complete", "提出と完了処理", "summary でレポート案が表示されると「レポート内容に同意して提出」ボタンが出ます。押すと公開の同意を聞くモーダルが開き、どちらかを選ぶと <code>POST /api/interview/complete</code> を呼びます。", '''<ol class="qs">
    <li><b>持ち主チェック</b>：セッションの user_id と、今の匿名ユーザーが一致しない場合は 403</li>
    <li><b>レポートの取り出し</b>：保存済みの AI の発言を新しい順に見て、最初に見つかった report を使う（なければエラー）</li>
    <li><b>モデレーション</b>：要約・意見・立場・会話全体を AI（既定 GPT-5.2）が 0〜100 点で採点し、理由も保存。<b>30秒でタイムアウト</b>し、失敗してもレポートの保存は止めない（点数は空のまま）</li>
    <li><b>レポートの保存</b>（upsert）：公開同意・二次利用の同意・自動公開の判定結果も一緒に保存。再提出のときは意見の再抽出の印を消す</li>
    <li><b>意見の保存</b>：意見を1件ずつ <code>interview_opinion</code> にも入れる（トピック分析用）。失敗しても完了は止めず、あとでバックフィルが取りこむ</li>
    <li><b>セッションを完了</b>：completed_at を記録し、完了画面 <code>/report/[id]/complete</code> へ</li>
  </ol>'''))

    C.append(("publish", "公開のルール", "レポートの公開は3つの値で決まります。表示してよいのは <b>本人の同意（is_public_by_user）と管理者の公開（is_public_by_admin）の両方が true</b> のときだけです。", table(
        ["値", "誰が変える", "説明"],
        [
            ["is_public_by_user", "本人", "提出時の公開同意。完了画面からいつでも切り替えられる"],
            ["is_public_by_admin", "自動 または 管理者", "自動公開の条件を満たすと true。管理者が個別・一括で切り替える"],
            ["admin_unpublished_at", "管理者", "管理者が非公開にした記録。これがあると、本人が公開に切り替えても自動では再公開しない"],
            ["is_data_reuse_consented", "本人", "オープンデータとしての第三者提供への同意。公開同意と連動して送る"],
        ],
        ["24%", "18%", None],
    ) + table(
        ["ルール", "条件"],
        [
            ["モデレーションの区分", "<code>ok</code>：29点以下 ／ <code>warning</code>：30〜69点 ／ <code>ng</code>：70点以上（DB の generated column）"],
            ["自動公開（提出時・本人の公開切り替え時）", "本人が公開に同意 かつ モデレーション 29点以下 かつ 情報充実度（total）50以上"],
            ["管理者の一括公開", "設定ごとに、本人同意あり・未公開・モデレーション点数と充実度が指定の範囲、のレポートをまとめて公開"],
            ["設定を削除したとき", "その設定のレポートをすべて非公開にし、admin_unpublished_at を記録"],
            ["トピック分析の対象", "本人同意 × 管理者公開 × モデレーション ok のレポートの意見だけ"],
            ["オープンデータ", "本人同意 × 管理者公開 × 二次利用の同意。さらに公開レポートが20件以上ある議案だけ"],
        ],
        ["30%", None],
    )))

    C.append(("consent", "同意と専門家登録", None, '''<h3>開始前（AIインタビュー同意事項）</h3>
  <ul class="rules">
    <li>回答データは党内での政策検討に利用する</li>
    <li>個人情報や機密情報の記載は控える</li>
    <li>回答後に公開を許可するか選べ、許可した場合はみらい議会に全文が掲載される場合がある</li>
    <li>利用規約とプライバシーポリシーへの同意 →「同意してはじめる」</li>
  </ul>
  <h3>提出時（公開設定）</h3>
  <ul class="rules">
    <li>許可すると、意見の要約とインタビュー原文が匿名で掲載されることがある</li>
    <li>「公開を許可して提出する」／「非公開で提出する」。非公開でも党内の政策検討には使う</li>
    <li>公開の許可は、オープンデータとしての二次利用の同意も兼ねる（データ利用規約へのリンクつき）</li>
  </ul>
  <h3>専門家登録</h3>
  <ul class="rules">
    <li>レポートの role が <code>subject_expert</code> か <code>work_related</code> のとき、完了画面に有識者リストへの登録を案内</li>
    <li>入力：お名前（100文字以内）・ご所属・肩書（200文字以内）・メールアドレス・プライバシーポリシーへの同意</li>
    <li><code>expert_registrations</code> に保存し、管理画面の <code>/experts</code> で確認</li>
  </ul>'''))

    C.append(("safety", "コスト・安全・権限", None, table(
        ["項目", "仕様"],
        [
            ["本人の1日の利用額", "<code>CHAT_DAILY_USER_COST_LIMIT_USD</code>（既定 0.5ドル）。AI チャットと共通。超えたら会話できない"],
            ["全体の利用額", "1日 <code>CHAT_DAILY_TOTAL_COST_LIMIT_USD</code>（既定 50ドル）、1か月 <code>CHAT_MONTHLY_TOTAL_COST_LIMIT_USD</code>（既定 1000ドル）"],
            ["利用額の記録", "AI Gateway が返す実費（取れなければトークン数から計算）を <code>chat_usage_events</code> に保存"],
            ["本人確認", "匿名ユーザーの ID とセッションの user_id の一致で判定（チャット・提出・評価・公開設定の変更）"],
            ["非公開データの保護", "プレビュートークンがないリクエストは、公開中の議案・設定しか読めない"],
            ["プロンプトインジェクション対策", "モデレーションなどで利用者の文章を AI に渡すときは、指示（system）とデータ（user）を分け、毎回ランダムな区切り行で囲む"],
            ["トレース", "Langfuse にリクエスト単位のトレース ID、セッション ID、議案 ID、ステージを送る"],
        ],
        ["26%", None],
    )))

    C.append(("admin", "管理画面の運用機能", None, table(
        ["画面", "できること"],
        [
            ["レポート一覧 <code>…/interview/[configId]/reports</code>", "並べ替え（メッセージ数・充実度・参考になった数・モデレーション点数など）、状態・公開・賛否・立場・モデレーションでの絞りこみ、ページ送り"],
            ["統計", "件数・完了数、賛否と立場の内訳、平均の評価と充実度、メッセージ数、所要時間（中央値・合計、1時間以上を除いた合計）、評価の理由タグの件数、質問ごとの回答数"],
            ["レポート詳細", "会話ログ、公開／非公開の切り替え、モデレーション・充実度の採点やり直し、メッセージへのリンクのコピー"],
            ["一括操作", "一括モデレーション採点（<code>/api/batch/moderation-scoring</code>）、条件つき一括公開、TSV 出力"],
            ["発言の検索 <code>…/reports/search</code>", "回答者の発言をキーワード検索"],
            ["シミュレーション", "AI が回答者役（ペルソナ）を最大10人ぶん並列で演じて模擬インタビュー（1本最大20ターン）。ペルソナは既存レポートか議案の内容から作り、AI が満足度と全体の評価をまとめる"],
        ],
        ["26%", None],
    )))

    C.append(("files", "主なファイル", None, table(
        ["役割", "場所"],
        [
            ["チャット API ・ 1往復の処理", "<code>web/src/app/api/interview/chat/route.ts</code><br><code>web/src/features/interview-session/server/services/handle-interview-chat-request.ts</code>"],
            ["最初の質問", "<code>web/src/features/interview-session/server/services/generate-initial-question.ts</code><br><code>…/server/loaders/initialize-interview-chat.ts</code>"],
            ["モード別ロジック", "<code>web/src/features/interview-session/server/utils/interview-logic/</code><br><code>…/shared/utils/interview-logic/</code>"],
            ["プロンプト本文", "<code>packages/shared/src/interview-prompts/</code>（bulk / loop / targeted / summary / stage-transition-guidance）"],
            ["出力スキーマ", "<code>web/src/features/interview-session/shared/schemas.ts</code><br><code>packages/shared/src/interview-report/schema.ts</code>"],
            ["チャット画面", "<code>web/src/features/interview-session/client/components/interview-chat-client.tsx</code><br><code>…/client/hooks/use-interview-chat.ts</code>"],
            ["提出・完了", "<code>web/src/app/api/interview/complete/route.ts</code><br><code>…/server/services/complete-interview-session.ts</code>"],
            ["公開ルール", "<code>packages/shared/src/report-publication/auto-publish.ts</code><br><code>packages/shared/src/moderation/moderation.ts</code>"],
            ["設定の編集（admin）", "<code>admin/src/features/interview-config/</code>"],
            ["レポート管理（admin）", "<code>admin/src/features/interview-reports/</code>"],
            ["シミュレーション（admin）", "<code>admin/src/features/interview-simulation/</code>"],
        ],
        ["24%", None],
    )))

    toc = "".join(f'<li><a href="#{cid}"><span class="n">{i + 1}</span>{t}</a></li>' for i, (cid, t, *_ ) in enumerate(C))
    body = "".join(chap(i + 1, cid, t, lead, b) for i, (cid, t, lead, b) in enumerate(C))
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AIインタビュー仕様</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{BASE_CSS}{SVG_CSS}{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div class="repo">github.com/team-mirai/mirai-gikai ・ {COMMIT}</div>
  <h1>AIインタビュー仕様</h1>
  <p class="lead">みらい議会の AI インタビューについて、設定・会話の進め方・レポートの形式・公開のルールを、いまのコードから読み取ってまとめたものです。数値や文言はすべてコード上の値です。</p>
  <ul class="toc">{toc}</ul>
</header>
{body}
</div>
</body>
</html>'''


if __name__ == "__main__":
    open("AIインタビュー仕様.html", "w").write(page())
    print("ok")
