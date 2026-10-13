---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM驱动的SQLite风格C语言数据库
translated: true
type: note
---

已完成。**isql** 现已提交并完全可用——这是一个用 C 语言实现的极简 SQLite 风格数据库，其 SQL 解析全部由 LLM 完成。

## 构建了什么

```
你输入 → LLM（系统提示中包含实时表结构）→ JSON 查询计划 → C 语言引擎 → ASCII 表格
```

| 文件 | 作用 |
| --- | --- |
| `main.c` | REPL · 将表结构打包到提示中 · 调用 LLM · 打印结果 · 持久化 |
| `db.c/h` | 引擎：CREATE/DROP TABLE、INSERT、SELECT（WHERE/ORDER BY/LIMIT）、UPDATE、DELETE、主键自增 + 唯一性、类型强制转换（`int`/`real`/`text`）、JSON 文件持久化 |
| `json.c/h` | 手写 JSON 解析器/序列化器——计划传输格式 |
| `llm.c/h` | 基于 libcurl 的 OpenAI 兼容 `/chat/completions` 客户端 |
| `tests/` | 离线测试 `test_engine`（22 项检查）+ `mock_llm.py` 伪造 OpenAI 服务器 |

## AI 协议

LLM 从未见过 SQL——它返回九种计划动词之一（`{"op":"select","table":"users","where":{"age":{"gt":26}},...}`）。**二进制文件中完全没有 SQL 解析**；正确性取决于 `LLM_RULES` 中的提示协议。可配合 OpenAI 或任何兼容端点（Ollama 等）使用。

## 已验证

- `make test` — **22/22 项引擎检查通过**
- 通过 `ISQL_FAKE_LLM=1`（离线）进行的完整 REPL 会话：创建 → 插入 ×3 → 选择/排序/限制 → 更新 → 删除 → 描述，包括跨重启的持久化
- **真实 HTTP 路径已测试**：沙盒可访问 `api.openai.com`——返回了正确的 `401` 错误，我们的解析器正确显示了 OpenAI 的错误正文，同时出站 HTTPS/代理路径工作正常

## 期间发现并修复的 Bug

1. `json_obj_set` 存储键指针时未进行复制 → 列名双重释放 *（那个让你无法移开视线的崩溃）*
2. SELECT 结果存在相同根本原因：单元格与数据库共享，导致双重释放
3. UPDATE 不是替换而是追加重复键 → 读取到过期数据
4. DELETE 删除了不匹配的行（逻辑反转）
5. REPL 的 EOF 路径中存在 **双重 `free(stmt)`**（缺少 `stmt = NULL`）

## 运行

```sh
make
make test                                  # 离线
ISQL_FAKE_LLM=1 ./isql                     # 离线演示
ISQL_KEY=sk-... ISQL_MODEL=gpt-4o-mini ./isql   # 真实 AI 解析
```
