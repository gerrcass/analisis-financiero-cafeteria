import { LAB_CONTROLS, SCENARIO_META, buildModel } from './model.js';
import { COLORS, groupedBarChart } from './charts.js';

const SHORT_KEYS = {
  demandFactor: 'd',
  demandGrowth: 'g',
  priceGrowth: 'p',
  productCostInflation: 'c',
  personnelFactor: 's',
  rentFactor: 'r',
  servicesInflation: 'v',
  marketingPct: 'm',
  otherOpexFactor: 'o',
  otherOpexGrowth: 'x'
};

const KEY_BY_SHORT = Object.fromEntries(Object.entries(SHORT_KEYS).map(([key, short]) => [short, key]));

const eur0 = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
const eur2 = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', minimumFractionDigits: 2, maximumFractionDigits: 2 });
const pct1 = new Intl.NumberFormat('es-ES', { style: 'percent', minimumFractionDigits: 1, maximumFractionDigits: 1 });
const num1 = new Intl.NumberFormat('es-ES', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const controlByKey = Object.fromEntries(LAB_CONTROLS.map((control) => [control.key, control]));

function esc(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function formatValue(control, value) {
  if (control.percent) return pct1.format(value);
  return num1.format(value);
}

function paybackLabel(months) {
  return months === null ? '>36 meses' : `${months} meses`;
}

export function createLab({ inputs, scenarioKey, toast }) {
  let currentScenario = scenarioKey;
  let overrides = {};
  let debounceTimer = null;
  let lastResult = null;

  const container = document.getElementById('lab-controls');
  const resetButton = document.getElementById('lab-reset');
  const copyButton = document.getElementById('lab-copy');
  const callout = document.getElementById('lab-callout');

  function scenarioValues() {
    return inputs.scenarios[currentScenario];
  }

  function syncControls() {
    for (const control of LAB_CONTROLS) {
      const input = document.getElementById(`lab-${control.key}`);
      const display = document.getElementById(`lab-${control.key}-value`);
      const value = overrides[control.key] ?? scenarioValues()[control.key];
      if (input) input.value = String(value);
      if (display) display.textContent = formatValue(control, value);
    }
  }

  function renderControls() {
    if (!container) return;
    container.innerHTML = LAB_CONTROLS.map((control) => {
      const id = `lab-${control.key}`;
      const step = control.step;
      return `<div class="lab-control" data-lab-control="${control.key}">
        <div class="lab-control-head">
          <label for="${id}">${esc(control.label)}</label>
          <output for="${id}" id="${id}-value">—</output>
        </div>
        <input id="${id}" type="range" min="${control.min}" max="${control.max}" step="${step}" value="${scenarioValues()[control.key]}" aria-describedby="${id}-hint">
        <p class="lab-hint" id="${id}-hint">${esc(control.hint)} <span class="mono">(${esc(control.unit)})</span></p>
      </div>`;
    }).join('');

    for (const control of LAB_CONTROLS) {
      const input = document.getElementById(`lab-${control.key}`);
      input?.addEventListener('input', () => {
        const value = Number(input.value);
        if (Math.abs(value - scenarioValues()[control.key]) < 1e-9) {
          delete overrides[control.key];
        } else {
          overrides[control.key] = value;
        }
        const display = document.getElementById(`lab-${control.key}-value`);
        if (display) display.textContent = formatValue(control, value);
        window.clearTimeout(debounceTimer);
        debounceTimer = window.setTimeout(render, 30);
      });
    }
  }

  function hasOverrides() {
    return Object.keys(overrides).length > 0;
  }

  function encodeHash() {
    if (!hasOverrides()) return '';
    const pairs = LAB_CONTROLS.filter((control) => Object.hasOwn(overrides, control.key)).map((control) => {
      const value = overrides[control.key];
      const encoded = control.percent ? Math.round(value * 100 * 1000) / 1000 : Math.round(value * 1000) / 1000;
      return `${SHORT_KEYS[control.key]}:${encoded}`;
    });
    return pairs.length ? `lab=${pairs.join(',')}` : '';
  }

  function updateHash() {
    const url = new URL(window.location.href);
    const encoded = encodeHash();
    if (encoded) url.hash = encoded;
    else url.hash = '';
    window.history.replaceState({}, '', url);
  }

  function parseHash() {
    const hash = window.location.hash.replace(/^#/, '');
    if (!hash.startsWith('lab=')) return {};
    const parsed = {};
    for (const pair of hash.slice(4).split(',')) {
      const [short, raw] = pair.split(':');
      const key = KEY_BY_SHORT[short];
      if (!key || raw === undefined) continue;
      const control = controlByKey[key];
      let numeric = Number(raw);
      if (!Number.isFinite(numeric)) continue;
      if (control.percent) numeric /= 100;
      numeric = Math.min(control.max, Math.max(control.min, numeric));
      parsed[key] = numeric;
    }
    return parsed;
  }

  function delta(current, base, { margin = false, payback = false } = {}) {
    if (payback) {
      if (current === base) return '—';
      return `${paybackLabel(base)} → ${paybackLabel(current)}`;
    }
    if (margin) {
      const diff = (current - base) * 100;
      return `${diff >= 0 ? '+' : ''}${num1.format(diff)} pp`;
    }
    if (!base) return '—';
    const diff = current / base - 1;
    if (Math.abs(diff) < 0.00005) return '—';
    return `${diff >= 0 ? '+' : ''}${pct1.format(diff)}`;
  }

  function render() {
    if (!container) return;
    syncControls();
    const base = buildModel(inputs, currentScenario);
    const result = buildModel(inputs, currentScenario, overrides);
    lastResult = result;
    const annual2028 = result.annual['2028'];
    const base2028 = base.annual['2028'];

    setText('lab-revenue', eur0.format(annual2028.revenue));
    setText('lab-ebitda', eur0.format(annual2028.ebitda));
    setText('lab-cash', eur0.format(annual2028.closingCash));
    setText('lab-payback', paybackLabel(result.paybackProjectMonths));
    setText('lab-delta-revenue', delta(annual2028.revenue, base2028.revenue));
    setText('lab-delta-ebitda', delta(annual2028.ebitda, base2028.ebitda));
    setText('lab-delta-cash', delta(annual2028.closingCash, base2028.closingCash));
    setText('lab-delta-payback', delta(result.paybackProjectMonths, base.paybackProjectMonths, { payback: true }));
    setText('lab-status', hasOverrides() ? 'Personalizado' : `Escenario ${SCENARIO_META[currentScenario].name}`);
    setText(
      'lab-reading',
      hasOverrides()
        ? `Con estos supuestos, el negocio gana ${eur0.format(annual2028.netIncome)} € en 2028 y recupera la inversión ${result.paybackProjectMonths ? `en ${result.paybackProjectMonths} meses` : 'más allá de 36 meses'}.`
        : `Estás viendo ${SCENARIO_META[currentScenario].name} sin cambios. Mueve un supuesto para crear tu propio caso.`
    );

    document.getElementById('chart-lab').innerHTML = groupedBarChart({
      id: 'lab-chart',
      title: 'EBITDA 2026–2028 con tus supuestos',
      description: `EBITDA de ${annual2028 ? '2026, 2027 y 2028' : ''} con los supuestos del laboratorio.`,
      categories: ['2026', '2027', '2028'],
      series: [{ name: 'EBITDA', color: COLORS.sageStrong, values: [result.annual['2026'].ebitda, result.annual['2027'].ebitda, annual2028.ebitda] }],
      height: 240
    });

    const warning = result.checks.minimumCash < inputs.financing.minimumCash || result.paybackProjectMonths === null;
    if (callout) {
      callout.hidden = !warning;
      if (warning) {
        const reasons = [];
        if (result.checks.minimumCash < inputs.financing.minimumCash) {
          reasons.push(`la caja mínima baja a ${eur0.format(result.checks.minimumCash)} (política: ${eur0.format(inputs.financing.minimumCash)})`);
        }
        if (result.paybackProjectMonths === null) reasons.push('el payback supera los 36 meses');
        callout.innerHTML = `<strong>Ojo con la liquidez.</strong> Con estos supuestos, ${reasons.join(' y ')}. No es una quiebra: es una señal para revisar demanda, precios o estructura.`;
      }
    }
    updateHash();
  }

  function setText(id, text) {
    const element = document.getElementById(id);
    if (element) element.textContent = text;
  }

  function syncScenario(key) {
    currentScenario = key;
    overrides = {};
    syncControls();
    render();
  }

  function reset() {
    overrides = {};
    syncControls();
    render();
  }

  async function copyLink() {
    updateHash();
    const url = window.location.href;
    try {
      await navigator.clipboard.writeText(url);
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = url;
      textarea.setAttribute('readonly', '');
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
      } finally {
        textarea.remove();
      }
    }
    toast?.('Enlace copiado. Comparte el escenario y tus supuestos.');
  }

  renderControls();
  overrides = parseHash();
  syncControls();
  render();

  resetButton?.addEventListener('click', () => {
    reset();
    toast?.('Laboratorio restablecido al escenario seleccionado.');
  });
  copyButton?.addEventListener('click', copyLink);

  return {
    syncScenario,
    reset,
    hasOverrides,
    getResult: () => lastResult,
    getOverrides: () => ({ ...overrides })
  };
}
