#!/bin/bash
# test-tools-ubuntu.sh - Verify all tools installed by kali-ansible playbook on Ubuntu
# Run after: sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=ubuntu login_user=$(whoami) login_home=$HOME"
#
# Usage: ./test-tools-ubuntu.sh [--list-only]
#   --list-only  Print commands only, do not run tests

set -e
LOGIN_HOME="${LOGIN_HOME:-$HOME}"
export PATH="$LOGIN_HOME/.local/bin:$LOGIN_HOME/go/bin:$PATH"

LIST_ONLY=false
[[ "${1:-}" == "--list-only" ]] && LIST_ONLY=true

PASS=0
FAIL=0

test_cmd() {
  local name="$1"
  local cmd="$2"
  if $LIST_ONLY; then
    echo "# $name"
    echo "$cmd"
    echo ""
    return
  fi
  if eval "$cmd" >/dev/null 2>&1; then
    echo "  OK   $name"
    ((PASS++)) || true
    return 0
  else
    echo "  FAIL $name"
    ((FAIL++)) || true
    return 1
  fi
}

test_path() {
  local name="$1"
  local path="$2"
  if $LIST_ONLY; then
    echo "# $name"
    echo "test -f \"$path\" || test -d \"$path\""
    echo ""
    return
  fi
  if [[ -f "$path" || -d "$path" ]]; then
    echo "  OK   $name"
    ((PASS++)) || true
    return 0
  else
    echo "  FAIL $name"
    ((FAIL++)) || true
    return 1
  fi
}

echo "=== kali-ansible tool verification (Ubuntu) ==="
echo ""

# --- Common ---
echo "--- Common ---"
test_cmd "uv" "uv --version"
test_cmd "cargo (rust)" "source $LOGIN_HOME/.cargo/env 2>/dev/null; cargo --version"
test_cmd "pwsh (PowerShell)" "pwsh --version"
test_cmd "getTGT.py (impacket)" "getTGT.py --help 2>/dev/null || impacket-GetTGT --help 2>/dev/null || impacket-getTGT --help"
test_cmd "secretsdump.py (impacket)" "secretsdump.py --help 2>/dev/null || impacket-secretsdump --help"
test_cmd "zsh" "zsh --version"
test_cmd "docker" "docker --version"
test_cmd "docker-compose" "docker-compose --version"
test_cmd "go" "go version"
test_cmd "jq" "jq --version"
test_cmd "git" "git --version"
test_cmd "vim" "vim --version"
test_cmd "xfreerdp/xfreerdp3" "xfreerdp --version 2>/dev/null || xfreerdp3 --version 2>/dev/null"
test_cmd "duckdb" "duckdb --version 2>/dev/null || (echo '.tables' | duckdb 2>/dev/null) || which duckdb"
test_path "SecLists" "/opt/SecLists"
test_path "stockpile" "/stockpile"
test_path "stockpile/Rubeus" "/stockpile/Rubeus/Rubeus.exe"
test_path "stockpile/mimikatz" "/stockpile/mimikatz"
test_path "stockpile/LinPEAS" "/stockpile/LinPEAS/linpeas.sh"
echo ""

# --- Web ---
echo "--- Web ---"
test_cmd "feroxbuster" "feroxbuster --version"
test_cmd "gowitness" "gowitness version"
test_cmd "nuclei" "nuclei -version"
test_cmd "tlsx" "tlsx -version"
test_cmd "httpx" "httpx -version"
test_cmd "dnsx" "dnsx -version"
test_cmd "urlfinder" "urlfinder -version"
test_cmd "katana" "katana -version"
test_cmd "subfinder" "subfinder -version"
test_cmd "ffuf" "ffuf -V"
test_cmd "wfuzz" "wfuzz --version 2>/dev/null || wfuzz -h"
test_cmd "meowEye" "meowEye --help 2>/dev/null || meowEye -h"
test_path "Burp Suite" "/opt/BurpSuiteCommunity/BurpSuiteCommunity"
echo ""

