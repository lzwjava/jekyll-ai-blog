---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter DOCTYPE Declarations Reference
translated: false
type: note
---

### Overview

This is a PHP array from the CodeIgniter framework (an open-source web application framework), which defines DOCTYPE declarations for various markup languages. A DOCTYPE is a document type declaration that informs browsers and validators about the version and standard of the markup language used in an HTML document. It ensures proper rendering and validation. These declarations are based on official W3C standards. Below, I'll explain each one by grouping them thematically, including their purpose and typical use cases.

### XHTML Doctypes

XHTML (eXtensible HyperText Markup Language) is HTML reformulated as XML, enforcing stricter syntax (e.g., requiring closing tags and lowercase elements).

- **xhtml11**: Declares XHTML 1.1, the latest XHTML version with modular features for advanced web apps. Strict, XML-compliant; used for modern, semantic web pages without frames or legacy elements.
- **xhtml1-strict**: XHTML 1.0 Strict; enforces clean, semantic markup without deprecated elements (e.g., no `<font>`). Ideal for standards-compliant sites needing backwards compatibility.
- **xhtml1-trans**: XHTML 1.0 Transitional; allows some legacy HTML elements for easier migration from HTML 3.2/4.0. Useful for existing sites mixing old and new markup.
- **xhtml1-frame**: XHTML 1.0 Frameset; supports framed layouts with `<frameset>`. Obsolete in modern web design due to usability issues and SEO drawbacks.
- **xhtml-basic11**: XHTML Basic 1.1; a lightweight profile for mobile devices and simple applications, excluding advanced features like forms or stylesheets.

### HTML Doctypes

HTML is the standard markup for web pages, evolving from loose to strict standards.

- **html5**: The modern HTML5 DOCTYPE; simple and future-proof, parsed in standards mode by all browsers. Supports multimedia, APIs, and semantic elements (e.g., `<article>`, `<header>`). Recommended for new websites.
- **html4-strict**: HTML 4.01 Strict; enforces semantic rigor without deprecated elements. Used in legacy projects requiring strict compliance.
- **html4-trans**: HTML 4.01 Transitional; permissive, allowing legacy tags for gradual updates. Common in older sites transitioning to standards.
- **html4-frame**: HTML 4.01 Frameset; for framed pages, now deprecated due to slow loading and accessibility problems.

### MathML Doctypes

MathML (Mathematical Markup Language) enables displaying mathematical notations on the web.

- **mathml1**: MathML 1.0; basic math rendering in XML format. Used in educational tools or documents with simple equations.
- **mathml2**: MathML 2.0; enhanced support for complex math, better integrated with other markup. Foundation for modern math web display.

### SVG Doctypes

SVG (Scalable Vector Graphics) defines vector images in XML for web graphics.

- **svg10**: SVG 1.0; basic 2D vector graphics. Used for static illustrations.
- **svg11**: SVG 1.1; full 2D graphics with animations and filters. Standard for dynamic web graphics.
- **svg11-basic**: SVG 1.1 Basic; mobile-focused subset with fewer features. For lightweight SVG on devices.
- **svg11-tiny**: SVG 1.1 Tiny; minimal profile for low-power devices like phones. Supports basic shapes and animations.

### Compound Doctypes

These combine multiple standards for rich, multimedia content.

- **xhtml-math-svg-xh**: XHTML 1.1 with MathML 2.0 and SVG 1.1; for documents mixing text, math, and graphics (e.g., scientific papers).
- **xhtml-math-svg-sh**: Similar to above but rooted in SVG (`<svg:svg>`), for SVG-dominant documents with embedded XHTML and MathML.
- **xhtml-rdfa-1**: XHTML with RDFa 1.0 (Resource Description Framework in attributes); enhances semantic web data embedding for metadata-rich sites.
- **xhtml-rdfa-2**: XHTML with RDFa 1.1; improved RDFa for linking data in HTML attributes, used in web of data applications.

### Usage Notes

- These are predefined in CodeIgniter for easy insertion via its `doctype()` helper function.
- Modern web development favors HTML5 (`html5`) for its flexibility and browser support. Older doctypes (e.g., HTML 4 or framed versions) are largely obsolete.
- Evidenced by W3C specifications (e.g., w3.org/TR/html5/, w3.org/TR/xhtml11/), these ensure consistent parsing: browsers use them to trigger standards or quirks mode, affecting layout and scripts. Choose based on your project's markup needs for best validation (via tools like the W3C Validator). If you're working in CodeIgniter, use the array key in your views to output the declaration.
