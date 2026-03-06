---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular tsconfig.json Guide Essentials
translated: false
type: note
---

**Question:** How does `tsconfig.json` work in an Angular project?

**Answer:**

## Overview

The `tsconfig.json` file in an Angular project plays a crucial role in the TypeScript compilation process. It is a configuration file that provides instructions to the TypeScript compiler on how to compile TypeScript code into JavaScript.

The presence of a `tsconfig.json` file in a directory indicates that the directory is the root of a TypeScript project. It specifies the root files and the compiler options required to compile the project.

---

## Multiple tsconfig Files in Angular

When you generate a new Angular project with the CLI, you typically get **three tsconfig files**:

| File | Purpose |
|---|---|
| `tsconfig.json` | Root/base config for the entire project |
| `tsconfig.app.json` | Config used when building the application |
| `tsconfig.spec.json` | Config used when running unit tests |

A `tsconfig.json` file can inherit configurations from another file using the `extends` property. The `extends` is a top-level property (alongside `compilerOptions`, `files`, `include`, and `exclude`). Its value is a string containing a path to another configuration file to inherit from. The configuration from the base file is loaded first, then overridden by those in the inheriting config file.

For example, `tsconfig.app.json` typically looks like:
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": "./out-tsc/app",
    "types": []
  },
  "files": ["src/main.ts"],
  "include": ["src/**/*.ts"],
  "exclude": ["src/test.ts", "src/**/*.spec.ts"]
}
```

---

## Top-Level Structure of tsconfig.json

It allows developers to specify compiler options, include/exclude files, and define the project's structure. The main sections are:

```json
{
  "compilerOptions": { },
  "include": [ ],
  "exclude": [ ],
  "angularCompilerOptions": { }
}
```

---

## Section 1: `compilerOptions`

The `compilerOptions` property is an object that specifies the TypeScript compiler options. This property is required in every `tsconfig.json` file and provides the compiler with important information about the code that needs to be compiled.

Key options explained:

| Option | Description |
|---|---|
| `target` | The JavaScript version to compile to (e.g., `es2020`) |
| `module` | Module format; Angular benefits from `esnext` for tree-shaking |
| `moduleResolution` | How modules are resolved; use `node` to match Node.js behavior |
| `lib` | Built-in APIs available (e.g., `es2020`, `dom`) |
| `strict` | Enables all strict type-checking options |
| `noImplicitAny` | Disallows variables with implicit `any` type |
| `sourceMap` | Generates source map files for debugging |
| `skipLibCheck` | Skips type-checking of `.d.ts` declaration files, speeding up builds |
| `esModuleInterop` | Allows default imports from CommonJS modules |
| `resolveJsonModule` | Allows importing `.json` files in TypeScript |
| `baseUrl` | Sets the base directory for resolving non-relative module names |
| `paths` | Maps custom import aliases to actual folder paths |

---

## Section 2: `include` and `exclude`

The `include` property is an array of file globs that should be included in the compilation process. By default, the compiler will include all files in the project that are not excluded by the `exclude` property.

The `exclude` option only changes which files are included as a result of the `include` setting. A file specified in `exclude` can still become part of your codebase due to an import statement in your code. It is not a mechanism that prevents a file from being included — it simply changes what the `include` setting finds.

Example:
```json
"include": ["src/**/*.ts"],
"exclude": ["node_modules", "dist", "e2e"]
```

---

## Section 3: `angularCompilerOptions`

This section is **Angular-specific** and controls the Angular template compiler (Ivy). Important options include:

| Option | Description |
|---|---|
| `strictInjectionParameters` | Enforces proper injection parameter types |
| `strictInputAccessModifiers` | Validates input binding access modifiers |
| `fullTemplateTypeCheck` | Enables type checking inside HTML templates (deprecated in Angular 13+) |
| `strictTemplates` | Modern replacement for `fullTemplateTypeCheck` |

---

## Section 4: Path Aliases (Bonus Best Practice)

Path mapping is incredibly useful for simplifying imports and avoiding long relative paths. `baseUrl` sets the base directory for resolving non-relative module names, and `paths` maps custom paths to specific folders, making imports cleaner.

```json
"compilerOptions": {
  "baseUrl": "./",
  "paths": {
    "@app/*": ["src/app/*"],
    "@assets/*": ["src/assets/*"]
  }
}
```

This lets you use `import { MyService } from '@app/services/my.service'` instead of `../../services/my.service`.

---

## Section 5: Error Handling Options

`noEmitOnError` prevents the compiler from emitting output if there are any errors. This ensures that only clean, error-free builds are generated — useful in CI/CD pipelines.

---

## Full Example of an Optimized Angular tsconfig.json

```json
{
  "compileOnSave": false,
  "compilerOptions": {
    "target": "es2020",
    "module": "esnext",
    "moduleResolution": "node",
    "lib": ["es2020"],
    "skipLibCheck": true,
    "strict": true,
    "noImplicitAny": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "sourceMap": true,
    "noEmitOnError": true,
    "baseUrl": "./",
    "paths": {
      "@app/*": ["src/app/*"],
      "@assets/*": ["src/assets/*"]
    }
  },
  "angularCompilerOptions": {
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist", "e2e"]
}
```

---

**References:**

- [Almost Perfect tsconfig.json Options for Angular Projects – Medium](https://medium.com/@sehban.alam/almost-perfect-tsconfig-json-options-for-your-angular-projects-5bec056f23d8)
- [Angular Compiler Options – angular.dev](https://angular.dev/reference/configs/angular-compiler-options)
- [What is a tsconfig.json – TypeScript Official Docs](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html)
- [TSConfig Reference – TypeScript](https://www.typescriptlang.org/tsconfig/)
- [Angular tsconfig.json file decoded – LinkedIn](https://www.linkedin.com/pulse/angular-tsconfigjson-file-decoded-guru-samrudh)