# todo

Checked against the roles on 2026-11-02. Installed since, and removed from
this list: PKINITtools, ldapdomaindump, adconnectdump, libesedb, Pretender,
Hoaxshell, prowler, trufflehog, testssl.sh, gobuster, whois, Nessus
(opt-in: install_nessus=true), and in the stockpile DomainPasswordSpray,
Snaffler, SharpHound, adPEAS, AADInternals, MFASweep, LaZagne.

Decided against:
- Aquatone: archived, last release 2019; GoWitness is installed.
- Ntdsxtract: Python 2 only, last commit 2016; ntdsdotsqlite/secretsdump.
- SSHscan: abandoned 2021; ssh-audit is installed.
- Certify: Certify.exe is already in the stockpile (Ghostpack-CompiledBinaries,
  SharpCollection); GhostPack/Certify publishes no release binaries.

## To fix

- ADCollector.exe: `Common/tasks/ADCollector.yml` is commented out in
  `stockpile.yml`; it needs `mono-complete`/`mono-xbuild`, and
  `mono-xbuild` is not in kali-rolling.
- BloodHound CE: listed as "to fix" before; check what is wrong with
  `roles/AD/files/bloodHoundCE` on the next run.
- LdapRelayScan: manual steps in install.md, "need fix".

## To check

- GhidraMCP 1.4 against Ghidra 12.2 (works on 12.1.4; declares 11.3.2)
- prowler is pinned to Python 3.13 (5.47.0 requires <3.14); drop the pin
  once prowler supports 3.14.

## Download to the stockpile

- adconnectdump's Windows binaries (ADSyncDecrypt, ADSyncQuery,
  ADSyncCertDump; Azure DevOps builds)
