# Spec 001 — Modelo financiero Cafetería Aurora

> **Estado**: listo para implementación.
> **Contrato de supuestos, fórmulas y objetivos dorados**: [`docs/project-brief.md`](../project-brief.md).
> **Vocabulario**: [`GLOSSARY.md`](../../GLOSSARY.md).
> **Decisiones de arquitectura**: [`docs/adr/`](../adr/).

## Problem Statement

Una persona que quiere abrir una cafetería de especialidad necesita responder tres preguntas antes de comprometer 160.000 €: cuánto puede vender, cuánto le costará operar y cuándo recuperará la inversión. Las hojas de cálculo improvisadas suelen mezclar PVP con IVA, confundir beneficio con caja, esconder el escenario pesimista y convertir los resultados en valores pegados que dejan de responder cuando cambia un supuesto.

El proyecto también debe servir para aprender. Quien lo use necesita ver la lógica económica, no solo el resultado: de dónde sale cada euro, qué coste es fijo, qué pasa si la demanda cae un 10% y por qué una cafetería rentable puede quedarse sin caja.

## Solution

Entregar un modelo financiero reproducible de 36 meses para Cafetería Aurora con tres escenarios (Pesimista, Base, Optimista), un libro Excel con fórmulas vivas y gráficos, un sitio estático que permita explorar el modelo y un laboratorio de supuestos, y una guía didáctica de finanzas en español construida con las cifras reales del caso.

La fuente única de verdad es un contrato de supuestos legible por máquina. El libro, el sitio y los tests consumen ese contrato. Cambiar un supuesto en el contrato regenera el libro y el sitio; cambiar un supuesto de entrada en el libro recalcula todas las celdas dependientes sin pegar valores. Los tres canales deben mostrar las mismas cifras dentro de una tolerancia documentada.

## User Stories

