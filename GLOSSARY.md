# Cafetería Aurora — Glosario de dominio

Este glosario fija el vocabulario del modelo financiero de Cafetería Aurora. Define conceptos del negocio y de la medición económica; no describe herramientas, hojas de cálculo ni decisiones de implementación.

## Negocio y demanda

**Cafetería Aurora**:
Café de especialidad de barrio con panadería artesanal y venta de café en grano, situado en el centro de Zaragoza. Es el sujeto del modelo, no una marca real.
_Avoid_: La tienda, el local, el proyecto.

**Café de especialidad**:
Café de origen trazable, tostado para resaltar atributos sensoriales y servido con estándares de extracción medibles. Justifica un ticket superior al de la cafetería convencional.
_Avoid_: Café gourmet, café premium.

**Ticket**:
Una compra completa de un cliente en una visita, con uno o varios ítems. Es la unidad de demanda del modelo.
_Avoid_: Transacción, compra, pedido.

**Ítems por ticket**:
Número medio de productos vendidos por ticket. Convierte tickets en unidades vendidas y permite separar tráfico de surtido.
_Avoid_: Líneas por ticket, artículos por cuenta.

**Ticket medio**:
Ingreso por ticket. Se expresa neto de IVA en el modelo y con IVA en la comunicación al cliente.
_Avoid_: Gasto medio, valor medio.

**Mix de producto**:
Reparto porcentual de las unidades vendidas entre los productos del catálogo. Suma 100% y se mantiene estable en los tres años.
_Avoid_: Surtido, composición de ventas.

**Estacionalidad**:
Patrón de demanda que se repite cada año y se expresa como factor mensual. La media de los doce factores es 1 y su suma es 12.
_Avoid_: Temporalidad, variación mensual.

**Rampa de maduración**:
Progresión de demanda de los primeros meses de un local nuevo, desde una fracción de su potencial hasta el régimen. En Aurora va del 75% al 100% en seis meses.
_Avoid_: Curva de aprendizaje, crecimiento inicial.

**Días operativos**:
Días al año en que el local abre y puede vender. Aurora normaliza 312 días y cierra los domingos y festivos.
_Avoid_: Días de apertura, jornada.

## Ingresos y producto

**PVP**:
Precio de venta al público con IVA incluido, tal como aparece en la carta. Es una entrada del catálogo.
_Avoid_: Precio de venta, precio de carta.

**Precio neto**:
PVP menos el IVA repercutido. Es el ingreso que reconoce la cuenta de resultados.
_Avoid_: Precio sin IVA, precio base.

**IVA repercutido**:
Impuesto sobre el valor añadido que el cliente paga y la empresa ingresa a Hacienda. No es ingreso ni coste del negocio; el modelo trabaja en neto.
_Avoid_: Impuesto sobre ventas, IVA soportado.

**Merma**:
Parte de la compra que no se vende por rotura, caducidad, error de preparación o cortesía. Se aplica al coste, no al precio.
_Avoid_: Pérdida, desperdicio.

**Coste ajustado por merma**:
Coste unitario dividido por (1 − merma). Refleja lo que cuesta cada unidad vendida después de asumir la pérdida.
_Avoid_: Coste real, coste efectivo.

**Margen bruto unitario**:
Precio neto menos coste ajustado por merma de una unidad. Es la contribución de cada producto antes de costes fijos.
_Avoid_: Beneficio unitario, margen de producto.

**Contribución**:
Ingreso menos costes variables. A nivel de ticket, es lo que queda para cubrir costes fijos y generar EBITDA.
_Avoid_: Margen de contribución, utilidad variable.

## Costes y resultados

**COGS**:
Coste de los productos vendidos. Incluye café, leche, panadería, packaging y merma, valorado a coste de compra.
_Avoid_: Coste de ventas, coste directo.

**Coste de personal**:
Salario bruto más la cotización empresarial a la Seguridad Social. No incluye IRPF, que se retiene del salario del empleado.
_Avoid_: Nómina, gasto de personal.

**Coste empresa**:
Coste total de un empleado para la empresa: salario bruto anual multiplicado por (1 + cotización empresarial). Se prorratea por FTE y por mes.
_Avoid_: Coste laboral, coste total.

**FTE**:
Equivalente a tiempo completo. Un trabajador a media jornada es 0,5 FTE; dos a media jornada suman 1,0 FTE.
_Avoid_: Empleado, cabeza, plantilla.

**Opex**:
Gastos operativos distintos de COGS y personal: alquiler, suministros, servicios, marketing y otros. En el modelo se separan fijos y variables.
_Avoid_: Gastos generales, gastos de estructura.

**EBITDA**:
Resultado antes de intereses, impuestos, amortizaciones y depreciaciones. Mide la caja operativa antes de inversión y financiación.
_Avoid_: Beneficio operativo, caja operativa.

**EBIT**:
Resultado antes de intereses e impuestos. Es el EBITDA menos la amortización; aproxima el beneficio de la operación.
_Avoid_: Beneficio operativo, resultado de explotación.

**Amortización**:
Reparto sistemático del coste de un activo a lo largo de su vida útil. No es una salida de caja del periodo.
_Avoid_: Depreciación, gasto de inversión.

**Intereses**:
Coste financiero del préstamo, calculado sobre el saldo vivo. Es una salida de caja y reduce el beneficio.
_Avoid_: Coste de la deuda, gastos financieros.

**EBT**:
Resultado antes de impuestos. Es el EBIT menos los intereses.
_Avoid_: Beneficio antes de impuestos, resultado antes de impuestos.

**Impuesto de sociedades**:
Tributo sobre el beneficio fiscal. Aurora aplica un tipo del 25% sobre la base imponible positiva.
_Avoid_: Corporación, IS.

