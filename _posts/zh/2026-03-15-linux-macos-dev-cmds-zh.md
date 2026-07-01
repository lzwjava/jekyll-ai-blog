---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux macOS 开发必备命令
translated: true
type: note
---

以下是 macOS 和 Linux 上开发者常用终端命令的全面参考，按类别组织。

---

## 📁 导航与目录

| Command | Description | Example |
| --- | --- | --- |
| `pwd` | 打印当前工作目录 | `pwd` |
| `ls` | 列出当前目录中的文件 | `ls -la` |
| `cd` | 更改目录 | `cd ~/projects` |
| `mkdir` | 创建新目录 | `mkdir my-app` |
| `rmdir` | 删除空目录 | `rmdir old-folder` |
| `find` | 搜索文件/目录 | `find . -name "*.js"` |

**有用的 `ls` 标志：**

- `ls -l` — 长格式列表，显示权限、大小、日期
- `ls -a` — 显示隐藏文件（点文件）
- `ls -la` — 组合两者

---

## 📄 文件操作

| Command | Description | Example |
| --- | --- | --- |
| `touch` | 创建空文件 | `touch index.js` |
| `cp` | 复制文件或目录 | `cp file.txt backup.txt` |
| `mv` | 移动或重命名文件 | `mv old.js new.js` |
| `rm` | 删除文件 | `rm -rf dist/` |
| `cat` | 打印文件内容 | `cat package.json` |
| `less` | 分页查看文件内容 | `less app.log` |
| `head` | 显示前 N 行 | `head -20 log.txt` |
| `tail` | 显示最后 N 行（适合日志） | `tail -f server.log` |
| `nano` / `vim` | 终端文本编辑器 | `vim config.yaml` |

---

## 🔍 搜索与文本

| Command | Description | Example |
| --- | --- | --- |
| `grep` | 在文件中搜索文本 | `grep -r "TODO" ./src` |
| `sed` | 流编辑器，查找并替换 | `sed 's/foo/bar/g' file.txt` |
| `awk` | 文本处理 / 模式扫描 | `awk '{print $1}' file.txt` |
| `wc` | 统计行数/字数/字符数 | `wc -l file.txt` |
| `sort` | 排序文本行 | `sort names.txt` |
| `uniq` | 删除重复行 | `sort file.txt \| uniq` |

---

## ⚙️ 进程管理

像 `ps`、`kill` 和 `top`/`htop` 这样的命令对于 macOS 和 Linux 上的进程管理至关重要。

| Command | Description | Example |
| --- | --- | --- |
| `ps` | 显示运行进程 | `ps aux` |
| `top` | 实时进程查看器 | `top` |
| `htop` | 增强进程查看器（通过 Homebrew 安装） | `htop` |
| `kill` | 通过 PID 终止进程 | `kill -9 1234` |
| `pkill` | 通过名称终止进程 | `pkill node` |
| `jobs` | 列出 shell 中的后台作业 | `jobs` |
| `bg` / `fg` | 在后台/前台恢复作业 | `fg %1` |
| `&` | 在后台运行命令 | `node server.js &` |
| `lsof` | 列出打开的文件（查找使用端口的进程） | `lsof -i :3000` |

---

## 🌐 网络与 HTTP

`curl` 和 `wget` 对于向服务器传输数据或从服务器获取数据至关重要，特别是用于测试 API。`ssh` 用于安全连接到远程服务器，这是部署工作流程的基础。

| Command | Description | Example |
| --- | --- | --- |
| `curl` | 通过 URL 传输数据 / 测试 API | `curl -I https://example.com` |
| `wget` | 从网络下载文件 | `wget https://example.com/file.zip` |
| `ssh` | 安全 shell 连接远程服务器 | `ssh user@192.168.1.1` |
| `scp` | 安全复制文件到/从远程 | `scp file.txt user@host:/path` |
| `ping` | 测试网络连接 | `ping google.com` |
| `netstat` | 显示网络连接 | `netstat -an` |
| `ifconfig` / `ip` | 显示网络接口信息 | `ifconfig` (macOS) |
| `nslookup` | DNS 查询 | `nslookup google.com` |