1. Como fundadora, quiero cambiar tickets/día, precios o costes en una sola hoja de supuestos, para que todos los escenarios y el resumen se recalculen sin tocar fórmulas.
2. Como fundadora, quiero ver el resultado mensual de 36 meses, para detectar los meses de caja ajustada que un resumen anual esconde.
3. Como fundadora, quiero comparar Pesimista, Base y Optimista lado a lado, para entender el rango de resultados antes de invertir.
4. Como fundadora, quiero ver un escenario pesimista realista y no maquillado, para probar si el negocio sobrevive a una demanda más baja y a costes más altos.
5. Como fundadora, quiero ver el punto de equilibrio en tickets/día, para saber cuánto margen de seguridad tengo antes de perder dinero.
6. Como fundadora, quiero ver el payback del proyecto y del equity, para decidir si el retorno justifica el riesgo.
7. Como fundadora, quiero ver la caja final y la deuda viva mes a mes, para anticipar necesidades de liquidez.
8. Como fundadora, quiero ver el detalle de ventas por producto y su margen, para decidir precios, mix y carta.
9. Como fundadora, quiero ver el coste de personal por rol y año, para planificar contrataciones y entender su impacto.
10. Como fundadora, quiero ver el alquiler, los suministros y los servicios desglosados, para negociar el local con datos.
11. Como banco o inversor, quiero una hoja de resumen con KPIs, comparativa y gráficos, para evaluar el caso sin abrir las hojas de escenario.
12. Como banco o inversor, quiero que los gráficos apunten a celdas vivas, para que la evidencia cambie cuando cambien los supuestos.
13. Como banco o inversor, quiero ver DSCR, EBITDA, deuda y caja, para evaluar la capacidad de servicio de la deuda.
14. Como aprendiz de finanzas, quiero una guía que recorra la cadena de ticket a caja, para entender cómo se conectan las líneas del modelo.
15. Como aprendiz de finanzas, quiero ejemplos numéricos con las cifras de Aurora, para ver la fórmula aplicada y no solo la definición.
16. Como aprendiz de finanzas, quiero ejercicios con respuestas, para comprobar si he entendido antes de usar el modelo en otro negocio.
17. Como aprendiz de finanzas, quiero un glosario preciso, para no confundir EBITDA, EBIT, margen bruto, COGS y caja.
18. Como aprendiz de finanzas, quiero una lista de errores comunes, para evitar los fallos que invalidan un modelo.
19. Como aprendiz de finanzas, quiero una checklist de validación, para auditar un modelo propio.
20. Como usuaria del sitio, quiero cambiar de escenario y de año con un clic, para explorar el modelo sin descargar Excel.
21. Como usuaria del sitio, quiero ver KPIs, gráficos y tablas que se actualicen juntos, para mantener una lectura coherente.
22. Como usuaria del sitio, quiero un laboratorio de supuestos con sliders, para entender la sensibilidad del resultado antes de editar el Excel.
23. Como usuaria del sitio, quiero restablecer el laboratorio y comparar contra el escenario original, para no perder la referencia.
24. Como usuaria del sitio, quiero compartir un enlace con el escenario, el año y los supuestos del laboratorio, para discutir un caso con otra persona.
25. Como usuaria del sitio, quiero descargar el libro Excel desde el sitio, para trabajar con el modelo completo.
26. Como usuaria móvil, quiero que el dashboard y las tablas sean legibles y navegables en un teléfono, para consultar el modelo fuera del escritorio.
27. Como persona que usa lector de pantalla o teclado, quiero controles accesibles, foco visible y gráficos con descripción, para usar el sitio sin depender del ratón.
28. Como mantenedor, quiero regenerar libro y sitio desde el contrato de supuestos con un comando, para evitar divergencias.
29. Como mantenedor, quiero tests que comparen las cifras del libro, del sitio y de los objetivos dorados, para detectar derivas.
30. Como mantenedor, quiero tests que verifiquen que las celdas calculadas son fórmulas y que los gráficos apuntan a rangos vivos, para proteger la promesa central del producto.
31. Como mantenedor, quiero que la integración continua ejecute los tests y falle si el sitio o el libro están desactualizados, para que `main` sea siempre reproducible.
32. Como revisora de un pull request, quiero ver la captura del cambio y la salida de los tests, para aprobar con evidencia.
33. Como visitante del repositorio, quiero un README con una captura representativa y el enlace al sitio, para entender el proyecto en menos de un minuto.
34. Como visitante del repositorio, quiero que el libro y la guía estén enlazados desde el README, para acceder a los entregables sin buscar en carpetas.
35. Como responsable del proyecto, quiero que el sitio esté publicado en GitHub Pages, para compartir el modelo con un enlace público.

## Implementation Decisions

### Contrato de supuestos y motores

- Un único contrato de supuestos, validado contra un esquema, contiene identidad, calendario, días operativos, estacionalidad, rampa, catálogo, plan de personal, costes fijos, capex, financiación, fiscalidad, capital circulante y la matriz de escenarios.
- El contrato debe distinguir con claridad entradas, supuestos estructurales y metadatos. Los valores calculados no viven en el contrato.
- Un motor de referencia en Python implementa las fórmulas del brief y produce objetivos dorados versionados. Un motor espejo en JavaScript implementa la misma lógica para el navegador. Los dos consumen el mismo contrato y se comparan contra los objetivos dorados con tolerancia de ±1 € y ±0,1 pp.
- Las fórmulas se definen una vez en el brief y se replican en los dos motores con los mismos nombres de dominio. Cualquier divergencia es un fallo de test, no una decisión editorial.
- La matriz de escenarios tiene diez variables: factor de demanda, crecimiento de demanda, crecimiento de precios, inflación de coste de producto, factor de personal, factor de alquiler, inflación de servicios, marketing variable, factor de otros gastos y crecimiento de otros gastos. El resto de entradas es estructural y común a los tres escenarios.
- El orden económico se verifica: Pesimista < Base < Optimista en demanda y precio; Pesimista > Base > Optimista en costes, con la excepción documentada de marketing.
- Los impuestos usan una bolsa de pérdidas compensables y una provisión mensual igual a la cuota anual dividida entre doce. Se calcula una segunda cuota sobre EBIT (sin deuda) para separar FCFF, escudo fiscal y FCFE.
- La deuda es un préstamo francés con cuota constante calculada con `PMT`; intereses y principal se separan mes a mes. La caja inicial financia la apertura y no se trata como ingreso.

