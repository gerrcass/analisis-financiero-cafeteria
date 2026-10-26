import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

import {
  SCENARIO_KEYS,
  buildModel,
  loanPayment,
  productEconomics,
  staffCosts
} from '../../site/js/model.js';

const inputs = JSON.parse(readFileSync(new URL('../../data/model.json', import.meta.url)));
const expected = JSON.parse(readFileSync(new URL('../../data/expected.json', import.meta.url)));

const MONEY_FIELDS = new Set([
  'revenue',
  'cogs',
  'grossProfit',
  'personnel',
  'opex',
  'ebitda',
  'depreciation',
  'ebit',
  'interest',
  'ebt',
  'tax',
  'netIncome',
  'closingCash',
  'fcff',
  'fcfe',
  'cfo',
  'maintenanceCapex',
  'workingCapitalChange',
  'principal'
]);

function assertClose(actual, wanted, tolerance, label) {
  assert.ok(
    Number.isFinite(actual),
    `${label}: el valor no es finito (${actual})`
  );
  assert.ok(
    Math.abs(actual - wanted) <= tolerance,
    `${label}: ${actual} frente a ${wanted} (tolerancia ${tolerance})`
  );
}

test('el contrato cumple las sumas y el orden congelados', () => {
  const products = productEconomics(inputs);
  assert.equal(Math.round(products.reduce((sum, p) => sum + p.mix, 0) * 100), 100);
  assertClose(
    inputs.calendar.seasonality.reduce((sum, value) => sum + value, 0),
    12,
    1e-9,
    'estacionalidad'
  );
  assert.equal(
    inputs.calendar.openingDays.reduce((sum, value) => sum + value, 0),
    312
  );
  const capex = inputs.capex.items.reduce((sum, item) => sum + item.amount, 0);
  assert.equal(capex, 132000);
  assert.equal(
    inputs.financing.equity + inputs.financing.loanAmount,
    capex + inputs.financing.initialStock + inputs.financing.openingCash
  );
  assert.equal(SCENARIO_KEYS.length, 3);
  assertClose(loanPayment(70000, 0.075, 60), 1402.6564, 0.01, 'cuota');
});

test('los tres escenarios reproducen los objetivos dorados', () => {
  for (const key of SCENARIO_KEYS) {
    const result = buildModel(inputs, key);
    const golden = expected.scenarios[key];
    for (const year of ['2026', '2027', '2028']) {
      for (const [field, wanted] of Object.entries(golden.annual[year])) {
        const tolerance = MONEY_FIELDS.has(field) ? expected.meta.tolerance.eur : 0.1;
        assertClose(result.annual[year][field], wanted, tolerance, `${key}/${year}/${field}`);
      }
    }
    assert.equal(result.paybackProjectMonths, golden.paybackProjectMonths);
    assert.equal(result.paybackEquityMonths, golden.paybackEquityMonths);
    assertClose(result.cumulativeFcfe, golden.cumulativeFcfe, 1, `${key}/cumulativeFcfe`);
    assertClose(result.cashOnCash * 100, golden.cashOnCash, 0.1, `${key}/cashOnCash`);
  }
});

test('las identidades contables y de caja se cumplen mes a mes', () => {
  for (const key of SCENARIO_KEYS) {
    const result = buildModel(inputs, key);
    for (const month of result.months) {
      assertClose(month.grossProfit, month.revenue - month.cogs, 1e-6, 'margen bruto');
      assertClose(month.ebitda, month.grossProfit - month.totalOpex, 1e-6, 'EBITDA');
      assertClose(month.ebit, month.ebitda - month.depreciation, 1e-6, 'EBIT');
      assertClose(month.ebt, month.ebit - month.interest, 1e-6, 'EBT');
      assertClose(month.netIncome, month.ebt - month.tax, 1e-6, 'beneficio neto');
      assertClose(
        month.closingCash,
        month.openingCash + month.fcfe,
        1e-6,
        'caja final'
      );
      assertClose(
        month.fcfe,
        month.fcff - month.interest + month.taxShield - month.principal,
        1e-6,
        'FCFE'
      );
      assertClose(
        month.fcfe,
        month.netIncome +
          month.depreciation -
          month.maintenanceCapex -
          month.workingCapitalChange -
          month.principal,
        1e-6,
        'reconciliación'
      );
    }
    assert.ok(result.checks.cashReconciliation < 1e-6);
    assert.ok(result.checks.loanClosesAtZero < 0.01);
    assert.ok(result.checks.minimumCash > 10000);
  }
});

test('los escenarios están ordenados y el Pesimista es visible', () => {
  const pes = buildModel(inputs, 'pessimistic');
  const base = buildModel(inputs, 'base');
  const opt = buildModel(inputs, 'optimistic');
  assert.ok(pes.annual['2028'].revenue < base.annual['2028'].revenue);
  assert.ok(base.annual['2028'].revenue < opt.annual['2028'].revenue);
  assert.ok(pes.annual['2028'].ebitda < base.annual['2028'].ebitda);
  assert.ok(base.annual['2028'].ebitda < opt.annual['2028'].ebitda);
  assert.equal(pes.paybackProjectMonths, null);
  assert.equal(base.paybackProjectMonths, 34);
  assert.equal(opt.paybackProjectMonths, 25);
  assert.ok(pes.annual['2028'].netIncome > 0);
  assert.ok(pes.annual['2028'].netIncome < 1000);
});

test('las sensibilidades documentadas se reproducen', () => {
  const base = buildModel(inputs, 'base');
  const ebitda2026 = base.annual['2026'].ebitda;
  const demand = buildModel(inputs, 'base', { demandFactor: 0.9 });
  assertClose(demand.annual['2026'].ebitda - ebitda2026, -24027.79, 1, 'demanda -10 %');
  const price = buildModel(inputs, 'base', {}, { priceLevel: 1.05 });
  assertClose(price.annual['2026'].ebitda - ebitda2026, 18644.39, 1, 'precio +5 %');
  const staff = buildModel(inputs, 'base', { personnelFactor: 1.05 });
  assertClose(staff.annual['2026'].ebitda - ebitda2026, -5523, 1, 'personal +5 %');
  const rent = buildModel(inputs, 'base', { rentFactor: 1.1 });
  assertClose(rent.annual['2026'].ebitda - ebitda2026, -2280, 1, 'alquiler +10 %');
  const marketing = buildModel(inputs, 'base', { marketingPct: 0.04 });
  assertClose(marketing.annual['2026'].ebitda - ebitda2026, -3844.19, 1, 'marketing +1 pp');
  const cost = buildModel(inputs, 'base', { productCostInflation: 0.045 });
  assertClose(cost.annual['2026'].ebitda - ebitda2026, 0, 0.5, 'coste 2026');
  assertClose(cost.annual['2027'].ebitda - base.annual['2027'].ebitda, -1455.0, 1, 'coste 2027');
});

test('el coste de personal y la amortización salen del plan', () => {
  assert.deepEqual(
    staffCosts(inputs).map((value) => Math.round(value)),
    [110460, 129350, 133230]
  );
  const result = buildModel(inputs, 'base');
  assertClose(result.capex.annualDepreciation, 16625, 0.01, 'amortización anual');
  assertClose(result.capex.monthlyDepreciation, 1385.4167, 0.01, 'amortización mensual');
  assertClose(result.annual['2026'].personnel, 110460, 0.01, 'personal 2026');
});
