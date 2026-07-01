---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 macOS 磁盘弹出问题
translated: true
type: note
---

## 快速解决方案

### 1. **使用 Activity Monitor (GUI)**

- 打开 **Activity Monitor** (Applications > Utilities)
- 点击 **Disk** 选项卡
- 查找使用外部驱动器的进程
- 选择进程并点击停止按钮 (⊘)
- 然后再次尝试弹出

### 2. **使用 Terminal (命令行)**

#### 查找使用磁盘的内容

```bash
# 将 DISKNAME 替换为实际磁盘名称（例如 MyDrive、Untitled 等）
lsof | grep DISKNAME

# 或使用此命令查看所有已挂载卷上的打开文件
lsof +D /Volumes
```

#### 识别磁盘挂载点

```bash
# 列出所有已挂载卷及其路径
mount | grep -E "Volumes|media"

# 或使用 diskutil
diskutil list
```

#### 查找访问驱动器的进程

```bash
# 将 /Volumes/DISKNAME 替换为实际路径
lsof | grep "/Volumes/DISKNAME"

# 显示进程名称和 PID (进程 ID)
```

#### 终止进程

```bash
# 将 PID 替换为实际进程 ID（例如 1234）
kill -9 PID

# 或按名称终止（不够精确，会影响所有实例）
killall -9 processname
```

---

## 逐步说明

### **方法 1: Activity Monitor (最简单)**

1. 打开 **Spotlight Search** (⌘ + Space)
2. 输入 "Activity Monitor" 并按 Enter
3. 在打开的窗口中，点击 **Disk** 选项卡
4. 在列表中查找磁盘名称（右侧显示 "I/O Read Bytes" 和 "I/O Write Bytes"）
5. 识别哪个进程正在访问它
6. 点击进程 → 点击 **Stop** 按钮（红色圆圈带 ⊘）
7. 确认强制退出
8. 再次尝试弹出磁盘

### **方法 2: Terminal (更多控制)**

1. 打开 **Terminal** (Applications > Utilities)

2. **查找磁盘挂载点：**

   ```bash
   diskutil list
   ```

   查找外部驱动器名称。记下挂载点（例如 `/Volumes/MyDrive`）

3. **查找使用该磁盘的进程：**

   ```bash
   lsof | grep "/Volumes/MyDrive"
   ```

   将 "MyDrive" 替换为实际磁盘名称

4. **检查输出** - 你会看到：

   ```
   COMMAND   PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
   Finder    123   user   cwd    DIR    1,2        4096 1234 /Volumes/MyDrive
   ```

   - **COMMAND**：进程名称
   - **PID**：进程 ID（需要终止的数字）

5. **终止进程：**

   ```bash
   kill -9 123
   ```

   将 123 替换为实际 PID

6. **再次尝试弹出**，从 Finder 或通过 Terminal：

   ```bash
   diskutil eject /Volumes/MyDrive
   ```

---

## 常见锁定磁盘的进程

| 进程 | 原因 | 解决方案 |
| ------ | ------ | ---------- |
| `Finder` | 浏览磁盘 | 关闭该磁盘的 Finder 窗口 |
| `Spotlight` | 索引驱动器 | 为外部驱动器禁用 Spotlight (System Settings > Siri & Spotlight) |
| `Backup` 或 `Time Machine` | 自动备份运行中 | 等待备份完成或禁用 |
| `Google Drive`、`Dropbox`、`OneDrive` | 云同步进行中 | 退出应用或等待同步完成 |
| `Terminal` | 当前工作目录在磁盘上 | 更改目录：`cd ~` 然后尝试弹出 |
| `Preview`、`Word`、`Excel` | 文件已打开 | 关闭应用程序 |

---

## 高级：通过 Terminal 安全弹出

```bash
# 首先，查找磁盘标识符（显示为 /dev/diskX）
diskutil list

# 使用标识符弹出（首选方法）
diskutil eject /dev/disk2

# 或按挂载点弹出
diskutil eject /Volumes/MyDrive

# 强制弹出（最后手段，立即卸载）
diskutil secureEject /Volumes/MyDrive
```

---

## 预防提示

1. **将外部驱动器添加到 Spotlight 排除列表：**
   - System Settings > Siri & Spotlight
   - 点击外部驱动器旁边的 "Exclude"

2. **使用正确弹出方法：**
   - 不要直接拔插——始终先弹出
   - 在 Finder 中右键磁盘 → Eject

3. **弹出前关闭应用程序：**
   - 保存并关闭驱动器上打开的任何文件
   - 弹出前退出云同步应用

4. **避免后台操作：**
   - 不要在弹出前启动备份或同步
   - 等待 Spotlight 索引完成（如果重新启用）

---

## 如果无效

```bash
# 列出所有已挂载卷
mount

# 强制卸载（谨慎使用 - 如果有写入待处理，可能导致数据丢失）
sudo umount -f /Volumes/MyDrive

# 或使用 diskutil
sudo diskutil unmountDisk force /Volumes/MyDrive
```

⚠️ **警告：** 使用 `sudo` 和强制卸载应作为最后手段，因为如果文件正在写入，可能导致数据丢失。
