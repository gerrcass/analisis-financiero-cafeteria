import { buildModel, SCENARIO_KEYS, SCENARIO_META, URL_SCENARIO_ALIASES } from './model.js';
import {
  bulletChart,
  comboChart,
  donutChart,
  groupedBarChart,
  horizontalBarChart,
  lineChart,
  COLORS,
  kEur,
  pct
} from './charts.js';

const state = {
  scenario: 'base',
  year: 2028,
  inputs: null,
  models: {},
  view: 'annual'
};

const eur0 = new Intl.NumberFormat('es-ES', {
  style: 'currency',
  currency: 'EUR',
  maximumFractionDigits: 0
});
const eur2 = new Intl.NumberFormat('es-ES', {
  style: 'currency',
  currency: 'EUR',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});
const pct1 = new Intl.NumberFormat('es-ES', { style: 'percent', minimumFractionDigits: 1, maximumFractionDigits: 1 });
const pct2 = new Intl.NumberFormat('es-ES', { style: 'percent', maximumFractionDigits: 2 });
const num0 = new Intl.NumberFormat('es-ES', { maximumFractionDigits: 0 });
const num1 = new Intl.NumberFormat('es-ES', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const nf2 = new Intl.NumberFormat('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const MONTH_SHORT = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];

function esc(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function monthLabel(month) {
  return `${MONTH_SHORT[month.calendarMonth - 1]}-${String(month.year).slice(2)}`;
}

function paybackText(months) {
  return months === null ? '>36 meses' : `${months} meses`;
}

function paybackShort(months) {
  return months === null ? '>36' : String(months);
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function setHtml(id, value) {
  const element = document.getElementById(id);
  if (element) element.innerHTML = value;
}

function setValue(id, raw, formatted) {
  const element = document.getElementById(id);
  if (!element) return;
  element.textContent = formatted;
  element.dataset.value = String(raw);
}

function deltaCell(current, previous, { margin = false } = {}) {
  if (!previous) return { text: 'año de rampa; sin comparación', className: '' };
  if (margin) {
    const diff = (current - previous) * 100;
    return {
      text: `${diff >= 0 ? '↑' : '↓'} ${nf2.format(Math.abs(diff))} pp vs año anterior`,
      className: diff >= 0 ? 'positive' : 'negative'
    };
  }
  const diff = current / previous - 1;
  return {
    text: `${diff >= 0 ? '↑' : '↓'} ${pct1.format(Math.abs(diff))} vs año anterior`,
    className: diff >= 0 ? 'positive' : 'negative'
  };
}

function dataTable({ caption, headers, rows, rowClasses = [], tableClass = '', firstColumnSticky = false }) {
  const head = headers
    .map((header, index) => `<th scope="col"${index === 0 && firstColumnSticky ? ' class="sticky-col"' : ''}>${header}</th>`)
    .join('');
  const body = rows
    .map((row, rowIndex) => {
      const cells = row
        .map((cell, cellIndex) => {
          const tag = rowIndex === rows.length - 1 && rowClasses.includes('row-total') ? 'td' : 'td';
          return `<${tag}${cellIndex === 0 && firstColumnSticky ? ' class="sticky-col"' : ''}>${cell}</${tag}>`;
        })
        .join('');
      return `<tr class="${rowClasses[rowIndex] || ''}">${cells}</tr>`;
    })
    .join('');
  return `<div class="table-wrap"><table class="data-table ${tableClass}">
    <caption>${caption}</caption>
    <thead><tr>${head}</tr></thead>
    <tbody>${body}</tbody>
  </table></div>`;
}

function parseState() {
  const params = new URLSearchParams(window.location.search);
  const scenario = URL_SCENARIO_ALIASES[params.get('escenario')] || 'base';
  const year = Number(params.get('anio'));
  state.scenario = SCENARIO_KEYS.includes(scenario) ? scenario : 'base';
  state.year = [2026, 2027, 2028].includes(year) ? year : 2028;
}

function updateUrl() {
  const url = new URL(window.location.href);
  url.searchParams.set('escenario', SCENARIO_META[state.scenario].urlKey);
  url.searchParams.set('anio', String(state.year));
  window.history.replaceState({}, '', url);
}

function activeResult() {
  return state.models[state.scenario];
}

function activeAnnual() {
  return activeResult().annual[String(state.year)];
}

function renderSelectors() {
  document.querySelectorAll('[data-scenario]').forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.scenario === state.scenario));
  });
  document.querySelectorAll('[data-year]').forEach((button) => {
    button.setAttribute('aria-selected', String(Number(button.dataset.year) === state.year));
    button.tabIndex = Number(button.dataset.year) === state.year ? 0 : -1;
  });
  const meta = SCENARIO_META[state.scenario];
  setText(
    'scenario-context',
    `${meta.name}: ${meta.summary} Los tres escenarios comparten catálogo, plantilla, capex y deuda.`
  );
}

