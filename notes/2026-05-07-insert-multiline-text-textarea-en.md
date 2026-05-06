---
audio: false
generated: true
image: false
lang: en
layout: post
title: Insert Multiline Text into Textarea
translated: false
type: note
---

Question: How can I easily insert multiple lines of text into a textarea with JavaScript when copying is difficult?

Answer:

Yes. The easiest way is to use a JavaScript **template string** with backticks `` ` `` so you can keep multiline content directly.

Example:

```javascript id="kj6ojg"
const text = `
Line 1
Line 2
Line 3

Another paragraph here.
`;

const textarea = document.getElementById("q12");

textarea.value = text;

textarea.dispatchEvent(new Event("input", { bubbles: true }));
```

---

# Better Method: Use Prompt Popup

This avoids escaping quotes manually.

Run:

```javascript id="nwwc6x"
const text = prompt("Paste your content here:");

const textarea = document.getElementById("q12");

textarea.value = text;

textarea.dispatchEvent(new Event("input", { bubbles: true }));
```

Then:

1. browser popup appears
2. paste large content there
3. automatically inserted into textarea

This is usually the most convenient approach.

---

# Super Convenient Bookmarklet

Create a browser bookmark with this as URL:

```javascript id="g3cixv"
javascript:(()=>{const t=prompt("Paste text");const e=document.getElementById("q12");e.value=t;e.dispatchEvent(new Event("input",{bubbles:true}))})()
```

Then:

* open interview page
* click bookmark
* paste content
* done

---

# Even Better: Read From Clipboard Automatically

Modern browsers support:

```javascript id="4kt81j"
(async () => {
  const text = await navigator.clipboard.readText();

  const textarea = document.getElementById("q12");

  textarea.value = text;

  textarea.dispatchEvent(new Event("input", { bubbles: true }));
})();
```

This directly inserts your clipboard contents.

You may need:

* HTTPS page
* clipboard permission
* user interaction first

---

# For Huge Text

If content is very large, simulated typing is safer:

```javascript id="9gq31o"
(async () => {
  const text = await navigator.clipboard.readText();

  const el = document.getElementById("q12");

  el.focus();

  for (const ch of text) {
    el.value += ch;

    el.dispatchEvent(
      new Event("input", { bubbles: true })
    );

    await new Promise(r => setTimeout(r, 1));
  }
})();
```

This looks more like real typing to some systems.