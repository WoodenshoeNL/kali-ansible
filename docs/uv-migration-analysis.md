# UV Migration: Analysis and Plan

## Executive Summary

The kali-ansible project uses **pip**, **pipx**, and **venv** across 25+ task files. All of these can be replaced with **uv**, which provides faster installs, better dependency resolution, and a single toolchain. This document analyzes current usage and provides a phased migration plan.

---

## 1. Current Usage Inventory

### 1.1 uv Installation (bootstrap)

| File | Current | Notes |
|------|---------|-------|
| `roles/Common/tasks/uv.yml` | `community.general.pipx` installs uv | **Change:** Use standalone installer (no pipx dependency) |

**Standalone uv installer** (no Python/pip/pipx required):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Installs to `~/.local/bin` (or `~/.cargo/bin` on some systems). Use `get_url` + `command` or `shell` in Ansible.

---

### 1.2 pipx → uv tool (CLI tools)

| Role | Task File | Package | Source | Notes |
|------|-----------|---------|--------|-------|
| Common | uv.yml | uv | pipx | → standalone installer (see 1.1) |
| AD | bloodhound-python.yml | bloodhound-python | PyPI | Simple |
| AD | bloodhound-python.yml | bloodhound-ce-python | PyPI | Simple |
| AD | DonPAPI.yml | donpapi | PyPI | **Special:** `--pip-args="--only-binary lxml"` + inject setuptools |
| AD | dploot.yml | dploot | PyPI | Simple |
| Network | mitm6.yml | mitm6 | PyPI | Simple |
| Network | netexec.yml | netexec | git+https | **Special:** `source: git+https://...` (Ubuntu fallback) |
| Network | evil-winrm-py.yml | evil-winrm-py[kerberos] | PyPI | **Already uses uv** ✓ |
| Network | Enum4linux-ng.yml | enum4linux-ng | PyPI | Simple |
| OSINT | sherlock.yml | sherlock-project | PyPI | Simple |
| OSINT | holehe.yml | holehe | PyPI | Simple |
| OSINT | theharvester.yml | theHarvester | git+https | **Special:** from git |
| OSINT | changedetection.yml | changedetection.io | PyPI | Simple |
| OSINT | maigret.yml | maigret | PyPI | Simple |
| OSINT | sublist3r.yml | sublist3r | PyPI | Simple |
| Extra | beads.yml | beads-mcp | PyPI | Simple (beads itself uses install script, not pipx) |

**uv tool install** supports:
- PyPI packages: `uv tool install <pkg>`
- Git: `uv tool install "package @ git+https://github.com/org/repo.git"` (PEP 508 URL spec)
- Extras: `uv tool install "evil-winrm-py[kerberos]"`

---

### 1.3 venv + pip → uv venv + uv pip (project-based tools)

| Role | Task File | Path | Requirements | Notes |
|------|-----------|------|--------------|-------|
| AD | Certipy.yml | ~/certipy/venv | certipy-ad (single pkg) | Symlink to /usr/local/bin |
| AD | gmsadumper.yml | ~/gmsadumper/venv | requirements.txt | Wrapper script |
| AD | SCCMHunter.yml | ~/sccmhunter/venv | requirements.txt | pip creates venv; wrapper |
| AD | ntdsdotsqlite.yml | ~/ntdsdotsqlite/venv | ntdsdotsqlite (single) | Symlink |
| Cloud | scoutsuite.yml | ~/scoutsuite/venv | scoutsuite (single) | Symlink |
| Cloud | Roadtx.yml | ~/roadtx/venv | roadtx (single) | Symlink |
| Cloud | Roadrecon.yml | ~/roadrecon/venv | roadrecon (single) | Symlink |
| Cloud | SeamlessPass.yml | ~/seamlesspass/venv | seamlesspass (single) | Symlink |
| OSINT | spiderfoot.yml | ~/Programs/spiderfoot/venv | **Special:** lxml first, then grep -v lxml | Two-step install |
| OSINT | recon-ng.yml | ~/Programs/recon-ng/venv | REQUIREMENTS (not .txt) | Different filename |
| OSINT | carbon14.yml | ~/Programs/Carbon14/venv | requirements.txt | Standard |
| OSINT | blackbird.yml | ~/Programs/blackbird/venv | requirements.txt | Standard |
| OSINT | whatsmyname.yml | ~/Programs/WhatsMyName-Python/venv | requirements.txt | Standard |
| Web | meowEye.yml | /opt/meowEye/venv | requirements.txt | **Special:** /opt, runs as root |

