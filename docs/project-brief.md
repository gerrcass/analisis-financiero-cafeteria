# Cafetería Aurora — Brief del proyecto y libro de supuestos

> **Estado**: congelado para implementación.  
> **Versión**: 1.0 — 25 de octubre de 2026.  
> **Alcance**: definición completa del modelo financiero, el libro Excel, el sitio público y la guía de aprendizaje.  
> **Fuente ejecutable**: `data/model.json` (se crea en la fase de implementación). Este documento es el contrato de supuestos, fórmulas y objetivos dorados.

---

## 1. Resumen ejecutivo

**Cafetería Aurora** es un café de especialidad de barrio en el centro de Zaragoza, con panadería artesanal y venta de café en grano. El modelo proyecta **36 meses (enero 2026 – diciembre 2028)**, en **EUR**, con granularidad mensual y resúmenes anuales, en tres escenarios: **Pesimista**, **Base** y **Optimista**.

La inversión inicial es de **160.000 €**: **132.000 € de capex**, **6.500 € de stock inicial** y **21.500 € de caja de apertura**. Se financia con **90.000 € de equity** y **70.000 € de préstamo** a 7,5% y 5 años.

La tesis del caso Base:

- El local alcanza **384.419 € de ingresos netos** en 2026, con **342 tickets/día** de media (360 en régimen, ajustados por rampa y estacionalidad).
- El **margen bruto** es del **65,5%**; el **EBITDA** de 2026 es **61.658 € (16,0%)** y crece hasta **79.505 € (17,3%)** en 2028.
- El **beneficio neto** pasa de **30.142 €** a **44.978 €**; la **caja final** pasa de **57.456 €** a **132.063 €**.
- El **payback** es de **34 meses** sobre el proyecto y **30 meses** sobre el equity.
- El **Pesimista** no recupera la inversión en 36 meses y termina 2028 con **134 € de beneficio neto** y un **DSCR de 1,17**: el negocio sobrevive, pero no remunera el riesgo. Es el test que decide si la inversión es resistente.
- El **Optimista** recupera el equity en **22 meses** y termina con **200.325 € de caja**.

**Entregables**: un `.xlsx` con 10 hojas y fórmulas vivas, un sitio estático en GitHub Pages con dashboard, laboratorio y guía, una guía de aprendizaje en español, y un README con captura y enlace.

**Regla de oro**: los únicos valores escritos a mano son los supuestos de `Supuestos`, `Productos`, `Personal` y `Costos` (y metadatos de `Portada`). Todo lo demás —ingresos, COGS, EBITDA, impuestos, caja, gráficos— es una fórmula que se recalcula.

---

## 2. Entrevista de diseño (auto-grill)

El encargo delegó todas las decisiones. Para no dejar huecos, se recorrió el árbol de diseño en cinco rondas. Cada pregunta se respondió con la opción recomendada y su razón; no queda ninguna pregunta abierta.

### Ronda 1 — Concepto y alcance

| # | Pregunta | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|---|
| 1 | ¿Qué negocio y dónde? | Café de especialidad en Zaragoza Centro, 92 m², 312 días/año, 360 tickets/día en régimen | Alquiler y salarios permiten un caso viable; la ciudad tiene demanda de especialidad y no exige precios de Madrid/Barcelona | Madrid prime (alquiler inviable), bakery-only (margen y ticket distintos) |
| 2 | ¿Horizonte y granularidad? | 36 meses mensuales, resumen anual | Captura estacionalidad, rampa, escalón de personal y deuda; el anual esconde los valles de caja | 5 años anual, 12 meses mensual, semanal |
| 3 | ¿Moneda e impuestos? | EUR; P&L neto de IVA; IVA 10%; sociedades 25% | El IVA no es ingreso; mezclar PVP y neto es el error más común | Ingresos con IVA, tipo reducido de microempresa |
| 4 | ¿Qué queda fuera? | Balance completo, liquidación de IVA, detalle de nóminas, multi-local, valoración, dividendos | El modelo debe ser didáctico y auditable, no un sistema contable | Modelo 3 estados completo, consolidación multitienda |
| 5 | ¿Qué produce? | `.xlsx` + sitio + guía + README | El encargo pide los cuatro; el modelo es el producto, no un anexo | Solo Excel, solo web |

### Ronda 2 — Motor de ingresos

| # | Pregunta | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|---|
| 6 | ¿Cuántos productos? | 8: 4 cafés calientes, 1 frío, 2 food, 1 retail | Cubre el surtido real y permite explicar mix y margen; 8 no satura la carta | 5 productos (pierde retail), 15 (inmanejable) |
| 7 | ¿Cómo se modela la demanda? | Tickets/día × ítems/ticket × estacionalidad × rampa | Es intuitivo, se puede contrastar con conteos y separa tráfico de surtido | Crecimiento de ingresos top-down |
| 8 | ¿Estacionalidad? | 12 factores que suman 12; agosto 0,72, diciembre 1,16 | Un café en Zaragoza pierde agosto y gana diciembre; el valle de caja es real | Demanda plana |
| 9 | ¿Rampa? | 75% → 100% en 6 meses | Un local nuevo no arranca a plena demanda; evita sobrestimar 2026 | 100% desde el mes 1 |
| 10 | ¿Precio? | PVP con IVA; precio neto = PVP/1,10; subida anual por escenario | La carta se piensa con IVA; el P&L necesita neto | Precio neto directo |
| 11 | ¿Mix fijo? | Sí, 22/20/10/13/8/14/9/4 durante 3 años | Sin datos de elasticidad, cambiarlo sería inventar; se prueba en el laboratorio | Mix que evoluciona por año |

### Ronda 3 — Costes, inversión y financiación

| # | Pregunta | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|---|
| 12 | ¿COGS? | Coste unitario / (1 − merma) × inflación anual | La merma es real y se aplica al coste, no al precio | COGS como % de ingresos |
| 13 | ¿Personal? | 4 roles, 3,5/4,0/4,0 FTE, 31,5% SS, 3% crecimiento, factor por escenario | Es el coste mayor y el escalón de 2027 explica por qué el margen no mejora ese año | Personal como % de ingresos |
| 14 | ¿Costes fijos? | Alquiler 1.900 €/mes; suministros 1.450; servicios 780; marketing 450 + 3%; otros 1.100 | Desglose auditable; cada línea tiene una palanca distinta | Un único bloque de opex |
| 15 | ¿Capex? | 132.000 € en 6 clases, vidas 4–10 años, mantenimiento 1,5% de ingresos | Refleja un local de 92 m² con cocina y maquinaria de café | 80.000 € (infravalora), 200.000 € (sobredimensiona) |
| 16 | ¿Financiación? | 90.000 equity + 70.000 deuda al 7,5% a 5 años; 21.500 caja; 6.500 stock | 56/44; DSCR >1,6 en Base; colchón de caja | Todo equity, 50% deuda, leasing |
| 17 | ¿Fiscalidad? | 25%; pérdidas compensables sin límite; provisión mensual = cuota anual/12 | Pyme; evita artefactos de tesorería mensual | Tipo reducido, impuesto mensual sin true-up |
| 18 | ¿Capital circulante? | 18 días de inventario, 30 de proveedor, 0 de cobro; ΔWC mensual | Los proveedores financian parte del stock; explica la caja | 10% de ingresos |

### Ronda 4 — Escenarios y salidas

| # | Pregunta | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|---|
| 19 | ¿Matriz de escenarios? | 10 variables: demanda (factor y crecimiento), precio, coste, personal, alquiler, servicios, marketing, otros (factor y crecimiento) | Compacta, completa y auditable; todo lo demás es estructural | Tres modelos independientes |
| 20 | ¿Orden? | Pesimista < Base < Optimista en demanda/precio; al revés en costes; marketing baja en Pesimista | Coherencia económica; marketing es respuesta de gestión, no coste externo | Escenarios sin orden |
| 21 | ¿P&L y caja? | EBITDA, EBIT, EBT, neto; FCFF, FCFE, escudo fiscal, payback proyecto y equity | Permite enseñar beneficio vs caja y hablar con un banco | Solo EBITDA |
| 22 | ¿Break-even? | Dos: EBITDA cero y beneficio antes de impuestos cero | Son dos decisiones distintas: operar y cubrir la inversión | Un único break-even |
| 23 | ¿Resumen? | Tabla de 9 KPIs, comparativa, 5 gráficos, selector de escenario | El Resumen debe responder sin abrir las hojas de escenario | Gráficos estáticos |
| 24 | ¿Objetivos dorados? | Tabla de outputs por escenario y año; tolerancia ±1 € / ±0,1 pp | Permite verificar libro y sitio contra el mismo contrato | “A ojo” |

### Ronda 5 — Sitio, guía y calidad

| # | Pregunta | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|---|
| 25 | ¿Arquitectura del sitio? | Dos páginas: dashboard + guía; vanilla JS; SVG; JSON estático | Sin backend, rápido, gratis en Pages, fácil de testear | React/Vite, API serverless |
| 26 | ¿Laboratorio? | 10 controles, presets, reset, delta vs escenario, URL compartible | Convierte el modelo en una herramienta, no en una lámina | Sitio de solo lectura |
| 27 | ¿Guía? | 10 capítulos, ejemplos con cifras reales, 36 ejercicios con respuesta, glosario y checklist | El encargo pide aprender, no solo ver | PDF o texto genérico |
| 28 | ¿Diseño? | Papel crema, espresso, terracota, salvia; serif editorial + sans; movimiento calmado | Coherente con café de especialidad, sin caer en cliché | Dashboard bancario azul/gris |
| 29 | ¿Tests? | Python (modelo, libro, fórmulas), Node (modelo JS), Playwright (sitio), CI | La integridad de fórmulas es el riesgo principal | QA manual |
| 30 | ¿Criterio de éxito? | Reproducible, sin valores pegados, cifras iguales en libro/sitio, Pesimista visible, guía útil | Alinea implementación y producto | “Que se vea bonito” |

**Decisiones cerradas**: no hay preguntas pendientes. Cualquier cambio posterior a la matriz de escenarios, al capex, al préstamo o al plan de personal exige regenerar los objetivos dorados y actualizar este documento.

---

## 3. Concepto y contexto

### 3.1 La marca

- **Nombre**: Cafetería Aurora.
- **Categoría**: café de especialidad con panadería artesanal y retail de grano.
- **Ubicación**: Zaragoza, distrito Centro, calle peatonal con oficinas y una facultad a menos de 400 m. Local de **92 m²** con escaparate y **12 m²** de terraza (3 mesas, 6 plazas).
- **Horario**: lunes a viernes 07:30–19:00; sábado 09:00–20:00; domingo cerrado. **312 días operativos** normalizados al año.
- **Cliente objetivo**: profesionales de 25–45 años, estudiantes y aficionados al café; alto componente de take-away (55%) y consumo en local (45%).
- **Posicionamiento**: especialidad accesible, no lujo. Café de origen rotativo, panadería del día, brunch ligero y grano para llevar. Precio medio: **3,96 € con IVA** por ticket.
- **Diferenciadores**: dos orígenes en espresso, método filtrado, panadería propia, venta de grano, fidelización simple (tarjeta de 10 cafés), eventos de cata mensuales.
- **Tono de marca**: cálido, preciso, cercano; "Aurora" como luz de amanecer, no como lujo.

### 3.2 La economía en una frase

Un local de 92 m² que vende **~342 tickets/día** a **3,60 € netos**, con **65,5% de margen bruto**, **28,7% de personal** y **5,9% de alquiler**, genera **61.658 € de EBITDA** en 2026 y **79.505 € en 2028**, después de absorber **132.000 € de capex** y **70.000 € de deuda**.

### 3.3 Qué es y qué no es este modelo

**Es**:

- Un modelo de decisión para abrir un local, negociar alquiler, dimensionar personal y hablar con un banco.
- Un modelo mensual, con estacionalidad, rampa, deuda e impuestos.
- Un contrato reproducible: el mismo JSON alimenta Excel, sitio y tests.

**No es**:

- Un balance contable completo ni una liquidación de IVA.
- Una previsión de demanda de un local concreto; los supuestos son ilustrativos.
- Un modelo de valoración (DCF, múltiplos) ni de reparto de dividendos.
- Un sistema de nóminas, fiscalidad o contabilidad.

---

## 4. Arquitectura del modelo

### 4.1 Periodo y dimensiones

| Dimensión | Valor |
|---|---|
| Inicio | 1 de enero de 2026 |
| Fin | 31 de diciembre de 2028 |
| Periodos | 36 mensuales |
| Años | 2026, 2027, 2028 |
| Escenarios | Pesimista, Base, Optimista |
| Moneda | EUR |
| Impuestos | P&L neto de IVA; sociedades 25% |
| Redondeo | 2 decimales internos; presentación a euro y 1 decimal % |

### 4.2 Flujo de datos

```
data/model.json  ──►  scripts/model.py  ──►  data/expected.json
       │                    │
       │                    └──►  scripts/build_workbook.py  ──►  .xlsx
       │
       └──►  site/js/model.js  ──►  sitio (dashboard, lab, guía)
```

- `data/model.json` es la única fuente de entradas.
- `scripts/model.py` implementa las fórmulas y genera `data/expected.json`.
- `scripts/build_workbook.py` escribe el `.xlsx` con fórmulas vivas.
- `site/js/model.js` replica las fórmulas para el navegador.
- Los tests comparan Python y JS contra `expected.json`.

### 4.3 Hojas del libro

| Orden | Hoja | Rol | ¿Entradas? |
|---|---|---|---|
| 1 | Portada | Identidad, instrucciones, leyenda, versión | Metadatos |
| 2 | Resumen | KPIs, comparativa, 5 gráficos, selector | No (solo selector) |
| 3 | Supuestos | Demanda, estacionalidad, matriz de escenarios, financiación, fiscalidad | Sí |
| 4 | Productos | Catálogo, PVP, IVA, coste, mix, merma | Sí |
| 5 | Personal | Roles, FTE, salarios, coste empresa | Sí |
| 6 | Costos | Costes fijos, capex, mantenimiento | Sí |
| 7 | Pesimista | Modelo mensual del escenario de estrés | Solo selector |
| 8 | Base | Modelo mensual del plan | Solo selector |
| 9 | Optimista | Modelo mensual del caso de expansión | Solo selector |
| 10 | Aprende | Guía resumida, ejemplos vivos y ejercicios | No |

### 4.4 Convenciones del libro

