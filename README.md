# INF-8239 · Unidad 04 · Gobernanza y DSS responsable

Proyecto base acumulativo para LAB11–13. El estudiante completa archivos pequeños en `student_inputs/`, ejecuta scripts y concentra su esfuerzo en interpretar y justificar decisiones.

## Inicio
```bash
uv sync --frozen
uv run pytest -q
uv run python scripts/check_environment.py
```

## Ruta
```bash
uv run python scripts/lab11_impact.py
uv run python scripts/lab12_audit.py --model logistic
uv run python scripts/lab13_governance.py
uv run streamlit run app.py
```

Los datos son sintéticos y didácticos. El sistema no autoriza decisiones automáticas sobre personas.

## Ejercicio 07 (U04.E07) — Evaluación de impacto y auditoría de equidad
Ver `docs/EX07_EXPEDIENTE.md`. Comando adicional (tarda 2–3 minutos por el bootstrap):
```bash
uv run python scripts/validate_lab12_decision.py
uv run python scripts/ex07_audit.py
```

## Ejercicio 08 (U04.E08) — Expediente de gobernanza y simulacro
Ver `docs/EX08_EXPEDIENTE.md`.
```bash
uv run python scripts/lab13_governance.py
uv run python scripts/simulate_incident.py
uv run python scripts/lab13_figures.py
uv run streamlit run app.py
```
