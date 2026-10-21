// Снимает кейсы локально из site/ каждого репо: мобильный длинный кадр (для скролла в телефоне)
// и десктопный первый экран. reducedMotion — чтобы reveal-анимации не оставили пустые блоки.
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';

const OUT = process.argv[2];
const sites = {
  darya: '/home/user/darya-korysheva/site',
  fedoristov: '/home/user/fedoristovv/site',
  confiteria: '/home/user/healthy-confiteria/site',
  romantic: '/home/user/proposal.romantic.ua-/site',
  sirenita: '/home/user/sirenita_infantil/site',
  katya: '/home/user/feedee-ai/katya.tsibrovska/site',
  sylchuk: '/home/user/romasylchuk/site',
  alifannk: '/home/user/alifannk/site',
};
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
let port = 8700;
for (const [name, dir] of Object.entries(sites)) {
  port++;
  const srv = spawn('npx', ['http-server', dir, '-p', String(port), '-s', '-c-1', '-e', 'html'], { stdio: 'ignore' });
  await new Promise((r) => setTimeout(r, 1500));
  const url = `http://127.0.0.1:${port}/`;
  try {
    for (const mode of ['m', 'd']) {
      const ctx = await browser.newContext(
        mode === 'm'
          ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, reducedMotion: 'reduce' }
          : { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5, reducedMotion: 'reduce' }
      );
      const page = await ctx.newPage();
      await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
      // Прокрутка вниз будит lazy-картинки и IntersectionObserver-ы.
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < Math.min(h, 6000); y += 400) {
        await page.evaluate((y) => window.scrollTo(0, y), y);
        await page.waitForTimeout(150);
      }
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(1200);
      if (mode === 'm') {
        await page.screenshot({ path: `${OUT}/${name}-m.png`, fullPage: true, clip: { x: 0, y: 0, width: 390, height: Math.min(h, 4600) } });
      } else {
        await page.screenshot({ path: `${OUT}/${name}-d.png` });
      }
      await ctx.close();
    }
    console.log('ok', name);
  } catch (e) {
    console.log('fail', name, e.message);
  }
  srv.kill();
}
await browser.close();