- **Columnas**: A concepto; B t0/nota; C–N 2026; O–Z 2027; AA–AL 2028; AM–AO totales anuales; AP total trienio.
- **Colores**: entrada `#FFF4D6` con fuente `#1F4E79`; cálculo blanco; check verde/rojo; cabecera espresso con texto cream; sección terracota.
- **Fórmulas**: nombres de función en inglés y separador coma (Excel los localiza al abrir); sin `XLOOKUP`, `IFS` ni funciones de matriz dinámica; usar `INDEX/MATCH`, `SUMPRODUCT`, `PMT`, `CHOOSE`, `IF`, `MAX`, `MIN`.
- **Recalculación**: `wb.calculation.fullCalcOnLoad = True` y `forceFullCalc = True`; tras generar, recalcular con LibreOffice headless si está disponible para dejar valores cacheados.
- **Sin valores pegados**: las celdas calculadas de escenarios y Resumen solo contienen fórmulas. Las etiquetas, fechas y el selector son las únicas constantes.

---

## 5. Libro de supuestos

> Convención: importes en EUR; porcentajes en tanto por uno en el JSON y en porcentaje en la documentación; los índices de precio/coste/servicios valen 1,000 en 2026 y se aplican desde enero de cada año.

### 5.1 Identidad y calendario

| Supuesto | Valor | Unidad | Nota |
|---|---:|---|---|
| Inicio | 01/01/2026 | fecha | Mes 1 |
| Meses | 36 | meses | 2026–2028 |
| Días operativos/año | 312 | días | Suma de la fila mensual |
| Año 1 | 2026 | año | Rampa de 6 meses |
| Año 2 | 2027 | año | Personal +0,5 FTE |
| Año 3 | 2028 | año | Último año del modelo |
| IVA | 10% | % | Hostelería y alimentación |
| Tipo de sociedades | 25% | % | Tipo general |
| Moneda | EUR | — | Sin inflación de moneda |

**Días operativos por mes** (suma 312):

| Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 27 | 24 | 27 | 26 | 27 | 26 | 27 | 24 | 26 | 27 | 25 | 26 |

### 5.2 Demanda y estacionalidad

| Supuesto | Valor | Unidad | Nota |
|---|---:|---|---|
| Tickets/día en régimen | 360 | tickets/día | A partir del mes 7 de 2026 |
| Ítems por ticket | 1,35 | ítems | 1 café + 0,35 food/retail |
| Rampa meses 1–6 | 75%, 82%, 88%, 93%, 97%, 100% | % | Solo año 1 |
| Tickets/día medio 2026 | 342,0 | tickets/día | Efecto de rampa, estacionalidad y días |
| Crecimiento de demanda | Según escenario | % anual | Ver matriz 5.9 |
| Crecimiento de precios | Según escenario | % anual | Se aplica en enero |

**Estacionalidad mensual** (suma 12,00):

| Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,92 | 0,93 | 1,02 | 1,04 | 1,08 | 1,06 | 0,88 | 0,72 | 1,06 | 1,09 | 1,04 | 1,16 |

**Rampa mensual año 1**:

| Mes | 1 | 2 | 3 | 4 | 5 | 6 | 7–12 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Factor | 0,75 | 0,82 | 0,88 | 0,93 | 0,97 | 1,00 | 1,00 |

**Lectura**: 360 × 0,946 (rampa media) ≈ 340; el ajuste por días y estacionalidad lleva la media de 2026 a 342. El mes 1 vende 248 tickets/día; diciembre, 418.

### 5.3 Productos

| # | Producto | Categoría | PVP con IVA | IVA | Precio neto | Coste unitario | Mix | Merma | Coste ajustado | Margen unitario | Margen % |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Espresso | Café | 1,70 € | 10% | 1,5455 € | 0,42 € | 22% | 4% | 0,4375 € | 1,1080 € | 71,7% |
| 2 | Flat white | Café con leche | 2,80 € | 10% | 2,5455 € | 0,72 € | 20% | 4% | 0,7500 € | 1,7955 € | 70,5% |
| 3 | Cappuccino | Café con leche | 2,60 € | 10% | 2,3636 € | 0,66 € | 10% | 4% | 0,6875 € | 1,6761 € | 70,9% |
| 4 | Latte | Café con leche | 2,90 € | 10% | 2,6364 € | 0,74 € | 13% | 4% | 0,7708 € | 1,8655 € | 70,8% |
| 5 | Cold brew | Café frío | 3,40 € | 10% | 3,0909 € | 0,95 € | 8% | 5% | 1,0000 € | 2,0909 € | 67,6% |
| 6 | Croissant | Panadería | 2,30 € | 10% | 2,0909 € | 0,82 € | 14% | 8% | 0,8913 € | 1,1996 € | 57,4% |
| 7 | Tostada | Salado | 3,90 € | 10% | 3,5455 € | 1,18 € | 9% | 6% | 1,2553 € | 2,2901 € | 64,6% |
| 8 | Bolsa café 250 g | Retail | 10,50 € | 10% | 9,5455 € | 4,60 € | 4% | 2% | 4,6939 € | 4,8520 € | 50,8% |
| | **Total / ponderado** | | **2,9360 €** | | **2,6691 €** | **0,8796 €** | **100%** | **4,7%** | **0,9207 €** | **1,7484 €** | **65,5%** |

**Fórmulas del catálogo**:

```
Precio neto_i = PVP_i / (1 + IVA_i)
Coste ajustado_i = Coste_i / (1 − Merma_i)
Margen unitario_i = Precio neto_i − Coste ajustado_i
Margen %_i = Margen unitario_i / Precio neto_i
Precio neto ponderado = SUMPRODUCT(Mix, Precio neto)
Coste ajustado ponderado = SUMPRODUCT(Mix, Coste ajustado)
```

**Chequeos**: mix = 100,0%; todos los PVP > coste ajustado; el margen bruto ponderado es 65,5%.

**Nota sobre el IVA**: todos los productos son hostelería/alimentación al 10%. La columna de IVA existe para que el catálogo sea extensible (por ejemplo, una cerveza al 21%); no se modela la liquidación de IVA.

### 5.4 Personal

| Rol | Salario bruto anual | FTE 2026 | FTE 2027 | FTE 2028 | Coste empresa 2026 | Coste empresa 2027 | Coste empresa 2028 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gerente | 30.000 € | 1,0 | 1,0 | 1,0 | 39.450 € | 40.634 € | 41.853 € |
| Barista | 23.000 € | 1,0 | 1,5 | 1,5 | 30.245 € | 46.729 € | 48.130 € |
| Ayudante de cocina | 21.000 € | 1,0 | 1,0 | 1,0 | 27.615 € | 28.443 € | 29.297 € |
| Fin de semana | 20.000 € | 0,5 | 0,5 | 0,5 | 13.150 € | 13.545 € | 13.951 € |
| **Total** | **84.000 €** | **3,5** | **4,0** | **4,0** | **110.460 €** | **129.350 €** | **133.230 €** |

| Supuesto | Valor | Unidad |
|---|---:|---|
| Cotización empresarial | 31,5% | % del bruto |
| Crecimiento salarial | 3,0% | % anual |
| Factor de personal | Según escenario | × |
| Coste empresa 2026 | 110.460 € | € |
| Personal / ingresos 2026 | 28,7% | % |
| Ingresos por FTE 2026 | 109.834 € | €/FTE |
| Coste medio por FTE 2026 | 31.560 € | €/FTE |

**Fórmulas**:

```
Coste empresa anual(y) = Σ(FTE_rol(y) × Salario_rol) × (1 + SS) × (1 + crecimiento)^(y−1)
Coste mensual(t) = Coste empresa anual(y) × Factor_personal / 12
```

**Decisión de plantilla**: el barista pasa de 1,0 a 1,5 FTE en 2027 por el aumento de tráfico; el fin de semana se mantiene en 0,5 FTE. No se modelan horas extras, bonificaciones ni bajas.

### 5.5 Costes fijos

| Concepto | €/mes año 1 | €/año año 1 | Indexación | Nota |
|---|---:|---:|---|---|
| Alquiler | 1.900 € | 22.800 € | +2,0%/año × factor de alquiler | 92 m² a 20,65 €/m²/mes |
| Suministros | 1.450 € | 17.400 € | Inflación de servicios del escenario | Luz, gas, agua, residuos |
| Servicios fijos | 780 € | 9.360 € | Inflación de servicios del escenario | Internet, TPV, software, seguro, gestoría, alarma |
| Marketing fijo | 450 € | 5.400 € | +2,5%/año | Contenido, fotografía, impresos |
| Otros gastos | 1.100 € | 13.200 € | Crecimiento de otros gastos × factor | Limpieza, mantenimiento, formación, banca, comisiones |
| **Total** | **5.680 €** | **68.160 €** | | Sin marketing variable |

**Marketing variable**: `% de marketing del escenario × ingresos netos`. En Base, 3,0% (11.533 € en 2026).

**Fórmulas**:

```
Alquiler(t) = Alquiler_mes × Factor_alquiler × (1 + 2,0%)^(año−1)
Suministros(t) = Suministros_mes × (1 + inflación_servicios)^(año−1)
Servicios_fijos(t) = Servicios_mes × (1 + inflación_servicios)^(año−1)
Marketing_fijo(t) = Marketing_mes × (1 + 2,5%)^(año−1)
Marketing_variable(t) = %_marketing × Ingresos(t)
Otros(t) = Otros_mes × Factor_otros × (1 + crecimiento_otros)^(año−1)
```

### 5.6 Capex

| Activo | Importe | Vida útil | Amortización anual | Amortización mensual |
|---|---:|---:|---:|---:|
| Obra y adecuación | 65.000 € | 10 años | 6.500 € | 541,67 € |
| Maquinaria de café | 28.000 € | 7 años | 4.000 € | 333,33 € |
| Mobiliario y menaje | 15.000 € | 8 años | 1.875 € | 156,25 € |
| Equipo de cocina y frío | 12.000 € | 8 años | 1.500 € | 125,00 € |
| Tecnología y TPV | 7.000 € | 4 años | 1.750 € | 145,83 € |
| Licencias y apertura | 5.000 € | 5 años | 1.000 € | 83,33 € |
| **Total** | **132.000 €** | | **16.625 €** | **1.385,42 €** |

| Supuesto | Valor | Unidad |
|---|---:|---|
| Capex inicial | 132.000 € | € |
| Capex de mantenimiento | 1,5% de ingresos netos | % |
| Amortización | Lineal, desde el mes 1 | — |
| Valor residual | 0 | € |
| Amortización del capex de mantenimiento | No se añade (simplificación) | — |

**Fórmulas**:

```
Amortización anual_i = Importe_i / Vida_i
Amortización mensual = Σ(Amortización anual_i) / 12
Capex mantenimiento(t) = 1,5% × Ingresos(t)
```

**Simplificación documentada**: el capex de mantenimiento es una salida de caja de inversión y no genera una capa adicional de amortización. En un modelo de 36 meses el efecto en impuestos es inmaterial; se documenta para que nadie lo “arregle” sin querer.

### 5.7 Financiación y caja inicial

| Concepto | Valor | Nota |
|---|---:|---|
| Equity | 90.000 € | 56,25% de la financiación |
| Préstamo | 70.000 € | 43,75% |
| Tipo nominal anual | 7,5% | Fijo |
| Plazo | 60 meses | 5 años |
| Cuota mensual | 1.402,66 € | PMT(7,5%/12, 60, −70.000) |
| Intereses totales | 14.159 € | Suma de 60 cuotas − principal |
| Caja de apertura | 21.500 € | Colchón inicial |
| Stock inicial | 6.500 € | 18 días de COGS de 2026 |
| Caja mínima de política | 10.000 € | Alerta, no revolver |
| Dividendos | 0 € | Todo se reinvierte |

**Cuadre de fuentes y usos**:

| Usos | Importe | Fuentes | Importe |
|---|---:|---|---:|
| Capex inicial | 132.000 € | Equity | 90.000 € |
| Stock inicial | 6.500 € | Préstamo | 70.000 € |
| Caja de apertura | 21.500 € | | |
| **Total** | **160.000 €** | **Total** | **160.000 €** |

**Calendario de deuda (francés)**:

| Año | Saldo inicial | Intereses | Principal | Saldo final |
|---|---:|---:|---:|---:|
| 2026 | 70.000 € | 4.843 € | 11.988 € | 58.012 € |
| 2027 | 58.012 € | 3.913 € | 12.919 € | 45.092 € |
| 2028 | 45.092 € | 2.910 € | 13.922 € | 31.170 € |

**Fórmulas**:

```
Cuota = PMT(Tipo/12, Plazo_meses, −Préstamo)
Interés(t) = Saldo_inicial(t) × Tipo/12
Principal(t) = MIN(Cuota − Interés(t), Saldo_inicial(t))
Saldo_final(t) = Saldo_inicial(t) − Principal(t)
Saldo_inicial(t+1) = Saldo_final(t)
```

**Caja inicial**: la caja de apertura es un uso financiado con equity y deuda; no es un ingreso. El stock inicial se paga al contado y se libera cuando los proveedores empiezan a financiar (mes 1).

### 5.8 Fiscalidad y capital circulante

| Supuesto | Valor | Unidad | Nota |
|---|---:|---|---|
| Tipo de sociedades | 25% | % | Sobre base imponible positiva |
| Pérdidas compensables | Sin límite (ingresos < 1 M€) | — | Pyme; se arrastran indefinidamente |
| Provision mensual | Cuota anual / 12 | € | Simplificación de tesorería |
| Días de inventario | 18 | días | Sobre COGS |
| Días de proveedor | 30 | días | Sobre COGS |
| Días de cobro | 0 | días | Cobro en el acto |
| Capital circulante inicial | 6.500 € | € | Stock inicial, sin proveedores |
| Caja mínima | 10.000 € | € | Alerta de liquidez |

**Fórmulas**:

```
Base imponible(y) = MAX(0, EBT(y) − Pérdidas_inicio(y))
Cuota(y) = 25% × Base imponible(y)
Pérdidas_fin(y) = Pérdidas_inicio(y) − MIN(Pérdidas_inicio(y), MAX(0, EBT(y)))
                  + MAX(0, −EBT(y))
Pérdidas_inicio(y+1) = Pérdidas_fin(y)
Capital circulante(t) = COGS(t) × (18 − 30) / 365
ΔCapital circulante(t) = Capital circulante(t) − Capital circulante(t−1)
Capital circulante(0) = 6.500 €
```

**Impuesto sin deuda**: se calcula igual sobre EBIT, con su propia bolsa de pérdidas. Se usa para el FCFF y para el escudo fiscal. El impuesto con deuda se usa en el P&L y en el FCFE.

