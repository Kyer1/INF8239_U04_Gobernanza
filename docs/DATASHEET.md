# Datasheet — territorial_risk_synthetic.csv
Formato basado en Gebru et al., *Datasheets for Datasets*. Las cifras salen de `reports/lab13/datasheet_facts.json` (lo genera `scripts/lab13_governance.py`).

## Motivación
- Conjunto sintético creado con una semilla fija para practicar contratos de datos, evaluación temporal, auditoría por subgrupos y gobernanza.
- No representa personas, lugares ni estadísticas reales de la República Dominicana.

## Composición
- 640 casos, uno por fila, recibidos del 2026-01-01 al 2026-12-27.
- 9 columnas, descritas en `student_inputs/data_inventory.csv`.
- Variable objetivo `target` (incidente sí/no); tasa positiva 0.552.
- Grupos: G1 = 396, G2 = 244.
- Franjas de edad: 18-29 = 148, 30-44 = 163, 45-59 = 150, 60+ = 179.
- Zonas: entre 155 y 164 casos cada una.
- Calidad: 0 valores ausentes y 0 `case_id` duplicados.
- No contiene identificadores directos; el esquema los rechaza (`validate_schema`).
- Hay atributos sensibles (`protected_group`, `age_band`), que solo se usan para auditar.

## Recolección y preprocesamiento
- Generación sintética, sin recolección a personas.
- El único preprocesamiento es el del pipeline: one-hot de `zone` y escalado de las variables numéricas, aprendidos solo en entrenamiento.
- Partición temporal: entrenamiento 480 casos (hasta 2026-09-24), prueba 160.

## Usos
- **Previstos:** docencia; priorizar la revisión humana en un DSS de demostración.
- **No permitidos:** decisiones sobre personas reales, elegibilidad, intervención automática o perfilamiento.

## Distribución y mantenimiento
- Se incluye en el repositorio por ser sintético.
- **Versión:** SHA-256 `2af1858fe874` (prefijo de 12 caracteres).
- Cualquier cambio de datos cambia la huella y obliga a repetir la auditoría.
- **Responsable:** Data Engineer (R), Institutional Owner (A), según la actividad *Data inventory and retention* de la matriz RACI.