function renderHero() {
  const result = activeResult();
  const annual = activeAnnual();
  const previous = state.year > 2026 ? result.annual[String(state.year - 1)] : null;
  const name = SCENARIO_META[state.scenario].name;

  setValue('kpi-revenue', annual.revenue, eur0.format(annual.revenue));
  setValue('kpi-ebitda', annual.ebitda, eur0.format(annual.ebitda));
  setValue('kpi-net', annual.netIncome, eur0.format(annual.netIncome));
  setValue('kpi-cash', annual.closingCash, eur0.format(annual.closingCash));
  setValue('kpi-payback', result.paybackProjectMonths ?? '>36', paybackText(result.paybackProjectMonths));

  setText('kpi-revenue-meta', previous ? `${deltaCell(annual.revenue, previous.revenue).text}` : 'año de rampa');
  setText('kpi-ebitda-meta', `${pct1.format(annual.ebitdaMargin)} del ingreso`);
  setText('kpi-net-meta', `${pct1.format(annual.netMargin)} del ingreso`);
  setText('kpi-cash-meta', `mínimo ${eur0.format(result.checks.minimumCash)}`);
  setText('kpi-payback-meta', `equity: ${paybackText(result.paybackEquityMonths)} · ${name} ${state.year}`);

  const cards = [
    { id: 'snap-revenue', raw: annual.revenue, display: eur0.format(annual.revenue), previous: previous?.revenue, margin: false },
    { id: 'snap-ebitda', raw: annual.ebitda, display: eur0.format(annual.ebitda), previous: previous?.ebitda, margin: false },
    { id: 'snap-margin', raw: annual.ebitdaMargin, display: pct1.format(annual.ebitdaMargin), previous: previous?.ebitdaMargin, margin: true },
    { id: 'snap-net', raw: annual.netIncome, display: eur0.format(annual.netIncome), previous: previous?.netIncome, margin: false },
    { id: 'snap-cash', raw: annual.closingCash, display: eur0.format(annual.closingCash), previous: previous?.closingCash, margin: false }
  ];
  for (const card of cards) {
    setValue(card.id, card.raw, card.display);
    const element = document.getElementById(`${card.id}-delta`);
    if (!element) continue;
    const delta = deltaCell(card.raw, card.previous, { margin: card.margin });
    element.textContent = delta.text;
    element.className = `delta ${delta.className}`;
  }
}

