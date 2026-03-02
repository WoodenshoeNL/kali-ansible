# Plan: Use uv for Python Tools in kali-ansible

## Current state

- **uv** is already installed via pipx in `roles/Common/tasks/uv.yml` and runs as `{{ login_user }}`. It is not yet used for any tool installation.
- Python tools in the repo use three patterns:
  1. **pipx** – CLI tools (bloodhound-python, sherlock, holehe, mitm6, netexec, evil-winrm-py, DonPAPI, enum4linux-ng, maigret, changedetection, beads, etc.).
  2. **venv + pip** – Git clone (or dir) + `python3 -m venv` + `ansible.builtin.pip` or shell `pip install -r requirements.txt`: Certipy, gMSADumper, SCCMHunter, spiderfoot, recon-ng, carbon14, blackbird, whatsmyname, ntdsdotsqlite, scoutsuite, roadtx, roadrecon, SeamlessPass, meowEye.
  3. **System pip** – impacket, BloodyAD (with `--break-system-packages`).

---

## What uv can do here

| Current pattern        | uv equivalent / improvement |
|------------------------|-----------------------------|
| `python3 -m venv`      | `uv venv` (faster; can pin Python with `--python 3.12`) |
| `pip install -r reqs`  | `uv pip install -r requirements.txt` in that venv |
| `pip install <pkg>`    | `uv pip install <pkg>` in that venv |
| pipx install &lt;pkg&gt;   | `uv tool install <pkg>` (optional migration) |

Benefits: faster installs, better resolver, lockfiles possible with `pyproject.toml`, optional Python version pinning per tool.

---

## What has to change

### 1. Ansible side

- There is **no built-in Ansible module for uv**. Two options:
  - **A (recommended):** Use `command` / `shell` to run `uv venv`, `uv pip install ...` with `become_user: "{{ login_user }}"` and correct `PATH` (so `uv` from pipx is found).
  - **B:** Use the **moreati.uv** Galaxy collection (`moreati.uv.pip`). There is a known issue: uv-created venvs may lack the `packaging` module required by that collection; would need testing and possibly a workaround.

Recommendation: start with **option A** (shell/command) for predictability and no extra collection dependency.

### 2. Ensure uv is available before use

- uv is already installed in the Common role. Any role that uses uv must run after Common (current playbook order is already correct).
- When calling uv from Ansible, run as `{{ login_user }}` and ensure pipx’s path is in the environment (e.g. `PATH: "{{ login_home }}/.local/bin:{{ ansible_env.PATH }}"`) so `uv` is found.

### 3. Per-tool task changes (venv + pip tools)

For each task file that currently does **venv + pip**:

| Step today                | Change to (uv) |
|---------------------------|----------------|
| `command: python3 -m venv "{{ login_home }}/.../venv"` | `command: uv venv "{{ login_home }}/.../venv"` (or `uv venv --python 3` if you want to pin). |
| `pip: requirements: ... virtualenv: ...` | `shell` or `command`: `uv pip install -r requirements.txt` with `virtualenv: "{{ login_home }}/.../venv"` expressed by using that venv’s Python: e.g. `"{{ login_home }}/.../venv/bin/uv" pip install ...` is not standard; instead run `uv pip install --python "{{ login_home }}/.../venv/bin/python" -r requirements.txt` from the project dir, or `uv pip install --python "{{ login_home }}/.../venv/bin/python" -r requirements.txt` with `chdir` set to the repo. |
| `pip: name: <pkg> virtualenv: ...` (single package) | `command: uv pip install --python "{{ login_home }}/.../venv/bin/python" <pkg>` (and optionally `state: latest` by running with `--upgrade` when desired). |
| Wrapper script / symlink  | No change: keep pointing at `venv/bin/python` or `venv/bin/<tool>`. |

Concrete example for **Certipy** (single package in venv):

- Create venv: `uv venv "{{ login_home }}/certipy/venv"`.
- Install: `uv pip install --python "{{ login_home }}/certipy/venv/bin/python" certipy-ad` (add `--upgrade` for “latest” behavior).
- Symlink/wrapper unchanged: `venv/bin/certipy-ad`.

For **gMSADumper** (clone + requirements.txt):

- Create venv: `uv venv "{{ login_home }}/gmsadumper/venv"`.
- Install: `uv pip install --python "{{ login_home }}/gmsadumper/venv/bin/python" -r "{{ login_home }}/gmsadumper/requirements.txt"` with `chdir: "{{ login_home }}/gmsadumper"` (so relative paths in requirements.txt work if any).
- Wrapper script unchanged.

Special cases:

