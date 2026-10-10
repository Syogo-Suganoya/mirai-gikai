"""X 投稿用の画像シリーズ（エンジニア向け：4テーマ×4枚＝16枚）の HTML を作る。
内容は主に 中学生向け_しくみ図鑑.html（一部はコード逆引き）から取り、画面は assets/screens のスクショを使う。

見た目は x-images/source/slides.html と同じ（CSS をそのまま読みこむ）。
撮影は 解説資料/tools で `npm run shots`。posts.html の section を1枚ずつ撮る。

    python3 build_posts.py   # → posts.html
"""
import os

from icons import icon

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(HERE, "../../x-images/source/slides.html")
_src = open(SLIDES).read()
BASE_CSS = _src.split("<style>")[1].split("</style>")[0]
FONT_LINK = _src[_src.index("<link rel=\"stylesheet\""): _src.index("<style>")]

EXTRA_CSS = """
.tile .ic svg { width: 34px; height: 34px; color: #fff; }
.tile.a .ic { background: var(--amber); }
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin-top: 44px; }
.grid3 .tile { padding: 30px 28px; min-height: 230px; grid-template-columns: 1fr; gap: 14px; }
.grid3 .tile b { font-size: 26px; }
.grid3 .tile p { font-size: 19px; }
.grid2 { gap: 28px; margin-top: 56px; }
.grid2 .tile { min-height: 236px; padding: 44px 40px; grid-template-columns: 72px 1fr; gap: 22px; }
.grid2 .tile .ic { width: 72px; height: 72px; border-radius: 18px; }
.grid2 .tile .ic svg { width: 38px; height: 38px; }
.grid2 .tile b { font-size: 32px; }
.grid2 .tile p { font-size: 23px; line-height: 1.6; margin-top: 8px; }
.sub + .grid2 { margin-top: 36px; gap: 24px; }
.sub + .grid2 .tile { min-height: 206px; padding: 36px 40px; }
.flow { margin-top: 56px; }
.flow .st { min-height: 390px; }
.flow .st b { font-size: 26px; word-break: keep-all; overflow-wrap: anywhere; }
.flow.c4 .st b { font-size: 28px; }
.flow .st p { font-size: 20px; }
.flow.c4 { grid-template-columns: repeat(4, 1fr); gap: 22px; }
.st .si { width: 40px; height: 40px; color: var(--teal-dark); }
.cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin-top: 40px; }
.colc { padding: 30px 30px 34px; display: grid; gap: 12px; align-content: start; min-height: 420px; }
.colc .ci { width: 52px; height: 52px; border-radius: 14px; background: var(--violet); display: grid; place-items: center; }
.colc .ci svg { width: 30px; height: 30px; color: #fff; }
.colc .en { font-family: var(--f-en); font-size: 20px; font-weight: 700; color: var(--violet); }
.colc b { font-size: 30px; font-weight: 900; }
.colc p { font-size: 20px; color: var(--ink-soft); line-height: 1.6; }
.colc ul { list-style: none; display: grid; gap: 8px; margin-top: 4px; }
.colc li { font-size: 19px; line-height: 1.5; padding-left: 22px; position: relative; }
.colc li::before { content: ""; position: absolute; left: 0; top: 11px; width: 10px; height: 10px; border-radius: 50%; background: var(--violet); }
.vis { padding: 32px 34px; display: grid; gap: 18px; }
.vis h3 { font-size: 24px; font-weight: 900; display: flex; align-items: center; gap: 10px; }
.vis h3 svg { width: 28px; height: 28px; color: var(--teal-dark); }
.vis .row { display: grid; grid-template-columns: 150px 1fr; gap: 14px; align-items: start; font-size: 19px; line-height: 1.5; }
.vis .row .k { font-weight: 700; color: var(--teal-dark); }
.chips2 { display: flex; flex-wrap: wrap; gap: 10px; }
.chips2 span { font-size: 19px; font-weight: 700; padding: 6px 16px; border-radius: 999px; background: var(--mint); color: var(--teal-dark); }
.chips2 span.neg { background: #fdecec; color: var(--red); }
.chips2 span.gray { background: #eef1f4; color: var(--ink-soft); }
.cmp { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.cmp div { border-radius: 14px; padding: 18px 20px; font-size: 19px; line-height: 1.7; background: #f7f4ee; }
.cmp div.hard { background: var(--mint); }
.cmp small { display: block; font-size: 15px; font-weight: 700; color: var(--teal-dark); margin-bottom: 6px; }
.tcard { border-radius: 14px; border: 2px solid #eef1f4; padding: 16px 20px; display: grid; gap: 8px; }
.tcard .tt { font-size: 22px; font-weight: 900; }
.tcard .sub2 { padding-left: 16px; border-left: 3px solid var(--mint); display: grid; gap: 6px; font-size: 18px; color: var(--ink-soft); }
.tcard q { font-size: 18px; color: var(--ink); quotes: "「" "」"; }
.rule { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; align-items: center; gap: 14px; }
.rule .r { border-radius: 14px; background: #fff; border: 3px solid var(--line); padding: 16px; text-align: center; }
.rule .r b { display: block; font-size: 22px; font-weight: 900; }
.rule .r small { display: block; font-size: 15px; color: var(--muted); margin-top: 4px; }
.rule .op { font-family: var(--f-en); font-size: 34px; font-weight: 700; color: var(--teal); }
.code { font-family: Menlo, monospace; font-size: 17px; background: #1f2937; color: #e2f6f3; border-radius: 12px; padding: 16px 20px; line-height: 1.7; white-space: pre; }
"""

SERIES = []  # (key, no, name, [slides])