function renderComparison() {
  const year = state.year;
  const labels = SCENARIO_KEYS.map((key) => SCENARIO_META[key].name);
  const values = SCENARIO_KEYS.map((key) => state.models[key].annual[String(year)]);
  const revenue = values.map((item) => item.revenue);
  const ebitda = values.map((item) => item.ebitda);
  const net = values.map((item) => item.netIncome);
  const description = `Comparativa de ${year}: ingresos, EBITDA y beneficio neto de los escenarios Pesimista, Base y Optimista.`;
  setHtml(
    'chart-comparison',
    groupedBarChart({
      id: 'comparison',
      title: `Los tres escenarios en ${year}`,
      description,
      categories: labels,
      series: [
        { name: 'Ingresos', color: COLORS.terracotta, values: revenue },
        { name: 'EBITDA', color: COLORS.sageStrong, values: ebitda },
        { name: 'Beneficio neto', color: COLORS.goldStrong, values: net }
      ]
    })
  );
  setText('comparison-sub', `Mismo año, tres hipótesis. ${year} · importes netos de IVA.`);
  setText(
    'comparison-caption',
    `Ingresos de ${eur0.format(Math.min(...revenue))} a ${eur0.format(Math.max(...revenue))}. El Pesimista no se esconde.`
  );

  const rows = values.map((item, index) => [
    `<strong>${SCENARIO_META[SCENARIO_KEYS[index]].name}</strong>`,
    eur0.format(item.revenue),
    eur0.format(item.ebitda),
    eur0.format(item.netIncome),
    eur0.format(item.closingCash)
  ]);
  setHtml(
    'table-comparison',
    dataTable({
      caption: `Comparativa de escenarios · ${year}`,
      headers: ['Escenario', 'Ingresos', 'EBITDA', 'Beneficio neto', 'Caja final'],
      rows,
      rowClasses: SCENARIO_KEYS.map((key) => (key === state.scenario ? 'is-active' : ''))
    })
  );

  const base = state.models.base.annual[String(year)];
  const pes = state.models.pessimistic.annual[String(year)];
  const opt = state.models.optimistic.annual[String(year)];
  setText('range-revenue', `${eur0.format(pes.revenue)} – ${eur0.format(opt.revenue)}`);
  setText('range-revenue-meta', `Base: ${eur0.format(base.revenue)}`);
  setText('range-ebitda', `${eur0.format(pes.ebitda)} – ${eur0.format(opt.ebitda)}`);
  setText('range-ebitda-meta', `Base: ${eur0.format(base.ebitda)}`);
  setText(
    'comparison-reading',
    `En ${year}, la horquilla de ingresos va de ${eur0.format(pes.revenue)} (Pesimista) a ${eur0.format(opt.revenue)} (Optimista). El beneficio neto del Pesimista es ${eur0.format(pes.netIncome)}; el del Base, ${eur0.format(base.netIncome)}.`
  );
}