**Nota**: se aplica compensación íntegra porque los ingresos son inferiores a 1 M€ (régimen de pyme). En los tres escenarios congelados no se activan pérdidas plurianuales (el EBT anual es positivo). El mecanismo se implementa y se prueba con un caso sintético de pérdidas en los tests.

### 5.9 Matriz de escenarios

| # | Variable | Unidad | Pesimista | Base | Optimista | Orden |
|---:|---|---|---:|---:|---:|---|
| 1 | Factor de demanda año 1 | × | 0,88 | 1,00 | 1,08 | Pes < Base < Opt |
| 2 | Crecimiento anual de demanda | % | 1,5% | 4,0% | 6,0% | Pes < Base < Opt |
| 3 | Crecimiento anual de precios | % | 1,5% | 2,5% | 3,2% | Pes < Base < Opt |
| 4 | Inflación anual de costes de producto | % | 4,5% | 3,5% | 2,8% | Pes > Base > Opt |
| 5 | Factor de personal | × | 1,03 | 1,00 | 0,98 | Pes > Base > Opt |
| 6 | Factor de alquiler | × | 1,05 | 1,00 | 0,96 | Pes > Base > Opt |
| 7 | Inflación de suministros y servicios | % | 6,0% | 4,0% | 3,0% | Pes > Base > Opt |
| 8 | Marketing variable | % ingresos | 2,0% | 3,0% | 4,0% | Pes < Base < Opt |
| 9 | Factor de otros gastos | × | 1,08 | 1,00 | 0,95 | Pes > Base > Opt |
| 10 | Crecimiento de otros gastos | % | 3,0% | 2,5% | 2,0% | Pes > Base > Opt |

**Variables estructurales comunes** (no cambian por escenario): catálogo y mix, plan de personal y salarios, capex y vidas útiles, préstamo, tipo impositivo, capital circulante, estacionalidad, días operativos, rampa y crecimiento salarial.

**Excepción intencional**: el marketing variable es más bajo en Pesimista (2,0%) porque es una respuesta de gestión para proteger caja, no un coste externo. Se documenta para que el orden no parezca un error.

### 5.10 Índices e inflación

| Índice | Año 1 (2026) | Año 2 (2027) | Año 3 (2028) | Fórmula |
|---|---:|---:|---:|---|
| Precio (Base) | 1,000 | 1,025 | 1,0506 | (1 + 2,5%)^(y−1) |
| Coste (Base) | 1,000 | 1,035 | 1,0712 | (1 + 3,5%)^(y−1) |
| Servicios (Base) | 1,000 | 1,040 | 1,0816 | (1 + 4,0%)^(y−1) |
| Alquiler | 1,000 | 1,020 | 1,0404 | (1 + 2,0%)^(y−1) |
| Marketing fijo | 1,000 | 1,025 | 1,0506 | (1 + 2,5%)^(y−1) |
| Salario | 1,000 | 1,030 | 1,0609 | (1 + 3,0%)^(y−1) |
| Otros (Base) | 1,000 | 1,025 | 1,0506 | (1 + 2,5%)^(y−1) |

**Timing**: todos los índices se aplican desde enero de cada año; no hay escalonamiento mensual. En 2026 el índice es 1,000, por lo que la inflación de costes no afecta al primer año (sí a 2027 y 2028).

### 5.11 Supuestos de cálculo y presentación

- **Redondeo interno**: se conservan 2 decimales; la presentación redondea a euro. Los totales pueden diferir en ±1 € por redondeo.
- **Impuestos**: provisión mensual constante = cuota anual / 12; no se modelan pagos fraccionados ni el calendario real de Hacienda.
- **Capital circulante**: se calcula sobre COGS mensual; el stock inicial es 6.500 € y los proveedores aparecen en el mes 1.
- **Capex**: todo el capex inicial se paga en t0 (diciembre 2025/enero 2026) y se amortiza desde el mes 1.
- **Deuda**: primera cuota en enero 2026; sin carencia; sin comisión de apertura.
- **Caja**: no hay descubierto ni revolver; si la caja baja de 10.000 €, el modelo avisa, pero no se financia automáticamente.
- **Dividendos**: 0; toda la caja se retiene.
- **Inflación de precios**: se aplica al precio neto; el PVP con IVA se recalcula implícitamente.
- **Mix**: constante; no hay elasticidad precio-demanda ni canibalización.

---

## 6. Modelo matemático

### 6.1 Notación

- `t = 1..36`: mes del modelo.
- `y = ROUNDUP(t/12,0)`: año 1, 2 o 3.
- `m = MOD(t−1,12)+1`: mes del calendario, 1..12.
- `S_k`: variable `k` de la matriz de escenarios, seleccionada con `INDEX(ScenarioMatrix, k, $B$3)`.
- `B3`: selector de escenario de la hoja (1 = Pesimista, 2 = Base, 3 = Optimista).
- Todas las fórmulas de la tabla se escriben en la columna `C` (enero 2026) y se arrastran a `AL` (diciembre 2028).

### 6.2 Filas de tiempo

| Fila | Concepto | Fórmula en C | Unidad |
|---:|---|---|---|
| 5 | Índice de mes | `1` (constante); D5 `=C5+1` | mes |
| 6 | Fecha | `=DATE(2026,1,1)`; D6 `=EDATE(C6,1)` | fecha |
| 7 | Año | `=ROUNDUP(C5/12,0)` | 1–3 |
| 8 | Mes | `=MOD(C5-1,12)+1` | 1–12 |
| 9 | Días operativos | `=INDEX(OpeningDays,1,C8)` | días |

### 6.3 Cuenta de resultados (filas 12–35)

**Totales anuales**: en las filas de flujo (12–48), `AM`/`AN`/`AO` son la suma de los 12 meses (C–N, O–Z, AA–AL). En las filas de stock (caja, deuda), `AM`/`AN`/`AO` son el valor de diciembre (`N`, `Z`, `AL`). `AP` es la suma del trienio para flujos y el valor de 2028 para stocks.

| Fila | Concepto | Fórmula en C | Unidad |
|---:|---|---|---|
| 12 | Tickets/día | `=BaseTicketsDay*INDEX(ScenarioMatrix,1,$B$3)*(1+INDEX(ScenarioMatrix,2,$B$3))^(C7-1)*INDEX(Seasonality,1,C8)*IF(C7=1,INDEX(Ramp,1,C8),1)` | tickets/día |
| 13 | Tickets | `=C12*C9` | tickets |
| 14 | Ítems vendidos | `=C13*ItemsPerTicket` | ítems |
| 15 | Ingresos netos | `=C14*WeightedNetPrice*(1+INDEX(ScenarioMatrix,3,$B$3))^(C7-1)` | € |
| 16 | COGS | `=C14*WeightedCostAdj*(1+INDEX(ScenarioMatrix,4,$B$3))^(C7-1)` | € |
| 17 | Margen bruto | `=C15-C16` | € |
| 18 | Personal | `=INDEX(StaffCostByYear,1,C7)*INDEX(ScenarioMatrix,5,$B$3)/12` | € |
| 19 | Alquiler | `=RentMonth*INDEX(ScenarioMatrix,6,$B$3)*(1+RentGrowth)^(C7-1)` | € |
| 20 | Suministros | `=UtilitiesMonth*(1+INDEX(ScenarioMatrix,7,$B$3))^(C7-1)` | € |
| 21 | Servicios fijos | `=FixedServicesMonth*(1+INDEX(ScenarioMatrix,7,$B$3))^(C7-1)` | € |
| 22 | Marketing fijo | `=FixedMarketingMonth*(1+FixedMarketingGrowth)^(C7-1)` | € |
| 23 | Marketing variable | `=INDEX(ScenarioMatrix,8,$B$3)*C15` | € |
| 24 | Otros gastos | `=OtherOpexMonth*INDEX(ScenarioMatrix,9,$B$3)*(1+INDEX(ScenarioMatrix,10,$B$3))^(C7-1)` | € |
| 25 | Total opex + personal | `=SUM(C18:C24)` | € |
| 26 | EBITDA | `=C17-C25` | € |
| 27 | Amortización | `=MonthlyDepreciation` | € |
| 28 | EBIT | `=C26-C27` | € |
| 29 | Intereses | `=C53` | € |
| 30 | EBT | `=C28-C29` | € |
| 31 | Impuestos | `=IF(C7=1,$B$63/12,IF(C7=2,$C$63/12,$D$63/12))` | € |
| 32 | Beneficio neto | `=C30-C31` | € |
| 33 | Margen bruto % | `=IFERROR(C17/C15,0)` | % |
| 34 | Margen EBITDA % | `=IFERROR(C26/C15,0)` | % |
| 35 | Margen neto % | `=IFERROR(C32/C15,0)` | % |

**Identidad de control**: `C17 = C15 − C16`; `C26 = C17 − C25`; `C28 = C26 − C27`; `C30 = C28 − C29`; `C32 = C30 − C31`.

### 6.4 Caja (filas 38–49)

| Fila | Concepto | Fórmula en C | Unidad |
|---:|---|---|---|
| 38 | Caja inicial | `=OpeningCash`; D38 `=C48` | € |
| 39 | Capital circulante | `=C16*(InventoryDays-PayableDays)/365` | € |
| 40 | Δ capital circulante | `=C39-WC0`; D40 `=D39-C39` | € |
| 41 | Capex de mantenimiento | `=C15*MaintenanceCapexPct` | € |
| 42 | Impuesto teórico sin deuda | `=IF(C7=1,$B$68/12,IF(C7=2,$C$68/12,$D$68/12))` | € |
| 43 | FCFF | `=C26-C42-C41-C40` | € |
| 44 | Intereses | `=C53` | € |
| 45 | Escudo fiscal | `=C42-C31` | € |
| 46 | Principal | `=C54` | € |
| 47 | FCFE | `=C43-C44+C45-C46` | € |
| 48 | Caja final | `=C38+C47` | € |
| 49 | Check caja mínima | `=IF(C48<MinCash,"Alerta","OK")` | texto |

**Identidades de control**:

```
FCFE = FCFF − intereses + escudo − principal
Caja final = caja inicial + FCFE
FCFE = beneficio neto + amortización − capex mantenimiento − ΔWC − principal
```

La tercera identidad se usa en el test `test_cash_reconciliation`; la diferencia debe ser 0 ±1 €.

### 6.5 Calendario de deuda (filas 52–57)

| Fila | Concepto | Fórmula en C | Unidad |
|---:|---|---|---|
| 52 | Deuda inicial | `=LoanAmount`; D52 `=C55` | € |
| 53 | Intereses | `=C52*LoanRate/12` | € |
| 54 | Principal | `=MIN(LoanPayment-C53,C52)` | € |
| 55 | Deuda final | `=C52-C54` | € |
| 56 | Cuota | `=LoanPayment` | € |
| 57 | DSCR | `=IFERROR((C26-C31)/(C53+C54),0)` | × |

`LoanPayment` se calcula en `Supuestos!B48` como `=PMT(LoanRate/12,LoanMonths,-LoanAmount)`.

**Control**: la deuda final del mes 60 debe ser 0; el modelo solo llega al mes 36, pero el test extendido verifica el cierre.

### 6.6 Impuesto anual y pérdidas (filas 59–70)

| Fila | Concepto | 2026 (B) | 2027 (C) | 2028 (D) |
|---:|---|---|---|---|
| 60 | EBT anual | `=AM30` | `=AN30` | `=AO30` |
| 61 | Pérdidas inicio (con deuda) | `0` | `=B64` | `=C64` |
| 62 | Base imponible | `=MAX(0,B60-B61)` | `=MAX(0,C60-C61)` | `=MAX(0,D60-D61)` |
| 63 | Cuota | `=B62*TaxRate` | `=C62*TaxRate` | `=D62*TaxRate` |
| 64 | Pérdidas fin | `=B61-MIN(B61,MAX(0,B60))+MAX(0,-B60)` | `=C61-MIN(C61,MAX(0,C60))+MAX(0,-C60)` | `=D61-MIN(D61,MAX(0,D60))+MAX(0,-D60)` |
| 65 | EBIT anual | `=AM28` | `=AN28` | `=AO28` |
| 66 | Pérdidas inicio (sin deuda) | `0` | `=B69` | `=C69` |
| 67 | Base imponible sin deuda | `=MAX(0,B65-B66)` | `=MAX(0,C65-C66)` | `=MAX(0,D65-D66)` |
| 68 | Cuota sin deuda | `=B67*TaxRate` | `=C67*TaxRate` | `=D67*TaxRate` |
| 69 | Pérdidas fin (sin deuda) | `=B66-MIN(B66,MAX(0,B65))+MAX(0,-B65)` | `=C66-MIN(C66,MAX(0,C65))+MAX(0,-C65)` | `=D66-MIN(D66,MAX(0,D65))+MAX(0,-D65)` |
| 70 | Escudo fiscal | `=B68-B63` | `=C68-C63` | `=D68-D63` |

**Nota**: la cuota mensual de la fila 31 es la cuota anual dividida entre 12; no se recalcula mes a mes. Esto evita el artefacto de pagar impuestos en meses positivos y no recuperarlos en meses negativos del mismo año.

### 6.7 Resumen anual (filas 76–107)

