


## TMUX


tmux source {{ login_home }}/.tmux.conf

prefix > shift + i





## NXC (NetExec)

The playbook installs netexec via uv. For manual install or updates:

```bash
# Install uv (if not already installed by playbook)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install netexec from git
uv tool install "netexec @ git+https://github.com/Pennyw0rth/NetExec.git"

# Upgrade
uv tool install --force "netexec @ git+https://github.com/Pennyw0rth/NetExec.git"
```

Ldap binding issue (inject impacket into netexec's environment):
```bash
# NetExec uses uv tool; to add impacket, use uv's --with option or install impacket separately
uv tool install --with "impacket @ git+https://github.com/fortra/impacket.git@refs/pull/1844/merge" "netexec @ git+https://github.com/Pennyw0rth/NetExec.git" --force
```




## LdapRelayScan

need fix

```bash
cd /opt
sudo git clone https://github.com/zyn3rgy/LdapRelayScan.git && cd LdapRelayScan
uv venv .venv
uv pip install --python .venv/bin/python -r requirements_exact.txt
.venv/bin/python LdapRelayScan.py -h
```




## Extra



https://github.com/prowler-cloud/prowler





https://github.com/dafthack/DomainPasswordSpray

https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors

https://github.com/SnaffCon/Snaffler