def footer(name, page, total=4):
    return (f'<footer><div class="brand"><img class="logo" src="logo.svg" alt=""><img class="svc" src="service-logo.svg" alt="みらい議会"></div>'
            f'<span class="url">github.com/team-mirai/mirai-gikai</span><span class="page">{name} {page} / {total}</span></footer>')


def kicker(no, name):
    return f'<div class="kicker"><span class="no">{no:02d}</span>{name}</div>'


def points(items):
    return '<ul class="points">' + "".join(f"<li><span>{t}</span></li>" for t in items) + "</ul>"


def feat(no, name, h1, items, visual, note=False):
    return (('<span class="note">※画面はイメージです</span>' if note else "")
            + f'<div class="feat"><div>{kicker(no, name)}<h1>{h1}</h1>{points(items)}</div>{visual}</div>')


def steps(no, name, h1, sub, items, cols=5):
    sts = ""
    for i, (t, d, ai, ic) in enumerate(items, 1):
        tag = '<span class="ai-tag">AI が担当</span>' if ai else ""
        sts += (f'<div class="card st{" ai" if ai else ""}"><div class="hd"><span class="n">{i}</span>{tag}</div>'
                f'{icon(ic, "si")}<b>{t}</b><p>{d}</p></div>')
    return (f'{kicker(no, name)}<h1>{h1}</h1>' + (f'<p class="sub">{sub}</p>' if sub else "")
            + f'<div class="flow{" c4" if cols == 4 else ""}">{sts}</div>')


def tiles(no, name, h1, sub, items, three=False):
    t = "".join(f'<div class="card tile {c}"><span class="ic">{icon(ic)}</span><div><b>{b}</b><p>{p}</p></div></div>'
                for ic, c, b, p in items)
    return (f'{kicker(no, name)}<h1>{h1}</h1>' + (f'<p class="sub">{sub}</p>' if sub else "")
            + f'<div class="{"grid3" if three else "grid2"}">{t}</div>')


def add(key, no, name, slides):
    SERIES.append((key, no, name, slides))


# ================================================================ エンジニア向けの部品
import re as _re

SHOT = "../../assets/screens/"
LOGO = "../../assets/logos/"

# 技術のロゴ（しくみ図鑑のバッジの SVG を使う。ないものは diagrams のアイコン）
_kids = open(os.path.join(HERE, "../../中学生向け_しくみ図鑑.html")).read()
TL = {name.strip(): svg for svg, name in _re.findall(r'<li>(<svg class="tl".*?</svg>)([^<]+)</li>', _kids, _re.S)}
for k, f in {"PostgreSQL": "postgresql", "OpenAI": "openai", "Anthropic": "anthropic", "Gemini": "gemini", "Langfuse": "activity", "Cloud Run": "cloud-run"}.items():
    TL[k] = f'<img class="tl" src="{LOGO}{f}.png" alt="">'


def logo(name, label=None):
    return f'<span class="lb">{TL[name]}{label or name}</span>'


def shot(file, name, route, cls=""):
    return (f'<figure class="sh {cls}"><div class="si"><img src="{SHOT}{file}.png" alt=""></div>'
            f'<figcaption><b>{name}</b><code>{route}</code></figcaption></figure>')


def head(no, name, h1, sub=None):
    return f'{kicker(no, name)}<h1>{h1}</h1>' + (f'<p class="sub">{sub}</p>' if sub else "")


def chain(nodes):
    """横に並べたノード。nodes: (アイコン, 色クラス, 題, 説明)"""
    out = []
    for i, (ic, c, t, d) in enumerate(nodes):
        if i:
            out.append('<span class="ch-a">' + icon("arrow-right") + "</span>")
        out.append(f'<div class="ch-n {c}"><span class="ch-i">{icon(ic)}</span><b>{t}</b><p>{d}</p></div>')
    return '<div class="ch">' + "".join(out) + "</div>"


LANE = {"browser": ("ブラウザ", "t"), "web": ("web", "t2"), "admin": ("admin", "b"), "cache": ("キャッシュ", "g"), "db": ("DB", "a"), "ai": ("AI", "v")}


def vsteps(steps):
    """縦の手順。steps: (レーン, 名前, 説明, 次へ渡すもの)"""
    out = []
    for i, (lane, name, desc, passes) in enumerate(steps, 1):
        ln, c = LANE[lane]
        out.append(f'<div class="vs"><span class="vs-l {c}">{ln}</span><span class="vs-n">{i}</span><div><code>{name}</code><p>{desc}</p></div></div>')
        if passes:
            out.append(f'<div class="vs-p"><span>{passes}</span></div>')
    return '<div class="card vss">' + "".join(out) + "</div>"


def tree(rows, cls=""):
    """rows: (深さ, 名前, 説明)"""
    out = []
    for depth, name, desc in rows:
        out.append(f'<div class="tr d{depth}"><code>{name}</code><span>{desc}</span></div>')
    return f'<div class="card tree {cls}">' + "".join(out) + "</div>"


