## VMWare Workstation

Go to shared drive:
```
cd /share/VMShare/kali-ansible
```

Run Ansible:
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=workstation login_user=kali login_home=/home/kali"
```

## Remote VM

### From WSL

Go to Ansible dir:
```
cd /mnt/c/VMShare/kali-ansible
```

### Run Ansible

Run Ansible against remote VM:
```
ansible-playbook -i '10.10.10.10,' -u kali --private-key ~/.ssh/key -e 'ansible_python_interpreter=/usr/bin/python3' --become playbook.yml -e "vmware_env=esx login_user=kali login_home=/home/kali"
```


## Laptop

Clone Repo
```
git clone https://github.com/WoodenshoeNL/kali-ansible.git
```

Run Ansible
```
sudo ansible-playbook -i localhost, -c local playbook.yml -e "vmware_env=laptop login_user=kali login_home=/home/kali"
```