| Fila | Métrica | 2026 (B) | 2027 (C) | 2028 (D) | 3 años (E) |
|---:|---|---|---|---|---|
| 76 | Ingresos netos | `=AM15` | `=AN15` | `=AO15` | `=SUM(B76:D76)` |
| 77 | COGS | `=AM16` | `=AN16` | `=AO16` | `=SUM(B77:D77)` |
| 78 | Margen bruto | `=AM17` | `=AN17` | `=AO17` | `=SUM(B78:D78)` |
| 79 | Personal | `=AM18` | `=AN18` | `=AO18` | `=SUM(B79:D79)` |
| 80 | Alquiler | `=AM19` | `=AN19` | `=AO19` | `=SUM(B80:D80)` |
| 81 | Suministros | `=AM20` | `=AN20` | `=AO20` | `=SUM(B81:D81)` |
| 82 | Servicios fijos | `=AM21` | `=AN21` | `=AO21` | `=SUM(B82:D82)` |
| 83 | Marketing fijo | `=AM22` | `=AN22` | `=AO22` | `=SUM(B83:D83)` |
| 84 | Marketing variable | `=AM23` | `=AN23` | `=AO23` | `=SUM(B84:D84)` |
| 85 | Otros gastos | `=AM24` | `=AN24` | `=AO24` | `=SUM(B85:D85)` |
| 86 | EBITDA | `=AM26` | `=AN26` | `=AO26` | `=SUM(B86:D86)` |
| 87 | Amortización | `=AM27` | `=AN27` | `=AO27` | `=SUM(B87:D87)` |
| 88 | EBIT | `=AM28` | `=AN28` | `=AO28` | `=SUM(B88:D88)` |
| 89 | Intereses | `=AM29` | `=AN29` | `=AO29` | `=SUM(B89:D89)` |
| 90 | EBT | `=AM30` | `=AN30` | `=AO30` | `=SUM(B90:D90)` |
| 91 | Impuestos | `=AM31` | `=AN31` | `=AO31` | `=SUM(B91:D91)` |
| 92 | Beneficio neto | `=AM32` | `=AN32` | `=AO32` | `=SUM(B92:D92)` |
| 93 | CFO | `=B92+B87-AM40` | `=C92+C87-AN40` | `=D92+D87-AO40` | `=SUM(B93:D93)` |
| 94 | Capex mantenimiento | `=AM41` | `=AN41` | `=AO41` | `=SUM(B94:D94)` |
| 95 | FCFF | `=AM43` | `=AN43` | `=AO43` | `=SUM(B95:D95)` |
| 96 | Principal | `=AM46` | `=AN46` | `=AO46` | `=SUM(B96:D96)` |
| 97 | FCFE | `=AM47` | `=AN47` | `=AO47` | `=SUM(B97:D97)` |
| 98 | Caja final | `=N48` | `=Z48` | `=AL48` | `=D98` |
| 99 | Tickets/día | `=AM13/AM9` | `=AN13/AN9` | `=AO13/AO9` | `=SUM(B99:D99)/3` |
| 100 | Ticket medio neto | `=B76/AM13` | `=C76/AN13` | `=D76/AO13` | `=E76/SUM(AM13:AO13)` |
| 101 | Ticket medio con IVA | `=B100*1.1` | `=C100*1.1` | `=D100*1.1` | `=E100*1.1` |
| 102 | Punto equilibrio EBITDA | `=(B79+B80+B81+B82+B83+B85)/((B76-B77-B84)/AM13)/AM9` | ídem C | ídem D | — |
| 103 | Punto equilibrio total | `=(B79+B80+B81+B82+B83+B85+B87+B89)/((B76-B77-B84)/AM13)/AM9` | ídem C | ídem D | — |
| 104 | Margen de seguridad | `=(B99-B103)/B99` | ídem C | ídem D | — |
| 105 | DSCR | `=(B86-B91)/(B89+B96)` | ídem C | ídem D | — |
| 106 | Cash-on-cash | `=AL110/Equity` | — | — | — |
| 107 | — | — | — | — | — |

**Ajuste de fila 93**: `CFO = beneficio neto + amortización − ΔWC`. `AM40`, `AN40`, `AO40` son las sumas anuales de la fila 40. Si se prefiere, `B93 = B92+B87-B40sum` con una fila auxiliar; el resultado es el mismo.

### 6.8 Payback (filas 109–114)

| Fila | Concepto | Fórmula |
|---:|---|---|
| 109 | FCFF acumulado | C109 `=C43`; D109 `=C109+D43`; … AL109 |
| 110 | FCFE acumulado | C110 `=C47`; D110 `=C110+D47`; … AL110 |
| 111 | Flag payback proyecto | C111 `=IF(C109>=TotalCapex+WC0,C5,999)` |
| 112 | Flag payback equity | C112 `=IF(C110>=Equity,C5,999)` |
| 113 | Payback proyecto (meses) | B113 `=IF(MIN(C111:AL111)=999,">36",MIN(C111:AL111))` |
| 114 | Payback equity (meses) | B114 `=IF(MIN(C112:AL112)=999,">36",MIN(C112:AL112))` |

**Inversión del proyecto**: `TotalCapex + WC0 = 132.000 + 6.500 = 138.500 €`.  
**Equity**: 90.000 €.  
**Regla**: si el mínimo de los flags es 999, el payback no se alcanza en 36 meses y se muestra `">36"`.

### 6.9 Rentabilidad por producto (filas 116–149)

Tres bloques idénticos, uno por año:

| Bloque | Cabecera | Productos | Total |
|---|---:|---:|---:|
| 2026 | 117 | 118–125 | 126 |
| 2027 | 128 | 129–136 | 137 |
| 2028 | 139 | 140–147 | 148 |

Columnas: A Producto, B Unidades, C Ingresos, D COGS, E Margen bruto, F Margen %.

Fórmulas para 2026 (fila 118, producto de la fila 5 de Productos):

```
B118 = $AM$14 * Productos!$H5
C118 = B118 * Productos!$F5
D118 = B118 * Productos!$J5
E118 = C118 - D118
F118 = E118 / C118
```

Para 2027 (fila 129):

```
B129 = $AN$14 * Productos!$H5
C129 = B129 * Productos!$F5 * (1 + INDEX(ScenarioMatrix,3,$B$3))^1
D129 = B129 * Productos!$J5 * (1 + INDEX(ScenarioMatrix,4,$B$3))^1
```

Para 2028 (fila 140):

```
B140 = $AO$14 * Productos!$H5
C140 = B140 * Productos!$F5 * (1 + INDEX(ScenarioMatrix,3,$B$3))^2
D140 = B140 * Productos!$J5 * (1 + INDEX(ScenarioMatrix,4,$B$3))^2
```

**Chequeo**: la suma de ingresos del bloque debe igualar `AM15`/`AN15`/`AO15`; la suma de COGS, `AM16`/`AN16`/`AO16`. Si no, `"Revisar"`.

### 6.10 Resumen: KPIs, comparativa y datos de gráficos

**KPIs por escenario (filas 6–15)**:

- Cabecera fila 6: Escenario, Año, Ingresos, EBITDA, Margen EBITDA, Beneficio neto, Margen neto, Caja final, Punto equilibrio total, Payback proyecto, Payback equity.
- Filas 7–9: Pesimista 2026–2028.
- Filas 10–12: Base 2026–2028.
- Filas 13–15: Optimista 2026–2028.
- Cada fila referencia la hoja del escenario: `Pesimista!AM76`, `Pesimista!AM86`, `Pesimista!AM92`, `Pesimista!N98`, `Pesimista!B103`, `Pesimista!B113`, `Pesimista!B114`; para 2027, `AN76/AN86/AN92`, `Z98` y `C103`; para 2028, `AO76/AO86/AO92`, `AL98` y `D103`. El payback (`B113/B114`) se repite.

**Payback y retorno (filas 17–21)**:

- Cabecera fila 17: Escenario, Payback proyecto, Payback equity, FCFE acumulado, Cash-on-cash.
- Filas 18–20: Pesimista, Base, Optimista. Referencias a `B113`, `B114`, `AL110`, `B106` de cada hoja.

**Comparativa 2028 (filas 23–25)**:

- Cabecera fila 22: Escenario, Ingresos, EBITDA, Beneficio neto, Caja final.
- Filas 23–25: los tres escenarios, referencias a 2028.

**Datos de gráficos**:

| Bloque | Filas | Columnas | Contenido |
|---|---:|---|---|
| Mensual | 110–146 | B–F | Mes, ingresos, EBITDA, beneficio neto, caja final del escenario seleccionado |
| Comparativa | 150–153 | B–F | Escenario, ingresos, EBITDA, beneficio neto, caja 2028 |
| Productos | 157–165 | B–C | Producto, ingresos Base 2028 |
| Costes | 168–174 | B–C | Categoría, importe Base 2026; fila 174 total |

**Fórmula del bloque mensual** (fila 111, enero 2026):

```
B111 = Base!C6
C111 = CHOOSE($B$4, Pesimista!C15, Base!C15, Optimista!C15)
D111 = CHOOSE($B$4, Pesimista!C26, Base!C26, Optimista!C26)
E111 = CHOOSE($B$4, Pesimista!C32, Base!C32, Optimista!C32)
F111 = CHOOSE($B$4, Pesimista!C48, Base!C48, Optimista!C48)
```

Se repite para los 36 meses, cambiando la columna de referencia (C..AL). `B4` es el selector 1/2/3.

**Bloque de costes (5 categorías)**:

| Fila | Categoría | Fórmula (Base 2026) |
|---:|---|---|
| 169 | Producto | `=Base!B77` |
| 170 | Personal | `=Base!B79` |
| 171 | Local | `=Base!B80+Base!B81+Base!B82` |
| 172 | Marketing | `=Base!B83+Base!B84` |
| 173 | Otros | `=Base!B85` |
| 174 | Total costes | `=SUM(B169:B173)` |

### 6.11 Punto de equilibrio: definición exacta

- **BE EBITDA**: tickets/día con EBITDA = 0. Costes fijos de caja = personal + alquiler + suministros + servicios fijos + marketing fijo + otros gastos. Contribución por ticket = (ingresos − COGS − marketing variable) / tickets.
- **BE total**: añade amortización e intereses; es el nivel de tickets/día con EBT = 0 (antes de impuestos).
- **Margen de seguridad**: (tickets/día previstos − BE total) / tickets/día previstos.

La fórmula anual de la fila 102/103 usa los totales anuales y los días del año; es una media ponderada, no la suma de los BE mensuales. El sitio muestra el BE mensual y el anual; el libro muestra el anual en el resumen y el mensual en cada hoja de escenario (filas auxiliares).

### 6.12 Payback: definición exacta

- **Payback proyecto**: primer mes en que el FCFF acumulado ≥ capex inicial + capital circulante inicial = 138.500 €.
- **Payback equity**: primer mes en que el FCFE acumulado ≥ equity aportado = 90.000 €.
- **Si no se alcanza en 36 meses**: `">36"`.
- **Cash-on-cash**: FCFE acumulado a 36 meses / equity.

### 6.13 Redondeo y tolerancias

- Los cálculos internos conservan 2 decimales; la presentación redondea a euro.
- Los objetivos dorados se comparan con tolerancia **±1 €** en importes y **±0,1 pp** en márgenes.
- El payback se compara como mes exacto; `">36"` es un valor válido.
- Las sumas anuales deben cuadrar con la suma de los 12 meses; el test lo verifica.

---

## 7. Escenarios

### 7.1 Matriz congelada

| # | Variable | Pesimista | Base | Optimista |
|---:|---|---:|---:|---:|
| 1 | Factor de demanda año 1 | 0,88 | 1,00 | 1,08 |
| 2 | Crecimiento anual de demanda | 1,5% | 4,0% | 6,0% |
| 3 | Crecimiento anual de precios | 1,5% | 2,5% | 3,2% |
| 4 | Inflación anual de costes de producto | 4,5% | 3,5% | 2,8% |
| 5 | Factor de personal | 1,03 | 1,00 | 0,98 |
| 6 | Factor de alquiler | 1,05 | 1,00 | 0,96 |
| 7 | Inflación de suministros y servicios | 6,0% | 4,0% | 3,0% |
| 8 | Marketing variable (% ingresos) | 2,0% | 3,0% | 4,0% |
| 9 | Factor de otros gastos | 1,08 | 1,00 | 0,95 |
| 10 | Crecimiento de otros gastos | 3,0% | 2,5% | 2,0% |

### 7.2 Narrativa

**Pesimista — "el invierno largo".** El barrio no responde como se esperaba: la demanda arranca un 12% por debajo del plan, crece solo un 1,5% y el precio no se puede subir más de un 1,5% sin perder clientes. El café y la energía se encarecen (4,5% y 6,0%), el convenio presiona el personal (factor 1,03) y el alquiler se revisa al alza (1,05). La empresa responde bajando marketing al 2,0% y ajustando otros gastos, pero no despide: mantiene el plan de FTE. **Para qué sirve**: test de resistencia para el banco, negociación del alquiler, decisión de contratar o no el segundo barista, y monitorización de covenants. **Disparadores**: tres meses consecutivos con tickets ≥10% por debajo del plan, coste del café >5% interanual, apertura de un competidor directo, obras que cortan la calle, caída del turismo.

**Base — "el plan creíble".** La demanda arranca en el potencial del local (360 tickets/día en régimen), crece un 4,0% anual, los precios suben un 2,5% y los costes un 3,5%. El personal pasa de 3,5 a 4,0 FTE en 2027; el alquiler se revisa un 2,0%; los servicios un 4,0%. **Para qué sirve**: presupuesto anual, seguimiento mensual, comunicación a socios y banco. **Disparadores de re-forecast**: dos meses consecutivos con tickets ≥10% por debajo del plan, inflación de costes ≥2 pp por encima, desviación de capex ≥10%, o una bajada de precios de la competencia.

**Optimista — "Aurora se convierte en referencia".** La demanda arranca un 8% por encima del plan y crece un 6,0%; el precio medio sube un 3,2% porque la marca se consolida; los costes se moderan (2,8%), el equipo gana productividad (factor 0,98), se negocia mejor el alquiler (0,96) y se invierte más en marketing (4,0%). **Para qué sirve**: decisión de segunda ubicación, caso para un inversor, inversión en retail/wholesale, evaluación de una ampliación. **Disparadores**: tickets/día >400 durante seis meses, retail >8% de ingresos, cuentas corporativas recurrentes, prensa local, lista de espera en fin de semana.

### 7.3 Qué cambia y qué no

**Cambia con el escenario**: solo las 10 variables de la matriz.

**No cambia**: catálogo, mix, merma, plan de personal y salarios, capex y vidas útiles, préstamo, tipo impositivo, capital circulante, estacionalidad, días operativos, rampa, crecimiento salarial, marketing fijo y crecimiento del alquiler.

**Por qué**: si cada escenario cambiara también la plantilla o el capex, la comparación dejaría de ser limpia. Para probar una segunda ubicación o un local más grande, se crea un modelo nuevo, no un escenario.

### 7.4 Sensibilidad (Base 2026)

| Cambio | Δ EBITDA | Δ Beneficio neto | Lectura |
|---|---:|---:|---|
| Demanda −10% | −24.028 € | −18.021 € | El riesgo principal; los costes fijos no bajan |
| Demanda +10% | +24.028 € | +18.021 € | El mismo efecto, al revés |
| Precio +5% (sin perder demanda) | +18.644 € | +13.983 € | Muy potente; la elasticidad no se modela |
| Personal +5% | −5.523 € | −4.142 € | El coste más grande y rígido |
| Alquiler +10% | −2.280 € | −1.710 € | Importante, pero menor que personal |
| Marketing +1 pp | −3.844 € | −2.883 € | Debe generar demanda; no se asume |
| Coste de producto +1 pp | 0 € en 2026; −1.455 € en 2027; −3.145 € en 2028 | 0 / −1.091 / −2.359 € | El índice parte de 1,000 en 2026 |

**Lectura**: la demanda y el precio mueven el resultado mucho más que el alquiler o el marketing. La demanda es lo que menos se controla; por eso el Pesimista es el escenario que decide.