- **spiderfoot**: custom steps (lxml first, then pip from filtered requirements). Same idea: create venv with `uv venv`, then two `uv pip install` steps (one for lxml, one for the rest from filtered list or file).
- **meowEye** (under `/opt`): if you keep it system-wide, ensure the user that runs the play has permission to create `/opt/meowEye/venv`; venv creation and install steps still switch to `uv venv` + `uv pip install --python /opt/meowEye/venv/bin/python ...`.

### 4. Optional: pipx → uv tool

- For tools that are **only** installed via pipx (no venv), you can optionally switch to `uv tool install <pkg>` so they live under uv’s tool directory (and share uv’s speed and resolver).
- This requires:
  - Ensuring `uv`’s tool path is on `PATH` for `{{ login_user }}` (uv documents where it puts tools; often compatible with `~/.local/bin` or similar).
  - Replacing each `community.general.pipx` block with a task that runs `uv tool install <pkg>` (and optionally `uv tool install --upgrade` for “latest”).
- Not required for “using uv more”; only if you want to standardize on uv for both venv-based and tool-based installs.

### 5. System-pip tools (impacket, BloodyAD)

- Can stay as-is, or later be moved into a dedicated venv managed by uv (e.g. `uv venv` + `uv pip install impacket`) and then symlink/copy scripts into a path on `PATH`. That would avoid `--break-system-packages` and isolate deps. Low priority unless you want to phase out system pip.

---

## Suggested order of work

1. **Decide scope**
   - Minimum: use uv only for **venv + pip** tools (leave pipx and system pip as-is).
   - Optional: also migrate **pipx** → **uv tool install** and/or move **impacket/BloodyAD** into uv-managed venvs.

2. **Environment**
   - In a single place (e.g. Common role or a shared vars file), define how `uv` is invoked for `{{ login_user }}` (e.g. `PATH` including `{{ login_home }}/.local/bin`). Use that in all uv tasks.

3. **Template migration (one or two tools)**
   - Migrate **Certipy** (single package) and **gMSADumper** (requirements.txt) to uv venv + uv pip.
   - Confirm idempotency (re-running playbook doesn’t break, and upgrades work when you want “latest”).

4. **Roll out to all venv-based tools**
   - Apply the same pattern to: SCCMHunter, spiderfoot, recon-ng, carbon14, blackbird, whatsmyname, ntdsdotsqlite, scoutsuite, roadtx, roadrecon, SeamlessPass, meowEye.
   - Adjust only where there are special cases (e.g. spiderfoot’s lxml + filtered requirements).

5. **Optional: pipx → uv tool**
   - Replace pipx installs with `uv tool install` for chosen tools; test PATH and wrappers.

6. **Docs**
   - Update **agent.md** (§5.3, §5.4, Quick Reference) to describe the uv-based venv + pip pattern and, if you did it, the uv tool pattern.
   - Update **install.md** (and any other user-facing docs) if they mention `pip`/`venv` for these tools.

---

## File checklist (venv + pip → uv)

| Role   | Task file            | Notes |
|--------|----------------------|--------|
| AD     | Certipy.yml          | Single pkg: uv venv + uv pip install certipy-ad |
| AD     | gmsadumper.yml       | requirements.txt: uv venv + uv pip install -r |
| AD     | SCCMHunter.yml       | requirements.txt |
| AD     | ntdsdotsqlite.yml    | Single pkg (ntdsdotsqlite) |
| OSINT  | spiderfoot.yml       | lxml first, then filtered requirements |
| OSINT  | recon-ng.yml         | REQUIREMENTS file |
| OSINT  | carbon14.yml         | requirements.txt |
| OSINT  | blackbird.yml        | requirements.txt |
| OSINT  | whatsmyname.yml      | requirements.txt |
| Cloud  | scoutsuite.yml       | Single pkg (scoutsuite) |
| Cloud  | Roadtx.yml           | Single pkg (roadtx) |
| Cloud  | Roadrecon.yml        | Single pkg (roadrecon) |
| Cloud  | SeamlessPass.yml     | Single pkg (seamlesspass) |
| Web    | meowEye.yml          | /opt path, requirements.txt |

---

## Summary

- **Required for “use uv more”:**  
  Use **uv venv** and **uv pip install** for every tool that currently uses **venv + pip**, and ensure uv is on PATH when Ansible runs those tasks.
- **Optional:**  
  Migrate **pipx** → **uv tool install**; move **impacket/BloodyAD** into uv-managed venvs.
- **Mechanics:**  
  Use `command`/`shell` with `uv venv` and `uv pip install --python <venv_python> ...`, running as `{{ login_user }}` with PATH that includes the directory where pipx installed uv (e.g. `~/.local/bin`).

Once the first two tasks (Certipy, gMSADumper) are done, the rest are the same pattern with different paths and package/requirements files.
