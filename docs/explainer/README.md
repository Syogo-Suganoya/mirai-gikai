# みらい議会 解説資料（非公式）

みらい議会のコードを読むための資料です。チームみらい・みらい議会の公式資料ではなく、公開されているソースコードを個人が読んでまとめた非公式の解説です。`develop @ 99840c65`（2026-10-06）時点のコードをもとに作っています。

GitHub Pages で公開しています：https://syogo-suganoya.github.io/mirai-gikai/explainer/how-it-works.html


| ファイル | 内容 |
| :-- | :-- |
| `code-map.html` | 構成図5枚と、画面・API ごとの「機能 → ファイル」逆引き（38件・検索つき）、横断的な仕組みの置き場所 |
| `ai-interview-spec.html` | AI インタビューの設定・モード・ステージ遷移・出力形式・公開ルールなど（全15章） |
| `how-it-works.html` | サービスの内部構造を中学生向けに説明した資料（全11章） |
| `code-map-images/` | コード逆引きを画像にしたもの（1600px 幅・12枚） |
| `x-images/` | X 投稿用の画像（1600×900・7枚） |
| `x-posts/` | X 投稿シリーズの画像（1600×900・4テーマ×4枚） |
| `assets/screens/` | 画面のスクリーンショット（`tools/app-shots.js` で撮影） |

HTML はブラウザで直接開けます。`docs/` を GitHub Pages の公開元にしているので、`docs/.nojekyll` で Jekyll の変換を止めています。HTML には非公式の注意書き（`.unofficial`）を入れています。

## 作り直す

HTML は Python のスクリプトで組み立てています（標準ライブラリだけで動きます）。

```bash
cd docs/explainer/code-map-images/source
python3 features.py           # 逆引きのファイル一覧を検証して features.json を作る
python3 build_codemap.py      # code-map.html
python3 build_interview_spec.py  # ai-interview-spec.html
python3 build_kids.py         # how-it-works.html
python3 build_images.py       # 画像用の images.html
```

生成した HTML はカレントディレクトリに出るので、`docs/explainer/` 直下へ移してください。

画像は Puppeteer（`puppeteer-core`）で撮ります。ブラウザは手元の Google Chrome を使います（`CHROME_BIN` で変更可）。

```bash
cd docs/explainer/tools
npm install
npm run shots                 # 全部撮る
npm run shots -- system s3    # id を指定して一部だけ撮る
SCALE=2 npm run shots         # 2倍の解像度で撮る
```

X 用画像の元は `x-images/source/slides.html` です。
