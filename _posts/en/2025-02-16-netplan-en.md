---
audio: false
generated: false
image: false
lang: en
layout: post
title: Netplan, Systemd, SSH, Conda Cleanup
translated: false
type: post
---

### Table of Contents

1. [Trying Netplan](#trying-netplan)
   - Static IP configuration caused SSH loss
   - Required physical access to revert
   - Modified system's DNS resolver file

2. [Systemd Service](#systemd-service)
   - Configure service for local LLM inference
   - Set up web interface for LLM models
   - Establish rule-based proxy tool service
   - Use systemctl commands for service management

3. [SSH Configuration](#ssh-configuration)
   - Proxy external connections through corkscrew
   - Exclude local network from proxy
   - Manage SSH keys via keychain and agent
   - Specify default private key location

4. [Delete Conda in Linux](#delete-conda-in-linux)
   - Remove entire conda installation directory
   - Delete conda initialization code from bashrc
   - Update PATH environment variable
   - Eliminate conda binaries from system path

## Trying Netplan

I tried the configuration below to assign a static IP address to an Ubuntu machine. I run OpenWebUI and llama.cpp on that server.

```
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.128/32
      gateway4: 192.168.1.1
```

After running `sudo netplan apply`, the machine could no longer be accessed via `ssh lzw@192.168.1.128`.

The keyboard and mouse were used to log in to the machine, remove the files, and revert the settings.

`/etc/resolv.conf` was changed.

---

## Systemd Service

*2025.02.13*

## LLaMA Server Service Configuration

This section explains how to set up a systemd service for running the LLaMA server, which provides local LLM inference capabilities.

```bash
sudo emacs /etc/systemd/system/llama.service
sudo systemctl daemon-reload
sudo systemctl enable llama.service
journalctl -u llama.service
```

```bash
[Unit]
Description=Llama Script

[Service]
ExecStart=/home/lzw/Projects/llama.cpp/build/bin/llama-server -m /home/lzw/Projects/llama.cpp/models/DeepSeek-R1-Distill-Qwen-14B-Q5_K_M.gguf --port 8000  --ctx-size 2048 --batch-size 512 --n-gpu-layers 49 --threads 8 --parallel 1
WorkingDirectory=/home/lzw/Projects/llama.cpp
StandardOutput=append:/home/lzw/llama.log
StandardError=append:/home/lzw/llama.err
Restart=always
User=lzw

[Install]
WantedBy=default.target
```

## Open WebUI Service Configuration

This section explains how to set up a systemd service for running Open WebUI, which provides a web interface for interacting with LLM models.

```bash
[Unit]
Description=Open Web UI Service

[Service]
ExecStart=/home/lzw/.local/bin/open-webui serve
WorkingDirectory=/home/lzw
StandardOutput=append:/home/lzw/open-webui.log
StandardError=append:/home/lzw/open-webui.err
Restart=always
User=lzw

[Install]
WantedBy=default.target
```

```bash
sudo systemctl enable openwebui.service
sudo systemctl daemon-reload
sudo systemctl start  openwebui.service
```

## Clash Service Configuration

This section explains how to set up a systemd service for running Clash, a rule-based proxy tool.

```bash
[Unit]
Description=Clash Service

[Service]
ExecStart=/home/lzw/clash-linux-386-v1.17.0/clash-linux-386
WorkingDirectory=/home/lzw/clash-linux-386-v1.17.0
StandardOutput=append:/home/lzw/clash.log
StandardError=append:/home/lzw/clash.err
Restart=always
User=lzw

[Install]
WantedBy=default.target
```

```bash
# Create the service file
sudo emacs /etc/systemd/system/clash.service

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable clash.service
sudo systemctl start clash.service
sudo systemctl restart clash.service

# Check status
sudo systemctl status clash.service
```

---

## SSH Configuration

*2025.02.09*

This `ssh-config` file configures SSH client behavior. Let's break down each part:

- `Host * !192.*.*.*`: This section applies to all hosts *except* those matching the `192.*.*.*` pattern (typically, local network addresses).
  - `ProxyCommand corkscrew localhost 7890 %h %p`:  This is the key part. It tells SSH to use the `corkscrew` program to connect to the target host.
    - `corkscrew`: A tool that allows you to tunnel SSH connections through HTTP or HTTPS proxies.
    - `localhost 7890`:  Specifies the proxy server's address (`localhost`) and port (`7890`).  This assumes you have a proxy server running on your local machine, listening on port 7890 (e.g., Shadowsocks, a SOCKS proxy, or another tunneling solution).
    - `%h`:  A special SSH variable that expands to the target hostname you're trying to connect to.
    - `%p`:  Another SSH variable that expands to the target port (usually 22 for SSH).
  - In summary, this `Host` block configures SSH to use the `corkscrew` proxy for all connections *except* those to the local network.

- `Host *`: This section applies to *all* hosts.
  - `UseKeychain yes`:  On macOS, this tells SSH to store and retrieve SSH keys from your Keychain, so you don't have to enter your password every time.
  - `AddKeysToAgent yes`:  This automatically adds your SSH keys to the SSH agent, so you don't have to manually add them after each reboot.
  - `IdentityFile ~/.ssh/id_rsa`:  Specifies the path to your private SSH key file.  `~/.ssh/id_rsa` is the default location for the RSA private key.

**In essence, this configuration sets up a proxy for all SSH connections except those on the local network, and it configures key management for convenience.**

```bash
Host 192.168.1.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
Host * !192.*.*.* !47.*.*.*
    ProxyCommand corkscrew localhost 7890 %h %p
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
```

---

## Delete Conda in Linux

*2025.02.07*

```bash
rm -rf ~/anaconda3
```

Delete below code in `.bashrc`:

```bash
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/lzw/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/lzw/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/lzw/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/lzw/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

Update path from:

```bash
export PATH="/usr/local/cuda-12.2/bin:/home/lzw/.local/share/gem/ruby/3.0.0/bin:/home/lzw/anaconda3/bin:/home/lzw/anaconda3/condabin:/home/lzw/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin"
```

To:

```bash
export PATH="/usr/local/cuda-12.2/bin:/home/lzw/.local/share/gem/ruby/3.0.0/bin:/home/lzw/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin"
```
