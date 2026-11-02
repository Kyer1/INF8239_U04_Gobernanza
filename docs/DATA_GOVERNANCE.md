# Inventario, minimización y retención

## Inventario
`student_inputs/data_inventory.csv` registra, para cada columna, su categoría, finalidad, uso, decisión de minimización, plazo de retención y acceso.

La prueba `tests/test_ex08.py` comprueba que:
- el inventario cubre exactamente las columnas de los datos;
- ningún atributo sensible es predictor del modelo desplegado;
- las variables declaradas como predictoras coinciden con las que usa el modelo.

## Minimización
- **Atributos sensibles:** `protected_group` y `age_band` se usan **solo para auditoría**. Desde el EX07, `age_band` dejó de ser predictor.
- **Vista del operador:** `minimize()` le entrega una vista sin atributos sensibles (`operator_view_columns` en `datasheet_facts.json`).
- **Generalización en origen:** la zona tiene 4 categorías (sin coordenadas), la edad va en franjas y los índices son agregados.
- **Reportes:** muestran métricas agregadas por grupo o mes, no casos individuales.

## Retención
`student_inputs/retention.csv` define, para cada artefacto, el plazo, la forma de borrado y su responsable:
- **Datos de casos:** mientras el caso esté abierto + 12 meses.
- **Reportes de auditoría:** mientras exista el modelo + 12 meses.
- **Incidentes:** 24 meses.
- **Modelos serializados:** no se versionan en Git (`.gitignore`); se conserva su huella SHA-256 para trazabilidad.
