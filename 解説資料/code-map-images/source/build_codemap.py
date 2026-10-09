import json
from diagrams import ALL
from svg import SVG_CSS

COMMIT = "develop @ 99840c65（2026-10-06）"
FEATURES = json.load(open("features.json"))

BASE_CSS = """
:root {
  --bg: #f7f4ee; --surface: #ffffff; --ink: #1f2937; --ink-soft: #5b6470; --line: #ddd6c8;
  --teal: #0f8472; --teal-wash: #e2f3ef; --blue: #2f6db5; --blue-wash: #e3edf9;
  --amber: #a86a00; --amber-wash: #fbf0d9; --violet: #6a4fb3; --violet-wash: #ece6f8;
  --f-body: "Noto Sans JP", "Hiragino Sans", "Yu Gothic", sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #12161a; --surface: #1b2127; --ink: #e6e9ec; --ink-soft: #a3acb5; --line: #313a42;
    --teal: #4fcdb7; --teal-wash: #15352f; --blue: #7fb0ec; --blue-wash: #182b42;
    --amber: #f0b552; --amber-wash: #382a10; --violet: #b49cf0; --violet-wash: #2a2240; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #12161a; --surface: #1b2127; --ink: #e6e9ec; --ink-soft: #a3acb5; --line: #313a42;
  --teal: #4fcdb7; --teal-wash: #15352f; --blue: #7fb0ec; --blue-wash: #182b42;
  --amber: #f0b552; --amber-wash: #382a10; --violet: #b49cf0; --violet-wash: #2a2240; color-scheme: dark;
}
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 15px; line-height: 1.8; margin: 0; padding-inline: 16px; padding-block: 0 72px; }
.wrap { max-width: 1120px; margin: 0 auto; }
h1, h2, h3 { text-wrap: balance; line-height: 1.4; margin: 0; }
p { margin: 0; }
a { color: var(--teal); }
:focus-visible { outline: 3px solid var(--teal); outline-offset: 2px; }
code { font-family: var(--f-mono); font-size: 0.86em; background: var(--teal-wash); padding: 1px 6px; border-radius: 4px; overflow-wrap: anywhere; }
header.top { padding-block: 44px 24px; display: grid; gap: 12px; border-bottom: 1px solid var(--line); }
.repo { font-family: var(--f-mono); font-size: 13px; color: var(--teal); }
header.top h1 { font-size: clamp(28px, 4.6vw, 40px); font-weight: 900; }
.lead { color: var(--ink-soft); max-width: 48em; }
.toc { display: flex; flex-wrap: wrap; gap: 6px; list-style: none; padding: 0; margin: 4px 0 0; }
.toc a { display: inline-block; text-decoration: none; font-size: 13px; color: var(--ink); background: var(--surface); border: 1px solid var(--line); border-radius: 999px; padding: 3px 12px; }
.toc a:hover { border-color: var(--teal); }
.toc .n { font-family: var(--f-mono); color: var(--teal); margin-right: 6px; font-size: 12px; }
section.chap { padding-block: 40px 4px; display: grid; gap: 16px; scroll-margin-top: 8px; }
.eyebrow { font-family: var(--f-mono); font-size: 12px; color: var(--teal); letter-spacing: 0.08em; }
.chap h2 { font-size: clamp(20px, 3vw, 26px); font-weight: 900; margin-top: -8px; }
.chap > p { max-width: 52em; color: var(--ink-soft); }
figure { margin: 0; }
figcaption { font-size: 12.5px; color: var(--ink-soft); margin-top: 6px; }
.diagram { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 12px; }
.diagram svg { display: block; width: 100%; height: auto; }
svg text { font-family: var(--f-body); }
svg .m { font-family: var(--f-mono); }
.tw { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }
table { border-collapse: collapse; width: 100%; min-width: 640px; font-size: 13.5px; }
th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-size: 12px; color: var(--ink-soft); background: var(--bg); font-weight: 700; }
tr:last-child td { border-bottom: none; }
td.p { font-family: var(--f-mono); font-size: 12px; color: var(--teal); overflow-wrap: anywhere; }
"""