**Pérdidas compensables**:
Pérdidas fiscales de un ejercicio que pueden restarse de beneficios futuros. El modelo las arrastra sin límite, por tratarse de una pyme con ingresos inferiores a 1 M€.
_Avoid_: Crédito fiscal, pérdidas acumuladas.

**Beneficio neto**:
EBT menos impuesto de sociedades. Es el resultado que queda para los accionistas después de intereses e impuestos.
_Avoid_: Utilidad, ganancia.

**Apalancamiento operativo**:
Sensibilidad del EBITDA a cambios en ventas cuando hay costes fijos. Cuanto mayores son los fijos, más amplifica el beneficio una caída de demanda.
_Avoid_: Leverage, efecto palanca.

## Caja y financiación

**Capital circulante**:
Recursos atrapados en inventario y cuentas por cobrar, menos financiación de proveedores. En un café suele ser negativo porque los proveedores financian parte del stock.
_Avoid_: Fondo de maniobra, working capital.

**Días de inventario**:
Días de COGS que se mantienen en almacén. Aurora asume 18 días.
_Avoid_: Rotación, stock days.

**Días de proveedor**:
Días de compra que se pagan a crédito. Aurora asume 30 días.
_Avoid_: Plazo de pago, DPO.

**Capex**:
Inversión en activos de larga vida: obra, maquinaria, mobiliario, tecnología y licencias. No se resta del EBITDA; se resta del flujo de caja.
_Avoid_: Inversión, CAPEX.

**Capex de mantenimiento**:
Inversión recurrente para conservar la capacidad del local. Se estima como un porcentaje de los ingresos netos.
_Avoid_: Inversión de reposición, mantenimiento.

**Flujo de caja libre (FCFF)**:
Caja que genera la operación después de impuestos teóricos sin deuda, capex de mantenimiento y variación de capital circulante. Es la caja disponible para todos los financiadores.
_Avoid_: Free cash flow, caja libre.

**Flujo de caja para el accionista (FCFE)**:
FCFF menos intereses, más el escudo fiscal de la deuda, menos devolución de principal. Es la caja que queda para el accionista después de pagar la deuda.
_Avoid_: Flujo equity, caja para socios.

**Escudo fiscal**:
Ahorro de impuestos que genera el interés de la deuda al reducir la base imponible. Es la diferencia entre el impuesto sin deuda y el impuesto con deuda.
_Avoid_: Tax shield, ahorro fiscal.

**Caja final**:
Caja disponible al cierre del periodo. Es la caja inicial más el FCFE.
_Avoid_: Saldo de tesorería, cash.

**Payback**:
Número de meses necesarios para recuperar la inversión inicial con la caja acumulada. Se calcula sobre el proyecto (FCFF) y sobre el equity (FCFE).
_Avoid_: Periodo de recuperación, retorno.

**DSCR**:
Cobertura del servicio de la deuda: (EBITDA − impuestos) dividido entre intereses más principal. Un DSCR de 1,0 significa que la caja operativa cubre justo la deuda.
_Avoid_: Cobertura de deuda, ratio de deuda.

**Cash-on-cash**:
Caja acumulada para el accionista dividida entre el equity aportado. Mide el retorno en caja, no el retorno contable.
_Avoid_: ROI, rentabilidad.

## Punto de equilibrio y decisión

**Punto de equilibrio**:
Nivel de ventas en el que el resultado es cero. El modelo lo expresa en tickets por día y distingue entre EBITDA cero y beneficio antes de impuestos cero.
_Avoid_: Break-even, umbral de rentabilidad.

**Margen de seguridad**:
Diferencia porcentual entre las ventas previstas y el punto de equilibrio. Indica cuánto puede caer la demanda antes de entrar en pérdidas.
_Avoid_: Colchón, buffer.

**Escenario**:
Combinación coherente de supuestos de demanda, precios y costes que describe un futuro posible. No es una predicción.
_Avoid_: Caso, hipótesis.

**Pesimista**:
Escenario de estrés: demanda 12% por debajo del plan en 2026, crecimiento del 1,5%, inflación de costes del 4,5% y presión salarial y de alquiler. Sirve para probar la resistencia, no para presupuestar.
_Avoid_: Malo, conservador.

**Base**:
Escenario de planificación: demanda en línea con el potencial del local, crecimiento del 4%, precios +2,5% y costes +3,5%. Es el presupuesto que se monitorea mes a mes.
_Avoid_: Realista, normal.

**Optimista**:
Escenario de expansión: demanda 8% por encima del plan, crecimiento del 6%, precios +3,2% y mejor productividad. Sirve para decidir inversiones de crecimiento, no para prometer resultados.
_Avoid_: Bueno, agresivo.

**Supuesto**:
Valor elegido para representar una variable que no se conoce con certeza. Debe poder justificarse y cambiarse.
_Avoid_: Dato, estimación.

**Dato**:
Valor observado o contratado, como un precio de proveedor, una cuota de préstamo o un tipo impositivo. Se distingue del supuesto.
_Avoid_: Hecho, referencia.

**Sensibilidad**:
Efecto de cambiar una variable sobre un resultado, manteniendo el resto constante. Sirve para ordenar riesgos, no para predecir.
_Avoid_: Elasticidad, escenario.

**Modelo financiero**:
Representación simplificada de la economía de un negocio que conecta supuestos, estados financieros y decisiones. En Aurora es mensual, a tres años y con tres escenarios.
_Avoid_: Excel, hoja de cálculo, proyección.

**Objetivo dorado**:
Cifra de referencia calculada con los supuestos congelados de este documento, usada para verificar que la implementación reproduce el modelo. No es un valor que se escriba en el libro.
_Avoid_: Resultado esperado, benchmark.
