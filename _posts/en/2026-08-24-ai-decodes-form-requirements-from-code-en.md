---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Decodes Form Requirements from Code
translated: false
type: note
---

Question: Is copying frontend source code to AI a useful trick for understanding form requirements, including hidden rules?

Answer:

Yes, this is a very effective technique, especially for government/enterprise forms. The visible webpage is often only the **presentation layer**; the actual validation logic may exist in JavaScript, HTML attributes, API requests, or hidden configuration.

A typical workflow:

```
Browser
  |
  |-- HTML
  |     ├── field names
  |     ├── required attributes
  |     ├── input types
  |     └── hidden fields
  |
  |-- JavaScript
  |     ├── validation rules
  |     ├── file size limits
  |     ├── accepted formats
  |     ├── conditional fields
  |     └── error messages
  |
  |-- Network API
        ├── backend validation
        ├── allowed values
        └── submission schema
```

Giving AI the frontend code can reveal things like:

### 1. Hidden required fields

Example:

```html
<input
  name="passportNumber"
  required
/>
```

The page may not visually show a red `*`, but the browser will reject empty values.

---

### 2. File upload rules

You may find:

```html
<input
 type="file"
 accept=".pdf,.jpg,.png"
>
```

or:

```javascript
if (file.size > 5 * 1024 * 1024) {
   alert("File too large");
}
```

This tells you:

* allowed formats
* maximum size
* whether PDF is preferred
* whether images are accepted

---

### 3. Conditional logic

Example:

```javascript
if (nationality === "China") {
   show("mainlandResidencePermit")
}
```

The webpage might not explain why a field appears, but code shows the rule.

---

### 4. Backend API schema

The most valuable part is often not the HTML but the network calls.

Open:

```
Chrome DevTools
 -> Network
 -> Submit button
 -> Payload
```

You may see:

```json
{
 "educationLevel": "MASTER",
 "documents": [
   {
     "type": "TRANSCRIPT",
     "fileId": "xxxx"
   }
 ]
}
```

This tells you the real data model.

---

For a form like Hong Kong QMAS, I would do:

```
1. Open page
2. DevTools → Sources
3. Search:
      required
      upload
      file
      pdf
      jpg
      size
      validation
      error
4. Network tab
5. Submit a test draft
6. Copy JS/API payload to AI
7. Ask AI:
      "Extract all validation rules and required documents"
```

The important caveat:

Frontend rules are **not always the final truth**. The backend can have additional checks.

Think of it like:

```
Frontend = client-side hints + user experience
Backend  = actual authority
```

So the strongest method is:

```
Page text
   +
HTML
   +
JavaScript
   +
Network API
   +
AI analysis
```

This is basically reverse-engineering the form's schema. For complex immigration, banking, tax, or enterprise forms, this approach is much faster than reading instructions manually.
