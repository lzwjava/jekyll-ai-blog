---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fast JSON Schema Validator for JavaScript
translated: false
type: note
---

**Question:** What is the ajv npm package?

**Answer:**

The **ajv** npm package is a high-performance **JSON Schema validator** for JavaScript. It stands for "Another JSON Validator" and is widely regarded as **the fastest JSON Schema validator** available for both Node.js and browser environments.

### Main features
- Supports multiple JSON Schema drafts: draft-04 (with additional package), draft-06, draft-07, draft/2019-09, and draft/2020-12.
- Supports **JSON Type Definition** (JTD — RFC 8927).
- Compiles JSON Schemas into highly optimized JavaScript validation functions (code generation), which enables very fast validation and good V8 engine optimization.
- Extremely popular in the JavaScript ecosystem — it has **hundreds of millions of weekly downloads** and is used by many major libraries and frameworks (including Fastify, webpack internally, and countless APIs).
- Allows custom keywords, formats (via **ajv-formats**), error handling options (allErrors, verbose, etc.), and more.

### Basic usage example

```javascript
const Ajv = require("ajv");
const ajv = new Ajv({ allErrors: true }); // options

const schema = {
  type: "object",
  properties: {
    name: { type: "string", minLength: 2 },
    age: { type: "integer", minimum: 0 }
  },
  required: ["name", "age"],
  additionalProperties: false
};

const validate = ajv.compile(schema);

const data = { name: "Alice", age: 28 };

if (validate(data)) {
  console.log("Valid!");
} else {
  console.log("Invalid:", validate.errors);
}
```

### Installation

```bash
npm install ajv
# For extra format validations (email, date, uri, etc.)
npm install ajv-formats
```

Ajv is the de-facto standard choice when you need fast, standards-compliant JSON validation in JavaScript projects, especially in APIs, configuration loaders, or any place where you want to validate structured data against a declarative schema.

**References:**

- [https://www.npmjs.com/package/ajv](https://www.npmjs.com/package/ajv)
- [https://ajv.js.org/](https://ajv.js.org/)
- [https://github.com/ajv-validator/ajv](https://github.com/ajv-validator/ajv)
