#!/usr/bin/env python3
"""
quiet_firefox.py  –  Silences background traffic in Firefox for pentesting.

Writes/overwrites <profile>/user.js with a hardened set of prefs and optionally
cleans up cached telemetry pings. Based on Silent-Firefox project.

Tested on Firefox ESR on Linux (Kali), macOS and Windows.
Supports both traditional and Snap Firefox installations on Linux.
"""

import argparse
import configparser
import json
import os
import shutil
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# ============================================================================
# PREFERENCES - All Firefox Silent Preferences for Pentesting
# ============================================================================
PREFS = {
    # === TELEMETRY & DATA COLLECTION ===
    "datareporting.healthreport.uploadEnabled": False,
    "datareporting.policy.dataSubmissionEnabled": False,
    "datareporting.sessions.current.clean": True,
    "toolkit.telemetry.enabled": False,
    "toolkit.telemetry.unified": False,
    "toolkit.telemetry.archive.enabled": False,
    "toolkit.telemetry.server": "data:,",
    "toolkit.telemetry.server_owner": "",
    "toolkit.telemetry.newProfilePing.enabled": False,
    "toolkit.telemetry.shutdownPingSender.enabled": False,
    "toolkit.telemetry.updatePing.enabled": False,
    "toolkit.telemetry.bhrPing.enabled": False,
    "toolkit.telemetry.firstShutdownPing.enabled": False,
    "toolkit.telemetry.coverage.opt-out": True,
    "toolkit.coverage.opt-out": True,
    "toolkit.coverage.endpoint.base": "",
    "browser.ping-centre.telemetry": False,
    "browser.newtabpage.activity-stream.feeds.telemetry": False,
    "browser.newtabpage.activity-stream.telemetry": False,

    # === EXPERIMENTS & NORMANDY STUDIES ===
    "app.normandy.enabled": False,
    "app.normandy.api_url": "",
    "app.shield.optoutstudies.enabled": False,
    "experiments.enabled": False,
    "experiments.supported": False,
    "experiments.activeExperiment": False,
    "network.allow-experiments": False,

    # === UPDATES (Browser, Extensions, Search, Themes) ===
    "app.update.enabled": False,
    "app.update.auto": False,
    "app.update.service.enabled": False,
    "app.update.staging.enabled": False,
    "app.update.silent": False,
    "extensions.update.enabled": False,
    "extensions.update.autoUpdateDefault": False,
    "browser.search.update": False,
    "lightweightThemes.update.enabled": False,

    # === CAPTIVE PORTAL & CONNECTIVITY CHECKS ===
    "captivedetect.canonicalURL": "",
    "network.captive-portal-service.enabled": False,
    "network.connectivity-service.enabled": False,
    "network.connectivity-check.enabled": False,
    "network.connectivity-check.IPv4.url": "",
    "network.connectivity-check.IPv6.url": "",

    # === SAFE BROWSING (Google/Mozilla Lookups) ===
    "browser.safebrowsing.malware.enabled": False,
    "browser.safebrowsing.phishing.enabled": False,
    "browser.safebrowsing.downloads.enabled": False,
    "browser.safebrowsing.passwords.enabled": False,
    "browser.safebrowsing.downloads.remote.enabled": False,
    "browser.safebrowsing.downloads.remote.url": "",
    "browser.safebrowsing.provider.google.updateURL": "",
    "browser.safebrowsing.provider.google.gethashURL": "",
    "browser.safebrowsing.provider.google4.updateURL": "",
    "browser.safebrowsing.provider.google4.gethashURL": "",
    "browser.safebrowsing.provider.mozilla.updateURL": "",
    "browser.safebrowsing.provider.mozilla.gethashURL": "",

    # === POCKET ===
    "extensions.pocket.enabled": False,
    "extensions.pocket.api": "",
    "extensions.pocket.site": "",

    # === SPONSORED CONTENT & ADS ===
    "browser.newtabpage.activity-stream.showSponsored": False,
    "browser.newtabpage.activity-stream.showSponsoredTopSites": False,
    "browser.newtabpage.activity-stream.feeds.section.topstories": False,
    "browser.newtabpage.activity-stream.feeds.snippets": False,
    "browser.newtabpage.activity-stream.section.highlights.includePocket": False,
    "browser.vpn_promo.enabled": False,
    "browser.promo.focus.enabled": False,

    # === FIREFOX ACCOUNTS & SYNC ===
    "identity.fxaccounts.enabled": False,
    "identity.fxaccounts.toolbar.enabled": False,
    "services.sync.prefs.sync.browser.safebrowsing.downloads.remote.enabled": False,

    # === REMOTE SETTINGS & CONTENT SIGNATURES ===
    # (Stops firefox.settings.services.mozilla.com)
    "services.settings.server": "",
    "services.settings.default_signer": "",
    "security.remote_settings.crlite_filters.enabled": False,
    "security.remote_settings.intermediates.enabled": False,

    # === BLOCKLIST & REMOTE UPDATES ===
    "extensions.blocklist.enabled": False,
    "extensions.blocklist.url": "",
    "services.blocklist.update_enabled": False,
    "services.blocklist.onecrl.collection": "",
    "services.blocklist.addons.collection": "",
    "services.blocklist.plugins.collection": "",
    "services.blocklist.gfx.collection": "",

    # === FIREFOX MONITOR (Stops fxmonitor-breaches) ===
    "extensions.fxmonitor.enabled": False,
    "signon.management.page.breach-alerts.enabled": False,
    "signon.management.page.breachAlertUrl": "",

    # === TOP SITES & TIPPYTOP ICONS ===
    "browser.topsites.contile.enabled": False,
    "browser.topsites.contile.endpoint": "",
    "browser.newtabpage.activity-stream.feeds.topsites": False,
    "browser.newtabpage.activity-stream.default.sites": "",

    # === MESSAGING SYSTEM (What's New, etc.) ===
    "browser.newtabpage.activity-stream.asrouter.providers.whats-new-panel": "",
    "browser.newtabpage.activity-stream.asrouter.providers.cfr": "",
    "browser.newtabpage.activity-stream.asrouter.providers.message-groups": "",
    "browser.newtabpage.activity-stream.asrouter.providers.messaging-experiments": "",
    "messaging-system.rsexperimentloader.enabled": False,

    # === CRASH REPORTS ===
    "browser.tabs.crashReporting.sendReport": False,
    "browser.crashReports.unsubmittedCheck.enabled": False,
    "browser.crashReports.unsubmittedCheck.autoSubmit2": False,

    # === PREFETCH & DNS ===
    "network.predictor.enabled": False,
    "network.dns.disablePrefetch": True,
    "network.prefetch-next": False,
    "network.http.speculative-parallel-limit": 0,
    "browser.urlbar.speculativeConnect.enabled": False,

    # === WEBRTC (Leak Prevention) ===
    "media.peerconnection.ice.default_address_only": True,
    "media.peerconnection.ice.no_host": True,

    # === GEOLOCATION ===
    "geo.enabled": False,
    "geo.provider.network.url": "",
    "browser.region.network.url": "",
    "browser.region.update.enabled": False,

    # === EXTENSION RECOMMENDATIONS ===
    "browser.discovery.enabled": False,
    "extensions.getAddons.showPane": False,
    "extensions.htmlaboutaddons.recommendations.enabled": False,

    # === SEARCH SUGGESTIONS (Stops google.com/complete/search) ===
    "browser.search.suggest.enabled": False,
    "browser.urlbar.suggest.searches": False,
    "browser.urlbar.suggest.engines": False,
    "browser.urlbar.suggest.calculator": False,
    "browser.urlbar.suggest.topsites": False,

    # === PRIVACY PRESERVING ATTRIBUTION (Stops mozgcp.net / OHTTP) ===
    "dom.private-attribution.submission.enabled": False,

    # === GECKO MEDIA PLUGINS (Stops aus5.mozilla.org/update/3/GMP) ===
    "media.gmp-manager.url": "",
    "media.gmp-manager.updateEnabled": False,
    "media.gmp-provider.enabled": False,

    # === WEB PUSH / NOTIFICATIONS ===
    "dom.push.enabled": False,
    "dom.push.connection.enabled": False,
    "dom.push.serverURL": "",

    # === ADDITIONAL NOISE REDUCTION ===
    "extensions.webcompat-reporter.enabled": False,
    "extensions.abuseReport.enabled": False,
    "browser.uitour.enabled": False,
    "browser.startup.homepage_override.mstone": "ignore",
    "startup.homepage_welcome_url": "",
    "startup.homepage_welcome_url.additional": "",
    "startup.homepage_override_url": "",
    "browser.pagethumbnails.capturing_disabled": True,

    # === PERFORMANCE (Keep caching enabled for usability) ===
    "browser.cache.disk.enable": True,
    "browser.cache.memory.enable": True,
}

