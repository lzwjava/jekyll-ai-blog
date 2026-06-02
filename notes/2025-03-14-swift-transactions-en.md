---
audio: false
generated: true
lang: en
layout: post
title: How SWIFT Transactions Work
translated: false
type: note
---

### How Do SWIFT Transactions Work Across Multiple Banks?

SWIFT, which stands for **Society for Worldwide Interbank Financial Telecommunication**, is a global network that enables banks to securely and efficiently exchange information about financial transactions. It’s important to understand that SWIFT does not move money itself; rather, it facilitates the communication of instructions between banks to make those transfers happen. Here’s a detailed explanation of how SWIFT transactions work, including the role of SWIFT codes and how banks integrate with the SWIFT system, especially across multiple banks.

---

#### **What Is a SWIFT Transaction?**
A SWIFT transaction refers to the process of sending standardized messages through the SWIFT network to instruct banks on how to transfer funds from one account to another. These messages contain critical details like the amount, currency, sender and recipient account information, and the banks involved. The actual movement of money happens separately through banking settlement systems, which we’ll explore later.

For example, if you want to send money from a bank in the United States to a bank in Germany, SWIFT ensures that the instructions are communicated accurately and securely between the two banks, even if they don’t have a direct relationship.

---

#### **The Role of SWIFT Codes**
Every bank participating in the SWIFT network has a unique identifier called a **SWIFT code** (also known as a **Bank Identifier Code** or **BIC**). This code, typically 8 or 11 characters long, identifies the specific bank and often its branch in a transaction. For instance:
- **Bank A in the US** might have a SWIFT code like `BOFAUS3N`.
- **Bank B in Germany** might have a code like `DEUTDEFF`.

When you initiate a transfer, you provide the recipient bank’s SWIFT code to ensure the instructions reach the correct institution.

---

#### **How SWIFT Transactions Work Step-by-Step**
Let’s break down the process of a SWIFT transaction across multiple banks using a simple example: sending $1,000 from Bank A (in the US) to Bank B (in Germany).

1. **Initiation**
   You provide Bank A with the transfer details:
   - Amount: $1,000
   - Recipient’s account number at Bank B
   - Bank B’s SWIFT code (e.g., `DEUTDEFF`)
   Bank A may convert the $1,000 to euros (e.g., 850 euros) based on the exchange rate, though this can vary depending on the banks’ policies.

2. **Message Creation**
   Bank A creates a standardized SWIFT message, such as an **MT103** (used for single customer credit transfers). This message includes:
   - Sender details (Bank A and your account)
   - Recipient details (Bank B and your friend’s account)
   - Amount and currency (e.g., 850 euros)
   - Instructions for processing the payment

3. **Sending the Message**
   Bank A transmits the MT103 message through the SWIFT network. The network ensures secure delivery using encryption and authentication measures.

4. **Routing Through Banks**
   - **Direct Relationship**: If Bank A and Bank B have accounts with each other, Bank A sends the message directly to Bank B.
   - **Intermediary Banks**: If they don’t, the message is routed through one or more **correspondent banks** (e.g., Bank C). For example:
     - Bank A sends the message to Bank C, instructing it to debit Bank A’s account with Bank C and credit Bank B’s account with Bank C.
     - Bank C forwards the instructions to Bank B, specifying the funds are for your friend’s account.
   Intermediary banks are common in international transfers when direct relationships don’t exist.

5. **Receiving and Processing**
   Bank B receives the SWIFT message, verifies the details, and prepares to credit your friend’s account with 850 euros.

6. **Settlement of Funds**
   Since SWIFT only handles messaging, the actual money movement occurs through settlement mechanisms:
   - **Direct Accounts**: If Bank A has a **nostro account** (an account in euros at Bank B), Bank B debits it and credits your friend’s account.
   - **Correspondent Banking**: If an intermediary (Bank C) is involved, Bank A settles with Bank C, and Bank C settles with Bank B via their respective accounts.
   - **Central Clearing Systems**: For some currencies (e.g., euros in the Eurozone), settlement might occur through systems like **TARGET2**.

7. **Completion**
   Your friend’s account at Bank B is credited with 850 euros. Fees may be deducted at various stages (by Bank A, intermediaries, or Bank B), and the process can take a few hours to several days, depending on the banks and intermediaries involved.

---

#### **How Banks Integrate with the SWIFT System**
To participate in SWIFT transactions, banks must integrate with the network. Here’s how they do it:

- **Membership**: Banks join SWIFT as members, agreeing to its rules and standards.
- **Infrastructure**: They install SWIFT-approved software and hardware to connect to the SWIFT network, a private, secure system separate from the public internet.
- **SWIFT Codes**: Each bank is assigned a unique SWIFT code to identify it in transactions.
- **Message Standards**: Banks use standardized message formats (e.g., MT103) with specific fields to ensure compatibility across the network.
- **Security**: SWIFT mandates encryption, digital signatures, and compliance with security protocols to protect against fraud and tampering.
- **Additional Services**: Beyond payments, banks use SWIFT for trade finance, securities transactions, and administrative messages, requiring further integration for these functions.

---

#### **Key Features and Considerations**
- **Standardization**: SWIFT’s use of structured messages (like MT103) ensures all banks interpret instructions the same way.
- **Security**: The network employs robust measures to safeguard transaction data.
- **Fees and Timing**: Intermediary banks may charge fees, and processing times vary based on the number of banks involved.
- **Modern Enhancements**: Initiatives like **SWIFT gpi** (Global Payments Innovation) improve transparency and speed by offering end-to-end tracking and faster settlement.

---

#### **Summary**
SWIFT transactions work by enabling banks to send secure, standardized messages (via SWIFT codes) to instruct fund transfers across borders. The process involves creating and routing messages—sometimes through intermediary banks—and settling funds separately via direct accounts, correspondent relationships, or clearing systems. Banks integrate with SWIFT by becoming members, setting up the necessary infrastructure, and adhering to its protocols. This system ensures that money moves reliably between accounts, even across multiple banks worldwide.
