---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Angular CLI Configuration Blueprint Guide
translated: false
type: note
---

**angular.json** is the main configuration file for Angular CLI projects. It defines how your project is structured and how the CLI should build, serve, and test your application.

**Key things it contains:**

**Project configuration** - If you have multiple apps or libraries in one workspace, each is defined here with its own settings.

**Build options** - Where your source files are, where to output built files, which assets to copy, style files to include, polyfills, etc.

**Architect targets** - Configurations for different CLI commands like:
- `build` - how to compile your app
- `serve` - dev server settings (port, proxy config, etc.)
- `test` - testing configuration
- `lint` - linting rules

**Different environments** - You can define configurations for development, production, staging, etc. with different settings (like whether to enable source maps, optimization level, base URLs).

**Example structure:**
```json
{
  "projects": {
    "my-app": {
      "architect": {
        "build": {
          "options": {
            "outputPath": "dist/my-app",
            "index": "src/index.html",
            "main": "src/main.ts",
            "styles": ["src/styles.css"]
          },
          "configurations": {
            "production": {
              "optimization": true,
              "sourceMap": false
            }
          }
        }
      }
    }
  }
}
```

When you run commands like `ng build --configuration=production`, the CLI reads angular.json to know exactly how to execute that build. It's basically the blueprint the CLI follows for all project operations.
