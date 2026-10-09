"""コード逆引きの画像用 HTML（images.html）を作る。撮影は _memo/tools/shots.js（Puppeteer）で行う。"""
import json, os, re, subprocess, sys
from diagrams import ALL
from svg import SVG_CSS
from build_codemap import BASE_CSS, CROSSCUT, COMMIT

FEATURES = json.load(open("features.json"))
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = sys.argv[1] if len(sys.argv) > 1 else "code-map-images"

LOOKUPS = [
    ("lookup-web-bills", "機能の逆引き：公開サイト（議案を読む）", "web", ["公開サイト：議案を読む"]),
    ("lookup-web-interview", "機能の逆引き：公開サイト（AIチャット・インタビュー）", "web", ["公開サイト：AIチャット", "公開サイト：インタビュー"]),
    ("lookup-web-topics", "機能の逆引き：公開サイト（意見・トピック・オープンデータ）", "web", ["公開サイト：意見とトピック", "公開サイト：オープンデータ・連携"]),
    ("lookup-admin-bills", "機能の逆引き：管理画面（ログイン・議案）", "admin", ["管理画面：ログイン・管理者", "管理画面：議案"]),
    ("lookup-admin-interview", "機能の逆引き：管理画面（インタビュー）", "admin", ["管理画面：インタビュー"]),
    ("lookup-admin-topics", "機能の逆引き：管理画面（トピック分析・MCP）", "admin", ["管理画面：トピック分析", "管理画面：外部連携"]),
]

EXTRA = """
html, body { background: #fff; }
body { padding: 0; margin: 0; width: 1600px; font-size: 16px; }
.img { display: none; width: 1600px; padding: 56px 72px 72px; background: var(--bg); position: relative; }
.img.on { display: block; }
.img::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 14px; background: var(--teal); }
.ih { display: grid; gap: 6px; margin-bottom: 28px; }
.kick { font-family: var(--f-mono); font-size: 16px; color: var(--teal); font-weight: 600; }
.ih h1 { font-size: 44px; font-weight: 900; }
.ih p { font-size: 20px; color: var(--ink-soft); }
.ih p.prefix { font-family: var(--f-mono); font-size: 15px; }
.canvas { background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 24px; }
.canvas svg { display: block; width: 100%; height: auto; }
svg text { font-family: var(--f-body); }
svg .m { font-family: var(--f-mono); }
.cap { margin-top: 14px; font-size: 16px; color: var(--ink-soft); }
.lk table, .cc table { min-width: 0; font-size: 15px; background: var(--surface); border-radius: 12px; overflow: hidden; }
.lk th, .cc th { font-size: 13px; padding: 10px 14px; }
.lk td { padding: 12px 14px; }
.lk td.name b { font-size: 17px; display: block; line-height: 1.5; }
.lk td.name .u { font-family: var(--f-mono); font-size: 12.5px; color: var(--ink-soft); display: block; margin-top: 4px; overflow-wrap: anywhere; line-height: 1.5; }
.lk td.name .ctx { display: inline-block; margin-top: 8px; font-family: var(--f-mono); font-size: 12px; font-weight: 600; color: var(--surface); background: var(--teal); border-radius: 4px; padding: 0 8px; }
.lk.admin td.name .ctx { background: var(--blue); }
.lk td ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 2px; }
.lk td li { font-family: var(--f-mono); font-size: 12.5px; overflow-wrap: anywhere; line-height: 1.6; }
.lk td li .x { color: var(--ink-soft); }
.lk th.c-comp { color: var(--violet); } .lk th.c-load { color: var(--blue); } .lk th.c-svc { color: var(--teal); } .lk th.c-repo { color: var(--amber); }
.lk tr.grp td { background: var(--teal-wash); font-weight: 700; font-size: 14px; padding: 6px 14px; color: var(--teal); }
.lk.admin tr.grp td { background: var(--blue-wash); color: var(--blue); }
.cc td { font-size: 15px; padding: 11px 14px; } .cc td.p { font-size: 13px; }
.wm { position: absolute; right: 72px; bottom: 26px; font-family: var(--f-mono); font-size: 13px; color: var(--ink-soft); }
"""

CAPS = {
    "system": "AI はすべて Vercel AI Gateway 経由。重いトピック分析だけ Google Cloud の Cloud Run Job で動かす",
    "features": "web と admin は同じ名前の feature があっても中身は別物。共有したいロジックだけ packages/ に置く",
    "layers": "シンプルな feature は loaders → repositories だけのように、使わない層は省く",
    "requests": "A のキャッシュは「議案ID × むずかしさ」ごと。B の invalidateWebCache は投げっぱなし（失敗してもログだけ）",
    "data": "矢印は 親 → 子。全テーブルで RLS 有効・ポリシーなし。サーバーが Secret Key で読み書きする",
}


