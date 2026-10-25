# Fuente única de supuestos y libro generado

- **Estado**: aceptado
- **Fecha**: 2026-10-25

## Contexto

El mismo modelo debe vivir en el libro `.xlsx`, en el sitio público y en los tests. Editar el Excel a mano y replicar números en el sitio produce deriva; el encargo exige fórmulas vivas y una sola fuente de verdad.

## Decisión

`data/model.json` es la única fuente de entradas. Un motor Python calcula el modelo y genera el `.xlsx` con `openpyxl`; un motor JavaScript lee el mismo JSON para el sitio; los tests comparan ambos contra `data/expected.json`. El `.xlsx` generado no se edita a mano: si cambia un supuesto, se cambia el JSON y se regenera.

## Consecuencias

- Libro, sitio y tests comparten números por construcción.
- El `.xlsx` sigue siendo editable para explorar qué pasa si, pero esos cambios no vuelven al JSON ni al sitio; se documenta en la portada y en el README.
- El esquema del JSON es un contrato estable; cambiarlo exige migración, regeneración y actualización de los objetivos dorados.
- Un usuario no técnico no puede cambiar la fuente sin editar JSON; se ofrecen el laboratorio del sitio y las celdas de entrada del Excel como alternativas de exploración.

## Alternativas consideradas

- **Excel como fuente y Python leyendo el `.xlsx`**: frágil ante fórmulas, formato y cambios de layout.
- **Duplicar supuestos en Python y JavaScript**: deriva garantizada entre libro y sitio.
- **Generar el sitio desde el Excel**: dependencia de un binario y de la recalculación, peor para CI.
