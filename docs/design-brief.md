# Brief de diseño — Cafetería Aurora

## 1. Idea visual

**Un cuaderno de café, no un dashboard de banco.** El sitio y el libro deben sentirse como la libreta de una cafetería de especialidad: papel crema, tinta espresso, terracota de taza y verde salvia de planta. La precisión financiera se muestra con tipografía editorial, números grandes y espacio en blanco; no con efectos, degradados ni jerga.

La marca es **Aurora**: luz de amanecer, comienzo, calma. El diseño debe transmitir **claridad, oficio y honestidad**, no lujo ni exclusividad. El pesimista se muestra con la misma dignidad que el base: el modelo no es marketing.

## 2. Principios

1. **Una idea por sección.** Cada bloque responde a una pregunta: ¿cuánto gano?, ¿dónde se va?, ¿qué pasa si?
2. **El número primero.** El KPI manda; el gráfico lo explica; el texto lo interpreta.
3. **Color con propósito.** Terracota para la marca y lo accionable; salvia para lo positivo; rojo para lo negativo; dorado solo como acento.
4. **Movimiento calmado.** Nada rebota ni cuenta hacia arriba durante segundos. Las transiciones ayudan a seguir el cambio, no a lucirse.
5. **Honestidad visual.** Los escenarios se ven todos; el Pesimista no se esconde en un desplegable.
6. **Didáctico sin infantilizar.** Se explica el concepto y se muestra la fórmula, sin tono de profesor condescendiente.

## 3. Paleta

| Token | Hex | Uso | Contraste |
|---|---|---|---|
| `--cream` | `#F7F1E7` | Fondo principal | Base |
| `--paper` | `#FFFDF9` | Tarjetas, tablas, gráficos | — |
| `--espresso` | `#2B1D16` | Texto principal, cabeceras, footer | 12:1 sobre cream |
| `--ink` | `#1C1917` | Texto de cuerpo alternativo | 13:1 sobre cream |
| `--terracotta` | `#C4623B` | Acento, líneas de gráfico, títulos grandes | 3,6:1 sobre cream; solo texto grande (≥24 px) y componentes |
| `--terracotta-strong` | `#A94E2C` | Botones, enlaces, foco | 4,9:1 con cream |
| `--sage` | `#7C8B6F` | Series positivas, fondos suaves | 3,2:1; no usar en texto pequeño |
| `--sage-strong` | `#5E6B52` | Texto positivo, etiquetas | 5,0:1 sobre cream |
| `--gold` | `#C9A227` | Acento, subrayados, highlight | 2,2:1; solo decorativo |
| `--gold-strong` | `#806410` | Texto de acento | 5,0:1 sobre cream |
| `--muted` | `#6F6259` | Texto secundario | 5,2:1 sobre cream |
| `--line` | `#E4D8C8` | Bordes, separadores, grid | — |
| `--negative` | `#A33A2B` | Pérdidas, alertas | 4,8:1 sobre cream |
| `--negative-bg` | `#F8E7E2` | Fondo de alerta | — |
| `--positive-bg` | `#EAF0E6` | Fondo de check | — |

**Reglas de color**

- El texto de cuerpo siempre en `--espresso` o `--ink`; nunca en `--gold` ni `--sage`.
- La terracota de marca (`#C4623B`) se usa en títulos ≥24 px, botones con fondo `--terracotta-strong`, líneas de gráfico y acentos. No en párrafos.
- Los estados positivos/negativos se acompañan siempre de texto o icono, no solo de color.
- Los gráficos usan máximo tres colores por gráfico: terracota, salvia y espresso; el dorado solo para un punto de referencia.

## 4. Tipografía

**Display:** `"Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif`.  
**Texto:** `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`.  
**Datos y fórmulas:** `"SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace`, con `font-variant-numeric: tabular-nums`.

No se cargan fuentes externas: el sitio debe funcionar sin red y sin dependencias. La pareja serif/sans da el aire editorial sin coste de rendimiento.

| Rol | Tamaño | Peso | Line-height | Uso |
|---|---:|---:|---:|---|
| Hero | `clamp(2.75rem, 6vw, 4.5rem)` | 600 | 1.05 | Titular de portada |
| H1 | 2.25rem / 36px | 600 | 1.15 | Título de página |
| H2 | 1.75rem / 28px | 600 | 1.2 | Sección |
| H3 | 1.25rem / 20px | 600 | 1.3 | Subsección, tarjeta |
| Body | 1rem / 16px | 400 | 1.6 | Párrafos |
| Small | 0.875rem / 14px | 400 | 1.5 | Notas, pies |
| Label | 0.6875rem / 11px | 600 | 1.2 | Etiquetas mayúsculas, tracking 0.08em |
| KPI | `clamp(2rem, 4vw, 3rem)` | 600 | 1.0 | Cifra principal |
| Table | 0.875rem / 14px | 400/600 | 1.4 | Tablas |