def build():
    secs = []
    for key, title, sub, fn in ALL:
        svg = re.sub(r'style="min-width:\d+px"', "", fn())
        secs.append(f'<section class="img" id="{key}"><div class="ih"><span class="kick">みらい議会 コード逆引き</span><h1>{title}</h1><p>{sub}</p></div><div class="canvas">{svg}</div><p class="cap">{CAPS[key]}</p></section>')
    for key, title, app, groups in LOOKUPS:
        secs.append(f'<section class="img" id="{key}" data-groups="{"|".join(groups)}" data-app="{app}"><div class="ih"><span class="kick">みらい議会 コード逆引き</span><h1>{title}</h1><p class="prefix"></p></div><div class="lk {app}"></div></section>')
    rows = "".join(f"<tr><td>{a}</td><td class=\"p\">{b}</td><td>{c}</td></tr>" for a, b, c in CROSSCUT)
    secs.append(f'<section class="img" id="crosscut"><div class="ih"><span class="kick">みらい議会 コード逆引き</span><h1>横断的な仕組みの場所</h1><p>認証・キャッシュ・AI・テストなど、機能をまたぐ仕組み</p></div><div class="cc"><table><thead><tr><th style="width:20%">知りたいこと</th><th style="width:42%">場所</th><th>メモ</th></tr></thead><tbody>{rows}</tbody></table></div></section>')
    js = r"""
const FEATURES = __F__;
const featOf = (p) => { const m = p.match(/features\/([^/]+)\//); return m ? m[1] : ""; };
const base = (p) => p.split("/").pop().replace(/\.tsx?$/, "");
const id = (location.hash || "#system").slice(1);
const sec = document.getElementById(id);
sec.classList.add("on");
document.querySelectorAll(".img").forEach((s) => { const w = document.createElement("div"); w.className = "wm"; w.textContent = "github.com/team-mirai/mirai-gikai ・ __C__"; s.append(w); });
if (sec.dataset.groups) {
  const groups = sec.dataset.groups.split("|");
  const app = sec.dataset.app;
  sec.querySelector(".prefix").textContent = app + "/src/features/<feature>/{server,client,shared}/…  ・ 色のラベルが主な feature。別 feature のファイルだけ「feature / 」を付けています ・ 拡張子は省略";
  const t = document.createElement("table");
  t.innerHTML = '<thead><tr><th style="width:22%">機能 / URL</th><th class="c-comp" style="width:22%">components・hooks</th><th class="c-load" style="width:22%">loaders・actions</th><th class="c-svc" style="width:34%">services・utils ／ <span style="color:var(--amber)">repositories</span> ・ packages</th></tr></thead>';
  const tb = document.createElement("tbody");
  for (const g of groups) {
    const fs = FEATURES.filter((f) => f.group === g);
    tb.insertAdjacentHTML("beforeend", '<tr class="grp"><td colspan="4">' + g + "</td></tr>");
    for (const f of fs) {
      const all = [...f.comp, ...f.load, ...f.svc, ...f.repo].map(featOf).filter(Boolean);
      const freq = {}; all.forEach((c) => (freq[c] = (freq[c] || 0) + 1));
      const main = Object.keys(freq).sort((a, b) => freq[b] - freq[a])[0] || "";
      const lab = (p) => {
        if (p.startsWith("packages/")) return '<span class="x">' + p.replace(/^packages\/([^/]+)\/src\/.*$/, "$1") + ' / </span>' + base(p);
        if (p.startsWith("worker/")) return '<span class="x">worker / </span>' + base(p);
        const c = featOf(p);
        if (!c) return '<span class="x">' + p.replace(/^(web|admin)\/src\//, "").replace(/[^/]+$/, "") + '</span>' + base(p);
        return (c !== main ? '<span class="x">' + c + ' / </span>' : "") + base(p);
      };
      const li = (arr, cls) => "<ul>" + arr.map((p) => '<li' + (cls ? ' style="color:var(--amber)"' : "") + ">" + lab(p) + "</li>").join("") + "</ul>";
      const tr = document.createElement("tr");
      tr.innerHTML = '<td class="name"><b></b><span class="u"></span>' + (main ? '<span class="ctx"></span>' : "") + "</td><td>" + li(f.comp) + "</td><td>" + li(f.load) + "</td><td>" + li(f.svc) + li(f.repo, 1) + li(f.pkg) + "</td>";
      tr.querySelector("b").textContent = f.name;
      tr.querySelector(".u").textContent = f.url;
      if (main) tr.querySelector(".ctx").textContent = main;
      tb.append(tr);
    }
  }
  t.append(tb);
  sec.querySelector(".lk").append(t);
}
document.fonts.ready.then(() => { document.body.dataset.h = Math.ceil(sec.getBoundingClientRect().height); });
""".replace("__F__", json.dumps(FEATURES, ensure_ascii=False)).replace("__C__", COMMIT)
    html = f'''<!doctype html><html lang="ja" data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{BASE_CSS}{SVG_CSS}{EXTRA}</style></head><body>
{"".join(secs)}
<script>{js}</script></body></html>'''
    open("images.html", "w").write(html)
    return [k for k, *_ in ALL] + [k for k, *_ in LOOKUPS] + ["crosscut"]


def shoot(ids):
    os.makedirs(OUT, exist_ok=True)
    url = "file://" + os.path.abspath("images.html")
    for i, key in enumerate(ids, 1):
        dom = subprocess.run([CH, "--headless=new", "--disable-gpu", "--window-size=1600,900", "--virtual-time-budget=5000", "--dump-dom", f"{url}#{key}"], capture_output=True, text=True).stdout
        h = int(re.search(r'data-h="(\d+)"', dom).group(1))
        out = os.path.abspath(f"{OUT}/{i:02d}-{key}.png")
        subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size=1600,{h}", "--virtual-time-budget=5000", f"--screenshot={out}", f"{url}#{key}"], capture_output=True)
        print(out, h)


if __name__ == "__main__":
    build()
    print("images.html を更新しました。撮影は cd ../../tools && npm run shots")
