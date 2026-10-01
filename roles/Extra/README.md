# Extra Role

Optional tools and environment-specific setups. Most tasks run only when `install_*` or `vmware_env` variables match.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `install_beads_rust` | `true` | Install Beads Rust (br). Default beads implementation. |
| `install_beads_original` | `false` | Install original beads (Python + Dolt + beads-mcp). |
| `install_n8n` | `false` | Install n8n workflow automation. |
| `install_mullvad` | `false` | Install Mullvad VPN. |
| `install_torbrowser` | `false` | Install Tor Browser. |
| `install_terraform` | `false` | Install Terraform. |
| `install_1password` | `false` | Install 1Password desktop app. |
| `install_claude_code` | `false` | Install Claude Code CLI. |
| `install_codex` | `false` | Install OpenAI Codex CLI (+ NodeSource Node.js). |
| `install_cursor` | `false` | Install Cursor editor (not on `esx`). |
| `install_antigravity` | `false` | Install Google Antigravity (not on `esx`). |
| `vmware_env` | — | Environment profile. Metasploit runs only on `ubuntu`. Cursor/Antigravity skip on `esx` even when opted in. Tor Browser path when `install_torbrowser=true`. |

## Task conditions

### install_* variables (opt-in tools)

These run only when explicitly requested:

| Variable | Tasks |
|----------|-------|
| `install_beads_original` | beads (original): Dolt, beads, beads-mcp |
| `install_beads_rust` | beads (rust): beads_rust (br) |
| `install_n8n` | n8n workflow automation |
| `install_mullvad` | Mullvad VPN |
| `install_torbrowser` | Tor Browser |
| `install_terraform` | Terraform |
| `install_1password` | 1Password desktop app |
| `install_claude_code` | Claude Code CLI |
| `install_codex` | Codex CLI (+ Node.js) |
| `install_cursor` | Cursor editor |
| `install_antigravity` | Antigravity |

**beads_rust** (br) is the default beads implementation and runs by default (`install_beads_rust=true`).

**AI CLIs (Claude Code, Codex, Cursor, Antigravity)** are opt-in since they change too much to install by default: pass `install_claude_code=true`, `install_codex=true`, `install_cursor=true`, and/or `install_antigravity=true`. Cursor and Antigravity additionally skip on `vmware_env=esx` (remote Kali).

Example:
```bash
ansible-playbook playbook.yml -e "vmware_env=ubuntu login_user=michel login_home=/home/michel install_beads_original=true install_n8n=true"
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

- **beads_rust** (br) (controlled by `install_beads_rust`)

AI CLIs (Claude Code, Codex, Cursor, Antigravity) no longer run by default — pass their `install_*` flags.

## Tags

Use `--tags` to run specific tools, e.g. `--tags beads_rust`, `--tags beads`, `--tags cursor`, `--tags mullvad`. 

Note: `--tags beads` now targets the **Rust** version (recommended). Use `--tags beads_original` for the Python version.

**`--tags AI`** — Install AI tools: beads_rust plus whichever AI CLIs are opted in via `install_*` flags.