BANNER = textwrap.dedent("""\
    // ============================================================================
    // Firefox Silent Configuration for Pentesting
    // Generated by quiet_firefox.py – {count} prefs to silence background traffic
    // Generated: {timestamp}
    // ============================================================================
    // Remove any line you don't want enforced.
    // Restart Firefox after changes for them to take effect.
    // ============================================================================
""")

# ============================================================================
# FUNCTIONS
# ============================================================================

def get_linux_firefox_bases() -> list[Path]:
    """
    Return a list of possible Firefox base directories on Linux.
    Handles both traditional and Snap installations.
    """
    bases = []
    home = Path.home()

    # Traditional Firefox location
    traditional = home / ".mozilla" / "firefox"
    if traditional.exists():
        bases.append(traditional)

    # Snap Firefox location (Ubuntu default)
    snap = home / "snap" / "firefox" / "common" / ".mozilla" / "firefox"
    if snap.exists():
        bases.append(snap)

    # Flatpak Firefox location
    flatpak = home / ".var" / "app" / "org.mozilla.firefox" / ".mozilla" / "firefox"
    if flatpak.exists():
        bases.append(flatpak)

    return bases


def parse_profiles_ini(base: Path) -> list[Path]:
    """
    Parse profiles.ini from a Firefox base directory and return profile paths.
    """
    ini = base / "profiles.ini"
    if not ini.exists():
        return []

    cp = configparser.ConfigParser()
    cp.read(ini)
    profs = []

    for section in cp.sections():
        if cp.has_option(section, "Path"):
            path = cp.get(section, "Path")
            # "IsRelative=1" ⇒ path is relative to base
            if cp.getint(section, "IsRelative", fallback=1):
                profs.append(base / path)
            else:
                profs.append(Path(path))

    return profs


