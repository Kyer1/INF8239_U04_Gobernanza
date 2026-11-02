# Declaración de uso de IA

- **Herramienta:** Claude (Anthropic), asistente conversacional.
- **Finalidad:**
  - Apoyo para estructurar el código de auditoría ampliada (`src/inf8239_u04/audit_ext.py`, `scripts/ex07_audit.py`, `tests/test_audit_ext.py`).
  - Corregir el error de sintaxis de `scripts/lab11_impact.py`.
  - Proponer redacciones iniciales de los archivos de `student_inputs/` y de la documentación.
- **Prompts principales:**
  - "Ayúdame con el Ejercicio 07: evaluación de impacto y auditoría de equidad integrando LAB11–LAB12".
  - Solicitudes de explicación de los resultados y de opciones de mitigación.
- **Lo que no delegué:**
  - El daño prioritario, la métrica principal, la tolerancia y la decisión final (LIMITAR).
  - Revisé cada valor y decidí con base en los reportes generados.
  - Las cifras del documento provienen de los archivos de `reports/`, no de la herramienta.
- **Verificaciones humanas:**
  - Ejecuté `uv run pytest -q` (14 pruebas pasan).
  - Ejecuté los scripts LAB11, LAB12 (logistic y tree) y EX07.
  - Comparé las cifras del informe con `model_comparison.csv`, `fairness_by_group_all.csv` y `gap_confidence_intervals.csv`.
- **Errores detectados y correcciones:**
  1. `lab11_impact.py` tenía una cadena sin cerrar y además sobrescribía el registro de decisión. Lo corregí para que solo cree la plantilla si no existe.
  2. Faltaba `matplotlib` para las figuras. Lo añadí con `uv add`.
  3. El primer umbral elegido en validación (objetivo de recall 0.80 → 0.55) no se sostuvo en prueba (recall 0.696). Cambié el objetivo a 0.85 → 0.45 y dejé constancia de que el umbral nunca se elige mirando la prueba.
  4. Una prueba unitaria inicial estaba mal planteada (grupos con una sola clase). La corregí.

## Ejercicio 08 (LAB13)
- **Prompt principal:** "Vamos a hacer el ejercicio 8" con la guía de LAB13.
- **Apoyo recibido para estructurar:**
  - los módulos `monitoring.py`, `inventory.py` e `incident.py`;
  - el simulacro (`simulate_incident.py`);
  - las pruebas `tests/test_ex08.py`;
  - los borradores de inventario, retención, traspaso, datasheet, runbook y respuesta al incidente.
- **Decisiones mías:**
  - plazos de retención;
  - escenario del simulacro;
  - severidad;
  - responsables y plazos;
  - mantener la decisión LIMITAR.
- **Verificaciones:**
  - 23 pruebas pasan;
  - ejecución de `lab13_governance.py`, `simulate_incident.py` y de la app;
  - comparación de cifras con `deployment_decision.json`, `monitoring.csv` y `reports/lab13/incident/`.
- **Errores detectados y correcciones:**
  1. `simulate_incident.py` tenía una cadena sin cerrar; lo reescribí como simulacro completo.
  2. `deployment_decision` nunca devolvía STOP; añadí la regla STOP: recall bajo junto con una brecha, o 3 o más puertas fallidas.
  3. La validación RACI no comprobaba que hubiera un solo Accountable; la reforcé.
  4. El primer monitoreo alertaba deriva cada mes (PSI de 0.36 a 0.46) sin que los datos cambiaran. Era ruido por ventanas de unos 50 casos y 10 bins. Lo corregí con 5 bins, suavizado, brechas solo con n ≥ 20 por grupo y una ventana acumulada.