EXTRA_CSS += """
/* エンジニア向けシリーズ */
.lb { display: inline-flex; align-items: center; gap: 10px; background: #fff; border: 2px solid #eef1f4; border-radius: 12px; padding: 8px 16px; font-size: 21px; font-weight: 700; }
.lb .tl { width: 28px; height: 28px; object-fit: contain; flex: none; }
.lbs { display: flex; flex-wrap: wrap; gap: 10px; }
.sh { display: grid; gap: 8px; margin: 0; }
.sh .si { border-radius: 14px; overflow: hidden; border: 2px solid #fff; box-shadow: 0 6px 24px rgba(15, 132, 114, 0.14); background: #fff; line-height: 0; }
.sh .si img { width: 100%; height: 100%; object-fit: cover; object-position: top left; }
.sh figcaption { display: flex; align-items: baseline; gap: 12px; }
.sh figcaption b { font-size: 21px; font-weight: 900; }
.sh figcaption code { font-family: Menlo, monospace; font-size: 15px; color: var(--teal-dark); }
.shots4 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px 24px; }
.shots4 .si { height: 236px; }
.split { display: grid; grid-template-columns: 470px 1fr; gap: 48px; height: 100%; padding-bottom: 116px; align-items: center; }
.split .points li { font-size: 22px; }
.ch { display: flex; align-items: stretch; margin-top: 40px; }
.ch-n { flex: 1 1 0; background: #fff; border-radius: 18px; box-shadow: 0 6px 24px rgba(15, 132, 114, 0.10); border-top: 6px solid var(--teal); padding: 22px 20px; display: grid; gap: 8px; align-content: start; }
.ch-n.b { border-top-color: var(--blue); } .ch-n.v { border-top-color: var(--violet); } .ch-n.a { border-top-color: var(--amber); } .ch-n.g { border-top-color: #9aa4ae; }
.ch-i { width: 48px; height: 48px; border-radius: 12px; background: var(--teal); display: grid; place-items: center; }
.ch-n.b .ch-i { background: var(--blue); } .ch-n.v .ch-i { background: var(--violet); } .ch-n.a .ch-i { background: var(--amber); } .ch-n.g .ch-i { background: #9aa4ae; }
.ch-i svg { width: 28px; height: 28px; color: #fff; }
.ch-n b { font-family: Menlo, monospace; font-size: 21px; font-weight: 700; line-height: 1.35; word-break: break-all; }
.ch-n p { font-size: 18.5px; color: var(--ink-soft); line-height: 1.55; }
.ch-a { flex: none; width: 40px; display: grid; place-items: center; color: var(--teal); }
.ch-a svg { width: 28px; height: 28px; }
.vss { padding: 22px 26px; display: grid; gap: 0; }
.vs { display: grid; grid-template-columns: 96px 34px 1fr; gap: 12px; align-items: start; padding: 8px 0; }
.vs-l { font-size: 15px; font-weight: 700; color: #fff; border-radius: 8px; text-align: center; padding: 3px 0; background: var(--teal); }
.vs-l.t2 { background: var(--teal-dark); } .vs-l.b { background: var(--blue); } .vs-l.g { background: #85868e; } .vs-l.a { background: var(--amber); } .vs-l.v { background: var(--violet); }
.vs-n { font-family: var(--f-en); font-size: 15px; font-weight: 700; color: #fff; background: var(--ink); width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; }
.vs code { font-family: Menlo, monospace; font-size: 20px; font-weight: 700; }
.vs p { font-size: 17.5px; color: var(--ink-soft); line-height: 1.5; margin-top: 2px; }
.vs-p { margin-left: 152px; border-left: 3px solid var(--teal); padding: 2px 0 2px 16px; }
.vs-p span { font-size: 16px; font-weight: 700; color: var(--teal-dark); background: var(--mint); border-radius: 999px; padding: 2px 14px; }
.tree { padding: 24px 30px; display: grid; gap: 2px; }
.tr { display: grid; grid-template-columns: 330px 1fr; gap: 16px; align-items: baseline; font-size: 19px; line-height: 1.6; }
.tr code { font-family: Menlo, monospace; font-weight: 700; color: var(--teal-dark); }
.tr.d1 code { padding-left: 28px; } .tr.d2 code { padding-left: 56px; color: var(--amber); font-weight: 400; }
.tr.d1 code::before { content: "├ "; color: #b8c2cc; } .tr.d2 code::before { content: "└ "; color: #b8c2cc; }
.tr span { color: var(--ink-soft); }
.tree.small .tr { font-size: 17px; line-height: 1.5; grid-template-columns: 250px 1fr; }
.trees2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 30px; }
.trees2 .tree h3 { font-size: 22px; font-weight: 900; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
.trees2 .tree h3 svg { width: 26px; height: 26px; color: var(--teal-dark); }
.trees2 .tree.admin h3 svg { color: var(--blue); } .trees2 .tree.admin .tr code { color: var(--blue); }
.tables { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 36px; }
.tg { padding: 24px 22px; display: grid; gap: 12px; align-content: start; border-top: 6px solid var(--teal); }
.tg.b { border-top-color: var(--violet); } .tg.a { border-top-color: var(--amber); } .tg.g { border-top-color: #9aa4ae; }
.tg h3 { font-size: 24px; font-weight: 900; display: flex; align-items: center; gap: 10px; }
.tg h3 svg { width: 28px; height: 28px; color: var(--teal-dark); }
.tg.b h3 svg { color: var(--violet); } .tg.a h3 svg { color: var(--amber); } .tg.g h3 svg { color: var(--ink-soft); }
.tg ul { list-style: none; display: grid; gap: 6px; }
.tg li { font-family: Menlo, monospace; font-size: 17px; background: #f7f8f8; border-radius: 8px; padding: 4px 10px; }
.tg li.old { color: var(--muted); }
.strip { margin-top: 26px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; font-size: 21px; font-weight: 700; }
.strip .k { color: var(--teal-dark); }
.strip span.c { background: #fff; border-radius: 999px; padding: 6px 18px; box-shadow: 0 4px 14px rgba(15, 132, 114, 0.10); }
.arch { padding: 26px 30px; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 64px; margin-top: 30px; }
.an { border: 3px solid var(--line); border-radius: 16px; padding: 12px 16px; background: #fff; display: flex; align-items: center; gap: 14px; }
.an img, .an .tl { width: 44px; height: 44px; object-fit: contain; flex: none; }
.an b { display: block; font-size: 22px; font-weight: 900; line-height: 1.3; }
.an small { display: block; font-size: 15px; color: var(--muted); line-height: 1.4; }
.an.t { border-color: var(--teal); background: var(--mint); } .an.b { border-color: var(--blue); background: var(--blue-wash); }
.an.a { border-color: var(--amber); background: var(--amber-wash); } .an.v { border-color: var(--violet); background: var(--violet-wash); }
.apair { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.adn { text-align: center; color: var(--teal-dark); font-size: 16px; font-weight: 700; padding: 8px 0; line-height: 1.35; }
.adn::before { content: "↓"; display: block; font-size: 22px; line-height: 1; }
.adn.b { color: var(--blue); } .adn.v { color: var(--violet); }
.aspan { grid-column: 1 / 3; display: grid; grid-template-columns: 1fr 1fr; column-gap: 64px; position: relative; }
.aspan.vercel::after { content: "キャッシュを消す →"; content: "← キャッシュを消す"; position: absolute; left: 50%; top: 50%; transform: translate(-50%, -140%); font-size: 15px; font-weight: 700; color: var(--blue); white-space: nowrap; }
.rules { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 36px; }
.rl { padding: 22px 24px; display: grid; gap: 8px; align-content: start; }
.rl b { font-size: 22px; font-weight: 900; display: flex; align-items: center; gap: 10px; }
.rl b svg { width: 26px; height: 26px; color: var(--teal-dark); flex: none; }
.rl p { font-size: 18px; color: var(--ink-soft); line-height: 1.55; }
.rl code, .tile code, .points code, .ch-n p code { font-family: Menlo, monospace; font-size: 0.88em; color: var(--teal-dark); background: var(--mint); border-radius: 6px; padding: 0 6px; }
.stg3 { display: flex; align-items: center; gap: 18px; margin-top: 28px; }
.stg3 .sg { flex: 1; background: #fff; border-radius: 18px; box-shadow: 0 6px 24px rgba(15, 132, 114, 0.10); padding: 20px 22px; border-top: 6px solid var(--violet); display: grid; gap: 10px; align-content: start; min-height: 300px; }
.stg3 .sg.end { border-top-color: var(--teal); }
.stg3 .sg h3 { font-family: Menlo, monospace; font-size: 26px; font-weight: 700; }
.stg3 .sg p { font-size: 18px; color: var(--ink-soft); line-height: 1.5; }
.stg3 .arr { flex: none; color: var(--violet); font-size: 15px; font-weight: 700; text-align: center; line-height: 1.4; width: 110px; }
.stg3 .arr svg { width: 34px; height: 34px; display: block; margin: 0 auto 4px; }
.fld { display: flex; flex-wrap: wrap; gap: 8px; }
.fld span { font-family: Menlo, monospace; font-size: 16.5px; background: var(--violet-wash); color: var(--violet); border-radius: 8px; padding: 2px 10px; }
.fld span.r { background: var(--mint); color: var(--teal-dark); }
"""

