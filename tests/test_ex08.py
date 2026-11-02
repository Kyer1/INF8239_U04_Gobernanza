import pandas as pd
import pytest

from inf8239_u04.data import FEATURES, load_data, temporal_split
from inf8239_u04.governance import deployment_decision, load_config, roles, validate_raci
from inf8239_u04.incident import inject_registry_failure, zero_rate_check
from inf8239_u04.inventory import minimize, validate_handoff, validate_inventory, validate_retention
from inf8239_u04.monitoring import monitor, psi

CFG = load_config(); DF = load_data()
INV = pd.read_csv("student_inputs/data_inventory.csv")
GATES = {"min_recall": .7, "max_recall_gap": .2, "max_fpr_gap": .2, "max_latency_ms": 10, "max_model_kb": 20}
RES = {"latency_ms": 1, "model_kb": 5}


def test_inventory_covers_every_column_and_no_sensitive_predictor():
    assert validate_inventory(INV, DF, CFG)
    assert not set(FEATURES[CFG["model_kind"]]) & set(CFG["sensitive_features"])


def test_inventory_rejects_uninventoried_column():
    with pytest.raises(ValueError): validate_inventory(INV, DF.assign(extra=1), CFG)


def test_operator_view_is_minimized():
    view = minimize(DF, INV)
    assert "protected_group" not in view and "age_band" not in view


def test_retention_and_handoff_are_complete_and_roles_exist():
    raci = pd.read_csv("student_inputs/raci.csv")
    assert validate_retention(pd.read_csv("student_inputs/retention.csv"))
    assert validate_handoff(pd.read_csv("student_inputs/handoff.csv"), roles(raci))


def test_raci_requires_exactly_one_accountable():
    assert validate_raci(pd.read_csv("student_inputs/raci.csv"))
    with pytest.raises(ValueError):
        validate_raci(pd.DataFrame([{"activity": "deploy", "R": "ML", "A": "PO, Owner", "C": "DS", "I": "Users"}]))


def test_low_recall_plus_gap_stops():
    d = deployment_decision({"recall": .5}, {"recall_gap": .3, "fpr_gap": .1}, RES, GATES)
    assert d["status"] == "STOP" and "baseline" in d["human_action"]


def test_psi_is_small_for_same_distribution_and_large_for_shift():
    ref = DF.exposure
    assert psi(ref, ref) < 0.01 and psi(ref, ref + 0.5) > 0.25


def test_monitor_does_not_alert_gaps_on_small_groups():
    train, test = temporal_split(DF)
    mon = monitor(train, test.assign(pred=test.target), CFG["monitoring"], 20)
    small = mon[mon.min_group_n < 20]
    assert not small.alerts.str.contains("brecha de recall").any()
    assert "acumulado" in set(mon.window)


def test_registry_failure_is_detected_without_labels():
    train, test = temporal_split(DF)
    bad, n = inject_registry_failure(test)
    table = zero_rate_check(train, bad[bad.received_date >= "2026-11-01"])
    assert n > 0 and table.loc["Norte", "alert"] and table.alert.sum() == 1