function renderRevenue() {
  const result = activeResult();
  const annual = activeAnnual();
  const name = SCENARIO_META[state.scenario].name;
  const labels = result.months.map(monthLabel);
  const description = `Ingresos netos y EBITDA de ${name}, 36 meses, de enero de 2026 a diciembre de 2028.`;
  setHtml(
    'chart-revenue',
    comboChart({
      id: 'revenue-chart',
      title: `Ingresos y EBITDA — ${name}`,
      description,
      labels,
      bars: { name: 'Ingresos', color: COLORS.terracotta, values: result.months.map((month) => month.revenue) },
      line: { name: 'EBITDA', color: COLORS.sageStrong, values: result.months.map((month) => month.ebitda) }
    })
  );
  setText('revenue-sub', `${name} · barras: ingresos netos; línea: EBITDA.`);
  setText('revenue-caption', `36 meses · ${name} · importes en €, netos de IVA.`);

  const rows = [2026, 2027, 2028].map((year) => {
    const item = result.annual[String(year)];
    return [
      `<strong>${year}</strong>`,
      eur0.format(item.revenue),
      eur0.format(item.ebitda),
      pct1.format(item.ebitdaMargin),
      eur0.format(item.netIncome)
    ];
  });
  setHtml(
    'table-revenue-annual',
    dataTable({
      caption: 'Resumen anual · importes netos de IVA',
      headers: ['Año', 'Ingresos', 'EBITDA', 'Margen EBITDA', 'Beneficio neto'],
      rows,
      rowClasses: [state.year === 2026 ? 'is-active' : '', state.year === 2027 ? 'is-active' : '', state.year === 2028 ? 'is-active' : '']
    })
  );

  const monthlyRows = result.months.map((month) => [
    monthLabel(month),
    eur0.format(month.revenue),
    eur0.format(month.ebitda),
    eur0.format(month.netIncome),
    eur0.format(month.closingCash)
  ]);
  setHtml(
    'table-revenue-monthly',
    dataTable({
      caption: `Serie mensual · ${name} · importes netos de IVA`,
      headers: ['Mes', 'Ingresos', 'EBITDA', 'Beneficio neto', 'Caja final'],
      rows: monthlyRows
    })
  );

  setValue('revenue-margin', annual.ebitdaMargin, pct1.format(annual.ebitdaMargin));
  setText('revenue-margin-meta', `${eur0.format(annual.ebitda)} de EBITDA`);
  setValue('revenue-ticket', annual.averageTicketNet, eur2.format(annual.averageTicketNet));
  setText('revenue-ticket-gross', eur2.format(annual.averageTicketGross));

  let reading;
  if (state.scenario === 'base' && state.year === 2028) {
    reading = '2026 arranca con rampa; 2027 absorbe el escalón de personal; 2028 amplía el margen. El ticket medio sube con los precios, no con más ítems.';
  } else {
    reading = `En ${state.year}, ${name} vende ${eur0.format(annual.revenue)} y deja ${eur0.format(annual.ebitda)} de EBITDA (${pct1.format(annual.ebitdaMargin)}). El ticket medio neto es ${eur2.format(annual.averageTicketNet)}.`;
  }
  setText('reading-revenue', reading);
}

function renderCash() {
  const result = activeResult();
  const annual = activeAnnual();
  const name = SCENARIO_META[state.scenario].name;
  const labels = result.months.map(monthLabel);
  const minimum = result.months.reduce((best, month) => (month.closingCash < best.closingCash ? month : best), result.months[0]);
  const description = `Caja final y deuda viva de ${name}, 36 meses. La caja mínima es ${eur0.format(minimum.closingCash)} en ${monthLabel(minimum)}.`;
  setHtml(
    'chart-cash',
    lineChart({
      id: 'cash-chart',
      title: `Caja y deuda — ${name}`,
      description,
      labels,
      series: [
        { name: 'Caja final', color: COLORS.espresso, values: result.months.map((month) => month.closingCash), area: true },
        { name: 'Deuda viva', color: COLORS.terracotta, values: result.months.map((month) => month.debtClosing) }
      ],
      band: { from: 0, to: 10000, color: COLORS.negative },
      minValue: 0
    })
  );
  setText('cash-sub', `${name} · la banda marca la caja mínima de política (10.000 €).`);
  setText('cash-caption', `36 meses · ${name} · caja final y deuda viva al cierre de cada mes.`);

  const monthlyRows = result.months.map((month) => [
    monthLabel(month),
    eur0.format(month.openingCash),
    eur0.format(month.fcfe),
    eur0.format(month.closingCash),
    eur0.format(month.debtClosing)
  ]);
  setHtml(
    'table-cash-monthly',
    dataTable({
      caption: `Caja y deuda · ${name}`,
      headers: ['Mes', 'Caja inicial', 'FCFE', 'Caja final', 'Deuda viva'],
      rows: monthlyRows
    })
  );

  setValue('cash-min', minimum.closingCash, eur0.format(minimum.closingCash));
  setText('cash-min-meta', `${monthLabel(minimum)} · mínimo de los 36 meses`);
  setValue('cash-payback', result.paybackProjectMonths ?? '>36', paybackText(result.paybackProjectMonths));
  setText('cash-payback-meta', `equity: ${paybackText(result.paybackEquityMonths)}`);
  setValue('cash-dscr', annual.dscr, `${nf2.format(annual.dscr)}×`);
  setValue('cash-debt', annual.debtClosing, eur0.format(annual.debtClosing));
  setText('dscr-year', String(state.year));
  setText('debt-year', String(state.year));
  setText(
    'reading-cash',
    `La caja mínima de ${name} es ${eur0.format(minimum.closingCash)} y llega en ${monthLabel(minimum)}. El DSCR de ${state.year} es ${nf2.format(annual.dscr)}×: ${annual.dscr >= 1.5 ? 'hay colchón sobre el servicio de la deuda.' : annual.dscr >= 1 ? 'cubre la deuda, pero sin mucho margen.' : 'no cubre el servicio de la deuda.'}`
  );
}

