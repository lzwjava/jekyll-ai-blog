---
audio: false
generated: true
image: false
lang: en
layout: post
title: Backtick and Tilde Key Functions
translated: false
type: note
---

**Question:** What key is near number 1 on a typical macOS keyboard — two keys up from Tab, and below Esc?

**Answer:**

That's the **backtick/tilde key** — `` ` `` / `~`.

Layout context:

```
[ Esc ]  [ 1 ][ 2 ][ 3 ]...
[  `~  ]  [ Q ][ W ][ E ]...
[ Tab  ]  [ A ][ S ][ D ]...
```

So `` ` `` sits:
- **Left of `1`**
- **Above `Tab`**
- **Below `Esc`**

---

### The two characters on this key

| Key combo | Character | Name |
|-----------|-----------|------|
| (plain) | `` ` `` | backtick / grave accent |
| `Shift` + `` ` `` | `~` | tilde |

---

### Why this key matters (especially for you)

**1. Shell — `cd` home shortcut**
```bash
cd ~        # ~ expands to $HOME
cd ~/projects/lzwjava.github.io
```

**2. Backtick in Markdown — inline code and fences**
````
`inline code`

```python
# fenced code block
```
````

**3. Python/JS template literals (JS)**
```js
const msg = `Hello ${name}, tokens used: ${count}`;
```

**4. Vim — jump to last cursor position**
```
``    # jump back to exact position
`^    # jump to last insert position
`.    # jump to last change
```

**5. tmux / terminal — backtick as prefix key**
Some tmux configs use `` ` `` as the prefix instead of `Ctrl-b`:
```bash
set -g prefix `
```

**6. Bash — command substitution (legacy style)**
```bash
# Old style (backtick) — avoid in new scripts
result=`ls -la`

# Modern preferred style
result=$(ls -la)
```

**7. macOS — switch input source shortcut**
`Ctrl + `` ` ``  is sometimes bound to cycle IME input sources (relevant if you switch between English/Chinese input).

---

The key you're thinking of is `` ` `` — one of the most overloaded keys on the keyboard for a developer.
