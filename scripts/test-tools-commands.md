# Tool Verification Commands (Ubuntu)

Run the playbook first:
```bash
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=ubuntu login_user=$(whoami) login_home=$HOME"
```

Ensure `~/.local/bin` and `~/go/bin` are in your PATH:
```bash
export PATH="$HOME/.local/bin:$HOME/go/bin:$PATH"
```

## Quick Test Script

```bash
chmod +x scripts/test-tools-ubuntu.sh
./scripts/test-tools-ubuntu.sh
```

To print all verification commands without running:
```bash
./scripts/test-tools-ubuntu.sh --list-only
```

---

## Manual Command List (by role)

### Common
| Tool | Verification Command |
|------|---------------------|
| uv | `uv --version` |
| cargo/rust | `cargo --version` (source ~/.cargo/env first) |
| pwsh | `pwsh --version` |
| impacket (getTGT.py) | `getTGT.py --help` or `impacket-GetTGT --help` |
| impacket (secretsdump.py) | `secretsdump.py --help` or `impacket-secretsdump --help` |
| zsh | `zsh --version` |
| docker | `docker --version` |
| docker-compose | `docker-compose --version` |
| go | `go version` |
| jq | `jq --version` |
| git | `git --version` |
| vim | `vim --version` |
| xfreerdp | `xfreerdp --version` or `xfreerdp3 --version` (freerdp2-x11 on jammy, freerdp3-x11 on noble+) |
| duckdb | `duckdb --version` |
| SecLists | `test -d /opt/SecLists` |
| stockpile | `test -d /stockpile` |

### Web
| Tool | Verification Command |
|------|---------------------|
| feroxbuster | `feroxbuster --version` |
| gowitness | `gowitness version` |
| nuclei | `nuclei -version` |
| tlsx | `tlsx -version` |
| httpx | `httpx -version` |
| dnsx | `dnsx -version` |
| urlfinder | `urlfinder -version` |
| katana | `katana -version` |
| subfinder | `subfinder -version` |
| ffuf | `ffuf -V` |
| wfuzz | `wfuzz --version` |
| meowEye | `meowEye --help` |
| Burp Suite | `test -f /opt/BurpSuiteCommunity/BurpSuiteCommunity` |

### Cloud
| Tool | Verification Command |
|------|---------------------|
| az | `az --version` |
| roadrecon | `roadrecon --help` |
| roadtx | `roadtx --help` |
| scout | `scout --help` |
| azurehound | `azurehound --help` |
| seamlesspass | `seamlesspass --help` |
| BlackCat | `test -d ~/blackcat` |
| EntraFalcon | `test -d ~/entrafalcon` |

### AD
| Tool | Verification Command |
|------|---------------------|
| certipy-ad | `certipy-ad --help` |
| windapsearch | `windapsearch --help` |
| sccmhunter | `sccmhunter --help` |
| dploot | `dploot --help` |
| donpapi | `donpapi --help` |
| kerbrute | `kerbrute -h` |
| ldapx | `ldapx --version` or `ldapx -v` |
| bloodhound-python | `bloodhound-python -h` |
| bloodhound-ce-python | `bloodhound-ce-python -h` |
| bloodyAD | `bloodyAD --help` |
| ntdsdotsqlite | `ntdsdotsqlite --help` |
| gMSADumper | `gMSADumper --help` |
| godap | `godap -h` |
| rusthound-ce | `rusthound-ce --help` |
| RunasCs (stockpile) | `test -d /stockpile/RunasCs` (Windows tool, in stockpile for transfer) |
| BloodHoundCE | `test -f ~/BloodHoundCE/docker-compose.yml` |

### Network
| Tool | Verification Command |
|------|---------------------|
| enum4linux-ng | `enum4linux-ng -h` |
| ssh-audit | `ssh-audit -h` |
| evil-winrm | `evil-winrm --version` |
| evil-winrm-py | `evil-winrm-py --help` |
| mitm6 | `mitm6 --help` |
| hashcat | `hashcat --version` |
| john | `john 2>&1 | head -1 | grep -q 'John the Ripper'` |
| nmap | `nmap --version` |
| netexec | `netexec --version` |

### OSINT
| Tool | Verification Command |
|------|---------------------|
| sherlock | `sherlock --help` |
| maigret | `maigret --help` |
| sublist3r | `sublist3r -h` |
| theHarvester | `theHarvester -h` |
| amass | `amass -version` |
| holehe | `holehe --help` |
| sn0int | `sn0int --version` |
| changedetection | `changedetection --help` |
| Carbon14 | `test -d ~/Programs/Carbon14` |
| blackbird | `test -d ~/Programs/blackbird` |
| WhatsMyName | `test -d ~/Programs/WhatsMyName-Python` |
| recon-ng | `test -d ~/Programs/recon-ng` |
| spiderfoot | `test -d ~/Programs/spiderfoot` |
| maltego | `maltego -h` or `which maltego` |
| exiftool | `exiftool -ver` |
| ripgrep | `rg --version` |

### Extra (optional - require specific vmware_env)
| Tool | Verification Command |
|------|---------------------|
| beads | `bd --version` |
| antigravity | `antigravity --version` |
| terraform | `terraform version` |
| metasploit | `test -f /opt/metasploit-framework/bin/msfconsole` |
| Tor Browser | `test -d /opt/tor-browser_en` |
| Cursor | `test -f /usr/share/cursor/cursor` |
| VS Code | `test -f /usr/share/code/code` |

---

**Note:** Replace `~` with your actual home path (e.g. `/home/michel`) when running in scripts. The test script uses `LOGIN_HOME` which defaults to `$HOME`.