EXTRA_CSS += """
/* 調整 */
.arch { column-gap: 110px; padding: 34px 40px; margin-top: 36px; }
.an { padding: 18px 20px; gap: 16px; }
.an img, .an .tl { width: 56px; height: 56px; }
.an b { font-size: 25px; } .an small { font-size: 17px; }
.adn { font-size: 18px; padding: 14px 0; }
.aspan { column-gap: 110px; }
.aspan.vercel::after { content: "キャッシュ削除"; transform: translate(-50%, -150%); font-size: 14px; }
.aspan.vercel::before { content: ""; position: absolute; left: calc(50% - 47px); width: 94px; top: 50%; border-top: 2px dashed var(--blue); }
.stack { margin-top: 30px; gap: 18px; }
.stack .sc { min-height: 0; padding: 22px 24px; }
.lb { font-size: 19px; padding: 6px 12px; gap: 8px; }
.lb .tl { width: 24px; height: 24px; }
.trees2 .tree.admin .tr { grid-template-columns: 360px 1fr; }
.ch { margin-top: 48px; }
.ch-n { padding: 28px 24px; min-height: 330px; gap: 12px; }
.ch-i { width: 60px; height: 60px; border-radius: 14px; } .ch-i svg { width: 34px; height: 34px; }
.ch-n b { font-size: 25px; } .ch-n p { font-size: 21px; }
.strip { margin-top: 34px; font-size: 22px; }
.tg li { font-size: 19px; }
.colc { min-height: 480px; }
.colc li { font-size: 22px; } .colc li b { font-size: inherit; color: var(--violet); }
.stg3 { margin-top: 40px; }
.stg3 .sg { min-height: 440px; padding: 28px 26px; gap: 16px; }
.stg3 .sg h3 { font-size: 30px; } .stg3 .sg p { font-size: 21px; }
.fld span { font-size: 19px; padding: 4px 12px; }
.stg3 .arr { font-size: 17px; width: 130px; }
.rules { gap: 22px; margin-top: 40px; }
.rl { padding: 30px 30px; min-height: 210px; gap: 12px; }
.rl b { font-size: 26px; } .rl b svg { width: 30px; height: 30px; }
.rl p { font-size: 21px; }
.arch { margin-top: 26px; padding: 24px 36px; column-gap: 100px; }
.aspan { column-gap: 100px; }
.aspan.vercel::before { left: calc(50% - 42px); width: 84px; }
.an { padding: 12px 18px; } .an img, .an .tl { width: 46px; height: 46px; }
.an b { font-size: 23px; } .an small { font-size: 15.5px; }
.adn { padding: 6px 0; font-size: 16.5px; }
"""

