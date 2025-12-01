


## TMUX


tmux source {{ login_home }}/.tmux.conf

prefix > shift + i





## NXC


```
sudo apt install pipx git
pipx ensurepath
pipx install git+https://github.com/Pennyw0rth/NetExec
```


```
pipx upgrade netexec        # Will update if there is a new version
pipx reinstall netexec      # Force download the latest commits from github
```

Ldap binding issue.
```
pipx runpip netexec install git+https://github.com/fortra/impacket.git@refs/pull/1844/merge
```




## LdapRelayScan

need fix

```
cd /opt
sudo git clone https://github.com/zyn3rgy/LdapRelayScan.git && cd LdapRelayScan
virtualenv env
source env/bin/activate
python3 -m pip install -r requirements_exact.txt
python3 LdapRelayScan.py -h
```




## Extra



https://github.com/prowler-cloud/prowler





https://github.com/dafthack/DomainPasswordSpray

https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors

https://github.com/SnaffCon/Snaffler

