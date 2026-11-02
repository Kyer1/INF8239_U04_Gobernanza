# Model Card — Regresión logística sin age_band (DSS territorial sintético)

## Intended use
Ordenar casos sintéticos para revisión técnica humana. El modelo prioriza; no decide ni excluye casos.
## Out-of-scope use
- Intervención automática, elegibilidad, declaración de emergencia o sanciones.
- Perfilamiento de personas.
- Uso con poblaciones reales.
## Version and traceability
- `model_kind: logistic_no_age`.
- Huellas: modelo `53b250fa700f`, política `f75d92c089bd`, datos `2af1858fe874` (`reports/lab13/traceability.json`). El modelo se identifica por su huella; el archivo no se versiona.
- Datos descritos en `docs/DATASHEET.md`.
## Data and split
- 640 casos sintéticos, con partición temporal: entrenamiento 480 (hasta 2026-09-24) y prueba 160.
- Predictores: zone, previous_incidents, infrastructure_score, exposure.
- `protected_group` y `age_band` solo se usan para auditar.
## Global and subgroup evaluation
- Global: accuracy 0.725, recall 0.717, FPR 0.265.
- Recall: G1 0.653, G2 0.791 (brecha 0.138, IC95% 0.008–0.320).
- FPR: G1 0.231, G2 0.375 (brecha 0.144, IC95% 0.008–0.428).
- Puertas: GO (`reports/lab13/deployment_decision.json`).
- Monitoreo mensual (`reports/lab13/monitoring.csv`):
  - Octubre: recall 0.607, con alerta.
  - Noviembre: brechas de recall 0.304 y de FPR 0.206, con grupos de n ≥ 20, con alerta.
  - El acumulado (n = 160) está dentro de la tolerancia.
## Green AI evidence
- Entrenamiento de unos 0.03 s; modelo de 3.3 KB; latencia de unos 0.02 ms por caso.
- El árbol pesa 7.9 KB y no mejora el recall.
## Limitations, human oversight and appeal
- Datos sintéticos y muestra pequeña: los IC de las brechas son amplios y las ventanas mensuales son ruidosas.
- `zone` u otras variables pueden actuar como proxy.
- Todos los casos se revisan; hay apelación con respuesta en 5 días hábiles.
- Retiro y vuelta a FIFO si se incumplen las puertas.
- **Decisión: LIMITAR** (`student_inputs/lab12_decision.yml`).
## Owner and review date
Product Owner (Accountable en Deployment). Próxima revisión: 2026-12-02.
