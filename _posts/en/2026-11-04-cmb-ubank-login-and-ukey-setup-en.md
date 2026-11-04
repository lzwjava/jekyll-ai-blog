---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMB UBank Login and UKey Setup
translated: false
type: note
---

**Question:** What is the login username format for CMB UBank corporate banking, and how do you set up U盾?

**Answer:**

## Login Username Format

For CMB (招商银行) UBank corporate banking, the login identity is **not** literally "company name + username" as free text. The actual format is:

- **企业编号 (Company Code)** — a numeric code assigned by CMB when the company opened the corporate banking account
- **操作员编号 / 用户名 (Operator Code / Username)** — assigned per individual user (admin, maker, approver)

These are two separate fields in the UBank login screen. The company code and user code are both set during the account opening process at the branch — the bank prints them in the password envelope delivered with the UKey.

> If you're unsure of your company code or username, check the **密码信封 (password envelope)** that came with the UKey, or contact your CMB account manager.

---

## U盾 (UKey) Setup Steps

The UBank client required is version 10.3.9.656 or above. Download it from: CMB homepage → Corporate Business → U-BANK Software Download.

**Step 1 — Enter Registration Page**
Launch UBank and insert the admin's UKey. The system will automatically pop up the "Register New Certificate" window.

**Step 2 — Fill in Certificate Info**
The system auto-detects the UKey certificate number and matches it to any unregistered admin users. Set an **8-digit certificate password** (no repeating or sequential digits).

**Step 3 — Fill in Admin User Info**
The last 4 digits of the ID number are the ones written on the application form submitted when opening the corporate banking account. Set an **8-digit login password** (no repeating or sequential digits).

**Step 4 — Get Verification Code**
Click "Get Verification Code" — it is sent to the admin's registered mobile phone or email. Valid for 5 minutes.

**Step 5 — Complete Registration**
Confirm the info and click "Confirm" to finish certificate and admin registration. You can then log in to UBank.

---

**Key things to double-check:**
- UKey light should be on when inserted (indicates hardware is recognized)
- Use a Windows PC with IE-compatible browser or the dedicated UBank desktop client
- If the UKey is not detected, verify the Smart Card service is set to **Automatic** in Windows Services

**References:**
- [招商银行网上企业银行初次使用指南 (PDF)](https://market.cmbchina.com/mpage/online/220516150452657/wyccsyzn/wyccsyzn.pdf)
- [CMB English Corporate Internet Banking](https://english.cmbchina.com/Corporate/Internet/Default.aspx)
