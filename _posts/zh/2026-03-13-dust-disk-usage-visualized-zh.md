---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Dust 磁盘使用量快速可视化
translated: true
type: note
---

## dust 是什么？

**dust** = `du` 的更快、更美观的替代品。它是一个基于 Rust 的 CLI 工具，以树状格式显示磁盘使用情况，带有彩色输出、进度条和直观的排序。设计上比传统的 `du` 更美观、更高效，命令语法更简单。

**与 `du` 的主要区别：** dust 针对快速扫描和视觉清晰度进行了优化，而 `du` 更“原始”且冗长。

---

## 安装

```bash
brew install dust
```

在 Linux 上：
```bash
cargo install du-dust    # 如果你有 Rust/Cargo
sudo apt install dust    # Debian/Ubuntu（某些发行版）
```

在 macOS 上使用 MacPorts：
```bash
sudo port install dust
```

验证安装：
```bash
dust --version
```

---

## 基本用法

**扫描当前目录：**
```bash
dust
```

**扫描特定文件夹：**
```bash
dust ~/Downloads
```

**扫描主目录：**
```bash
dust ~
```

**扫描整个系统（需要 sudo）：**
```bash
sudo dust /
```

---

## 理解输出

运行 `dust` 时，你会看到类似以下内容：

```
 45.6 GiB │████████████████████│ Library
 28.3 GiB │█████████████        │ Projects
 18.7 GiB │██████████           │ Downloads
 12.1 GiB │██████               │ Applications
  8.4 GiB │████                 │ Desktop
  6.2 GiB │███                  │ Documents
```

**各列含义：**
- **第一个数字** = 文件夹大小
- **条形图** = 视觉表示（彩色、比例）
- **文件夹名称** = 目录名称

**默认情况下，dust：**
- 按大小排序（从最大开始）
- 只显示顶级项目
- 使用颜色提高可读性
- 包含美观的视觉条形图

---

## 命令行选项

### 排序与显示

| Flag | 功能 |
|------|------|
| `-r` | 反向排序（从小到大） |
| `-s` | 按大小排序（默认） |
| `-n` | 按名称字母顺序排序 |
| `-d` | 按修改日期排序 |
| `-e` | 按文件扩展名排序 |
| `-c` | 显示彩色输出（默认） |
| `-C` | 禁用彩色输出 |

### 限制与过滤

| Flag | 功能 |
|------|------|
| `-n <num>` | 只显示前 N 个结果（例如 `-n 20`） |
| `-d <depth>` | 限制递归深度（例如 `-d 2`） |
| `-X` | 排除匹配正则表达式的文件 |
| `-i` | 忽略大小写匹配 |
| `-z` | 排除隐藏文件 |

### 输出与显示

| Flag | 功能 |
|------|------|
| `-b` | 以字节打印大小 |
| `-k` | 以千字节打印大小 |
| `-m` | 以兆字节打印大小 |
| `-g` | 以吉字节打印大小 |
| `-T` | 以树状结构显示总计 |
| `-L` | 使用 ASCII 而非 Unicode |
| `-p` | 打印父目录的百分比 |
| `-A` | 聚合小文件 |
| `-h` | 显示帮助 |

---

## 常见用法模式

### 1. **查找 Downloads 中最大的文件夹**

```bash
dust ~/Downloads
```

输出按大小排名显示文件夹，从最大开始。

### 2. **限制为前 10 个结果**

```bash
dust -n 10 ~
```

只显示主目录中 10 个最大项目。

### 3. **仅显示 2 层深度**

```bash
dust -d 2 ~
```

适合获取高层概述，而不深入挖掘：

```
 85.4 GiB │████████████████████│ Library
          │                    │   ├─ Caches (32.1 GiB)
          │                    │   ├─ Application Support (28.7 GiB)
          │                    │   └─ Logs (12.8 GiB)
 45.2 GiB │███████████         │ Projects
          │                    │   ├─ LargeProject (28.3 GiB)
          │                    │   └─ OtherProject (16.9 GiB)
```

### 4. **反向排序（从小到大）**

```bash
dust -r ~/Downloads
```

有助于查看真正重要的内容与占用空间的内容。

### 5. **排除某些文件/文件夹**

```bash
dust -X 'node_modules|\.git' ~
```

跳过沉重的依赖和版本控制：

```bash
dust -X '\.cache|venv' ~/Projects
```

### 6. **显示百分比**

```bash
dust -p ~
```

显示每个文件夹占父目录的百分比：

```
 45.6 GiB (38%) │████████████████████│ Library
 28.3 GiB (24%) │█████████████        │ Projects
 18.7 GiB (16%) │██████████           │ Downloads
 12.1 GiB (10%) │██████               │ Applications
```

### 7. **扫描整个系统**

```bash
sudo dust -n 20 /
```

你的 Mac 上前 20 个最大目录。

### 8. **以树状显示总大小**

```bash
dust -T ~
```

包含显示累积大小的摘要树。

### 9. **忽略隐藏文件**

```bash
dust -z ~
```

排除点文件和隐藏文件夹（扫描更快）。

### 10. **自定义单位显示**

以兆字节显示大小：
```bash
dust -m ~/Downloads
```

或吉字节：
```bash
dust -g ~
```

---

## 实际场景

### 场景 1：清理 macOS 系统臃肿

```bash
sudo dust -d 2 ~/Library | head -20
```

查找：
- `Caches` — 安全删除
- `Logs` — 通常安全删除
- `Application Support` — 删除前检查

然后深入挖掘：

```bash
dust ~/Library/Caches -n 15
```

### 场景 2：查找最大的项目

```bash
dust -d 2 ~/Projects -n 10
```

识别哪些项目占用最多空间。