### 7.5 Objetivos dorados

> Cifras calculadas con los supuestos congelados. Son objetivos de verificación, no valores que se escriban en el libro. Tolerancia: ±1 € y ±0,1 pp.

#### Base

| Métrica | 2026 | 2027 | 2028 |
|---|---:|---:|---:|
| Ingresos netos | 384.419 € | 432.330 € | 460.864 € |
| COGS | 132.608 € | 150.591 € | 162.096 € |
| Margen bruto | 251.810 € | 281.739 € | 298.768 € |
| Margen bruto % | 65,5% | 65,2% | 64,8% |
| Personal | 110.460 € | 129.350 € | 133.230 € |
| Opex (sin personal) | 79.693 € | 83.121 € | 86.032 € |
| EBITDA | 61.658 € | 69.268 € | 79.505 € |
| Margen EBITDA | 16,0% | 16,0% | 17,3% |
| Amortización | 16.625 € | 16.625 € | 16.625 € |
| EBIT | 45.033 € | 52.643 € | 62.880 € |
| Intereses | 4.843 € | 3.913 € | 2.910 € |
| EBT | 40.189 € | 48.730 € | 59.970 € |
| Impuestos | 10.047 € | 12.183 € | 14.993 € |
| Beneficio neto | 30.142 € | 36.548 € | 44.978 € |
| Margen neto | 7,8% | 8,5% | 9,8% |
| Caja final | 57.456 € | 91.258 € | 132.063 € |
| Tickets/día | 342,0 | 375,2 | 390,2 |
| Ticket medio neto | 3,60 € | 3,69 € | 3,79 € |
| BE EBITDA / total | 254 / 285 | 278 / 307 | 281 / 308 |
| DSCR | 3,07 | 3,39 | 3,83 |

#### Pesimista

| Métrica | 2026 | 2027 | 2028 |
|---|---:|---:|---:|
| Ingresos netos | 338.289 € | 367.682 € | 378.796 € |
| COGS | 116.695 € | 130.584 € | 138.507 € |
| Margen bruto | 221.593 € | 237.099 € | 240.289 € |
| Margen bruto % | 65,5% | 64,5% | 63,4% |
| Personal | 113.774 € | 133.230 € | 137.227 € |
| Opex (sin personal) | 77.122 € | 80.357 € | 83.348 € |
| EBITDA | 30.698 € | 23.511 € | 19.713 € |
| Margen EBITDA | 9,1% | 6,4% | 5,2% |
| Amortización | 16.625 € | 16.625 € | 16.625 € |
| EBIT | 14.073 € | 6.886 € | 3.088 € |
| Intereses | 4.843 € | 3.913 € | 2.910 € |
| EBT | 9.229 € | 2.974 € | 178 € |
| Impuestos | 2.307 € | 743 € | 45 € |
| Beneficio neto | 6.922 € | 2.230 € | 134 € |
| Margen neto | 2,0% | 0,6% | 0,0% |
| Caja final | 34.875 € | 35.319 € | 32.499 € |
| Tickets/día | 300,9 | 322,2 | 327,1 |
| Ticket medio neto | 3,60 € | 3,66 € | 3,71 € |
| BE EBITDA / total | 258 / 288 | 289 / 318 | 299 / 327 |
| DSCR | 1,69 | 1,35 | 1,17 |

#### Optimista

| Métrica | 2026 | 2027 | 2028 |
|---|---:|---:|---:|
| Ingresos netos | 415.172 € | 479.145 € | 524.147 € |
| COGS | 143.217 € | 164.645 € | 179.410 € |
| Margen bruto | 271.955 € | 314.501 € | 344.737 € |
| Margen bruto % | 65,5% | 65,6% | 65,8% |
| Personal | 108.251 € | 126.763 € | 130.566 € |
| Opex (sin personal) | 83.195 € | 87.380 € | 90.848 € |
| EBITDA | 80.509 € | 100.358 € | 123.323 € |
| Margen EBITDA | 19,4% | 20,9% | 23,5% |
| Amortización | 16.625 € | 16.625 € | 16.625 € |
| EBIT | 63.884 € | 83.733 € | 106.698 € |
| Intereses | 4.843 € | 3.913 € | 2.910 € |
| EBT | 59.041 € | 79.820 € | 103.788 € |
| Impuestos | 14.760 € | 19.955 € | 25.947 € |
| Beneficio neto | 44.281 € | 59.865 € | 77.841 € |
| Margen neto | 10,7% | 12,5% | 14,9% |
| Caja final | 71.169 € | 127.596 € | 200.325 € |
| Tickets/día | 369,3 | 413,0 | 437,8 |
| Ticket medio neto | 3,60 € | 3,72 € | 3,84 € |
| BE EBITDA / total | 253 / 284 | 273 / 301 | 271 / 297 |
| DSCR | 3,91 | 4,78 | 5,79 |

#### Payback y retorno

| Escenario | Payback proyecto | Payback equity | FCFE acumulado 3 años | Cash-on-cash 3 años |
|---|---:|---:|---:|---:|
| Pesimista | >36 meses | >36 meses | 10.999 € | 12,2% |
| Base | 34 meses | 30 meses | 110.563 € | 122,8% |
| Optimista | 25 meses | 22 meses | 178.825 € | 198,7% |

### 7.6 Validación aritmética

| Chequeo | Cálculo | Resultado |
|---|---|---:|
| Mix de producto | 22+20+10+13+8+14+9+4 | 100% |
| Estacionalidad | suma de 12 factores | 12,00 |
| Días operativos | suma de 12 meses | 312 |
| Precio neto ponderado | SUMPRODUCT(mix, PVP/1,10) | 2,6691 € |
| Coste ajustado ponderado | SUMPRODUCT(mix, coste/(1−merma)) | 0,9207 € |
| Margen bruto ponderado | 1 − 0,9207/2,6691 | 65,50% |
| Coste personal 2026 | 84.000 × 1,315 | 110.460 € |
| Capex | 65.000+28.000+15.000+12.000+7.000+5.000 | 132.000 € |
| Amortización anual | suma de capex/vida | 16.625 € |
| Fuentes = usos | 90.000+70.000 = 132.000+6.500+21.500 | 160.000 € |
| Cuota del préstamo | PMT(7,5%/12,60,−70.000) | 1.402,66 € |
| P&L Base 2026 | 384.419−132.608−110.460−79.693 | 61.658 € |
| Caja Base 2026 | 21.500+35.956 | 57.456 € |
| Payback proyecto Base | FCFF acumulado ≥ 138.500 | mes 34 |
| Payback equity Base | FCFE acumulado ≥ 90.000 | mes 30 |

### 7.7 Reglas de integridad de escenarios

1. **Orden de demanda y precio**: Pesimista < Base < Optimista.
2. **Orden de costes**: Pesimista > Base > Optimista para coste de producto, personal, alquiler, servicios y otros; marketing es la excepción documentada.
3. **Estructural común**: cualquier cambio en catálogo, personal, capex, préstamo, fiscalidad o circulante se aplica a los tres escenarios.
4. **Si se cambia la matriz**: regenerar `expected.json`, el libro, el sitio y este documento; actualizar los objetivos dorados.
5. **Si un escenario deja de ser coherente** (por ejemplo, Pesimista con más beneficio que Base), el test `test_scenario_ordering` falla.

---

## 8. Diseño del libro Excel

### 8.1 Layout global

| Elemento | Valor |
|---|---|
| Columnas | A concepto (42), B t0/nota (14), C–AL meses 1–36 (11), AM–AO totales anuales (13), AP total trienio (13) |
| Filas de cabecera | 1–4 título, subtítulo, selector, nota |
| Filas de tiempo | 5–9 índice, fecha, año, mes, días |
| P&L | 11–35 |
| Caja | 37–49 |
| Deuda | 51–57 |
| Impuesto | 58–70 |
| Resumen anual | 74–107 |
| Payback | 109–114 |
| Productos | 116–149 |
| Congelar | `C10` |
| Zoom | 85% |
| Fuente | Calibri 10; títulos 16/12 |
| Gridlines | Ocultas en la vista de impresión; visibles en pantalla |

### 8.2 Portada

| Celda | Contenido |
|---|---|
| A1 | "Cafetería Aurora" (28 pt, espresso) |
| A2 | "Modelo financiero 2026–2028" (16 pt, terracota) |
| A3 | "Café de especialidad · Zaragoza · EUR" |
| A5 | "Qué es este libro" |
| A6 | Texto de 3 líneas: tres escenarios, 36 meses, fórmulas vivas |
| A8 | "Cómo usarlo" |
| A9–A14 | 1) Elige escenario en Resumen B4; 2) cambia solo celdas amarillas; 3) no edites celdas blancas; 4) revisa los checks; 5) descarga la versión web |
| A16 | "Leyenda" |
| A17 | Cuadrado amarillo "Entrada editable" |
| A18 | Cuadrado blanco "Fórmula (no editar)" |
| A19 | Cuadrado verde/rojo "Check" |
| A21 | "Fuente de verdad: data/model.json" |
| A22 | "Versión 1.0 · 25/10/2026" |
| A24 | "Aviso: modelo educativo; no es asesoramiento financiero" |

Sin fórmulas calculadas; solo texto y formato.

### 8.3 Resumen

**Selector**:

- `B4` = 2 (entrada, validación 1–3).
- `C4` = `=INDEX({"Pesimista","Base","Optimista"},B4)`.
- Nota en `D4`: "Selecciona el escenario de los gráficos mensuales".

**KPIs por escenario (filas 6–15)**:

| Fila | Contenido |
|---:|---|
| 6 | Cabecera: Escenario, Año, Ingresos, EBITDA, Margen EBITDA, Beneficio neto, Margen neto, Caja final, Punto equilibrio total, Payback proyecto, Payback equity |
| 7–9 | Pesimista 2026, 2027, 2028 |
| 10–12 | Base 2026, 2027, 2028 |
| 13–15 | Optimista 2026, 2027, 2028 |

Fórmulas de referencia:

```
C7 = Pesimista!AM76      D7 = Pesimista!AM86      E7 = D7/C7
F7 = Pesimista!AM92      G7 = F7/C7               H7 = Pesimista!N98
I7 = Pesimista!B103      J7 = Pesimista!B113      K7 = Pesimista!B114
```

Para 2027, sustituir `AM` por `AN`, `N98` por `Z98` y `B103` por `C103`; para 2028, `AM` por `AO`, `N98` por `AL98` y `B103` por `D103`. El payback es único por escenario y se repite en las tres filas con `B113/B114`; el BE total sí cambia por año (`B103/C103/D103`).

**Payback y retorno (filas 17–21)**:

| Fila | Contenido |
|---:|---|
| 17 | Cabecera: Escenario, Payback proyecto, Payback equity, FCFE acumulado, Cash-on-cash |
| 18 | Pesimista: `=Pesimista!B113`, `=Pesimista!B114`, `=Pesimista!AL110`, `=Pesimista!B106` |
| 19 | Base: ídem |
| 20 | Optimista: ídem |

**Comparativa 2028 (filas 22–25)**:

| Fila | Contenido |
|---:|---|
| 22 | Cabecera: Escenario, Ingresos, EBITDA, Beneficio neto, Caja final |
| 23 | Pesimista: `=Pesimista!AO76`, `=Pesimista!AO86`, `=Pesimista!AO92`, `=Pesimista!AL98` |
| 24 | Base: ídem |
| 25 | Optimista: ídem |

**Datos de gráficos**:

| Bloque | Filas | Columnas | Contenido |
|---|---:|---|---|
| Mensual | 110–146 | B–F | Mes, ingresos, EBITDA, beneficio neto, caja final |
| Comparativa | 150–153 | B–E | Escenario, ingresos, EBITDA, beneficio neto |
| Productos | 157–165 | B–C | Producto, ingresos Base 2028 |
| Costes | 168–174 | B–C | Categoría, importe Base 2026; fila 174 total |

**Fórmulas del bloque mensual** (fila 111, enero 2026):

```
B111 = Base!C6
C111 = CHOOSE($B$4,Pesimista!C15,Base!C15,Optimista!C15)
D111 = CHOOSE($B$4,Pesimista!C26,Base!C26,Optimista!C26)
E111 = CHOOSE($B$4,Pesimista!C32,Base!C32,Optimista!C32)
F111 = CHOOSE($B$4,Pesimista!C48,Base!C48,Optimista!C48)
```

Se repite para las 36 columnas C–AL.

**Fórmulas del bloque de costes**:

```
B168 = "Categoría"; C168 = "Importe"
B169 = "Producto";  C169 = Base!B77
B170 = "Personal";  C170 = Base!B79
B171 = "Local";     C171 = Base!B80+Base!B81+Base!B82
B172 = "Marketing"; C172 = Base!B83+Base!B84
B173 = "Otros";     C173 = Base!B85
B174 = "Total";     C174 = SUM(C169:C173)
```

### 8.4 Supuestos

| Bloque | Filas | Contenido |
|---|---:|---|
| Identidad | 4–10 | Nombre, moneda, inicio, meses, año base |
| Demanda | 12–15 | Tickets/día, ítems/ticket, días/año |
| Estacionalidad | 17–23 | Cabecera de meses, factores, días, rampa, checks |
| Matriz | 25–38 | Cabecera, 10 variables, check de orden |
| Financiación | 40–49 | Equity, deuda, tipo, plazo, caja, stock, mínimo, PMT, cuadre |
| Fiscalidad | 52–57 | Tipo, días de inventario/proveedor/cobro, tratamiento de pérdidas |
| Crecimientos | 60–63 | Alquiler, marketing fijo |
| Checks | 65–72 | Mix, estacionalidad, días, capex, fuentes/usos, orden |

**Celdas clave**:

| Celda | Valor |
|---|---|
| B13 | 360 tickets/día |
| B14 | 1,35 ítems/ticket |
| B15 | 312 días/año (fórmula) |
| C19:N19 | Estacionalidad |
| C20:N20 | Días operativos |
| C21:N21 | Rampa |
| D27:F36 | Matriz de escenarios |
| B41 | 90.000 € |
| B42 | 70.000 € |
| B43 | 7,5% |
| B44 | 60 |
| B45 | 21.500 € |
| B46 | 6.500 € |
| B47 | 10.000 € |
| B48 | `=PMT(B43/12,B44,-B42)` |
| B53 | 25% |
| B54 | 18 |
| B55 | 30 |
| B56 | 0 |
| B61 | 2,0% |
| B62 | 2,5% |

**Checks**:

```
B67 = SUM(Productos!H5:H12)          -> 100%
B68 = SUM(C19:N19)                    -> 12
B69 = SUM(C20:N20)                    -> 312
B70 = Costos!B21                      -> 132.000
B71 = IF(B41+B42=Costos!B30,"OK","Revisar")
B72 = IF(AND(D27<E27,E27<F27,D28<E28,E28<F28,D29<E29,E29<F29),"OK","Revisar orden")
```

El check de costes se hace en una celda aparte (B73) con las desigualdades inversas; el de marketing se documenta como excepción.

### 8.5 Productos

| Fila | Contenido |
|---:|---|
| 4 | Cabecera: #, Producto, Categoría, PVP, IVA, Precio neto, Coste, Mix, Merma, Coste ajustado, Margen unitario, Margen %, Contribución |
| 5–12 | 8 productos |
| 13 | Totales y ponderados |
| 14 | Checks: mix 100%, PVP > coste |

**Fórmulas**:

```
F5 = D5/(1+E5)
J5 = G5/(1-I5)
K5 = F5-J5
L5 = K5/F5
M5 = F5*H5
F13 = SUMPRODUCT(F5:F12,H5:H12)
J13 = SUMPRODUCT(J5:J12,H5:H12)
K13 = F13-J13
L13 = K13/F13
H13 = SUM(H5:H12)
```

### 8.6 Personal

| Fila | Contenido |
|---:|---|
| 4 | Cabecera: Rol, Salario bruto, FTE 2026, FTE 2027, FTE 2028, Coste 2026, Coste 2027, Coste 2028 |
| 5–8 | 4 roles |
| 9 | Totales: FTE y coste |
| 11 | Cotización empresarial 31,5% |
| 12 | Crecimiento salarial 3,0% |

**Fórmulas**:

```
F5 = B5*C5*(1+$B$11)
G5 = B5*(1+$B$12)*D5*(1+$B$11)
H5 = B5*(1+$B$12)^2*E5*(1+$B$11)
C9 = SUM(C5:C8), etc.
F9 = SUM(F5:F8), etc.
```

### 8.7 Costos

| Bloque | Filas | Contenido |
|---|---:|---|
| Costes fijos | 4–11 | Cabecera, 5 conceptos, total |
| Capex | 13–21 | Cabecera, 6 activos, total |
| Mantenimiento | 23–24 | % de ingresos |
| Cuadre | 26–32 | Capex, stock, caja, usos, fuentes, check |

**Celdas clave**:

| Celda | Valor |
|---|---|
| B6 | 1.900 €/mes alquiler |
| B7 | 1.450 €/mes suministros |
| B8 | 780 €/mes servicios |
| B9 | 450 €/mes marketing fijo |
| B10 | 1.100 €/mes otros |
| B21 | 132.000 € capex total |
| D21 | 16.625 € amortización anual |
| E21 | 1.385,42 € amortización mensual |
| B24 | 1,5% mantenimiento |
| B30 | `=B21+Supuestos!B46+Supuestos!B45` (usos) |
| B31 | `=Supuestos!B41+Supuestos!B42` (fuentes) |
| B32 | `=IF(B30=B31,"OK","Revisar")` |

### 8.8 Hojas de escenario

Cada hoja es idéntica; solo cambia `B3` (1, 2, 3) y el nombre de la pestaña. La tabla de filas 1–149 de la Sección 6 es el contrato.

**Cabecera**:

| Fila | Contenido |
|---:|---|
| 1 | "Cafetería Aurora — Escenario Base" |
| 2 | "EUR, sin IVA. Solo se editan las hojas de entrada." |
| 3 | "Selector (1/2/3):" y B3 |
| 4 | "Escenario:" y B4 `=INDEX({"Pesimista","Base","Optimista"},B3)` |
| 5–9 | Tiempo |

**Bloques**: P&L 11–35; caja 37–49; deuda 51–57; impuesto 58–70; resumen 74–107; payback 109–114; productos 116–149.

**Formato condicional**:

- `C49:AL49`: si "Alerta", fondo rojo.
- `C26:AL26`: si EBITDA < 0, fondo ámbar.
- `C32:AL32`: si beneficio neto < 0, fondo rojo.
- `C33:AL33`: si margen bruto < 60%, ámbar.
- `C34:AL34`: si margen EBITDA < 10%, ámbar.

### 8.9 Aprende

- A1 título; A2 introducción; A4 leyenda; A6 "Cómo leer".
- 10 capítulos, uno cada 8 filas desde la fila 10: título, texto, ejemplo vivo, ejercicio, respuesta.
- **Ejemplos vivos**: las celdas de ejemplo son fórmulas que referencian `Base!` y usan `TEXT(...)`; no se escriben cifras a mano.
- Ejemplo de fórmula: `="Ingresos 2026: "&TEXT(Base!AM15,"#.##0 €")&" · EBITDA: "&TEXT(Base!AM86,"#.##0 €")`.
- Ejercicios: una celda de respuesta con fórmula; el texto de la pregunta puede ser estático.

### 8.10 Nombres definidos

| Nombre | Hoja | Celda/rango | Uso |
|---|---|---|---|
| `BaseTicketsDay` | Supuestos | B13 | Demanda |
| `ItemsPerTicket` | Supuestos | B14 | Ítems |
| `Seasonality` | Supuestos | C19:N19 | Estacionalidad |
| `OpeningDays` | Supuestos | C20:N20 | Días |
| `Ramp` | Supuestos | C21:N21 | Rampa |
| `ScenarioMatrix` | Supuestos | D27:F36 | Matriz |
| `Equity` | Supuestos | B41 | Payback equity |
| `LoanAmount` | Supuestos | B42 | Deuda |
| `LoanRate` | Supuestos | B43 | Interés |
| `LoanMonths` | Supuestos | B44 | Plazo |
| `LoanPayment` | Supuestos | B48 | Cuota |
| `OpeningCash` | Supuestos | B45 | Caja inicial |
| `WC0` | Supuestos | B46 | Circulante inicial |
| `MinCash` | Supuestos | B47 | Alerta |
| `TaxRate` | Supuestos | B53 | Impuesto |
| `InventoryDays` | Supuestos | B54 | Circulante |
| `PayableDays` | Supuestos | B55 | Circulante |
| `RentGrowth` | Supuestos | B61 | Alquiler |
| `FixedMarketingGrowth` | Supuestos | B62 | Marketing |
| `ProductPVP` | Productos | D5:D12 | Catálogo |
| `ProductVAT` | Productos | E5:E12 | Catálogo |
| `ProductNetPrice` | Productos | F5:F12 | Ingresos |
| `ProductCost` | Productos | G5:G12 | COGS |
| `ProductMix` | Productos | H5:H12 | Mix |
| `ProductWaste` | Productos | I5:I12 | Merma |
| `ProductCostAdj` | Productos | J5:J12 | COGS |
| `ProductUnitMargin` | Productos | K5:K12 | Margen |
| `WeightedNetPrice` | Productos | F13 | Ingresos |
| `WeightedCostAdj` | Productos | J13 | COGS |
| `StaffSalary` | Personal | B5:B8 | Personal |
| `StaffFTE_Y1` | Personal | C5:C8 | Personal |
| `StaffFTE_Y2` | Personal | D5:D8 | Personal |
| `StaffFTE_Y3` | Personal | E5:E8 | Personal |
| `StaffCostByYear` | Personal | F9:H9 | Personal |
| `EmployerSS` | Personal | B11 | Personal |
| `SalaryGrowth` | Personal | B12 | Personal |
| `RentMonth` | Costos | B6 | Alquiler |
| `UtilitiesMonth` | Costos | B7 | Suministros |
| `FixedServicesMonth` | Costos | B8 | Servicios |
| `FixedMarketingMonth` | Costos | B9 | Marketing |
| `OtherOpexMonth` | Costos | B10 | Otros |
| `CapexAmount` | Costos | B15:B20 | Capex |
| `CapexLife` | Costos | C15:C20 | Vida |
| `MonthlyDepreciation` | Costos | E21 | Amortización |
| `TotalCapex` | Costos | B21 | Payback |
| `MaintenanceCapexPct` | Costos | B24 | Capex mantenimiento |

### 8.11 Gráficos del Resumen

| # | Título | Tipo | Datos | Categorías | Ancla |
|---:|---|---|---|---|---|
| 1 | Ingresos y EBITDA — escenario seleccionado | Barras + línea | `Resumen!$C$110:$D$146` | `Resumen!$B$111:$B$146` | M6 |
| 2 | Beneficio neto y caja final | Barras + línea (eje secundario) | `Resumen!$E$110:$E$146` y `$F$110:$F$146` | `Resumen!$B$111:$B$146` | M23 |
| 3 | Comparativa de escenarios 2028 | Barras agrupadas | `Resumen!$C$150:$E$153` | `Resumen!$B$151:$B$153` | M40 |
| 4 | Ingresos por producto — Base 2028 | Barras horizontales | `Resumen!$C$157:$C$165` | `Resumen!$B$158:$B$165` | M57 |
| 5 | Estructura de costes — Base 2026 | Dona | `Resumen!$C$168:$C$173` | `Resumen!$B$169:$B$173` | M74 |

**Estilo**: título 12 pt espresso; ejes 10 pt muted; grid horizontal suave; leyenda inferior; colores terracota/salvia/dorado/espresso/gris; sin 3D; sin sombra; número `#,##0 €`.

**Tamaño**: 15 × 8 cm; 5 gráficos no se solapan (M6, M23, M40, M57, M74; cada uno ocupa ~17 filas).

### 8.12 Checks y formato condicional

| Check | Celda | Condición | Mensaje |
|---|---|---|---|
| Mix 100% | Supuestos!B67 | `=SUM(ProductMix)` | "OK"/"Revisar" |
| Estacionalidad 12 | Supuestos!B68 | `=SUM(Seasonality)` | "OK"/"Revisar" |
| Días 312 | Supuestos!B69 | `=SUM(OpeningDays)` | "OK"/"Revisar" |
| Capex 132.000 | Supuestos!B70 | `=TotalCapex` | "OK"/"Revisar" |
| Fuentes = usos | Supuestos!B71 | `=Equity+LoanAmount=TotalUses` | "OK"/"Revisar" |
| Orden escenarios | Supuestos!B72 | demanda/precio | "OK"/"Revisar" |
| Orden costes | Supuestos!B73 | costes inversos | "OK"/"Revisar" |
| Caja mínima | Escenario!C49:AL49 | `>=MinCash` | "Alerta" |
| P&L cuadrado | Escenario!C36 | `=C17-C25-C26` | 0 |
| Caja cuadrada | Escenario!C50 | `=C38+C47-C48` | 0 |
| Producto vs P&L | Escenario!C149 | `=C148-AM15` | 0 |

### 8.13 Impresión y exportación

- Escenario: A4 horizontal, ajustar a 1 página de ancho, repetir filas 1–9, columnas A–B, gridlines off, encabezado "Cafetería Aurora — Modelo 2026–2028", pie "Página X de Y".
- Resumen: A4 horizontal, ajustar a 1 página de ancho; los gráficos se imprimen en color.
- Aprende: A4 vertical, ajustar a 1 página de ancho.
- PDF: exportar Resumen + Base + Aprende como PDF de 3 páginas para revisión; no es un entregable obligatorio.

### 8.14 Reglas de integridad de fórmulas

1. **Celdas calculadas = fórmulas**: en escenarios, Resumen y tablas de producto, toda celda numérica calculada tiene `data_type == "f"`.
2. **Sin enlaces externos**: ninguna fórmula contiene `[` o `.xlsx`.
3. **Funciones permitidas**: `SUM`, `SUMPRODUCT`, `INDEX`, `MATCH`, `IF`, `IFERROR`, `MAX`, `MIN`, `ROUND`, `ROUNDUP`, `MOD`, `DATE`, `EDATE`, `PMT`, `CHOOSE`, `TEXT`, `ABS`. Prohibidas: `XLOOKUP`, `IFS`, `LET`, `LAMBDA`, `FILTER`, `SORT`, `UNIQUE`, `WEBSERVICE`, `HYPERLINK` a archivos locales.
4. **Nombres definidos**: todos resuelven; no hay `#NAME?`.
5. **Plantilla única**: las tres hojas de escenario tienen las mismas fórmulas normalizadas (solo cambia B3).
6. **Gráficos**: cada serie apunta a un rango con celdas; ninguna imagen.
7. **Recalculación**: `fullCalcOnLoad=True`; test con LibreOffice headless o `formulas`; sin `#REF!`, `#VALUE!`, `#DIV/0!`.
8. **Tolerancia**: ±1 € / ±0,1 pp contra `expected.json`.

---

## 9. Sitio web

### 9.1 Principios

- **Estático y sin dependencias**: HTML, CSS y JS vanilla; SVG inline; sin CDN, sin fuentes externas, sin analytics.
- **Todo el cálculo en el cliente**: el mismo modelo JS que se testea en Node.
- **Dos páginas**: dashboard (`index.html`) y guía (`aprende.html`); el resto son secciones.
- **Una idea por sección**: KPI → gráfico → lectura → detalle.
- **Honestidad**: los tres escenarios visibles; el Pesimista no se esconde.
- **Rendimiento**: <100 KB de JS propio, primera carga <2,5 s en 4G, sin bloqueo de render.

### 9.2 Arquitectura de información

```
index.html
├── Header (marca, nav, CTA descarga)
├── Hero + tira de 5 KPIs
├── Selector de escenario + selector de año
├── 1. La foto del negocio (KPIs)
├── 2. Ingresos y EBITDA (gráfico + tabla anual)
├── 3. Caja y deuda (gráfico + payback)
├── 4. Unit economics (tabla de productos)
├── 5. Dónde se va el dinero (costes)
├── 6. Punto de equilibrio (bullet + margen)
├── 7. El modelo completo (P&L anual/mensual)
├── 8. Laboratorio de supuestos
├── 9. Aprende (CTA a la guía)
├── 10. Descarga + metodología + aviso
└── Footer

aprende.html
├── Header
├── Portada de la guía + índice sticky
├── 10 capítulos
├── Calculadoras (ticket, break-even, caja)
├── Glosario
├── Checklist
└── Footer
```

### 9.3 Dashboard: contenido exacto

**Hero**

- Titular: "Un café se puede modelar. Y se puede tocar."
- Subtítulo: "36 meses, tres escenarios y todas las fórmulas a la vista. La economía de una cafetería de especialidad en Zaragoza."
- KPIs del escenario activo (Base por defecto, año 2028):
  - Ingresos: **460.864 €**.
  - EBITDA: **79.505 €** (17,3%).
  - Beneficio neto: **44.978 €** (9,8%).
  - Caja final: **132.063 €**.
  - Payback: **34 meses** (proyecto) / **30** (equity).

