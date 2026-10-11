"""lucide-react（リポジトリが使っているアイコン集）の定義から、インライン SVG を作る。"""
import glob
import os
import re

# リポジトリの node_modules（pnpm install 済み）にある lucide-react を使う
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
_DIR = glob.glob(os.path.join(_ROOT, "node_modules/.pnpm/lucide-react@*/node_modules/lucide-react/dist/esm/icons"))[0]
_cache = {}


def _nodes(name):
    if name not in _cache:
        src = open(f"{_DIR}/{name}.js").read()
        if "const __iconNode" not in src:
            # 別名のアイコン（filter → funnel など）は、参照先の定義を使う
            target = re.search(r"from '\./([\w-]+)\.js'", src).group(1)
            _cache[name] = _nodes(target)
            return _cache[name]
        body = src[src.index("const __iconNode = [") : src.index("];", src.index("const __iconNode"))]
        els = []
        for tag, attrs in re.findall(r'\[\s*"(\w+)",\s*\{(.*?)\}\s*\]', body, re.S):
            pairs = re.findall(r'(\w+): "([^"]*)"', attrs)
            a = " ".join(f'{k.replace("strokeWidth", "stroke-width")}="{v}"' for k, v in pairs if k != "key")
            els.append(f"<{tag} {a}/>")
        _cache[name] = "".join(els)
    return _cache[name]


def icon(name, cls="ic", label=None):
    """HTML に置くアイコン。色は currentColor、大きさは CSS で決める。"""
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
        f'stroke-linecap="round" stroke-linejoin="round" {aria}>{_nodes(name)}</svg>'
    )