function renderProducts() {
  const result = activeResult();
  const annual = activeAnnual();
  const name = SCENARIO_META[state.scenario].name;
  const block = result.productProfitability.find((item) => item.year === state.year);
  const yearIndex = state.year - 2026;
  const priceIndex = (1 + result.scenario.priceGrowth) ** yearIndex;
  const costIndex = (1 + result.scenario.productCostInflation) ** yearIndex;
  const rows = block.products
    .map((product) => {
      const meta = result.products.find((item) => item.id === product.id);
      const netPrice = meta.netPrice * priceIndex;
      const adjustedCost = meta.adjustedCost * costIndex;
      const unitMargin = product.units ? (product.revenue - product.cogs) / product.units : netPrice - adjustedCost;
      return {
        product: meta,
        pvp: meta.pvp * priceIndex,
        netPrice,
        adjustedCost,
        unitMargin,
        marginPct: product.marginPct,
        revenue: product.revenue,
        share: product.revenue / annual.revenue
      };
    })
    .sort((a, b) => b.revenue - a.revenue);

  setHtml(
    'table-products',
    dataTable({
      caption: `Carta y márgenes · ${name} · ${state.year} · importes del año activo`,
      headers: ['Producto', 'PVP', 'Precio neto', 'Coste', 'Margen unit.', 'Margen %', 'Mix', 'Ingresos', '% ingresos'],
      rows: rows.map((row) => [
        `<strong>${esc(row.product.name)}</strong>`,
        eur2.format(row.pvp),
        eur2.format(row.netPrice),
        eur2.format(row.adjustedCost),
        eur2.format(row.unitMargin),
        pct1.format(row.marginPct),
        pct1.format(row.product.mix),
        eur0.format(row.revenue),
        pct1.format(row.share)
      ]),
      tableClass: 'product-table',
      firstColumnSticky: true
    })
  );
  setText('products-sub', `${name} · ${state.year} · PVP y coste con los índices del año; ordenado por ingresos.`);

  const sortedByMargin = [...rows].sort((a, b) => b.unitMargin - a.unitMargin);
  const description = `Margen unitario de los ocho productos en ${state.year}, de mayor a menor: ${sortedByMargin
    .map((row) => `${row.product.name} ${eur2.format(row.unitMargin)}`)
    .join('; ')}.`;
  const mobile = typeof window !== 'undefined' && window.matchMedia('(max-width: 600px)').matches;
  if (mobile) {
    const maxMargin = sortedByMargin[0]?.unitMargin || 1;
    setHtml(
      'chart-products',
      `<div class="product-bars-mobile" aria-label="${esc(description)}">
        ${sortedByMargin
          .map(
            (row) => `<div class="pb-row">
              <span class="pb-name">${esc(row.product.name)}</span>
              <span class="pb-track" aria-hidden="true"><span class="pb-fill" style="width:${(row.unitMargin / maxMargin) * 100}%"></span></span>
              <span class="pb-value">${eur2.format(row.unitMargin)}</span>
            </div>`
          )
          .join('')}
      </div>`
    );
  } else {
    setHtml(
      'chart-products',
      horizontalBarChart({
        id: 'products-chart',
        title: `Margen unitario por producto — ${name} ${state.year}`,
        description,
        items: sortedByMargin.map((row, index) => ({
          label: row.product.name,
          value: row.unitMargin,
          color: index % 2 === 0 ? COLORS.terracotta : COLORS.sageStrong
        })),
        valueLabel: 'Margen unitario',
        valueFormatter: (value) => eur2.format(value),
        height: 310
      })
    );
  }
  setText('product-chart-caption', `Margen unitario de ${state.year}, ordenado de mayor a menor. La barra no es el margen %: son euros por unidad vendida.`);

  const highestPct = [...rows].sort((a, b) => b.marginPct - a.marginPct)[0];
  const highestAbsolute = sortedByMargin[0];
  const bag = rows.find((row) => row.product.id === 'bolsa-cafe');
  setText(
    'reading-products',
    `En ${state.year}, ${highestPct.product.name} tiene el mayor margen % (${pct1.format(highestPct.marginPct)}). La unidad con mayor margen absoluto es ${highestAbsolute.product.name} (${eur2.format(highestAbsolute.unitMargin)}). La bolsa de café aporta el ${pct1.format(bag.share)} de los ingresos con solo el ${pct1.format(bag.product.mix)} del mix.`
  );
  setText('product-best-pct', pct1.format(highestPct.marginPct));
  setText('product-best-pct-meta', highestPct.product.name);
  setText('product-best-abs', eur2.format(highestAbsolute.unitMargin));
  setText('product-best-abs-meta', highestAbsolute.product.name);
  setText('product-bag-share', pct1.format(bag.share));
  setText('product-bag-mix', pct1.format(bag.product.mix));
}

