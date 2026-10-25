# Guía de aprendizaje — Cafetería Aurora

> **Para quién**: alguien que quiere entender finanzas de negocio desde cero, con un caso real y números que puede tocar.  
> **Qué vas a aprender**: a leer una cuenta de resultados, separar costes fijos y variables, calcular un punto de equilibrio, reconciliar beneficio y caja, entender una deuda y decidir con escenarios.  
> **Cómo se usa**: lee un capítulo, mira el ejemplo con el escenario Base, haz los ejercicios y comprueba la respuesta. Después abre el laboratorio del sitio y cambia un supuesto para ver qué pasa.

Este documento es el **guion completo** de la guía. La versión publicada en el sitio (`aprende.html`) desarrolla el mismo contenido con calculadoras interactivas; la versión de Excel (`Aprende`) ofrece un resumen con ejemplos vivos. Todas las cifras siguientes son del escenario **Base** y del modelo congelado en `docs/project-brief.md`; si cambias un supuesto, los números cambiarán y el modelo se recalculará.

## Mapa de la guía

| # | Capítulo | Pregunta que responde | Ejercicios |
|---|---|---|---|
| 1 | Qué es un modelo financiero | ¿Qué estoy mirando y qué no? | 3 |
| 2 | La cuenta de resultados | ¿De dónde sale el beneficio? | 4 |
| 3 | Ingresos, tickets y estacionalidad | ¿Cómo se genera la venta? | 4 |
| 4 | COGS, merma y margen bruto | ¿Cuánto cuesta lo que vendo? | 4 |
| 5 | Costes fijos y punto de equilibrio | ¿Cuánto tengo que vender para no perder? | 4 |
| 6 | Personal y productividad | ¿Cuánto cuesta el equipo? | 3 |
| 7 | De EBITDA a caja | ¿Por qué el beneficio no es la caja? | 4 |
| 8 | Deuda, intereses y DSCR | ¿Puedo pagar el préstamo? | 3 |
| 9 | Escenarios y sensibilidad | ¿Qué pasa si me equivoco? | 4 |
| 10 | Decidir con el modelo | ¿Invierto o no? | 3 |

**Convención de cifras**: euros sin IVA salvo que se indique "con IVA"; porcentajes con un decimal; tickets/día con un decimal. Las diferencias de ±1 € son de redondeo.

---

## Capítulo 1 — Qué es un modelo financiero y cómo leer Aurora

### Objetivo

Entender que un modelo financiero no es una bola de cristal: es un **mapa de decisiones** que conecta supuestos con consecuencias.

### Conceptos clave

- **Supuesto**: lo que eliges porque no lo sabes (demanda, precio, merma).
- **Dato**: lo que observas o contratas (alquiler, cuota del préstamo, IVA).
- **Fórmula**: la relación entre ambos; en Aurora, casi todo se calcula.
- **Escenario**: una combinación coherente de supuestos, no una predicción.
- **Tres vistas**: cuenta de resultados (¿gano?), caja (¿tengo dinero?) y deuda (¿puedo pagar?).

### La cadena del modelo

```
Supuestos → Tickets → Ingresos → COGS → Margen bruto
          → Personal + Opex → EBITDA → Amortización → EBIT
          → Intereses → EBT → Impuestos → Beneficio neto
          → Capital circulante + Capex + Deuda → Caja final
```

### Ejemplo con Aurora (Base, 2026)

| Métrica | Valor | Qué significa |
|---|---:|---|
| Ingresos netos | 384.419 € | Lo que factura el local, sin IVA |
| EBITDA | 61.658 € | Caja operativa antes de inversión, intereses e impuestos |
| Beneficio neto | 30.142 € | Lo que queda después de amortizar, pagar intereses e impuestos |
| Caja final | 57.456 € | Dinero disponible al cerrar 2026 |

Los cuatro números son distintos y los cuatro son correctos. Si solo miras ingresos, no sabes si el negocio gana; si solo miras beneficio, no sabes si hay caja; si solo miras caja, no sabes si el negocio es rentable.

### Error común

Creer que "modelo financiero" es sinónimo de "previsión de ventas". La previsión es una parte; el valor está en conectar esa previsión con costes, caja y deuda.

### Ejercicios

1. ¿Cuál de las cuatro cifras del ejemplo es una medida de caja operativa?
2. ¿Por qué el beneficio neto es menor que el EBITDA?
3. ¿Qué diferencia hay entre un escenario y una predicción?

### Respuestas

1. El EBITDA (61.658 €). No es caja libre todavía: faltan impuestos, inversión y capital circulante.
2. Porque al EBITDA se le restan la amortización (16.625 €), los intereses (4.843 €) y los impuestos (10.047 €): 61.658 − 16.625 − 4.843 − 10.047 = 30.143 € (redondeo).
3. Un escenario es una hipótesis coherente que se puede comparar con otras; una predicción afirma lo que va a pasar. Aurora no predice: prueba.

---

## Capítulo 2 — La cuenta de resultados

### Objetivo

Leer una cuenta de resultados de arriba abajo y saber qué decisión toca en cada línea.

### Conceptos clave

