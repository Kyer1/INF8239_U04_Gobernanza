import numpy as np
import pandas as pd
from inf8239_u04.audit_ext import bootstrap_gap_ci, flag_support, threshold_for_recall


def test_bootstrap_gap_ci_contains_gap():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 200); pred = y.copy(); pred[:30] = 1 - pred[:30]
    groups = np.where(np.arange(200) < 100, "A", "B")
    r = bootstrap_gap_ci(y, pred, groups, "recall", n_boot=200)
    assert 0 <= r["ci_low"] <= r["gap"] <= r["ci_high"] <= 1


def test_identical_groups_have_zero_gap():
    y = np.array([1, 0, 1, 0] * 10); groups = np.array(["A"] * 20 + ["B"] * 20)
    r = bootstrap_gap_ci(y, y, groups, "recall", n_boot=50)
    assert r["gap"] == 0


def test_flag_support_marks_small_groups():
    t = pd.DataFrame({"count": [5, 25]}, index=["x", "y"])
    out = flag_support(t, 20)
    assert list(out.support) == ["insuficiente", "suficiente"]


def test_threshold_reaches_target_recall():
    y = np.array([1, 1, 1, 1, 0, 0, 0, 0]); p = np.array([.9, .8, .6, .4, .5, .3, .2, .1])
    thr = threshold_for_recall(y, p, 0.75)
    assert ((p >= thr) & (y == 1)).sum() / y.sum() >= 0.75
