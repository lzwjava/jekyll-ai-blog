---
audio: false
generated: true
image: false
lang: en
layout: post
title: Essential Linux macOS Dev Commands
translated: false
type: note
---

Question: What are the commonly used terminal commands (like `ls`, `pwd`, `ps`) in macOS or Linux for development?

Answer:

Here is a comprehensive reference of frequently used terminal commands for developers on macOS and Linux, organized by category.

---

## 📁 Navigation & Directory

| Command | Description | Example |
| --- | --- | --- |
| `pwd` | Print current working directory | `pwd` |
| `ls` | List files in current directory | `ls -la` |
| `cd` | Change directory | `cd ~/projects` |
| `mkdir` | Create a new directory | `mkdir my-app` |
| `rmdir` | Remove an empty directory | `rmdir old-folder` |
| `find` | Search for files/directories | `find . -name "*.js"` |

**Useful `ls` flags:**

- `ls -l` — long listing with permissions, size, date
- `ls -a` — show hidden files (dotfiles)
- `ls -la` — combine both

---

## 📄 File Operations

| Command | Description | Example |
| --- | --- | --- |
| `touch` | Create an empty file | `touch index.js` |
| `cp` | Copy file or directory | `cp file.txt backup.txt` |
| `mv` | Move or rename file | `mv old.js new.js` |
| `rm` | Remove file | `rm -rf dist/` |
| `cat` | Print file content | `cat package.json` |
| `less` | Page through file content | `less app.log` |
| `head` | Show first N lines | `head -20 log.txt` |
| `tail` | Show last N lines (great for logs) | `tail -f server.log` |
| `nano` / `vim` | Text editors in terminal | `vim config.yaml` |

---

## 🔍 Search & Text

| Command | Description | Example |
| --- | --- | --- |
| `grep` | Search text inside files | `grep -r "TODO" ./src` |
| `sed` | Stream editor, find & replace | `sed 's/foo/bar/g' file.txt` |
| `awk` | Text processing / pattern scanning | `awk '{print $1}' file.txt` |
| `wc` | Count lines/words/chars | `wc -l file.txt` |
| `sort` | Sort lines of text | `sort names.txt` |
| `uniq` | Remove duplicate lines | `sort file.txt \| uniq` |

---

## ⚙️ Process Management

Commands like `ps`, `kill`, and `top`/`htop` are essential for process management on both macOS and Linux.

| Command | Description | Example |
| --- | --- | --- |
| `ps` | Show running processes | `ps aux` |
| `top` | Real-time process viewer | `top` |
| `htop` | Enhanced process viewer (install via Homebrew) | `htop` |
| `kill` | Kill a process by PID | `kill -9 1234` |
| `pkill` | Kill process by name | `pkill node` |
| `jobs` | List background jobs in shell | `jobs` |
| `bg` / `fg` | Resume job in background/foreground | `fg %1` |
| `&` | Run command in background | `node server.js &` |
| `lsof` | List open files (find what's using a port) | `lsof -i :3000` |

---

## 🌐 Network & HTTP

`curl` and `wget` are essential for transferring data to or from a server, particularly useful for testing APIs. `ssh` is used for securely connecting to remote servers, which is fundamental for deployment workflows.

| Command | Description | Example |
| --- | --- | --- |
| `curl` | Transfer data via URL / test APIs | `curl -I https://example.com` |
| `wget` | Download files from the web | `wget https://example.com/file.zip` |
| `ssh` | Secure shell into remote server | `ssh user@192.168.1.1` |
| `scp` | Securely copy files to/from remote | `scp file.txt user@host:/path` |
| `ping` | Test network connectivity | `ping google.com` |
| `netstat` | Show network connections | `netstat -an` |
| `ifconfig` / `ip` | Show network interface info | `ifconfig` (macOS) |
| `nslookup` | DNS lookup | `nslookup google.com` |

---

## 🗜️ Archives & Compression

| Command | Description | Example |
| --- | --- | --- |
| `tar` | Archive files | `tar -czvf archive.tar.gz ./dist` |
| `tar` (extract) | Extract archive | `tar -xzvf archive.tar.gz` |
| `zip` / `unzip` | Zip and unzip files | `zip -r out.zip ./folder` |
| `gzip` | Compress a file | `gzip file.txt` |

---

## 🔐 Permissions & Ownership

| Command | Description | Example |
| --- | --- | --- |
| `chmod` | Change file permissions | `chmod +x script.sh` |
| `chown` | Change file owner | `chown user:group file.txt` |
| `sudo` | Run command as superuser | `sudo npm install -g yarn` |
| `whoami` | Show current user | `whoami` |

---

## 💻 System Info & Disk

| Command | Description | Example |
| --- | --- | --- |
| `df` | Disk free space | `df -h` |
| `du` | Disk usage of directory | `du -sh ./node_modules` |
| `uname` | System info | `uname -a` |
| `uptime` | How long system has been running | `uptime` |
| `env` | Show environment variables | `env` |
| `export` | Set environment variable | `export NODE_ENV=production` |
| `echo` | Print text / variable value | `echo $PATH` |
| `history` | Show command history | `history` |
| `clear` | Clear terminal screen | `clear` |

---

## 🛠️ Developer-Specific

`git` is the cornerstone of version control — command-line proficiency is invaluable even if you also use GUI tools.

| Command | Description | Example |
| --- | --- | --- |
| `git` | Version control | `git log --oneline --graph --all` |
| `npm` / `yarn` / `pnpm` | Node.js package managers | `npm install` |
| `brew` | Homebrew package manager (macOS) | `brew install htop` |
| `docker` | Container management | `docker ps`, `docker-compose up` |
| `python3` / `node` | Run scripts | `python3 app.py` |
| `which` | Find location of a command | `which node` |
| `alias` | Create command shortcuts | `alias ll='ls -la'` |
| `xargs` | Build command from input | `find . -name "*.log" \| xargs rm` |
| `tee` | Read stdin and write to file + stdout | `npm test \| tee results.txt` |
| `man` | Show manual for a command | `man grep` |

---

## 🔗 Pipe & Redirection (Essential Concepts)

| Operator | Description | Example |
| --- | --- | --- |
| `\|` | Pipe output to another command | `ps aux \| grep node` |
| `>` | Redirect output to file (overwrite) | `echo "hello" > file.txt` |
| `>>` | Append output to file | `echo "line" >> file.txt` |
| `<` | Use file as input | `sort < names.txt` |
| `2>&1` | Redirect stderr to stdout | `cmd > out.txt 2>&1` |

---

## 💡 Tips

- Use `Ctrl + C` to cancel a running command
- Use `Ctrl + Z` to suspend, then `bg` to run in background
- Use `!!` to repeat the last command
- Use `Tab` for autocomplete
- Use `man <command>` to read the full manual for any command

References:

- [Mac Terminal Commands I Use Everyday](https://catalins.tech/mac-terminal-commands/)
- [macOS for Developers: Essential Skills](https://rakiabensassi.substack.com/p/macos-for-developers-5-essential)
- [Complete Mac Terminal Commands Cheat Sheet – GeeksforGeeks](https://www.geeksforgeeks.org/linux-unix/complete-mac-terminal-commands-cheat-sheet/)
- [Terminal Commands for Linux and OS X Users – TechBeamers](https://techbeamers.com/terminal-commands-linux-mac-osx/)
- [20 Mac Terminal Commands Every User Should Know – TechRepublic](https://www.techrepublic.com/article/16-terminal-commands-every-user-should-know/)