- **Ingresos netos**: PVP menos IVA. Es el dinero que se reconoce como ingreso.
- **COGS**: coste de los productos vendidos (café, leche, panadería, packaging, merma).
- **Margen bruto**: ingresos − COGS. Es lo que queda para pagar la estructura.
- **Opex**: alquiler, suministros, servicios, marketing y otros gastos.
- **EBITDA**: margen bruto − personal − opex. Mide la caja operativa antes de inversión y financiación.
- **Amortización**: reparto del capex; no es caja del periodo.
- **EBIT**: EBITDA − amortización.
- **Intereses**: coste de la deuda.
- **EBT**: EBIT − intereses.
- **Impuestos**: 25% de la base imponible positiva.
- **Beneficio neto**: EBT − impuestos.

### Fórmulas

```
Margen bruto = Ingresos netos − COGS
EBITDA = Margen bruto − Personal − Alquiler − Suministros − Servicios
         − Marketing fijo − Marketing variable − Otros gastos
EBIT = EBITDA − Amortización
EBT = EBIT − Intereses
Beneficio neto = EBT − Impuesto de sociedades
```

### Ejemplo con Aurora (Base, 2026)

| Línea | Importe | % ingresos |
|---|---:|---:|
| Ingresos netos | 384.419 € | 100,0% |
| COGS | 132.608 € | 34,5% |
| **Margen bruto** | **251.810 €** | **65,5%** |
| Personal | 110.460 € | 28,7% |
| Alquiler | 22.800 € | 5,9% |
| Suministros | 17.400 € | 4,5% |
| Servicios fijos | 9.360 € | 2,4% |
| Marketing fijo | 5.400 € | 1,4% |
| Marketing variable | 11.533 € | 3,0% |
| Otros gastos | 13.200 € | 3,4% |
| **Total opex + personal** | **190.153 €** | **49,5%** |
| **EBITDA** | **61.658 €** | **16,0%** |
| Amortización | 16.625 € | 4,3% |
| **EBIT** | **45.033 €** | **11,7%** |
| Intereses | 4.843 € | 1,3% |
| **EBT** | **40.189 €** | **10,5%** |
| Impuestos (25%) | 10.047 € | 2,6% |
| **Beneficio neto** | **30.142 €** | **7,8%** |

Lectura: de cada 100 € que entran, 34,50 € se van en producto, 28,70 € en personal, 5,90 € en alquiler y 16,00 € quedan como EBITDA. De esos 16 €, la amortización se lleva 4,30 €, los intereses 1,30 € y Hacienda 2,60 €; al final quedan 7,80 € de beneficio neto.

### Error común

Restar el capex del EBITDA. El capex no es un gasto del periodo: se activa y se amortiza. Si compras una máquina de 28.000 €, no reduces el EBITDA de ese año; reduces la caja y, con el tiempo, el beneficio vía amortización.

### Ejercicios

1. Calcula el margen bruto porcentual y el margen EBITDA porcentual.
2. Si el personal sube un 5% y todo lo demás no cambia, ¿cuál es el nuevo EBITDA y el nuevo beneficio neto?
3. ¿Qué línea de la cuenta de resultados no es una salida de caja del periodo?
4. Si el alquiler sube un 10%, ¿cuánto baja el beneficio neto?

### Respuestas

1. Margen bruto = 251.810 / 384.419 = 65,5%. Margen EBITDA = 61.658 / 384.419 = 16,0%.
2. Personal +5% = +5.523 €; EBITDA = 56.135 €; EBT = 34.666 €; impuesto = 8.667 €; beneficio neto = 26.000 € (redondeo).
3. La amortización (16.625 €). Es un gasto contable que reparte una inversión pasada; la salida de caja fue el capex.
4. Alquiler +10% = +2.280 €; EBT baja a 37.909 €; impuesto 9.477 €; beneficio neto 28.432 €; caída de 1.710 €.

---

## Capítulo 3 — Ingresos, tickets y estacionalidad

### Objetivo

Entender de dónde sale cada euro de venta y por qué un año no se reparte igual entre los meses.

### Conceptos clave

- **Tickets/día**: clientes que compran al día. En Aurora, 360 en régimen; la media de 2026 es 342 por la rampa.
- **Ítems por ticket**: 1,35. Un cliente puede llevarse un café y un croissant.
- **Mix**: reparto de unidades entre los 8 productos.
- **PVP vs precio neto**: el PVP incluye 10% de IVA; el modelo usa el neto.
- **Estacionalidad**: factores mensuales que suman 12. Agosto 0,72; diciembre 1,16.
- **Rampa**: 75% en enero, 82% en febrero, 88% en marzo, 93% en abril, 97% en mayo, 100% desde junio.

### Fórmula

```
Tickets/día(t) = 360 × factor_escenario × (1+crecimiento)^(año−1)
                 × estacionalidad(mes) × rampa(mes)
Tickets(t) = tickets/día × días_operativos(mes)
Ítems(t) = tickets × 1,35
Ingresos(t) = ítems × Σ(mix_i × PVP_i/(1+IVA_i)) × (1+precio)^(año−1)
```

### Ejemplo con Aurora (Base, 2026)

- Tickets/día medio: 342,0 (360 × rampa media 0,946 × ajuste de días).
- Tickets del año: 106.686.
- Ítems: 144.026.
- Precio neto ponderado: 2,6691 €.
- Ticket medio neto: 3,60 €; con IVA: 3,96 €.
- Ingresos: 106.686 × 1,35 × 2,6691 = 384.419 €.

Comparación mensual:

| Mes | Tickets/día | Ingresos | Por qué |
|---|---:|---:|---|
| Enero | 248,4 | 24.166 € | Rampa 75% + estacionalidad 0,92 |
| Febrero | 274,5 | 23.741 € | Rampa 82% + mes corto (24 días) |
| Agosto | 259,2 | 22.415 € | Estacionalidad 0,72 (vacaciones) |
| Diciembre | 417,6 | 39.123 € | Estacionalidad 1,16 + rampa 100% |

El mismo local, con el mismo precio, factura un 62% más en diciembre que en enero. Eso no es un error: es estacionalidad y rampa.

### Error común

Multiplicar tickets por el PVP medio con IVA. Si usas 3,96 € en vez de 3,60 €, inflas los ingresos un 10% y todo el modelo queda desviado. Otro error: usar la media anual para decidir la caja de enero; en enero el EBITDA es casi cero y en febrero negativo.

### Ejercicios

1. Si los tickets/día suben un 10%, ¿cuánto suben los ingresos de 2026?
2. Si el precio sube un 5% y la demanda no cambia, ¿cuánto suben los ingresos?
3. Si suben ambos (demanda +10% y precio +5%), ¿cuál es el ingreso aproximado?
4. ¿Por qué diciembre factura más que enero si el local es el mismo?

### Respuestas

1. +10% de tickets = +10% de ítems e ingresos: 384.419 × 1,10 = 422.861 € (+38.442 €).
2. 384.419 × 1,05 = 403.640 € (+19.221 €).
3. 384.419 × 1,10 × 1,05 = 444.004 € (+59.585 €).
4. Por la estacionalidad (1,16 vs 0,92) y porque en enero la rampa es del 75%; además diciembre tiene más días operativos que febrero.

---

## Capítulo 4 — COGS, merma y margen bruto

### Objetivo

Saber cuánto cuesta realmente lo que se vende y cómo la merma y la inflación erosionan el margen.

### Conceptos clave

- **Coste unitario**: lo que pagas al proveedor por unidad.
- **Merma**: parte que no se vende; se aplica al coste.
- **Coste ajustado**: coste / (1 − merma).
- **Inflación de costes**: se aplica una vez al año, desde 2027.
- **Mix**: cambiar el reparto de productos cambia el margen aunque las ventas no cambien.

### Fórmula

```
Coste ajustado_i = coste_i / (1 − merma_i)
COGS(t) = ítems × Σ(mix_i × coste_ajustado_i) × (1+inflación)^(año−1)
Margen bruto = ingresos − COGS
Margen bruto % = margen bruto / ingresos
```

### Ejemplo con Aurora (Base, 2026)

| Producto | PVP | Precio neto | Coste | Merma | Coste ajustado | Margen unitario | Margen % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Espresso | 1,70 € | 1,5455 € | 0,42 € | 4% | 0,4375 € | 1,1080 € | 71,7% |
| Flat white | 2,80 € | 2,5455 € | 0,72 € | 4% | 0,7500 € | 1,7955 € | 70,5% |
| Cappuccino | 2,60 € | 2,3636 € | 0,66 € | 4% | 0,6875 € | 1,6761 € | 70,9% |
| Latte | 2,90 € | 2,6364 € | 0,74 € | 4% | 0,7708 € | 1,8655 € | 70,8% |
| Cold brew | 3,40 € | 3,0909 € | 0,95 € | 5% | 1,0000 € | 2,0909 € | 67,6% |
| Croissant | 2,30 € | 2,0909 € | 0,82 € | 8% | 0,8913 € | 1,1996 € | 57,4% |
| Tostada | 3,90 € | 3,5455 € | 1,18 € | 6% | 1,2553 € | 2,2901 € | 64,6% |
| Bolsa 250 g | 10,50 € | 9,5455 € | 4,60 € | 2% | 4,6939 € | 4,8520 € | 50,8% |

- COGS 2026: 132.608 €.
- Margen bruto: 251.810 € (65,5%).
- Coste ajustado ponderado por ítem: 0,9207 €.
- COGS por ticket: 1,24 €.
- Margen bruto por ticket: 2,36 €.

El producto con mayor margen porcentual es el espresso (71,7%); el de mayor margen absoluto por unidad es la bolsa de café (4,85 €). El croissant tiene el margen más bajo (57,4%) pero genera tráfico y ticket. La bolsa de café es solo el 4% de las unidades, pero aporta el 14,3% de los ingresos de 2028.

### Error común

Aplicar la merma al precio en vez de al coste. Si un croissant cuesta 0,82 € y se merma el 8%, el coste de cada unidad vendida es 0,82 / 0,92 = 0,8913 €, no 0,82 × 1,08 = 0,8856 €. La diferencia parece pequeña, pero se acumula en 20.000 unidades.

### Ejercicios

1. ¿Cuál es el COGS de 2026 en porcentaje de ingresos?
2. Si la inflación de costes sube 1 punto en 2027 (de 3,5% a 4,5%), ¿cuánto sube el COGS de 2027?
3. Si la merma del croissant sube del 8% al 16%, ¿cuánto sube el coste de las unidades vendidas en 2026?
4. Si 5 puntos de mix se mueven de la bolsa de café al espresso, ¿qué pasa con el margen bruto?

### Respuestas