PAGE_CSS = """
.finder { position: sticky; top: 0; z-index: 2; background: var(--bg); padding-block: 10px; display: grid; gap: 10px; border-bottom: 1px solid var(--line); }
.search { display: flex; gap: 10px; align-items: center; }
.search input { flex: 1; min-width: 0; font: inherit; font-size: 15px; padding: 9px 14px; border-radius: 10px; border: 1px solid var(--line); background: var(--surface); color: var(--ink); }
.search .count { font-family: var(--f-mono); font-size: 12.5px; color: var(--ink-soft); white-space: nowrap; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chips button { font: inherit; font-size: 12.5px; padding: 3px 12px; border-radius: 999px; border: 1px solid var(--line); background: var(--surface); color: var(--ink-soft); cursor: pointer; }
.chips button[aria-pressed="true"] { background: var(--teal); border-color: var(--teal); color: var(--surface); }
.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; font-family: var(--f-mono); font-size: 11.5px; }
.group-h { font-size: 13px; font-weight: 700; color: var(--ink-soft); margin-top: 18px; display: flex; gap: 10px; align-items: center; }
.group-h::after { content: ""; flex: 1; border-top: 1px dashed var(--line); }
.feats { display: grid; gap: 10px; }
.feat { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 18px; display: grid; gap: 8px; min-width: 0; }
.feat-h { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: baseline; }
.feat-h h3 { font-size: 16px; font-weight: 700; }
.app { font-family: var(--f-mono); font-size: 11px; font-weight: 600; padding: 1px 8px; border-radius: 4px; }
.app.web { background: var(--teal-wash); color: var(--teal); }
.app.admin { background: var(--blue-wash); color: var(--blue); }
.url { font-family: var(--f-mono); font-size: 12.5px; color: var(--ink-soft); overflow-wrap: anywhere; }
.feat .desc { font-size: 13.5px; color: var(--ink-soft); }
dl.layers { margin: 0; display: grid; grid-template-columns: 128px minmax(0, 1fr); gap: 4px 12px; font-size: 12.5px; }
dl.layers dt { font-family: var(--f-mono); font-size: 11px; padding-top: 3px; font-weight: 600; }
dl.layers dd { margin: 0; display: flex; flex-wrap: wrap; gap: 4px 6px; min-width: 0; }
.c-entry { color: var(--ink-soft); } .c-comp { color: var(--violet); } .c-load { color: var(--blue); }
.c-svc { color: var(--teal); } .c-repo { color: var(--amber); } .c-pkg { color: var(--ink-soft); }
.fp { font-family: var(--f-mono); font-size: 12px; background: var(--bg); border: 1px solid var(--line); border-radius: 5px; padding: 0 7px; cursor: pointer; color: var(--ink); overflow-wrap: anywhere; text-align: left; max-width: 100%; }
.fp:hover { border-color: var(--teal); }
.fp .d { color: var(--ink-soft); }
.fp.copied { border-color: var(--teal); background: var(--teal-wash); }
.empty { color: var(--ink-soft); padding: 20px 0; }
@media (max-width: 560px) { dl.layers { grid-template-columns: 1fr; } dl.layers dt { padding-top: 6px; } }
"""

LAYER_KEYS = [
    ("entry", "page / route", "c-entry"),
    ("comp", "components・hooks", "c-comp"),
    ("load", "loaders・actions", "c-load"),
    ("svc", "services・utils", "c-svc"),
    ("repo", "repositories", "c-repo"),
    ("pkg", "packages", "c-pkg"),
]

