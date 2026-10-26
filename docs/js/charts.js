/**
 * Gráficos SVG de Cafetería Aurora. Sin dependencias, sin DOM global.
 * Cada función devuelve una cadena SVG accesible con <title> y <desc>.
 */

const COLORS = {
  terracotta: '#C4623B',
  terracottaStrong: '#A94E2C',
  sage: '#7C8B6F',
  sageStrong: '#5E6B52',
  gold: '#C9A227',
  goldStrong: '#806410',
  espresso: '#2B1D16',
  muted: '#6F6259',
  line: '#E4D8C8',
  paper: '#FFFDF9',
  cream: '#F7F1E7',
  negative: '#A33A2B'
};

const nf0 = new Intl.NumberFormat('es-ES', { maximumFractionDigits: 0 });
const nf1 = new Intl.NumberFormat('es-ES', { maximumFractionDigits: 1 });

function esc(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function niceMax(value) {
  if (!Number.isFinite(value) || value <= 0) return 1;
  const exponent = Math.floor(Math.log10(value));
  const fraction = value / 10 ** exponent;
  const nice = fraction <= 1 ? 1 : fraction <= 2 ? 2 : fraction <= 5 ? 5 : 10;
  return nice * 10 ** exponent;
}

function niceMin(value) {
  if (!Number.isFinite(value) || value >= 0) return 0;
  const abs = Math.abs(value);
  const exponent = Math.floor(Math.log10(abs));
  const fraction = abs / 10 ** exponent;
  const nice = fraction <= 1 ? 1 : fraction <= 2 ? 2 : fraction <= 5 ? 5 : 10;
  return -(nice * 10 ** exponent);
}

function kEur(value) {
  if (Math.abs(value) >= 1000) return `${nf0.format(Math.round(value / 1000))} k€`;
  return `${nf0.format(Math.round(value))} €`;
}

function kEurTick(value) {
  return `${nf0.format(Math.round(value / 1000))} k€`;
}

function pct(value) {
  return `${nf1.format(value * 100)} %`;
}

function svgOpen(id, title, description, width = 720, height = 320) {
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="${id}-title ${id}-desc" preserveAspectRatio="xMidYMid meet">
    <title id="${id}-title">${esc(title)}</title>
    <desc id="${id}-desc">${esc(description)}</desc>`;
}

function legend(items) {
  const itemWidth = 110;
  const start = 8;
  return `<g transform="translate(${start}, 0)">
    ${items
      .map(
        (item, index) => `<g transform="translate(${index * itemWidth}, 0)">
          <rect x="0" y="-8" width="9" height="9" rx="2" fill="${item.color}"></rect>
          <text x="14" y="0" font-size="11" fill="${COLORS.muted}">${esc(item.name)}</text>
        </g>`
      )
      .join('')}
  </g>`;
}

function xTickIndices(length) {
  const wanted = [0, 5, 11, 17, 23, 29, 35];
  return wanted.filter((index) => index < length);
}

function lineChart({
  id,
  title,
  description,
  labels,
  series,
  minValue = 0,
  maxValue = null,
  band = null,
  highlightLast = true,
  height = 320
}) {
  const width = 720;
  const margin = { top: 22, right: 18, bottom: 54, left: 58 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;
  const values = series.flatMap((item) => item.values).filter((value) => Number.isFinite(value));
  const dataMin = Math.min(minValue, ...values);
  const dataMax = Math.max(...values, 1);
  const yMin = dataMin < 0 ? niceMin(dataMin) : minValue;
  const yMax = maxValue ?? niceMax(dataMax * 1.05);
  const x = (index) => margin.left + (labels.length <= 1 ? innerW / 2 : (index / (labels.length - 1)) * innerW);
  const y = (value) => margin.top + innerH - ((value - yMin) / (yMax - yMin)) * innerH;
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((fraction) => yMin + (yMax - yMin) * fraction);

  let content = '';
  if (band) {
    content += `<rect x="${margin.left}" y="${y(band.to)}" width="${innerW}" height="${Math.max(0, y(band.from) - y(band.to))}" fill="${band.color || COLORS.negative}" opacity="0.06"></rect>`;
    content += `<line x1="${margin.left}" x2="${margin.left + innerW}" y1="${y(band.from)}" y2="${y(band.from)}" stroke="${band.color || COLORS.negative}" stroke-width="1" stroke-dasharray="4 4" opacity="0.5"></line>`;
  }

  for (const tick of ticks) {
    content += `<line x1="${margin.left}" x2="${margin.left + innerW}" y1="${y(tick)}" y2="${y(tick)}" class="grid-line"></line>`;
    content += `<text x="${margin.left - 8}" y="${y(tick) + 4}" text-anchor="end">${kEurTick(tick)}</text>`;
  }
  const zeroY = y(0);
  content += `<line x1="${margin.left}" x2="${margin.left + innerW}" y1="${zeroY}" y2="${zeroY}" class="zero-line"></line>`;

  for (const index of xTickIndices(labels.length)) {
    content += `<text x="${x(index)}" y="${height - 30}" text-anchor="middle">${esc(labels[index])}</text>`;
  }

  for (const item of series) {
    const points = item.values.map((value, index) => `${x(index)},${y(value)}`);
    if (item.area) {
      content += `<path d="M ${x(0)},${y(0)} L ${points.join(' L ')} L ${x(labels.length - 1)},${y(0)} Z" fill="${item.color}" opacity="0.08"></path>`;
    }
    content += `<path d="M ${points.join(' L ')}" class="series-line" stroke="${item.color}" ${item.dashed ? 'stroke-dasharray="5 4"' : ''}></path>`;
    if (highlightLast) {
      const lastValue = item.values[item.values.length - 1];
      content += `<circle class="point" cx="${x(labels.length - 1)}" cy="${y(lastValue)}" r="4" fill="${item.color}"><title>${esc(item.name)}: ${kEur(lastValue)}</title></circle>`;
    }
    for (let index = 0; index < item.values.length; index += 1) {
      content += `<circle cx="${x(index)}" cy="${y(item.values[index])}" r="7" fill="transparent"><title>${esc(labels[index])} · ${esc(item.name)}: ${kEur(item.values[index])}</title></circle>`;
    }
  }

  content += `<g transform="translate(${margin.left}, ${height - 12})">${legend(series.map((item) => ({ name: item.name, color: item.color })))}</g>`;
  return `${svgOpen(id, title, description, width, height)}${content}</svg>`;
}

function comboChart({
  id,
  title,
  description,
  labels,
  bars,
  line,
  height = 320
}) {
  const width = 720;
  const margin = { top: 22, right: 64, bottom: 54, left: 58 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;
  const revenueMax = niceMax(Math.max(...bars.values) * 1.05);
  const lineMin = niceMin(Math.min(0, ...line.values));
  const lineMax = niceMax(Math.max(...line.values) * 1.1);
  const x = (index) => margin.left + (index / Math.max(1, labels.length - 1)) * innerW;
  const barWidth = Math.max(8, innerW / labels.length - 7);
  const yBar = (value) => margin.top + innerH - (value / revenueMax) * innerH;
  const yLine = (value) => margin.top + innerH - ((value - lineMin) / (lineMax - lineMin)) * innerH;

  let content = '';
  for (const fraction of [0, 0.25, 0.5, 0.75, 1]) {
    const value = revenueMax * fraction;
    content += `<line x1="${margin.left}" x2="${margin.left + innerW}" y1="${yBar(value)}" y2="${yBar(value)}" class="grid-line"></line>`;
    content += `<text x="${margin.left - 8}" y="${yBar(value) + 4}" text-anchor="end">${kEurTick(value)}</text>`;
  }

  bars.values.forEach((value, index) => {
    const barX = x(index) - barWidth / 2;
    content += `<rect x="${barX}" y="${yBar(value)}" width="${barWidth}" height="${Math.max(0, yBar(0) - yBar(value))}" rx="2" fill="${bars.color}"><title>${esc(labels[index])} · ${esc(bars.name)}: ${kEur(value)}</title></rect>`;
  });

  content += `<line x1="${margin.left}" x2="${margin.left + innerW}" y1="${yLine(0)}" y2="${yLine(0)}" stroke="${COLORS.line}" stroke-width="1"></line>`;
  for (const fraction of [0, 0.5, 1]) {
    const value = lineMin + (lineMax - lineMin) * fraction;
    content += `<text x="${width - 10}" y="${yLine(value) + 4}" text-anchor="end" fill="${line.color}">${kEurTick(value)}</text>`;
  }

  const points = line.values.map((value, index) => `${x(index)},${yLine(value)}`);
  content += `<path d="M ${points.join(' L ')}" class="series-line" stroke="${line.color}"></path>`;
  for (let index = 0; index < line.values.length; index += 1) {
    content += `<circle cx="${x(index)}" cy="${yLine(line.values[index])}" r="7" fill="transparent"><title>${esc(labels[index])} · ${esc(line.name)}: ${kEur(line.values[index])}</title></circle>`;
  }

  for (const index of xTickIndices(labels.length)) {
    content += `<text x="${x(index)}" y="${height - 30}" text-anchor="middle">${esc(labels[index])}</text>`;
  }

  content += `<g transform="translate(${margin.left}, ${height - 12})">${legend([
    { name: bars.name, color: bars.color },
    { name: line.name, color: line.color }
  ])}</g>`;
  return `${svgOpen(id, title, description, width, height)}${content}</svg>`;
}

function groupedBarChart({
  id,
  title,
  description,
  categories,
  series,
  height = 300
}) {
  const width = 720;
  const margin = { top: 22, right: 18, bottom: 54, left: 58 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;
  const max = niceMax(Math.max(...series.flatMap((item) => item.values)) * 1.08);
  const y = (value) => margin.top + innerH - (value / max) * innerH;
  const groupWidth = innerW / categories.length;
  const barWidth = Math.min(34, (groupWidth - 24) / series.length);

  let content = '';
  for (const fraction of [0, 0.25, 0.5, 0.75, 1]) {
    const value = max * fraction;
    content += `<line x1="${margin.left}" x2="${margin.left + innerW}" y1="${y(value)}" y2="${y(value)}" class="grid-line"></line>`;
    content += `<text x="${margin.left - 8}" y="${y(value) + 4}" text-anchor="end">${kEurTick(value)}</text>`;
  }

  categories.forEach((category, categoryIndex) => {
    const center = margin.left + groupWidth * categoryIndex + groupWidth / 2;
    content += `<text x="${center}" y="${height - 30}" text-anchor="middle">${esc(category)}</text>`;
    series.forEach((item, seriesIndex) => {
      const value = item.values[categoryIndex];
      const barX = center - (series.length * barWidth) / 2 + seriesIndex * barWidth;
      content += `<rect x="${barX}" y="${y(value)}" width="${barWidth - 2}" height="${Math.max(0, y(0) - y(value))}" rx="2" fill="${item.color}"><title>${esc(category)} · ${esc(item.name)}: ${kEur(value)}</title></rect>`;
    });
  });

  content += `<g transform="translate(${margin.left}, ${height - 12})">${legend(series)}</g>`;
  return `${svgOpen(id, title, description, width, height)}${content}</svg>`;
}

function horizontalBarChart({
  id,
  title,
  description,
  items,
  valueLabel = 'Margen unitario',
  height = 320
}) {
  const width = 720;
  const margin = { top: 18, right: 72, bottom: 24, left: 150 };
  const innerW = width - margin.left - margin.right;
  const rowHeight = (height - margin.top - margin.bottom) / items.length;
  const max = niceMax(Math.max(...items.map((item) => item.value)));
  const barHeight = Math.min(18, rowHeight * 0.55);

  let content = '';
  items.forEach((item, index) => {
    const y = margin.top + index * rowHeight + rowHeight / 2;
    const barWidth = (item.value / max) * innerW;
    content += `<text x="${margin.left - 12}" y="${y + 4}" text-anchor="end" font-size="11" fill="${COLORS.espresso}">${esc(item.label)}</text>`;
    content += `<rect x="${margin.left}" y="${y - barHeight / 2}" width="${innerW}" height="${barHeight}" rx="4" fill="${COLORS.cream}"></rect>`;
    content += `<rect x="${margin.left}" y="${y - barHeight / 2}" width="${Math.max(2, barWidth)}" height="${barHeight}" rx="4" fill="${item.color || COLORS.terracotta}"><title>${esc(item.label)} · ${esc(valueLabel)}: ${kEur(item.value)}</title></rect>`;
    content += `<text x="${margin.left + barWidth + 8}" y="${y + 4}" font-size="10" fill="${COLORS.muted}">${kEur(item.value)}</text>`;
  });
  return `${svgOpen(id, title, description, width, height)}${content}</svg>`;
}

function donutChart({
  id,
  title,
  description,
  items,
  centerLabel = 'Costes',
  height = 320
}) {
  const width = 720;
  const cx = 180;
  const cy = 165;
  const radius = 105;
  const innerRadius = 62;
  const total = items.reduce((sum, item) => sum + item.value, 0);
  const colors = [COLORS.terracotta, COLORS.sageStrong, COLORS.espresso, COLORS.goldStrong, COLORS.muted];
  let angle = -Math.PI / 2;
  let content = '';

  items.forEach((item, index) => {
    const slice = (item.value / total) * Math.PI * 2;
    const end = angle + slice;
    const large = slice > Math.PI ? 1 : 0;
    const x1 = cx + radius * Math.cos(angle);
    const y1 = cy + radius * Math.sin(angle);
    const x2 = cx + radius * Math.cos(end);
    const y2 = cy + radius * Math.sin(end);
    const ix1 = cx + innerRadius * Math.cos(angle);
    const iy1 = cy + innerRadius * Math.sin(angle);
    const ix2 = cx + innerRadius * Math.cos(end);
    const iy2 = cy + innerRadius * Math.sin(end);
    content += `<path d="M ${x1} ${y1} A ${radius} ${radius} 0 ${large} 1 ${x2} ${y2} L ${ix2} ${iy2} A ${innerRadius} ${innerRadius} 0 ${large} 0 ${ix1} ${iy1} Z" fill="${colors[index % colors.length]}"><title>${esc(item.label)}: ${kEur(item.value)} (${pct(item.value / total)})</title></path>`;
    angle = end;
  });

  content += `<text x="${cx}" y="${cy - 6}" text-anchor="middle" font-size="11" fill="${COLORS.muted}">${esc(centerLabel)}</text>`;
  content += `<text x="${cx}" y="${cy + 16}" text-anchor="middle" font-size="20" font-weight="600" fill="${COLORS.espresso}">${kEur(total)}</text>`;

  items.forEach((item, index) => {
    const y = 58 + index * 38;
    content += `<rect x="330" y="${y - 11}" width="12" height="12" rx="2" fill="${colors[index % colors.length]}"></rect>`;
    content += `<text x="350" y="${y}" font-size="12" fill="${COLORS.espresso}">${esc(item.label)}</text>`;
    content += `<text x="520" y="${y}" font-size="12" fill="${COLORS.muted}">${pct(item.value / total)}</text>`;
    content += `<text x="610" y="${y}" font-size="12" text-anchor="end" fill="${COLORS.muted}">${kEur(item.value)}</text>`;
  });

  return `${svgOpen(id, title, description, width, height)}${content}</svg>`;
}

function bulletChart({
  id,
  title,
  description,
  max = 420,
  value,
  markers,
  height = 190
}) {
  const width = 720;
  const margin = { top: 34, right: 28, bottom: 40, left: 28 };
  const innerW = width - margin.left - margin.right;
  const x = (amount) => margin.left + (Math.min(max, Math.max(0, amount)) / max) * innerW;
  const y = 82;
  const barHeight = 26;

  let content = '';
  content += `<rect x="${margin.left}" y="${y - barHeight / 2}" width="${innerW}" height="${barHeight}" rx="5" fill="${COLORS.cream}"></rect>`;
  content += `<rect x="${margin.left}" y="${y - barHeight / 2}" width="${x(value)}" height="${barHeight}" rx="5" fill="${COLORS.terracotta}"></rect>`;
  for (let tick = 0; tick <= max; tick += 100) {
    content += `<line x1="${x(tick)}" x2="${x(tick)}" y1="${y + 18}" y2="${y + 24}" stroke="${COLORS.line}"></line>`;
    content += `<text x="${x(tick)}" y="${y + 40}" text-anchor="middle" font-size="10">${tick}</text>`;
  }
  markers.forEach((marker, index) => {
    const color = index === 0 ? COLORS.espresso : index === 1 ? COLORS.goldStrong : COLORS.sageStrong;
    content += `<line x1="${x(marker.value)}" x2="${x(marker.value)}" y1="${y - 26}" y2="${y + 16}" stroke="${color}" stroke-width="2"></line>`;
    content += `<text x="${x(marker.value)}" y="${y - 32}" text-anchor="middle" font-size="10" fill="${color}">${esc(marker.label)} ${nf0.format(Math.round(marker.value))}</text>`;
    content += `<circle cx="${x(marker.value)}" cy="${y}" r="3.5" fill="${color}"></circle>`;
  });
  content += `<text x="${margin.left}" y="${y + 56}" font-size="10" fill="${COLORS.muted}">0</text>`;
  content += `<text x="${margin.left + innerW}" y="${y + 56}" text-anchor="end" font-size="10" fill="${COLORS.muted}">${max} tickets/día</text>`;
  return `${svgOpen(id, title, description, width, height)}${content}</svg>`;
}

export {
  COLORS,
  kEur,
  kEurTick,
  pct,
  lineChart,
  comboChart,
  groupedBarChart,
  horizontalBarChart,
  donutChart,
  bulletChart
};
