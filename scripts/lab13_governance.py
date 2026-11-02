"""LAB13 / EX08: decisión gobernada y trazable, inventario, monitoreo y datasheet."""
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from inf8239_u04.data import FEATURES, load_data, temporal_split
from inf8239_u04.governance import load_config, roles, validate_raci
from inf8239_u04.inventory import minimize, validate_handoff, validate_inventory, validate_retention
from inf8239_u04.monitoring import monitor, sha256
from inf8239_u04.pipeline import run

DATA, POLICY, MODEL = "data/territorial_risk_synthetic.csv", "configs/governance.yml", "models/model.joblib"
out = Path("reports/lab13"); out.mkdir(parents=True, exist_ok=True)
cfg = load_config(); df = load_data()

# 1. Controles previos: RACI, inventario, retención y traspaso
raci = pd.read_csv("student_inputs/raci.csv"); validate_raci(raci)
inv = pd.read_csv("student_inputs/data_inventory.csv"); validate_inventory(inv, df, cfg)
validate_retention(pd.read_csv("student_inputs/retention.csv"))
validate_handoff(pd.read_csv("student_inputs/handoff.csv"), roles(raci))

# 2. Entrenamiento, auditoría y puertas con el modelo decidido en EX07
result = run(df, cfg["gates"], cfg["model_kind"])
human = yaml.safe_load(Path("student_inputs/lab12_decision.yml").read_text(encoding="utf-8"))
decision = {
    "system": cfg["system_name"], "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "trace": {"model_kind": cfg["model_kind"], "features": FEATURES[cfg["model_kind"]],
              "model_sha256": sha256(MODEL), "policy_sha256": sha256(POLICY), "data_sha256": sha256(DATA),
              "train_rows": int(len(df) * .75), "test_rows": len(result["test"])},
    "metrics": result["metrics"], "gaps": result["gaps"], "resources": result["resources"],
    "gate_decision": result["decision"],
    "human_decision": {"recommendation": human["recommendation"], "owner": "Product Owner (Accountable en Deployment)"},
    "evidence": ["reports/ex07/model_comparison.csv", "reports/ex07/gap_confidence_intervals.csv",
                 "reports/lab13/monitoring.csv", "reports/lab13/fairness_by_group.csv"],
}
(out / "deployment_decision.json").write_text(json.dumps(decision, indent=2, ensure_ascii=False), encoding="utf-8")
(out / "traceability.json").write_text(json.dumps(decision["trace"], indent=2), encoding="utf-8")
result["by_group"].to_csv(out / "fairness_by_group.csv")

# 3. Monitoreo mensual sobre el periodo de prueba (referencia = entrenamiento)
train, test = temporal_split(df)
scored = test.assign(pred=result["pred"])
mon = monitor(train, scored, cfg["monitoring"], cfg["min_group_support"]); mon.to_csv(out / "monitoring.csv", index=False)

# 4. Hechos del datasheet y vista minimizada para el operador
facts = {"data_sha256": sha256(DATA), "rows": len(df), "columns": list(df.columns),
         "date_range": [str(df.received_date.min().date()), str(df.received_date.max().date())],
         "target_rate": round(float(df.target.mean()), 3),
         "by_group": df.protected_group.value_counts().to_dict(), "by_age_band": df.age_band.value_counts().to_dict(),
         "by_zone": df.zone.value_counts().to_dict(), "missing_values": int(df.isna().sum().sum()),
         "duplicated_case_id": int(df.case_id.duplicated().sum()),
         "operator_view_columns": list(minimize(df, inv).columns)}
(out / "datasheet_facts.json").write_text(json.dumps(facts, indent=2, ensure_ascii=False), encoding="utf-8")

print("gate_status:", result["decision"]["status"], "| failed:", result["decision"]["failed"])
print("trace:", decision["trace"]["model_sha256"], decision["trace"]["policy_sha256"], decision["trace"]["data_sha256"])
print(mon[["window", "n", "recall", "recall_gap", "fpr_gap", "psi_max", "status", "alerts"]].round(3).to_string(index=False))