CROSSCUT = [
    ("admin のログイン判定", "admin/src/middleware.ts<br>admin/src/lib/auth/permissions.ts", "未ログイン・roles に admin がない人は /login へ。/api/mcp だけは Bearer トークンで別判定"),
    ("Server Action の認可", "admin/src/features/auth/server/lib/auth-server.ts", "actions の先頭で requireAdmin()。mirai-stance の3つの action だけは呼んでおらず middleware 頼み"),
    ("Google ログインで admin を自動付与", "supabase/migrations/20260427100000_auto_admin_role_for_google_workspace_users.sql", "team-mir.ai ドメインの Google ログインなら roles: admin を付ける DB 関数"),
    ("市民の本人確認（匿名ユーザー）", "web/src/features/chat/client/hooks/use-anonymous-supabase-user.ts<br>web/src/features/chat/server/utils/supabase-server.ts", "ブラウザで匿名ログインし、API 側で user を取り出す。インタビューの持ち主チェックにも使う"),
    ("web のキャッシュ", "web/src/lib/cache-tags.ts<br>web/src/features/*/server/loaders/*.ts", "loader で unstable_cache（議案は600秒）。タグは bills / diet-sessions / interview-configs / public-interview-reports"),
    ("admin から web のキャッシュを消す", "admin/src/lib/utils/cache-invalidation.ts<br>web/src/app/api/revalidate/route.ts", "タグ名は両方に同じ値を書いて同期している"),
    ("AI モデルの名前", "packages/shared/src/ai/models.ts", "AI Gateway 形式（openai/gpt-5.2 など）。用途ごとの既定モデルもここ"),
    ("AI チャットのプロンプト", "web/src/lib/prompt/index.ts<br>web/src/lib/prompt/source-code/", "チャット用はソースコード内、それ以外は Langfuse から取得"),
    ("インタビューのプロンプト部品", "packages/shared/src/interview-prompts/", "モード別（bulk / loop / targeted）と共通セクション。admin のプレビューとも共有"),
    ("AI の利用額と上限", "web/src/features/chat/server/services/cost-tracker.ts<br>…/system-cost-guard.ts<br>web/src/lib/ai/calculate-ai-cost.ts", "1人あたりの日次、全体の日次・月次。CHAT_*_COST_LIMIT_USD"),
    ("LLM のトレース", "web/src/lib/telemetry/register.ts", "OpenTelemetry → Langfuse。route.ts の先頭で明示的に初期化"),
    ("モデレーション（不適切チェック）", "packages/shared/src/moderation/<br>web/src/features/interview-session/server/services/evaluate-moderation-score.ts", "レポート保存時に採点。ok / warning / ng は DB の generated column"),
    ("信頼できない入力を AI に渡すとき", "packages/shared/src/prompt-safety/untrusted-content.ts", "利用者の文章を区切って、指示として読まれないようにする"),
    ("ルート（URL）の定義", "web/src/lib/routes.ts<br>admin/src/lib/routes.ts", "リンクは文字列で書かずここの関数を使う。routes.test.ts が page.tsx と同期を検査"),
    ("環境変数", "web/src/lib/env.ts<br>admin/src/lib/env.ts<br>.env.example", "process.env はここに集約"),
    ("DB の型", "packages/supabase/types/supabase.types.ts", "pnpm db:types:gen で生成。マイグレーションとセットでコミット"),
    ("DB 関数（RPC）のテスト", "tests/supabase/db-function/", "migrations で関数を足したらここに統合テスト。ローカルの Supabase を実際に使う"),
    ("MCP ツールのテスト", "tests/mcp/", "ツールごとに実 DB で検証"),
    ("UI 部品の見本", "web/src/app/dev/", "開発中だけ見られるプレビュー。本番は 404"),
    ("Basic 認証（staging など）", "web/src/lib/basic-auth.ts", "設定があるときだけ、HTML のページ遷移にだけかける"),
    ("Cloud Run Job の起動", "admin/src/lib/cloud-run-job.ts<br>infra/cloud-run/provision.sh", "サービスアカウントの鍵で jobs:run を呼ぶ。インフラ作成はスクリプト"),
    ("CI とデプロイ", ".github/workflows/", "code_check / integration_test / deploy（DB → Vercel）/ deploy_worker / supabase_preview"),
]


def svgs():
    return {k: (title, sub, fn()) for k, title, sub, fn in ALL}