# --- Cloud ---
echo "--- Cloud ---"
test_cmd "az (Azure CLI)" "az --version"
test_cmd "roadrecon" "roadrecon --help"
test_cmd "roadtx" "roadtx --help"
test_cmd "scout" "scout --help"
test_cmd "azurehound" "azurehound --help"
test_cmd "seamlesspass" "seamlesspass --help"
test_path "BlackCat" "$LOGIN_HOME/blackcat"
test_path "EntraFalcon" "$LOGIN_HOME/entrafalcon"
echo ""

# --- AD ---
echo "--- AD ---"
test_cmd "certipy-ad" "certipy-ad --help"
test_cmd "windapsearch" "windapsearch --help"
test_cmd "sccmhunter" "sccmhunter --help"
test_cmd "dploot" "dploot --help"
test_cmd "donpapi" "donpapi --help"
test_cmd "kerbrute" "kerbrute -h"
test_cmd "ldapx" "ldapx -h"
test_cmd "bloodhound" "bloodhound --help"
test_cmd "bloodhound-ce" "bloodhound-ce --help"
test_cmd "bloodyAD" "bloodyAD --help"
test_cmd "ntdsdotsqlite" "ntdsdotsqlite --help"
test_cmd "gMSADumper" "gMSADumper --help"
test_cmd "godap" "godap -h"
test_cmd "rusthound-ce" "rusthound-ce --help"
test_cmd "runascs" "runascs --help"
test_path "BloodHoundCE" "$LOGIN_HOME/BloodHoundCE/docker-compose.yml"
echo ""

# --- Network ---
echo "--- Network ---"
test_cmd "enum4linux-ng" "enum4linux-ng -h"
test_cmd "ssh-audit" "ssh-audit -h"
test_cmd "evil-winrm" "evil-winrm --version"
test_cmd "evil-winrm-py" "evil-winrm-py --help"
test_cmd "mitm6" "mitm6 --help"
test_cmd "hashcat" "hashcat --version"
test_cmd "john" "john --version"
test_cmd "nmap" "nmap --version"
test_cmd "netexec" "netexec --version"
echo ""

# --- OSINT ---
echo "--- OSINT ---"
test_cmd "sherlock" "sherlock --help"
test_cmd "maigret" "maigret --help"
test_cmd "sublist3r" "sublist3r -h"
test_cmd "theHarvester" "theHarvester -h"
test_cmd "amass" "amass -version"
test_cmd "holehe" "holehe --help"
test_cmd "sn0int" "sn0int --version"
test_cmd "changedetection" "changedetection --help 2>/dev/null || which changedetection 2>/dev/null"
test_path "Carbon14" "$LOGIN_HOME/Programs/Carbon14"
test_path "blackbird" "$LOGIN_HOME/Programs/blackbird"
test_path "whatsmyname" "$LOGIN_HOME/Programs/WhatsMyName-Python"
test_path "recon-ng" "$LOGIN_HOME/Programs/recon-ng"
test_path "spiderfoot" "$LOGIN_HOME/Programs/spiderfoot"
test_cmd "maltego" "maltego -h 2>/dev/null || which maltego"
test_cmd "exiftool" "exiftool -ver"
test_cmd "rg (ripgrep)" "rg --version"
echo ""

# --- Extra (optional, may not be installed) ---
echo "--- Extra (optional) ---"
test_cmd "bd (beads)" "bd --version 2>/dev/null || which bd"
test_cmd "antigravity" "antigravity --version 2>/dev/null || which antigravity"
test_cmd "terraform" "terraform version"
test_cmd "msfconsole" "test -f /opt/metasploit-framework/bin/msfconsole"
test_path "Tor Browser" "/opt/tor-browser_en/Browser/start-tor-browser"
test_path "Cursor" "/usr/share/cursor/cursor"
test_path "VS Code" "/usr/share/code/code"
echo ""

if ! $LIST_ONLY; then
  echo "=== Summary ==="
  echo "  Passed: $PASS"
  echo "  Failed: $FAIL"
  echo ""
  if [[ $FAIL -gt 0 ]]; then
    echo "Some tools failed. Check that:"
    echo "  1. Playbook was run with: vmware_env=ubuntu login_user=\$(whoami) login_home=\$HOME"
    echo "  2. PATH includes ~/.local/bin and ~/go/bin"
    echo "  3. Optional Extra tools (Cursor, n8n, terraform, etc.) require specific vmware_env values"
    exit 1
  fi
  echo "All tested tools are installed correctly."
fi
