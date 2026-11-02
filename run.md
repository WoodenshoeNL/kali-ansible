## VMWare Workstation

Go to shared drive:
```
cd /share/VMShare/kali-ansible
```

Run Ansible:
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=workstation login_user=kali login_home=/home/kali"
```

## Remote VM

### From WSL

Go to Ansible dir:
```
cd /mnt/c/VMShare/kali-ansible
```

### Run Ansible

Run Ansible against remote VM:
```
ansible-playbook -i '10.10.10.10,' -u kali --private-key ~/.ssh/key -e 'ansible_python_interpreter=/usr/bin/python3' --become playbook.yml -e "vmware_env=esx login_user=kali login_home=/home/kali"
```


## Laptop

The laptop runs Ubuntu (26.04 LTS), so use the Ubuntu command below with
`vmware_env=ubuntu`; the `vmware_env=laptop` form here is for a Kali laptop.

Clone Repo
```
git clone https://github.com/WoodenshoeNL/kali-ansible.git
```

Run Ansible
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=laptop login_user=kali login_home=/home/kali"
```

## Tags

Install with specific tag:
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=workstation login_user=kali login_home=/home/kali" --tags core
```

Install AI tools only (beads_rust, Claude Code, Codex, Cursor, Antigravity) — AI CLIs are opt-in since they change too much to install by default, so pass the flags:
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=workstation login_user=kali login_home=/home/kali install_claude_code=true install_codex=true install_cursor=true install_antigravity=true" --tags AI
```

## Ubuntu

Run for Ansible (Ubuntu VM or the Ubuntu laptop — same command):
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=ubuntu login_user=michel login_home=/home/michel"
```

The VMware shared folder (`.host:/VMShare` in `/etc/fstab`) is only set up when
the host is actually a VMware guest (Ansible's virtualization facts), and it
carries `nofail`. On a physical machine any VMShare line left in `/etc/fstab`
by an older run is removed. (It used to be written on the laptop too, without
`nofail`, which dropped boot into emergency mode.)

## Ghidra (opt-in)

Ghidra 12.2 + GhidraMCP + triage scripts, only when asked for:
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=ubuntu login_user=michel login_home=/home/michel install_ghidra=true" --tags Ghidra
```
Add `install_ghidra_vms=true` for the KVM/libvirt stack for the Windows lab VM
(bare metal only; adds the user to the `libvirt` and `kvm` groups). Versions and
the Ghidra SHA-256 are in `roles/Ghidra/defaults/main.yml`. Ghidra is in
`~/tools/ghidra` (a symlink to the versioned directory), the MCP bridge in
`~/tools/ghidramcp` (uv-managed Python 3.13 venv). One manual step remains:
enable GhidraMCPPlugin in CodeBrowser -> File -> Configure -> Developer.

## hashcat

hashcat 8.0.0 is installed from the official release into `~/tools/hashcat`
and linked as `/usr/local/bin/hashcat` (pinned with its SHA-256 in
`roles/Network/defaults/main.yml`). The release build is portable, so
`hashcat.potfile`, sessions and the kernel cache live in `~/tools/hashcat`.
Upgrades unpack over that directory and keep the potfile. The distro package
is left installed; `/usr/local/bin` comes first on PATH.

## GitHub downloads

No task calls `api.github.com` (unauthenticated: 60 requests/hour per source
IP, shared by everyone behind the same NAT). Latest releases come from
`releases/latest/download/<asset>` or the `releases/latest` redirect.

## Codex CLI (OpenAI)

Opt-in: pass `install_codex=true`. No special `vmware_env` needed.

## Optional Extra tools (install_* variables)

These tools run only when explicitly requested. Add the variable to your `-e` flags:

| Tool | Variable | Example |
|------|----------|---------|
| Beads (original) | `install_beads_original=true` | `-e "install_beads_original=true"` |
| n8n | `install_n8n=true` | `-e "install_n8n=true"` |
| Mullvad VPN | `install_mullvad=true` | `-e "install_mullvad=true"` |
| Tor Browser | `install_torbrowser=true` | `-e "install_torbrowser=true"` |
| Terraform | `install_terraform=true` | `-e "install_terraform=true"` |
| 1Password | `install_1password=true` | `-e "install_1password=true"` |
| Claude Code | `install_claude_code=true` | `-e "install_claude_code=true"` |
| Codex CLI | `install_codex=true` | `-e "install_codex=true"` |
| Cursor | `install_cursor=true` | `-e "install_cursor=true"` |
| Antigravity | `install_antigravity=true` | `-e "install_antigravity=true"` |

Example (Ubuntu with beads, n8n, and Mullvad):
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=ubuntu login_user=michel login_home=/home/michel install_beads_original=true install_n8n=true install_mullvad=true"
```

**Tor Browser**: `install_torbrowser=true` installs `torbrowser-launcher` from the distro (Kali or Ubuntu universe). `vmware_env=torbrowser` no longer does anything special.

## Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `vmware_env` | Yes | — | Environment/profile. Affects which optional tools run. |
| `login_user` | Yes | — | Unix user for configs (e.g. `kali`, `michel`). |
| `login_home` | Yes | — | Home directory (e.g. `/home/kali`, `/home/michel`). |
| `install_beads_original` | No | `false` | Install original beads (Python/Dolt). Default is `beads_rust` only. |
| `install_n8n` | No | `false` | Install n8n workflow automation. |
| `install_mullvad` | No | `false` | Install Mullvad VPN. |
| `install_torbrowser` | No | `false` | Install Tor Browser. |
| `install_terraform` | No | `false` | Install Terraform. |
| `install_1password` | No | `false` | Install 1Password desktop app. |
| `install_claude_code` | No | `false` | Install Claude Code CLI. Opt-in — AI CLIs change too much for default installs. |
| `install_codex` | No | `false` | Install OpenAI Codex CLI (+ NodeSource Node.js). Opt-in — AI CLIs change too much for default installs. |
| `install_cursor` | No | `false` | Install Cursor editor. Opt-in — AI CLIs change too much for default installs. |
| `install_antigravity` | No | `false` | Install Google Antigravity. Opt-in — AI CLIs change too much for default installs. |
| `install_ghidra` | No | `false` | Ghidra role: Ghidra, GhidraMCP, triage scripts. |
| `install_ghidra_vms` | No | `false` | With `install_ghidra`: KVM/libvirt stack for the Windows lab VM. |

### vmware_env values (Extra role)

**Always installed**: beads_rust.

**AI CLIs (Claude Code, Codex, Cursor, Antigravity)**: opt-in via `install_*` flags since they change too much to install by default. Cursor and Antigravity additionally skip on `esx` (remote Kali) even when opted in.

| Value | Effect |
|-------|--------|
| `esx` | Remote Kali — Cursor and Antigravity **not** installed |
| `ubuntu` | Metasploit installed |

See `roles/Extra/README.md` for full details.

