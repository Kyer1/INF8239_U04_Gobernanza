"""Extensiones para el Ejercicio 07: incertidumbre de brechas, soporte mínimo y umbral elegido en validación."""
import numpy as np
import pandas as pd
from sklearn.metrics import recall_score

from .fairness import audit, gap


def bootstrap_gap_ci(y_true, y_pred, groups, metric="recall", n_boot=1000, seed=42, alpha=0.05):
    """Intervalo de confianza bootstrap (remuestreo dentro de cada grupo) para la brecha entre grupos."""
    rng = np.random.default_rng(seed)
    data = pd.DataFrame({"y": np.asarray(y_true), "p": np.asarray(y_pred), "g": np.asarray(groups)})
    gaps = []
    for _ in range(n_boot):
        sample = pd.concat([part.sample(len(part), replace=True, random_state=int(rng.integers(1e9)))
                            for _, part in data.groupby("g")])
        _, by_group, _ = audit(sample.y, sample.p, sample.g)
        gaps.append(gap(by_group, metric))
    _, by_group, _ = audit(data.y, data.p, data.g)
    low, high = np.quantile(gaps, [alpha / 2, 1 - alpha / 2])
    return {"metric": metric, "gap": gap(by_group, metric), "ci_low": float(low), "ci_high": float(high)}


def flag_support(table: pd.DataFrame, min_count: int) -> pd.DataFrame:
    """Marca los grupos con menos observaciones que el mínimo: se reportan, pero no se interpretan."""
    out = table.copy()
    out["support"] = np.where(out["count"] >= min_count, "suficiente", "insuficiente")
    return out


def threshold_for_recall(y_valid, proba_valid, target_recall=0.80, grid=None):
    """Mayor umbral cuyo recall en VALIDACIÓN alcanza el objetivo (evita usar la prueba para decidir)."""
    grid = np.round(np.arange(0.30, 0.71, 0.05), 2) if grid is None else grid
    ok = [t for t in grid if recall_score(y_valid, (proba_valid >= t).astype(int), zero_division=0) >= target_recall]
    return float(max(ok)) if ok else float(min(grid))


NO_AGE_COLUMNS = ["zone", "previous_incidents", "infrastructure_score", "exposure"]


def build_model_without_age():
    """Mitigación: regresión logística sin age_band, que la política (governance.yml) declara atributo sensible."""
    from sklearn.compose import ColumnTransformer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["zone"]),
                              ("num", StandardScaler(), NO_AGE_COLUMNS[1:])])
    return make_pipeline(prep, LogisticRegression(max_iter=1200, class_weight="balanced", random_state=42))
