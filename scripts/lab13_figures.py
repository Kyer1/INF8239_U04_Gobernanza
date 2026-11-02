"""Figura de monitoreo: operación normal frente al simulacro de incidente."""
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from inf8239_u04.governance import load_config

cfg = load_config()["monitoring"]
normal = pd.read_csv("reports/lab13/monitoring.csv"); inc = pd.read_csv("reports/lab13/incident/monitoring_incident.csv")
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, metric, limit, title in [(axes[0], "recall", cfg["alert_recall"], "Recall por ventana"),
                                 (axes[1], "recall_gap", cfg["alert_recall_gap"], "Brecha de recall por ventana")]:
    for df, label, style in [(normal, "operación normal", "o-"), (inc, "simulacro (falla zona Norte)", "s--")]:
        d = df[df.status != "INSUFICIENTE"]; ax.plot(d.window, d[metric], style, label=label)
    ax.axhline(limit, color="red", ls=":", lw=1, label=f"umbral {limit}")
    ax.set_title(title); ax.set_ylim(0, 1 if metric == "recall" else 0.4)
axes[0].legend(fontsize=8, loc="lower left")
axes[1].text(0.02, 0.95, "Oct y dic: brechas no evaluables (grupo n < 20)", transform=axes[1].transAxes, fontsize=8, va="top")
fig.tight_layout(); Path("reports/lab13").mkdir(parents=True, exist_ok=True); fig.savefig("reports/lab13/monitoring.png", dpi=160)
print("reports/lab13/monitoring.png")
