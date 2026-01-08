---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Advanced Outlook Email Search Techniques
translated: false
type: note
---

Question: How to use "AND", "OR", or other advanced techniques to search in Outlook emails?

Answer: 

Microsoft Outlook supports advanced search techniques in both the desktop application and the web version (Outlook on the web) to help you find emails more precisely. The search box is located at the top of the window or page.

### Basic Principles
- By default, multiple words without operators act as **AND** (e.g., "project budget" finds emails containing both words).
- Use **quotes** for exact phrases: "project budget".
- Operators like **AND**, **OR**, **NOT** must be in uppercase.
- Use parentheses **()** for grouping complex queries.

### In Outlook Desktop (Windows)
Outlook uses **Instant Search** with Keyword Query Language (KQL).

#### Common Keywords (field operators)
- **from:** sender (e.g., from:john@example.com)
- **to:** recipient
- **subject:** in subject line
- **body:** in message body
- **hasattachment:yes** or **hasattachment:no**
- **received:** date (e.g., received:2025 or received:>01/01/2025)
- **category:** color category

#### Using AND and OR
- **AND** (default or explicit): project AND budget (both words anywhere)
- **OR**: project OR budget (either word)
- Combine fields: (subject:project OR body:project) AND from:john

#### Examples
- Emails with "report" in subject from John: subject:report from:john
- Emails with attachments containing "invoice" or "bill": hasattachment:yes (invoice OR bill)
- Emails received last week with "meeting": received:lastweek meeting
- Complex: (from:alice OR from:bob) AND (subject:urgent OR category:red)

#### Additional Techniques
- Click the search box to open the **Search** tab on the ribbon, then use **Refine** options (e.g., From, Subject, Has Attachments) – these add operators automatically.
- For very complex searches: Go to **Search Tools > Advanced Find** (Ctrl+Shift+F). Use the Advanced tab to add multiple conditions, or enable Query Builder via registry for full AND/OR control.
- Search scope: Choose Current Folder, All Subfolders, Current Mailbox, or All Mailboxes.

### In Outlook on the Web (browser version)
Uses **Advanced Query Search (AQS)**, similar but with some differences.

#### Common Keywords
- **from:**
- **to:**
- **subject:**
- **body:** (may vary)
- Others like **attachments:**, **received:**

#### Using AND and OR
- AND is implied for multiple terms.
- Explicit **AND**, **OR**, **NOT**.
- Examples often use colon syntax.

#### Examples
- subject:report
- from:john subject:(project OR budget)
- hasattachments:yes invoice

#### Additional Techniques
- Click **Filters** next to the search box for options like From, To, Date, Attachments.
- For more: Type keywords directly (e.g., subject:keyword).

Note: The web version may have slightly fewer advanced fields than desktop, but basic AND/OR work similarly. Search is often faster in the web version for large mailboxes.

These techniques work across most recent versions (Outlook for Microsoft 365, 2021, etc.). If results seem incomplete, ensure indexing is complete (desktop: File > Options > Search > Indexing Options).

References:  

- [How to search in Outlook - Microsoft Support](https://support.microsoft.com/en-us/office/how-to-search-in-outlook-d824d1e9-a255-4c8a-8553-276fb895a8da)  
- [Search Mail and People in Outlook on the web - Microsoft Support](https://support.microsoft.com/en-us/office/search-mail-and-people-in-outlook-on-the-web-b27e5eb7-3255-4c61-bf16-1c6a16bc2e6b)  
- [Instant Search query commands reference](https://www.howto-outlook.com/howto/searchcommands.htm)