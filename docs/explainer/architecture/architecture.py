"""みらい議会のアーキテクチャ図を、Python の diagrams（Graphviz）で描く。

    pip install diagrams   # Graphviz（dot コマンド）も必要
    python3 architecture.py
    → ../assets/architecture.png

icons/ のロゴは simple-icons（CC0）と lucide（ISC）から PNG にしたもの。
"""
import os

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.gcp.compute import Run
from diagrams.gcp.devtools import Scheduler
from diagrams.onprem.client import Users
from diagrams.onprem.database import Postgresql
from diagrams.programming.framework import Nextjs

HERE = os.path.dirname(os.path.abspath(__file__))
ICON = lambda n: os.path.join(HERE, "icons", f"{n}.png")  # noqa: E731
OUT = os.path.join(HERE, "..", "assets", "architecture")

FONT = "Hiragino Sans"
TEAL, BLUE, VIOLET, AMBER, GRAY = "#0f8472", "#2f6db5", "#6a4fb3", "#b06f00", "#85868e"

graph_attr = {"fontname": FONT, "fontsize": "22", "bgcolor": "white", "pad": "0.4", "nodesep": "0.7", "ranksep": "1.6", "splines": "spline", "newrank": "true"}
node_attr = {"fontname": FONT, "fontsize": "13"}
edge_attr = {"fontname": FONT, "fontsize": "12"}


def cluster(label, color, fill):
    return Cluster(label, graph_attr={"fontname": FONT, "fontsize": "15", "fontcolor": color, "style": "rounded,filled", "color": color, "fillcolor": fill, "penwidth": "1.5", "margin": "18"})


def e(label="", color=TEAL, style="solid"):
    return Edge(label=label, color=color, fontcolor=color, style=style, penwidth="1.6")


with Diagram("", filename=OUT, outformat="png", show=False, direction="LR",
             graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    with cluster("使う人・外部", GRAY, "#f7f8f8"):
        citizen = Users("市民\nブラウザ・スマホ")
        dev = Custom("外部の開発者\nオープンデータ API", ICON("braces"))
        staff = Users("運営メンバー")
        agent = Custom("AI エージェント\nMCP", ICON("claude"))

    with cluster("Vercel（Next.js 15）", TEAL, "#eef8f5"):
        web = Nextjs("web\n公開サイト")
        admin = Nextjs("admin\n管理画面")

    with cluster("Supabase", AMBER, "#fdf6e8"):
        auth = Custom("Auth\n匿名ログイン / Google", ICON("supabase"))
        db = Postgresql("PostgreSQL\nRLS 有効・ポリシーなし")

    with cluster("AI", VIOLET, "#f5f1fc"):
        gateway = Custom("Vercel AI Gateway\nOpenAI・Anthropic・Google", ICON("vercel"))
        langfuse = Custom("Langfuse\nトレース", ICON("activity"))

    with cluster("Google Cloud", BLUE, "#eef3fb"):
        scheduler = Scheduler("Cloud Scheduler\n毎朝 6:00")
        job = Run("Cloud Run Job\nトピック分析 worker")

    citizen >> e("閲覧・チャット\nインタビュー") >> web
    dev >> e("JSON") >> web
    staff >> e(color=BLUE) >> admin
    agent >> e("MCP", color=VIOLET) >> admin
    web >> e(style="dashed") >> auth
    admin >> e(color=BLUE, style="dashed") >> auth
    web >> e("読み書き") >> db
    admin >> e("読み書き", color=BLUE) >> db
    admin >> e("キャッシュを消す\n/api/revalidate", color=BLUE, style="dashed") >> web
    web >> e("AI 呼び出し", color=VIOLET) >> gateway
    admin >> e(color=VIOLET) >> gateway
    gateway >> e(color=GRAY, style="dotted") >> langfuse
    admin >> e("jobs:run", color=BLUE) >> job
    scheduler >> e("analyze-all", color=BLUE) >> job
    job >> e(color=BLUE) >> db
    job >> e(color=VIOLET) >> gateway

print("ok:", OUT + ".png")
