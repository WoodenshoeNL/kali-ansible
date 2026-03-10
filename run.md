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

Install AI tools only (beads_rust, Claude Code, Codex, Cursor, Antigravity):
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=workstation login_user=kali login_home=/home/kali" --tags AI
```

## Ubuntu

Run for Ansible:
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=ubuntu login_user=michel login_home=/home/michel"
```

## Codex CLI (OpenAI)

Codex CLI is installed on every system by default. No special `vmware_env` needed.

## Optional Extra tools (install_* variables)

These tools run only when explicitly requested. Add the variable to your `-e` flags:

| Tool | Variable | Example |
|------|----------|---------|
| Beads (original) | `install_beads=true` | `-e "install_beads=true"` |
| n8n | `install_n8n=true` | `-e "install_n8n=true"` |
| Mullvad VPN | `install_mullvad=true` | `-e "install_mullvad=true"` |
| Tor Browser | `install_torbrowser=true` | `-e "install_torbrowser=true"` |
| Terraform | `install_terraform=true` | `-e "install_terraform=true"` |

Example (Ubuntu with beads, n8n, and Mullvad):
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=ubuntu login_user=michel login_home=/home/michel install_beads=true install_n8n=true install_mullvad=true"
```

**Tor Browser**: When `install_torbrowser=true`, use `vmware_env=torbrowser` for the official Tor Project repo, or another value for Kali repos.

## Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `vmware_env` | Yes | — | Environment/profile. Affects which optional tools run. |
| `login_user` | Yes | — | Unix user for configs (e.g. `kali`, `michel`). |
| `login_home` | Yes | — | Home directory (e.g. `/home/kali`, `/home/michel`). |
| `install_beads` | No | `false` | Install original beads (Python/Dolt). Default is `beads_rust` only. |
| `install_n8n` | No | `false` | Install n8n workflow automation. |
| `install_mullvad` | No | `false` | Install Mullvad VPN. |
| `install_torbrowser` | No | `false` | Install Tor Browser. |
| `install_terraform` | No | `false` | Install Terraform. |

### vmware_env values (Extra role)

**Always installed**: beads_rust, Claude Code, Codex.

**Cursor and Antigravity**: Installed on all except `esx` (remote Kali).

| Value | Effect |
|-------|--------|
| `esx` | Remote Kali — Cursor and Antigravity **not** installed |
| `ubuntu` | Metasploit installed |

See `roles/Extra/README.md` for full details.

