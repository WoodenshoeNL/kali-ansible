# kali-ansible — Agent Guide for Adding Tasks

This document helps AI agents and contributors add new tasks to the kali-ansible playbook consistently with existing patterns.

---

## 1. Project Overview

**Purpose**: Ansible playbook to provision fresh Kali (or Ubuntu) VMs with security/AD/cloud/OSINT tooling.

**Key files**:
- `playbook.yml` — Single play, `hosts: all`, `gather_facts: yes`, `become: true`. Runs roles in order.
- `run.md` — How to run Ansible (VMware Workstation, remote VM, laptop, Ubuntu, tags).
- `bootstrap.sh` — Minimal VM bootstrap: `apt install git ansible open-vm-tools-desktop`, mount VMShare, then run the playbook.
- `requirements.yml` — Ansible Galaxy collections (e.g. `community.general` for `pipx`). Install with `ansible-galaxy install -r requirements.yml` if needed.

**Roles** (order matters):
1. **Common** — Base system, docker, pipx, golang, tmux, Firefox, stockpile, etc.
2. **Web** — Feroxbuster, Nuclei, httpx, Burp, etc.
3. **Cloud** — Azure CLI, Roadrecon, ScoutSuite, etc.
4. **AD** — BloodHound CE, Certipy, kerbrute, ldapx, etc.
5. **Network** — Nmap, hashcat, mitm6, evil-winrm, etc.
6. **OSINT** — Sherlock, theHarvester, Maltego, etc.
7. **Extra** — Mullvad, n8n, Cursor, Tor Browser, Terraform, etc.
8. **Tools** — Placeholder; currently empty.

---

## 2. How to Run (from `run.md`)

| Target | Command |
|--------|---------|
| **VMware Workstation** | `cd /share/VMShare/kali-ansible` then `sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=workstation login_user=kali login_home=/home/kali"` |
| **Remote VM** | `ansible-playbook -i '10.10.10.10,' -u kali --private-key ~/.ssh/key -e 'ansible_python_interpreter=/usr/bin/python3' --become playbook.yml -e "vmware_env=esx login_user=kali login_home=/home/kali"` |
| **Laptop** | Clone repo, then `sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=laptop login_user=kali login_home=/home/kali"` |
| **Ubuntu** | `sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=ubuntu login_user=michel login_home=/home/michel"` |
| **Tags** | Append `--tags <tag>` e.g. `--tags core`, `--tags nmap`, `--tags AD`. |

**Variables always passed via `-e`**:
- `vmware_env` — `workstation` \| `laptop` \| `ubuntu` \| `esx` \| `cursor` \| `n8n` \| `claude_code` \| `ubuntu_terraform` etc.
- `login_user` — Unix user (e.g. `kali`, `michel`).
- `login_home` — Home directory (e.g. `/home/kali`, `/home/michel`).

---

## 3. Role and Task Structure

### 3.1 Role layout

```
roles/
  <RoleName>/
    files/           # Static files, configs, optional *Tools.txt
    tasks/
      main.yml       # Imports; optionally copies *Tools.txt
      <tool>.yml     # One file per tool
```

### 3.2 Domain roles (AD, Web, Cloud, Network, OSINT)

- **main.yml**:
  1. *(Optional)* Copy `*_Tools.txt` to `{{ login_home }}` with `become: false`, `mode: "0644"`. Tag: role name (e.g. `AD`, `web`).
  2. `import_tasks: <tool>.yml` for each tool, in a sensible order.

