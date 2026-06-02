---
audio: false
generated: true
lang: en
layout: post
title: Fixing LaTeX Apostrophe Rendering
translated: false
type: note
---

The issue you're experiencing with the apostrophe in "HSBC's" is likely related to how LaTeX handles certain quote/apostrophe characters in PDF output. Here are several ways to improve the rendering:

## 1. Use the correct LaTeX apostrophe
Replace the straight apostrophe (') with the proper LaTeX apostrophe:
```latex
\item {Backend Engineer outsourced to HSBC Bank under TEKsystems, developing and optimizing backend systems for the \href{https://www.google.com/search?q=Finance+Timezone+Platform+HSBC}{Finance Transformation Platform} in HSBC's Enterprise Technology Department.}
```
Change to:
```latex
\item {Backend Engineer outsourced to HSBC Bank under TEKsizer, developing and optimizing backend systems for the \href{https://www.google.com/search?q=Finance+Transformation+Platform+HSBC}{Finance Transformation Platform} in HSBC's Enterprise Technology Department.}
```

## 2. Use `\textquotesingle` command
```latex
HSBC\textquotesingle{}s
```

## 3. Use the `\textasciigrave` and `\textquotesingle` approach
```latex
HSBC\textquotesingle{}s
```

## 4. Add the `textcomp` package
Add this to your preamble:
```latex
\usepackage{textcomp}
```
Then use:
```latex
HSBC\textquotesingle{}s
```

## 5. Use UTF-8 encoding (if not already)
Make sure your document uses UTF-8 encoding:
```latex
\usepackage[utf8]{inputenc}
```

## 6. Try the `babel` package for better typography
```latex
\usepackage[british]{babel}
```

## Most reliable solution:
For the best results, I recommend using the backtick-apostrophe combination, which is the traditional LaTeX way for proper typography:

```latex
\item {Backend Engineer outsourced to HSBC Bank under TEKsystems, developing and optimizing backend systems for the \href{https://www.google.com/search?q=Finance+Transformation+Platform+HSBC}{Finance Transformation Platform} in HSBC`s Enterprise Technology Department.}
```

This will render with proper typographical spacing and curvature in the PDF output. The backtick (`) followed by the apostrophe (') creates the correct appearance for possessive forms in LaTeX.
