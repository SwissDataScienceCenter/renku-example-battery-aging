"""Cycle-level metrics for a coin cell cycled on Empa's Aurora robotic platform.

Input: the battery data format (BDF) time series published on Zenodo
(doi:10.5281/zenodo.15794498), as .parquet or .csv, with the columns
test_time_millisecond, current_ampere, voltage_volt, cycle_dimensionless, ...
Positive current = charge, negative current = discharge.
"""
from pathlib import Path

import numpy as np
import pandas as pd

COLUMNS = ["test_time_millisecond", "current_ampere", "voltage_volt", "cycle_dimensionless"]


def load(path):
    path = Path(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path, columns=COLUMNS)
    return pd.read_csv(path, usecols=COLUMNS)


def per_cycle(raw, reference_cycle=5):
    """Charge/discharge capacity (mAh), coulombic efficiency and retention per cycle."""
    df = raw.sort_values("test_time_millisecond")
    dt_h = df.test_time_millisecond.diff().fillna(0).to_numpy() / 3.6e6
    i_mid = (df.current_ampere + df.current_ampere.shift(1).fillna(0)).to_numpy() / 2
    charge_mah = np.where(i_mid > 0, i_mid * dt_h * 1000, 0.0)
    discharge_mah = np.where(i_mid < 0, -i_mid * dt_h * 1000, 0.0)
    cycle = df.cycle_dimensionless.shift(1).fillna(df.cycle_dimensionless.iloc[0]).astype(int).to_numpy()

    out = pd.DataFrame({"cycle": cycle, "charge_mah": charge_mah, "discharge_mah": discharge_mah}) \
        .groupby("cycle", as_index=False).sum()
    out = out[out.discharge_mah > 0].copy()
    out["coulombic_efficiency_pct"] = 100 * out.discharge_mah / out.charge_mah
    ref = out.loc[out.cycle == reference_cycle, "discharge_mah"]
    ref = ref.iloc[0] if len(ref) else out.discharge_mah.iloc[0]
    out["retention_pct"] = 100 * out.discharge_mah / ref
    return out.round(4).reset_index(drop=True)


def cycles_to(cycles, threshold=80.0):
    below = cycles[cycles.retention_pct < threshold]
    return int(below.cycle.iloc[0]) if len(below) else None