### 场景 3：检查 Downloads 中的旧安装程序

```bash
dust -d 1 ~/Downloads | grep -E '\.dmg|\.zip|\.iso'
```

或者直接：

```bash
dust ~/Downloads -n 20
```

### 场景 4：监控磁盘使用增长

定期扫描并比较：

```bash
dust -n 15 ~ > ~/Desktop/disk_usage_$(date +%Y%m%d).txt
```

比较输出以查看增长内容。

### 场景 5：查找旧的 Node/Python 缓存

```bash
dust -X 'node_modules|__pycache__|\.venv' ~
```

避免显示依赖文件夹，专注于实际代码/数据。

### 场景 6：扫描而不跟随符号链接

```bash
dust ~/Applications
```

适用于 applications 文件夹，而不深入 bundle。

---

## 高级组合

### 在 Downloads 中查找大文件，显示前 5 个

```bash
dust ~/Downloads -n 5
```

### 获取最大项目的完整树

```bash
dust -d 10 ~/Library -n 1
```

显示单个最大项目的整个树状结构。

### 导出结果到文件

```bash
dust -C ~ > disk_usage.txt
```

`-C` 禁用颜色，使文本文件干净。

### 美观打印百分比和前 20 个

```bash
dust -p -n 20 ~
```

### 同时扫描多个文件夹

```bash
dust ~/Downloads ~/Projects ~/Library
```

比较三个文件夹的顶级内容。

### 查找大于特定大小的文件

```bash
dust ~ -d 10 | grep GiB
```

过滤输出，只显示吉字节项目（即“大”项目）。

---

## dust 与 du 与 ncdu：快速比较

| 功能 | `du` | `dust` | `ncdu` |
|------|------|--------|--------|
| **速度** | ⚡⚡ 非常快 | ⚡⚡⚡ 最快 | ⚡⚡ 快 |
| **视觉** | 纯文本 | 美观、彩色 | 交互式 |
| **易用性** | 困难（许多标志） | 简单 | 简单 |
| **交互式** | 否 | 否 | ✅ 是 |
| **排序** | 手动 | 内置 | 内置 |
| **删除** | 手动 | 手动 | ✅ 直接删除 |
| **最适合** | 脚本/管道 | 快速概述 | 探索与清理 |

**何时使用每个：**
- **`dust`** — 你想要快速、美观的摘要：`dust ~/Downloads`
- **`du`** — 你在编写脚本或需要原始数据：`du -sh */ | sort -hr`
- **`ncdu`** — 你需要交互式探索和删除：`ncdu ~`

---

## 专业提示

### 提示 1：为常见扫描创建别名

添加到 `~/.zshrc` 或 `~/.bash_profile`：

```bash
alias dusthome='dust -p ~'
alias dustsys='sudo dust -p /'
alias dustdown='dust ~/Downloads'
alias dustlibs='sudo dust ~/Library -d 2'
```

然后只需：
```bash
dustdown
```

### 提示 2：与 `watch` 结合实现实时监控

```bash
watch -n 5 'dust -n 10 ~'
```

每 5 秒更新一次（适合监控活跃下载）。

### 提示 3：比较两个目录

```bash
dust ~/OldProject ~/NewProject
```

并排比较最大内容。

### 提示 4：查找大小重复的文件

虽然 dust 无法检测实际重复项，但你可以发现可疑模式：

```bash
dust -d 5 ~/Downloads | grep -E '500 MiB|1 GiB'
```

### 提示 5：检查应用大小

```bash
dust /Applications -d 1 -n 20
```

查看哪些应用占用最多空间。

### 提示 6：聚合小文件

```bash
dust -A ~/Downloads
```

`-A` 标志将小项目组合成“Other”，输出更干净。

---

## 将 dust 与其他工具结合

### 与 grep 结合进行过滤

只显示包含“GiB”的项目（大项目）：
```bash
dust ~ | grep GiB
```

### 管道到 head 获取前 N 个

```bash
dust ~ | head -15
```

### 查找大缓存

```bash
dust ~/Library/Caches -d 3 -n 20
```

### 检查特定文件类型

```bash
dust ~ -d 5 | grep -E '\.iso|\.dmg|\.zip'
```

---

## 故障排除

**dust 运行太慢？**
```bash
dust -z -X 'node_modules|\.git' ~
```
跳过隐藏文件和大依赖文件夹。

**想要排除多个模式？**
```bash
dust -X 'node_modules|\.git|\.cache|__pycache__' ~
```

**权限被拒绝？**
```bash
sudo dust /
```

**想要纯文本输出（无颜色）？**
```bash
dust -C ~ > results.txt
```

---

## 快速备忘单

```bash
dust                           # 扫描当前目录
dust ~                         # 扫描主目录
dust ~/Downloads               # 扫描特定文件夹
dust -n 20 ~                   # 显示前 20 个
dust -d 2 ~                    # 显示 2 层深度
dust -p ~                      # 显示百分比
dust -r ~/Downloads            # 反向排序（从小到大）
dust -X 'node_modules|\.git' ~ # 排除模式
dust -c ~/Library/Caches       # 计数文件（不可用，但有用组合）
sudo dust /                    # 扫描整个系统
dust -C ~ > output.txt         # 无颜色导出
```

---

## 总结

`dust` 完美适用于：
- ✅ 快速磁盘使用概述
- ✅ 快速找到空间占用大户
- ✅ 美观、彩色输出
- ✅ 简单命令语法
- ✅ 脚本与管道结果

当你想要速度和可读性时使用 **dust**，当你想要交互式探索和删除时使用 **ncdu**，当你编写脚本或需要最大控制时使用 **du**。

如果你有问题，请告诉我！