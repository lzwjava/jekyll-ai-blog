---
audio: false
generated: false
image: false
lang: zh
layout: post
title: Netplan、Systemd、SSH、Conda清理
translated: true
type: post
---

### 目录

1. [尝试Netplan](#trying-netplan)
   - 静态IP配置导致SSH连接丢失
   - 需要物理访问才能恢复
   - 修改了系统的DNS解析器文件

2. [Systemd服务](#systemd-service)
   - 配置本地LLM推理服务
   - 为LLM模型设置Web界面
   - 建立基于规则的代理工具服务
   - 使用systemctl命令进行服务管理

3. [SSH配置](#ssh-configuration)
   - 通过corkscrew代理外部连接
   - 从代理中排除本地网络
   - 通过keychain和agent管理SSH密钥
   - 指定默认私钥位置

4. [在Linux中删除Conda](#delete-conda-in-linux)
   - 删除整个conda安装目录
   - 从bashrc中删除conda初始化代码
   - 更新PATH环境变量
   - 从系统路径中删除conda二进制文件

## 尝试Netplan

我尝试了以下配置来为一台Ubuntu机器分配静态IP地址。我在那台服务器上运行OpenWebUI和llama.cpp。

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

运行 `sudo netplan apply` 后，无法通过 `ssh lzw@192.168.1.128` 访问该机器。

我使用键盘和鼠标登录到机器，删除了文件并恢复了设置。

`/etc/resolv.conf` 已更改。

---

## Systemd服务

*2025.02.13*

## LLaMA服务器服务配置

本节解释如何设置systemd服务来运行LLaMA服务器，该服务器提供本地LLM推理功能。

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

## Open WebUI服务配置

本节解释如何设置systemd服务来运行Open WebUI，它提供了一个用于与LLM模型交互的Web界面。

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

## Clash服务配置

本节解释如何设置systemd服务来运行Clash，一个基于规则的代理工具。

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

## SSH配置

*2025.02.09*

此 `ssh-config` 文件配置SSH客户端行为。让我们分解每个部分：

- `Host * !192.*.*.*`: 此部分适用于所有主机，*除了*匹配 `192.*.*.*` 模式（通常是本地网络地址）的主机。
  - `ProxyCommand corkscrew localhost 7890 %h %p`: 这是关键部分。它告诉SSH使用 `corkscrew` 程序连接到目标主机。
    - `corkscrew`: 一个工具，允许您通过HTTP或HTTPS代理隧道SSH连接。
    - `localhost 7890`: 指定代理服务器的地址 (`localhost`) 和端口 (`7890`)。这假定您的本地机器上运行着一个代理服务器，并监听端口7890（例如，Shadowsocks、SOCKS代理或其他隧道解决方案）。
    - `%h`: 一个特殊的SSH变量，扩展为要连接的目标主机名。
    - `%p`: 另一个SSH变量，扩展为目标端口（SSH通常为22）。
  - 简而言之，此 `Host` 块将SSH配置为对所有连接（*除了*本地网络连接）使用 `corkscrew` 代理。

- `Host *`: 此部分适用于*所有*主机。
  - `UseKeychain yes`: 在macOS上，这告诉SSH从您的Keychain存储和检索SSH密钥，这样您就不必每次都输入密码。
  - `AddKeysToAgent yes`: 这会自动将您的SSH密钥添加到SSH agent中，这样您就不必在每次重新启动后手动添加它们。
  - `IdentityFile ~/.ssh/id_rsa`: 指定您的私有SSH密钥文件的路径。`~/.ssh/id_rsa` 是RSA私钥的默认位置。

**实质上，此配置为所有SSH连接（本地网络上的连接除外）设置了代理，并为方便起见配置了密钥管理。**

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

## 在Linux中删除Conda

*2025.02.07*

```bash
rm -rf ~/anaconda3
```

删除 `.bashrc` 中的以下代码：

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

将路径从：

```bash
export PATH="/usr/local/cuda-12.2/bin:/home/lzw/.local/share/gem/ruby/3.0.0/bin:/home/lzw/anaconda3/bin:/home/lzw/anaconda3/condabin:/home/lzw/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin"
```

更改为：

```bash
export PATH="/usr/local/cuda-12.2/bin:/home/lzw/.local/share/gem/ruby/3.0.0/bin:/home/lzw/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin"
```