function renderCosts() {
  const result = activeResult();
  const annual = activeAnnual();
  const name = SCENARIO_META[state.scenario].name;
  const months = result.months.filter((month) => month.year === state.year);
  const local = months.reduce((sum, month) => sum + month.rent + month.utilities + month.fixedServices, 0);
  const marketing = months.reduce((sum, month) => sum + month.fixedMarketing + month.variableMarketing, 0);
  const items = [
    { label: 'Producto', value: annual.cogs },
    { label: 'Personal', value: annual.personnel },
    { label: 'Local', value: local },
    { label: 'Marketing', value: marketing },
    { label: 'Otros', value: months.reduce((sum, month) => sum + month.otherOpex, 0) }
  ];
  const total = items.reduce((sum, item) => sum + item.value, 0);
  setHtml(
    'chart-costs',
    donutChart({
      id: 'costs-chart',
      title: `Estructura de costes — ${name} ${state.year}`,
      description: `Reparto del gasto total (${eur0.format(total)}): producto ${eur0.format(items[0].value)}, personal ${eur0.format(items[1].value)}, local ${eur0.format(items[2].value)}, marketing ${eur0.format(items[3].value)} y otros ${eur0.format(items[4].value)}. Los porcentajes de la dona son sobre el gasto total.`,
      items,
      centerLabel: 'Gasto total'
    })
  );
  setText('costs-sub', `${name} · ${state.year}. Dona: % del gasto total. Tabla y tarjetas: % de los ingresos.`);
  setText(
    'costs-caption',
    `El gasto total asciende a ${eur0.format(total)}. La dona reparte ese gasto; producto y personal suman el ${pct1.format((items[0].value + items[1].value) / annual.revenue)} de los ingresos.`
  );
  setHtml(
    'table-costs',
    dataTable({
      caption: `Costes por categoría · ${name} · ${state.year} · importe y % de los ingresos`,
      headers: ['Categoría', 'Importe', '% ingresos'],
      rows: [
        ...items.map((item) => [esc(item.label), eur0.format(item.value), pct1.format(item.value / annual.revenue)]),
        ['<strong>Total</strong>', `<strong>${eur0.format(total)}</strong>`, `<strong>${pct1.format(total / annual.revenue)}</strong>`]
      ],
      rowClasses: ['', '', '', '', '', 'row-total']
    })
  );
  setValue('cost-product', annual.cogs, eur0.format(annual.cogs));
  setText('cost-product-meta', `${pct1.format(annual.cogs / annual.revenue)} de los ingresos`);
  setValue('cost-personnel', annual.personnel, eur0.format(annual.personnel));
  setText('cost-personnel-meta', `${pct1.format(annual.personnel / annual.revenue)} de los ingresos`);
  setText(
    'reading-costs',
    `Producto ${pct1.format(items[0].value / annual.revenue)} de los ingresos + personal ${pct1.format(items[1].value / annual.revenue)} de los ingresos = ${pct1.format((items[0].value + items[1].value) / annual.revenue)} de cada euro facturado. La dona reparte el gasto total; esta lectura y las tarjetas usan ingresos como denominador.`
  );
}

