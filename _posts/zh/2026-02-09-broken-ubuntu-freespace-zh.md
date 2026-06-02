---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复受损 Ubuntu 系统的空闲空间
translated: true
type: note
---

Question: 在这种情况下（sudo 损坏，系统因巨大的 CUPS logs 导致空间不足，目前正从 Ubuntu live USB 启动），我可以安全删除 /usr 中的哪些文件或目录来释放空间？

Answer:

既然你已经在 live USB 环境中（或者可以 chroot 进入损坏的系统），你就拥有了 live session 提供的完整 root 权限 —— 这是在修复 sudo 之前释放空间的绝佳时机。目标是在不进一步破坏系统的前提下，删除 `/usr` 内部**巨大的、非关键的、可重新生成的或可安全移除的数据**。

**在 /usr 中最安全且最有效的删除项（从 live USB 操作）：**

1. **巨大的 CUPS log 文件**（目前为止最大的收益 —— 可能有 200–300 GB）
   这些**不在** `/usr` 中 —— 它们位于 `/var/log/cups/`。但既然你问到了 `/usr`，我还是将它们列为第一优先级：

   ```
   sudo rm -rf /mnt/root/var/log/cups/*
   # 或者只清空大文件：
   sudo truncate -s 0 /mnt/root/var/log/cups/error_log*
   sudo truncate -s 0 /mnt/root/var/log/cups/access_log*
   sudo truncate -s 0 /mnt/root/var/log/cups/page_log*
   ```

2. **实际上位于 /usr 内部、通常可以安全删除或清理的大型项目**

   - 旧的缓存 .deb 软件包（在运行已久的系统中通常有 5–30 GB）

     ```
     sudo rm -rf /mnt/root/usr/share/doc/*               # 文档 —— 通常 1–5 GB，安全
     sudo rm -rf /mnt/root/var/cache/apt/archives/*.deb  # 已下载的包 —— 非常安全，需要时会重新下载
     sudo rm -rf /mnt/root/var/cache/apt/archives/partial/*
     ```

   - Locale 数据（如果你只需要英语或少数几种语言）

     ```
     sudo rm -rf /mnt/root/usr/share/locale/{af,am,ar,as,az,be*,bg,bn*,bo*,br*,bs*,ca,cs,cy,da,de*,dz*,el,en_AU,en_CA,eo,es*,et*,eu*,fa*,fi,fr*,ga,gez*,gl*,gu*,haw,he*,hi*,hr,hu*,hy*,id*,is*,it*,ja*,ka*,kk*,km*,kn*,ko*,ku*,ky*,lo*,lt*,lv*,mg*,mi*,mk*,ml*,mn*,mr*,ms*,mt*,my*,nb*,ne*,nl*,nn*,no*,or*,pa*,pl,ps*,pt*,ro*,ru*,rw*,si*,sk*,sl*,sq*,sr*,sv*,sw*,ta*,te*,tg*,th*,ti*,tk*,tl*,tr*,tt*,uk*,ur*,uz*,vi*,wa*,xh*,yi*,yo*,zh*,zu*}
     ```

     （仅保留 en*, zh* 以及你使用的语言 —— 这可以释放 1–4 GB）

   - Man pages 和 info 文档（可以重新生成，通常 500 MB–2 GB）

     ```
     sudo rm -rf /mnt/root/usr/share/man/*
     sudo rm -rf /mnt/root/usr/share/info/*
     ```

   - 不需要的图标主题 / pixmaps（可能有 1–3 GB）

     ```
     sudo rm -rf /mnt/root/usr/share/icons/*             # 极端操作 —— 删除所有图标，仅在绝望时进行
     sudo rm -rf /mnt/root/usr/share/pixmaps/*
     ```

   - 旧内核（如果安装了许多 —— 请先检查）

     ```
     ls -lh /mnt/root/boot/vmlinuz* /mnt/root/boot/initrd.img*
     sudo rm -f /mnt/root/boot/vmlinuz-OLDVERSION /mnt/root/boot/initrd.img-OLDVERSION
     ```

     （只删除比当前版本旧的内核 —— 至少保留最新的一个 + 一个备份）

   - Snap 缓存 / 旧版本（如果使用了 snap —— 通常有几个 GB）

     ```
     sudo rm -rf /mnt/root/var/lib/snapd/cache/*
     sudo rm -rf /mnt/root/var/lib/snapd/snaps/*.old   # 旧的 snap 版本
     ```

   - Python / pip 缓存（有时很大）

     ```
     sudo rm -rf /mnt/root/usr/local/lib/python*/dist-packages/*/__pycache__/
     sudo rm -rf /mnt/root/root/.cache/pip/*
     ```

**快速清单 – 从 live USB 运行这些命令（将 /mnt/root 替换为你的挂载点）：**

```bash
# 首先处理影响最大的
sudo du -sh /mnt/root/var/log/cups/               # 确认大小
sudo rm -rf /mnt/root/var/log/cups/*

sudo du -sh /mnt/root/var/cache/apt/archives/
sudo rm -rf /mnt/root/var/cache/apt/archives/*.deb

sudo du -sh /mnt/root/usr/share/locale/
# 决定是否要精简它（见上文）

sudo du -sh /mnt/root/usr/share/doc/
sudo rm -rf /mnt/root/usr/share/doc/*

# 删除前检查
sudo du -sh /mnt/root/boot/
# 然后选择性地移除旧内核
```

**绝对不能在 /usr 中删除的东西（会导致系统严重崩溃）：**

- /usr/bin, /usr/sbin, /usr/lib, /usr/libexec, /usr/lib64
- /usr/share/applications, /usr/share/glib-2.0, /usr/share/mime
- 任何包含 libc, libstdc++, libgcc, openssl, ca-certificates 等内容的文件
- /usr/share/fonts （除非你非常清楚自己在做什么）

**释放空间后** → 继续执行之前信息中的 chroot + 修复 sudo 步骤。

如果你运行 `sudo du -sh /mnt/root/usr/* | sort -hr | head -20`，你将看到实际最大的目录，并可以进行更精准的决策。

References:

- [Ask Ubuntu: How to free space on root partition](https://askubuntu.com/questions/19914/how-to-free-up-space-on-the-root-partition)
- [Ubuntu Community Help: Freeing disk space](https://help.ubuntu.com/community/FreeingUpDiskSpace)
