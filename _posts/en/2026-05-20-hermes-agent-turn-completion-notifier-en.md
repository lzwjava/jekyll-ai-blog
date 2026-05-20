---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Turn Completion Notifier
translated: false
type: note
---

Question: Can you explain what this Bash script does?

Answer:

This script is a **post-processing hook** for the Hermes agent on macOS. It’s designed to notify the user whenever Hermes completes a turn in a conversation. Let’s break it down step by step:

---

### 1. **Script Metadata**

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/on-agent-done.sh
```

* Shebang (`#!/usr/bin/env bash`) ensures the script runs with Bash.
* The script lives in `~/.hermes/agent-hooks/` and is triggered when Hermes finishes a turn.

---

### 2. **Bash Safety Options**

```bash
set -euo pipefail
```

* `-e` → Exit if any command fails.
* `-u` → Treat unset variables as an error.
* `-o pipefail` → Makes the script fail if any part of a pipeline fails.

This makes the script robust and avoids silent errors.

---

### 3. **Read Payload**

```bash
payload="$(cat -)"
```

* Reads JSON input from `stdin`. Hermes passes info about the turn to the hook via JSON.

---

### 4. **Extract Data Using Python**

```bash
extracted=$(echo "$payload" | python3 -c "
import json, sys
data = json.load(sys.stdin)

# Directory name from cwd
cwd = data.get('cwd', '')
import os
dirname = os.path.basename(cwd) if cwd else 'unknown'

# First 10 chars of user message
extra = data.get('extra', {})
user_msg = extra.get('user_message', '')[:10]

# Conversation history item count
history = extra.get('conversation_history', [])
hist_count = len(history)

print(f'{dirname}|{user_msg}|{hist_count}')
" 2>/dev/null) || extracted="unknown||0"
```

* Uses Python to parse the JSON safely.
* Extracts three key pieces of info:

  1. `dirname` → Current working directory name (if available).
  2. `user_msg` → First 10 characters of the user's last message.
  3. `hist_count` → Number of conversation turns so far.
* Outputs a `|`-separated string for Bash to parse.
* If anything fails, defaults to `"unknown||0"`.

---

### 5. **Split Extracted Values**

```bash
IFS='|' read -r dirname user_preview hist_count <<< "$extracted"
```

* Uses `IFS='|'` to split the string into three variables:

  * `dirname` → folder name
  * `user_preview` → snippet of user message
  * `hist_count` → conversation turns

---

### 6. **Build Notification Subtitle**

```bash
subtitle="msg: ${user_preview}  |  turns: ${hist_count}"
```

* Combines the extracted info into a small string for the macOS notification.

---

### 7. **Send macOS Notification**

```bash
osascript -e "
display notification \"Hermes has completed one turn.\" with title \"Hermes Agent — ${dirname}\" subtitle \"${subtitle}\" sound name \"Glass\"
" >/dev/null 2>&1 || true
```

* Uses `osascript` (AppleScript via shell) to display a notification:

  * **Title:** `"Hermes Agent — <directory>"`
  * **Subtitle:** `"msg: <first 10 chars> | turns: <count>"`
  * **Sound:** `"Glass"`
* Redirects all output to `/dev/null` to keep it silent.
* `|| true` ensures the script doesn’t fail even if notifications are blocked.

---

### 8. **Return Empty JSON**

```bash
printf '{}\n'
```

* Outputs `{}` so Hermes’ hook system knows the script completed successfully.
* Acts as a “silent no-op” response.

---

### ✅ **Summary**

* This hook triggers after each Hermes agent turn.
* Extracts basic context: directory, user message preview, and conversation length.
* Sends a **non-intrusive macOS notification**.
* Fails gracefully if anything goes wrong.

It’s a **simple but effective way to keep track of Hermes’ activity visually on macOS**.

---

If you want, I can also **draw a small flow diagram showing how JSON moves from Hermes → this script → macOS notification**, which makes the flow easier to understand.

Do you want me to do that?