1. 132.608 / 384.419 = 34,5%.
2. El índice pasa de 1,035 a 1,045; el COGS de 2027 sube un 0,966%: 150.591 × 0,00966 = 1.455 €.
3. Coste ajustado pasa de 0,8913 a 0,82/0,84 = 0,9762 €; +0,0849 €/unidad × 20.164 unidades = +1.712 €.
4. Por cada ítem, ingresos bajan 0,05 × (9,5455 − 1,5455) = 0,40 €; COGS bajan 0,05 × (4,6939 − 0,4375) = 0,2128 €; margen bruto baja 0,1872 €/ítem × 144.026 = −26.960 €. Mover mix hacia productos baratos puede reducir el margen aunque vendas lo mismo.

---

## Capítulo 5 — Costes fijos, apalancamiento y punto de equilibrio

### Objetivo

Calcular cuántos tickets al día necesita Aurora para no perder dinero y entender por qué una caída pequeña de ventas puede golpear fuerte al beneficio.

### Conceptos clave

- **Coste fijo**: no cambia con cada ticket (alquiler, personal, seguros).
- **Coste variable**: cambia con cada ticket (COGS, marketing variable).
- **Contribución por ticket**: ingreso del ticket menos sus costes variables.
- **Punto de equilibrio**: tickets/día con los que el resultado es cero.
- **Apalancamiento operativo**: proporción de costes fijos; amplifica el efecto de la demanda.
- **Margen de seguridad**: distancia entre las ventas previstas y el equilibrio.

### Fórmula

```
Contribución/ticket = ingreso/ticket − COGS/ticket − marketing variable/ticket
Costes fijos de caja = personal + alquiler + suministros + servicios
                       + marketing fijo + otros gastos
BE EBITDA (tickets/día) = costes fijos de caja / contribución / días
BE total (tickets/día) = (costes fijos de caja + amortización + intereses)
                         / contribución / días
Margen de seguridad = (tickets/día previstos − BE total) / tickets/día previstos
```

### Ejemplo con Aurora (Base, 2026)

- Ingreso por ticket: 3,602 €.
- COGS por ticket: 1,243 €.
- Marketing variable por ticket: 0,108 €.
- Contribución por ticket: 2,251 €.
- Costes fijos de caja: 110.460 + 22.800 + 17.400 + 9.360 + 5.400 + 13.200 = 178.620 €.
- BE EBITDA: 178.620 / 2,251 / 312 = 254,2 tickets/día.
- BE total (añade 16.625 de amortización y 4.843 de intereses): 285,0 tickets/día.
- Tickets previstos: 342,0.
- Margen de seguridad: (342,0 − 285,0) / 342,0 = 16,7%.

Lectura: Aurora puede perder 57 tickets/día (16,7% de la demanda) antes de entrar en pérdidas contables. Si pierde 10% de demanda (34 tickets/día), el EBITDA cae de 61.658 € a 37.630 € (−39%), porque los costes fijos no bajan.

### Error común

Incluir el COGS en los costes fijos. El COGS es variable; si no vendes, no compras (o no deberías). Otro error: dividir los costes fijos entre los ingresos totales en vez de entre la contribución por ticket; el resultado sería un porcentaje sin sentido operativo.

### Ejercicios

1. Si el alquiler sube un 10%, ¿cuánto sube el punto de equilibrio?
2. Si el personal sube un 5%, ¿cuánto sube el punto de equilibrio?
3. Si la demanda cae un 10%, ¿cuál es el nuevo margen de seguridad?
4. ¿Por qué el punto de equilibrio total es mayor que el de EBITDA?

### Respuestas

1. Costes fijos +2.280 €; BE EBITDA = 180.900 / 2,251 / 312 = 257,6 tickets/día (+3,4). BE total = (180.900 + 21.468) / 2,251 / 312 = 288,1 (+3,1).
2. Costes fijos +5.523 €; BE EBITDA = 184.143 / 2,251 / 312 = 262,3 (+8,1). BE total = 292,8 (+7,8).
3. Tickets/día = 307,8; BE total 285,0; margen de seguridad = (307,8 − 285,0) / 307,8 = 7,4%.
4. Porque el punto de equilibrio total incluye la amortización (16.625 €) y los intereses (4.843 €), que no son costes de caja operativa pero sí reducen el beneficio.

---

## Capítulo 6 — Personal y productividad

### Objetivo

Entender el coste más grande y menos flexible del negocio, y cómo un cambio de FTE o de salario afecta al resultado.

### Conceptos clave

- **FTE**: equivalente a tiempo completo; 0,5 FTE es media jornada.
- **Salario bruto**: lo que se paga al empleado antes de IRPF y cotización del trabajador.
- **Cotización empresarial**: 31,5% adicional sobre el bruto.
- **Coste empresa**: salario bruto × (1 + 31,5%).
- **Crecimiento salarial**: 3,0% anual.
- **Factor de personal del escenario**: 1,03 en Pesimista, 1,00 en Base, 0,98 en Optimista.
- **Productividad**: ingresos por FTE; no mide horas ni calidad, solo una relación.

### Fórmula

```
Coste empresa anual = Σ(FTE_rol × salario_rol) × (1+SS) × (1+crecimiento)^(año−1)
Coste mensual = coste empresa anual / 12
% ingresos = coste personal / ingresos netos
Ingresos por FTE = ingresos netos / FTE
```

### Ejemplo con Aurora (Base)

