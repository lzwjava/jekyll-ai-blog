---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JavaScript 快速 JSON Schema 验证器
translated: true
type: note
---

**问题：** ajv npm package 是什么？

**答案：**

**ajv** npm 包是一个高性能的 **JSON Schema validator**，用于 JavaScript。它代表 "Another JSON Validator"，并被广泛认为是 Node.js 和浏览器环境中可用的 **最快的 JSON Schema validator**。

### 主要特性
- 支持多个 JSON Schema drafts：draft-04（需要额外包）、draft-06、draft-07、draft/2019-09 和 draft/2020-12。
- 支持 **JSON Type Definition** (JTD — RFC 8927)。
- 将 JSON Schema 编译成高度优化的 JavaScript 验证函数（代码生成），这使得验证非常快速，并能获得良好的 V8 引擎优化。
- 在 JavaScript 生态系统中极受欢迎——每周下载量达 **数亿次**，并被许多主要库和框架使用（包括 Fastify、webpack 内部，以及无数 API）。
- 支持自定义 keywords、formats（通过 **ajv-formats**）、错误处理选项（allErrors、verbose 等）等。

### 基本用法示例

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

### 安装

```bash
npm install ajv
# For extra format validations (email, date, uri, etc.)
npm install ajv-formats
```

Ajv 是 JavaScript 项目中进行快速、符合标准的 JSON 验证的实际标准选择，特别是在 API、配置加载器，或任何需要根据声明式 schema 验证结构化数据的地方。

**参考资料：**

- [https://www.npmjs.com/package/ajv](https://www.npmjs.com/package/ajv)
- [https://ajv.js.org/](https://ajv.js.org/)
- [https://github.com/ajv-validator/ajv](https://github.com/ajv-validator/ajv)
