---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 避免过度使用大模型的日志记录
translated: true
type: note
---

问题：
如何设计一个简单的日志系统（类似`wwlogs/log-history.txt`），使用基于时间戳的文件名并允许可选的可读名称，以避免过度使用LLM API来命名和搜索日志，目前（如在Meta）过度使用AI是否导致了令牌浪费？

答案：
你指出了一个非常现实且实际的问题：**人们过度使用LLM来处理本应确定且廉价的任务**。日志命名就是一个典型例子。

让我们把问题分为两部分：**系统设计**和**AI过度使用问题**。

---

# 1. 简洁实用的日志设计（无需LLM）

你的想法很合理。实际上，*它比在这个用例中使用AI更好*。

### ✅ 核心设计

* 默认文件名：
  `yyyyMMdd_HHmmss`（例如`20260417_153045.txt`）
* 可选参数：
  `--friendly-name "vpn_issue_coffee_shop"`

最终文件名：

```
20260417_153045__vpn_issue_coffee_shop.txt
```

---

## 为何此方案优于LLM命名

* **确定性** → 无随机性
* **可搜索** → grep / fzf / ripgrep 可即时搜索
* **低成本** → 零令牌消耗
* **可组合** → 可在shell流水线中工作
* **稳定** → 无幻觉或奇怪命名

你实际上是在运用一个经典原则：

> 如果一个问题可以用函数解决，就不要使用模型。

---

## 建议的CLI设计

示例命令：

```bash
wwlog "VPN在咖啡店连接失败" --friendly-name vpn_issue
```

生成文件：

```
wwlogs/20260417_153045__vpn_issue.txt
```

---

## 最简实现（bash）

```bash
#!/bin/bash

LOG_DIR="wwlogs"
mkdir -p "$LOG_DIR"

timestamp=$(date +"%Y%m%d_%H%M%S")

friendly=""

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --friendly-name) friendly="$2"; shift ;;
    *) message="$1" ;;
  esac
  shift
done

if [ -n "$friendly" ]; then
  filename="${timestamp}__${friendly}.txt"
else
  filename="${timestamp}.txt"
fi

echo "$message" > "$LOG_DIR/$filename"

echo "已保存：$LOG_DIR/$filename"
```

---

## 日志搜索（无需AI）

```bash
# 关键词搜索
rg vpn wwlogs/

# 模糊查找
fzf --preview "cat {}" < <(ls wwlogs)

# 时间过滤
ls wwlogs | grep 20260417
```

---

## 可选升级：结构化日志（仍无需AI）

替代纯文本：

```json
{
  "time": "2026-04-17T15:30:45",
  "tag": "vpn_issue",
  "content": "VPN在咖啡店连接失败"
}
```

现在可以：

```bash
jq '.tag == "vpn_issue"' *.json
```

仍然**零令牌消耗**。

---

# 2. 是否应该使用LLM进行命名/搜索？

简短回答：**几乎永远不要**。

仅在以下情况使用LLM：

* 需要**语义聚类**（“将相似日志分组”）
* 忘记关键词并希望**自然语言检索**
* 需要**自动生成摘要**

否则：

> 文件名 + grep > LLM

---

# 3. 关于AI过度使用（例如Meta内部推动）

你的直觉方向正确，但不够完整。

### 是的，存在浪费

当公司推行“处处用AI”时：

* 简单任务 → LLM调用
* 重复提示 → 令牌激增
* 无缓存 → 重复开销

这导致：

* 更高的基础设施成本
* 延迟开销
* 有时更差的用户体验

---

### 但这并非纯粹浪费

像Meta这样的公司正在优化：

* **行为改变**（早期强制采用）
* **数据收集**（人们如何实际使用AI）
* **长期杠杆效应**，而非短期效率

因此内部接受：

> 当前低效 → 未来能力

---

# 4. 真正原则（重要）

你已经从正确的抽象层面思考：

### 使用此决策规则：

| 任务类型             | 工具          |
| -------------------- | ------------- |
| 确定性任务           | 代码 / 脚本   |
| 结构化检索           | grep / 数据库 |
| 模糊匹配 / 语义任务  | LLM           |
| 创造性 / 未知任务    | LLM           |

---

# 5. 你的思路（优化版）

你正在构建的本质上是一个：

> **“LLM最小化个人知识系统”**

关键特征：

* 基于时间戳的索引
* 人类可读标签
* 原生shell检索
* 可选的LLM层（非默认）

这实际上比“处处用LLM”*更具扩展性*。

---

# 最终结论

* 你的日志设计是**正确且高效的**
* 使用LLM命名日志属于**过度设计**
* 是的，当前AI使用趋势中存在真实的令牌浪费
* 但企业正在用成本换取学习与速度

---

如果你需要，我可以将其扩展为：

* 完整的`wwlog`工具（带标签、搜索、摘要功能）
* 或混合系统（本地日志 + 可选LLM语义搜索）

这才是真正强大的方向。