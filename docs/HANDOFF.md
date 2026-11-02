# Traspaso entre roles

Trabajo de forma individual y asumo todos los roles. Aun así, mantengo la separación de responsabilidades de la matriz RACI (`student_inputs/raci.csv`, 9 actividades):
- cada actividad tiene **un solo Accountable**, y la prueba lo verifica;
- `student_inputs/handoff.csv` define cada entrega entre roles, con su artefacto, criterio de aceptación y evidencia;
- la validación comprueba que todos los roles del traspaso existan en la RACI.

| De | A | Qué se entrega | Se acepta si… |
|---|---|---|---|
| Data Engineer | Data Scientist | Datos validados e inventario | esquema válido, sin identificadores, inventario completo |
| Data Scientist | ML Engineer | Modelo y auditoría de equidad | puertas en PASS, IC y soporte documentados, Model Card |
| ML Engineer | Product Owner | DSS trazable | decisión con huellas de modelo/política/datos; app sin errores; monitoreo |
| Product Owner | Operator | Procedimiento de uso y apelación | operador capacitado en límites y apelación |
| ML Engineer | Institutional Owner | Simulacro y postmortem | alerta detectada, rollback ejecutado, evidencia preservada |

Un traspaso que no cumple su criterio no avanza: el rol receptor lo devuelve y lo registra.