# ================================================================ 01 全体像（しくみ図鑑 1〜2章）
ARCH = f'''<div class="card arch">
  <div class="an"><img src="{LOGO}users.png" alt=""><div><b>市民・開発者</b><small>ブラウザ ／ オープンデータ API</small></div></div>
  <div class="an"><img src="{LOGO}claude.png" alt=""><div><b>運営・AIエージェント</b><small>管理画面 ／ MCP</small></div></div>
  <div class="an b"><img src="{LOGO}cloud-scheduler.png" alt=""><div><b>Cloud Scheduler</b><small>毎朝 6:00</small></div></div>
  <div class="adn">閲覧・チャット・インタビュー</div><div class="adn b">管理・MCP ツール</div><div class="adn b">analyze-all</div>
  <div class="aspan vercel"><div class="an t"><img src="{LOGO}nextjs.png" alt=""><div><b>web 公開サイト</b><small>Vercel ・ Next.js 15</small></div></div><div class="an b"><img src="{LOGO}nextjs.png" alt=""><div><b>admin 管理画面</b><small>Vercel ・ Next.js 15</small></div></div></div>
  <div class="an b"><img src="{LOGO}cloud-run.png" alt=""><div><b>Cloud Run Job</b><small>トピック分析 worker</small></div></div>
  <div class="adn">読み書き・匿名ログイン</div><div class="adn b">読み書き・Google ログイン</div><div class="adn v">AI 呼び出し</div>
  <div class="aspan"><div class="an a"><img src="{LOGO}supabase.png" alt=""><div><b>Supabase Auth</b><small>匿名・Google ログイン</small></div></div><div class="an a"><img src="{LOGO}postgresql.png" alt=""><div><b>PostgreSQL</b><small>RLS 有効・ポリシーなし</small></div></div></div>
  <div class="an v"><img src="{LOGO}vercel.png" alt=""><div><b>AI Gateway</b><small>OpenAI・Anthropic・Google ／ Langfuse</small></div></div>
</div>'''

def app(cls, ic, name, folder, file, items):
    return (f'<div class="card app {cls}"><h3>{icon(ic)}{name}<code>{folder}</code></h3>'
            f'<div class="si"><img src="{SHOT}{file}.png" alt=""></div>'
            "<ul>" + "".join(f"<li>{t}</li>" for t in items) + "</ul></div>")


add("overview", 1, "全体像", [
    head(1, "全体像", "みらい議会は<em>2つのアプリ</em>", "国会の議案をやさしく解説し、AI に質問したり、AI のインタビューで意見を届けたりできる Web サービス。")
    + '<div class="apps">'
    + app("web", "globe", "公開サイト", "web/", "web-bill", ["議案の一覧・会期ごとのまとめ", "やさしい解説とふりがな、チームみらいの賛否", "AI チャットと AI インタビュー", "みんなの意見・トピック、オープンデータ API"])
    + app("admin", "lock", "管理画面（運営だけ）", "admin/", "admin-bill-edit", ["議案の登録・解説の執筆・公開の切りかえ", "賛否と理由の登録（公開日時の予約）", "インタビューの質問づくりと試運転", "レポートの確認・トピック分析の実行"])
    + "</div>",
    head(1, "全体像", "全体の<em>地図</em>", "データベースは1つだけ。管理画面で書いた解説を公開サイトが読み、インタビューの内容は管理画面で確かめます。") + ARCH,
    f'<div class="split"><div>{kicker(1, "全体像")}<h1>公開サイト<br><em>web</em></h1>'
    + points(["<b>Server Components</b> が基本。操作する部分だけ Client", "市民は<b>匿名ログイン</b>。メール登録なし",
              "議案は <b>unstable_cache</b> で10分作りおき", "AI チャットとインタビューは<b>ストリーミング</b>"])
    + '</div><div class="shots4">' + shot("web-home", "トップ", "/") + shot("web-bill", "議案の詳細", "/bills/[id]")
    + shot("web-interview", "インタビュー", "…/interview") + shot("web-report", "公開レポート", "/report/[id]") + "</div></div>",
    f'<div class="split"><div>{kicker(1, "全体像")}<h1>管理画面<br><em>admin</em></h1>'
    + points(["<b>Google ログイン</b>＋ middleware で管理者だけ", "保存すると web の<b>キャッシュを消して</b>すぐ反映",
              "トピック分析は <b>Cloud Run Job</b> を起動", "AI エージェントは <b>MCP</b> で同じ操作ができる"])
    + '</div><div class="shots4">' + shot("admin-bills", "議案一覧", "/bills") + shot("admin-bill-edit", "議案の編集・賛否", "/bills/[id]/edit")
    + shot("admin-reports", "レポート一覧・統計", "…/reports") + shot("admin-topic-analysis", "トピック分析", "…/user-topic-analysis") + "</div></div>",
])

