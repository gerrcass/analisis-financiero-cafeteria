/**
 * Motor espejo del modelo financiero de Cafetería Aurora.
 *
 * Debe reproducir `scripts/model.py` y los objetivos dorados de
 * `data/expected.json`. No toca el DOM: es un módulo puro que consumen el
 * dashboard, el laboratorio, la guía y los tests de Node.
 */

export const SCENARIO_KEYS = ['pessimistic', 'base', 'optimistic'];

export const SCENARIO_META = {
  pessimistic: {
    key: 'pessimistic',
    name: 'Pesimista',
    urlKey: 'pesimista',
    tone: 'negative',
    summary:
      'El invierno largo: demanda un 12 % por debajo del plan, costes al alza y presión salarial.'
  },
  base: {
    key: 'base',
    name: 'Base',
    urlKey: 'base',
    tone: 'neutral',
    summary:
      'El plan creíble: demanda en el potencial del local, precios +2,5 % y costes +3,5 %.'
  },
  optimistic: {
    key: 'optimistic',
    name: 'Optimista',
    urlKey: 'optimista',
    tone: 'positive',
    summary:
      'Aurora se convierte en referencia: demanda +8 %, precios +3,2 % y mejor productividad.'
  }
};

export const URL_SCENARIO_ALIASES = {
  pesimista: 'pessimistic',
  pessimistic: 'pessimistic',
  base: 'base',
  optimista: 'optimistic',
  optimistic: 'optimistic'
};

export const LAB_CONTROLS = [
  {
    key: 'demandFactor',
    label: 'Factor de demanda año 1',
    unit: '×',
    min: 0.7,
    max: 1.2,
    step: 0.01,
    digits: 2,
    hint: 'Solo afecta a 2026; los años siguientes crecen desde aquí.'
  },
  {
    key: 'demandGrowth',
    label: 'Crecimiento anual de demanda',
    unit: '%',
    min: 0,
    max: 0.1,
    step: 0.005,
    digits: 1,
    percent: true,
    hint: 'Se compone en 2027 y 2028.'
  },
  {
    key: 'priceGrowth',
    label: 'Crecimiento anual de precios',
    unit: '%',
    min: 0,
    max: 0.06,
    step: 0.001,
    digits: 1,
    percent: true,
    hint: 'Se aplica en enero de cada año.'
  },
  {
    key: 'productCostInflation',
    label: 'Inflación anual de costes',
    unit: '%',
    min: 0,
    max: 0.08,
    step: 0.001,
    digits: 1,
    percent: true,
    hint: 'Afecta al COGS desde 2027.'
  },
  {
    key: 'personnelFactor',
    label: 'Factor de personal',
    unit: '×',
    min: 0.9,
    max: 1.15,
    step: 0.01,
    digits: 2,
    hint: 'Multiplica el coste empresa del plan de personal.'
  },
  {
    key: 'rentFactor',
    label: 'Factor de alquiler',
    unit: '×',
    min: 0.9,
    max: 1.15,
    step: 0.01,
    digits: 2,
    hint: 'Negociar 1.900 €/mes arriba o abajo cambia poco; el personal pesa más.'
  },
  {
    key: 'servicesInflation',
    label: 'Inflación de servicios',
    unit: '%',
    min: 0,
    max: 0.1,
    step: 0.001,
    digits: 1,
    percent: true,
    hint: 'Luz, gas, agua y servicios fijos.'
  },
  {
    key: 'marketingPct',
    label: 'Marketing variable',
    unit: '% ingresos',
    min: 0,
    max: 0.06,
    step: 0.001,
    digits: 1,
    percent: true,
    hint: 'No se asume que genere más demanda; es un coste.'
  },
  {
    key: 'otherOpexFactor',
    label: 'Factor de otros gastos',
    unit: '×',
    min: 0.85,
    max: 1.2,
    step: 0.01,
    digits: 2,
    hint: 'Limpieza, mantenimiento, banca y formación.'
  },
  {
    key: 'otherOpexGrowth',
    label: 'Crecimiento de otros gastos',
    unit: '%',
    min: 0,
    max: 0.06,
    step: 0.001,
    digits: 1,
    percent: true,
    hint: 'Se aplica desde 2027.'
  }
];