**Detalles**

- Cifras con `font-variant-numeric: tabular-nums` para que las columnas no bailen.
- Títulos con `letter-spacing: -0.02em`; etiquetas mayúsculas con `+0.08em`.
- No usar más de tres tamaños distintos en una misma tarjeta.
- Los importes en euros usan formato español: `384.419 €`, coma decimal, punto de miles. En el código, `Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })`.

## 5. Layout y grid

- Ancho máximo: **1180 px**; padding lateral 24 px (16 px en móvil).
- Grid de 12 columnas, gutter 24 px; las tarjetas ocupan 3, 4, 6 o 12 columnas.
- Separación entre secciones: **80 px** desktop, **48 px** móvil.
- Escala de espaciado: 4, 8, 12, 16, 24, 32, 48, 64, 80 px.
- Cabecera sticky de 64 px, con fondo `rgba(247,241,231,.92)` y `backdrop-filter: blur(8px)`; en móvil se convierte en menú.
- Breakpoints: 480, 768, 1024, 1280 px.
- Las tarjetas tienen radio 12 px, borde 1 px `--line`, sombra suave `0 1px 2px rgba(43,29,22,.06), 0 8px 24px rgba(43,29,22,.04)`.
- Las tablas largas tienen scroll horizontal con la primera columna sticky; en móvil, degradado en el borde para indicar scroll.
- El dashboard usa una columna principal de 8 y una lateral de 4 para las secciones de gráfico + lectura; en móvil se apilan.

## 6. Componentes

### Cabecera

- Marca: mark de aurora + wordmark "Aurora" en display + "café de especialidad" en label.
- Navegación: Modelo · Escenarios · Laboratorio · Aprende · Descargar.
- CTA "Descargar Excel" con fondo `--espresso` y texto cream.
- Enlace al repo en el footer, no en la cabecera.

### Hero

- Fondo cream con una composición sutil de líneas de amanecer (SVG, opacidad 0.08) en la esquina superior derecha.
- Titular: "Un café se puede modelar. Y se puede tocar."
- Subtítulo: "36 meses, tres escenarios y todas las fórmulas a la vista. Así se ve la economía de una cafetería de especialidad en Zaragoza."
- Debajo, una tira de 5 KPIs del escenario activo: ingresos 2028, EBITDA, beneficio neto, caja final y payback.
- No usar foto de stock como fondo; si se usa fotografía, que sea propia y con tratamiento cálido, no genérica.

### Selector de escenario

- Control segmentado de tres botones: Pesimista · Base · Optimista.
- El activo tiene fondo `--espresso`, texto cream; los inactivos, borde `--line`, texto espresso.
- Debajo, una línea de contexto: "Base: el plan que se monitorea. Pesimista: el test de resistencia. Optimista: el caso de expansión."
- `aria-pressed` y navegación con flechas.

### Tarjeta KPI

- Label mayúscula, cifra grande, delta vs año anterior o vs Base, unidad.
- El delta positivo usa `--sage-strong` con una flecha; el negativo, `--negative`.
- Si el KPI es "payback", el valor es "34 meses" y el delta es "−4 vs Pesimista" (no aplica).
- No animar la cifra con contadores largos; un fade de 150 ms es suficiente.

### Tarjeta de gráfico

- Título, subtítulo de una línea, gráfico SVG, leyenda y una nota de lectura ("Diciembre concentra el 10,2% de los ingresos").
- El gráfico tiene `role="img"` y `aria-label` con el resumen; debajo, un `<details>` con la tabla de datos.
- Altura 320 px desktop, 240 px móvil.

### Tabla de producto

- Columnas: Producto, PVP, Precio neto, Coste, Margen, Mix, Ingresos 2028, % ingresos.
- La barra de margen se dibuja como una línea fina bajo el porcentaje, no como un gráfico aparte.
- Los productos se ordenan por ingresos, no por mix.
- La fila de totales es sticky y tiene fondo `--cream`.

### Laboratorio

- Dos columnas: controles a la izquierda, resultados a la derecha.
- Cada control: label, valor actual, input range, unidad y una nota de una línea ("Solo afecta a 2027-2028").
- Presets de escenario arriba; "Restablecer" a la derecha.
- Resultados: 4 KPIs (ingresos 2028, EBITDA 2028, caja 2028, payback) y un delta vs escenario seleccionado.
- Si la caja mínima baja de 10.000 € o el payback supera 36 meses, aparece un callout ámbar con texto, no solo color.
- El estado se refleja en la URL (`#lab=...`) para compartir; no se guarda en servidor.

### Callouts