| Rol | Salario bruto | FTE 2026 | FTE 2027 | FTE 2028 |
|---|---:|---:|---:|---:|
| Gerente | 30.000 € | 1,0 | 1,0 | 1,0 |
| Barista | 23.000 € | 1,0 | 1,5 | 1,5 |
| Ayudante de cocina | 21.000 € | 1,0 | 1,0 | 1,0 |
| Fin de semana | 20.000 € | 0,5 | 0,5 | 0,5 |
| **Total FTE** | | **3,5** | **4,0** | **4,0** |

- Masa salarial 2026: 30.000 + 23.000 + 21.000 + 10.000 = 84.000 €.
- Coste empresa 2026: 84.000 × 1,315 = 110.460 €.
- % ingresos: 110.460 / 384.419 = 28,7%.
- Ingresos por FTE: 384.419 / 3,5 = 109.834 €.
- Coste medio por FTE: 110.460 / 3,5 = 31.560 €.

2027: 4,0 FTE, coste 129.350 € (+17,1%), ingresos 432.330 € (+12,5%), personal 29,9% de ingresos. El escalón de 0,5 FTE del barista explica la mayor parte del aumento; el resto es el 3% de crecimiento salarial.

### Error común

Usar el salario neto en vez del bruto, u olvidar la cotización empresarial. Un barista de 23.000 € brutos no cuesta 23.000 €, cuesta 30.245 €. Otro error: añadir FTE sin ajustar el salario y la cotización; el modelo lo hace automáticamente, pero el plan de personal debe reflejar quién entra y cuándo.

### Ejercicios

1. Si el barista pasa a 2,0 FTE en 2028, ¿cuál es el nuevo coste de personal y el nuevo porcentaje sobre ingresos?
2. Si el crecimiento salarial fuera del 4% en 2027, ¿cuánto subiría el coste de personal?
3. ¿Qué significa que los ingresos por FTE sean 109.834 €? ¿Es mucho o poco?

### Respuestas

1. +0,5 FTE × 23.000 × 1,0609 × 1,315 = +16.043 €; personal 149.273 €; 149.273 / 460.864 = 32,4%.
2. 129.350 × (1,04/1,03) = 130.605 €; +1.255 €. El efecto es pequeño en un año, pero se acumula.
3. Que cada equivalente a tiempo completo genera 109.834 € de ingresos netos. Es una referencia; para juzgarla hay que comparar con locales similares, horas de apertura y mix de producto. No es una medida de esfuerzo ni de calidad.

---

## Capítulo 7 — De EBITDA a caja

### Objetivo

Reconciliar beneficio y caja, y entender por qué un negocio rentable puede quedarse sin liquidez.

### Conceptos clave

- **Amortización**: gasto no cash; se suma de vuelta.
- **Capital circulante**: inventario + cuentas por cobrar − proveedores. En Aurora es negativo (los proveedores financian).
- **Δ capital circulante**: cambio del capital circulante; si aumenta, consume caja; si baja, libera caja.
- **Capex de mantenimiento**: inversión recurrente para mantener el local; 1,5% de ingresos.
- **FCFF**: caja para todos los financiadores, antes de intereses y principal.
- **FCFE**: caja para el accionista, después de intereses, escudo fiscal y principal.
- **Escudo fiscal**: ahorro de impuestos por los intereses.

### Fórmula

```
FCFF = EBITDA − impuesto_teórico_sin_deuda − capex_mantenimiento − ΔWC
FCFE = FCFF − intereses + escudo_fiscal − principal
Caja final = caja inicial + FCFE
```

### Ejemplo con Aurora (Base, 2026)

| Concepto | Importe |
|---|---:|
| EBITDA | 61.658 € |
| Impuesto teórico sin deuda | −11.258 € |
| Capex de mantenimiento | −5.766 € |
| Δ capital circulante | +6.944 € |
| **FCFF** | **51.577 €** |
| Intereses | −4.843 € |
| Escudo fiscal | +1.211 € |
| Principal de deuda | −11.988 € |
| **FCFE** | **35.956 €** |
| Caja inicial | 21.500 € |
| **Caja final** | **57.456 €** |

Reconciliación por la vía del beneficio neto:

```
Beneficio neto 30.142
+ Amortización 16.625
− Capex mantenimiento 5.766
+ Liberación de circulante 6.944
− Principal 11.988
= FCFE 35.957 (1 € de redondeo)
```

El ΔWC es positivo porque el capital circulante pasa de +6.500 € (stock inicial) a −444 € (proveedores financian más que el stock). Es una liberación de caja de 6.944 €, no un ingreso.

### Error común

Decir "tengo 30.142 € de beneficio, luego tengo 30.142 € de caja". No: hay amortización que no es caja, capex que sí lo es, circulante que se mueve y deuda que se devuelve. En 2026, la caja sube 35.956 €, más que el beneficio, porque la amortización y la liberación de circulante compensan el capex y el principal.

### Ejercicios

1. Si el capex de mantenimiento fuera el 2% de ingresos en vez del 1,5%, ¿cuál sería la caja final?
2. Si el ΔWC fuera cero, ¿cuál sería la caja final?
3. Si el principal fuera 15.000 €, ¿cuál sería la caja final?
4. ¿Por qué se suma la amortización y se resta el capex?

### Respuestas

