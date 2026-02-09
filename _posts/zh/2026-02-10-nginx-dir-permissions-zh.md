---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Nginx 目录权限详解
translated: true
type: note
---

**Question:** 请解释一下这里 nginx 目录及其文件的权限：

lzw@to:~$ ls -alrt nginx  
total 28  
drwxr-x--- 81 lzw lzw 4096 Feb 10 02:53 ..  
drwxrwxr-x 2 lzw lzw 4096 Feb 10 02:56 .  
-rw-r--r-- 1 lzw lzw 412 Feb 10 02:58 access.log  
-rw-r--r-- 1 lzw lzw 14938 Feb 10 02:58 error.log

**Answer:**

此输出显示了一个自定义目录 `/home/lzw/nginx`（或类似路径），这可能是你在尝试以 `lzw` 用户身份运行 nginx 时，为了存储 nginx logs 而创建的。  
让我们逐步分解权限和所有权（ownership）的每个部分。

### 目录列表逐行解析

1. `drwxr-x--- 81 lzw lzw 4096 Feb 10 02:53 ..`  
   - 这是 **父目录**（极有可能是 `/home/lzw`）。  
   - 权限：`drwxr-x---`  
     - `d` → 这是一个 directory  
     - Owner (lzw): rwx (read, write, execute)  
     - Group (lzw): r-x (read + execute，无 write)  
     - Others: --- (无任何权限 – 完全无法访问)  
   → 只有你 (`lzw`) 可以在你的 home folder 中写入。其他用户（包括 www-data）甚至无法列出或进入该目录，除非你提供额外权限。

2. `drwxrwxr-x 2 lzw lzw 4096 Feb 10 02:56 .`  
   - 这是 **当前目录**（即 `nginx` 文件夹本身）。  
   - 权限：`drwxrwxr-x`  
     - Owner (lzw): rwx (完全访问权限)  
     - Group (lzw): rwx (完全访问权限 – 这不寻常，通常 group 只获得 r-x)  
     - Others: r-x (可以列出文件并进入文件夹，但不能写入)  
   → **重要提示：** 因为 “others” 拥有 `r-x` 权限，nginx process（当以 www-data 运行时）**可以进入此文件夹并查看文件名** — 但前提是它必须先能到达 `/home/lzw`（目前该路径对 others 的 `---` 权限阻断了访问）。

3. `-rw-r--r-- 1 lzw lzw 412 Feb 10 02:58 access.log`  
   - 普通文件 (`-`)  
   - 权限：`rw-r--r--`  
     - Owner (lzw): rw- (可以 read + write)  
     - Group (lzw): r-- (只能 read)  
     - Others: r-- (其他人都可以 read)  
   → 任何能够访问到该文件的 process（包括 www-data）**都可以读取**它，但只有你可以写入。

4. `-rw-r--r-- 1 lzw lzw 14938 Feb 10 02:58 error.log`  
   - 与 access.log 相同：所有人可读，仅 owner `lzw` 可写。

### 为什么当前的设置会导致问题

当 nginx 以 **www-data** 运行（默认/正确的方式）时：

- www-data **不是** 用户 `lzw`
- www-data **不在** `lzw` 组（你的私有组）中
- 因此 www-data 属于 **“others”** 类别
- 要在 `/home/lzw/nginx` 中读取/写入 logs，www-data 需要：
  1. 对 `/home/lzw` 有 Execute (`x`) 权限 → 目前 others 为 `---` → **在这里被拦截**
  2. 对 `/home/lzw/nginx` 有 Execute (`x`) 权限 → 拥有 `r-x` → 正常
  3. 对 log 文件有 Read (`r`) 权限 → 拥有 `r--` → 正常
  4. 对 log 文件有 Write (`w`) 权限 → 拥有 `r--` → **没有写入权限**

→ 主要阻碍：**你的 home 目录没有 execute 权限**（`/home/lzw` 对 others 是 `---`）。

### 如何解决（两个清晰的方案）

**方案 1 – 推荐：让 nginx 重新使用默认 logs**

撤销自定义 logs 和自定义用户的尝试：

```bash
# 删除任何自定义的 user 行
sudo sed -i '/^user\s/d' /etc/nginx/nginx.conf

# 如果你添加了 User=lzw，删除 systemd override
sudo rm -f /etc/systemd/system/nginx.service.d/override.conf
sudo systemctl daemon-reload

# 正常重启（logs 将回到 /var/log/nginx/）
sudo nginx -t && sudo systemctl restart nginx
```

然后修复你的电影文件夹访问权限：

```bash
sudo chgrp -R www-data /home/lzw/qDownloads
sudo chmod -R g+rx /home/lzw/qDownloads
sudo chmod g+x /home/lzw
```

**方案 2 – 将自定义 logs 保留在 ~/nginx 但使其对 nginx 可写**

如果你希望 nginx (www-data) 在此处写入 logs：

```bash
# 允许 nginx 进入你的 home 目录
sudo chmod o+x /home/lzw

# 将 nginx 文件夹及其文件的 group 更改为 www-data
sudo chgrp -R www-data ~/nginx

# 给 group 对文件的 write 权限 + 对目录的 execute 权限
sudo chmod -R g+rw ~/nginx/*.log
sudo chmod g+w ~/nginx
```

或者更简单（但安全性较低）的方法：

```bash
sudo chmod -R o+rw ~/nginx
```

但再次重申：使用默认设置的 `/var/log/nginx/` 更整洁、更规范。

**总结 – 当前状态一句话概括**

你的 `~/nginx` 文件夹和 logs 对所有人可见，但 nginx (www-data) 目前甚至无法到达你的 home 目录，并且由于缺少 group/write 权限，也无法写入 logs。

**References:**

- 无需参考文献 – 这是标准的 Linux `ls -l` 权限解释。