def crosscut_table():
    rows = "".join(f"<tr><td>{a}</td><td class=\"p\">{b}</td><td>{c}</td></tr>" for a, b, c in CROSSCUT)
    return f'<table><thead><tr><th style="width:22%">知りたいこと</th><th style="width:40%">場所</th><th>メモ</th></tr></thead><tbody>{rows}</tbody></table>'


CAPTIONS = {
    "system": "ローカルでは Supabase を npx supabase start で起動し、web は :3000、admin は :3001 で動きます。worker は worker/run-local.sh で手元実行もできます。",
    "features": "feature 名は web と admin で同じものがあります（bills、interview-config など）が、中身は別物です。共通にしたいロジックだけ packages/ に置きます。",
    "layers": "シンプルな feature は loaders → repositories だけ、のように一部の層を省きます。詳しいルールは docs/repository-layer.md と AGENTS.md にあります。",
    "requests": "A の unstable_cache は「議案ID × むずかしさ」ごとに保存されます。B の invalidateWebCache は await せずに投げっぱなしです（失敗してもログだけ）。",
    "data": "矢印は「親 → 子（子が外部キーで親を参照）」の向きです。すべてのテーブルで RLS を有効にし、ポリシーは作りません。ブラウザから直接は読めず、サーバーが Secret Key で読み書きします。",
}

LEADS = {
    "system": "Next.js のアプリが2つ（公開用 web と管理用 admin）で、データは Supabase に集まります。AI はすべて Vercel AI Gateway 経由です。重いトピック分析だけは Google Cloud の Cloud Run Job で動かします。",
    "features": "アプリごとに <code>src/features/</code> の下が機能単位で分かれています（Bulletproof React 方式）。web と admin の間ではコードを import せず、共有したいものは <code>packages/</code> に出します。",
    "layers": "1つの feature の中は server / client / shared の3つに分かれ、server の中はさらに役割ごとのフォルダになっています。矢印の向きに呼び出します。",
    "requests": "読み取り・書きこみ・AI の3パターンを押さえると、ほとんどの機能が読めます。",
    "data": "テーブルは <code>supabase/migrations/</code> の SQL（108ファイル）で作られます。中心は <code>bills</code> で、インタビューとトピック分析がそこにぶら下がります。",
}


