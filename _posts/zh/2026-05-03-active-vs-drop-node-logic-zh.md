---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 主动节点与关闭节点逻辑详解
translated: true
type: note
---

这是完整的图解：

## ACTIVE与DROP的工作原理

### 两个关键枚举类型（`models.py:12-54`）

```python
class NodeStatus(str, Enum):
    ACTIVE = "ACTIVE"           # 存活的，可继续扩展
    PRUNED_BY_RULE = "PRUNED_BY_RULE"  # 因硬性物理规则被剔除
    PRUNED_BY_SLM = "PRUNED_BY_SLM"   # 因软评分被剔除（预留）

class NodeResultState(str, Enum):
    PASS = "PASS"    # 本轮存活
    DROP = "DROP"    # 死亡 —— 不再扩展
```

仅当**同时**满足以下两个条件时节点才会被标记为`DROP`：
```python
self.node.status = NodeStatus.PRUNED_BY_RULE
self.node.result_state = NodeResultState.DROP
self.node.fsm_state = FSMState.FINALIZED   # 不再进行状态转移
```

---

### DROP的触发时机

**1. 在`calculate`阶段**（`builder.py:295-310`）—— `skills.py`中的`tot_hard_rule_check`返回`physical_violations`：
```python
if not hard_rule_result["passed"]:
    if physical_violations:
        → status = PRUNED_BY_RULE, result_state = DROP
```

**2. 在`evaluate`阶段**（`builder.py:396-416`）—— 评估结果本身包含`hard_rule_violations`：
```python
if breakdown.hard_rule_violations:
    → status = PRUNED_BY_RULE, result_state = DROP
```

---

### 不会导致DROP的情况

- **低评分** —— `builder.py:76`处的文档字符串已明确说明：*"低评分从不剪除节点；仅降低下游扩展优先级。"* 节点保持`ACTIVE`状态，仅排名降低。
- **可恢复的违规** —— 会被送往`REFLECT`状态重试而非直接丢弃（`builder.py:317`）。
- **根节点违规** —— 通过`_bounce_root_rule_violations()`特殊处理：获得反思机会而非立即DROP。

---

**一句话总结：** 只有硬性物理规则违规（由`skills.py`检测）才会将节点转为`DROP`状态。软评分仅影响扩展优先级，节点仍保持`ACTIVE`状态。