1. Capex 7.688 € en vez de 5.766 €; FCFE 34.034 €; caja final 55.534 €.
2. FCFE 29.012 €; caja final 50.512 €.
3. FCFE 32.944 €; caja final 54.444 €.
4. La amortización es un gasto contable que ya ocurrió como capex en el pasado; no vuelve a salir caja. El capex es la salida de caja real del periodo. Se suma la primera para llegar al beneficio cash y se resta el segundo para reflejar la inversión.

---

## Capítulo 8 — Deuda, intereses y DSCR

### Objetivo

Entender cómo funciona un préstamo francés, cuánto cuesta y cómo se mide la capacidad de pagarlo.

### Conceptos clave

- **Préstamo francés**: cuota constante; al principio se paga más interés y menos principal.
- **Tipo fijo**: 7,5% nominal anual; cuota mensual calculada con tipo mensual 0,625%.
- **Interés**: saldo vivo × tipo mensual.
- **Principal**: cuota − interés.
- **DSCR**: (EBITDA − impuestos) / (intereses + principal).
- **Escudo fiscal**: los intereses reducen la base imponible; el ahorro es tipo × interés (con matices de pérdidas).

### Fórmula

```
Cuota = PMT(tipo/12, meses, −préstamo)
Interés(t) = saldo_vivo(t−1) × tipo/12
Principal(t) = cuota − interés(t)
Saldo(t) = saldo(t−1) − principal(t)
DSCR(t) = (EBITDA(t) − impuestos(t)) / (intereses(t) + principal(t))
```

### Ejemplo con Aurora

- Préstamo: 70.000 €.
- Tipo: 7,5% nominal anual.
- Plazo: 60 meses.
- Cuota: 1.402,66 €/mes (16.831,88 €/año).
- Interés total del préstamo: 14.159 €.

| Año | Intereses | Principal | Saldo final | DSCR Base | DSCR Pesimista | DSCR Optimista |
|---|---:|---:|---:|---:|---:|---:|
| 2026 | 4.843 € | 11.988 € | 58.012 € | 3,07 | 1,69 | 3,91 |
| 2027 | 3.913 € | 12.919 € | 45.092 € | 3,39 | 1,35 | 4,78 |
| 2028 | 2.910 € | 13.922 € | 31.170 € | 3,83 | 1,17 | 5,79 |

Lectura: en Base, el EBITDA menos impuestos cubre 3,1 veces el servicio de la deuda en 2026; en Pesimista, 1,7 veces en 2026 y 1,17 en 2028. Si el banco exige un covenant de 1,2x, el Pesimista lo incumple en 2028. La deuda no es el problema principal en Base; el problema es la combinación de menos demanda y más costes.

### Error común

Dividir el EBITDA entre el saldo del préstamo. Eso mide apalancamiento, no capacidad de pago. El DSCR compara la caja operativa con **lo que hay que pagar cada año** (intereses + principal). Otro error: olvidar el principal; el interés es solo una parte de la cuota.

### Ejercicios

1. Si el tipo sube al 8,5%, ¿cuál es la nueva cuota y el DSCR de 2026 en Base?
2. Si el plazo se alarga a 7 años, ¿qué pasa con la cuota, los intereses totales y el DSCR?
3. ¿Qué harías si el DSCR del Pesimista baja de 1,2x?

### Respuestas

1. Cuota 1.436,16 €; intereses 2026 5.500 €; principal 11.734 €; DSCR = (61.658 − 10.047) / (5.500 + 11.734) = 2,99.
2. Cuota 1.073,68 € (−329 €/mes); intereses totales 20.189 € (+6.030 €); el DSCR sube porque el principal anual baja, pero pagan más intereses en total. Es un trade-off de liquidez vs coste.
3. Negociar una carencia de principal, ampliar el plazo, aportar equity o reducir capex/personal. El modelo permite probar el efecto antes de hablar con el banco; no se debe confiar en que el escenario Base se cumpla.

---

## Capítulo 9 — Escenarios y sensibilidad

### Objetivo

Usar escenarios para tomar decisiones robustas, no para elegir el futuro que más gusta.

### Conceptos clave

- **Matriz de escenarios**: 10 variables; todo lo demás es estructural y común.
- **Pesimista**: demanda 12% por debajo del plan, crecimiento 1,5%, precios +1,5%, costes +4,5%, personal 1,03, alquiler 1,05, servicios +6%, marketing 2%, otros 1,08/+3%.
- **Base**: demanda en plan, crecimiento 4%, precios +2,5%, costes +3,5%, personal 1,00, alquiler 1,00, servicios +4%, marketing 3%, otros 1,00/+2,5%.
- **Optimista**: demanda +8%, crecimiento 6%, precios +3,2%, costes +2,8%, personal 0,98, alquiler 0,96, servicios +3%, marketing 4%, otros 0,95/+2%.
- **Sensibilidad**: cambiar una variable y medir el efecto, manteniendo el resto.

### Fórmula

No hay una fórmula única: cada variable entra en su línea. La sensibilidad se calcula como:

```
ΔEBITDA = EBITDA(variable + Δ) − EBITDA(base)
```

### Ejemplo con Aurora (2028)