# ================================================================ 02 コードの中（しくみ図鑑 3・8・9章）
add("code", 2, "コードの中", [
    head(2, "コードの中", "上から順に<em>呼び出す</em>", "機能ごとの部屋（features/）を、仕事の種類ごとのフォルダに分ける。DB にさわるのは repositories だけ。")
    + chain([("file", "g", "app/…/<br>page.tsx", "URL を受けとる。/bills/123 から id を読みとって渡すだけ"),
             ("layout-template", "", "components", "データを並べて画面にする。例 <code>bill-detail-layout.tsx</code>"),
             ("download", "b", "loaders<br>actions", "データを用意する・操作を受ける。よく使うデータは作りおき"),
             ("cog", "v", "services", "手順とルール。例 <code>handle-interview-chat-request.ts</code>"),
             ("database", "a", "repositories", "DB の読み書きだけ。例 <code>bill-repository.ts</code>")])
    + '<div class="strip"><span class="k">ほかに</span><span class="c">client/ … ブラウザで動く部品（"use client"）</span><span class="c">shared/ … 純粋関数。テストしやすい</span></div>',
    head(2, "コードの中", "機能ごとに<em>フォルダを分ける</em>", "<code>src/features/</code> の下を機能単位に分ける Bulletproof React 方式。")
    + '<div class="trees2">'
    + tree([(0, "web/src/features/", "")] + [(1, n + "/", d) for n, d in [
        ("bills", "議案の一覧・詳細・検索"), ("bill-difficulty", "ふつう／詳しくの切りかえ"), ("diet-sessions", "会期ごとのまとめ"),
        ("chat", "AI チャットと利用料"), ("interview-config", "インタビューの設定・開示"), ("interview-session", "会話・完了処理"),
        ("interview-report", "レポート・公開設定"), ("report-reaction", "「参考になった」"), ("user-topic-analysis", "みんなの意見・トピック"),
        ("open-data", "オープンデータ API")]], "small").replace('class="card tree small"', 'class="card tree small web"', 1).replace('<div class="tr d0">', '<h3>' + icon("globe") + 'web（10）</h3><div class="tr d0" style="display:none">', 1)
    + tree([(0, "admin/src/features/", "")] + [(1, n + "/", d) for n, d in [
        ("auth ・ admins", "ログイン・管理者"), ("bills ・ bills-edit", "議案の一覧・編集"), ("mirai-stance", "チームみらいの賛否"),
        ("diet-sessions ・ tags", "会期・タグ"), ("interview-config", "インタビュー設定"), ("interview-simulation", "AI の回答者役で試運転"),
        ("interview-reports ・ interviews", "レポート確認・一覧"), ("experts", "有識者の登録"), ("topic-analysis ・ user-topic-analysis", "トピック分析"),
        ("analysis-viewer", "分析のマインドマップ"), ("mcp", "MCP サーバー")]], "small").replace('class="card tree small"', 'class="card tree small admin"', 1).replace('<div class="tr d0">', '<h3>' + icon("lock") + 'admin（16）</h3><div class="tr d0" style="display:none">', 1)
    + "</div>",
    head(2, "コードの中", "データベースの<em>中身</em>", "25のテーブルを外部キーでつなぐ。RLS は有効にして許可のルールは書かず、読み書きはサーバーだけ。")
    + '<div class="tables">'
    + f'<div class="card tg"><h3>{icon("file-text")}議案</h3><ul>' + "".join(f"<li>{t}</li>" for t in ["bills", "bill_contents", "mirai_stances", "tags", "bills_tags", "diet_sessions", "preview_tokens"]) + "</ul></div>"
    + f'<div class="card tg b"><h3>{icon("mic")}インタビュー</h3><ul>' + "".join(f"<li>{t}</li>" for t in ["interview_configs", "interview_questions", "interview_sessions", "interview_messages", "interview_report", "interview_opinion", "interview_rating_feedbacks", "report_reactions", "expert_registrations"]) + "</ul></div>"
    + f'<div class="card tg a"><h3>{icon("tags")}トピック分析</h3><ul>' + "".join(f"<li>{t}</li>" for t in ["topic_analysis_versions", "topic_analysis_topics", "topic_analysis_classifications"]) + "".join(f'<li class="old">{t}（旧）</li>' for t in ["topic_analysis_version", "topic", "topic_opinion"]) + "</ul></div>"
    + f'<div class="card tg g"><h3>{icon("gauge")}AI と利用</h3><ul>' + "".join(f"<li>{t}</li>" for t in ["chats", "chat_usage_events", "api_rate_limits"]) + "</ul></div>"
    + "</div>",
    head(2, "コードの中", "使っている<em>道具</em>")
    + '<div class="stack">'
    + '<div class="card sc"><h3>画面</h3><div class="lbs">' + logo("Next.js", "Next.js 15") + logo("React", "React 19") + logo("TypeScript") + logo("Tailwind CSS") + logo("Radix UI") + "</div></div>"
    + '<div class="card sc"><h3>データ</h3><div class="lbs">' + logo("Supabase") + logo("PostgreSQL") + logo("zod") + logo("react-hook-form") + "</div></div>"
    + '<div class="card sc"><h3>AI</h3><div class="lbs">' + logo("Vercel AI SDK（ai）", "AI SDK") + logo("AI Gateway") + logo("OpenAI") + logo("Anthropic") + logo("Gemini") + logo("Langfuse") + "</div></div>"
    + '<div class="card sc"><h3>動かす場所</h3><div class="lbs">' + logo("Vercel") + logo("Cloud Run") + logo("Cloud Scheduler") + "</div></div>"
    + '<div class="card sc"><h3>品質</h3><div class="lbs">' + logo("Vitest") + logo("Biome") + logo("GitHub Actions") + logo("Codecov") + logo("CodeRabbit") + "</div></div>"
    + '<div class="card sc"><h3>画面の部品</h3><div class="lbs">' + logo("lucide-react") + logo("streamdown") + logo("@xyflow/react", "React Flow") + logo("react-markdown") + "</div></div>"
    + "</div>",
])

# ================================================================ 03 データの流れ（しくみ図鑑 4・5・7章）
def req(h1, sub, steps_, file, name, route, cls=""):
    return (f'<div class="split" style="grid-template-columns: 560px 1fr"><div>{kicker(3, "データの流れ")}<h1 style="font-size:54px">{h1}</h1><p class="sub" style="font-size:22px">{sub}</p>'
            f'<div style="margin-top:28px">{shot(file, name, route, "big " + cls)}</div></div>{vsteps(steps_)}</div>')


LANE["job"] = ("Job", "b")

