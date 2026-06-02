---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 掌握 ncdu 进行磁盘清理
translated: true
type: note
---

## ncdu 是什么？

**ncdu** = **NCurses Disk Usage**。它是一个交互式终端工具，可以精确显示哪些文件夹和文件占用了磁盘空间，并提供一个可视化的树状结构，您可以实时导航和探索。将它想象成一个“磁盘使用浏览器”——比管道 `du` 命令更快、更直观。

---

## 安装

```bash
brew install ncdu
```

在 Linux 上：
```bash
sudo apt install ncdu    # Debian/Ubuntu
sudo yum install ncdu    # Red Hat/CentOS
```

---

## 基本用法

**扫描整个 home 目录：**
```bash
ncdu ~
```

**扫描特定文件夹：**
```bash
ncdu ~/Downloads
```

**扫描整个系统（需要 sudo）：**
```bash
sudo ncdu /
```

**排除某些目录（更快扫描）：**
```bash
ncdu --exclude node_modules --exclude .git ~/Projects
```

---

## 理解界面

ncdu 启动时，您会看到类似以下内容：

```
 ncdu 1.16 ~ Total: 245.3 GiB  Apparent size: 120.4 GiB  Items: 89543

 --- /Users/yourname ---
  45.2 GiB [####################] /Library
  32.1 GiB [####################] /Projects
  28.5 GiB [####################] /Downloads
  12.3 GiB [####################] /Applications
   8.7 GiB [####################] /Desktop
   ...
```

**各列含义：**
- **左侧数字** = 该文件夹/文件的尺寸
- **条形图** = 相对尺寸的可视化表示
- **文件夹/文件名** = 路径

---

## 键盘导航

| Key | Action |
|-----|--------|
| **↑ / ↓** | 在列表中上下移动 |
| **→ / Enter** | 打开/展开文件夹 |
| **← / Backspace** | 返回父文件夹 |
| **d** | 删除选中的文件/文件夹（需确认） |
| **q** | 退出 ncdu |
| **n** | 按名称排序 |
| **s** | 按尺寸排序（从大到小） |
| **a** | 按表观尺寸排序 |
| **?** | 显示帮助菜单 |
| **r** | 刷新/重新扫描当前目录 |
| **i** | 显示文件详情（权限、日期等） |
| **c** | 显示子项数量 |
| **e** | 导出结果到文件 |
| **g** | 切换百分比/图表显示 |

---

## 常见工作流程

### 1. **查找并删除大文件夹**

```bash
ncdu ~/Downloads
```

1. 按 `↓` 导航到最大的文件夹
2. 按 `→` 展开查看内部内容
3. 找到罪魁祸首（旧视频、备份等）
4. 按 `d` 删除
5. 用 `y` 确认

### 2. **扫描整个 home 目录**

```bash
ncdu ~
```

非常适合查找“神秘空间占用者”。常见罪魁祸首：
- `~/Library/Caches` — 旧应用缓存（安全删除）
- `~/Library/Logs` — 累积日志
- `~/Downloads` — 您忘记的旧文件
- `~/.Trash` — 未完全删除的清空文件
- `~/Applications` — 旧/重复应用

### 3. **查找大文件（不仅仅是文件夹）**

默认情况下，ncdu 显示文件夹。要查看单个大**文件**：
1. 按 `→` 展开文件夹
2. 查找尺寸较大的文件
3. 文件显示时没有尾随的 `/`

### 4. **并排比较文件夹尺寸**

```bash
ncdu ~/Projects
```

然后使用 **`s`** 按尺寸排序。立即看到哪个项目文件夹最大。

### 5. **排除垃圾并加速扫描**

```bash
ncdu --exclude node_modules --exclude .git --exclude .venv --exclude venv ~
```

跳过重量级但非必需的文件夹（依赖、版本控制、虚拟环境）。

---

## 高级用法

### 导出结果到文件

