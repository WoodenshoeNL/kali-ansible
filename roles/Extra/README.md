# Extra Role

Optional tools and environment-specific setups. Most tasks run only when `install_*` or `vmware_env` variables match.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `install_beads` | `false` | Install original beads (Python + Dolt + beads-mcp). When `false`, only **beads_rust** (br) is installed. |
| `install_n8n` | `false` | Install n8n workflow automation. |
| `install_mullvad` | `false` | Install Mullvad VPN. |
| `install_torbrowser` | `false` | Install Tor Browser. |
| `install_terraform` | `false` | Install Terraform. |
| `vmware_env` | — | Environment profile. Claude Code and Codex install on every system. Cursor and Antigravity install on all except `esx` (remote Kali). Metasploit runs only on `ubuntu`. Tor Browser path when `install_torbrowser=true`. |

## Task conditions

### install_* variables (opt-in tools)

These run only when explicitly requested:

| Variable | Tasks |
|----------|-------|
| `install_beads` | beads (original): Dolt, beads, beads-mcp |
| `install_n8n` | n8n workflow automation |
| `install_mullvad` | Mullvad VPN |
| `install_torbrowser` | Tor Browser |
| `install_terraform` | Terraform |

**beads_rust** (br) is the default beads implementation and always runs.

**Claude Code** and **Codex** install on every system by default.

**Cursor** and **Antigravity** install on all systems except remote Kali (`vmware_env=esx`).

Example:
```bash
ansible-playbook playbook.yml -e "vmware_env=ubuntu login_user=michel login_home=/home/michel install_beads=true install_n8n=true install_mullvad=true"
```

### vmware_env (still used for)

| vmware_env | Effect |
|------------|-------|
| `esx` | Remote Kali — Cursor and Antigravity are **not** installed |
| `ubuntu` | Metasploit is installed |
| `torbrowser` (with `install_torbrowser=true`) | Tor Browser uses official Tor Project repo |

**Tor Browser**: When `install_torbrowser=true`, use `vmware_env=torbrowser` for the official Tor Project repo, or another value for Kali repos.

## Always-run tasks

These run on every system (unless skipped via `--tags`):

- **beads_rust** (br)
- **Claude Code**
- **Codex**

**Cursor** and **Antigravity** run on all except `vmware_env=esx` (remote Kali).

## Tags

Use `--tags` to run specific tools, e.g. `--tags beads_rust`, `--tags beads`, `--tags cursor`, `--tags mullvad`.
