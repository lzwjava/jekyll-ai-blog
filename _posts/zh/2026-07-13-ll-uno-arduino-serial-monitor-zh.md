audio: false
generated: true
image: false
lang: en
layout: post
title: `ll uno` Arduino Serial Monitor
translated: false
type: note

以下是本次会话所做工作的全面总结：

---

## 会话总结：`ll uno` 子命令 — Arduino UNO 串口监视器

### 项目背景

`ll` 是一个 Rust CLI 工具（`/home/xiaoxin/projects/ll/`），带有 ratatui TUI 界面。它已包含 `info`（系统信息）、`gcloud` 和 `word2vec` 子命令。仓库中有一个 Arduino 草图文件（`sketch_jul9a/sketch_jul9a.ino`），用于读取 A0 引脚上的麦克风信号，并通过串口以 9600 波特率输出振幅值。

### 目标

添加一个 `cargo run -- uno status` 命令，用于读取 Arduino 的串口输出并在实时 TUI 中显示。

### 改动内容

**1. `Cargo.toml`** — 添加了 `serialport = "4.7"` 依赖以便访问串口。

**2. `src/uno.rs`**（新文件，232 行）— 包含两个子命令：

- **`uno listen`** — 将原始串口数据输出到标准输出。经测试可用：以 9600 波特率从 `/dev/ttyUSB0` 读取振幅值（麦克风范围为 44–65）。
- **`uno status`** — TUI 界面，包含：
  - 顶部信息栏显示端口/波特率
  - 实时振幅显示（超过 30 阈值时变为绿色加粗）
  - 滚动折线图（200 个样本，Y 轴自动缩放）
  - 统计信息栏：最小值、最大值、平均值、采样数
  - 按 `q` 或 `Esc` 退出

**3. `src/main.rs`** — 添加了模块、匹配分支及更新帮助文本。

### 遇到的问题及解决方案

| 问题 | 原因 | 修复方法 |
| ------ | ------ | ---------- |
| 未安装 Rust 工具链 | 新开发机器 | 通过 rustup 安装 |
| 缺少 `libudev-dev` | `serialport` crate 需要该依赖 | `apt install libudev-dev` |
| `/dev/ttyUSB0` 权限被拒绝 | 用户不在 `dialout` 组 | 使用 `sg dialout`（与用户已有模式相同） |
| 通过 `sg` 运行时出现 ENXIO 错误 | `sg` 将标准输入与 TTY 分离，导致 `enable_raw_mode()` 失败 | 重写读取循环以使用 `BufReader`（与 `listen` 相同模式）；添加帮助性错误消息，指导用户使用 `sudo usermod -a -G dialout` |

### 使用方法

```bash
# 推荐：将用户添加到 dialout 组一次，然后直接运行
sudo usermod -a -G dialout $USER
# 注销并重新登录

cargo run -- uno status          # TUI 界面带图表
cargo run -- uno listen          # 原始串口数据输出
```

### Git 提交

```
b2b62f8  feat: 添加 Arduino 串口监视器的 uno 子命令
  5 个文件变更，新增 433 行，删除 12 行
  创建模式 100644 src/uno.rs
```
