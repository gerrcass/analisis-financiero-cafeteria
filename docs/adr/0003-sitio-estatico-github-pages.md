# Sitio estático en GitHub Pages desde /docs

- **Estado**: aceptado
- **Fecha**: 2026-10-25

## Contexto

El sitio debe ser público, gratuito, sin backend y con un laboratorio interactivo que recalcule en el navegador. GitHub Pages sirve desde `/docs` en `main`; el repositorio es público y no hay servidor ni base de datos.

## Decisión

Sitio estático de dependencias cero: HTML, CSS y JavaScript vanilla en `site/`, copiado y generado a `docs/` para Pages. El modelo JavaScript se ejecuta en el cliente; los datos viven en `data/model.json`; el `.xlsx` se descarga como archivo estático. Los gráficos se dibujan en SVG inline, sin librerías.

## Consecuencias

- Despliegue gratis, rápido y reproducible; no hay secretos ni backend que mantener.
- Todo el cálculo es público e inspeccionable; el rendimiento depende del navegador del visitante.
- No hay persistencia, login ni analítica; el estado del laboratorio se puede compartir por URL, no se guarda.
- Las rutas deben ser relativas para funcionar bajo `/analisis-financiero-cafeteria/`; se prueban con servidor local y Playwright.
- Cambiar a un framework o a un backend sería una decisión nueva, no una evolución incremental.

## Alternativas consideradas

- **React/Vite**: más potencia, pero añade build y dependencias para un sitio de dos páginas.
- **API serverless**: prohibida por el requisito de no backend.
- **Observable/Plotly**: dependencia externa y menos control visual.
