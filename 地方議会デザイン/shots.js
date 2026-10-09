/**
 * 使い方ガイド（mocks/guide.html）に載せる画面の写しを撮る。
 *
 *   cd 地方議会デザイン && npm install && npm run shots
 *
 * モックは静的HTMLなので、サーバーを立てずに file:// で開いて撮る。
 * モックを直したら撮り直すだけでガイドの画像が追随する。
 * Chrome は手元のものを使う。場所が違うときは CHROME_BIN で指定する。
 */

const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const puppeteer = require("puppeteer-core");

const MOCKS = path.join(__dirname, "mocks");
const OUT = process.env.OUT_DIR || path.join(MOCKS, "shots");
const CHROME =
  process.env.CHROME_BIN ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

// 公開サイトはスマホ、管理画面はPCで見る前提なので、幅を分ける。
const PHONE = { width: 390, height: 844 };
const DESKTOP = { width: 1280, height: 800 };

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// 撮るもの。selector を指定したものは、その要素が画面の上に来るまで送ってから撮る。
const SHOTS = [
  { name: "w1-select", file: "web-01-select.html", size: PHONE },
  { name: "w2-assembly", file: "web-02-assembly.html", size: PHONE },
  { name: "w3-bill", file: "web-03-bill.html", size: PHONE },
  {
    name: "w3-bill-actions",
    file: "web-03-bill.html",
    size: PHONE,
    selector: "#ask",
  },
  { name: "w4-submit", file: "web-04-submit.html", size: PHONE },
  { name: "w5-not-yet", file: "web-05-not-yet.html", size: PHONE },
  { name: "a1-assemblies", file: "admin-01-assemblies.html", size: DESKTOP },
  { name: "a2-dashboard", file: "admin-02-dashboard.html", size: DESKTOP },
  {
    name: "a3-upload",
    file: "admin-03-upload.html",
    size: { ...DESKTOP, height: 900 },
  },
  {
    name: "a4-review",
    file: "admin-04-review.html",
    size: { ...DESKTOP, height: 960 },
  },
  { name: "a5-submissions", file: "admin-05-submissions.html", size: DESKTOP },
  { name: "a6-members", file: "admin-06-members.html", size: DESKTOP },
];

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    args: ["--font-render-hinting=none"],
  });
  const page = await browser.newPage();
  page.on("pageerror", (e) => console.log(`[画面] ${e.message}`));

  for (const s of SHOTS) {
    await page.setViewport({ ...s.size, deviceScaleFactor: 2 });
    const url = pathToFileURL(path.join(MOCKS, s.file)).href;
    await page.goto(url, { waitUntil: "load" });
    // モック上部の注記バーと設計メモは実際の画面には出ないので消してから撮る。
    await page.addStyleTag({
      content: ".mock-bar, .note { display: none !important; }",
    });
    if (s.selector) {
      const found = await page.evaluate((sel) => {
        const el = document.querySelector(sel);
        if (!el) return false;
        window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 8);
        return true;
      }, s.selector);
      // 見出しが無いまま撮ると、ガイドの説明と違う画面が載ってしまう。
      if (!found) throw new Error(`${s.file} に ${s.selector} が無い`);
    } else {
      await page.evaluate(() => window.scrollTo(0, 0));
    }
    await sleep(300);
    await page.screenshot({ path: path.join(OUT, `${s.name}.png`) });
    console.log(`撮影: ${s.name}.png`);
  }

  await browser.close();
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