---

### 1.4 System pip (--break-system-packages)

| Role | Task File | Package | Notes |
|------|-----------|---------|-------|
| Common | im_packet.yml | impacket | Installs to user site-packages |
| AD | BloodyAD.yml | bloodyAD | Ubuntu only; Kali uses apt |

**Migration:** Create dedicated venv (e.g. `~/impacket/venv`), install with uv, symlink scripts to `/usr/local/bin` or ensure `~/.local/bin` on PATH.

---

## 2. Dependencies to Remove or Reduce

After full migration:

| Package | Location | Action |
|---------|----------|--------|
| pipx | roles/Common/tasks/main.yml (apt) | Remove (or keep only if other roles need it) |
| python3-pip | roles/Common/tasks/main.yml | Can remove if no other use |
| python3-virtualenv | roles/Common/tasks/main.yml | Can remove |
| community.general | requirements.yml / Galaxy | Still needed for: npm, ufw. pipx usage can be removed. |

---

## 3. Special Cases and Gotchas

### DonPAPI
- pipx: `pipx install donpapi --pip-args="--only-binary lxml"` then `pipx inject donpapi setuptools`
- uv: `uv tool install donpapi --only-binary lxml --with setuptools`. uv supports `--only-binary` (same as pip). The system package `python3-lxml` is already installed by DonPAPI task; uv tool uses its own venv, so `--only-binary lxml` ensures we use wheels and avoid build issues.

### theHarvester (git source)
- pipx: `source: git+https://github.com/laramies/theHarvester.git`
- uv: `uv tool install "theHarvester @ git+https://github.com/laramies/theHarvester.git"`

### netexec (git source, Ubuntu fallback)
- pipx: `source: git+https://github.com/Pennyw0rth/NetExec.git`
- uv: `uv tool install "netexec @ git+https://github.com/Pennyw0rth/NetExec.git"`

### spiderfoot
- Two-step: install lxml>=5.0 first, then `grep -v lxml requirements.txt | pip install -r /dev/stdin`
- uv: `uv pip install --python <venv>/bin/python lxml>=5.0` then `uv pip install --python <venv>/bin/python -r <(grep -v lxml requirements.txt)` or use a temp filtered file

### recon-ng
- Uses `REQUIREMENTS` (no .txt extension). uv accepts any requirements file path.

### meowEye
- Installed under `/opt`, runs as root. Ensure uv is available for root (install uv system-wide or in /usr/local/bin).

---

## 4. uv PATH and Environment

All uv commands must run with:
- `become_user: "{{ login_user }}"` (for user installs)
- `environment: { PATH: "{{ login_home }}/.local/bin:{{ ansible_env.PATH }}" }`

If uv is installed via standalone script as `{{ login_user }}`, it goes to `~/.local/bin`. If installed system-wide (e.g. `/usr/local/bin`), PATH may already include it.

---

## 5. Migration Plan (Phased)

### Phase 0: Bootstrap uv without pipx
**Goal:** Install uv via standalone script so we can remove pipx dependency for uv itself.

1. Replace `roles/Common/tasks/uv.yml`:
   - Use `get_url` to fetch `https://astral.sh/uv/install.sh`
   - Run install script as `{{ login_user }}` (or use `curl -LsSf ... | sh`)
   - Ensure `~/.local/bin` is in PATH for subsequent tasks