### Libro Excel

- El libro se genera con openpyxl desde el contrato de supuestos; nunca se edita a mano.
- Tiene diez hojas: Portada, Resumen, Supuestos, Productos, Personal, Costos, Pesimista, Base, Optimista y Aprende.
- Las hojas de escenario comparten exactamente la misma estructura de 36 columnas mensuales y columnas anuales. Las fórmulas se escriben una vez y se replican para los tres escenarios; cambiar una fórmula exige regenerar los tres.
- Las únicas celdas de entrada son las de Supuestos, Productos, Personal, Costos y los metadatos de Portada. El selector de escenario de cada hoja y el selector del Resumen son entradas controladas con validación.
- Todas las celdas calculadas de escenarios y Resumen son fórmulas. Las etiquetas, fechas y selectores son las únicas constantes.
- Se usan nombres definidos para los supuestos clave, para que las fórmulas sean legibles y auditables. Se evitan funciones no soportadas por la recalculación de validación.
- El Resumen contiene la comparativa de KPIs, el bloque de payback y retorno, la comparativa 2028, el block de datos de gráficos y cinco gráficos: ingresos/EBITDA mensuales del escenario activo, caja y deuda, comparativa de escenarios, mix de productos y estructura de costes. Todos los gráficos apuntan a celdas.
- Las hojas de escenario incluyen la cuenta de resultados mensual, la caja, el calendario de deuda, el impuesto anual con pérdidas, el resumen anual, el payback y la rentabilidad por producto.
- El libro incluye chequeos visibles de integridad (sumas, identidades, caja mínima, orden de escenarios) y formato condicional para márgenes y alertas.
- El libro se configura para recálculo completo al abrir. Se incluye un mecanismo de recalculación de validación y, si el entorno lo permite, se cachean valores para visores que no recalculan.
- La hoja Aprende es una guía resumida dentro del propio libro: cómo usarlo, mapa de hojas, fórmulas clave, glosario, preguntas de lectura y errores comunes. Sus ejemplos son fórmulas vivas que apuntan a las hojas de escenario.
- El estilo sigue la dirección visual del brief: papel crema, espresso, terracota y salvia; entradas resaltadas; cabeceras claras; formatos de euro y porcentaje; anchos de columna legibles; impresión configurada.

### Sitio y guía

- El sitio es estático y sin dependencias de runtime: HTML, CSS y JavaScript vanilla, gráficos SVG propios, sin CDN, sin fuentes externas, sin analytics.
- Tiene dos páginas: dashboard y guía. El dashboard incluye hero, selector de escenario y año, KPIs, ingresos/EBITDA, caja/deuda, unit economics, estructura de costes, punto de equilibrio, modelo completo, laboratorio, CTA de aprendizaje y descarga.
- El estado de escenario, año y laboratorio se refleja en la URL para que un enlace sea compartible. Cambiar de escenario resetea el laboratorio para evitar overrides invisibles y avisa con un mensaje breve.
- El laboratorio replica las diez variables de escenario y permite editar los supuestos clave. Muestra el delta frente al escenario original, restablece con un botón y nunca modifica el contrato fuente.
- La guía se genera desde un documento Markdown canónico con una plantilla, índice, navegación, calculadoras y glosario. No se duplica el texto a mano en HTML.
- La guía tiene diez capítulos, ejemplos con las cifras de Aurora, treinta y seis ejercicios con respuesta, un glosario y una checklist de validación. Incluye un taller de 90 minutos y notas para facilitar su uso.
- La descarga del libro apunta al artefacto generado y se verifica en el test de extremo a extremo.
- El diseño sigue el brief visual: papel crema, espresso, terracota, salvia; serif editorial para titulares, sans para interfaz; movimiento calmado; tono cálido y preciso.
- La accesibilidad es parte del producto: navegación por teclado, foco visible, contraste, etiquetas ARIA, gráficos con título y descripción textual, tablas con encabezados y alternativa móvil.
- El sitio se publica desde la carpeta `docs/` de `main` en GitHub Pages. La página principal y la guía deben funcionar con rutas relativas.
- La integración continua instala dependencias, ejecuta tests Python, tests Node y el test de extremo a extremo, regenera libro y sitio, y falla si hay deriva sin commitear.
- El README incluye una captura representativa, el enlace al sitio, el enlace al libro, cómo regenerar, cómo testear y el aviso de que es un modelo educativo.

