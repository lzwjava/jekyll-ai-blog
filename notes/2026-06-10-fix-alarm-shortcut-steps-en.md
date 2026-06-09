---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Alarm Shortcut Steps
translated: false
type: note
---

Now here's what you need to fix in the shortcut. Open "ww-create-alarm-signed" in Shortcuts.app and set up these actions:

**Action 1: Receive text input from Shortcuts**
- Already set (Input Type = Text)

**Action 2: Split Text**
- Input: Shortcut Input
- Separator: Custom
- Custom Separator: `|`

**Action 3: Get Item from List**
- Input: Split Text result
- Item: Item at Index, Index: 1

**Action 4: Date**
- Input: Item from List result (this parses "HH:MM" into a Date)

**Action 5: Get Item from List**
- Input: Split Text result (from Action 2)
- Item: Item at Index, Index: 2

**Action 6: Create Alarm**
- Time: Date result (from Action 4)
- Label: Item from List result (from Action 5)

The input format will be `HH:MM|label` (e.g. `01:38|clothes`). After you update the shortcut, test with:

```
ww alarm 3 "clothes"
```

Let me know when you've updated it and I'll test.
