"""Simulacro de incidente: detección, contención, preservación, comunicación, rollback y postmortem."""
import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from inf8239_u04.data import features, load_data, temporal_split
from inf8239_u04.fairness import audit, gap
from inf8239_u04.governance import deployment_decision, load_config
from inf8239_u04.incident import inject_registry_failure, validate_response, zero_rate_check
from inf8239_u04.model import build_model, fit_measure
from inf8239_u04.monitoring import monitor, sha256

cfg = load_config(); kind = cfg["model_kind"]
resp = yaml.safe_load(Path("student_inputs/incident_response.yml").read_text(encoding="utf-8")); validate_response(resp)
out = Path("reports/lab13/incident"); out.mkdir(parents=True, exist_ok=True)
t0 = datetime.now(timezone.utc).replace(microsecond=0); log = []
def step(name, detail, minutes):
    log.append({"step": name, "at": (t0 + timedelta(minutes=minutes)).isoformat(), "detail": detail}); print(f"[{name}] {detail}")

# Modelo en producción (el mismo de LAB13)
df = load_data(); train, test = temporal_split(df)
model = build_model(kind); res = fit_measure(model, features(train, kind), train.target, "models/model.joblib")

# Escenario simulado: falla de registro en zona Norte desde 2026-11-01
bad, affected = inject_registry_failure(test)
pred = model.predict(features(bad, kind))

# 1. Detección: control sin etiquetas + monitoreo con etiquetas + puertas
zr = zero_rate_check(train, bad[bad.received_date >= "2026-11-01"]); zr.to_csv(out / "zero_rate_check.csv")
mon = monitor(train, bad.assign(pred=pred), cfg["monitoring"], cfg["min_group_support"]); mon.to_csv(out / "monitoring_incident.csv", index=False)
overall, by_group, _ = audit(bad.target, pred, bad.protected_group)
res["latency_ms"] = 0.02
gates = deployment_decision({"recall": float(overall["recall"])}, {"recall_gap": gap(by_group, "recall"), "fpr_gap": gap(by_group, "fpr")}, res, cfg["gates"])
step("deteccion", f"control de ceros: alerta en {list(zr.index[zr.alert])}; ventanas en ALERTA: {list(mon.window[mon.status == 'ALERTA'])}; "
     f"puertas={gates['status']} fallan {gates['failed']} (recall {overall['recall']:.3f}, brecha recall {gap(by_group,'recall'):.3f}, brecha FPR {gap(by_group,'fpr'):.3f})", 0)
step("clasificacion", f"severidad {'GRAVE' if gates['status']=='STOP' else 'MODERADA'} según regla: {resp['severity_rule']}", 15)

# 2. Contención y rollback a la línea base segura (FIFO: todos los casos, por orden de llegada)
step("contencion", f"Se suspende la puntuación y se activa safe_baseline={cfg['safe_baseline']}. Responsable: {resp['containment_owner']}", 30)
missed_model = int(((pred == 0) & (bad.target == 1)).sum())
step("rollback", f"con el modelo, {missed_model} casos reales quedaban sin priorizar; con FIFO se revisan los {len(bad)} casos (0 omitidos). Casos afectados por la falla: {affected}", 45)

# 3. Preservación de evidencia (antes de corregir nada)
shutil.copy("models/model.joblib", out / "model_at_incident.joblib")
manifest = {"incident_id": resp["incident_id"], "model_sha256": sha256("models/model.joblib"), "policy_sha256": sha256("configs/governance.yml"),
            "data_sha256": sha256("data/territorial_risk_synthetic.csv"), "scenario": "zone=Norte, previous_incidents=0 desde 2026-11-01",
            "affected_cases": affected, "gate_decision": gates,
            "files": ["zero_rate_check.csv", "monitoring_incident.csv", "incident_log.json", "INCIDENT_POSTMORTEM.md"]}
(out / "evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
step("preservacion", "modelo, huellas SHA-256 y reportes guardados en reports/lab13/incident/", 60)

# 4. Comunicación y 5. postmortem
step("comunicacion_interna", resp["communication_internal"], 90)
step("comunicacion_afectados", resp["communication_affected"], 24 * 60)
step("postmortem", f"{resp['postmortem_owner']}; plazo: {resp['postmortem_due']}", 25 * 60)
(out / "incident_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")

pm = f"""# Postmortem {resp['incident_id']} (simulacro)

**Escenario:** {manifest['scenario']} ({affected} casos afectados).

## Detección
{log[0]['detail']}

## Contención y rollback
- {log[2]['detail']}
- {log[3]['detail']}

## Evidencia preservada
Modelo `{manifest['model_sha256']}`, política `{manifest['policy_sha256']}`, datos `{manifest['data_sha256']}`. Ver `evidence_manifest.json`.

## Comunicación
- Interna: {resp['communication_internal']}
- Personas afectadas: {resp['communication_affected']}

## Causa raíz (hipótesis)
{resp['root_cause_hypothesis']}

## Acciones correctivas, responsables y plazos
{resp['corrective_actions']}

**Responsable del postmortem:** {resp['postmortem_owner']} · **Plazo:** {resp['postmortem_due']}

## Lecciones
{resp['lessons']}
"""
(out / "INCIDENT_POSTMORTEM.md").write_text(pm, encoding="utf-8")
print("postmortem:", out / "INCIDENT_POSTMORTEM.md")
