



## Windapsearch

https://github.com/ropnop/go-windapsearch/releases

sudo mkdir windapsearch

/opt/windapsearch/

wget https://github.com/ropnop/go-windapsearch/releases/download/v0.3.0/windapsearch-linux-amd64

cp windapsearch-linux-amd64 windapsearch

chmod +x windapsearch

vim .profile
```
export PATH=$PATH:/opt/windapsearch/
```


## SCCMHunter

```
cd ~
git clone https://github.com/garrettfoster13/sccmhunter.git
cd sccmhunter
virtualenv --python=python3 .
source bin/activate
pip3 install -r requirements.txt
python3 sccmhunter.py -h
```

## TMUX


vim .tmux.conf
```
C:\VMKali\tmux.conf
```


### TMUX Plugins
https://github.com/tmux-plugins/tpm

tmux new -s attack

tmux source ~/.tmux.conf

prefix > shift + i

### TMUX-yank prereq
https://github.com/tmux-plugins/tmux-yank

```
sudo apt-get install xsel
```


## Enum4linux-ng

```
sudo apt install enum4linux-ng
```



## Upgrade Kali

```
sudo apt update
sudo apt full-upgrade -y
```


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

## SSH-Audit

```
git clone https://github.com/jtesta/ssh-audit
```



## impacket

https://github.com/fortra/impacket
```
python3 -m pipx install impacket
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


## mitm6

```
https://github.com/dirkjanm/mitm6
```


## GoWitness

https://github.com/sensepost/gowitness
```
go install github.com/sensepost/gowitness@latest
```

```
sudo apt install gowitness
```



## Feroxbuster

```
sudo apt install feroxbuster
```


## Todo


- xxx
- Feroxbuster


chrome


Azure CLI

```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```



Road recon


```
sudo apt install python3-virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install roadrecon
```


scoute suite


```
sudo apt install python3-virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install scoutsuite
scout --help
```



blackcat



Azure hound
```
sudo apt install azurehound
```


Install Roadtx
```
# Debian/Ubuntu/Kali example
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
python3 -m venv ~/venv
source ~/venv/bin/activate

# stable PyPI build
pip install --upgrade pip
pip install roadtx            # drops a `roadtx` entry-point on your PATH

```
