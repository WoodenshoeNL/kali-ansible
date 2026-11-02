# todo

Checked against the roles on 2026-11-02. Already installed and removed from
this list: AzureHound, Krbrelayx, ROADtools, BloodHound CE + bloodhound-python,
Burp, Coercer, mitm6, Responder, wfuzz, evil-winrm, windapsearch, Certipy,
NetExec (README.md and install.md describe its install).

## To fix

- ADCollector.exe: `Common/tasks/ADCollector.yml` is commented out in
  `stockpile.yml`; it needs `mono-complete`/`mono-xbuild`, and
  `mono-xbuild` is not in kali-rolling.
- BloodHound CE: listed as "to fix" before; check what is wrong with
  `roles/AD/files/bloodHoundCE` on the next run.
- LdapRelayScan: manual steps in install.md, "need fix".

## To check

- certify (the Windows one; Certipy is installed)
- GhidraMCP 1.4 against Ghidra 12.2 (works on 12.1.4; declares 11.3.2)

## Tools to add

- prowler
- adconnectdump
- LaZagne
- MFASweep
- Hoaxshell
- Libesedb
- Ntdsxtract
- PKINITtools
- Pretender
- Nessus
- Aquatone
- ldapdomaindump (a dependency of impacket, not on PATH)
- gobuster
- SSHscan
- testssl.sh
- trufflehog
- whois
- DomainPasswordSpray, Snaffler, BloodHound collectors (stockpile)

## Download to the stockpile

- AADInternals
- adPeas
