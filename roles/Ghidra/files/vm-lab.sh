#!/bin/bash
# vm-lab.sh — helper for the win11-lab bughunting VM
# usage: vm-lab.sh start|stop|snap <name>|revert <name>|snaps|console
set -e
CMD=${1:-help}
V=win11-lab
case "$CMD" in
  start)   sudo virsh start $V && echo "started — open with: virt-viewer $V (or virt-manager)" ;;
  stop)    sudo virsh shutdown $V ;;
  forceoff) sudo virsh destroy $V ;;
  snap)    [ -z "$2" ] && { echo "usage: vm-lab.sh snap <name>"; exit 1; }
           sudo virsh snapshot-create-as $V "$2" && echo "snapshot '$2' created" ;;
  revert)  [ -z "$2" ] && { echo "usage: vm-lab.sh revert <name>"; exit 1; }
           sudo virsh snapshot-revert $V "$2" && echo "reverted to '$2'" ;;
  snaps)   sudo virsh snapshot-list $V ;;
  console) sudo virt-viewer --wait $V >/dev/null 2>&1 & echo "viewer launched" ;;
  *) echo "usage: vm-lab.sh start|stop|forceoff|snap <name>|revert <name>|snaps|console" ;;
esac