add("flow", 3, "データの流れ", [
    req("<em>議案ページ</em>が<br>表示されるまで", "/bills/123 を開いたとき。作りおき（キャッシュ）があれば DB に行かない。", [
        ("browser", "GET /bills/123", "Cookie にむずかしさ（normal / hard）", "URL と Cookie"),
        ("web", "page.tsx", "params から id を取り出して呼ぶだけ", "id とむずかしさ"),
        ("cache", "unstable_cache", "同じ引数の結果があれば返す。600秒・タグ bills", "キャッシュがないときだけ"),
        ("db", "bill-repository × 4", "議案・賛否・本文・タグを Promise.all で取得", "BillWithContent"),
        ("web", "hideUnpublishedStance", "公開日時がまだ先なら賛否を外す（毎回判定）", "表示してよいデータ"),
        ("web", "BillDetailLayout", "Server Component で HTML を作る", None),
    ], "web-bill", "議案の詳細", "/bills/[id]"),
    req("作りおきを<br><em>捨てる</em>タイミング", "管理画面で賛否を保存してから、公開サイトに反映されるまで。", [
        ("browser", "stance-form", "react-hook-form で入力し Server Action を呼ぶ", "billId と入力値"),
        ("admin", "createStance", "zod で入力をチェック。middleware で管理者だけ", "チェック済みの値"),
        ("db", "mirai-stance-repository", "mirai_stances に insert", "保存結果"),
        ("admin", "invalidateWebCache", "web の /api/revalidate に Bearer 付きで POST", 'tags: ["bills"]'),
        ("web", "/api/revalidate", "秘密の文字列を確認して revalidateTag", "次のアクセスで取り直す"),
    ], "admin-bill-edit", "議案の編集・賛否", "/bills/[id]/edit"),
    req("<em>AI に質問</em>する<br>しくみ", "送信ボタンを押してから、答えが少しずつ表示されるまで。", [
        ("browser", "POST /api/chat", "会話の配列を JSON にして送る", "会話と議案 ID"),
        ("web", "匿名ユーザーの確認", "ユーザー ID がなければ 401 で終了", "user.id"),
        ("db", "利用額の確認", "1人1日・全体の1日と1か月の上限。こえたらエラー", "上限内なら次へ"),
        ("db", "プロンプトを作る", "議案の名前・要約・本文を DB から取り直す。リクエストの議案情報は使わない", "プロンプトと会話"),
        ("ai", "streamText()", "できた文字から順に返す。ウェブ検索やインタビューの提案も", "答えの文字列"),
        ("db", "onFinish", "トークン数と金額を chat_usage_events に1行追加", None),
    ], "web-bill", "議案ページの AI チャット", "/bills/[id]", "right"),
    req("みんなの意見を<br><em>まとめる</em>", "Cloud Scheduler が毎朝6時（<code>0 6 * * *</code>）に Cloud Run Job を起動。新しい意見がない議案は continue で飛ばす。", [
        ("job", "意見を集める", "公開ずみ・チェック合格のレポートの意見だけ使う", None),
        ("ai", "話題を見つける", "AI（Claude Haiku）が「どんな話題があるか」候補を出す", None),
        ("ai", "まとめる", "にた話題を合体してトピックを決める", None),
        ("ai", "仕分ける", "それぞれの意見をトピックに割り当てる", None),
        ("db", "2階層にして保存", "大きなトピックの下に小さなトピック。終わると自動で公開。次の日は増えた意見だけ仕分ける", None),
    ], "web-topics", "トピック一覧", "/bills/[id]/topics"),
])

# ================================================================ 04 ミスや悪用を防ぐ（しくみ図鑑 10章）
def guards(items):
    """items: (アイコン, 色クラス, 名前, 防ぐもの, しくみ)"""
    return (f'<div class="guards n{len(items)}">'
            + "".join(f'<div class="card gd {c}"><span class="ic">{icon(ic)}</span><b>{n}</b>'
                      f'<p class="pv"><span>防ぐもの</span>{pv}</p><p>{how}</p></div>' for ic, c, n, pv, how in items)
            + "</div>")


