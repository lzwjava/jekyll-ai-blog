---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting Textarea Value with JavaScript
translated: false
type: note
---

Question: What JavaScript code can set the value of this `<textarea>`?

Answer:

For your textarea:

```html
<textarea autocomplete="off" rows="3" style="max-height:100px;" id="q12" name="q12"></textarea>
```

use this JavaScript:

```javascript
document.getElementById("q12").value = "your text here";
```

If the page uses React/Vue/Angular and normal `.value` does not update the internal state properly, use:

```javascript
const textarea = document.getElementById("q12");

textarea.value = "your text here";

textarea.dispatchEvent(new Event("input", { bubbles: true }));
textarea.dispatchEvent(new Event("change", { bubbles: true }));
```

You can run it in:

* Browser DevTools Console
* Bookmarklet
* Tampermonkey userscript
* Injected script

Example:

```javascript
const textarea = document.getElementById("q12");

textarea.value = `
Hello interviewer,

This is inserted programmatically.
`;

textarea.dispatchEvent(new Event("input", { bubbles: true }));
```

If the textarea is inside an iframe:

```javascript
const iframe = document.querySelector("iframe");

const textarea =
  iframe.contentDocument.getElementById("q12");

textarea.value = "hello";
textarea.dispatchEvent(new Event("input", { bubbles: true }));
```

If there are multiple textareas:

```javascript
document.querySelectorAll("textarea")[0].value = "hello";
```

Or specifically:

```javascript
document.querySelector('textarea[name="q12"]').value = "hello";
```