def page():
    d = svgs()
    toc = [(k, d[k][0]) for k in d] + [("lookup", "機能の逆引き"), ("crosscut", "横断的な仕組みの場所")]
    toc_html = "".join(f'<li><a href="#{k}"><span class="n">{i + 1}</span>{t}</a></li>' for i, (k, t) in enumerate(toc))
    chaps = []
    for i, (k, (title, sub, svg)) in enumerate(d.items()):
        chaps.append(f'''<section class="chap" id="{k}">
  <div class="eyebrow">{i + 1:02d}</div>
  <h2>{title}</h2>
  <p>{LEADS[k]}</p>
  <figure><div class="diagram">{svg}</div><figcaption>{CAPTIONS[k]}</figcaption></figure>
</section>''')
    legend = "".join(f'<span class="{c}">{lab}</span>' for _, lab, c in LAYER_KEYS)
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>みらい議会 コード逆引き</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{BASE_CSS}{SVG_CSS}{PAGE_CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div class="repo">github.com/team-mirai/mirai-gikai ・ {COMMIT}</div>
  <h1>みらい議会 コード逆引き</h1>
  <p class="lead">構成図でシステムの全体像をつかんでから、「この機能のコードはどこ？」を画面や API の単位で引けるようにしたリファレンスです。逆引きのファイルパスはクリックでコピーできます。</p>
  <ul class="toc">{toc_html}</ul>
</header>
{"".join(chaps)}
<section class="chap" id="lookup">
  <div class="eyebrow">06</div>
  <h2>機能の逆引き</h2>
  <p>画面や API ごとに、関係する主なファイルを呼び出しの順に並べています。page.tsx から import をたどって作ったもので、すべて今の develop に実在します。機能名・URL・ファイル名のどれでも検索できます。</p>
  <div class="finder">
    <div class="search">
      <input id="q" type="search" placeholder="例：賛否、interview、/api/chat、repository" aria-label="機能を検索" autocomplete="off">
      <span class="count" id="count"></span>
    </div>
    <div class="chips" id="chips" role="group" aria-label="アプリで絞りこむ">
      <button type="button" data-app="all" aria-pressed="true">すべて</button>
      <button type="button" data-app="web" aria-pressed="false">web</button>
      <button type="button" data-app="admin" aria-pressed="false">admin</button>
    </div>
    <div class="legend">{legend}</div>
  </div>
  <div id="results"></div>
</section>
<section class="chap" id="crosscut">
  <div class="eyebrow">07</div>
  <h2>横断的な仕組みの場所</h2>
  <p>認証・キャッシュ・AI・テストなど、機能をまたいで使う仕組みの置き場所です。</p>
  <div class="tw">{crosscut_table()}</div>
</section>
</div>
<script>
const FEATURES = {json.dumps(FEATURES, ensure_ascii=False)};
const LAYERS = {json.dumps([[k, l, c] for k, l, c in LAYER_KEYS], ensure_ascii=False)};
const short = (p) => p.replace(/^(web|admin)\\/src\\/features\\//, "$1:").replace(/^packages\\//, "pkg:");
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({{"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}})[c]);
const q = document.getElementById("q"), results = document.getElementById("results"), count = document.getElementById("count");
let app = "all";
try {{ const saved = localStorage.getItem("gikai-lookup-app"); if (saved) app = saved; }} catch (e) {{}}
function render() {{
  const term = q.value.trim().toLowerCase();
  const hit = FEATURES.filter((f) => (app === "all" || f.app === app) && (!term || [f.name, f.url, f.desc, f.group, ...LAYERS.flatMap(([k]) => f[k])].join(" ").toLowerCase().includes(term)));
  count.textContent = hit.length + " / " + FEATURES.length + " 件";
  if (!hit.length) {{ results.innerHTML = '<p class="empty">見つかりませんでした。別のことばで探してみてください。</p>'; return; }}
  let html = "", g = "";
  for (const f of hit) {{
    if (f.group !== g) {{ if (g) html += "</div>"; g = f.group; html += '<div class="group-h">' + esc(g) + '</div><div class="feats">'; }}
    html += '<article class="feat"><div class="feat-h"><span class="app ' + f.app + '">' + f.app + '</span><h3>' + esc(f.name) + '</h3><span class="url">' + esc(f.url) + '</span></div><p class="desc">' + esc(f.desc) + '</p><dl class="layers">';
    for (const [k, label, c] of LAYERS) {{
      if (!f[k].length) continue;
      html += '<dt class="' + c + '">' + label + '</dt><dd>' + f[k].map((p) => {{ const s = short(p); const i = s.lastIndexOf("/"); return '<button type="button" class="fp" data-path="' + esc(p) + '" title="' + esc(p) + '"><span class="d">' + esc(s.slice(0, i + 1)) + '</span>' + esc(s.slice(i + 1)) + '</button>'; }}).join("") + '</dd>';
    }}
    html += "</dl></article>";
  }}
  results.innerHTML = html + "</div>";
}}
document.getElementById("chips").addEventListener("click", (e) => {{
  const b = e.target.closest("button"); if (!b) return;
  app = b.dataset.app;
  try {{ localStorage.setItem("gikai-lookup-app", app); }} catch (err) {{}}
  syncChips(); render();
}});
function syncChips() {{ document.querySelectorAll("#chips button").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.app === app))); }}
results.addEventListener("click", async (e) => {{
  const b = e.target.closest(".fp"); if (!b) return;
  try {{ await navigator.clipboard.writeText(b.dataset.path); b.classList.add("copied"); setTimeout(() => b.classList.remove("copied"), 900); }} catch (err) {{}}
}});
q.addEventListener("input", render);
syncChips(); render();
</script>
</body>
</html>'''


if __name__ == "__main__":
    open("コード逆引き.html", "w").write(page())
    print("ok")