---

## 🗜️ 归档与压缩

| Command | Description | Example |
| --- | --- | --- |
| `tar` | 归档文件 | `tar -czvf archive.tar.gz ./dist` |
| `tar` (extract) | 解压归档 | `tar -xzvf archive.tar.gz` |
| `zip` / `unzip` | 压缩和解压文件 | `zip -r out.zip ./folder` |
| `gzip` | 压缩文件 | `gzip file.txt` |

---

## 🔐 权限与所有权

| Command | Description | Example |
| --- | --- | --- |
| `chmod` | 更改文件权限 | `chmod +x script.sh` |
| `chown` | 更改文件所有者 | `chown user:group file.txt` |
| `sudo` | 以超级用户身份运行命令 | `sudo npm install -g yarn` |
| `whoami` | 显示当前用户 | `whoami` |

---

## 💻 系统信息与磁盘

| Command | Description | Example |
| --- | --- | --- |
| `df` | 磁盘可用空间 | `df -h` |
| `du` | 目录磁盘使用量 | `du -sh ./node_modules` |
| `uname` | 系统信息 | `uname -a` |
| `uptime` | 系统运行时间 | `uptime` |
| `env` | 显示环境变量 | `env` |
| `export` | 设置环境变量 | `export NODE_ENV=production` |
| `echo` | 打印文本 / 变量值 | `echo $PATH` |
| `history` | 显示命令历史 | `history` |
| `clear` | 清空终端屏幕 | `clear` |

---

## 🛠️ 开发者专用

`git` 是版本控制的基石——即使您也使用 GUI 工具，命令行熟练度也非常宝贵。

| Command | Description | Example |
| --- | --- | --- |
| `git` | 版本控制 | `git log --oneline --graph --all` |
| `npm` / `yarn` / `pnpm` | Node.js 包管理器 | `npm install` |
| `brew` | Homebrew 包管理器 (macOS) | `brew install htop` |
| `docker` | 容器管理 | `docker ps`, `docker-compose up` |
| `python3` / `node` | 运行脚本 | `python3 app.py` |
| `which` | 查找命令位置 | `which node` |
| `alias` | 创建命令快捷方式 | `alias ll='ls -la'` |
| `xargs` | 从输入构建命令 | `find . -name "*.log" \| xargs rm` |
| `tee` | 读取 stdin 并写入文件 + stdout | `npm test \| tee results.txt` |
| `man` | 显示命令手册 | `man grep` |

---

## 🔗 管道与重定向（基本概念）

| Operator | Description | Example |
| --- | --- | --- |
| `\|` | 将输出管道到另一个命令 | `ps aux \| grep node` |
| `>` | 重定向输出到文件（覆盖） | `echo "hello" > file.txt` |
| `>>` | 追加输出到文件 | `echo "line" >> file.txt` |
| `<` | 使用文件作为输入 | `sort < names.txt` |
| `2>&1` | 将 stderr 重定向到 stdout | `cmd > out.txt 2>&1` |

---

## 💡 提示

- 使用 `Ctrl + C` 取消运行中的命令
- 使用 `Ctrl + Z` 暂停，然后 `bg` 在后台运行
- 使用 `!!` 重复上一个命令
- 使用 `Tab` 进行自动补全
- 使用 `man <command>` 阅读任何命令的完整手册

参考资料：

- [我每天使用的 Mac 终端命令](https://catalins.tech/mac-terminal-commands/)
- [macOS 开发者指南：基本技能](https://rakiabensassi.substack.com/p/macos-for-developers-5-essential)
- [完整的 Mac 终端命令速查表 – GeeksforGeeks](https://www.geeksforgeeks.org/linux-unix/complete-mac-terminal-commands-cheat-sheet/)
- [Linux 和 OS X 用户的终端命令 – TechBeamers](https://techbeamers.com/terminal-commands-linux-mac-osx/)
- [每个用户都应该知道的 20 个 Mac 终端命令 – TechRepublic](https://www.techrepublic.com/article/16-terminal-commands-every-user-should-know/)
