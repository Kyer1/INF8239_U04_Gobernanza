"""Simulacro de incidente (LAB13 / EX08)."""
import numpy as np
import pandas as pd

REQUIRED_RESPONSE = {"incident_id", "severity_rule", "containment_owner", "communication_internal",
                     "communication_affected", "root_cause_hypothesis", "corrective_actions", "postmortem_owner",
                     "postmortem_due", "lessons"}


def inject_registry_failure(df, zone="Norte", start="2026-11-01", column="previous_incidents", value=0):
    """Escenario: tras una migración del formulario, en una zona el campo deja de migrarse y se guarda como 0."""
    out = df.copy()
    mask = (out.zone == zone) & (out.received_date >= pd.Timestamp(start))
    out.loc[mask, column] = value
    return out, int(mask.sum())


def zero_rate_check(reference, current, column="previous_incidents", by="zone", tolerance=0.15):
    """Control de calidad que no necesita etiquetas: proporción de ceros por zona frente a la referencia."""
    ref = reference.groupby(by)[column].apply(lambda s: (s == 0).mean())
    cur = current.groupby(by)[column].apply(lambda s: (s == 0).mean())
    table = pd.DataFrame({"reference_zero_rate": ref, "current_zero_rate": cur}).fillna(0)
    table["alert"] = (table.current_zero_rate - table.reference_zero_rate) > tolerance
    return table


def validate_response(data):
    incomplete = [k for k in REQUIRED_RESPONSE if str(data.get(k, "")).strip() in {"", "REPLACE"}]
    if incomplete: raise ValueError(f"Complete incident_response.yml: {sorted(incomplete)}")
    return True
