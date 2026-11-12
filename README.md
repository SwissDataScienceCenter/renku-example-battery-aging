# renku-example-battery-aging

Adopt a colleague's project: battery ageing (Python, conda)

> **Training scenario.** "Alex" is a fictional colleague. The data and its authors are real: one coin cell cycled 1000 times on **Aurora**, Empa's robotic battery research platform.

## Your mission (30–40 min)

Alex has left for a six-month research stay. The group wants Alex's battery-ageing analysis on Renku, so that anyone can rerun it and show it without Alex's laptop. **You don't change the science.** Your job is to make the project run on Renku, end to end.

Read *Alex's handover note* below first, then work through the checklist. Stuck? Open [HINTS.md](HINTS.md) and reveal one hint at a time.

### Definition of done

- [ ] **Project.** A public Renku project, with this repository forked and linked as its code.
- [ ] **Input data.** Alex's dataset is connected to the project. *Not copied, not uploaded.*
- [ ] **Results storage.** A read/write data connector for results (PolyBox/SWITCHdrive or project storage).
- [ ] **Environment.** A session launcher whose environment is built from Alex's `environment.yml`.
- [ ] **Session.** `capacity_fade.py` runs in a session and its results land in your results connector, **without editing Alex's code**.
- [ ] **Job.** The same analysis runs as a Renku job, unattended, and its results persist after the job ends.
- [ ] **App.** Alex's dashboard is public: it opens from a share link in a browser window that is not logged in to Renku.
- [ ] **Hand over.** A colleague opens your session launch link and can rerun everything without asking you anything.

When everything is ticked, answer in one sentence each: *Where does the data live? What did you have to configure instead of changing the code? What can the public see?*

### Bonus

- Write the hand-over section Alex should have written: add "How to run this on Renku" to this README, commit and push it from your session.
- Start the job from your laptop with the [`rnk` CLI](https://docs.renkulab.io/en/latest/docs/users/cli/cli-reference/).
- Export your results connector to a **Zenodo draft** ([guide](https://docs.renkulab.io/en/latest/docs/users/data/guides/export-data-connector-to-zenodo)). Keep it a draft.

---

## Alex's handover note

Hi! Here's how I run the coin cell ageing analysis. It takes about 10 seconds on my laptop.

**Data.** I downloaded `empa__ccid000002.bdf.parquet` from the Zenodo record https://zenodo.org/records/15794498 (there's also a CSV version, but the parquet is 4× smaller) into my Downloads folder.

**Environment.**
```bash
conda env create -f environment.yml
conda activate battery-ageing
```
Note: we can't use the `defaults` channel, so the file uses `nodefaults` and conda-forge only.

**Analysis.**
```bash
python capacity_fade.py
```
It writes `cycles.csv`, `capacity_fade.png` and `summary.txt` into `figures/`. You can change where it reads and writes with the environment variables `CELL_DATA` and `OUT_DIR`.

**Dashboard.**
```bash
streamlit run dashboard.py
```
It shows `figures/cycles.csv` (set `CYCLES_CSV` to use another file). If that file isn't there, it recomputes everything from `CELL_DATA`.

**What's in the repo**

| File | What it does |
| --- | --- |
| `ageing.py` | Charge and discharge capacity per cycle (integrates current over time), coulombic efficiency, capacity retention |
| `capacity_fade.py` | The analysis: per-cycle table, figure, summary |
| `dashboard.py` | Streamlit dashboard with an adjustable end-of-life threshold |
| `environment.yml` | Conda environment (conda-forge, nodefaults) |

Good luck, and don't break my plots! — Alex

---

*Data: Svaluto-Ferro, E., Kimbell, G., Kim, Y., Plainpan, N., Kunz, B., Scholz, L., et al. (2025). Subset of dataset for publication "Toward an Autonomous Robotic Battery Materials Research Platform Powered by Automated Workflow and Ontologized FAIR Data Management". Zenodo. [doi:10.5281/zenodo.15794498](https://doi.org/10.5281/zenodo.15794498). CC BY 4.0. Publication: [doi:10.1002/batt.202500155](https://doi.org/10.1002/batt.202500155).*
