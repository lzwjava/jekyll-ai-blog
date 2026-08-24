---
audio: false
generated: true
image: false
lang: en
layout: post
title: QMAS Application Form Guide
translated: false
type: note
---

I've analyzed the HTML for the Hong Kong Quality Migrant Admission Scheme (QMAS) online application. Here's a structured analysis of what to notice, the rules, and what to be careful about when filling this form.

---

## Overview: 11-Step Multi-Tab Structure

The form is a horizontal 11-step stepper. Note the navigation flow:

| # | Step | Data captured |
| --- | --- | --- |
| ① | **Assessment Routes** | Choose GPT vs APT point system |
| ② | **Prerequisites** | DOB, financial capacity, "good character" questions, dependants, net worth |
| ③ | **General Points Test** | Age etc., scoring 0/12 |
| ④–⑨ | Academic/Professional, Work Experience, Income, Language Skills, Accomplishments/Future Plans, Sector | Dynamic sub-pages |
| ⑩ | **Personal and Family Members' Particulars** | Manual fill OR auto-fill via travel doc upload / iAM Smart |
| ⑪ | **Confirm and Submit** | Review, declaration, signature |

---

## ⚠️ Critical Rules & Things to Be Careful About

### 1. Passing Threshold (Step ③)

- **Passing threshold = 6 out of 12** assessment criteria.
- The System computes a real-time count at the bottom: *"Number of assessment criteria you met: 0 / 12"*.
- Applicants who don't meet threshold **cannot submit** (the "Next step" / `continueBtn` stays **disabled**).

### 2. Two Assessment Routes (Step ①) — choose carefully

| Route | Notices |
| --- | --- |
| **General Points Test (GPT)** | Default selected. 12 criteria across 6 aspects: Age, Academic Qualifications, Language Proficiency, Work Experience, Annual Income, Business Ownership. |
| **Achievement-based Points Test (APT)** | Very high bar — only for applicants with an exceptional award (e.g. **Olympic medal, Nobel Prize, national/international award**) OR work acknowledged by peers / contribution to field. **If you fail any criterion → application refused immediately.** |

> ⚠️ **Be careful:** The APT questions are `hidden` in the HTML (only shown if APT is selected). Choose GPT unless you genuinely hold major awards.

### 3. Prerequisites (Step ②) — Eligibility Gate

These are threshold/filter questions. **Answering "No" here effectively disqualifies you:**

- **Q1 DOB** — auto-calculates and locks your **age** (relevant to scoring). Date format **DD/MM/YYYY**.
- **Q2** — *"Are you capable of supporting and accommodating yourself ... without relying on public assistance?"* → **must answer YES**
- **Q3** — *"minimum of graduate level education or a good technical qualification?"* → **must answer YES** to proceed
- (Page 2) — **all these MUST be "No":**
  - **Q4** convicted of any crime in HK or elsewhere
  - **Q5** refused entry / deported / required to leave HK or elsewhere
  - **Q6** refused a visa / entry permit for HK or elsewhere
  - **Q7** breached any long-term immigration law in HK or elsewhere
  - **Q8** applied for visa under a *different identity/name* than current travel doc

> ⚠️ If you answer YES to Q4–Q8, detail fields + supporting-document uploads appear (and it will likely block forward progress). Only choose YES if truly applicable — be truthful; making a false statement is a criminal offence (see declaration).

### 4. "Sensitive" fields with hidden / auto-locked logic

- **Date of Birth is locked from Step ① → Step ⑩ read-only:** the form warns *"Please return to '2. Prerequisites' if you wish to amend your Date of Birth."* So set it correctly in Step ②.
- The system pre-fills some data when you **upload a travel document or use iAM Smart e-ME** (Name, DOB, given name, photo tags `iams-img-tag` appear). This reduces manual typing and errors.

### 5. File upload constraints (strict)

Each upload component has hard limits you must respect:

