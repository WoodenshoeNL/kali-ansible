# Fixing apt update warnings

If you see warnings when running `sudo apt update`, use these one-off fixes on the target machine. The Ansible roles have also been updated to prevent these issues on future runs.

## 4. VS Code (duplicate vscode.list and vscode.sources) – “Target … is configured multiple times” (vscode.list and vscode.sources)

Both `vscode.list` and `vscode.sources` exist, causing duplicate configuration. Remove the extra file and keep only one:

```bash
# Keep the .list format, remove .sources
sudo rm -f /etc/apt/sources.list.d/vscode.sources
```

Or if you prefer DEB822 format, remove the .list instead:

```bash
sudo rm -f /etc/apt/sources.list.d/vscode.list
```

Then run `sudo apt update`.


## 1. Azure CLI – missing GPG key (NO_PUBKEY EB3E94ADBE1229CF)

Install Microsoft’s key into the keyring and ensure the repo uses it:

```bash
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /usr/share/keyrings/microsoft.gpg > /dev/null
```

Ensure the Azure CLI repo file uses this key. Edit (or create) `/etc/apt/sources.list.d/azure-cli.list` so it has a single line like:

```
deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ noble main
```

(Use your release codename instead of `noble` if different, e.g. `jammy` for 22.04.)

Then run:

```bash
sudo apt update
```

## 2. Google Chrome – “Target … is configured multiple times”

Duplicate lines in `/etc/apt/sources.list.d/google-chrome.list` cause this. Keep a single repo line:

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] https://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
```

If the keyring is missing:

```bash
curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor | sudo tee /usr/share/keyrings/google-linux-signing-keyring.gpg > /dev/null
```

Then:

```bash
sudo apt update
```

## 3. Tor Project – duplicate lines or key in legacy trusted.gpg

**Duplicate lines in tor.list:** If you see "Target … is configured multiple times" for tor.list, keep a single repo line:

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/torproject.gpg] https://deb.torproject.org/torproject.org $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/tor.list
```

**Legacy key:** If the message means the Tor key is still in the old `apt-key` keyring, remove it and use the keyring-based repo instead.

Remove the legacy key:

```bash
sudo apt-key del A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89
```

Ensure the Tor repo uses the keyring (e.g. in `/etc/apt/sources.list.d/tor.list`):

```
deb [arch=amd64 signed-by=/usr/share/keyrings/torproject.gpg] https://deb.torproject.org/torproject.org noble main
```

If the keyring is missing:

```bash
curl -sSL https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | sudo tee /usr/share/keyrings/torproject.gpg > /dev/null
```

Then:

```bash
sudo apt update
```

---

After applying these, run `sudo apt update` again; the warnings should be gone. Re-running the playbook will keep things consistent for future runs.
