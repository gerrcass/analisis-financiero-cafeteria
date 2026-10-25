# Benchmarks y fuentes

> Fecha de consulta: 25 de octubre de 2026.  
> Este documento calibra los supuestos del modelo; no es una valoración, una oferta ni un estudio de mercado. Los rangos son referencias públicas y de listados, no precios cerrados.

## Cómo leer esta nota

Cada fila distingue entre:

- **Dato**: hay una fuente pública o un precio contratado que lo respalda.
- **Supuesto**: es una elección del modelo, informada por el rango pero no demostrada.
- **A validar**: requiere presupuesto, contrato o prueba antes de invertir.

## Tabla de calibración

| Variable | Valor del modelo | Referencia / rango | Tipo | Comentario |
|---|---:|---|---|---|
| IVA de hostelería | 10% | AEAT: servicios de hostelería y restaurantes al 10% | Dato | Aplica a café preparado, comida servida y café en grano; el alcohol y los refrescos van al 21%, fuera del catálogo. |
| Tipo de sociedades | 25% | AEAT: tipo general del Impuesto sobre Sociedades | Dato | Se aplica sobre base imponible positiva; no se modelan deducciones ni el tipo reducido de microempresa. |
| Cotización empresarial | 31,5% | Seguridad Social: contingencias comunes 23,6%, desempleo 5,5%, FOGASA 0,2%, formación 0,6% y AT/EP ~1,6% | Dato + supuesto | El 1,6% de AT/EP es una aproximación; el tipo exacto depende de la actividad y la mutua. |
| SMI 2025 | 1.184 €/mes en 14 pagas (16.576 €/año) | Ministerio de Trabajo / SMI 2025 | Dato | Todos los salarios del modelo están por encima del SMI. |
| Salario de barista | 23.000 €/año | Convenio estatal de hostelería: camarero ~1.160–1.250 €/mes en 14 pagas (16.240–17.500 €/año); mercado de especialidad 20.000–25.000 € | Supuesto | Se paga por encima de convenio para atraer baristas con experiencia en especialidad. |
| Salario de gerente | 30.000 €/año | Rango de gerente de local en hostelería: 28.000–35.000 € | Supuesto | Incluye responsabilidad de compras, equipo y cumplimiento. |
| Ayudante de cocina | 21.000 €/año | Convenio de hostelería + mercado | Supuesto | A jornada completa; apoyo de panadería y salados. |
| Alquiler | 1.900 €/mes para 92 m² (20,65 €/m²/mes) | Idealista/Fotocasa Zaragoza: locales desde ~10 €/m²/mes; centro y calles comerciales, 15–25 €/m²/mes; prime, más | Supuesto | Precio de anuncio, no de cierre. Validar con tres ofertas y revisar gastos comunes. |
| Suministros | 1.450 €/mes | PVPC/CNMC y facturas tipo de local de 90–100 m² | Supuesto | Luz, gas, agua y residuos; sensitive a la estacionalidad y al horario. |
| Servicios fijos | 780 €/mes | Internet, TPV, software, seguro, gestoría, alarma | Supuesto | Contratos anuales; revisar en la negociación. |
| Marketing fijo | 450 €/mes | Contenido, fotografía, impresos, acciones locales | Supuesto | Se suma un 3% variable de ingresos en el escenario Base. |
| Otros gastos | 1.100 €/mes | Limpieza, mantenimiento menor, formación, banca y comisiones | Supuesto | Incluye una estimación de comisiones de cobro; no se separa para no complicar el P&L. |
| Precio de espresso | 1,70 € | Cafeterías de especialidad en España: 1,50–2,00 € | Supuesto | Producto de entrada; margen alto, ticket bajo. |
| Precio de flat white | 2,80 € | Especialidad: 2,50–3,50 € | Supuesto | Bebida de leche más vendida; el precio relativo al espresso es clave. |
| Precio de café en grano 250 g | 10,50 € | Retail de especialidad: 9–14 € por 250 g | Supuesto | Producto de margen inferior (50,8%) pero ticket alto. |
| Coste de café | 0,42 €/espresso | Café verde/tostado de especialidad: 20–30 €/kg; dosis 18 g → 0,36–0,54 € | Supuesto | Incluye merma; el coste del flat white añade leche y packaging. |
| Coste de leche | ~0,16 €/bebida | Leche entera 1,05 €/L; 150 ml | Supuesto | Alternativas vegetales más caras; no se modelan. |
| Merma | 2–8% | Rango típico de café, panadería y retail | Supuesto | 2% retail, 4% café, 5% cold brew, 6% tostada, 8% croissant. |
| Inflación de costes | 3,5% Base; 4,5% Pesimista; 2,8% Optimista | ICO: volatilidad del precio del café; inflación de alimentación | Supuesto | No es una previsión; es una hipótesis de estrés. |
| Inflación de suministros | 4,0% Base; 6,0% Pesimista; 3,0% Optimista | CNMC/PVPC: volatilidad energética | Supuesto | La luz y el gas son el componente más volátil. |
| Crecimiento de precios | 2,5% Base; 1,5% Pesimista; 3,2% Optimista | IPC de alimentación y hostelería | Supuesto | Se aplica una vez al año, en enero. |
| Crecimiento de demanda | 4,0% Base; 1,5% Pesimista; 6,0% Optimista | No hay fuente para un local concreto | Supuesto | Es la variable más incierta; se prueba con la rampa y el escenario Pesimista. |
| Capex inicial | 132.000 € | 1.435 €/m² para 92 m², incluyendo equipo | Supuesto | Obra 65.000 €, maquinaria 28.000 €, mobiliario 15.000 €, cocina 12.000 €, tecnología 7.000 €, licencias 5.000 €. Validar con tres presupuestos. |
| Vida útil | 4–10 años | Práctica contable habitual | Supuesto | Obra 10, maquinaria 7, mobiliario 8, cocina 8, tecnología 4, licencias 5. |
| Préstamo | 70.000 € a 7,5% y 5 años | Tipos de préstamo para pymes en 2025–2026: 6–9% | Supuesto | Tipo fijo; no se modela Euríbor ni comisión de apertura. |
| Equity | 90.000 € | 56% de la inversión total | Supuesto | Colchón para cumplir el mínimo de caja y el DSCR. |

