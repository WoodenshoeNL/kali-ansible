#!/usr/bin/env python3
"""
Turn *off* every XFCE auto-lock path that Kali 2024/2025 ships.
Run it as the logged-in desktop user once per session (or via Ansible).
"""

import shutil, subprocess, os, sys

def cmd(*args):
    print("→", *args)
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print("   !", e)

def xfconf(channel, prop, value="false"):
    cmd("xfconf-query", "-c", channel, "-p", prop, "-n", "-t", "bool", "-s", value)

def main():
    de = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if "xfce" not in de:
        print("This helper targets XFCE only (detected:", de or "unknown", ")")
        sys.exit(1)

    print("Disabling every known XFCE lock trigger…")

    # 1. Kill the daemon if it is already up (harmless if not)
    if shutil.which("pkill"):
        cmd("pkill", "-f", "xfce4-screensaver")

    # 2. Flip all lock bits in xfce4-screensaver
    xfconf("xfce4-screensaver", "/lock/enabled")
    xfconf("xfce4-screensaver", "/lock/sleep-activation")
    xfconf("xfce4-screensaver", "/saver/idle-activation-enabled")

    # 3. Stop xfce4-screensaver from autostarting next login
    autostart = os.path.expanduser("~/.config/autostart/xfce4-screensaver.desktop")
    os.makedirs(os.path.dirname(autostart), exist_ok=True)
    with open(autostart, "w") as f:
        f.write("[Desktop Entry]\nHidden=true\n")

    # 4. Legacy light-locker (rare on Kali ≥2023 but cheap insurance)
    if os.path.exists("/etc/xdg/autostart/light-locker.desktop"):
        cmd("sudo", "sed", "-i", "s/^Hidden=.*/Hidden=true/", "/etc/xdg/autostart/light-locker.desktop")

    print("Done.  Log out and back in once to make sure the change sticks.")

if __name__ == "__main__":
    main()