### Decisiones de contenido

- El libro y el sitio deben mostrar el Pesimista con la misma claridad que el Base; no se esconde el riesgo.
- Las cifras de la guía y del sitio deben coincidir con los objetivos dorados. Un test busca los importes clave y falla si no aparecen.
- El IVA no se trata como ingreso: el catálogo muestra PVP con IVA y precio neto; el P&L trabaja en neto.
- El capex de mantenimiento es una salida de caja de inversión y no genera una capa adicional de amortización; la simplificación se documenta.
- No se modelan elasticidad precio-demanda, canibalización, estacionalidad por producto ni promociones. Se declaran como no objetivos.

## Testing Decisions

Un buen test verifica comportamiento externo, no detalles de implementación. Debe fallar cuando cambia una cifra, una fórmula, un escenario o una interacción visible para el usuario, y debe pasar cuando se refactoriza la estructura interna sin cambiar el comportamiento.

### Seams

1. **Seam principal — contrato de supuestos → resultados del modelo**: el mismo contrato alimenta el motor Python y el motor JavaScript. Los tests comparan ambos contra los objetivos dorados y contra invariantes económicas. Es el seam más alto y protege la promesa de reproducibilidad.
2. **Seam del libro — libro generado → valores recalculados**: se abre el libro generado y se recalculan las fórmulas con un motor de recalculación. Se comparan los valores con los objetivos dorados y se audita que las celdas calculadas sean fórmulas, que las hojas tengan la estructura esperada y que los gráficos apunten a rangos vivos. Es el seam que protege la promesa de "fórmulas vivas".
3. **Seam del sitio — sitio construido → DOM e interacciones**: se sirve el sitio construido y se comprueba carga, cambio de escenario, cambio de año, laboratorio, reset, URL compartible, descarga y responsive. Es el seam que protege la experiencia.
4. **Seam de contenido — guía Markdown → HTML publicado**: se comprueba que el HTML contiene los capítulos, ejemplos, ejercicios, glosario y checklist, y que las cifras clave aparecen.

### Tests de modelo

- Validación del contrato: mix suma 100%, estacionalidad suma 12, días operativos suman 312, fuentes = usos, orden de escenarios, rangos válidos.
- Tests unitarios de cada bloque: demanda, ingresos, COGS, personal, opex, EBITDA, deuda, impuestos con pérdidas, capital circulante, caja, break-even, payback.
- Tests de identidades: margen bruto = ingresos − COGS; EBITDA = margen bruto − opex − personal; EBIT = EBITDA − amortización; EBT = EBIT − intereses; neto = EBT − impuestos; caja final = caja inicial + FCFE; FCFE = FCFF − intereses + escudo − principal.
- Test de reconciliación de caja contra beneficio neto: `FCFE = beneficio neto + amortización − capex mantenimiento − ΔWC − principal`.
- Test de escenarios: los tres producen resultados finitos, ordenados y con el Pesimista visible; los valores coinciden con los objetivos dorados.
- Test de pérdidas: un caso sintético con EBT negativo comprueba que la bolsa de pérdidas se arrastra y que la cuota es cero.
- Test de sensibilidad: demanda ±10%, precio +5%, personal +5%, alquiler +10% y marketing +1 pp reproducen las sensibilidades documentadas.

### Tests del libro