## Fuentes

1. **Agencia Tributaria — Tipos impositivos del IVA 2025**  
   https://sede.agenciatributaria.gob.es/static_files/Sede/Tema/IVA/IVA_reperc/Tipos_IVA_2025.pdf  
   https://sede.agenciatributaria.gob.es/Sede/en_gb/iva/calculo-iva-repercutido-clientes/tipos-impositivos-iva.html

2. **Seguridad Social — Bases y tipos de cotización**  
   https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/CotizacionRecaudacionTrabajadores/36537  
   https://www.boe.es/buscar/act.php?id=BOE-A-2025-3780

3. **XVII Convenio Colectivo Estatal de Hostelería (BOE, 20/06/2025)**  
   https://www.boe.es/boe/dias/2025/06/20/pdfs/BOE-A-2025-12598.pdf

4. **SMI 2025: 1.184 €/mes en 14 pagas**  
   https://leglobal.law/2025/03/26/spain-new-minimum-interprofessional-salary-smi-in-spain-for-2025/

5. **Alquiler de locales en Zaragoza (anuncios)**  
   https://www.idealista.com/alquiler-locales/zaragoza-zaragoza/  
   https://www.fotocasa.es/es/alquiler/locales/zaragoza-provincia/todas-las-zonas/

6. **Precio del café y volatilidad**  
   https://www.ico.org/  
   https://cafesmyway.com/noticias/mercado-del-cafe-espana/

7. **Precio de café de especialidad en España**  
   https://www.elcorreo.com/vivir/tendencias/cafes-especialidad-euros-justificado-precio-puro-postureo-20241105001546-ntrc.html

8. **Energía y PVPC**  
   https://www.cnmc.es/

## Lo que no está respaldado por una fuente

Son supuestos, no datos: la demanda de 360 tickets/día, la rampa de seis meses, la estacionalidad, el mix de producto, los precios exactos de la carta, la merma, el capex, el alquiler concreto, la cuota de mercado y el crecimiento. Se eligieron para que el modelo sea internamente coherente y didáctico, no para predecir un local real.

## Cómo validar antes de invertir

1. **Alquiler**: tres ofertas de locales comparables, con gastos comunes, fianza y revisión anual.
2. **Obra y equipo**: tres presupuestos de fit-out y tres de maquinaria; añadir un 10% de contingencia.
3. **Demanda**: conteo de peatones y tickets en la zona durante dos semanas, en franjas mañana, mediodía y tarde.
4. **Carta**: prueba de menú con 20 clientes y análisis de margen por producto.
5. **Proveedores**: dos ofertas de café, leche, panadería y packaging; contrato a seis meses con revisión de precio.
6. **Personal**: simulación de nómina con convenio, cotización y horas; validar que 4,0 FTE cubren 312 días de apertura.
7. **Financiación**: dos entidades, comparar tipo fijo, comisión de apertura, carencia y covenants.
8. **Fiscalidad**: confirmar tipo de sociedades, obligaciones de IVA y retenciones con un asesor.

## Advertencia

Los enlaces se consultaron en la fecha indicada. Los precios de anuncios y los tipos de interés cambian; antes de usar el modelo para una decisión real, sustituir los supuestos por ofertas y contratos vigentes.