- **files/**:
  - `*_Tools.txt` — Reference: tool name, usage, description, OPSEC notes, GitHub. See `roles/AD/files/AD_Tools.txt` and `roles/Web/files/Web_Tools.txt`.
  - Tool-specific configs (e.g. `bloodHoundCE/` with `.env`, `docker-compose.yml`) when needed.

### 3.3 Common role

- No `*_Tools.txt`. `main.yml` does cleanup, apt upgrade, core packages, vmware mount, then `import_tasks` for tmux, firefox, stockpile, powershell, impacket, vscode, chrome, obsidian, rust, duckdb, foxyproxy, etc.

### 3.4 Extra role

- No `*_Tools.txt`. Only `import_tasks` for mullvad, n8n, cursor, antigravity, claude-code, tor-browser, terraform. Some tasks run only when `vmware_env` matches (e.g. `cursor`, `n8n`).

---

## 4. Task File Conventions

### 4.1 Naming

- **Task file**: `kebab-case.yml` (e.g. `bloodhound-python.yml`, `evil-winrm-py.yml`). Some use PascalCase (e.g. `GoWitness.yml`) — prefer kebab-case for new ones.
- **Task names**: Prefix with `ToolName - `, e.g. `nmap - install nmap package`, `mitm6 - install/upgrade mitm6 via pipx`.

### 4.2 Tags

**Every task must have tags.** Use:

1. **Tool tag** — Lowercase, matches tool (e.g. `nmap`, `mitm6`, `certipy`, `bloodhound-python`).
2. **Role tag** — Matches role: `common`, `web`, `cloud`, `AD`, `network`, `OSINT`. (Case follows existing role usage.)

Example:
```yaml
tags:
  - mitm6
  - network
```

### 4.3 Variables

- **`login_user`**, **`login_home`** — Always available; use for user-specific dirs, pipx, venvs, GOPATH.
- **`vmware_env`** — Use in `when:` to vary behaviour (Kali vs Ubuntu, or optional tools like Cursor/n8n).

### 4.4 `become` and `become_user`

- Playbook uses `become: true` by default.
- **`become: false`**: When copying to `{{ login_home }}` as the control-machine user (e.g. `*_Tools.txt`). Also sometimes for pipx (see dploot Ubuntu path).
- **`become_user: "{{ login_user }}"`**: User-space tools (pipx, venv, `~/go`), so config and binaries stay in the target user’s home.

### 4.5 `when` conditions

- **Kali vs Ubuntu**: `when: vmware_env != "ubuntu"` (Kali-only) or `when: vmware_env == "ubuntu"` (Ubuntu-only). Use for different install methods (apt vs pipx vs binary).
- **Desktop / optional**: `when: vmware_env in ["workstation", "laptop"]` or `when: vmware_env == "cursor"` etc.
- **Optional roles**: Extra tools often use `when: vmware_env == "<env>"` so they only run when explicitly requested.

### 4.6 Idempotency

- **apt**: `update_cache: yes`, `cache_valid_time: 3600` when adding packages.
- **pipx**: `state: latest` or `state: present`; pipx is idempotent.
- **get_url**: Use `force: no` to avoid re-download when file exists, or `force: yes` to always refresh.
- **unarchive**: Use `creates: /path/to/file` or `remote_src: yes` as appropriate.
- **git**: `update: yes` for pulls; `depth: 1` for shallow clone.
- **command/shell**: Prefer `args: creates: /path/to/result` where possible.

---

## 5. Installation Method Templates

Use these patterns when adding new tools. Keep task names, tags, and `when` conditions consistent with the rest of the project.

### 5.1 APT (Kali or Ubuntu)

```yaml
- name: <tool> - install <tool> package
  ansible.builtin.apt:
    name: <package>
    state: latest   # or present
    update_cache: yes
    cache_valid_time: 3600
  tags:
    - <tool>
    - <role>
```

If Kali vs Ubuntu differ (e.g. different packages or extra deps), split with `when: vmware_env != "ubuntu"` / `when: vmware_env == "ubuntu"`.

### 5.2 Pipx (user-space, recommended for many Python CLI tools)

```yaml
- name: <tool> - install/upgrade <tool> via pipx
  become: yes
  become_user: "{{ login_user }}"
  community.general.pipx:
    name: <pip-package-name>
    state: latest
  tags:
    - <tool>
    - <role>
```

`pipx ensurepath` is sometimes used elsewhere but often omitted; ensure pipx is installed (Common role).

### 5.3 Git clone + venv + pip (project with requirements.txt)

```yaml
- name: <tool> - clone repository
  ansible.builtin.git:
    repo: https://github.com/org/repo.git
    dest: "{{ login_home }}/<tool>"
    version: main
    update: yes
  become: yes
  become_user: "{{ login_user }}"
  tags: [<tool>, <role>]

- name: <tool> - install Python requirements into virtualenv
  ansible.builtin.pip:
    requirements: "{{ login_home }}/<tool>/requirements.txt"
    virtualenv: "{{ login_home }}/<tool>/venv"
    virtualenv_python: python3
  become: yes
  become_user: "{{ login_user }}"
  tags: [<tool>, <role>]

- name: <tool> - add launcher to /usr/local/bin
  ansible.builtin.copy:
    dest: /usr/local/bin/<tool>
    mode: "0755"
    content: |
      #!/usr/bin/env bash
      source "{{ login_home }}"/<tool>/venv/bin/activate
      exec python "{{ login_home }}"/<tool>/<main_script>.py "$@"
  tags: [<tool>, <role>]
```

See `roles/AD/tasks/SCCMHunter.yml` for a full example with run script and README.

### 5.4 Virtualenv + pip (single package, no repo)

```yaml
- name: <tool> - create project directory
  file:
    path: "{{ login_home }}/<tool>"
    state: directory
    owner: "{{ login_user }}"
    group: "{{ login_user }}"
    mode: "0755"
  tags: [<tool>, <role>]

- name: <tool> - create virtualenv
  command: python3 -m venv "{{ login_home }}"/<tool>/venv
  args:
    creates: "{{ login_home }}/<tool>/venv/bin/activate"
  become: yes
  become_user: "{{ login_user }}"
  tags: [<tool>, <role>]

- name: <tool> - install package in virtualenv
  pip:
    name: <pip-package>
    virtualenv: "{{ login_home }}/<tool>/venv"
    virtualenv_python: python3
    state: latest
  become: yes
  become_user: "{{ login_user }}"
  tags: [<tool>, <role>]

- name: <tool> - symlink CLI into /usr/local/bin
  file:
    src: "{{ login_home }}/<tool>/venv/bin/<binary>"
    dest: /usr/local/bin/<binary>
    state: link
    force: yes
  tags: [<tool>, <role>]
```

See `roles/AD/tasks/Certipy.yml`.

### 5.5 Go install (system-wide binary in /usr/local/bin)

```yaml
- name: <tool> - install via go install
  ansible.builtin.command: >
    go install github.com/org/repo@latest
  args:
    creates: /usr/local/bin/<binary>
  environment:
    GOBIN: /usr/local/bin
    GO111MODULE: "on"
  tags: [<tool>, <role>]
```

See `roles/AD/tasks/ldapx.yml`, `godap.yml`.

### 5.6 Go install (user GOPATH, then copy to /usr/local/bin)

```yaml
- name: <tool> - create GOPATH directory
  ansible.builtin.file:
    path: "{{ login_home }}/go"
    state: directory
    owner: "{{ login_user }}"
    group: "{{ login_user }}"
    mode: "0755"
  tags: [<tool>, <role>]

- name: <tool> - install via go install
  become_user: "{{ login_user }}"
  environment:
    GOPATH: "{{ login_home }}/go"
    PATH: "{{ login_home }}/go/bin:{{ ansible_env.PATH }}"
    TMPDIR: "{{ login_home }}/.cache/go-tmp"
  ansible.builtin.shell: |
    set -euo pipefail
    mkdir -p "$TMPDIR"
    go install github.com/org/repo/cmd/<tool>@latest
  args:
    executable: /bin/bash
    creates: "{{ login_home }}/go/bin/<tool>"
  tags: [<tool>, <role>]

- name: <tool> - copy binary to /usr/local/bin
  become: true
  ansible.builtin.copy:
    src: "{{ login_home }}/go/bin/<tool>"
    dest: /usr/local/bin/<tool>
    owner: root
    group: root
    mode: "0755"
    remote_src: true
  tags: [<tool>, <role>]
```

See `roles/Web/tasks/nuclei.yml`, `subfinder.yml`, `katana.yml`.

### 5.7 Binary from GitHub release (get_url + symlink)

```yaml
- name: <tool> - ensure install directory exists
  file:
    path: /opt/<tool>
    state: directory
    owner: root
    group: root
    mode: "0755"
  tags: [<tool>, <role>]

- name: <tool> - download binary
  get_url:
    url: "https://github.com/org/repo/releases/download/vX.Y.Z/<binary>-linux-amd64"
    dest: "/opt/<tool>/<binary>"
    mode: "0755"
    force: no
  tags: [<tool>, <role>]

- name: <tool> - symlink into /usr/local/bin
  file:
    src: "/opt/<tool>/<binary>"
    dest: "/usr/local/bin/<binary>"
    state: link
    force: yes
  tags: [<tool>, <role>]
```

See `roles/AD/tasks/kerbrute.yml`, `windapsearch.yml`.

### 5.8 Binary from GitHub release (get_url + unarchive)

```yaml
- name: <tool> - download archive
  get_url:
    url: "https://github.com/org/repo/releases/latest/download/<artifact>.zip"
    dest: /tmp/<tool>.zip
  when: vmware_env == "ubuntu"
  tags: [<tool>, <role>]

- name: <tool> - extract and install
  unarchive:
    src: /tmp/<tool>.zip
    dest: /usr/local/bin
    remote_src: yes
  when: vmware_env == "ubuntu"
  tags: [<tool>, <role>]

- name: <tool> - remove installer
  file:
    path: /tmp/<tool>.zip
    state: absent
  when: vmware_env == "ubuntu"
  tags: [<tool>, <role>]
```

Combine with Kali `apt` install when tool is in Kali repos. See `roles/Web/tasks/feroxbuster.yml`.

### 5.9 Third-party APT repo (e.g. Microsoft)

1. Remove old repo/key files (`state: absent`).
2. Add GPG key (e.g. `get_url` → `gpg --dearmor`).
3. `apt_repository` with `signed-by`.
4. `apt` install.

See `roles/Cloud/tasks/azcli.yml`, `roles/Common/tasks/vscode.yml`.

### 5.10 Docker (compose + config)

1. Create `{{ login_home }}/<ToolName>` (or similar).
2. Copy `docker-compose.yml` and config files from `roles/<Role>/files/` (use `template` if needed).
3. Optionally add a README with `docker compose up -d` and URL.

See `roles/AD/tasks/BloodhoundCE.yml` and `roles/AD/files/bloodHoundCE/`.

### 5.11 Installer script (.sh) then symlink

1. `get_url` the installer, mode `0755`.
2. `command: /tmp/installer.sh -q` with `args: creates: /opt/Package/bin/binary`.
3. `file` symlink from `/usr/local/bin/<tool>` to the binary.
4. `file` remove installer.

See `roles/Web/tasks/burp.yml`.

### 5.12 Kali vs Ubuntu split (apt vs pipx or binary)

- One block for Kali: `apt` install, `when: vmware_env != "ubuntu"`.
- Another for Ubuntu: deps (e.g. pipx, build-essential) then pipx or `get_url` + unarchive, `when: vmware_env == "ubuntu"`.

See `roles/Network/tasks/hashcat.yml`, `roles/AD/tasks/dploot.yml`, `roles/Web/tasks/feroxbuster.yml`, `roles/Network/tasks/Enum4linux-ng.yml`.

---

## 6. Adding a New Task — Checklist

1. **Choose the role** (Common, Web, Cloud, AD, Network, OSINT, Extra).
2. **Create `roles/<Role>/tasks/<tool>.yml`** using the closest template from §5. Use kebab-case for the filename.
3. **Tags**: Add both tool tag and role tag to every task.
4. **Task names**: Use `ToolName - <action>`.
5. **Variables**: Use `login_user` / `login_home` for user-specific paths; use `vmware_env` in `when` if behaviour differs by environment.
6. **Idempotency**: Use `creates`, `force`, `update: yes`, etc. as in §4.6.
7. **Import in main.yml**: Add `- name: Run <Tool> setup` and `import_tasks: <tool>.yml` in the right order.
8. **Domain roles only**: If the role has `*_Tools.txt`, add an entry (tool name, usage, description, OPSEC, GitHub). Then ensure `main.yml` copies that file (it usually already does).
9. **Optional tools**: If the tool should run only for specific `vmware_env`, add `when: vmware_env == "..."` (and document in `run.md` if you introduce new `vmware_env` values).
10. **Run**:  
    `sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=workstation login_user=kali login_home=/home/kali" --tags <tool>`  
    to test the new tasks.

---

## 7. File and Path Conventions

| Purpose | Location |
|--------|----------|
| Stockpile (binaries, wordlists, scripts) | `/stockpile/`, `/stockpile/<Tool>/` |
| User-specific tool installs | `{{ login_home }}/<tool>`, `{{ login_home }}/go` |
| System-wide optional installs | `/opt/<tool>` |
| Symlinked binaries | `/usr/local/bin/<binary>` |
| Firefox extensions (Kali) | `/usr/lib/firefox-esr/distribution/extensions/` |
| Firefox extensions (Ubuntu) | `/usr/lib/firefox/distribution/extensions/` |
| User scripts | `{{ login_home }}/scripts/` |
| Config templates | `roles/<Role>/files/` |

---

## 8. Bootstrap (`bootstrap.sh`)

The script:

1. `apt update` and install `git`, `ansible`, `open-vm-tools-desktop`.
2. Mount VMShare at `/share/VMShare`.
3. `cd /share/VMShare/kali-ansible` and run the playbook with `vmware_env=workstation`, `login_user=kali`, `login_home=/home/kali`.

New tasks generally do not change bootstrap; ensure they work with that default environment (and with the `run.md` invocations).

---

## 9. Quick Reference

| Need | Use |
|------|-----|
| Python CLI, available on PyPI | pipx (§5.2) |
| Python project with requirements.txt | Git + venv + pip (§5.3) |
| Go binary, single main | Go install + GOBIN (§5.5) or GOPATH + copy (§5.6) |
| Pre-built binary | get_url ± unarchive (§5.7, §5.8) |
| Kali package | apt (§5.1); add Ubuntu path if different (§5.12) |
| Docker-based service | Copy compose + config (§5.10) |
| Vendor .deb or install script | get_url + apt deb / command (§5.11) |

Use this guide when creating or modifying tasks so they stay consistent with the rest of kali-ansible.