def platform_profiles() -> list[Path]:
    """
    Return a list of profile directories discovered via profiles.ini.
    Supports Windows, macOS, and Linux (including Snap/Flatpak).
    """
    if sys.platform.startswith("win"):
        base = Path(os.getenv("APPDATA", "")) / "Mozilla" / "Firefox"
        ini = base / "profiles.ini"
        if not ini.exists():
            print(f"Could not find profiles.ini at {ini} – is Firefox installed?", file=sys.stderr)
            return []
        return parse_profiles_ini(base)

    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support" / "Firefox"
        ini = base / "profiles.ini"
        if not ini.exists():
            print(f"Could not find profiles.ini at {ini} – is Firefox installed?", file=sys.stderr)
            return []
        return parse_profiles_ini(base)

    else:  # Linux, BSD, etc.
        bases = get_linux_firefox_bases()

        if not bases:
            # Check common locations and report which ones were tried
            tried_locations = [
                Path.home() / ".mozilla" / "firefox",
                Path.home() / "snap" / "firefox" / "common" / ".mozilla" / "firefox",
                Path.home() / ".var" / "app" / "org.mozilla.firefox" / ".mozilla" / "firefox",
            ]
            print("Could not find Firefox profiles in any of these locations:", file=sys.stderr)
            for loc in tried_locations:
                print(f"  - {loc}", file=sys.stderr)
            print("\nIs Firefox installed? If using Snap, try running Firefox once first.", file=sys.stderr)
            return []

        # Collect profiles from all found base directories
        all_profiles = []
        for base in bases:
            profiles = parse_profiles_ini(base)
            if profiles:
                print(f"[*] Found Firefox installation: {base}")
                all_profiles.extend(profiles)

        if not all_profiles:
            print("Found Firefox directories but no profiles.ini files:", file=sys.stderr)
            for base in bases:
                print(f"  - {base}", file=sys.stderr)
            print("\nTry running Firefox once to create a profile.", file=sys.stderr)

        return all_profiles