const MONTH_LABELS = [
  'ene',
  'feb',
  'mar',
  'abr',
  'may',
  'jun',
  'jul',
  'ago',
  'sep',
  'oct',
  'nov',
  'dic'
];

const OVERRIDE_KEYS = new Set(LAB_CONTROLS.map((control) => control.key));

function round2(value) {
  const rounded = Math.round((Number(value) + Number.EPSILON) * 100) / 100;
  return Object.is(rounded, -0) ? 0 : rounded;
}

export function loanPayment(principal, annualRate, months) {
  if (months <= 0) throw new Error('El plazo debe ser positivo.');
  const monthly = annualRate / 12;
  if (monthly === 0) return principal / months;
  return (principal * monthly) / (1 - (1 + monthly) ** -months);
}

export function amortizationSchedule(principal, annualRate, months) {
  const payment = loanPayment(principal, annualRate, months);
  const monthly = annualRate / 12;
  let balance = principal;
  const schedule = [];
  for (let month = 1; month <= months; month += 1) {
    const interest = balance * monthly;
    let principalPaid = Math.min(payment - interest, balance);
    if (balance <= 1e-9) principalPaid = 0;
    const opening = balance;
    balance = Math.max(0, balance - principalPaid);
    schedule.push({
      month,
      opening,
      interest,
      principal: principalPaid,
      closing: balance,
      payment: interest + principalPaid
    });
  }
  return schedule;
}

export function productEconomics(inputs) {
  return inputs.products.map((product) => {
    const netPrice = product.pvp / (1 + product.vat);
    const adjustedCost = product.unitCost / (1 - product.waste);
    const unitMargin = netPrice - adjustedCost;
    return {
      ...product,
      netPrice,
      adjustedCost,
      unitMargin,
      marginPct: netPrice ? unitMargin / netPrice : 0
    };
  });
}

export function staffCosts(inputs) {
  const { roles, employerSocialSecurity, salaryGrowth } = inputs.staff;
  return [0, 1, 2].map((year) => {
    const base = roles.reduce(
      (total, role) => total + role.grossSalary * role.fte[year],
      0
    );
    return base * (1 + employerSocialSecurity) * (1 + salaryGrowth) ** year;
  });
}

export function staffFteTotals(inputs) {
  return [0, 1, 2].map((year) =>
    inputs.staff.roles.reduce((total, role) => total + role.fte[year], 0)
  );
}

export function capexSummary(inputs) {
  const items = inputs.capex.items.map((item) => ({
    ...item,
    annualDepreciation: item.amount / item.lifeYears,
    monthlyDepreciation: item.amount / item.lifeYears / 12
  }));
  const total = items.reduce((sum, item) => sum + item.amount, 0);
  const annualDepreciation = items.reduce(
    (sum, item) => sum + item.annualDepreciation,
    0
  );
  return {
    items,
    total,
    annualDepreciation,
    monthlyDepreciation: annualDepreciation / 12
  };
}

function taxBag(annualResults, rate) {
  let losses = 0;
  const out = { tax: [], lossesStart: [], taxable: [], lossesEnd: [] };
  for (const result of annualResults) {
    out.lossesStart.push(losses);
    const base = Math.max(0, result - losses);
    out.taxable.push(base);
    out.tax.push(base * rate);
    losses = losses - Math.min(losses, Math.max(0, result)) + Math.max(0, -result);
    out.lossesEnd.push(losses);
  }
  return out;
}

export function applyOverrides(scenario, overrides = {}) {
  const resolved = { ...scenario };
  for (const [key, value] of Object.entries(overrides)) {
    if (!OVERRIDE_KEYS.has(key)) {
      throw new Error(`Override no permitido: ${key}`);
    }
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) throw new Error(`Override no numérico: ${key}`);
    resolved[key] = numeric;
  }
  return resolved;
}

export function resolveScenario(inputs, scenarioKey, overrides = {}) {
  if (!inputs.scenarios[scenarioKey]) {
    throw new Error(`Escenario desconocido: ${scenarioKey}`);
  }
  return applyOverrides(inputs.scenarios[scenarioKey], overrides);
}

