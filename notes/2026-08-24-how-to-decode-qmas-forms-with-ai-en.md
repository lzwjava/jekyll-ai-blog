---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Decode QMAS Forms with AI
translated: false
type: note
---

Question: Can I inspect the QMAS online form by copying frontend code / using browser console and give it to AI to understand the criteria?

Answer: Yes, this is actually a very practical way to understand complex government forms, especially modern web apps. The idea is:

1. **Inspect the frontend**

   * Open Chrome DevTools:

     * `F12` → Network / Sources / Application
     * Look for:

       * JSON schemas
       * API responses
       * JavaScript bundles
       * field names
       * validation rules
       * hidden options

2. **Extract form structure**

   For example:

```javascript
// in browser console
document.querySelectorAll("input, select, textarea")
```

or:

```javascript
copy(document.documentElement.innerHTML)
```

Then give the extracted HTML/JS to AI and ask:

> "Analyze this immigration form. Extract every field, required documents, validation rules, and explain what evidence should be uploaded."

AI can often reconstruct:

* field meaning
* mandatory vs optional
* expected format
* dependencies between fields
* scoring criteria

For QMAS this is especially useful because the application is not just a normal form; it maps to the assessment criteria:

* age
* academic qualifications
* language ability
* work experience
* income
* business ownership
* achievements

The Immigration Department says the online application information must match the documentary proof submitted, and the General Points Test information should correspond to your stated age, academic qualifications, language proficiency, work experience, annual income and business ownership. ([Immigration Department Hong Kong][1])

The official upload categories already reveal the evaluation structure:

* travel document
* photo
* proof of net worth
* academic/professional qualifications
* work experience
* company proof
* income record
* language proof
* achievements
* dependant documents

([Government of Hong Kong][2])

A good workflow:

```text
Browser
  |
  |-- inspect HTML/JS/API
  |
  v
Extract fields
  |
  v
AI analysis
  |
  +--> "What does this field mean?"
  +--> "What document proves this?"
  +--> "How strong is my evidence?"
  +--> "What points can I claim?"
```

For example:

```
Field:
"Professional qualifications"

AI:
- likely wants certificates/licenses
- not the same as academic degree
- upload PDF scans
- include issuing authority
- include translation if not English/Chinese
```

For your case, this can be very useful because your profile is unusual:

* strong software engineering experience
* AI/LLM work
* startup/business experience
* non-traditional education background

You can use AI to map:

```
Your evidence
      |
      v
QMAS criterion
      |
      v
Possible points / risk
```

One caution: don't rely only on frontend code. Government systems often hide the real rules server-side. The official guidance notes and document checklist remain the source of truth. ([Immigration Department Hong Kong][1])

A stronger approach is:

1. Download official QMAS guidance PDF.
2. Inspect online form.
3. Build a personal "QMAS evidence matrix":

```
Criterion              Evidence                  Strength
--------------------------------------------------------
Work experience        employment letters        strong
AI achievement         papers/projects           medium
Degree                 self-study diploma        risk
Income                 tax records               depends
Business ownership     company records           strong if available
```

Then you know exactly where your application is weak before submitting.

[1]: https://www.immd.gov.hk/pdforms/id%28e%29982.pdf?utm_source=chatgpt.com "Quality Migrant Admission Scheme Guidance Notes - English version"
[2]: https://www.gov.hk/en/nonresidents/visarequire/visasentrypermits/applyqmas.htm?pla=null&utm_source=chatgpt.com "GovHK: Online Application for Entry to Hong Kong under the Quality Migrant Admission Scheme"
