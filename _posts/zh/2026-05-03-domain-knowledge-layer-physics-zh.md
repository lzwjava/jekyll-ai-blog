---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 物理学领域知识层
translated: true
type: note
---

`skills.py`是FSM/思维树引擎在推理过程中调用的**领域知识层**。

## 存在意义

FSM负责**搜索控制**（节点扩展、评分、剪枝）但不具备物理知识。`skills.py`填补了这一空白：

| FSM的职责 | skills.py的职责 |
|---|---|
| 状态转移、树搜索 | 物理计算（麦克斯韦、拉格朗日、量子力学等） |
| 决定探索哪个分支 | `tot_hard_rule_check` — 否决违反物理规则的节点 |
| 管理推理阶段 | `tot_stage_prompt_contract` — 注入阶段特定的提示词约束 |
| 加载领域配置 | `tot_domain_plugin_bundle` — 提供领域插件数据 |

核心调用位置：
- `fsm/builder.py:1050` — 在计算阶段调用`tot_hard_rule_check`；若公式违反物理规则，对应节点将被否决
- `fsm/backend.py:111` — 加载领域插件包
- `fsm/backend.py:130` — 获取当前推理阶段的提示词约束

**简而言之：** FSM是搜索框架；`skills.py`是物理“规则裁判+计算器”。两者共同实现了受约束的、具备物理感知的推理能力。