| Métrica | Pesimista | Base | Optimista |
|---|---:|---:|---:|
| Ingresos | 378.796 € | 460.864 € | 524.147 € |
| EBITDA | 19.713 € | 79.505 € | 123.323 € |
| Margen EBITDA | 5,2% | 17,3% | 23,5% |
| Beneficio neto | 134 € | 44.978 € | 77.841 € |
| Caja final | 32.499 € | 132.063 € | 200.325 € |
| DSCR | 1,17 | 3,83 | 5,79 |
| Payback proyecto | >36 meses | 34 meses | 25 meses |

Sensibilidad del EBITDA de 2026 en Base:

| Cambio | Δ EBITDA | Lectura |
|---|---:|---|
| Demanda −10% | −24.028 € | El más peligroso: los costes fijos no bajan |
| Demanda +10% | +24.028 € | El mismo efecto, al revés |
| Precio +5% (sin perder demanda) | +18.644 € | Muy potente, pero la elasticidad no se modela |
| Personal +5% | −5.523 € | El coste más grande y rígido |
| Alquiler +10% | −2.280 € | Importante, pero menor que personal |
| Marketing +1 pp | −3.844 € | Se come parte del margen; debe generar demanda |
| Inflación de costes +1 pp | 0 € en 2026; −1.455 € en 2027; −3.145 € en 2028 | El índice parte de 1,00 en 2026 |

La conclusión práctica: **la demanda y el precio mueven el resultado mucho más que el alquiler o el marketing**. Pero la demanda es lo que menos controlas; por eso el Pesimista es el escenario que decide si la inversión es resistente.

### Error común

Cambiar demanda y precio a la vez sin una historia que lo justifique. Si bajas la demanda y subes el precio, estás mezclando recesión con una subida de precios que probablemente no podrías aplicar. Otro error: usar el Optimista como presupuesto; el presupuesto debe ser el Base, y el Optimista una opción de crecimiento.

### Ejercicios

1. ¿Qué variable tiene más impacto por cada 1% de cambio: demanda, precio, personal o alquiler?
2. Si la demanda cae 10% y el precio sube 5%, ¿cuál es el EBITDA aproximado?
3. Si en 2027 el precio sube 1 punto y la inflación de costes sube 1 punto, ¿qué pasa con el EBITDA?
4. ¿Por qué el Pesimista tiene un margen EBITDA del 5,2% y no es negativo?

### Respuestas

1. Demanda: 10% → 39% de EBITDA. Precio: 5% → 30%. Personal: 5% → 9%. Alquiler: 10% → 3,7%. La demanda es la más potente, seguida del precio.
2. 61.658 − 24.028 + 18.644 = 56.274 € (aproximado; hay interacciones pequeñas).
3. Precio +1%: ingresos +4.323 €; marketing variable +130 €; EBITDA +4.193 €. Coste +1 pp: COGS +1.455 €. Efecto neto: +2.738 €.
4. Porque la demanda, aunque baja, sigue siendo positiva y el local cubre costes variables y parte de los fijos; el EBITDA es 19.713 €. Lo que casi desaparece es el beneficio neto (134 €), porque la amortización y los intereses se comen el margen.

---

## Capítulo 10 — Decidir con el modelo

### Objetivo

Convertir los números en una decisión: invertir, negociar o esperar.

### Conceptos clave

- **Payback**: meses para recuperar la inversión con la caja acumulada.
- **Payback proyecto**: usa FCFF y la inversión total (capex + circulante inicial = 138.500 €).
- **Payback equity**: usa FCFE y el equity aportado (90.000 €).
- **Cash-on-cash**: FCFE acumulado / equity.
- **DSCR**: capacidad de pagar la deuda.
- **Margen de seguridad**: colchón ante una caída de demanda.
- **Coste de oportunidad**: lo que podrías hacer con el dinero y el tiempo.

### Fórmula

```
Payback = primer mes en que la caja acumulada ≥ inversión
Cash-on-cash = FCFE acumulado / equity
Margen de seguridad = (tickets previstos − BE total) / tickets previstos
```

### Ejemplo con Aurora

| Métrica | Pesimista | Base | Optimista |
|---|---:|---:|---:|
| Payback proyecto | >36 meses | 34 meses | 25 meses |
| Payback equity | >36 meses | 30 meses | 22 meses |
| FCFE acumulado 3 años | 10.999 € | 110.563 € | 178.825 € |
| Cash-on-cash 3 años | 12,2% | 122,8% | 198,7% |
| Caja final 2028 | 32.499 € | 132.063 € | 200.325 € |
| DSCR 2028 | 1,17 | 3,83 | 5,79 |

Lectura: en Base, el accionista recupera los 90.000 € en 30 meses y acumula 110.563 € de FCFE en tres años, un 122,8% del equity aportado. En Pesimista, no recupera la inversión en 36 meses y el DSCR roza el covenant. En Optimista, recupera en 22 meses y acumula 178.825 € de FCFE, un 198,7% del equity.

### Criterios de decisión

1. **¿Aguantas el Pesimista?** Si la respuesta es no, no inviertas o negocia mejor alquiler/capex.
2. **¿El DSCR en Base es ≥1,5x con colchón?** En Aurora es 3,07; hay margen.
3. **¿El alquiler es ≤6% de ingresos?** En Base 2026 es 5,9%; justo en el límite.
4. **¿El personal es ≤30% de ingresos?** En Base 2026 es 28,7%; en 2027 sube a 29,9%.
5. **¿El margen de seguridad es ≥15%?** En Base 2026 es 16,7%; en Pesimista 2028 es 0%.
6. **¿La localización pasa una prueba de demanda de dos semanas?** El modelo no lo puede responder; hay que contar clientes.
7. **¿Puedes perder el equity sin cambiar tu vida?** Es una decisión personal, no financiera.

