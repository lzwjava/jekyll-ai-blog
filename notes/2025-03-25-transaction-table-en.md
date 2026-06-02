---
audio: false
generated: true
lang: en
layout: post
title: Transaction Table
translated: false
type: note
---

A **transaction table** in a banking system typically stores details of all financial transactions processed by the bank. This table is essential for tracking customer transactions, reconciling accounts, and ensuring regulatory compliance.

---

### **Key Fields in a Banking Transaction Table**

| **Field Name**           | **Data Type** | **Description** |
|--------------------------|--------------|----------------|
| **Transaction_ID**       | `VARCHAR` / `BIGINT` | Unique identifier for each transaction |
| **Account_Number**       | `VARCHAR` / `BIGINT` | Customer’s bank account number involved in the transaction |
| **Transaction_Type**     | `VARCHAR` | Type of transaction (e.g., DEPOSIT, WITHDRAWAL, TRANSFER, PAYMENT) |
| **Transaction_Amount**   | `DECIMAL(15,2)` | Amount involved in the transaction |
| **Currency_Code**        | `VARCHAR(3)` | Currency of the transaction (e.g., USD, EUR, INR) |
| **Transaction_Date**     | `DATETIME` | Timestamp when the transaction occurred |
| **Value_Date**           | `DATETIME` | Date when the transaction is settled or processed |
| **Debit_Credit_Flag**    | `CHAR(1)` | Indicator whether the transaction is a **Debit ('D')** or **Credit ('C')** |
| **Counterparty_Account** | `VARCHAR` | Destination account number (if applicable) |
| **Transaction_Mode**     | `VARCHAR` | Payment method (SWIFT, RTGS, NEFT, ACH, UPI, Card, Wallet, etc.) |
| **Transaction_Status**   | `VARCHAR` | Status of the transaction (PENDING, SUCCESS, FAILED, REVERSED) |
| **Reference_Number**     | `VARCHAR` | Unique identifier for external systems (e.g., SWIFT Reference, UTR, UPI Transaction ID) |
| **Transaction_Description** | `TEXT` | Additional details about the transaction (e.g., “Bill Payment - Electricity”, “Salary Credit”) |
| **Branch_Code**          | `VARCHAR(10)` | Identifier for the bank branch processing the transaction |
| **Transaction_Fee**      | `DECIMAL(10,2)` | Any charges deducted for the transaction |
| **Exchange_Rate**        | `DECIMAL(10,6)` | Exchange rate applied if currency conversion is involved |
| **Initiating_Channel**   | `VARCHAR` | Channel used for transaction (ATM, Mobile Banking, Internet Banking, POS, Teller) |
| **Fraud_Check_Status**   | `VARCHAR` | Status of fraud detection (e.g., PASSED, FLAGGED, UNDER REVIEW) |
| **Reversal_Transaction_ID** | `VARCHAR` | If reversed, links to the original transaction ID |

---

### **Example Transaction Records**

| Transaction_ID | Account_Number | Type      | Amount  | Currency | Date                 | Debit/Credit | Counterparty | Mode   | Status  |
|---------------|---------------|-----------|---------|----------|----------------------|--------------|--------------|--------|---------|
| 100001       | 123456789012   | DEPOSIT   | 1000.00 | USD      | 2025-03-25 10:15:00 | C            | -            | ATM    | SUCCESS |
| 100002       | 123456789012   | TRANSFER  | 500.00  | USD      | 2025-03-25 12:30:00 | D            | 987654321098 | SWIFT  | SUCCESS |
| 100003       | 987654321098   | TRANSFER  | 500.00  | USD      | 2025-03-25 12:30:00 | C            | 123456789012 | SWIFT  | SUCCESS |
| 100004       | 123456789012   | PAYMENT   | 50.00   | USD      | 2025-03-25 14:00:00 | D            | Utility Co.  | ACH    | PENDING |

---

### **How These Fields Are Used in Banking**

1. **Transaction Tracking:** Every transaction has a unique ID and can be tracked through its status.
2. **Account Reconciliation:** Helps in matching debits and credits for accurate financial records.
3. **Fraud Detection:** Suspicious transactions can be flagged using fraud check status and monitoring transaction patterns.
4. **Regulatory Reporting:** Ensures compliance with financial regulations (AML, KYC, Basel III).
5. **Customer Service:** Helps banks resolve disputes and inquiries regarding failed or pending transactions.

Would you like a more detailed schema with SQL queries? 🚀