export function buildModel(inputs, scenarioKey = 'base', overrides = {}, modifiers = {}) {
  const scenario = resolveScenario(inputs, scenarioKey, overrides);
  const priceLevel = Number(modifiers.priceLevel ?? 1);
  const costLevel = Number(modifiers.costLevel ?? 1);

  const { calendar, financing, tax, workingCapital } = inputs;
  const products = productEconomics(inputs);
  const weightedNetPrice = products.reduce(
    (sum, product) => sum + product.netPrice * product.mix,
    0
  );
  const weightedCost = products.reduce(
    (sum, product) => sum + product.adjustedCost * product.mix,
    0
  );
  const staffByYear = staffCosts(inputs);
  const capex = capexSummary(inputs);
  const loan = amortizationSchedule(
    financing.loanAmount,
    financing.loanRate,
    financing.loanMonths
  );
  const taxRate = tax.corporateRate;
  const wcDays =
    workingCapital.inventoryDays -
    workingCapital.payableDays +
    workingCapital.receivableDays;

  const months = [];
  for (let index = 0; index < 36; index += 1) {
    const monthNumber = index + 1;
    const yearIndex = Math.floor(index / 12);
    const calendarMonth = index % 12;
    const days = calendar.openingDays[calendarMonth];
    const ticketsPerDay =
      calendar.baseTicketsPerDay *
      scenario.demandFactor *
      (1 + scenario.demandGrowth) ** yearIndex *
      calendar.seasonality[calendarMonth] *
      (yearIndex === 0 ? calendar.ramp[calendarMonth] : 1);
    const tickets = ticketsPerDay * days;
    const items = tickets * calendar.itemsPerTicket;
    const revenue =
      items *
      weightedNetPrice *
      (1 + scenario.priceGrowth) ** yearIndex *
      priceLevel;
    const cogs =
      items *
      weightedCost *
      (1 + scenario.productCostInflation) ** yearIndex *
      costLevel;
    const grossProfit = revenue - cogs;
    const personnel = (staffByYear[yearIndex] * scenario.personnelFactor) / 12;
    const rent =
      inputs.fixedCosts.rent *
      scenario.rentFactor *
      (1 + inputs.fixedCosts.rentGrowth) ** yearIndex;
    const utilities =
      inputs.fixedCosts.utilities *
      (1 + scenario.servicesInflation) ** yearIndex;
    const fixedServices =
      inputs.fixedCosts.fixedServices *
      (1 + scenario.servicesInflation) ** yearIndex;
    const fixedMarketing =
      inputs.fixedCosts.fixedMarketing *
      (1 + inputs.fixedCosts.fixedMarketingGrowth) ** yearIndex;
    const variableMarketing = scenario.marketingPct * revenue;
    const otherOpex =
      inputs.fixedCosts.other *
      scenario.otherOpexFactor *
      (1 + scenario.otherOpexGrowth) ** yearIndex;
    const totalOpex =
      personnel +
      rent +
      utilities +
      fixedServices +
      fixedMarketing +
      variableMarketing +
      otherOpex;
    const ebitda = grossProfit - totalOpex;
    const depreciation = capex.monthlyDepreciation;
    const ebit = ebitda - depreciation;
    const debt = loan[monthNumber - 1];
    const interest = debt.interest;
    const principal = debt.principal;
    const ebt = ebit - interest;
    const workingCapital = (cogs * wcDays) / 365;
    months.push({
      index: monthNumber,
      month: monthNumber,
      year: calendar.years[yearIndex],
      yearIndex,
      calendarMonth: calendarMonth + 1,
      monthLabel: MONTH_LABELS[calendarMonth],
      openingDays: days,
      ticketsPerDay,
      tickets,
      items,
      revenue,
      cogs,
      grossProfit,
      personnel,
      rent,
      utilities,
      fixedServices,
      fixedMarketing,
      variableMarketing,
      otherOpex,
      totalOpex,
      ebitda,
      depreciation,
      ebit,
      interest,
      ebt,
      debtOpening: debt.opening,
      debtClosing: debt.closing,
      principal,
      workingCapital
    });
  }

  const annualEbt = [0, 1, 2].map((year) =>
    months
      .slice(year * 12, (year + 1) * 12)
      .reduce((sum, month) => sum + month.ebt, 0)
  );
  const annualEbit = [0, 1, 2].map((year) =>
    months
      .slice(year * 12, (year + 1) * 12)
      .reduce((sum, month) => sum + month.ebit, 0)
  );
  const taxWithDebt = taxBag(annualEbt, taxRate);
  const taxWithoutDebt = taxBag(annualEbit, taxRate);

  const initialStock = financing.initialStock;
  months.forEach((month, index) => {
    const yearIndex = month.yearIndex;
    const statementTax = taxWithDebt.tax[yearIndex] / 12;
    const theoreticalTax = taxWithoutDebt.tax[yearIndex] / 12;
    month.tax = statementTax;
    month.netIncome = month.ebt - statementTax;
    month.taxNoDebt = theoreticalTax;
    month.taxShield = theoreticalTax - statementTax;
    month.maintenanceCapex = month.revenue * inputs.capex.maintenancePct;
    const previousWc = index === 0 ? initialStock : months[index - 1].workingCapital;
    month.workingCapitalChange = month.workingCapital - previousWc;
    month.fcff =
      month.ebitda -
      month.taxNoDebt -
      month.maintenanceCapex -
      month.workingCapitalChange;
    month.fcfe =
      month.fcff - month.interest + month.taxShield - month.principal;
    month.openingCash =
      index === 0 ? financing.openingCash : months[index - 1].closingCash;
    month.closingCash = month.openingCash + month.fcfe;
    month.dscr =
      month.interest + month.principal
        ? (month.ebitda - month.tax) / (month.interest + month.principal)
        : 0;
    month.grossMargin = month.revenue ? month.grossProfit / month.revenue : 0;
    month.ebitdaMargin = month.revenue ? month.ebitda / month.revenue : 0;
    month.netMargin = month.revenue ? month.netIncome / month.revenue : 0;
  });

  const annual = {};
  calendar.years.forEach((year, yearIndex) => {
    const slice = months.slice(yearIndex * 12, (yearIndex + 1) * 12);
    const revenue = slice.reduce((sum, month) => sum + month.revenue, 0);
    const cogs = slice.reduce((sum, month) => sum + month.cogs, 0);
    const grossProfit = revenue - cogs;
    const personnel = slice.reduce((sum, month) => sum + month.personnel, 0);
    const opex = slice.reduce((sum, month) => sum + month.totalOpex - month.personnel, 0);
    const ebitda = grossProfit - personnel - opex;
    const depreciation = slice.reduce((sum, month) => sum + month.depreciation, 0);
    const ebit = ebitda - depreciation;
    const interest = slice.reduce((sum, month) => sum + month.interest, 0);
    const ebt = ebit - interest;
    const yearTax = taxWithDebt.tax[yearIndex];
    const netIncome = ebt - yearTax;
    const tickets = slice.reduce((sum, month) => sum + month.tickets, 0);
    const days = slice.reduce((sum, month) => sum + month.openingDays, 0);
    const ticketsPerDay = tickets / days;
    const fixedCashCosts =
      personnel +
      slice.reduce((sum, month) => sum + month.rent, 0) +
      slice.reduce((sum, month) => sum + month.utilities, 0) +
      slice.reduce((sum, month) => sum + month.fixedServices, 0) +
      slice.reduce((sum, month) => sum + month.fixedMarketing, 0) +
      slice.reduce((sum, month) => sum + month.otherOpex, 0);
    const variableMarketing = slice.reduce(
      (sum, month) => sum + month.variableMarketing,
      0
    );
    const contributionPerTicket = (revenue - cogs - variableMarketing) / tickets;
    const breakEvenEbitda = fixedCashCosts / contributionPerTicket / days;
    const breakEvenTotal =
      (fixedCashCosts + depreciation + interest) / contributionPerTicket / days;
    const principal = slice.reduce((sum, month) => sum + month.principal, 0);
    const fcfe = slice.reduce((sum, month) => sum + month.fcfe, 0);
    const fcff = slice.reduce((sum, month) => sum + month.fcff, 0);
    const workingCapitalChange = slice.reduce(
      (sum, month) => sum + month.workingCapitalChange,
      0
    );
    annual[year] = {
      year,
      openingCash: slice[0].openingCash,
      closingCash: slice[slice.length - 1].closingCash,
      revenue,
      cogs,
      grossProfit,
      grossMargin: revenue ? grossProfit / revenue : 0,
      personnel,
      personnelPct: revenue ? personnel / revenue : 0,
      opex,
      totalOpex: personnel + opex,
      ebitda,
      ebitdaMargin: revenue ? ebitda / revenue : 0,
      depreciation,
      ebit,
      ebitMargin: revenue ? ebit / revenue : 0,
      interest,
      ebt,
      tax: yearTax,
      taxable: taxWithDebt.taxable[yearIndex],
      taxLossesStart: taxWithDebt.lossesStart[yearIndex],
      taxLossesEnd: taxWithDebt.lossesEnd[yearIndex],
      netIncome,
      netMargin: revenue ? netIncome / revenue : 0,
      tickets,
      ticketsPerDay,
      averageTicketNet: tickets ? revenue / tickets : 0,
      averageTicketGross: tickets ? (revenue / tickets) * (1 + calendar.vat) : 0,
      breakEvenEbitda,
      breakEvenTotal,
      safetyMargin: (ticketsPerDay - breakEvenTotal) / ticketsPerDay,
      contributionPerTicket,
      fixedCashCosts,
      dscr: (ebitda - yearTax) / (interest + principal),
      principal,
      fcff,
      fcfe,
      cfo: netIncome + depreciation - workingCapitalChange,
      maintenanceCapex: slice.reduce((sum, month) => sum + month.maintenanceCapex, 0),
      workingCapitalChange,
      taxNoDebt: taxWithoutDebt.tax[yearIndex],
      taxShield: taxWithoutDebt.tax[yearIndex] - yearTax,
      debtClosing: slice[slice.length - 1].debtClosing
    };
  });

  const productProfitability = calendar.years.map((year, yearIndex) => {
    const yearItems = months
      .slice(yearIndex * 12, (yearIndex + 1) * 12)
      .reduce((sum, month) => sum + month.items, 0);
    return {
      year,
      products: products.map((product) => {
        const units = yearItems * product.mix;
        const revenue =
          units *
          product.netPrice *
          (1 + scenario.priceGrowth) ** yearIndex *
          priceLevel;
        const cogs =
          units *
          product.adjustedCost *
          (1 + scenario.productCostInflation) ** yearIndex *
          costLevel;
        const grossProfit = revenue - cogs;
        return {
          id: product.id,
          name: product.name,
          units,
          revenue,
          cogs,
          grossProfit,
          marginPct: revenue ? grossProfit / revenue : 0
        };
      })
    };
  });

  let cumulativeFcff = 0;
  let cumulativeFcfe = 0;
  let paybackProjectMonths = null;
  let paybackEquityMonths = null;
  const projectTarget = capex.total + initialStock;
  for (const month of months) {
    cumulativeFcff += month.fcff;
    cumulativeFcfe += month.fcfe;
    if (paybackProjectMonths === null && cumulativeFcff >= projectTarget) {
      paybackProjectMonths = month.month;
    }
    if (paybackEquityMonths === null && cumulativeFcfe >= financing.equity) {
      paybackEquityMonths = month.month;
    }
  }

  const minimumCash = Math.min(...months.map((month) => month.closingCash));
  const checks = {
    cashIdentity: Math.max(
      ...months.map((month) =>
        Math.abs(month.closingCash - (month.openingCash + month.fcfe))
      )
    ),
    cashReconciliation: Math.max(
      ...months.map((month) =>
        Math.abs(
          month.fcfe -
            (month.netIncome +
              month.depreciation -
              month.maintenanceCapex -
              month.workingCapitalChange -
              month.principal)
        )
      )
    ),
    loanClosesAtZero: loan[loan.length - 1].closing,
    minimumCash,
    paybackProjectMonths,
    paybackEquityMonths
  };

  return {
    scenarioKey,
    scenario,
    products,
    weightedNetPrice,
    weightedCost,
    staffCostByYear: staffByYear,
    staffFteByYear: staffFteTotals(inputs),
    capex,
    loan,
    loanPayment: loan[0].payment,
    months,
    annual,
    productProfitability,
    paybackProjectMonths,
    paybackEquityMonths,
    cumulativeFcff,
    cumulativeFcfe,
    cashOnCash: cumulativeFcfe / financing.equity,
    checks
  };
}

export function annualSummary(result) {
  return result.annual;
}

export function roundAmount(value) {
  return round2(value);
}

export function monthlyAt(result, index) {
  return result.months[index];
}
