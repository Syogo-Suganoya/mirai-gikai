# 解説資料

みらい議会のコードを読むための資料です。`develop @ 99840c65`（2026-10-06）時点のコードをもとに作っています。

| ファイル | 内容 |
| :-- | :-- |
| `コード逆引き.html` | 構成図5枚と、画面・API ごとの「機能 → ファイル」逆引き（38件・検索つき）、横断的な仕組みの置き場所 |
| `AIインタビュー仕様.html` | AI インタビューの設定・モード・ステージ遷移・出力形式・公開ルールなど（全15章） |
| `中学生向け_しくみ図鑑.html` | サービスの内部構造を中学生向けに説明した資料（全11章） |
| `code-map-images/` | コード逆引きを画像にしたもの（1600px 幅・12枚） |
| `x-images/` | X 投稿用の画像（1600×900・7枚） |

HTML はブラウザで直接開けます。

## 作り直す

HTML は Python のスクリプトで組み立てています（標準ライブラリだけで動きます）。

```bash
cd 解説資料/code-map-images/source
python3 features.py           # 逆引きのファイル一覧を検証して features.json を作る
python3 build_codemap.py      # コード逆引き.html
python3 build_interview_spec.py  # AIインタビュー仕様.html
python3 build_kids.py         # 中学生向け_しくみ図鑑.html
python3 build_images.py       # 画像用の images.html
```

生成した HTML はカレントディレクトリに出るので、`解説資料/` 直下へ移してください。

画像は Puppeteer（`puppeteer-core`）で撮ります。ブラウザは手元の Google Chrome を使います（`CHROME_BIN` で変更可）。

```bash
cd 解説資料/tools
npm install
npm run shots                 # 全部撮る
npm run shots -- system s3    # id を指定して一部だけ撮る
SCALE=2 npm run shots         # 2倍の解像度で撮る
```

X 用画像の元は `x-images/source/slides.html` です。
