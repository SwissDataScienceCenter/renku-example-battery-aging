"""Alex's dashboard: explore the capacity fade interactively.

    streamlit run dashboard.py

Shows the results of capacity_fade.py (CYCLES_CSV). If that file is not there,
it computes the cycles directly from the raw data (CELL_DATA).
"""
import os
from pathlib import Path

import plotly.express as px
import streamlit as st

from ageing import cycles_to, load, per_cycle

CYCLES_CSV = Path(os.environ.get("CYCLES_CSV", "figures/cycles.csv"))
CELL_DATA = os.environ.get("CELL_DATA", "/Users/alex/Downloads/empa__ccid000002.bdf.parquet")

st.set_page_config(page_title="Coin cell ageing", layout="wide")
st.title("How fast does this coin cell age?")
st.caption("NMC//graphite coin cell, 1000 cycles on Empa's Aurora platform · "
           "data: Zenodo doi:10.5281/zenodo.15794498 (CC BY 4.0)")


@st.cache_data
def get_cycles():
    import pandas as pd
    if CYCLES_CSV.exists():
        return pd.read_csv(CYCLES_CSV), f"results file {CYCLES_CSV}"
    if Path(CELL_DATA).exists():
        return per_cycle(load(CELL_DATA)), f"raw data {CELL_DATA}"
    return None, None


cycles, source = get_cycles()
if cycles is None:
    st.error(f"No data found. Looked for {CYCLES_CSV} and {CELL_DATA}.")
    st.stop()
st.caption(f"Computed from the {source}")

threshold = st.slider("End-of-life threshold [% of cycle-5 capacity]", 60, 95, 80)
n_eol = cycles_to(cycles, threshold)
c1, c2, c3 = st.columns(3)
c1.metric("Cycles recorded", len(cycles))
c2.metric("Capacity now", f"{cycles.retention_pct.iloc[-1]:.1f} %")
c3.metric(f"First cycle below {threshold} %", n_eol if n_eol else "not reached")

fig = px.scatter(cycles, x="cycle", y="retention_pct", labels={"retention_pct": "capacity retention [%]"})
fig.add_hline(y=threshold, line_dash="dash", line_color="red")
st.plotly_chart(fig, width="stretch")
st.plotly_chart(px.scatter(cycles[cycles.cycle >= 5], x="cycle", y="coulombic_efficiency_pct",
                           labels={"coulombic_efficiency_pct": "coulombic efficiency [%]"}), width="stretch")
