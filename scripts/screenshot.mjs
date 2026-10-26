import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';
import { chromium } from '@playwright/test';

const port = 4330;
const server = spawn('python3', ['-m', 'http.server', String(port), '--directory', 'docs'], {
  stdio: 'ignore'
});

async function waitForServer() {
  for (let attempt = 0; attempt < 80; attempt += 1) {
    try {
      const response = await fetch(`http://127.0.0.1:${port}/`);
      if (response.ok) return;
    } catch {
      // El servidor aún no está listo.
    }
    await sleep(100);
  }
  throw new Error('El servidor local no respondió');
}

let browser;
try {
  await waitForServer();
  browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1
  });
  await page.goto(`http://127.0.0.1:${port}/?escenario=base&anio=2028`, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.body.dataset.ready === 'true');
  await page.waitForTimeout(350);
  await page.screenshot({ path: 'docs/assets/screenshot-dashboard.png' });
  console.log('Captura escrita en docs/assets/screenshot-dashboard.png');
} finally {
  await browser?.close();
  server.kill('SIGTERM');
}
