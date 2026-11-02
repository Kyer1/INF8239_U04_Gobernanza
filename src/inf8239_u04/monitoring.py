"""Monitoreo operativo (LAB13 / EX08): desempeño, equidad y deriva por ventana temporal."""
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

from .fairness import audit, gap

NUMERIC = ["previous_incidents", "infrastructure_score", "exposure"]


def psi(reference, current, bins=5):
    """Population Stability Index respecto de la referencia (entrenamiento).

    Se usan 5 bins por cuantiles y suavizado de Laplace (+0.5 por bin): con ventanas de ~50 casos,
    10 bins y bins vacíos producen PSI altos solo por ruido de muestreo (falsas alarmas).
    """
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    ref_c = np.histogram(reference, edges)[0] + 0.5
    cur_c = np.histogram(current, edges)[0] + 0.5
    ref, cur = ref_c / ref_c.sum(), cur_c / cur_c.sum()
    return float(np.sum((cur - ref) * np.log(cur / ref)))


def monitor(reference, scored, cfg, min_group_support=20):
    """Una fila por ventana mensual: n, recall, brechas, PSI máximo y alertas.

    `scored` necesita received_date, target, pred, protected_group y las variables numéricas.
    """
    rows = []
    windows = [(str(p), part) for p, part in scored.groupby(scored.received_date.dt.to_period("M"))]
    windows.append(("acumulado", scored))  # las brechas necesitan más casos que una ventana mensual
    for period, part in windows:
        overall, by_group, _ = audit(part.target, part.pred, part.protected_group)
        drift = {c: psi(reference[c], part[c]) for c in NUMERIC}
        row = {"window": period, "n": len(part), "recall": float(overall["recall"]),
               "recall_gap": gap(by_group, "recall"), "fpr_gap": gap(by_group, "fpr"),
               "min_group_n": int(by_group["count"].min()), "psi_max": max(drift.values()),
               "psi_variable": max(drift, key=drift.get)}
        alerts = []
        if row["n"] < cfg["min_window_cases"]:
            row["status"] = "INSUFICIENTE"; row["alerts"] = "ventana con pocos casos: se reporta sin alertar"
            rows.append(row); continue
        if row["recall"] < cfg["alert_recall"]: alerts.append("recall bajo")
        if row["min_group_n"] < min_group_support:
            alerts.append(f"aviso: brechas no evaluables (grupo con n={row['min_group_n']} < {min_group_support})")
        else:
            if row["recall_gap"] > cfg["alert_recall_gap"]: alerts.append("brecha de recall")
            if row["fpr_gap"] > cfg["alert_fpr_gap"]: alerts.append("brecha de FPR")
        if row["psi_max"] >= cfg["psi_alert"]: alerts.append(f"deriva en {row['psi_variable']}")
        elif row["psi_max"] >= cfg["psi_warning"]: alerts.append(f"aviso de deriva en {row['psi_variable']}")
        hard = [a for a in alerts if not a.startswith("aviso")]
        row["status"] = "ALERTA" if hard else ("AVISO" if alerts else "OK")
        row["alerts"] = "; ".join(alerts)
        rows.append(row)
    return pd.DataFrame(rows)


def sha256(path, n=12):
    """Huella corta de un archivo para trazabilidad (versión de datos, política o modelo)."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:n]
