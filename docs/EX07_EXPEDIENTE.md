# Ejercicio 07 — Expediente de evaluación de impacto y auditoría de equidad

| Componente | Archivo editable / evidencia |
|---|---|
| Finalidad, decisión asistida, alternativa no predictiva, retiro y apelación | `student_inputs/lab11_impact.yml` |
| Partes interesadas (beneficio, daño, poder, participación) | `student_inputs/stakeholders.csv` |
| Registro de 8 riesgos priorizados (probabilidad × impacto) | `student_inputs/risk_register.csv` → `reports/lab11/risk_register_scored.csv` |
| Mapeo NIST AI RMF | `reports/lab11/rmf_summary.json` |
| Auditoría LAB12 por modelo | `reports/lab12/{logistic,tree}/` |
| Comparación de candidatos y puertas | `reports/ex07/model_comparison.csv` |
| Métricas por grupo de todos los candidatos | `reports/ex07/fairness_by_group_all.csv`, `fairness_by_group.png` |
| IC95% bootstrap de las brechas | `reports/ex07/gap_confidence_intervals.csv` |
| Auditoría interseccional con soporte mínimo | `reports/ex07/fairness_intersectional_flagged.csv`, `intersectional_recall.png` |
| Trade-off utilidad / brecha | `reports/ex07/tradeoff.png` |
| Decisión de daño, métrica, tolerancia y recomendación | `student_inputs/lab12_decision.yml`, `reports/lab11/DECISION_RECORD.md` |
| Obligación legal / marco voluntario / ética | `docs/NORMATIVA.md` |
| Model Card, Runbook, Declaración de IA | `docs/` |
| Pruebas | `tests/` (14 pruebas, incluye `test_audit_ext.py`) |

## Reproducir
```
uv sync --frozen
uv run pytest -q
uv run python scripts/lab11_impact.py
uv run python scripts/lab12_audit.py --model logistic
uv run python scripts/lab12_audit.py --model tree
uv run python scripts/validate_lab12_decision.py
uv run python scripts/ex07_audit.py
```

## Aplicación al trabajo final
Este expediente funciona como plantilla para el sistema del trabajo final (pronóstico de calidad del aire):
- **Finalidad y alternativa no predictiva:** por ejemplo, avisos basados en la medición del día anterior.
- **Registro de riesgos con NIST AI RMF:** p. ej., una alerta no emitida en un episodio de mala calidad del aire.
- **Auditoría por subgrupo:** en lugar de grupos de personas, por estación o zona y por temporada, con soporte mínimo e IC.
- **Gestión:** decisión documentada (desplegar, modificar, limitar o no utilizar), retiro y vuelta a la línea base.