### Error común

Usar un solo número (payback, ROI o EBITDA) como respuesta. La decisión es un conjunto de condiciones; el modelo ayuda a verlas, no a sustituirlas. Otro error: comparar el payback del proyecto (34 meses) con el del equity (30 meses) y elegir el que parece mejor; miden cosas distintas.

### Ejercicios

1. ¿Por qué el payback del equity es menor que el del proyecto si el equity es menor que la inversión total?
2. ¿Qué tres condiciones pondrías para invertir en Aurora?
3. ¿Qué tendría que pasar para que decidieras no invertir?

### Respuestas

1. Porque el equity (90.000 €) es menor que la inversión total (138.500 €) y el FCFE incluye el efecto de la deuda. El payback del equity mide cuándo recuperas tu aportación; el del proyecto, cuándo se recupera toda la inversión.
2. Ejemplo: (a) el Pesimista no quiebra y cubre la deuda; (b) el alquiler no supera el 6% de ingresos; (c) la prueba de demanda de dos semanas confirma al menos 250 tickets/día en hora punta; (d) tienes 12 meses de colchón de caja; (e) el capex tiene un 10% de contingencia.
3. Ejemplo: que el Pesimista tenga DSCR <1,0, que el alquiler supere el 8% de ingresos, que la demanda real sea <250 tickets/día, que el capex se desvíe >15% o que el banco no financie más del 40%.

---

## Glosario mínimo

Estos son los 12 términos que más se usan en la guía. El glosario completo está en `GLOSSARY.md`.

| Término | Definición breve |
|---|---|
| Ticket | Una compra completa de un cliente en una visita. |
| Ítems por ticket | Productos vendidos por ticket; en Aurora, 1,35. |
| PVP | Precio con IVA; el modelo usa el neto. |
| COGS | Coste de los productos vendidos, incluida la merma. |
| Margen bruto | Ingresos − COGS. |
| EBITDA | Beneficio antes de intereses, impuestos, amortización y depreciación. |
| EBIT | EBITDA − amortización. |
| Capital circulante | Inventario + cobros − proveedores. |
| FCFF | Caja para todos los financiadores, antes de deuda. |
| FCFE | Caja para el accionista, después de deuda. |
| DSCR | Cobertura del servicio de la deuda. |
| Payback | Meses para recuperar la inversión. |

## Checklist de validación

Antes de confiar en una cifra del modelo, comprueba:

- [ ] El mix de producto suma 100%.
- [ ] La estacionalidad suma 12,00.
- [ ] Los días operativos suman 312.
- [ ] Los ingresos usan precio neto, no PVP con IVA.
- [ ] El COGS usa coste ajustado por merma, no coste bruto.
- [ ] El personal incluye cotización empresarial y FTE.
- [ ] El EBITDA no incluye amortización, intereses ni capex.
- [ ] El EBIT resta la amortización.
- [ ] El EBT resta los intereses.
- [ ] El impuesto se calcula sobre base positiva y compensa pérdidas.
- [ ] El capital circulante usa días de inventario y proveedor.
- [ ] El FCFF resta capex de mantenimiento y ΔWC.
- [ ] El FCFE resta intereses y principal, y suma el escudo fiscal.
- [ ] La caja final = caja inicial + FCFE.
- [ ] El préstamo cierra a cero en el mes 60.
- [ ] El payback usa la inversión correcta (proyecto vs equity).
- [ ] Los escenarios están ordenados: demanda/precio Pesimista < Base < Optimista; costes al revés.
- [ ] Los gráficos apuntan a celdas vivas, no a imágenes.
- [ ] Ninguna celda calculada tiene un número pegado.
- [ ] El sitio y el libro dan las mismas cifras.

## Notas para un taller de 90 minutos

1. **Minutos 0–10**: presenta Aurora y el problema: 132.000 € de capex, 70.000 € de deuda, 90.000 € de equity. Pregunta: ¿es una buena inversión?
2. **Minutos 10–30**: capítulo 2. Reparte la cuenta de resultados de 2026 y pide que marquen qué líneas son caja y cuáles no.
3. **Minutos 30–50**: capítulo 5. Calcula el punto de equilibrio en la pizarra y compara con 342 tickets/día. Pide un margen de seguridad.
4. **Minutos 50–70**: capítulo 9. Mueve el laboratorio: demanda −10%, precio +5%, personal +5%. ¿Qué decisión cambia?
5. **Minutos 70–85**: capítulo 10. Debate: ¿invertirías? ¿Qué condición te haría decir no?
6. **Minutos 85–90**: cierra con el checklist y la idea clave: el modelo no decide, ordena las decisiones.

## Respuestas consolidadas

Las respuestas están al final de cada capítulo. Si vas a usar la guía en un taller, no las imprimas en la primera hoja: deja que el alumno intente primero y compruebe después.

## Aviso

Esta guía es material educativo. No es asesoramiento financiero, fiscal ni de inversión. Los supuestos son ilustrativos y deben sustituirse por ofertas, contratos y datos reales antes de tomar una decisión.
