/**
 * 画面遷移図に入れる、実際の画面のスクリーンショットを撮る。
 *
 *   npx supabase start && pnpm seed && pnpm dev   （リポジトリのルートで）
 *   cd 解説資料/tools && node app-shots.js
 *
 * ID はローカルのデータベースから選ぶ。管理画面は pnpm seed の管理者でログインする
 * （ADMIN_EMAIL / ADMIN_PASSWORD で変えられる）。
 */

const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer-core");

const OUT = path.resolve(__dirname, "../assets/screens");
const CHROME =
  process.env.CHROME_BIN ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const DB =
  process.env.DB_URL || "postgresql://postgres:postgres@127.0.0.1:54432/postgres";
const WEB = process.env.WEB_URL || "http://localhost:3000";
const ADMIN = process.env.ADMIN_URL || "http://localhost:3001";
const ADMIN_EMAIL = process.env.ADMIN_EMAIL || "admin@example.com";
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "admin123456";

function sql(q) {
  return execFileSync("psql", [DB, "-Atc", q], { encoding: "utf8" }).trim();
}

function ids() {
  // 公開中のレポートがあるインタビュー設定を1つ選ぶ
  const [report, session, config, bill] = sql(
    `select r.id, s.id, c.id, c.bill_id from interview_report r
       join interview_sessions s on s.id = r.interview_session_id
       join interview_configs c on c.id = s.interview_config_id
      where r.is_public_by_admin and r.is_public_by_user
      order by r.created_at limit 1`,
  ).split("|");
  const slug = sql("select slug from diet_sessions order by start_date desc limit 1");
  return { report, session, config, bill, slug };
}

function jobs({ report, session, config, bill, slug }) {
  const web = [
    ["web-home", "/"],
    ["web-bills", "/bills"],
    ["web-kokkai", `/kokkai/${slug}/bills`],
    ["web-bill", `/bills/${bill}`],
    ["web-interview", `/bills/${bill}/interview`],
    ["web-disclosure", `/bills/${bill}/interview/disclosure`],
    ["web-chat", `/bills/${bill}/interview/chat`],
    // 完了画面は本人しか見られない。web-chat で作られた自分のセッションに、一時的なレポートを付けて撮る
    ["web-complete", null],
    ["web-opinions", `/bills/${bill}/opinions`],
    ["web-topics", `/bills/${bill}/topics`],
    ["web-report", `/report/${report}`],
  ].map(([name, p]) => ({ name, url: p && WEB + p }));
  const iv = `/bills/${bill}/interview`;
  const admin = [
    ["admin-bills", "/bills"],
    ["admin-bill-new", "/bills/new"],
    ["admin-topic-analysis", `/bills/${bill}/user-topic-analysis`],
    ["admin-analysis-viewer", `/bills/${bill}/analysis-viewer`],
    ["admin-bill-edit", `/bills/${bill}/edit`],
    ["admin-contents-edit", `/bills/${bill}/contents/edit`],
    ["admin-interview", iv],
    ["admin-interview-edit", `${iv}/${config}/edit`],
    ["admin-reports", `${iv}/${config}/reports`],
    ["admin-report", `${iv}/${config}/reports/${session}`],
    ["admin-search", `${iv}/${config}/reports/search`],
    ["admin-old-topic", `${iv}/${config}/topic-analysis`],
    // ヘッダーのメニュー
    ["admin-diet-sessions", "/diet-sessions"],
    ["admin-tags", "/tags"],
    ["admin-interviews", "/interviews"],
    ["admin-experts", "/experts"],
    ["admin-admins", "/admins"],
  ].map(([name, p]) => ({ name, url: ADMIN + p, admin: true }));
  return [{ name: "admin-login", url: `${ADMIN}/login` }, ...web, ...admin];
}

/** web-chat を開いたときにできた自分のセッションに、既存のレポートの写しを付ける */
async function tempReport(config, from, started) {
  let session = "";
  // セッションは画面の読み込み後に作られるので、少し待つ
  for (let i = 0; i < 30 && !session; i++) {
    session = sql(
      `select id from interview_sessions
        where interview_config_id = '${config}' and created_at >= '${started}'
        order by created_at desc limit 1`,
    );
    if (!session) await new Promise((r) => setTimeout(r, 500));
  }
  if (!session) throw new Error("先に web-chat を撮ってください");
  const cols =
    "summary, stance, role, role_description, opinions, content_richness, role_title, moderation_score, is_public_by_admin, is_public_by_user";
  const id = sql(
    `insert into interview_report (interview_session_id, ${cols})
     select '${session}', ${cols} from interview_report where id = '${from}' returning id`,
  ).split("\n")[0];
  return { report: id, session };
}

async function login(page) {
  await page.goto(`${ADMIN}/login`, { waitUntil: "networkidle2" });
  await page.type('input[type="email"]', ADMIN_EMAIL);
  await page.type('input[type="password"]', ADMIN_PASSWORD);
  await Promise.all([
    page.waitForNavigation({ waitUntil: "networkidle2" }),
    page.click('button[type="submit"]'),
  ]);
}

async function main() {
  const only = process.argv.slice(2);
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    args: ["--font-render-hinting=none"],
  });
  const page = await browser.newPage();
  // 画面遷移図には上の方だけを小さく入れるので、横長の1画面分で十分
  await page.setViewport({ width: 1280, height: 800 });
  const id = ids();
  const started = sql("select now()");
  try {
    let loggedIn = false;
    for (const job of jobs(id)) {
      if (only.length && !only.includes(job.name)) continue;
      if (job.admin && !loggedIn) {
        await login(page);
        loggedIn = true;
      }
      let temp = null;
      if (job.name === "web-complete") {
        temp = await tempReport(id.config, id.report, started);
        job.url = `${WEB}/report/${temp.report}/complete`;
      }
      try {
        await page.goto(job.url, { waitUntil: "networkidle2", timeout: 90000 });
        // 開発用のインジケーター（左下の N など）を隠す
        await page.addStyleTag({ content: "nextjs-portal { display: none !important; }" });
        await new Promise((r) => setTimeout(r, 800));
        await page.screenshot({ path: path.join(OUT, `${job.name}.png`) });
        console.log(`ok ${job.name}  ${page.url()}`);
      } catch (e) {
        console.log(`NG ${job.name}  ${e.message}`);
      }
      if (temp) sql(`delete from interview_report where id = '${temp.report}'`);
    }
  } finally {
    await browser.close();
    // 撮影中にできたセッションと匿名ユーザーを消して、データベースを元に戻す
    sql(`delete from interview_sessions where created_at >= '${started}'`);
    sql(`delete from auth.users where is_anonymous and created_at >= '${started}'`);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