function renderBreakEven() {
  const annual = activeAnnual();
  const name = SCENARIO_META[state.scenario].name;
  setHtml(
    'chart-break-even',
    bulletChart({
      id: 'break-even-chart',
      title: `Punto de equilibrio — ${name} ${state.year}`,
      description: `Tickets/día previstos ${num1.format(annual.ticketsPerDay)}, BE EBITDA ${num1.format(annual.breakEvenEbitda)} y BE total ${num1.format(annual.breakEvenTotal)}.`,
      max: 420,
      value: annual.ticketsPerDay,
      markers: [
        { label: 'BE EBITDA', value: annual.breakEvenEbitda },
        { label: 'BE total', value: annual.breakEvenTotal },
        { label: 'Real', value: annual.ticketsPerDay }
      ]
    })
  );
  setText('break-even-sub', `${name} · ${state.year} · la barra es la demanda prevista.`);
  setText(
    'break-even-caption',
    `Margen de seguridad: ${pct1.format(annual.safetyMargin)}. Si la demanda cae más que eso, el resultado antes de impuestos se vuelve negativo.`
  );
  setValue('be-ebitda', annual.breakEvenEbitda, num1.format(annual.breakEvenEbitda));
  setValue('be-total', annual.breakEvenTotal, num1.format(annual.breakEvenTotal));
  setValue('be-safety', annual.safetyMargin, pct1.format(annual.safetyMargin));
  setValue('be-contribution', annual.contributionPerTicket, eur2.format(annual.contributionPerTicket));
  setText('be-fixed', eur0.format(annual.fixedCashCosts));
  const cushion = annual.ticketsPerDay - annual.breakEvenTotal;
  setText(
    'reading-break-even',
    `Con ${num1.format(annual.ticketsPerDay)} tickets/día, ${name} puede perder ${num1.format(cushion)} tickets/día antes de entrar en pérdidas contables. El BE total añade amortización e intereses al EBITDA.`
  );
}

function modelRows(result, monthly = false) {
  const rows = [
    ['Ingresos netos', 'revenue'],
    ['COGS', 'cogs'],
    ['Margen bruto', 'grossProfit'],
    ['Personal', 'personnel'],
    ['Alquiler', 'rent'],
    ['Suministros', 'utilities'],
    ['Servicios fijos', 'fixedServices'],
    ['Marketing fijo', 'fixedMarketing'],
    ['Marketing variable', 'variableMarketing'],
    ['Otros gastos', 'otherOpex'],
    ['EBITDA', 'ebitda'],
    ['Amortización', 'depreciation'],
    ['EBIT', 'ebit'],
    ['Intereses', 'interest'],
    ['EBT', 'ebt'],
    ['Impuestos', 'tax'],
    ['Beneficio neto', 'netIncome']
  ];
  if (monthly) {
    return rows.map(([label, key]) => [label, ...result.months.map((month) => eur0.format(month[key]))]);
  }
  return rows.map(([label, key]) => [
    label,
    ...[2026, 2027, 2028].map((year) => eur0.format(result.annual[String(year)][key]))
  ]);
}

