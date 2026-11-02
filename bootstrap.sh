#!/usr/bin/env bash
# bootstrap.sh — first run on a fresh machine.
#
#   ./bootstrap.sh [extra ansible-playbook args...]
#   e.g. ./bootstrap.sh -e install_ghidra=true
#
# Detects the machine instead of assuming a Kali VMware VM:
#   Ubuntu (VM or laptop)   -> vmware_env=ubuntu
#   Kali in VMware          -> vmware_env=workstation (+ open-vm-tools, VMShare)
#   Kali elsewhere          -> vmware_env=laptop
# login_user/login_home are the user who ran sudo (or the current user).
# Only on a VMware guest is the VMShare mounted and the repo there used;
# everywhere else the playbook runs from the directory this script is in.
set -euo pipefail

if [ "$(id -u)" -eq 0 ] && [ -z "${SUDO_USER:-}" ]; then
  echo "Run this as your normal user (it calls sudo itself), not as root." >&2
  exit 1
fi
LOGIN_USER="${SUDO_USER:-$USER}"
LOGIN_HOME="$(getent passwd "$LOGIN_USER" | cut -d: -f6)"

. /etc/os-release
VIRT="$(systemd-detect-virt 2>/dev/null || true)"

case "$ID" in
  ubuntu) VMWARE_ENV=ubuntu ;;
  kali)   if [ "$VIRT" = vmware ]; then VMWARE_ENV=workstation; else VMWARE_ENV=laptop; fi ;;
  *)      echo "Unsupported distribution: $ID (this playbook targets Kali and Ubuntu)." >&2; exit 1 ;;
esac

# 1. Minimum tools. The apt `ansible` package bundles the collections the
#    playbook needs (ansible.posix, community.general).
sudo apt-get update
sudo apt-get install -y git ansible

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 2. VMware guests only: tools + shared folder, and run the repo from the share.
if [ "$VIRT" = vmware ]; then
  sudo apt-get install -y open-vm-tools-desktop
  sudo mkdir -p /share/VMShare
  if ! mountpoint -q /share/VMShare; then
    sudo /usr/bin/vmhgfs-fuse .host:/VMShare /share/VMShare -o subtype=vmhgfs-fuse,allow_other
  fi
  if [ -f /share/VMShare/kali-ansible/playbook.yml ]; then
    REPO_DIR=/share/VMShare/kali-ansible
  fi
fi

# 3. Run the playbook.
echo "Running playbook from $REPO_DIR: vmware_env=$VMWARE_ENV login_user=$LOGIN_USER login_home=$LOGIN_HOME"
cd "$REPO_DIR"
sudo ansible-playbook -i localhost, -c local playbook.yml \
  -e "vmware_env=$VMWARE_ENV login_user=$LOGIN_USER login_home=$LOGIN_HOME" "$@"
