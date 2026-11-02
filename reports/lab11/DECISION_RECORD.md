# Registro de decisión — Territorial Review DSS (sintético)

**Fecha:** 2026-11-02 · **Responsable:** Responsable institucional del programa (Product Owner) · **Elaborado por:** Kimberly Pereyra Moreta

## Decisión
**LIMITAR (equivale a REVIEW en la escala GO/REVIEW/STOP).** Uso la regresión logística sin `age_band` (umbral 0.50) solo para ordenar la cola de revisión humana. Ningún caso se excluye ni se cierra por la puntuación.

## Evidencia
- Las puertas técnicas pasan: recall 0.717 (mínimo 0.68), brecha de recall 0.138 y de FPR 0.144 (máximo 0.16), 3.3 KB, menos de 1 ms por caso.
- El árbol de decisión no pasa: brecha de recall 0.181 y de FPR 0.168.
- El grupo G1 tiene menor recall (0.653 frente a 0.791). Es el daño prioritario: casos reales que esperan más.

## Incertidumbre
- La prueba tiene solo 160 casos.
- Los IC95% bootstrap de las brechas llegan hasta ~0.32 (recall) y ~0.43 (FPR), por encima de la tolerancia.
- Cinco de ocho subgrupos interseccionales tienen menos de 20 casos.
- Por eso no presento la puerta como evidencia suficiente de equidad, y no recomiendo un despliegue pleno (GO).

## Condiciones
- Todos los casos se revisan; el modelo solo cambia el orden.
- Revisión mensual del recall de G1.
- Canal de apelación con respuesta en 5 días hábiles.
- Retiro y vuelta a FIFO según `lab11_impact.yml`.
- Nueva auditoría cuando haya al menos 20 casos por subgrupo.