**Selector**

- Escenario: Pesimista / Base / Optimista.
- Año: 2026 / 2027 / 2028.
- Texto de contexto de una línea por escenario.
- Al cambiar, se actualizan KPIs, gráficos, tablas y el estado de la URL.

**La foto del negocio**

- 5 tarjetas: ingresos, EBITDA, margen EBITDA, beneficio neto, caja final.
- Delta vs año anterior: 2028 vs 2027 en Base: ingresos +6,6%, EBITDA +14,8%, beneficio +23,1%, caja +44,7%.

**Ingresos y EBITDA**

- Gráfico de barras (ingresos) + línea (EBITDA) para 36 meses.
- Tabla anual 2026–2028 con ingresos, EBITDA, margen.
- Lectura: "2026 arranca con rampa; 2027 absorbe el escalón de personal; 2028 amplía el margen."

**Caja y deuda**

- Línea de caja final y deuda viva, 36 meses.
- Tarjetas: caja mínima, payback, DSCR 2028, deuda viva 2028.
- Lectura: "La caja nunca baja de 23.245 € en Base; el mes más ajustado es febrero."

**Unit economics**

- Tabla de 8 productos: PVP, precio neto, coste, margen unitario, margen %, mix, ingresos 2028, % ingresos.
- Barras de margen por producto.
- Lectura: "El espresso tiene el mayor margen %; la bolsa de café, el mayor margen absoluto y el 14,3% de los ingresos."

**Dónde se va el dinero**

- Dona de 5 categorías: producto, personal, local, marketing, otros.
- Tabla con € y % de ingresos (Base 2026).
- Lectura: "Producto 34,5% + personal 28,7% = 63,2% de cada euro."

**Punto de equilibrio**

- Bullet chart: 0 → 400 tickets/día; marcador de BE total 285, BE EBITDA 254, real 342.
- Tarjetas: margen de seguridad 16,7%, contribución/ticket 2,25 €, costes fijos 178.620 €.
- Lectura: "Puedes perder 57 tickets/día antes de entrar en pérdidas contables."

**El modelo completo**

- Tabs "Anual" / "Mensual".
- Anual: filas de P&L (ingresos, COGS, margen bruto, personal, opex, EBITDA, D&A, EBIT, intereses, EBT, impuestos, neto) × 2026/2027/2028.
- Mensual: 36 columnas con scroll horizontal; mismas filas; sticky first column.
- Botón "Descargar CSV" opcional; no requerido.

**Laboratorio**

- Ver 9.5.

**Aprende**

- 3 tarjetas: "Lee una cuenta de resultados", "Calcula tu punto de equilibrio", "Separa beneficio y caja".
- CTA "Abrir la guía".

**Descarga**

- Botón "Descargar el Excel" → `./assets/Cafeteria-Aurora-Modelo-Financiero.xlsx`.
- Enlace al repo.
- Metodología: "Los supuestos y las fórmulas están en docs/project-brief.md".
- Aviso: "Modelo educativo; no es asesoramiento financiero."

### 9.4 Selector de escenario y año

- Estado por defecto: `base`, año 2028.
- El selector es un grupo de botones con `aria-pressed`; teclado izquierda/derecha.
- El año se muestra como tabs 2026/2027/2028; en móvil, un `<select>`.
- Al cambiar de escenario, el laboratorio se resetea (para evitar overrides invisibles); se avisa con un toast de 2 s.
- La URL refleja `?escenario=base&anio=2028` o hash; los enlaces son compartibles.
- No se recarga la página; se re-renderiza el DOM.

### 9.5 Laboratorio de supuestos

**Controles** (10):

| # | Control | Rango | Paso | Valor inicial | Efecto |
|---:|---|---:|---:|---:|---|
| 1 | Factor de demanda año 1 | 0,70–1,20 | 0,01 | escenario | Tickets/día, ingresos, COGS, marketing |
| 2 | Crecimiento anual de demanda | 0–10% | 0,5 pp | escenario | Años 2–3 |
| 3 | Crecimiento anual de precios | 0–6% | 0,1 pp | escenario | Ingresos y marketing variable |
| 4 | Inflación anual de costes | 0–8% | 0,1 pp | escenario | COGS desde 2027 |
| 5 | Factor de personal | 0,90–1,15 | 0,01 | escenario | Personal |
| 6 | Factor de alquiler | 0,90–1,15 | 0,01 | escenario | Alquiler |
| 7 | Inflación de servicios | 0–10% | 0,1 pp | escenario | Suministros y servicios |
| 8 | Marketing variable | 0–6% | 0,1 pp | escenario | Coste y contribución |
| 9 | Factor de otros gastos | 0,85–1,20 | 0,01 | escenario | Otros gastos |
| 10 | Crecimiento de otros gastos | 0–6% | 0,1 pp | escenario | Otros gastos años 2–3 |

**Comportamiento**:

- Al mover un control, se recalcula el escenario seleccionado con los overrides; los demás escenarios no cambian.
- Se muestra "Personalizado" y un delta vs el escenario base seleccionado.
- "Restablecer" vuelve a los valores del escenario.
- "Copiar enlace" codifica los overrides en el hash (`#lab=d:1.05,g:4.5,...`).
- Si la caja mínima < 10.000 € o el payback > 36, aparece un callout ámbar.
- Si el usuario cambia de escenario, los overrides se limpian.
- Debounce de 30 ms; cálculo <50 ms; sin parpadeo.

**Resultados**:

- 4 KPIs: ingresos 2028, EBITDA 2028, caja final 2028, payback proyecto.
- Un mini gráfico de EBITDA 2026–2028.
- Una frase de lectura generada: "Con estos supuestos, el negocio gana X € en 2028 y recupera la inversión en Y meses."

**Persistencia**: solo URL; no localStorage obligatorio. Si se usa, no debe ser la única forma de compartir.

### 9.6 Gráficos del sitio

| Sección | Tipo | Series | Notas |
|---|---|---|---|
| Ingresos y EBITDA | Barras + línea | Ingresos, EBITDA | 36 meses; tooltip; eje en k€ |
| Caja y deuda | Líneas | Caja final, deuda viva | 36 meses; banda de caja mínima |
| Unit economics | Barras horizontales | Margen unitario | 8 productos; orden por margen |
| Costes | Dona | 5 categorías | 5 porciones, no 8 |
| Punto de equilibrio | Bullet | BE EBITDA, BE total, real | 0–400 tickets/día |
| Comparativa | Barras agrupadas | Ingresos, EBITDA, neto | 3 escenarios, año activo |

**Reglas**: SVG inline, responsive `viewBox`, colores del design brief, ejes legibles, sin 3D, sin animaciones largas, tabla de datos en `<details>`, `aria-label` con el insight.

### 9.7 Arquitectura JavaScript

```
site/js/model.js   -> buildModel(inputs, scenarioKey, overrides) puro
site/js/charts.js  -> helpers SVG: line, bar, combo, donut, bullet
site/js/app.js     -> carga JSON, estado, render del dashboard, selector, lab
site/js/guide.js   -> calculadoras de la guía
site/data/model.json -> copia generada del JSON raíz
```

- `model.js` no toca el DOM; exporta `buildModel`, `annualSummary`, `SCENARIO_KEYS`.
- `app.js` usa `fetch('./data/model.json')`; si falla, muestra "Sirve el sitio por HTTP".
- Los tres escenarios se calculan al cargar; el lab recalcula solo el activo.
- Estado: `{ scenario, year, overrides }`; se sincroniza con la URL.
- Sin frameworks, sin build step para JS; el build solo copia y versiona.
- Los números se formatean con `Intl.NumberFormat('es-ES')`.

### 9.8 Contenido y copy

- Todo en español de España, tuteo, frases cortas.
- Cada sección tiene: título, subtítulo de una línea, gráfico/tabla, lectura de 1–2 frases.
- Los importes siempre con unidad y periodo.
- La guía se enlaza desde el dashboard y desde el footer.
- No se usan testimonios, logos de clientes ni cifras inventadas de mercado.

### 9.9 Accesibilidad, rendimiento y SEO

**Accesibilidad**

- `lang="es"`, skip link, foco visible, contraste ≥4,5:1.
- Botones de escenario con `aria-pressed`; tabs con roles; formularios con `<label>`.
- Gráficos con `role="img"`, `aria-label` y tabla alternativa.
- `prefers-reduced-motion`.
- Navegación completa con teclado; sin trampas de foco.

**Rendimiento**

- JS propio <100 KB minificado; CSS <30 KB; sin fuentes externas.
- SVG generado en el cliente; sin imágenes pesadas salvo el screenshot del README (no en la home).
- `loading="lazy"` en imágenes; `fetch` del JSON <50 KB.
- Objetivo Lighthouse: Performance ≥90, Accessibility ≥90, Best Practices ≥90, SEO ≥90 en móvil.

**SEO**

- `<title>` y `<meta name="description">` por página.
- Open Graph con título, descripción e imagen (`assets/og-image.png`, 1200×630).
- `canonical` a la URL de Pages.
- Encabezados semánticos; texto alternativo.
- `robots.txt` y `sitemap.xml` opcionales; no bloquean la entrega.

### 9.10 Despliegue

- GitHub Pages desde `main`, carpeta `/docs`.
- `docs/.nojekyll` para evitar procesamiento de Jekyll.
- Rutas relativas (`./css/...`, `./data/...`) para funcionar bajo `/analisis-financiero-cafeteria/`.
- `docs/404.html` con enlace a la home.
- El build copia `site/` a `docs/` sin borrar los Markdown de documentación (`project-brief.md`, `adr/`, `research/`, etc.).
- URL: `https://gerrcass.github.io/analisis-financiero-cafeteria/`.
- El README enlaza la URL y muestra la captura `docs/assets/screenshot-dashboard.png`.

### 9.11 Descarga del Excel

- Archivo: `docs/assets/Cafeteria-Aurora-Modelo-Financiero.xlsx`.
- Enlace con `download` y texto "Descargar el modelo (Excel, 10 hojas)".
- Peso objetivo: <500 KB.
- El archivo se genera en el build; no se edita a mano.
- Test e2e: el enlace responde 200, `Content-Type` de Excel o descarga, y el archivo abre con openpyxl.

### 9.12 Criterios de aceptación del sitio

1. Carga sin errores de consola y sin peticiones externas.
2. El selector de escenario actualiza KPIs, gráficos y tablas.
3. El laboratorio recalcula en <100 ms y muestra deltas.
4. La guía tiene los 10 capítulos, ejemplos, ejercicios y respuestas.
5. El enlace de descarga devuelve el `.xlsx` y el archivo es válido.
6. Funciona a 390, 768 y 1440 px sin scroll horizontal.
7. Teclado y lector de pantalla: flujo principal completo.
8. Lighthouse móvil ≥90 en Performance y Accessibility.
9. La URL de Pages funciona y el 404 enlaza a la home.
10. La captura del README existe y muestra el dashboard real.

---

## 10. Guía de aprendizaje

La guía completa está en `docs/education-outline.md` y se publica en `aprende.html`. Requisitos:

- **10 capítulos**: modelo, P&L, ingresos, COGS, costes fijos/break-even, personal, caja, deuda, escenarios, decisión.
- **Ejemplos con cifras reales** del escenario Base; cada cifra se puede reproducir con el modelo.
- **36 ejercicios** con respuesta razonada (3–4 por capítulo).
- **Glosario mínimo** de 12 términos y enlace al glosario completo.
- **Checklist de validación** de 20 puntos.
- **Notas para un taller de 90 minutos**.
- **Formato**: Markdown canónico en `docs/education-outline.md`; el build lo convierte a HTML para `aprende.html` con una plantilla, índice y calculadoras. No se duplica el texto a mano.
- **Tono**: didáctico, tuteo, sin jerga sin explicar; los errores comunes se nombran.
- **Exactitud**: las cifras de la guía deben coincidir con `expected.json`; un test busca los importes clave y falla si no aparecen.

---

## 11. Entregables y criterios de éxito

### 11.1 Entregables

| # | Entregable | Ruta | Criterio de aceptación |
|---:|---|---|---|
| 1 | Fuente de supuestos | `data/model.json` | JSON válido contra `data/schema.json`; suma de mix 100%, estacionalidad 12, días 312 |
| 2 | Esquema | `data/schema.json` | Valida el JSON; campos obligatorios y rangos |
| 3 | Objetivos dorados | `data/expected.json` | Generado por `scripts/model.py`; incluye 3 escenarios × 3 años |
| 4 | Motor Python | `scripts/model.py` | Reproduce `expected.json`; tests unitarios |
| 5 | Generador del libro | `scripts/build_workbook.py` | Crea el `.xlsx` con 10 hojas, fórmulas y 5 gráficos |
| 6 | Generador del sitio | `scripts/build_site.py` | Copia `site/` a `docs/` sin borrar Markdown; genera `aprende.html` |
| 7 | Libro | `docs/assets/Cafeteria-Aurora-Modelo-Financiero.xlsx` | Abre sin reparaciones; fórmulas recalculan; sin valores pegados |
| 8 | Sitio | `docs/index.html`, `docs/aprende.html`, `docs/404.html` | Funciona en Pages; sin errores de consola; responsive |
| 9 | CSS/JS | `site/css/styles.css`, `site/js/*.js` | Sin dependencias; <100 KB JS; tests Node |
| 10 | Guía | `docs/guia-finanzas.md` + `aprende.html` | 10 capítulos, 36 ejercicios, respuestas, glosario, checklist |
| 11 | README | `README.md` | Captura representativa, enlace a Pages, cómo regenerar, tests |
| 12 | Captura | `docs/assets/screenshot-dashboard.png` | 1440×900, dashboard real, sin chrome del navegador |
| 13 | Tests Python | `tests/test_model.py`, `test_workbook.py`, `test_golden.py` | Pasan en CI |
| 14 | Tests JS | `tests/js/model.test.js` | Pasan con `node --test` |
| 15 | Test e2e | `tests/e2e/site.spec.ts` | Playwright: carga, escenario, lab, descarga, móvil |
| 16 | CI | `.github/workflows/ci.yml` | Corre tests y verifica que `docs/` está actualizado |
| 17 | Marca | `assets/aurora-mark.svg`, `docs/assets/aurora-mark.svg` | SVG limpio, legible a 24 px, contraste |
| 18 | Documentación | `docs/project-brief.md`, `GLOSSARY.md`, `docs/adr/*`, `docs/research/benchmarks.md`, `docs/design-brief.md`, `docs/education-outline.md` | Coherente, en español, sin decisiones abiertas |

### 11.2 Criterios de éxito

