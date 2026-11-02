from pathlib import Path
import pandas as pd
import yaml

def load_config(path="configs/governance.yml"):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

MULTI_ROLE = r"[,;/&+]| and | y "

def validate_raci(df):
    required={"activity","R","A","C","I"}
    if required-set(df.columns): raise ValueError("RACI columns missing")
    if df[["R","A"]].fillna("").apply(lambda s:s.str.strip().eq("")).any().any(): raise ValueError("Every activity needs R and A")
    if df.A.fillna("").str.contains(MULTI_ROLE, regex=True).any(): raise ValueError("Exactly one Accountable per activity")
    if df.activity.duplicated().any(): raise ValueError("Duplicated activity")
    return True

def roles(df):
    """Roles individuales nombrados en la matriz RACI."""
    import re
    out=set()
    for col in ["R","A","C","I"]:
        for cell in df[col].fillna(""):
            out |= {r.strip() for r in re.split(MULTI_ROLE, cell) if r.strip()}
    return out

def deployment_decision(metrics, gaps, resources, gates):
    checks={
      "recall": metrics["recall"] >= gates["min_recall"],
      "recall_gap": gaps["recall_gap"] <= gates["max_recall_gap"],
      "fpr_gap": gaps["fpr_gap"] <= gates["max_fpr_gap"],
      "latency": resources["latency_ms"] <= gates["max_latency_ms"],
      "model_size": resources["model_kb"] <= gates["max_model_kb"],
    }
    failed=[k for k,v in checks.items() if not v]
    # STOP: el sistema deja de ser útil (recall) y además trata distinto a los grupos, o fallan muchas puertas a la vez
    stop = ("recall" in failed and any(k in failed for k in ("recall_gap","fpr_gap"))) or len(failed) >= gates.get("stop_failed_checks", 99)
    status = "STOP" if stop else ("REVIEW" if failed else "GO")
    action = {"GO":"Document review and final decision","REVIEW":"Accountable owner reviews evidence and records decision before use",
              "STOP":"Suspend model, return to safe baseline (FIFO) and open incident"}[status]
    return {"status":status, "checks":checks, "failed":failed, "human_action":action}