- Abre el libro generado y verifica las diez hojas, los nombres definidos y la configuración de recálculo.
- Verifica que las celdas de entrada son las únicas constantes numéricas y que las celdas calculadas de los escenarios y el Resumen son fórmulas.
- Verifica que las tres hojas de escenario tienen la misma estructura de fórmulas normalizada.
- Verifica que el Resumen referencia celdas de los escenarios y que los cinco gráficos tienen referencias a rangos, no imágenes.
- Recalcula el libro y compara los valores anuales con los objetivos dorados. Si el motor de recalculación no soporta una función, se aísla en una lista explícita y se valida con una comprobación alternativa, sin relajar el resto.
- Verifica que no hay `#REF!`, `#VALUE!`, `#DIV/0!` ni celdas clave vacías.
- Verifica la hoja Aprende: contiene las secciones, los ejemplos y las fórmulas vivas.

### Tests del sitio

- Tests Node del motor JavaScript contra los objetivos dorados y los mismos invariantes que Python.
- Test de extremo a extremo: carga del dashboard, KPIs por defecto, cambio de escenario, cambio de año, actualización de gráficos/tablas, laboratorio, reset, URL compartible, descarga del Excel, navegación a la guía.
- Test responsive a 390 px y 1440 px, sin overflow horizontal no intencionado y con tablas legibles.
- Test de accesibilidad básica: foco visible, botones con `aria-pressed`, gráficos con título/descripción, contraste y navegación por teclado.
- Test de contenido: la guía contiene los diez capítulos, los ejercicios y las cifras clave; el README contiene el enlace y la captura.

### Tests de integración y CI

- Un comando regenera el libro y el sitio desde el contrato.
- CI ejecuta la validación del contrato, los tests Python, los tests Node, la auditoría del libro y el test de extremo a extremo.
- CI comprueba que los artefactos generados en el checkout coinciden con los commitados; si no, falla con un mensaje que indica regenerar.
- El test de extremo a extremo se ejecuta contra el sitio construido, servido localmente, con un navegador headless.

### Prior art

No hay código previo en el repositorio. El prior art es el contrato congelado en `docs/project-brief.md`: sus tablas de supuestos, fórmulas y objetivos dorados son la especificación ejecutable. Los tests deben citar las secciones del brief que verifican.

## Out of Scope

- Balance de situación completo, estado de flujos de efectivo contable y conciliación de IVA.
- Liquidación de IVA, retenciones de IRPF, nóminas, convenios colectivos y cotizaciones detalladas por trabajador.
- Valoración de la empresa (DCF, múltiplos), reparto de dividendos, ampliaciones de capital o refinanciación.
- Expansión a múltiples locales, franquicias, wholesale, e-commerce o líneas de negocio distintas.
- Elasticidad precio-demanda, promociones, canibalización y estacionalidad por producto.
- Datos de mercado en tiempo real, integraciones con TPV, contabilidad o banca.
- Backend, autenticación, base de datos, panel de administración o generación de Excel en el navegador.
- Asesoramiento financiero, fiscal o legal. El producto es educativo y debe declararlo.

## Further Notes

- El brief congela los supuestos y los objetivos dorados. Cualquier cambio en la matriz de escenarios, capex, préstamo o personal obliga a regenerar los objetivos, el libro, el sitio y la documentación.
- La demanda es el supuesto menos evidenciado. El README y la guía deben decirlo con claridad y recomendar un conteo real antes de invertir.
- El libro se sirve desde GitHub Pages; su nombre y ruta deben ser estables para que los enlaces del README y del sitio no se rompan.
- La captura del README debe ser del dashboard real, a 1440×900, sin chrome del navegador, y debe mostrar un escenario y KPIs representativos.
- Cada pull request debe adjuntar evidencia visual o de ejecución con `gh --attach` y seguir la plantilla del skill `pr`. La integración final se fusiona en `main` solo con los tests verdes.
- El proyecto debe dejar `main` limpio: sin issues ni pull requests abiertos sin justificación, con el sitio desplegado y el README actualizado.
