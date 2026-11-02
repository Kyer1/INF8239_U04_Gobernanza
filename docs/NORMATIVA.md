# Obligación legal, marco voluntario y recomendación ética

| Tipo | Referencia | Qué implica para este sistema |
|---|---|---|
| **Obligación legal** | Constitución de la República Dominicana, art. 44, y Ley 172-13 sobre Protección de Datos de Carácter Personal (vigente desde 2013) | Si el sistema se usara con datos reales de personas, su tratamiento debe respetar los principios de licitud, calidad, finalidad y seguridad. En este ejercicio los datos son sintéticos y el esquema rechaza identificadores directos (`tests/test_privacy.py`). |
| **Obligación legal (datos reales)** | Ley 172-13, principios de calidad y finalidad del tratamiento | Con datos reales, solo se tratan los datos necesarios para la finalidad declarada y se conservan el tiempo necesario. Por eso hay inventario, minimización y retención (`docs/DATA_GOVERNANCE.md`). Los plazos concretos son una decisión del equipo, no los fija esta ley. |
| **Marco voluntario** | NIST AI RMF 1.0 (GOVERN, MAP, MEASURE, MANAGE); Principios de IA de la OCDE; Model Card (Mitchell et al.) y Datasheets for Datasets (Gebru et al.); matriz RACI | No son obligatorios en la República Dominicana. Los adopto para organizar el registro de riesgos, la auditoría y la gestión (`reports/lab11/rmf_summary.json`). |
| **Recomendación ética** | Recomendación de la UNESCO sobre la ética de la IA (2021, no vinculante); criterio propio del equipo | Supervisión humana, no excluir casos por la puntuación, apelación, priorizar el daño de los falsos negativos en G1, no concluir sobre subgrupos pequeños, y comunicar los incidentes a las personas afectadas aunque ninguna ley específica lo exija hoy. |

**Nota sobre el estado normativo (noviembre 2026):**
- A octubre de 2026 no hay en el país una ley general de IA aprobada; hay iniciativas en estudio en el Congreso.
- La Ley 172-13 no regula de forma específica las decisiones automatizadas.
- Una reforma en discusión propone añadir ese derecho y evaluaciones de impacto.
- Por eso, que no exista una obligación legal específica no significa que no deba haber control: el límite "el sistema prioriza, no decide" es una decisión de diseño y ética, no un requisito legal actual.