- **Info**: fondo `--paper`, borde izquierdo 3 px `--terracotta`.
- **Advertencia**: fondo `--negative-bg`, borde izquierdo 3 px `--negative`, icono de alerta.
- **Check**: fondo `--positive-bg`, borde izquierdo 3 px `--sage-strong`, icono de check.
- Título en negrita, cuerpo de 2-3 líneas máximo.

### Footer

- Fondo `--espresso`, texto cream.
- Tres columnas: marca + descripción; enlaces (modelo, guía, descarga, repo); aviso ("Modelo educativo; no es asesoramiento financiero").
- Tipografía small; logo en negativo.

## 7. Gráficos

- **Barras** para comparar magnitudes entre categorías o escenarios; **líneas** para evolución mensual; **área** solo para caja acumulada; **dona** solo para 5-6 categorías de coste, nunca para 8 productos.
- Colores: ingresos `--terracotta`, EBITDA `--sage-strong`, beneficio neto `--gold-strong`, caja `--espresso`, costes `--muted`.
- Líneas de 2 px; puntos de 4 px solo en el último dato o en hitos; sin sombras ni 3D.
- Ejes: grid horizontal 1 px `--line`, sin grid vertical; etiquetas 11 px `--muted`; cero marcado con línea más fuerte.
- Formato de importes: `384 k€` en ejes para no saturar; tooltip con `384.419 €`.
- Títulos de gráfico en H3; subtítulo con el periodo y el escenario.
- Accesibilidad: `aria-label` con el insight principal, tabla de datos en `<details>`, no depender solo del color.
- En el libro, los gráficos usan la misma paleta y tipografía; el título incluye el escenario y el periodo.

## 8. Sistema visual del libro

### Hojas y pestañas

| Hoja | Color de pestaña | Rol |
|---|---|---|
| Portada | `#2B1D16` espresso | Identidad y guía de uso |
| Resumen | `#C4623B` terracota | KPIs, comparativa y gráficos |
| Supuestos | `#7C8B6F` salvia | Entradas de demanda, escenarios, financiación y fiscalidad |
| Productos | `#7C8B6F` salvia | Catálogo, precios, costes, mix y merma |
| Personal | `#7C8B6F` salvia | Roles, FTE, salarios y coste empresa |
| Costos | `#7C8B6F` salvia | Costes fijos, capex y mantenimiento |
| Pesimista | `#A33A2B` rojo | Modelo mensual del escenario de estrés |
| Base | `#C4623B` terracota | Modelo mensual del plan |
| Optimista | `#5E6B52` salvia oscura | Modelo mensual del caso de expansión |
| Aprende | `#C9A227` dorado | Guía y ejercicios |

### Convenciones de celda

- **Entrada**: fondo `#FFF4D6`, fuente `#1F4E79`, borde fino `#E4D8C8`. Solo en Supuestos, Productos, Personal, Costos y metadatos de Portada.
- **Cálculo**: fondo blanco, fuente espresso, sin borde. Toda celda calculada es una fórmula.
- **Check**: fondo verde `#E2EFDA` o rojo `#FCE4D6`, texto "OK"/"Revisar".
- **Nota**: cursiva, `--muted`, sin borde.
- **Cabecera de sección**: fondo `#C4623B`, texto cream, negrita, fila completa.
- **Cabecera de tabla**: fondo `#2B1D16`, texto cream, negrita, wrap.
- **Totales**: fondo `#F7F1E7`, borde superior 1 px espresso, negrita.

### Formatos numéricos

| Tipo | Formato | Ejemplo |
|---|---|---|
| Euros enteros | `#,##0 €` | 384.419 € |
| Euros con decimales | `#,##0.00 €` | 3,60 € |
| Porcentaje | `0.0%` | 16,0% |
| Tickets/día | `0.0` | 342,0 |
| Mes | `mmm-yy` | ene-26 |
| Fecha | `dd/mm/aaaa` | 01/01/2026 |
| Índice | `0.000` | 1,025 |

### Layout del libro

- Columnas: A concepto (42), B t0/nota (14), C–AL meses 1–36 (11), AM–AO totales anuales (13), AP total trienio (13).
- Filas 1–4: título, subtítulo, selector, nota.
- Filas 5–9: índice de mes, fecha, año, mes, días operativos.
- Filas 11–35: cuenta de resultados.
- Filas 37–49: caja y deuda.
- Filas 51–56: calendario de deuda.
- Filas 58–70: impuesto anual y pérdidas.
- Filas 74–95: resumen anual y payback.
- Filas 100–130: rentabilidad por producto.
- Congelar paneles en `C10`; repetir filas 1–9 al imprimir; orientación horizontal; ajustar a 1 página de ancho; sin líneas de cuadrícula.
- Ancho de impresión: A4 horizontal; escala 70–80%; encabezado con "Cafetería Aurora — Modelo 2026-2028" y pie con número de página.

