---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内存过载诊断与修复
translated: true
type: note
---

这是最新的情况。有些东西已经发生了变化。

---

## 当前内存占用大户

| 排名 | 项目 | 内存 | 进程数 | 结论 |
|---|---|---|---|---|
| **1** | **CGPDFService** (×8) | **~16 GB** | 8 | 某处打开了PDF文件 → 关闭它们 |
| **2** | **VSCode** | **~23 GB** | 25 | 关闭不用的项目 |
| **3** | **WeChat** | **~20 GB** | 12 | 仍在运行！ |
| **4** | **mds_stores** (Spotlight) | **~14 GB** | 1 | 正在重建索引 — 暂时性的 |
| **5** | **Browsers** (Safari + WebKit) | **~13.5 GB** | 27 | 标签页太多 |
| 6 | Python | 2.8 GB | 2 | 取决于正在运行的内容 |
| 7 | Microsoft (Teams/Office) | 1.7 GB | 4 | 如不使用请退出 |
| 8 | GitHub Desktop | 1.5 GB | 1 | 如不使用请退出 |
| 9 | Ghostty | 1.3 GB | 1 | 正常 |

**总需求**：约95 GB 在 16 GB 物理内存上。你的机器能撑下来真是个英雄。

---

## 接下来清理什么（按影响大小排序）

**1. 关闭微信** — 尽管之前建议过，它还在运行

```
pkill -9 WeChat WeChatAppEx WeApp
```

仅这一项就能减少20 GB的虚拟内存需求。小程序引擎是你系统中最占用资源的部分。

**2. 关闭产生 CGPDFService 的 PDF 文件**

你有 **8 个 CGPDFService 进程** 占用约16 GB。这些进程是在 Safari、预览或邮件打开 PDF 时产生的。找到哪个应用打开了 PDF，然后关闭相应标签或窗口。

```
# 快速检查哪些进程在使用 PDF
lsof -c CGPDFService 2>/dev/null | head -5
```

**3. 关闭 VSCode 项目**

25个进程 × 每个约1 GB。只保留你正在编辑的那个项目，其余用 `Cmd+Q` 退出。

**4. 再等两分钟让 Spotlight 完成**

mds_stores 占用14 GB，仍在擦除后重建索引。一旦完成，它会降到接近0。

---

要我帮你关闭微信并找出哪个 PDF 是打开的吗？这两个步骤能立即释放约36 GB的内存压力。