| Field | Rules |
| --- | --- |
| Proofs of personal net worth | **max 3 files**, ≤5MB each |
| Supporting docs for Q4–Q8 (if YES) | **max 2 files**, ≤5MB |
| Recent photograph | **only JPEG**, **MIN 1200px(W) × 1600px(H)**, **1 file**, ≤5MB |
| Travel / identity document | **max 5 files**, ≤5MB |
| Macao ID / Taiwan documents (conditional) | **max 2 files**, ≤5MB |
| Other supporting documents | **max 5 files**, ≤5MB |

> Note: File **size ≤ 5MB** and **count/type limits** are enforced. Oversized or non-JPEG will reject.

### 6. Mandatory personal fields with validation (Step ⑩)

Fields marked `required-star`:

- **Name in English** — format `Surname, [space] Given Names` (auto-uppercase via `all-caps`)
- **Sex** (Male/Female checkboxes — note *"For unknown sex , please select 'Male' and 'Female'"*)
- **Chinese name** (≤6 chars) — *if applicable*
- **Place of birth**, **Nationality / domicile**, **Others specifys** (if "OTHERS")
- **Travel/Identity doc type + number + place of issue + date of issue/expiry**
- **Present country/territory of domicile** + permanent residence (Y/N radio)
- **Marital / Relationship status** (Bachelor, Married, Separated, Divorced, Widowed, Others)
- **E-mail + Re-enter e-mail** (paste disabled — `onpaste="return false;"`, must be typed twice, must match)
- **Contact telephone** (country code + number), **Present address** (opens popup modal)

### 7. Negative-address & equality / personal net worth

- **Address** is entered via a modal (`adi-address`) with **Chinese/English** and **HK / Other Address** types — not free text at first. Use "Input address" button; full address in textarea is otherwise disabled.
- **HK ID no.** — two fields: main value (≤8 chars) + bracket check digit (1 char).
- **Nationality dropdown** — has disabled headers ("Resident of:", "National of:"). Choose the leaf option value correctly (e.g. `TWP` Mainland, `CHN` Mainland-overseas, `TWN` Taiwan, or country codes like `USA`).

### 8. Declaration & Signature (Step ⑪)

Before submission you must:

- Read consent clauses (i–iv, incl. IRD/MPF verification consent, "Director has absolute discretionary absolute discretion")
- Confirm **personal net worth ≥ amount stated in Part 2**
- (Mainland Chinese residents) declare you'll apply for **EEP** for entry
- Signature via **"Sign to Continue"** button (typed/signature widget) — signatures are required per the panel, plus a **Date** field.

> ⚠️ **Warning box (Step ①):** Making a **false statement** under the Scheme is an offence under HK law → prosecut + removal + nullification of visa for self/family. Answer truthfully.

---

## 🧠 Practical "Careful" Checklist

1. **Double-check DOB** in Step ② — it's locked afterward.
2. **Answer the threshold questions deliberately** — wrong "No" will kill the application.
3. **Don't exceed upload limits** (count + 5MB) — especially the photo (JPEG, ≥1200×1600, it's 1 file only).
4. **Email must be typed twice and identical** — no notes, no paste.
5. **Wait for the /12 score** in Step ③ to reach 6+ before proceeding.
6. **Verify locked/modal fields** (address modal, HK ID brackets, nationality dropdown headers) — these are easy to mis-enter.
7. **Never falsify** crime / entry / immigration / identity answers.
8. **Choose route deliberately (GPT vs APT)** — APT failure = immediate refusal.
9. **For dependants** — spouse/partner + unmarried children <18, each completing their own Part (child <16 signed by parent/guardian). "Number of accompanying dependants: 0" adjustable via "Change number" button.
10. **Save and Exit** is available; but note entry requires applicant full name, DOB, email **twice** to verify identity when restoring.

---

If you'd like, I can help you:

- **Draft suggested answers** for each field (if you give me your background),
- **Build a checklist/script** to auto-fill the fields via the form's element IDs (there are `id` attributes I can target), e.g. `dobDate`, `personalNetWorth`, `minimumEducationLevelYes`, `assessmentQ01Yes`, `givenName`, `pob`, `email`, etc.

Let me know which direction you want to go — and whether this is a **personal application** or a **headless/automation** task.
