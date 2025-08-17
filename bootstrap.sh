#!/usr/bin/env bash
set -euo pipefail

# 1. Make sure the VM has the minimum tools
sudo apt update
sudo apt install -y git ansible open-vm-tools-desktop

# 2. Mount the shared folder where you like
sudo mkdir -p /share/VMShare
sudo /usr/bin/vmhgfs-fuse .host:/VMShare /share/VMShare -o subtype=vmhgfs-fuse,allow_other


# 3. Run with ansible-playbook
cd /share/VMShare/kali-ansible
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=workstation"
