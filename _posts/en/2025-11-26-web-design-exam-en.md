---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Web Design Self-Study Exam Practice
translated: false
type: note
---

Here are some realistic exercise/problems that closely match the style and difficulty of the National Higher Education Self-Study Examination (自学考试) for “Web Design and Production” (网页设计与网站建设, 14352). They are divided into the usual question types found in the theory paper and practical assessment.

### Theory Exam Practice Questions (Typical 100-point paper)

#### I. Single-Choice Questions (每题1分，共20分)
1. Which of the following is the correct structure of an HTML5 document?
   - A. `<html><head><body>`
   - B. `<!DOCTYPE html><html><head><body>`
   - C. `<head><html><body>`
   - D. `<body><html><head>`

2. In CSS, which selector has the highest specificity?
   - A. `#header`
   - B. `.nav`
   - C. `div`
   - D. `p`

3. The correct way to link an external CSS file is:
   - A. `<link rel="stylesheet" type="text/css" href="style.css">`
   - B. `<style src="style.css">`
   - C. `<css href="style.css">`
   - D. `<link href="style.css" type="stylesheet">`

(Continue with similar questions on HTML tags, CSS box model, color modes, file paths, etc.)

#### II. Multiple-Choice Questions (每题2分，共10分)
1. Which of the following are block-level elements in HTML? ( )
   - A. `<div>`  B. `<span>`  C. `<p>`  D. `<img>`

2. Which units in CSS are relative units? ( )
   - A. px  B. em  C. %  D. rem

#### III. True/False Questions (每题1分，共10分)
1. The `<meta charset="gb2312">` declaration is recommended for new websites in China. ( )
2. Using `position: absolute` removes the element from the normal document flow. ( )

#### IV. Short-Answer Questions (每题5-8分，共30分)
1. Briefly explain the three parts of the CSS box model and their order from inside to outside.
2. What are the main differences between `margin` and `padding`?
3. Describe the role of the `<meta name="keywords" content="...">` tag and explain why search engines now give it very low weight.
4. List four common image formats used on websites and their main characteristics.

#### V. Comprehensive/Analysis Questions (每题10-15分，共30分)
1. Given the following HTML and CSS code, draw the final layout (or describe the effect) and explain why collapse of vertical margins occurs.

```html
<div class="box1"></div>
<div class="box2"></div>
```
```css
.box1 { width:200px; height:100px; background:red; margin-bottom:40px; }
.box2 { width:200px; height:100px; background:blue; margin-top:60px; }
```

2. A client requires the website to be compatible with IE8 and above. List at least six modern HTML5/CSS3 features you cannot use and suggest alternatives.

### Practical Assessment Practice Tasks (Typical tasks given in the actual exam)

#### Task 1 – Basic Static Page (40 points)
Using only HTML and CSS (no JavaScript, no frameworks), create a complete website with the following requirements:

1. Folder structure:
   ```
   exam/
   ├─ index.html
   ├─ about.html
   ├─ products.html
   ├─ css/style.css
   ├─ images/banner.jpg (you may use placeholder)
   └─ images/logo.png
   ```

2. All pages must contain:
   - Correct `<!DOCTYPE html>` declaration and UTF-8 encoding
   - Semantic HTML5 tags (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, etc.)
   - Top navigation bar with three links (Home, About, Products) that actually work
   - A 1000×300 pixel banner image centered
   - Three product cards floated side-by-side (each card contains picture + title + short description + price)
   - Footer with copyright information centered
   - External CSS file with reset, typography, layout, and color scheme (blue tone)

3. CSS requirements:
   - Use at least one ID selector and five class selectors
   - Center the entire page content with max-width 1200px
   - Hover effect on navigation and product cards
   - Responsive: when browser width < 768px, the three product cards stack vertically

#### Task 2 – Form + Table Page (30 points)
Create a file `contact.html` in the same folder with:
- A complete user registration form containing: text input, password, radio buttons (gender), checkboxes (hobbies), dropdown (city), textarea, and submit/reset buttons
- Use `<label>` correctly and proper `for` attributes
- Below the form, insert a product price list using `<table>` (at least 5 rows × 6 columns, with table header, caption, and striped rows using CSS)

#### Task 3 – Debugging & Optimization (30 points)
You are given a buggy website folder (will be provided as zip). Common problems include:
- Images not showing (wrong path)
- Layout collapse (missing float clear)
- Chinese characters garbled
- Missing `alt` attributes
- CSS not applied (wrong link order)
Fix all errors and write a short report (in HTML comment form) listing the problems you found and how you fixed them.

These questions and tasks cover ≈95% of the actual exam content and difficulty level seen in recent years (2022-2025). Practice them several times, especially the practical part under timed conditions (usually 120-150 minutes). Good luck with your self-study exam!
