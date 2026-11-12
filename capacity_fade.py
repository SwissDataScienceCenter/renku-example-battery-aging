"""Capacity fade of one NMC//graphite coin cell over 1000 cycles.

Alex's analysis script. Runs on my laptop in about 10 seconds:

    python capacity_fade.py

Writes cycles.csv, capacity_fade.png and summary.txt to OUT_DIR.
"""
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ageing import cycles_to, load, per_cycle

# Where the data and the results are. Works on my machine!
CELL_DATA = os.environ.get("CELL_DATA", "/Users/alex/Downloads/empa__ccid000002.bdf.parquet")
OUT_DIR = Path(os.environ.get("OUT_DIR", "figures"))

print(f"Reading {CELL_DATA}")
cycles = per_cycle(load(CELL_DATA))
OUT_DIR.mkdir(parents=True, exist_ok=True)
cycles.to_csv(OUT_DIR / "cycles.csv", index=False)

last = cycles.iloc[-1]
n80 = cycles_to(cycles, 80)
summary = (f"Cycles analysed: {len(cycles)}\n"
           f"Discharge capacity, cycle 5: {cycles.loc[cycles.cycle == 5, 'discharge_mah'].iloc[0]:.3f} mAh\n"
           f"Discharge capacity, last cycle ({int(last.cycle)}): {last.discharge_mah:.3f} mAh\n"
           f"Retention after {int(last.cycle)} cycles: {last.retention_pct:.1f} %\n"
           f"First cycle below 80 % retention: {n80}\n"
           f"Median coulombic efficiency (cycles 10+): "
           f"{cycles.loc[cycles.cycle >= 10, 'coulombic_efficiency_pct'].median():.2f} %\n")
(OUT_DIR / "summary.txt").write_text(summary)
print(summary)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
ax1.plot(cycles.cycle, cycles.discharge_mah, ".", markersize=2)
ax1.set_ylabel("discharge capacity [mAh]")
ax1.set_title("NMC//graphite coin cell, Aurora platform (Empa)")
ax2.plot(cycles.cycle, cycles.coulombic_efficiency_pct, ".", markersize=2, color="tab:orange")
ax2.set_ylim(95, 101)
ax2.set_ylabel("coulombic efficiency [%]")
ax2.set_xlabel("cycle")
fig.tight_layout()
fig.savefig(OUT_DIR / "capacity_fade.png", dpi=120)
print(f"Saved results to {OUT_DIR.resolve()}")
