# Hints

Open one hint at a time. The first hint nudges; the second gives the answer.

## Project

<details><summary>Hint 1</summary>

Fork first (on GitHub), then create the Renku project and link the **fork**: you will push to it later.
</details
>
<details><summary>Hint 2</summary>

Renku → *Create project* → visibility **public** (the app needs it)
Renku project →*Code* ➕ → paste your fork's clone URL.
</details>

## Input data

<details><summary>Hint 1</summary>

Alex gives a Zenodo record URL. Renku can mount Zenodo datasets by their **DOI**. What's this record's DOI?
</details>
<details><summary>Hint 2</summary>

*Data* ➕ → **Link a data connector** → `10.5281/zenodo.15794498` → **Link**. 
In a session, the files appear in a folder under `/home/renku/work/`: run `ls /home/renku/work` to see its name.
</details>

## Results storage

<details><summary>Hint 1</summary>

The DOI connector is read-only, and anything written elsewhere in a session or job disappears. You need storage you can write to.
</details>

<details><summary>Hint 2</summary>

Connect a PolyBox or SWITCHdrive folder with **write** access ([guide](https://docs.renkulab.io/en/latest/docs/users/data/guides/connect-data/connect-shared-switchdrive-or-polybox-folder-to-project/)), mount point `results`.
</details>

## Environment

<details><summary>Hint 1</summary>

Renku can build an environment straight from the dependency file in a code repository.
</details>
<details><summary>Hint 2</summary>

*Launchers* ➕ → **Session launcher** → **Create from code** → Code repository: your repository → Environment type: Python → User interface: JupyterLab or VS Code. Renku detects `environment.yml`. The first build takes a few minutes: read on while it runs.
</details>

## Session

<details><summary>Hint 1</summary>

Don't edit `capacity_fade.py`. Alex already made the paths configurable: look at the top of the script.
</details>
<details><summary>Hint 2</summary>
Click on the **Session Launcher** so the right hand-side menu appears. Scroll down to Environment Variables and click on the Edit button.

Add two Environment variables and **Update the session launcher**.
*MY_ENV_VAR* → **CELL_DATA** → *value* → **/home/renku/work/<doi-folder>/empa__ccid000002.bdf.parquet** (replace `<doi-folder>` with the folder name from `ls /home/renku/work`))

Start a new session and in the terminal you can run:

```bash
python /home/renku/work/renku-adopt-battery-ageing/capacity_fade.py
```
Expected: about 1.66 mAh at cycle 5, about 60 % retention after 1000 cycles, first drop below 80 % around cycle 400, coulombic efficiency close to 99 %.
</details>

## Job

<details><summary>Hint 1</summary>

A job runs one command, with no terminal to type `export` in. Where else can environment variables be set?
</details>
<details><summary>Hint 2</summary>

*Launchers* ➕ → **Job Launcher** → **Create from code** → your repository.
- Job command: `["python", "renku-adopt-battery-ageing/capacity_fade.py"]`
- Environment variables on the launcher: `CELL_DATA` and `OUT_DIR`, the same values as in the session.

**Submit**, read the logs, then check `results/battery/` in a session or in your PolyBox.
</details>

## App

<details><summary>Hint 1</summary>

An app needs two things Alex's laptop didn't: a `Procfile` saying how to start it, and data that a **logged-out visitor** is allowed to see.
</details>
<details><summary>Hint 2</summary>

1. In a session, create `Procfile` in the repository root with this single line, then commit and push it:
   ```
   web: streamlit run dashboard.py --server.port $RENKU_SESSION_PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false
   ```
2. *Launchers* ➕ → **App Launcher** → **Create from code** → your repository.
3. Apps mount only public, credential-free data: **not** your PolyBox results. Point the dashboard at the public DOI data instead: set `CELL_DATA` on the app launcher to the DOI path. The dashboard then recomputes the cycles itself.
4. **Start** → *Live* → **Open** → **Copy share link** → open it in a private browser window.

If the app launcher doesn't offer environment variables, change the default value of `CELL_DATA` in `dashboard.py`, push, and restart the app.
</details>

## Hand over

<details><summary>Hint 1</summary>

Your colleague should not need to know any of the paths you just figured out.
</details>
<details><summary>Hint 2</summary>

Share the session launch link ([guide](https://docs.renkulab.io/en/latest/docs/users/compute/session/guides/share-session-launch-link/)). Your colleague needs their own write access to the results storage: credentials are never shared through Renku.
</details>
