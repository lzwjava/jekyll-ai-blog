---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 银行业中分类账的含义
translated: true
type: note
---

问题：在银行业务中，“ledger（账本）”是什么意思？

回答：账本是账户或实体所有金融交易的完整记录——按顺序记录每一笔借方和贷方，并包含运行余额。它是数据的真实来源；所有其他报告（对账单、资产负债表、利润表）都由此衍生。

核心机制：

- **复式记账**：每笔交易至少影响两个账户——一个借方，一个贷方——因此账本始终平衡（资产 = 负债 + 权益）。
- **总账（GL）**：包含所有账户（现金、应收账款、应付账款、收入、费用等）的顶层账本。
- **明细账**：输入总账的详细账本——例如，应收账款明细账（按客户余额）、应付账款明细账（按供应商余额）。它们的总额汇总到总账的一个控制账户中。
- **银行内部账本与你的账户对账单**：当你看到“待处理”与“已入账”交易时，这实际上就是银行的账本余额与可用余额——账本在结算时更新，而非授权时更新。

最小示例（这实际上就是底层建模的方式，例如在 Postgres 或账本风格的数据存储中）：

```sql
CREATE TABLE ledger_entries (
    id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    entry_type CHAR(1) CHECK (entry_type IN ('D','C')), -- 借方/贷方
    amount NUMERIC(18,2) NOT NULL,
    tx_ref TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 对于资产账户，余额 = 贷方总和 - 借方总和（负债账户则相反）
SELECT account_id,
       SUM(CASE WHEN entry_type='C' THEN amount ELSE -amount END) AS balance
FROM ledger_entries
GROUP BY account_id;
```

每笔转账、支付或费用都以原子方式插入两行（一笔借方，一笔贷方）——这种原子性加上不可变性（仅追加，无更新/删除）正是“账本”作为数据结构的意义，这也正是加密货币/区块链借用该术语（“分布式账本”）的原因。

参考资料：

- [Investopedia — 总账](https://www.investopedia.com/terms/g/generalledger.asp)
- [复式记账法 — 维基百科](https://en.wikipedia.org/wiki/Double-entry_bookkeeping)
