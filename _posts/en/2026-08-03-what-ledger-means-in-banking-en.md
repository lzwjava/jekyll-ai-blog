---
audio: false
generated: true
image: false
lang: en
layout: post
title: What Ledger Means in Banking
translated: false
type: note
---

Question: What does "ledger" mean in banking?

Answer: A ledger is the master record of all financial transactions for an account or entity — every debit and credit, in order, with a running balance. It's the source of truth; every other report (statement, balance sheet, income statement) is derived from it.

Core mechanics:
- **Double-entry**: every transaction hits at least two accounts — one debit, one credit — so the ledger always balances (Assets = Liabilities + Equity).
- **General ledger (GL)**: the top-level ledger containing all accounts (cash, receivables, payables, revenue, expenses, etc.).
- **Sub-ledgers**: detailed ledgers feeding into the GL — e.g., accounts receivable ledger (per-customer balances), accounts payable ledger (per-vendor balances). Their totals roll up into a single GL control account.
- **Bank's internal ledger vs. your account statement**: when you see "pending" vs "posted" transactions, that's literally the bank's ledger balance vs. available balance — the ledger updates on settlement, not on authorization.

Minimal example (this is literally how it's modeled under the hood, e.g. in Postgres or a ledger-style datastore):

```sql
CREATE TABLE ledger_entries (
    id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    entry_type CHAR(1) CHECK (entry_type IN ('D','C')), -- debit/credit
    amount NUMERIC(18,2) NOT NULL,
    tx_ref TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- balance = sum(credits) - sum(debits) for asset accounts (or reverse for liability)
SELECT account_id,
       SUM(CASE WHEN entry_type='C' THEN amount ELSE -amount END) AS balance
FROM ledger_entries
GROUP BY account_id;
```

Every transfer, payment, or fee is two rows inserted atomically (one D, one C) — that atomicity + immutability (append-only, no updates/deletes) is what "ledger" means as a data structure, and it's exactly why crypto/blockchain co-opted the term ("distributed ledger").

References:
- [Investopedia — General Ledger](https://www.investopedia.com/terms/g/generalledger.asp)
- [Double-entry bookkeeping — Wikipedia](https://en.wikipedia.org/wiki/Double-entry_bookkeeping)