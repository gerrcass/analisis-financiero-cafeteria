import { buildModel } from './model.js';

const eur0 = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
const eur2 = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', minimumFractionDigits: 2, maximumFractionDigits: 2 });
const num1 = new Intl.NumberFormat('es-ES', { minimumFractionDigits: 1, maximumFractionDigits: 1 });

const byId = (id) => document.getElementById(id);
const value = (id) => Number(byId(id)?.value || 0);
const setText = (id, text) => {
  const element = byId(id);
  if (element) element.textContent = text;
};

function calculateTicket() {
  const tickets = value('calc-ticket-tickets');
  const items = value('calc-ticket-items');
  const price = value('calc-ticket-price');
  const days = value('calc-ticket-days');
  setText('calc-ticket-output', eur0.format(tickets * items * price * days));
}

function calculateBreakEven() {
  const fixed = value('calc-be-fixed');
  const contribution = value('calc-be-contribution');
  const days = value('calc-be-days');
  setText('calc-be-output', contribution > 0 && days > 0 ? `${num1.format(fixed / contribution / days)} tickets/día` : '—');
}

function calculateCash() {
  const fcfe =
    value('calc-cash-ebitda') -
    value('calc-cash-tax') -
    value('calc-cash-capex') -
    value('calc-cash-wc') -
    value('calc-cash-interest') +
    value('calc-cash-shield') -
    value('calc-cash-principal');
  setText('calc-cash-output', eur0.format(fcfe));
}

function bindCalculators() {
  const groups = [
    ['calc-ticket', ['calc-ticket-tickets', 'calc-ticket-items', 'calc-ticket-price', 'calc-ticket-days'], calculateTicket],
    ['calc-be', ['calc-be-fixed', 'calc-be-contribution', 'calc-be-days'], calculateBreakEven],
    ['calc-cash', ['calc-cash-ebitda', 'calc-cash-tax', 'calc-cash-capex', 'calc-cash-wc', 'calc-cash-interest', 'calc-cash-shield', 'calc-cash-principal'], calculateCash]
  ];
  for (const [, ids, fn] of groups) {
    for (const id of ids) {
      byId(id)?.addEventListener('input', fn);
    }
    fn();
  }
}

function bindNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('site-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('is-open', !open);
  });
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    });
  });
}

async function hydrateDefaults() {
  try {
    const response = await fetch('./data/model.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const inputs = await response.json();
    const base = buildModel(inputs, 'base');
    const annual = base.annual['2026'];
    const days = inputs.calendar.openingDays.reduce((sum, value) => sum + value, 0);
    const defaults = {
      'calc-ticket-tickets': annual.ticketsPerDay,
      'calc-ticket-items': inputs.calendar.itemsPerTicket,
      'calc-ticket-price': base.weightedNetPrice,
      'calc-ticket-days': days,
      'calc-be-fixed': annual.fixedCashCosts,
      'calc-be-contribution': annual.contributionPerTicket,
      'calc-be-days': days,
      'calc-cash-ebitda': annual.ebitda,
      'calc-cash-tax': annual.taxNoDebt,
      'calc-cash-capex': annual.maintenanceCapex,
      'calc-cash-wc': annual.workingCapitalChange,
      'calc-cash-interest': annual.interest,
      'calc-cash-shield': annual.taxShield,
      'calc-cash-principal': annual.principal
    };
    for (const [id, amount] of Object.entries(defaults)) {
      const input = byId(id);
      if (input) input.value = String(Math.round(amount * 10000) / 10000);
    }
  } catch (error) {
    // Los valores estáticos del HTML siguen siendo válidos para leer la fórmula.
    console.warn('No se pudo cargar el modelo para las calculadoras.', error);
  }
}

hydrateDefaults().finally(() => {
  bindCalculators();
  bindNav();
});
