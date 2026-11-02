"""Ejercicio 07: auditoría ampliada (baseline, modelos, umbral, incertidumbre, interseccionalidad y puertas)."""
import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from inf8239_u04.audit_ext import NO_AGE_COLUMNS, bootstrap_gap_ci, build_model_without_age, flag_support, threshold_for_recall
from inf8239_u04.data import features, load_data, temporal_split
from inf8239_u04.fairness import audit, gap, intersectional
from inf8239_u04.model import build_model, fit_measure

OUT = Path("reports/ex07"); OUT.mkdir(parents=True, exist_ok=True)
cfg = yaml.safe_load(Path("configs/governance.yml").read_text(encoding="utf-8"))
gates, MIN_SUPPORT = cfg["gates"], cfg.get("min_group_support", 20)

df = load_data(); train, test = temporal_split(df)
inner, valid = temporal_split(train, test_fraction=0.20)          # validación temporal dentro de entrenamiento
y_te, g_te = test.target, test.protected_group

# Umbral de la variante orientada a recall: se elige en VALIDACIÓN para recall >= 0.85 (daño prioritario: no detectar un caso)
val_model = build_model("logistic").fit(features(inner), inner.target)
thr = threshold_for_recall(valid.target, val_model.predict_proba(features(valid))[:, 1], 0.85)

candidates = {}
candidates["revisar_todo (sin modelo)"] = (np.ones(len(test), dtype=int), {"training_seconds": 0.0, "model_kb": 0.0}, None)
for kind in ("logistic", "tree"):
    m = build_model(kind); res = fit_measure(m, features(train), train.target, f"models/{kind}.joblib")
    start = time.perf_counter(); proba = m.predict_proba(features(test))[:, 1]
    res["latency_ms_per_case"] = (time.perf_counter() - start) * 1000 / len(test)
    candidates[f"{kind} (umbral 0.50)"] = ((proba >= 0.5).astype(int), res, 0.5)
    if kind == "logistic":
        candidates[f"logistic (umbral {thr:.2f}, validación)"] = ((proba >= thr).astype(int), res, thr)
        m2 = build_model_without_age(); res2 = fit_measure(m2, train[NO_AGE_COLUMNS], train.target, "models/logistic_sin_edad.joblib")
        start = time.perf_counter(); proba2 = m2.predict_proba(test[NO_AGE_COLUMNS])[:, 1]
        res2["latency_ms_per_case"] = (time.perf_counter() - start) * 1000 / len(test)
        candidates["logistic sin age_band (umbral 0.50)"] = ((proba2 >= 0.5).astype(int), res2, 0.5)

rows, by_group_all, ci_rows = [], [], []
for name, (pred, res, t) in candidates.items():
    overall, groups, _ = audit(y_te, pred, g_te)
    groups = groups.assign(model=name); by_group_all.append(groups.reset_index())
    row = {"modelo": name, "umbral": t, **{k: float(overall[k]) for k in ["accuracy", "recall", "precision", "fpr", "selection_rate"]},
           "brecha_recall": gap(groups, "recall"), "brecha_fpr": gap(groups, "fpr"), "brecha_seleccion": gap(groups, "selection_rate"),
           "tiempo_s": res["training_seconds"], "modelo_kb": res["model_kb"], "latencia_ms": res.get("latency_ms_per_case", 0.0)}
    row["puertas"] = "PASS" if (row["recall"] >= gates["min_recall"] and row["brecha_recall"] <= gates["max_recall_gap"]
                               and row["brecha_fpr"] <= gates["max_fpr_gap"] and row["modelo_kb"] <= gates["max_model_kb"]) else "FAIL"
    rows.append(row)
    if t is not None:
        for metric in ("recall", "fpr"):
            ci_rows.append({"modelo": name, **bootstrap_gap_ci(y_te, pred, g_te, metric)})

