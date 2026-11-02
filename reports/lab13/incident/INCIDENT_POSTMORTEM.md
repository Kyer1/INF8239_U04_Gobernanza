# Postmortem INC-2026-11-01-SIM (simulacro)

**Escenario:** zone=Norte, previous_incidents=0 desde 2026-11-01 (25 casos afectados).

## Detección
control de ceros: alerta en ['Norte']; ventanas en ALERTA: ['2026-10', '2026-11', '2026-12', 'acumulado']; puertas=STOP fallan ['recall', 'recall_gap', 'fpr_gap'] (recall 0.565, brecha recall 0.161, brecha FPR 0.163)

## Contención y rollback
- Se suspende la puntuación y se activa safe_baseline=FIFO. Responsable: Institutional Owner (Accountable en Incident response); ejecuta el ML Engineer.
- con el modelo, 40 casos reales quedaban sin priorizar; con FIFO se revisan los 160 casos (0 omitidos). Casos afectados por la falla: 25

## Evidencia preservada
Modelo `53b250fa700f`, política `f75d92c089bd`, datos `2af1858fe874`. Ver `evidence_manifest.json`.

## Comunicación
- Interna: Aviso al Product Owner, Data Scientist y operadores en menos de 24 horas: el orden de la cola vuelve a FIFO y se suspende la puntuación.
- Personas afectadas: Aviso a los representantes de las personas afectadas en 5 días hábiles: qué pasó, qué casos de zona Norte se revisan de nuevo y cómo apelar.

## Causa raíz (hipótesis)
La migración del formulario de zona Norte no trasladó el campo previous_incidents y los valores ausentes se guardaron como 0.

## Acciones correctivas, responsables y plazos
1) Revisar de nuevo, con prioridad, los casos de zona Norte recibidos desde 2026-11-01 (Operator, 3 días). 2) Corregir la migración y recargar el campo (Data Engineer, 7 días). 3) Añadir al contrato de datos la regla de que un valor ausente no se codifica como 0 y el control de proporción de ceros por zona (Data Engineer, 10 días). 4) Repetir auditoría y puertas antes de reactivar el modelo (Data Scientist, 10 días).

**Responsable del postmortem:** Data Scientist (R) con aprobación del Institutional Owner (A) · **Plazo:** 10 días hábiles después de la contención

## Lecciones
Las métricas con etiquetas detectan el problema tarde; el control de calidad sin etiquetas (proporción de ceros por zona) lo detecta el mismo mes. Las ventanas mensuales son pequeñas para medir brechas: las alertas de equidad se confirman con el acumulado.
