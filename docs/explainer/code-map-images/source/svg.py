"""構成図を組み立てる小さなヘルパー。色はすべて CSS 変数（クラス）経由で、ダークモードでも読めるようにする。"""
from html import escape


class Svg:
    _n = 0

    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.parts = []
        Svg._n += 1
        # マーカーの id を図ごとに分ける（同じページに複数の図があっても、非表示の図の定義を参照しないように）
        self.mid = f"m{Svg._n}"

    def add(self, s):
        self.parts.append(s)

    def group(self, x, y, w, h, label, kind="gray"):
        self.add(f'<rect class="grp g-{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>')
        self.add(f'<text class="gl g-{kind}" x="{x + 14}" y="{y + 22}">{escape(label)}</text>')

    def box(self, x, y, w, h, title, lines=(), kind="teal", mono=False, size=15, sub_size=12):
        self.add(f'<rect class="bx b-{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>')
        cls = "bt m" if mono else "bt"
        n = len(lines)
        line_h = sub_size + 6
        total = size + (n * line_h if n else 0)
        ty = y + (h - total) / 2 + size - 2
        self.add(f'<text class="{cls}" x="{x + w / 2}" y="{ty:.1f}" text-anchor="middle" font-size="{size}">{escape(title)}</text>')
        for i, ln in enumerate(lines):
            mono_ln = ln.startswith("`")
            t = ln.strip("`")
            c = "s m" if mono_ln else "s"
            self.add(f'<text class="{c}" x="{x + w / 2}" y="{ty + (i + 1) * line_h:.1f}" text-anchor="middle" font-size="{sub_size}">{escape(t)}</text>')

    def lbox(self, x, y, w, h, title, lines=(), kind="teal", size=15, sub_size=12.5, mono_title=False):
        """左寄せのリスト入りボックス"""
        self.add(f'<rect class="bx b-{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>')
        self.add(f'<text class="bt{" m" if mono_title else ""}" x="{x + 16}" y="{y + 28}" font-size="{size}">{escape(title)}</text>')
        for i, ln in enumerate(lines):
            indent = (len(ln) - len(ln.lstrip(" "))) * 6
            t = ln.strip(" ")
            mono_ln = t.startswith("`")
            t = t.strip("`")
            self.add(f'<text class="s{" m" if mono_ln else ""}" x="{x + 16 + indent}" y="{y + 52 + i * (sub_size + 7.5):.1f}" font-size="{sub_size}">{escape(t)}</text>')

    def arrow(self, pts, label=None, at=None, dashed=False, kind="ink", anchor="middle", lsize=11.5, both=False):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        da = ' stroke-dasharray="5 4"' if dashed else ""
        ms = ' marker-start="url(#ahs)"' if both else ""
        self.add(f'<path class="ar a-{kind}" d="{d}"{da} marker-end="url(#ah-{kind})"{ms}/>')
        if label:
            lx, ly = at if at else ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2 - 6)
            for i, part in enumerate(label.split("\n")):
                mono = part.startswith("`")
                self.add(f'<text class="al{" m" if mono else ""}" x="{lx}" y="{ly + i * (lsize + 4)}" text-anchor="{anchor}" font-size="{lsize}">{escape(part.strip("`"))}</text>')

    def text(self, x, y, s, cls="s", size=12, anchor="start"):
        mono = s.startswith("`")
        self.add(f'<text class="{cls}{" m" if mono else ""}" x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{escape(s.strip("`"))}</text>')

    def chip(self, x, y, s, kind="teal", w=None, size=12):
        w = w or (len(s) * 7.6 + 18)
        self.add(f'<rect class="chip b-{kind}" x="{x}" y="{y}" width="{w}" height="24" rx="12"/>')
        self.add(f'<text class="bt m" x="{x + w / 2}" y="{y + 16.5}" text-anchor="middle" font-size="{size}">{escape(s)}</text>')
        return w

    def render(self):
        defs = "<defs>" + "".join(
            f'<marker id="ah-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah a-{k}" d="M0,0 L10,5 L0,10 z"/></marker>'
            for k in ("ink", "teal", "blue", "amber", "violet")
        ) + '<marker id="ahs" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah a-ink" d="M0,0 L10,5 L0,10 z"/></marker></defs>'
        defs = defs.replace('id="ah', f'id="{self.mid}-ah')
        body = "".join(self.parts).replace('url(#ah', f'url(#{self.mid}-ah')
        return (f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.label)}" '
                f'style="min-width:{min(self.w, 860)}px">{defs}{body}</svg>')


SVG_CSS = """
.grp { fill: none; stroke: var(--line); stroke-width: 1.5; stroke-dasharray: 6 5; }
.grp.g-teal { stroke: var(--teal); } .grp.g-blue { stroke: var(--blue); } .grp.g-amber { stroke: var(--amber); } .grp.g-violet { stroke: var(--violet); }
.gl { font-size: 12.5px; font-weight: 700; fill: var(--ink-soft); }
.gl.g-teal { fill: var(--teal); } .gl.g-blue { fill: var(--blue); } .gl.g-amber { fill: var(--amber); } .gl.g-violet { fill: var(--violet); }
.bx, .chip { stroke-width: 1.5; }
.b-teal { fill: var(--teal-wash); stroke: var(--teal); }
.b-blue { fill: var(--blue-wash); stroke: var(--blue); }
.b-amber { fill: var(--amber-wash); stroke: var(--amber); }
.b-violet { fill: var(--violet-wash); stroke: var(--violet); }
.b-gray { fill: var(--surface); stroke: var(--line); }
.b-ink { fill: var(--surface); stroke: var(--ink-soft); }
.bt { font-weight: 700; fill: var(--ink); }
.s { fill: var(--ink-soft); }
.ar { fill: none; stroke-width: 1.6; }
.a-ink { stroke: var(--ink-soft); } .ah.a-ink { fill: var(--ink-soft); stroke: none; }
.a-teal { stroke: var(--teal); } .ah.a-teal { fill: var(--teal); stroke: none; }
.a-blue { stroke: var(--blue); } .ah.a-blue { fill: var(--blue); stroke: none; }
.a-amber { stroke: var(--amber); } .ah.a-amber { fill: var(--amber); stroke: none; }
.a-violet { stroke: var(--violet); } .ah.a-violet { fill: var(--violet); stroke: none; }
.al { fill: var(--ink-soft); paint-order: stroke; stroke: var(--surface); stroke-width: 5px; stroke-linejoin: round; }
.num { font-weight: 900; fill: var(--surface); }
.numc { fill: var(--teal); }
"""
