# Incident Runbook
Roles según `student_inputs/raci.csv` (actividad *Incident response*): R = ML Engineer, A = Institutional Owner, C = Legal y Data Scientist, I = representantes de personas afectadas. Simulacro probado con `scripts/simulate_incident.py`.

1. **Detection and classification:**
   - **Señales de cada mes** (`reports/lab13/monitoring.csv`):
     - control sin etiquetas de proporción de ceros por zona;
     - PSI de las variables;
     - recall de la ventana;
     - brechas solo cuando cada grupo tiene n ≥ 20, confirmadas con el acumulado.
   - **Severidad:**
     - GRAVE si la puerta devuelve STOP o se incumple una condición de retiro;
     - MODERADA si devuelve REVIEW;
     - LEVE si solo hay avisos de deriva.
2. **Containment authority:**
   - El Institutional Owner puede suspender la puntuación de inmediato; el ML Engineer la ejecuta.
   - Si es GRAVE, se suspende sin esperar el postmortem.
3. **Evidence preservation:**
   - Antes de corregir nada, guardar en `reports/lab13/incident/` lo siguiente:
     - el modelo;
     - las huellas SHA-256 de modelo, política y datos;
     - el monitoreo;
     - el control de calidad;
     - el registro con hora de cada paso (`evidence_manifest.json`, `incident_log.json`).
4. **Internal and affected-party communication:**
   - **Interna:** en menos de 24 h.
   - **Representantes de personas afectadas:** en 5 días hábiles, con los casos que se revisan de nuevo y la vía de apelación.
5. **Rollback or safe baseline:**
   - Volver a revisión por orden de llegada (FIFO, `safe_baseline` en `configs/governance.yml`), que no omite casos.
   - Revisar de nuevo, con prioridad, los casos afectados.
6. **Postmortem, owner and due date:**
   - El Data Scientist (R) lo elabora y el Institutional Owner (A) lo aprueba, en 10 días hábiles.
   - Antes de reactivar el modelo, repetir la auditoría y las puertas.