在 ncdu 内按 **`e`** 导出到文本文件（适用于报告）。

```bash
ncdu ~ --output results.txt
```

然后稍后查看：
```bash
ncdu --file results.txt
```

### 扫描并立即删除大项目

```bash
ncdu -r ~
```

`-r` 标志禁止删除确认（小心使用！）。

### 非交互模式（仅打印总数）

```bash
ncdu -0 ~ | head -20
```

以简单格式显示输出，而不使用交互式 UI。

### 忽略挂载卷

```bash
ncdu --one-file-system ~
```

不进入挂载驱动器/网络（适合避免扫描外部驱动器）。

---

## 专业提示

### 提示 1：检查 macOS 系统臃肿

```bash
ncdu ~/Library
```

导航到：
- `Caches` — 旧应用缓存文件（通常安全删除）
- `Logs` — 累积系统日志
- `Application Support` — 应用特定数据（此处要小心）

### 提示 2：查找重复文件

虽然 ncdu 不直接查找重复文件，但您可以发现模式：
```bash
ncdu ~/Downloads
```

查找电影、归档文件或安装程序的多个副本。

### 提示 3：监控尺寸随时间增长

在不同时间导出结果：
```bash
ncdu --output ~/Desktop/scan_$(date +%Y%m%d).txt ~
```

稍后比较输出以查看增长内容。

### 提示 4：与 `find` 结合进行精确删除

查找大于 1GB 的所有文件：
```bash
find ~ -size +1G -type f
```

然后打开 ncdu 可视化后再手动删除。

### 提示 5：安全清理 macOS 缓存

```bash
sudo ncdu ~/Library/Caches
```

导航每个缓存文件夹并用 **`d`** 删除。大多数可以安全移除（应用会重新创建它们）。

---

## 常见删除场景

### 场景 1：清理 Downloads 文件夹

```bash
ncdu ~/Downloads
```

1. 按尺寸排序 (`s`)
2. 查找旧 .dmg 安装程序、zip 文件、旧项目
3. 按 `→` 确认文件夹内容
4. 按 `d` 删除

### 场景 2：移除旧 Xcode/Developer 缓存

```bash
ncdu ~/Library/Developer
```

包含旧模拟器、构建产物——往往数百 GB。导航并选择性删除旧版本。

### 场景 3：清除 Node 包依赖

```bash
ncdu ~/Projects
```

导航到每个项目，检查 `node_modules` 文件夹尺寸，如果有 `package.json` 则删除（可以用 `npm install` 重新安装）。

---

## 与其他工具比较

| Tool | Best For | Speed | Ease |
|------|----------|-------|------|
| **ncdu** | 交互式探索与删除 | Fast | 🟢 Easy |
| **du** | 快速 CLI 单行命令 | Very fast | 🟡 Medium |
| **dust** | 漂亮 CLI 输出 | Fast | 🟡 Medium |
| **Grand Perspective** | 可视化 GUI 概览 | Medium | 🟢 Easy |

---

## 故障排除

**ncdu 在某些文件夹上挂起？**
```bash
ncdu --exclude .git --exclude node_modules ~
```

**权限被拒绝错误？**
```bash
sudo ncdu ~
```

**想要扫描但不具有删除权限？**
```bash
ncdu -r ~    # 只读模式
```

---

## 快速备忘单

```bash
ncdu ~                           # 开始扫描 home
ncdu ~/Downloads                 # 扫描 Downloads
sudo ncdu /                      # 扫描整个系统
ncdu --exclude node_modules ~    # 跳过重型文件夹
ncdu --one-file-system ~         # 不跟随挂载
```

**ncdu 内：**
- **↑↓** = 导航
- **→** = 展开文件夹
- **←** = 返回
- **d** = 删除
- **s** = 按尺寸排序
- **q** = 退出

---

这应该为您提供掌握 ncdu 并回收磁盘空间所需的一切！如果遇到任何问题，请告诉我。
