import { expect, test } from '@playwright/test';

const BASE = '/';

test.describe('Cafetería Aurora — dashboard', () => {
  test('carga por defecto con Base 2028 y sin errores de consola', async ({ page }) => {
    const errors: string[] = [];
    const external: string[] = [];
    page.on('console', (message) => {
      if (message.type() === 'error') errors.push(message.text());
    });
    page.on('pageerror', (error) => errors.push(error.message));
    page.on('request', (request) => {
      const url = request.url();
      if (!url.startsWith('http://127.0.0.1:4322') && !url.startsWith('data:')) external.push(url);
    });

    await page.goto(BASE, { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toHaveAttribute('data-ready', 'true');
    await expect(page).toHaveTitle(/Cafetería Aurora/);
    await expect(page.locator('#kpi-revenue')).toContainText('460.864');
    await expect(page.locator('#kpi-ebitda')).toContainText('79.505');
    await expect(page.locator('#kpi-net')).toContainText('44.978');
    await expect(page.locator('#kpi-cash')).toContainText('132.063');
    await expect(page.locator('#kpi-payback')).toContainText('34 meses');
    await expect(page.locator('#kpi-payback-meta')).toContainText('30 meses');
    await expect(page.locator('#snap-margin')).toContainText('17,3');
    await expect(page.locator('.chart svg')).toHaveCount(6);
    expect(errors).toEqual([]);
    expect(external).toEqual([]);
  });

  test('cambia de escenario y actualiza KPIs, comparativa y URL', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    await page.getByRole('button', { name: 'Pesimista' }).click();
    await expect(page).toHaveURL(/escenario=pesimista/);
    await expect(page.locator('#kpi-revenue')).toContainText('378.796');
    await expect(page.locator('#kpi-net')).toContainText('134');
    await expect(page.locator('#snap-margin')).toContainText('5,2');
    await expect(page.locator('#table-comparison tbody tr.is-active')).toContainText('Pesimista');
    await expect(page.locator('#kpi-payback')).toContainText('>36 meses');

    await page.getByRole('button', { name: 'Optimista' }).click();
    await expect(page).toHaveURL(/escenario=optimista/);
    await expect(page.locator('#kpi-revenue')).toContainText('524.147');
    await expect(page.locator('#kpi-net')).toContainText('77.841');
    await expect(page.locator('#table-comparison tbody tr.is-active')).toContainText('Optimista');
    await expect(page).toHaveURL(/anio=2028/);
  });

  test('cambia de año y actualiza tablas y gráficos juntos', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    await page.getByRole('tab', { name: '2026' }).click();
    await expect(page).toHaveURL(/anio=2026/);
    await expect(page.locator('#kpi-revenue')).toContainText('384.419');
    await expect(page.locator('#kpi-ebitda')).toContainText('61.658');
    await expect(page.locator('#kpi-cash')).toContainText('57.456');
    await expect(page.locator('#revenue-margin')).toContainText('16,0');
    await expect(page.locator('#table-revenue-annual tbody tr.is-active')).toContainText('2026');
    await expect(page.locator('#comparison-title')).toContainText('2026');
    await expect(page.locator('#reading-revenue')).toContainText('2026');
    await expect(page.locator('#model-annual thead th')).toHaveCount(4);
  });

  test('el modelo completo alterna anual y mensual con primera columna fija', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    await expect(page.locator('#model-annual')).toBeVisible();
    await page.getByRole('button', { name: 'Mensual' }).click();
    await expect(page.locator('#model-monthly')).toBeVisible();
    await expect(page.locator('#model-annual')).toBeHidden();
    await expect(page.locator('#model-monthly thead th')).toHaveCount(37);
    await expect(page.locator('#model-monthly thead th').first()).toHaveClass(/sticky-col/);
    await page.getByRole('button', { name: 'Anual' }).click();
    await expect(page.locator('#model-annual')).toBeVisible();
  });

  test('la descarga entrega un Excel válido', async ({ page, request }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const link = page.locator('a[href$="Cafeteria-Aurora-Modelo-Financiero.xlsx"]').first();
    await expect(link).toHaveAttribute('download', '');
    const href = await link.getAttribute('href');
    expect(href).toBeTruthy();
    const response = await request.get(new URL(href!, page.url()).toString());
    expect(response.ok()).toBeTruthy();
    const body = await response.body();
    expect(body.subarray(0, 2).toString()).toBe('PK');
    expect(body.byteLength).toBeGreaterThan(50_000);
  });

  test('la URL es compartible y restaura escenario y año', async ({ page }) => {
    await page.goto('/?escenario=optimista&anio=2027', { waitUntil: 'networkidle' });
    await expect(page.locator('#kpi-revenue')).toContainText('479.145');
    await expect(page.locator('#kpi-payback')).toContainText('25 meses');
    await expect(page.locator('#snap-margin')).toContainText('20,9');
    await expect(page.locator('[data-scenario="optimistic"]')).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('[data-year="2027"]')).toHaveAttribute('aria-selected', 'true');
  });

  test('teclado: flechas cambian escenario y año', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    await page.locator('[data-scenario="base"]').focus();
    await page.keyboard.press('ArrowRight');
    await expect(page.locator('[data-scenario="optimistic"]')).toHaveAttribute('aria-pressed', 'true');
    await expect(page).toHaveURL(/escenario=optimista/);
    await page.locator('[data-year="2026"]').focus();
    await page.keyboard.press('ArrowRight');
    await expect(page.locator('[data-year="2027"]')).toHaveAttribute('aria-selected', 'true');
    await expect(page).toHaveURL(/anio=2027/);
  });

  test('responsive 390 y 768 sin overflow horizontal', async ({ page }) => {
    for (const viewport of [
      { width: 390, height: 844 },
      { width: 768, height: 1024 },
      { width: 1440, height: 900 }
    ]) {
      await page.setViewportSize(viewport);
      await page.goto(BASE, { waitUntil: 'networkidle' });
      const metrics = await page.evaluate(() => ({
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth
      }));
      expect(metrics.scrollWidth, `overflow a ${viewport.width}px`).toBeLessThanOrEqual(metrics.clientWidth + 1);
      await expect(page.locator('#kpi-revenue')).toBeVisible();
    }
  });

  test('menú móvil accesible', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const toggle = page.locator('.nav-toggle');
    await expect(toggle).toBeVisible();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect(page.locator('#site-nav')).toBeVisible();
    await page.locator('#site-nav a').first().click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  });

  test('accesibilidad básica: skip link, ARIA y gráficos descritos', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    await expect(page.locator('html')).toHaveAttribute('lang', 'es');
    await expect(page.locator('.skip-link')).toHaveAttribute('href', '#contenido');
    for (const button of await page.locator('[data-scenario]').all()) {
      await expect(button).toHaveAttribute('aria-pressed', /true|false/);
    }
    const charts = page.locator('.chart svg[role="img"]');
    expect(await charts.count()).toBe(6);
    for (let index = 0; index < (await charts.count()); index += 1) {
      const chart = charts.nth(index);
      await expect(chart.locator('title')).not.toHaveCount(0);
      await expect(chart.locator('desc')).not.toHaveCount(0);
      await expect(chart).toHaveAttribute('aria-labelledby', /.+-title .+-desc/);
    }
    await expect(page.locator('#table-products caption')).toContainText('Carta y margen');
    await expect(page.locator('#model-annual caption')).toContainText('Cuenta de resultados');
  });
});
