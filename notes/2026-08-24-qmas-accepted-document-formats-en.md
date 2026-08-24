---
audio: false
generated: true
image: false
lang: en
layout: post
title: QMAS Accepted Document Formats
translated: false
type: note
---

Question: What file formats does the Hong Kong QMAS online application system accept for uploaded documents?

Answer:

The QMAS online application system accepts these formats: ([Immigration Department Web App][1])

| Format     | Recommended usage                                                       |
| ---------- | ----------------------------------------------------------------------- |
| PDF        | ✅ Best choice for certificates, contracts, bank statements, transcripts |
| JPEG / JPG | Good for passport pages, ID cards, photos                               |
| PNG        | Accepted, useful for screenshots/scanned images                         |
| GIF        | Accepted but not recommended                                            |
| TIF / TIFF | Accepted, mainly professional scanning                                  |

Limits: ([Immigration Department Web App][1])

* Maximum size: **5 MB per file**
* Documents without photos: grayscale is acceptable
* Documents with photos: use colour scan

---

My recommendation for QMAS:

## Use PDF for almost everything

Example:

```
01 Passport.pdf
02 ID Card.pdf

03 Net Worth/
   bank_statement.pdf
   property_certificate.pdf

04 Education/
   degree_certificate.pdf
   transcript.pdf

05 Work Experience/
   LeanCloud_employment.pdf
   HSBC_employment.pdf
   Meitai_employment.pdf

06 Income/
   tax_record.pdf
   salary_slips.pdf

07 IELTS.pdf

08 Achievement/
   github_projects.pdf
   blog_statistics.pdf
```

---

## Scanning settings

Recommended:

```
Resolution:
300 dpi

Color:
Color for certificates/photos

Format:
PDF

Compression:
Medium
```

A 10-page PDF should normally be under 5 MB.

---

## For your passport

Better:

```
passport.pdf
```

Include:

* Personal information page
* Visa pages
* HK entry stamps (if any)

Do not upload separate PNG pages unless necessary.

---

## For your photo

Use:

```
photo.jpg
```

because it is an image requirement. The system accepts JPEG/PNG, but JPEG is usually safest. ([Government of Hong Kong][2])

---

## File count matters

QMAS has maximum upload counts for each category. For example: ([Government of Hong Kong][2])

* Passport: up to 5 files
* Net worth: up to 3 files
* Education: up to 10 files
* Work experience: up to 10 files
* Achievement: up to 10 files

So instead of uploading 50 small images:

Bad:

```
salary1.png
salary2.png
salary3.png
salary4.png
...
```

Better:

```
salary_records_2023_2026.pdf
```

Combine related pages into one PDF.

---

For your case (AI engineer + possible QMAS):

I would prepare a **professional PDF package**:

```
QMAS_Application/
├── Identity.pdf
├── Education.pdf
├── Career_History.pdf
├── AI_Achievements.pdf
├── Financial_Status.pdf
├── Income.pdf
├── IELTS.pdf
└── Family_Documents.pdf
```

This makes the immigration officer's review easier.

[1]: https://webapp.es2.immd.gov.hk/applies2-client/static/faq/pnv-qmas/en-US/entry_faq.html?utm_source=chatgpt.com "ESERVICES2"
[2]: https://www.gov.hk/en/nonresidents/visarequire/visasentrypermits/applyqmas.htm?pla=null&utm_source=chatgpt.com "GovHK: Online Application for Entry to Hong Kong under the Quality Migrant Admission Scheme"