add("guard", 4, "ミスや悪用を防ぐ", [
    head(4, "ミスや悪用を防ぐ", "コードのミスを<em>本番の前に</em>止める", "「人が気をつける」だけに頼らず、プログラムで自動的に止める。")
    + guards([("flask-conical", "", "テスト（Vitest）", "計算や変換のまちがい", "入力と期待する出力を書いて確かめる。DB 関数はローカルの本物の Supabase で"),
              ("braces", "b", "型チェック（TypeScript）", "「数値のはずが文字列」など", "変数や引数に型を書き、実行する前に見つける"),
              ("wand-sparkles", "v", "書き方（Biome）", "書き方のばらつきとよくあるミス", "コミット前に自動で整形し、ルール違反を知らせる"),
              ("github", "a", "GitHub Actions", "チェックを通っていないコード", "PR のたびに lint・型・ビルド・テストを実行")])
    + '<div class="strip"><span class="c">コミット前に整形</span>→<span class="c">PR で自動チェック</span>→<span class="c">テストと型がすべて通る</span>→<span class="c">マージして本番へ</span>'
    + '<span class="k" style="margin-left:16px">＋ Codecov・CodeRabbit</span></div>',
    head(4, "ミスや悪用を防ぐ", "AI の<em>使いすぎと悪用</em>を防ぐ")
    + guards([("wallet", "", "利用料の上限", "使いすぎや、いたずらの大量の質問", "1人1日 0.5ドル、全体で1日 50ドル・1か月 1000ドル（既定）。こえたら止める。確認に失敗したときも止める"),
              ("shield-check", "a", "モデレーション", "悪口や個人情報が入ったレポートの公開", "別の AI が0〜100点で採点。29点以下で本人が同意したものだけ自動で公開"),
              ("brackets", "v", "入力の区切り", "「今までの指示を忘れて…」でだます攻撃", "利用者の文章は毎回ランダムな区切りで囲み、指示とは別のデータとして渡す")]),
    head(4, "ミスや悪用を防ぐ", "<em>データ</em>を守る")
    + guards([("database", "a", "RLS（行レベルセキュリティ）", "ブラウザから DB を直接読まれること", "全テーブルで有効にして、許可のルールは書かない。読み書きは秘密の鍵を持つサーバーだけ"),
              ("lock", "b", "管理者のチェック", "スタッフ以外が管理画面に入ること", "middleware がページを開くたびに admin の役割を確かめる。actions でも確認"),
              ("key-round", "", "プレビュー用のトークン", "公開前の議案を URL だけで見られること", "管理画面で有効期限つきのトークンを発行。正しいときだけ見せる"),
              ("user-round", "v", "匿名ユーザー", "他人のインタビューを見たり続けたりすること", "メール登録なしの匿名ログイン。セッションの user_id と一致するかで本人を判定")]),
    head(4, "ミスや悪用を防ぐ", "コードの<em>ルール</em>", "AGENTS.md（CLAUDE.md）に書かれている決まりごと。")
    + '<div class="rules">'
    + f'<div class="card rl"><b>{icon("file")}page.tsx は薄く</b><p>パラメータを受けとって feature に渡すだけ。index.ts は作らない</p></div>'
    + f'<div class="card rl"><b>{icon("server")}server-only</b><p>サーバー側のファイルには <code>"server-only"</code>、Client には <code>"use client"</code></p></div>'
    + f'<div class="card rl"><b>{icon("package")}共有は packages へ</b><p>web と admin に同じコードを置かない</p></div>'
    + f'<div class="card rl"><b>{icon("smile")}アイコンは lucide-react</b><p>インライン SVG は使わない。ボタンは共通の Button</p></div>'
    + f'<div class="card rl"><b>{icon("palette")}色はトークン</b><p><code>text-[#xxx]</code> などの直書きは禁止。globals.css に足してから使う</p></div>'
    + f'<div class="card rl"><b>{icon("link")}リンクは routes.ts</b><p>href や redirect に文字列のパスを書かない</p></div>'
    + "</div>",
])
EXTRA_CSS += """
.sh.big .si { height: 330px; }
.sh.right .si img { object-position: top right; }
/* 2つのアプリ */
.apps { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin-top: 34px; }
.app { padding: 24px 28px 26px; display: grid; gap: 16px; align-content: start; border-top: 8px solid var(--teal); }
.app.admin { border-top-color: var(--blue); }
.app h3 { display: flex; align-items: center; gap: 12px; font-size: 28px; font-weight: 900; }
.app h3 svg { width: 32px; height: 32px; color: var(--teal-dark); }
.app.admin h3 svg { color: var(--blue); }
.app h3 code { margin-left: auto; font-family: Menlo, monospace; font-size: 18px; color: var(--ink-soft); }
.app .si { height: 210px; border-radius: 12px; overflow: hidden; border: 2px solid #eef1f4; line-height: 0; }
.app .si img { width: 100%; height: 100%; object-fit: cover; object-position: top left; }
.app ul { list-style: none; display: grid; gap: 8px; }
.app li { font-size: 20px; padding-left: 22px; position: relative; line-height: 1.45; }
.app li::before { content: ""; position: absolute; left: 0; top: 11px; width: 10px; height: 10px; border-radius: 50%; background: var(--teal); }
.app.admin li::before { background: var(--blue); }
/* 防ぐしくみ */
.guards { display: grid; gap: 20px; margin-top: 40px; }
.guards.n3 { grid-template-columns: repeat(3, 1fr); margin-top: 56px; }
.guards.n4 { grid-template-columns: repeat(4, 1fr); }
.gd { padding: 28px 26px; display: grid; gap: 14px; align-content: start; border-top: 6px solid var(--teal); }
.gd.b { border-top-color: var(--blue); } .gd.v { border-top-color: var(--violet); } .gd.a { border-top-color: var(--amber); }
.gd .ic { width: 56px; height: 56px; border-radius: 14px; background: var(--teal); display: grid; place-items: center; }
.gd.b .ic { background: var(--blue); } .gd.v .ic { background: var(--violet); } .gd.a .ic { background: var(--amber); }
.gd .ic svg { width: 30px; height: 30px; color: #fff; }
.gd b { font-size: 25px; font-weight: 900; line-height: 1.35; }
.gd p { font-size: 19px; color: var(--ink-soft); line-height: 1.6; }
.gd p.pv { color: var(--ink); font-weight: 700; background: var(--amber-wash); border-radius: 10px; padding: 10px 14px; font-size: 18px; }
.gd p.pv span { display: block; font-size: 14px; color: var(--amber); }
.guards.n3 .gd { padding: 34px 32px; min-height: 440px; }
.guards.n3 .gd b { font-size: 29px; }
.guards.n3 .gd p { font-size: 21px; }
.guards.n3 .gd p.pv { font-size: 20px; }
.sub code { font-family: Menlo, monospace; font-size: 0.85em; color: var(--teal-dark); background: var(--mint); border-radius: 6px; padding: 0 6px; }
"""

def build():
    secs = []
    for key, no, name, slides in SERIES:
        for i, body in enumerate(slides, 1):
            secs.append(f'<section class="slide" id="{no:02d}-{key}-{i}">{body}{footer(name, i, len(slides))}</section>')
    html = f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
{FONT_LINK}
<style>{BASE_CSS}{EXTRA_CSS}</style>
</head>
<body>
{"".join(secs)}
<script>
const id = (location.hash || "#01-overview-1").slice(1);
document.getElementById(id).classList.add("on");
</script>
</body>
</html>'''
    open(os.path.join(HERE, "posts.html"), "w").write(html)
    print(f"posts.html を作りました（{len(secs)}枚）")


if __name__ == "__main__":
    build()