1. **Fórmulas vivas**: el 100% de las celdas calculadas de escenarios y Resumen son fórmulas; cambiar un supuesto recalcula el libro.
2. **Cifras iguales**: libro, sitio y `expected.json` coinciden dentro de ±1 € / ±0,1 pp.
3. **Escenarios**: los tres existen, están ordenados y comparten estructura; el Pesimista es visible.
4. **Gráficos**: al menos 4 (se entregan 5) y todos apuntan a celdas vivas.
5. **Sitio**: dashboard, selector, detalle de producto/coste, laboratorio y guía; descarga funcional.
6. **Guía**: 10 capítulos, ejemplos con cifras reales, 36 ejercicios con respuesta, glosario y checklist.
7. **README**: captura representativa y enlace de despliegue.
8. **Calidad**: tests Python/Node/e2e verdes; sin `#REF!`, `#VALUE!`, `#DIV/0!`.
9. **Accesibilidad**: teclado, contraste, `aria`, responsive 390–1440 px.
10. **Reproducibilidad**: `make all` desde un clon limpio genera libro y sitio; CI detecta deriva.
11. **Honestidad**: supuestos documentados; Pesimista no maquillado; aviso de no asesoramiento.
12. **Rendimiento**: Lighthouse móvil ≥90 en Performance y Accessibility.

### 11.3 Puertas de calidad

| Puerta | Comando | Criterio |
|---|---|---|
| Modelo | `python -m pytest tests/test_model.py` | 100% verde |
| Golden | `python -m pytest tests/test_golden.py` | ±1 € / ±0,1 pp |
| Libro | `python -m pytest tests/test_workbook.py` | 10 hojas, fórmulas, checks, 5 gráficos |
| Recalc | `python scripts/recalc.py` o LibreOffice | Sin errores; cifras coinciden |
| JS | `node --test tests/js/model.test.js` | 100% verde |
| E2E | `npm run test:e2e` | Flujo completo, móvil, descarga |
| Deriva | `git diff --exit-code docs/` | Sin cambios sin commit |
| Accesibilidad | Lighthouse/axe | ≥90 o revisión manual documentada |
| Enlaces | `python scripts/check_links.py` | 0 enlaces rotos |

### 11.4 Definition of Done

- Todos los entregables de 11.1 existen en las rutas indicadas.
- `make all` funciona desde un clon limpio.
- `make test` pasa.
- El libro se abre en Excel y LibreOffice sin reparaciones.
- El sitio se ve correctamente en Pages y en local.
- El README explica qué es, cómo se usa y cómo se regenera.
- No hay decisiones abiertas en este brief.

### 11.5 README

El README debe incluir, en este orden:

1. **Título y una frase**: "Cafetería Aurora — modelo financiero interactivo de una cafetería de especialidad".
2. **Captura**: `docs/assets/screenshot-dashboard.png`, 1440×900, dashboard real con KPIs y selector; sin chrome del navegador; alt text.
3. **Enlace de despliegue**: `https://gerrcass.github.io/analisis-financiero-cafeteria/`.
4. **Qué es**: libro Excel con 10 hojas, 36 meses, 3 escenarios, sitio interactivo y guía.
5. **Qué incluye**: bullets de libro, dashboard, laboratorio, guía, tests.
6. **Cómo usarlo**: abrir el sitio, cambiar escenario, mover el laboratorio, descargar el Excel.
7. **Cómo regenerarlo**: comandos `make model`, `make workbook`, `make site`, `make test`; requisitos Python/Node.
8. **Estructura del repo**: árbol resumido.
9. **Supuestos clave**: 360 tickets/día, 132.000 € capex, 70.000 € deuda, 90.000 € equity; enlace al brief.
10. **Tests y CI**: comandos y qué cubren.
11. **Aviso**: modelo educativo, no asesoramiento financiero.

La captura se genera con Playwright (`scripts/make_screenshot.py`) después de `make site`; no se inventa ni se recorta de una diapositiva.

---

## 12. No objetivos

Quedan explícitamente fuera de alcance:

- **Balance de situación completo** y estado de flujos de efectivo contable formal. El modelo es P&L + caja + deuda.
- **Liquidación de IVA** (Modelo 303), plazos de Hacienda y tesorería de IVA. Se trabaja en neto.
- **Detalle de nóminas**: IRPF, contratos, bonificaciones, bajas, horas extras, convenio por provincia.
- **Modelo semanal o diario**; la granularidad es mensual.
- **Multi-local, franquicia, wholesale** más allá de la bolsa de grano retail.
- **Valoración de empresa** (DCF, múltiplos), cap table, dividendos, ampliaciones.
- **Leasing, IFRS 16, subvenciones, ayudas públicas, financiación alternativa**.
- **Backend, login, pagos, base de datos, analítica, CMS**.
- **Integración con TPV** o datos reales en tiempo real.
- **Internacionalización**; el contenido es español.
- **Modo oscuro** y app móvil nativa; no son necesarios para el encargo.
- **Asesoramiento fiscal, legal o de inversión**.

Si alguna de estas necesidades aparece, se abre un proyecto nuevo; no se improvisa dentro de este modelo.

---

## 13. Riesgos y mitigaciones

| Riesgo | Prob. | Impacto | Mitigación | Disparador |
|---|---|---|---|---|
| Demanda por debajo del plan | Media | Alto | Escenario Pesimista, rampa conservadora, prueba de demanda de 2 semanas, marketing local | 3 meses con tickets ≥10% bajo plan |
| Inflación del café | Alta | Medio | Contratos a 6 meses, dos orígenes, ajuste de PVP 2 veces/año, cobertura parcial | Coste >5% interanual |
| Presión salarial / convenio | Media | Alto | Plan FTE, polivalencia, factor 1,03 en Pesimista, revisión anual | Personal >32% de ingresos |
| Alquiler y renovación | Media | Medio | Negociar 5+5, factor 1,05, cláusula de IPC | Revisión >3% o subida >10% |
| Desviación de capex | Media | Alto | 10% de contingencia, 3 presupuestos, compra por fases | Desviación >10% |
| Subida de tipos | Baja | Medio | Tipo fijo 7,5%, colchón de caja, DSCR >1,5 en Base | +100 pb |
| Error de fórmula en Excel | Media | Medio | Tests, auditoría de fórmulas, recalculación, plantilla única | `#REF!`, `#VALUE!`, `#DIV/0!` |
| Deriva entre libro y sitio | Media | Alto | Fuente única JSON, `expected.json`, CI, `git diff` | Cifras distintas |
| Rutas de GitHub Pages | Baja | Bajo | Rutas relativas, `.nojekyll`, e2e bajo subpath | 404 en CSS/JSON |
| `fetch` bloqueado en `file://` | Baja | Bajo | Servir por HTTP; mensaje claro | JSON no carga |
| Sobrepromesa al inversor | Media | Alto | Publicar Pesimista, supuestos y aviso; no hardcodear | ROI prometido > modelo |
| Fatiga de mantenimiento | Media | Bajo | Documentación, tests, un solo JSON, build reproducible | Cambios manuales en `.xlsx` |
| Sesgo del modelo | Media | Alto | Revisión de supuestos con benchmarks, prueba de demanda, escenario de estrés | Resultado “demasiado bueno” sin evidencia |
| Plazo de implementación | Media | Medio | Fases con DoD, priorizar libro y sitio, guía después | Bloqueo >2 días en una fase |

---

## 14. Plan de implementación

### 14.1 Fases

| Fase | Objetivo | Tareas | DoD |
|---|---|---|---|
| 0 | Datos y motor | `model.json`, `schema.json`, `model.py`, `expected.json`, tests unitarios | JSON válido; Python reproduce los objetivos dorados |
| 1 | Libro | `build_workbook.py`, plantilla de escenarios, fórmulas, gráficos, checks | 10 hojas; recalc; sin valores pegados; 5 gráficos |
| 2 | Sitio | `model.js`, `charts.js`, `app.js`, dashboard, selector | Paridad JS/Python; dashboard responsive |
| 3 | Laboratorio y guía | `lab.js`, `guide.js`, `aprende.html`, `guia-finanzas.md` | 10 capítulos; 10 controles; ejercicios |
| 4 | Calidad | Playwright, CI, screenshot, README | Tests verdes; captura; enlace |
| 5 | Despliegue | Pages, verificación pública, tag | URL pública; 404; descarga |

### 14.2 Dependencias

- Fase 1 depende de 0.
- Fase 2 depende de 0; puede ir en paralelo con 1 si hay dos personas.
- Fase 3 depende de 2.
- Fase 4 depende de 1, 2 y 3.
- Fase 5 depende de 4.

### 14.3 Estructura de archivos objetivo

```
.
├── AGENTS.md
├── GLOSSARY.md
├── README.md
├── Makefile
├── package.json
├── requirements.txt
├── assets/
│   ├── icon.svg
│   └── aurora-mark.svg
├── data/
│   ├── model.json
│   ├── schema.json
│   └── expected.json
├── docs/
│   ├── index.html
│   ├── aprende.html
│   ├── 404.html
│   ├── .nojekyll
│   ├── css/styles.css
│   ├── js/{model,charts,app,guide}.js
│   ├── data/model.json
│   ├── assets/
│   │   ├── Cafeteria-Aurora-Modelo-Financiero.xlsx
│   │   ├── screenshot-dashboard.png
│   │   ├── og-image.png
│   │   └── aurora-mark.svg
│   ├── project-brief.md
│   ├── design-brief.md
│   ├── education-outline.md
│   ├── guia-finanzas.md
│   ├── research/benchmarks.md
│   ├── adr/0001..0003.md
│   └── agents/...
├── scripts/
│   ├── model.py
│   ├── build_workbook.py
│   ├── build_site.py
│   ├── recalc.py
│   ├── make_screenshot.py
│   └── check_links.py
├── site/
│   ├── index.html
│   ├── aprende.html
│   ├── 404.html
│   ├── css/styles.css
│   ├── js/{model,charts,app,lab,guide}.js
│   ├── data/model.json
│   └── assets/...
└── tests/
    ├── test_model.py
    ├── test_golden.py
    ├── test_workbook.py
    ├── js/model.test.js
    └── e2e/site.spec.ts
```

### 14.4 Comandos objetivo

```bash
make model       # data/model.json -> expected.json + validación
make workbook    # expected.json -> docs/assets/...xlsx + auditoría
make site        # site/ + guía -> docs/
make test        # pytest + node --test + playwright
make check       # fórmulas, enlaces, deriva, recalc
make all         # model + workbook + site + test
```

### 14.5 Riesgos de ejecución y orden

- **Primero el motor, luego el libro, luego el sitio.** Si el motor cambia, se regenera todo.
- **No empezar por el diseño visual** hasta que los números estén congelados; el diseño no debe ocultar un modelo mal calibrado.
- **No escribir la guía con cifras a mano** hasta que `expected.json` esté estable; después, generar y testear.
- **No tocar el `.xlsx` generado**; si hace falta un cambio, se cambia la plantilla o el JSON.

---

## 15. Anexos

### A. Forma de `expected.json`

```json
{
  "meta": {
    "version": "1.0",
    "generatedAt": "2026-10-25",
    "tolerance": { "eur": 1, "pp": 0.1 }
  },
  "scenarios": {
    "pessimistic": {
      "annual": {
        "2026": {
          "revenue": 338288.50,
          "cogs": 116695.39,
          "grossProfit": 221593.11,
          "personnel": 113773.80,
          "opex": 77122.00,
          "ebitda": 30697.54,
          "depreciation": 16625.00,
          "ebit": 14072.54,
          "interest": 4843.46,
          "ebt": 9229.08,
          "tax": 2307.27,
          "netIncome": 6921.81,
          "closingCash": 34874.52,
          "ticketsPerDay": 300.91,
          "averageTicketNet": 3.60,
          "breakEvenEbitda": 257.91,
          "breakEvenTotal": 287.98,
          "dscr": 1.69
        },
        "2027": {},
        "2028": {}
      },
      "paybackProjectMonths": null,
      "paybackEquityMonths": null,
      "cumulativeFcfe": 10998.77,
      "cashOnCash": 0.122
    },
    "base": {},
    "optimistic": {}
  }
}
```

**Nota**: `null` en payback significa `">36"`; el sitio y el libro lo muestran como texto. Los importes se guardan con 2 decimales; la presentación redondea.

### B. Checklist de auditoría de fórmulas

- [ ] Las 3 hojas de escenario tienen exactamente las mismas fórmulas normalizadas.
- [ ] `B3` es el único selector de escenario de cada hoja.
- [ ] Todas las filas 12–56 son fórmulas (salvo etiquetas y B3/B4).
- [ ] Las filas 76–107 del resumen anual son fórmulas.
- [ ] Las tablas de producto 116–149 son fórmulas.
- [ ] El Resumen no contiene importes pegados; solo referencias y `CHOOSE`.
- [ ] Los 5 gráficos apuntan a rangos con celdas, no a imágenes.
- [ ] No hay enlaces externos ni `#REF!`.
- [ ] Los nombres definidos resuelven.
- [ ] La cuota del préstamo usa `PMT`.
- [ ] El impuesto usa la cuota anual /12.
- [ ] El payback usa `TotalCapex+WC0` y `Equity`.
- [ ] La caja final = caja inicial + FCFE.
- [ ] El FCFE = FCFF − intereses + escudo − principal.
- [ ] El COGS usa coste ajustado por merma.
- [ ] El personal usa coste empresa (con SS).
- [ ] La estacionalidad suma 12 y los días 312.
- [ ] El mix suma 100%.
- [ ] Los escenarios están ordenados.
- [ ] La recalculación no produce errores.

### C. Decisiones abiertas

**Ninguna.** La matriz de escenarios, el catálogo, el plan de personal, el capex, el préstamo, la fiscalidad y el diseño están congelados a fecha 25/10/2026. Cualquier cambio se registra como una nueva versión del brief y obliga a regenerar los objetivos dorados.

### D. Referencias internas

- `GLOSSARY.md`: vocabulario de dominio.
- `docs/adr/0001-modelo-mensual-36-meses.md`: horizonte y granularidad.
- `docs/adr/0002-fuente-unica-supuestos-y-libro-generado.md`: JSON como fuente de verdad.
- `docs/adr/0003-sitio-estatico-github-pages.md`: sitio sin backend.
- `docs/research/benchmarks.md`: fuentes y supuestos.
- `docs/design-brief.md`: dirección visual.
- `docs/education-outline.md`: guía completa.
- `AGENTS.md`: expectativas del repositorio.

---

**Fin del brief.** La implementación puede empezar por la fase 0 sin preguntas adicionales.

