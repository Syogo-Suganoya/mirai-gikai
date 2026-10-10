/**
 * _memo の画像（コード逆引き12枚・X用7枚）を撮り直す。
 *
 *   cd _memo/tools && npm install && npm run shots
 *
 * ブラウザは1つだけ起動して、ページの切り替えだけで全部撮る。
 * 高さは要素ごとのスクリーンショットに任せるので、事前に測らなくてよい。
 * Chrome は手元にあるものを使う（puppeteer-core なのでブラウザをダウンロードしない）。
 */

const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer-core");

const MEMO = path.resolve(__dirname, "..");
const CHROME =
  process.env.CHROME_BIN ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
// 1 なら幅 1600px。X に高解像度で出したいときは SCALE=2
const SCALE = Number(process.env.SCALE || 1);

const JOBS = [
  {
    // コード逆引き：縦の長さは図や表ごとに違う
    html: path.join(MEMO, "code-map-images/source/images.html"),
    outDir: path.join(MEMO, "code-map-images"),
    selector: "section.img",
    visible: ".img.on",
    viewport: { width: 1600, height: 900 },
    name: (id, i) => `${String(i + 1).padStart(2, "0")}-${id}.png`,
  },
  {
    // X 用：1600×900 固定
    html: path.join(MEMO, "x-images/source/slides.html"),
    outDir: path.join(MEMO, "x-images"),
    selector: "section.slide",
    visible: ".slide.on",
    viewport: { width: 1600, height: 900 },
    name: (_id, i) => `mirai-gikai-x-${String(i + 1).padStart(2, "0")}.png`,
  },
  {
    // X 投稿シリーズ：エンジニア向け4テーマ×4枚（1600×900 固定）
    html: path.join(MEMO, "x-posts/source/posts.html"),
    outDir: path.join(MEMO, "x-posts"),
    selector: "section.slide",
    visible: ".slide.on",
    viewport: { width: 1600, height: 900 },
    name: (id) => `${id}.png`,
  },
];

async function main() {
  const only = process.argv.slice(2); // 例: node shots.js system crosscut s3
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    args: ["--font-render-hinting=none"],
  });
  const page = await browser.newPage();
  page.on("pageerror", (e) => console.log(`[画面] ${e.message}`));

  for (const job of JOBS) {
    if (!fs.existsSync(job.html)) {
      console.log(`スキップ（見つからない）: ${job.html}`);
      continue;
    }
    await page.setViewport({ ...job.viewport, deviceScaleFactor: SCALE });
    const url = `file://${job.html}`;

    // 撮る対象の一覧は HTML の section の id から取る
    await page.goto(url, { waitUntil: "networkidle0" });
    const ids = await page.$$eval(job.selector, (els) => els.map((e) => e.id));

    for (const [i, id] of ids.entries()) {
      if (only.length && !only.includes(id)) continue;
      // 表示する section は location.hash で選ぶ作りなので、毎回読み込み直す
      await page.goto("about:blank");
      await page.goto(`${url}#${id}`, { waitUntil: "networkidle0" });
      await page.evaluate(() => document.fonts.ready);
      const el = await page.waitForSelector(job.visible, { timeout: 15000 });
      const out = path.join(job.outDir, job.name(id, i));
      await el.screenshot({ path: out });
      console.log(`撮影: ${path.relative(MEMO, out)}`);
    }
  }

  await browser.close();
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
