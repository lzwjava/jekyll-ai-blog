---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SEC EDGAR 金融预训练语料库
translated: true
type: note
---

**问题：** Hugging Face 上的 `kapilrao/SEC-EDGAR` 数据集是什么？

**答案：**

这是一个大规模金融文档预训练语料库——590GB、800万份文件、430亿个token——从SEC EDGAR数据库抓取而来。由Datamule、Teraflop AI和Eventual共同构建。

**每行数据结构：**

| 字段 | 描述 |
|---|---|
| `content` | 原始SEC SGML文件内容 |
| `text` | 解析后的纯文本（已去除HTML/XML） |
| `metadata_accession-number` | 唯一的SEC文件ID |
| `metadata_filing-date` | 提交日期 |
| `metadata_period` | 涵盖期间 |
| `metadata_filer` | 公司名称、CIK、SIC代码、地址等 |
| `metadata_documents` | 文件类型、序号、描述 |

**文件分类（高token量部分）：**

- 10-Q：175亿token（季度报告）
- 10-K：145亿token（年度报告）
- 8-K：35亿token（重大事件）
- S-1：29亿token（IPO文件）
- 20-F：29亿token（外国私人发行人）

**对你为何重要：** 你是一家全球银行的AI工程师。这正是适合用于以下场景的领域专用语料库：

1. **微调或继续预训练** 金融大语言模型（使用10-K和10-Q文件对Llama/Mistral进行LoRA微调）
2. **构建RAG管道** 基于SEC文件进行盈利分析、风险披露提取
3. **训练金融NER/分类模型**（元数据中已包含SIC代码——免费标签）
4. **评估大语言模型的金融推理能力**——结构化元数据可轻松构造问答对

`datamule-python`库也值得收藏——它允许你通过股票代码+文件类型编程拉取文件，绕过EDGAR每秒10次请求的限制。
