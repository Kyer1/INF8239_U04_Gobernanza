# Ejercicio 08 — Expediente de gobernanza y simulacro (LAB13)

| Criterio | Artefactos editables | Evidencia y pruebas |
|---|---|---|
| Inventario, minimización y retención | `student_inputs/data_inventory.csv`, `student_inputs/retention.csv`, `docs/DATA_GOVERNANCE.md` | `reports/lab13/datasheet_facts.json` (operator_view_columns); `tests/test_ex08.py` |
| Datasheet y Model Card trazables | `docs/DATASHEET.md`, `docs/MODEL_CARD.md` | `reports/lab13/traceability.json`, `deployment_decision.json` (huellas SHA-256 de modelo, política y datos) |
| RACI y traspaso | `student_inputs/raci.csv`, `student_inputs/handoff.csv`, `docs/HANDOFF.md` | `validate_raci` (un solo Accountable), `validate_handoff`; `tests/test_ex08.py` |
| Monitoreo, runbook y simulacro | `configs/governance.yml` (monitoring), `docs/RUNBOOK.md`, `student_inputs/incident_response.yml` | `reports/lab13/monitoring.csv`, `monitoring.png`, `reports/lab13/incident/` (log, manifiesto, postmortem) |
| Pruebas, Git y documentación | `tests/` (23 pruebas), `requirements.txt` | historial Git y etiqueta `u04-lab13` |

## Reproducir
```
uv sync --frozen
uv run pytest -q
uv run python scripts/lab13_governance.py
uv run python scripts/simulate_incident.py
uv run python scripts/lab13_figures.py
uv run streamlit run app.py
```

## Aplicación al trabajo final (calidad del aire)
- **Inventario y minimización:** estación, fecha y hora, y meteorología. No hay datos personales, pero sí se aplica la retención de los datos y de los modelos.
- **Datasheet:** fuente UCI con licencia CC BY 4.0 y huella del ZIP descargado. **Model Card:** gradient boosting, con la huella del modelo.
- **RACI:** quién publica una alerta de PM2.5 y quién puede suspenderla.
- **Monitoreo:**
  - control sin etiquetas: proporción de valores ausentes del sensor;
  - recall de la clase "alto" por mes y por temporada.
- **Simulacro:** sensor que deja de reportar o que reporta 0. El rollback vuelve al baseline de persistencia.