### Gráficos del libro

- 5 gráficos en Resumen: ingresos/EBITDA, beneficio/caja, comparativa de escenarios, ingresos por producto, estructura de costes.
- Título 12 pt, ejes 10 pt, leyenda inferior, sin 3D, sin sombra.
- Colores: terracota, salvia, dorado, espresso, gris.
- Los rangos apuntan a celdas con fórmulas; nunca a imágenes.

## 9. Marca

- **Mark**: un sol naciente de tres rayos sobre la silueta de una taza, en monoline 2,5 px, terracota sobre cream. Debe leerse a 24 px y a 64 px.
- **Wordmark**: "Aurora" en display serif, con "café de especialidad" debajo en label sans, tracking 0.12em.
- **Favicon**: mark simplificado en 32×32, fondo espresso, sol cream.
- **Uso**: mark + wordmark en cabecera; mark solo en favicon y en el pie; no deformar, no rotar, no añadir sombras.
- **Archivo nuevo**: `assets/aurora-mark.svg`. El `assets/icon.svg` existente (teal, "AF") no representa la marca; se conserva hasta que la implementación cree el nuevo mark y actualice el README.

## 10. Tono y copy

- Español de España, tuteo, frases cortas, verbos concretos.
- Decir "coste", "beneficio", "caja", "ticket", "local", "plantilla". Evitar "costo", "utilidad", "efectivo" (salvo dinero físico), "sinergia", "disrupción", "empoderar".
- Explicar el término la primera vez: "EBITDA (el beneficio antes de amortizaciones, intereses e impuestos)".
- Los números siempre con unidad y periodo: "79.505 € de EBITDA en 2028", no "79.505 €".
- No prometer: "El modelo muestra", "si se cumple el escenario", "el riesgo está en".
- Microcopy del laboratorio: "Mueve un supuesto y mira qué pasa." "Los números no son promesas." "Si la caja baja de 10.000 €, el modelo te avisa."
- Evitar emojis en la interfaz; usar iconos SVG de 16/20 px.
- El pesimista se presenta como "test de resistencia", no como "el malo".

## 11. Movimiento

- Duración 150–250 ms; easing `cubic-bezier(.2,.7,.2,1)`.
- Al cambiar de escenario: fade de 150 ms en KPIs y transición de 300 ms en las líneas del gráfico.
- Al mover un slider: actualización inmediata (<50 ms), sin animación de la cifra.
- Respetar `prefers-reduced-motion: reduce`; en ese caso, sin transiciones.
- No usar parallax, autoplay ni contadores que retrasen la lectura.

## 12. Accesibilidad

- Contraste mínimo 4,5:1 para texto pequeño; 3:1 para texto grande y componentes.
- Foco visible de 2 px `--terracotta-strong` con offset 2 px.
- Skip link al contenido principal.
- Formularios con `<label for>`, no solo placeholder; los rangos muestran el valor numérico.
- Tabs con `role="tablist"`, `aria-selected`, flechas; o botones con `aria-pressed`.
- Gráficos con `role="img"`, `aria-label` y tabla de datos alternativa.
- Tablas con `<caption>`, `<th scope="col">`, cifras alineadas a la derecha.
- `lang="es"`; errores de formulario con `aria-live="polite"`.
- No transmitir información solo por color; usar texto, icono o patrón.

## 13. Responsive

- **390 px**: una columna; KPIs en 2×2; gráficos 240 px; tablas con scroll horizontal y primera columna sticky; menú hamburguesa; lab apilado.
- **768 px**: dos columnas para KPIs y tarjetas; gráficos 280 px; lab apilado; nav compacta.
- **1024 px**: grid de 12; KPIs en 4+1; lab en 2 columnas; gráfico principal a 8 columnas y lectura a 4.
- **1440 px**: max-width 1180; márgenes generosos; no estirar gráficos más allá de 720 px de ancho.
- Probar sin scroll horizontal en 390 px y con zoom de 200%.

## 14. Hacer / no hacer

**Hacer**

- Dejar respirar los números; una cifra grande por tarjeta.
- Usar una sola idea de color por sección.
- Etiquetar unidades y periodos.
- Mostrar el Pesimista con claridad.
- Citar los supuestos y enlazar al brief.
- Probar el sitio sin red y en móvil.

**No hacer**

- Gráficos 3D, sombras duras, degradados de arcoíris.
- Tartas de 8 porciones para el mix de producto; usar barras.
- Rojo/verde como única señal.
- Contadores animados que impiden leer.
- Fotos de stock genéricas de café.
- Tono de "hustle" o promesas de rentabilidad.
- Ocultar el escenario Pesimista en un desplegable.
