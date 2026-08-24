---
audio: false
generated: true
image: false
lang: en
layout: post
title: Frontend Source Code Analysis
translated: false
type: note
---

Question: Is copying frontend source code to AI a powerful way to understand forms and hidden rules?

Answer:

Yes, this is a very effective technique. Modern web forms are basically **executable specifications**. The visible page is only one layer; the real rules are often distributed across:

```
Browser UI
    ↓
HTML structure
    ↓
JavaScript validation
    ↓
API request payload
    ↓
Backend validation
    ↓
Database/business rules
```

The frontend source can reveal many things that are not obvious from the page:

### 1. Hidden field requirements

Example:

```html
<input name="passportNumber" required>
<input name="previousNationality" style="display:none">
```

The page may not tell you clearly that `previousNationality` matters, but the code does.

AI can quickly scan:

* required fields
* regex validation
* allowed formats
* dropdown options
* conditional fields

---

### 2. Business logic hidden in JavaScript

Example:

```javascript
if (country === "CN") {
    showField("hukou");
}
```

The user sees:

> Country: China

But the code says:

> If China, ask for extra document.

AI can explain these conditions.

---

### 3. API payload is often the real specification

Open browser DevTools:

```
F12
 → Network
 → Submit form
 → Inspect request
```

You may see:

```json
{
  "passportNo": "XXXX",
  "educationLevel": "MASTER",
  "employmentHistory": [
     {
       "company": "...",
       "years": 8
     }
  ]
}
```

This tells you what the backend actually receives.

For immigration/government systems, this is especially useful because the PDF instructions may be written for humans, while the API schema is written for machines.

---

### 4. AI is good at reverse engineering forms

A good workflow:

```
Save page source
        |
        v
Give HTML + JS to AI
        |
        v
Ask:

"Analyze this form.
Find:
1. required fields
2. hidden validation rules
3. conditional logic
4. possible rejection reasons
5. document requirements"
```

Then inspect network calls.

---

Your observation:

> 数字世界 一切皆代码 一切皆规则

is basically correct for software systems.

A form is not really a "paper form". It is a state machine:

```
state 1:
personal information

      |
      v

state 2:
eligibility check

      |
      v

state 3:
document upload

      |
      v

state 4:
submission validation
```

The UI is just a visualization of this state machine.

---

The TOEFL experience is a good example. Traditional users see:

> "The exam failed because network problem."

An engineer sees:

```
browser
  |
websocket/session
  |
authentication
  |
camera/microphone permission
  |
bandwidth
  |
latency
  |
server timeout
  |
proctoring system
```

Each layer has logs and failure modes.

The advantage of being technical is that you can debug the system instead of just suffering from it.

The next evolution is probably:

```
Human:
"Fill this government application"

AI agent:
- reads rules
- analyzes frontend
- prepares documents
- checks consistency
- fills fields
- detects missing items
```

A lot of bureaucracy is essentially a UI problem sitting on top of deterministic rules. AI is very suitable for this because it can combine unstructured documents + code + workflows.