function renderModel() {
  const result = activeResult();
  const name = SCENARIO_META[state.scenario].name;
  const annualRows = modelRows(result);
  setHtml(
    'model-annual',
    dataTable({
      caption: `Cuenta de resultados anual · ${name} · importes netos de IVA`,
      headers: ['Concepto', '2026', '2027', '2028'],
      rows: annualRows,
      rowClasses: annualRows.map((row) => (['EBITDA', 'Beneficio neto'].includes(row[0]) ? 'is-active' : ''))
    })
  );

  const monthlyRows = modelRows(result, true);
  const headers = ['Concepto', ...result.months.map(monthLabel)];
  setHtml(
    'model-monthly',
    dataTable({
      caption: `Cuenta de resultados mensual · ${name} · importes netos de IVA`,
      headers,
      rows: monthlyRows,
      tableClass: 'monthly-table',
      firstColumnSticky: true
    })
  );
}

function renderAll() {
  renderSelectors();
  renderHero();
  renderComparison();
  renderRevenue();
  renderCash();
  renderProducts();
  renderCosts();
  renderBreakEven();
  renderModel();
  updateUrl();
  document.body.dataset.ready = 'true';
}

function toast(message) {
  const element = document.getElementById('toast');
  if (!element) return;
  element.textContent = message;
  element.classList.add('is-visible');
  window.clearTimeout(toast.timeout);
  toast.timeout = window.setTimeout(() => element.classList.remove('is-visible'), 2200);
}

function setScenario(key) {
  if (key === state.scenario) return;
  state.scenario = key;
  renderAll();
  toast(`${SCENARIO_META[key].name}: ${SCENARIO_META[key].summary}`);
}

function setYear(year) {
  if (year === state.year) return;
  state.year = year;
  renderAll();
}

function bindEvents() {
  const scenarioButtons = [...document.querySelectorAll('[data-scenario]')];
  scenarioButtons.forEach((button, index) => {
    button.addEventListener('click', () => setScenario(button.dataset.scenario));
    button.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      event.preventDefault();
      const direction = event.key === 'ArrowRight' ? 1 : -1;
      const next = (index + direction + scenarioButtons.length) % scenarioButtons.length;
      scenarioButtons[next].focus();
      setScenario(scenarioButtons[next].dataset.scenario);
    });
  });

  const yearButtons = [...document.querySelectorAll('[data-year]')];
  yearButtons.forEach((button, index) => {
    button.addEventListener('click', () => setYear(Number(button.dataset.year)));
    button.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      let next = index;
      if (event.key === 'ArrowRight') next = (index + 1) % yearButtons.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + yearButtons.length) % yearButtons.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = yearButtons.length - 1;
      yearButtons[next].focus();
      setYear(Number(yearButtons[next].dataset.year));
    });
  });

  document.querySelectorAll('[data-view]').forEach((button) => {
    button.addEventListener('click', () => {
      state.view = button.dataset.view;
      document.querySelectorAll('[data-view]').forEach((item) => {
        item.setAttribute('aria-pressed', String(item.dataset.view === state.view));
      });
      document.getElementById('model-annual').hidden = state.view !== 'annual';
      document.getElementById('model-monthly').hidden = state.view !== 'monthly';
    });
  });

  const navToggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('site-nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const open = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navToggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
      });
    });
  }

  window.addEventListener('popstate', () => {
    parseState();
    renderAll();
  });
}

async function init() {
  parseState();
  bindEvents();
  try {
    const response = await fetch('./data/model.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.inputs = await response.json();
    state.models = Object.fromEntries(SCENARIO_KEYS.map((key) => [key, buildModel(state.inputs, key)]));
    renderAll();
  } catch (error) {
    const box = document.getElementById('app-error');
    if (box) box.hidden = false;
    setText('scenario-context', 'No se pudo cargar el modelo. Sirve el sitio por HTTP.');
    console.error(error);
  }
}

const productMedia = window.matchMedia('(max-width: 600px)');
productMedia.addEventListener?.('change', () => {
  if (state.inputs) renderProducts();
});

init();