def write_userjs(profile: Path, prefs: dict, dry: bool = False, no_backup: bool = False):
    """
    Write user.js to the given profile directory with all silencing preferences.
    """
    profile.mkdir(parents=True, exist_ok=True)
    userjs = profile / "user.js"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Backup existing user.js if it exists and backup is enabled
    if not no_backup and userjs.exists():
        backup_name = f"user.js.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = profile / backup_name
        if not dry:
            shutil.copy2(userjs, backup_path)
            print(f"  [+] Backed up existing user.js to: {backup_path}")
        else:
            print(f"  [DRY] Would backup {userjs} to {backup_path}")

    # Generate user.js content
    lines = [BANNER.format(count=len(prefs), timestamp=timestamp)]
    for key, value in prefs.items():
        js_val = json.dumps(value)  # renders true/false/"string"/0
        lines.append(f'user_pref("{key}", {js_val});')
    data = "\n".join(lines) + "\n"

    if dry:
        print(f"--- {userjs} ---")
        print(data[:500] + "..." if len(data) > 500 else data)
    else:
        userjs.write_text(data, encoding="utf-8")
        print(f"  [+] Created/updated user.js at: {userjs}")


def clear_telemetry_pings(profile: Path, dry: bool = False):
    """
    Clear cached telemetry pings from the profile directory.
    """
    ping_folders = [
        "saved-telemetry-pings",
        "datareporting/archived",
        "datareporting/active",
    ]

    cleaned = False
    for folder in ping_folders:
        target = profile / folder
        if target.is_dir():
            # Check if there are any files to clean
            files = list(target.rglob("*"))
            if any(f.is_file() for f in files):
                if dry:
                    print(f"  [DRY] Would clean telemetry from: {target}")
                else:
                    for f in files:
                        if f.is_file():
                            f.unlink()
                cleaned = True

    if cleaned and not dry:
        print(f"  [+] Cleared cached telemetry pings")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Silence Firefox background traffic for pentesting with Burp Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s                     # Configure all Firefox profiles
              %(prog)s --profile /path/to/profile
              %(prog)s --no-backup --skip-cleanup
              %(prog)s --dry-run           # Preview changes without writing

            Supported Firefox installations:
              - Traditional: ~/.mozilla/firefox/
              - Snap (Ubuntu): ~/snap/firefox/common/.mozilla/firefox/
              - Flatpak: ~/.var/app/org.mozilla.firefox/.mozilla/firefox/
              - Windows: %%APPDATA%%/Mozilla/Firefox/
              - macOS: ~/Library/Application Support/Firefox/
        """)
    )
    parser.add_argument(
        "--profile", "-p",
        metavar="DIR",
        help="Path to a single Firefox profile to modify"
    )
    parser.add_argument(
        "--no-backup", "-n",
        action="store_true",
        help="Skip creating backups of existing user.js files"
    )
    parser.add_argument(
        "--skip-cleanup", "-c",
        action="store_true",
        help="Skip deleting cached telemetry pings"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be written, do not touch the disk"
    )
    args = parser.parse_args()

    # Determine target profiles
    if args.profile:
        targets = [Path(args.profile)]
        if not targets[0].is_dir():
            parser.error(f"Specified profile path does not exist: {args.profile}")
    else:
        targets = platform_profiles()

    if not targets:
        parser.error("No Firefox profiles found. Use --profile to specify one manually.")

    print(f"\n[*] Found {len(targets)} Firefox profile(s)\n")

    for prof in targets:
        profile_name = prof.name
        print(f"[*] Configuring: {profile_name}")

        write_userjs(prof, PREFS, dry=args.dry_run, no_backup=args.no_backup)

        if not args.skip_cleanup:
            clear_telemetry_pings(prof, dry=args.dry_run)

        print()

    print("=" * 60)
    print("Firefox has been silenced!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Close Firefox completely")
    print("  2. Restart Firefox")
    print("  3. Configure Firefox to use Burp Suite proxy (127.0.0.1:8080)")
    print("  4. Verify in Burp Suite that background noise is gone")
    print()