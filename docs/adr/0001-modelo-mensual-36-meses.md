# Modelo mensual de 36 meses

- **Estado**: aceptado
- **Fecha**: 2026-10-25

## Contexto

Cafetería Aurora tiene una estacionalidad mensual fuerte (agosto 0,72; diciembre 1,16), una rampa de maduración de seis meses, una plantilla que crece en 2027 y un préstamo a cinco años. Un modelo anual escondería los meses de EBITDA negativo y el mínimo de caja; un modelo semanal añadiría detalle que no cambia las decisiones de inversión.

## Decisión

Modelar 36 periodos mensuales, de enero de 2026 a diciembre de 2028, con resúmenes anuales y tres escenarios: Pesimista, Base y Optimista. Cada hoja de escenario tiene 36 columnas mensuales y columnas de total anual; el Resumen agrega los tres escenarios y permite seleccionar uno para los gráficos mensuales.

## Consecuencias

- Se ven los valles de caja de enero y febrero, el escalón de personal de 2027 y el efecto del servicio de la deuda.
- El libro es más ancho y tiene más fórmulas; se mitiga con una plantilla única, nombres definidos y tests de integridad.
- No se modela el ciclo completo del préstamo a cinco años: el año 3 muestra la deuda viva y el DSCR, suficiente para la decisión de inversión.
- Cambiar el horizonte obliga a regenerar libro, sitio y tests; no es un cambio incremental.

## Alternativas consideradas

- **Cinco años en anual**: más simple, pero oculta la estacionalidad y los meses de caja negativa.
- **Doce meses en mensual**: insuficiente para evaluar payback, rampa y deuda.
- **Semanal**: sobra detalle y no hay datos para calibrarlo.
