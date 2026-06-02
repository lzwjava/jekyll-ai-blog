---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 实用命令
translated: true
type: post
---

这里有一些我在开发和系统管理中经常使用的有用命令。

## Linux

```bash
cd ~/.ssh/
ls
cat config
mv config config1
git status
gpa
git push --verbose
code .
tmux a
exit
bundle exec jekyll serve
cat README.md
cat ~/.bashrc
./watch-nvidia.sh
ifconfig
chmod +x Outline-Client.AppImage
./Outline-Client.AppImage
sudo apt install fuse
sudo apt update
sudo apt upgrade
journalctl -u NetworkManager --since "10 minutes ago"
systemctl list-unit-files | grep outline
sudo systemctl disable outline_proxy_controller.service
sudo systemctl stop outline_proxy_controller.service
git clone git@github.com:zuoFeng59556/learning-notes.git
javac
sudo apt install openjdk-21-jdk-headless
uname -m
dpkg --print-architecture
sudo tar -xzf OpenJDK22U-jdk_x64_linux_hotspot_22.0.2_9.tar.gz -C /opt/
sudo apt-get install libcups2-dev
sudo apt-get install libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev
make images
make test-tier1
du -sh * | sort -hr
start_proxy
stop_proxy
snap list --outdated
sudo snap refresh --list
nvidia-smi
curl -fsSL https://ollama.com/install.sh | sh
ping weibo.com
curl -I google.com
checkproxy
conda
sudo ufw status verbose
sudo ufw allow 11434
sudo ufw reload
sudo ufw enable
telnet localhost 11434
ollama run deepseek-r1:7b
OLLAMA_HOST=0.0.0.0 ollama run deepseek-r1:7b
ps aux | grep ollama
sudo kill 668318
sudo lsof -i :11434
ollama ps
ollama list
ollama stop
sudo systemctl status ollama.service
sudo systemctl disable ollama.service
tmux list-clients
tmux list-sessions
history > history.txt
```


## macOS

```bash
pip3 install -r requirements.txt --break-system-packages
git status
gpa
history
historypip3 install --upgrade pip --break-system-package
diskutil list
diskutil unmountDisk /dev/disk6
kill 319
diskutil unmountDisk force /dev/disk6
cd ~/Downloads
pwd
ls archlinux-2025.02.01-x86_64.iso
sudo dd if=archlinux-2025.02.01-x86_64.iso of=/dev/rdisk6 bs=1m
cd ~/Downloads
diskutil list
sudo dd if=ubuntu-24.04.1-desktop-amd64.iso of=/dev/rdisk6 bs=1m
cd ~/projects/employment-files
git status
gpa
git push
git add -A
git commit -m "chore: add files"
git config --global --get http.proxy
git config --global --get https.proxy
brew install netcat
cursor ~/.ssh/config
cd ..
git clone git@github.com:huggingface/open-r1.git
cd open-r1
git pull
ssh root@192.168.1.1
cursor .
git pull -v
git pull --verbose
GIT_CURL_VERBOSE=1 git push
GIT_TRACE=1 GIT_CURL_VERBOSE=1 git push
curl -x socks5h://localhost:7891 http://example.com
curl -x socks5h://localhost:7891 google.com
brew install connect-proxy
brew install "connect-proxy"
brew install corkscrew
cursor ~/.ssh/config
GIT_TRACE=1 GIT_CURL_VERBOSE=1 git push -v
ssh root@192.168.1.1 -vvv
cat ~/.ssh/config
git pull
cat ~/.zprofile
gca
pip install alibabacloud_vpc20160428 --break-system-packages
cursor ~/.zprofile
source ~/.zprofile
ifconfig
open .
```