comparison = pd.DataFrame(rows); comparison.round(4).to_csv(OUT / "model_comparison.csv", index=False)
pd.concat(by_group_all).round(4).to_csv(OUT / "fairness_by_group_all.csv", index=False)
ci = pd.DataFrame(ci_rows); ci.round(4).to_csv(OUT / "gap_confidence_intervals.csv", index=False)

# Interseccional (grupo x edad) para cada modelo con soporte mínimo
inter_rows = []
for name, (pred, _, t) in candidates.items():
    if t is None: continue
    _, inter, _ = audit(y_te, pred, intersectional(test))
    inter = flag_support(inter, MIN_SUPPORT).assign(model=name); inter_rows.append(inter.reset_index().rename(columns={"sensitive_feature_0": "grupo"}))
inter_all = pd.concat(inter_rows); inter_all.round(4).to_csv(OUT / "fairness_intersectional_flagged.csv", index=False)

# Figuras
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
bg = pd.concat(by_group_all); bg = bg[bg.model != "revisar_todo (sin modelo)"]
for ax, metric, title in zip(axes, ["recall", "fpr"], ["Recall por grupo (casos reales detectados)", "Tasa de falsos positivos por grupo"]):
    piv = bg.pivot(index="model", columns="protected_group", values=metric)
    piv.plot.barh(ax=ax); ax.set_title(title); ax.set_xlim(0, 1.25); ax.set_ylabel(""); ax.legend(title="grupo", loc="lower right")
    if metric == "recall": ax.axvline(gates["min_recall"], color="red", ls="--", lw=1)
fig.tight_layout(); fig.savefig(OUT / "fairness_by_group.png", dpi=160)

fig, ax = plt.subplots(figsize=(7, 5))
sub = comparison[comparison.umbral.notna()]
ax.scatter(sub.brecha_recall, sub.recall, s=80)
seen = {}
for _, r in sub.iterrows():
    key = (round(r.brecha_recall, 3), round(r.recall, 3)); k = seen.get(key, 0); seen[key] = k + 1
    ax.annotate(r.modelo, (r.brecha_recall, r.recall), textcoords="offset points", xytext=(6, 6 - 12 * k), fontsize=8)
ax.axvline(gates["max_recall_gap"], color="red", ls="--", lw=1, label=f"tolerancia brecha {gates['max_recall_gap']}")
ax.axhline(gates["min_recall"], color="gray", ls=":", lw=1, label=f"recall mínimo {gates['min_recall']}")
ax.set(xlabel="Brecha de recall entre grupos", ylabel="Recall global", title="Utilidad frente a brecha (prueba)"); ax.legend(fontsize=8, loc="lower center")
fig.tight_layout(); fig.savefig(OUT / "tradeoff.png", dpi=160)

fig, ax = plt.subplots(figsize=(8, 4))
li = inter_all[inter_all.model.str.startswith("logistic (umbral 0.50")].set_index("grupo")
colors = ["#1f77b4" if s == "suficiente" else "#c7c7c7" for s in li.support]
ax.bar(li.index, li.recall, color=colors)
for i, (_, r) in enumerate(li.iterrows()): ax.text(i, r.recall + 0.02, f"n={int(r['count'])}", ha="center", fontsize=8)
ax.set(title=f"Recall interseccional, logistic 0.50 (gris: n < {MIN_SUPPORT}, no interpretable)", ylabel="Recall", ylim=(0, 1.15))
plt.xticks(rotation=30, ha="right"); fig.tight_layout(); fig.savefig(OUT / "intersectional_recall.png", dpi=160)

summary = {"validation_threshold": thr, "min_group_support": MIN_SUPPORT, "gates": gates,
           "test_size": int(len(test)), "test_by_group": test.protected_group.value_counts().to_dict(),
           "base_rate_by_group": test.groupby("protected_group").target.mean().round(3).to_dict()}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(comparison.round(3).to_string(index=False)); print(ci.round(3).to_string(index=False)); print(summary)