2. **Order:** uv must run before any role that uses uv. Current order (Common before others) is correct.

---

### Phase 1: venv + pip → uv venv + uv pip (high impact, low risk)

**Pattern per file:**
```yaml
# OLD
- command: python3 -m venv "{{ path }}/venv"
- pip: name: X  virtualenv: "{{ path }}/venv"

# NEW
- command: uv venv "{{ path }}/venv"
  environment: { PATH: "{{ login_home }}/.local/bin:{{ ansible_env.PATH }}" }
- command: uv pip install --python "{{ path }}/venv/bin/python" X
  # or: uv pip install --python "{{ path }}/venv/bin/python" -r requirements.txt
  # with chdir for relative paths in requirements
```

**Order of migration (easiest first):**
1. Certipy (single pkg)
2. gMSADumper (requirements.txt)
3. ntdsdotsqlite, scoutsuite, Roadtx, Roadrecon, SeamlessPass (single pkg each)
4. carbon14, blackbird, whatsmyname, recon-ng (requirements)
5. SCCMHunter (pip creates venv; change to explicit uv venv first)
6. spiderfoot (two-step lxml + filtered requirements)
7. meowEye (/opt, root)

---

### Phase 2: pipx → uv tool (standardize CLI tools)

**Pattern:**
```yaml
# OLD
- community.general.pipx:
    name: mitm6
    state: latest

# NEW
- command: uv tool install --upgrade mitm6
  become_user: "{{ login_user }}"
  environment: { PATH: "{{ login_home }}/.local/bin:{{ ansible_env.PATH }}" }
```

**Order:**
1. Simple PyPI tools: mitm6, sherlock, holehe, changedetection, maigret, sublist3r, beads-mcp, dploot, enum4linux-ng, bloodhound-python, bloodhound-ce-python
2. Git sources: theHarvester, netexec (Ubuntu fallback)
3. DonPAPI (special pip-args; test carefully)

---

### Phase 3: System pip → uv venv (impacket, BloodyAD)

1. **impacket:** Create `~/impacket/venv` (or `/opt/impacket/venv`), install with uv, symlink/copy `impacket-*` scripts to `/usr/local/bin`
2. **BloodyAD:** Same pattern for Ubuntu path (Kali uses apt)

---

### Phase 4: Cleanup

1. Remove `pipx` from apt packages in Common (if no longer needed)
2. Remove `python3-pip` and `python3-virtualenv` if unused
3. Update `install.md`, `agent.md`, and tool docs
4. Update `docs/uv-migration-plan.md` to reflect completion

---

## 6. File Checklist (Quick Reference)

| Category | Files to Modify | Status |
|----------|-----------------|--------|
| **uv bootstrap** | roles/Common/tasks/uv.yml | Done (Phase 0) |
| **venv+pip** | Certipy, gmsadumper, SCCMHunter, ntdsdotsqlite, scoutsuite, Roadtx, Roadrecon, SeamlessPass, spiderfoot, recon-ng, carbon14, blackbird, whatsmyname, meowEye | Done (Phase 1) |
| **pipx** | bloodhound-python, DonPAPI, dploot, mitm6, netexec, Enum4linux-ng, sherlock, holehe, theharvester, changedetection, maigret, sublist3r, beads |
| **system pip** | im_packet, BloodyAD |
| **apt cleanup** | roles/Common/tasks/main.yml |

---

## 7. Testing Strategy

- Run playbook with `--tags` for one role at a time (e.g. `--tags certipy`)
- Verify idempotency: run twice, second run should show no changes
- For tools: run the binary (e.g. `certipy-ad -h`, `mitm6 -h`) to confirm it works
- For venv tools with wrappers: test the wrapper script

---

## 8. Rollback

If issues arise, revert the modified task files. The old pip/pipx/venv approach remains valid; no data loss. uv and pipx can coexist during migration.
