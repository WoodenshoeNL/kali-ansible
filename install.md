


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


## mitm6

```
https://github.com/dirkjanm/mitm6
```


## Extra


install evil-winrm-py
```
pipx install evil-winrm-py
```


https://github.com/prowler-cloud/prowler


https://github.com/eslam3kl/meowEye

https://github.com/projectdiscovery/nuclei


https://github.com/dafthack/DomainPasswordSpray

https://github.com/ropnop/windapsearch

https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors

https://github.com/SnaffCon/Snaffler

 
## OSINT


SocialScan
```
pipx install socialscan
```
github.com/iojw/socialscan


Blackbird
```
cd ~/Downloads/Programs
git clone https://github.com/p1ngul1n0/blackbird
cd blackbird
python3 -m venv blackbirdEnvironment
source blackbirdEnvironment/bin/activate
sudo pip install -r requirements.txt
deactivate
```
github.com/p1ngul1n0/blackbird




WhatsMyName-Python
```
cd ~/Downloads/Programs
git clone https://github.com/C3n7ral051nt4g3ncy/WhatsMyName-
Python.git
cd WhatsMyName-Python
python3 -m venv wmnpythonEnvironment
source wmnpythonEnvironment/bin/activate
sudo pip3 install -r requirements.txt
deactivate
```
github.com/C3n7ral051nt4g3ncy


Holehe
```
pipx install holehe
```
github.com/megadose/holehe


Eyes
```
mkdir ~/Downloads/Programs/eyes
cd ~/Downloads/Programs/eyes
git clone https://github.com/N0rz3/Eyes.git
cd Eyes
python3 -m venv eyesEnvironment
source eyesEnvironment/bin/activate
sudo pip install -r requirements.txt
deactivate
```
https://github.com/N0rz3/Eyes



GHunt
```
pipx install ghunt
```
github.com/mxrch/Ghunt


H8Mail
```
pipx install h8mail
```
https://github.com/khast3x/h8mail


Hash Tools
```
pipx install search-that-hash
pipx install name-that-hash
```
github.com/HashPals/


Amass
```
cd ~/Downloads
ver=$(dpkg --print-architecture)
wget https://github.com/owasp-
amass/amass/releases/latest/download/amass_Linux_"$ver".zip
mkdir ~/Downloads/Programs/Amass
unzip amass_Linux_"$ver".zip -d ~/Downloads/Programs/Amass/
cd Programs/Amass/amass_Linux_"$ver"/
mv * ~/Downloads/Programs/Amass
rm -r ~/Downloads/Programs/Amass/amass_Linux_"$ver"/
rm '/home/osint/Downloads/amass_Linux_arm64.zip'
```
https://github.com/owasp-amass/amass



Photon
```
cd ~/Downloads/Programs
git clone https://github.com/s0md3v/Photon.git
cd Photon
python3 -m venv PhotonEnvironment
source PhotonEnvironment/bin/activate
sudo pip install -r requirements.txt
deactivate
```
https://github.com/s0md3v/Photon






Change Detection
```
pipx install changedetection.io
```
github.com/dgtlmoon/changedetection.io



MediaInfo
```
sudo apt update && sudo apt install mediainfo-gui -y
```
https://mediaarea.net/en/MediaInfo




Mr. Holmes
```
cd ~/Downloads/Programs
git clone https://github.com/Lucksi/Mr.Holmes
cd Mr.Holmes
sudo apt update
sudo chmod +x install.sh
sudo bash install.sh
```
https://github.com/Lucksi/Mr.Holmes


sn0int
```
cd ~/Downloads/Programs
sudo apt install curl sq
curl -sSf https://apt.vulns.sexy/kpcyrd.pgp | sq dearmor |
sudo tee /etc/apt/trusted.gpg.d/apt-vulns-sexy.gpg
echo deb http://apt.vulns.sexy stable main | sudo tee
/etc/apt/sources.list.d/apt-vulns-sexy.list
sudo apt update && sudo apt install sn0int
```
https://github.com/kpcyrd/sn0int


