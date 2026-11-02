"""Inventario de datos, minimización, retención y traspaso entre roles (EX08)."""
import pandas as pd

from .data import FEATURES

INVENTORY_COLS = {"field", "description", "category", "purpose", "use", "minimization", "retention", "access"}
RETENTION_COLS = {"artifact", "location", "retention", "deletion", "owner"}
HANDOFF_COLS = {"from_role", "to_role", "artifact", "acceptance_criterion", "evidence"}


def _complete(df, cols, name):
    if cols - set(df.columns): raise ValueError(f"{name}: columns missing {sorted(cols - set(df.columns))}")
    if df[list(cols)].fillna("").astype(str).apply(lambda s: s.str.strip().isin(["", "REPLACE"])).any().any():
        raise ValueError(f"{name}: complete all fields")


def validate_inventory(inv, data, cfg):
    """Cada columna de los datos está inventariada; ningún atributo sensible es predictor; no hay identificadores directos."""
    _complete(inv, INVENTORY_COLS, "data_inventory")
    fields, cols = set(inv.field), set(data.columns)
    if cols - fields: raise ValueError(f"Columns not inventoried: {sorted(cols - fields)}")
    if fields - cols: raise ValueError(f"Inventoried fields not in data: {sorted(fields - cols)}")
    used = set(FEATURES[cfg["model_kind"]])
    sensitive_used = used & set(cfg["sensitive_features"])
    if sensitive_used: raise ValueError(f"Sensitive features used as predictors: {sorted(sensitive_used)}")
    declared = set(inv.loc[inv.use == "predictor", "field"])
    if declared != used: raise ValueError(f"Inventory predictors {sorted(declared)} differ from model features {sorted(used)}")
    if set(cfg["direct_identifiers"]) & fields: raise ValueError("Direct identifiers must not be inventoried for use")
    return True


def minimize(data, inv):
    """Vista mínima para el operador: sin atributos de uso exclusivo de auditoría."""
    audit_only = inv.loc[inv.use == "solo auditoría", "field"].tolist()
    return data.drop(columns=audit_only)


def validate_retention(ret):
    _complete(ret, RETENTION_COLS, "retention")
    return True


def validate_handoff(handoff, raci_roles):
    _complete(handoff, HANDOFF_COLS, "handoff")
    unknown = (set(handoff.from_role) | set(handoff.to_role)) - raci_roles
    if unknown: raise ValueError(f"Handoff roles not in RACI: {sorted(unknown)}")
    return True
