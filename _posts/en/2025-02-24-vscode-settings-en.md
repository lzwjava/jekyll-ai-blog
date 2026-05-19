---
audio: false
generated: true
lang: en
layout: post
title: VSCode Settings
translated: false
type: note
---

This JSON file contains various VS Code settings that customize the editor's behavior and appearance. Here's a brief overview of what each setting does:

*   `eslint.autoFixOnSave`: Automatically fixes ESLint issues when saving a file.
*   `java.errors.incompleteClasspath.severity`: Configures how VS Code handles incomplete Java classpath errors. In this case, it ignores them.
*   `files.associations`: Associates specific file extensions with languages for syntax highlighting and language support.
*   `emmet.syntaxProfiles`: Defines syntax profiles for Emmet abbreviations in specific file types.
*   `editor.suggestSelection`: Determines how suggestions are selected in the editor.
*   `vsintellicode.modify.editor.suggestSelection`: Modifies the editor's suggestion selection behavior using VS IntelliCode.
*   `git.ignoreMissingGitWarning`: Disables the warning for missing Git repositories.
*   `python.jediEnabled`: Disables Jedi as the completion engine for Python (Pylance is preferred).
*   `editor.codeActionsOnSave`: Specifies code actions to run on save, such as ESLint fixes.
*   `python.languageServer`: Sets the Python language server to Pylance.
*   `editor.renderWhitespace`: Controls how whitespace is rendered in the editor.
*   `workbench.editorAssociations`: Associates file patterns with specific editors.
*   `debug.console.fontSize`: Sets the font size for the debug console.
*   `terminal.integrated.fontSize`: Sets the font size for the integrated terminal.
*   `terminal.integrated.shell.osx`: Specifies the shell to use on macOS.
*   `explorer.confirmDelete`: Disables confirmation dialogs when deleting files in the Explorer.
*   `ruby.codeCompletion`: Sets the code completion engine for Ruby.
*   `ruby.intellisense`: Configures Ruby IntelliSense.
*   `C_Cpp.updateChannel`: Sets the update channel for the C/C++ extension.
*   `editor.formatOnType`: Enables formatting as you type.
*   `[Log]`: Specific editor settings for files identified as "Log".
*   `files.exclude`: Excludes specified files and folders from the Explorer.
*   `redhat.telemetry.enabled`: Enables or disables Red Hat telemetry.
*   `java.configuration.runtimes`: Configures Java runtime environments.
*   `java.debug.settings.vmArgs`: Sets VM arguments for Java debugging.
*   `mssql.connections`: Stores connection information for MSSQL databases.



{% raw %}
```json
{
      "eslint.autoFixOnSave": true,
      "java.errors.incompleteClasspath.severity": "ignore",
      "files.associations": {
            "*.vue": "vue",
            "*.wpy": "vue",
            "*.wxml": "html",
            "*.wxss": "css",
            "*.rb": "ruby"
      },
      "emmet.syntaxProfiles": {
            "vue-html": "html",
            "vue": "html"
      },
      "editor.suggestSelection": "first",
      "vsintellicode.modify.editor.suggestSelection": "automaticallyOverrodeDefaultValue",
      "git.ignoreMissingGitWarning": true,
      "python.jediEnabled": false,
      "editor.codeActionsOnSave": {
            "source.fixAll.eslint": "explicit"
      },
      "python.languageServer": "Pylance",
      "editor.renderWhitespace": "none",
      "workbench.editorAssociations": {
            "*.ipynb": "jupyter-notebook"
      },
      "debug.console.fontSize": 13,
      "terminal.integrated.fontSize": 14,
      "terminal.integrated.shell.osx": "/bin/zsh",
      "explorer.confirmDelete": false,
      "ruby.codeCompletion": "rcodetools",
      "ruby.intellisense": "rubyLocate",
      "C_Cpp.updateChannel": "Insiders",
      "editor.formatOnType": true,
      "[Log]": {
            "editor.wordWrap": "off"
      },
      "files.exclude": {
            "**/.classpath": true,
            "**/.project": true,
            "**/.settings": true,
            "**/.factorypath": true
      },
      "redhat.telemetry.enabled": true,
      "java.configuration.runtimes": [],
      "java.debug.settings.vmArgs": "-ea",
      "mssql.connections": [
            {
                  "server": "{{put-server-name-here}}",
                  "database": "{{put-database-name-here}}",
                  "user": "{{put-username-here}}",
                  "password": "{{put-password-here}}"
            }
      ],
      "notebook.cellToolbarLocation": {
            "default": "right",
            "jupyter-notebook": "left"
      },
      "java.home": "",
      "java.saveActions.organizeImports": true,
      "java.jdt.ls.vmargs": "-XX:+UseParallelGC -XX:GCTimeRatio=4 -XX:AdaptiveSizePolicyWeight=90 -Dsun.zip.disableMemoryMapping=true -Xmx1G -Xms100m -javaagent:\"/Users/lzw/.vscode/extensions/gabrielbb.vscode-lombok-1.0.1/server/lombok.jar\"",
      "editor.accessibilitySupport": "off",
      "security.workspace.trust.untrustedFiles": "newWindow",
      "explorer.confirmDragAndDrop": false,
      "workbench.colorTheme": "One Monokai",
      "C_Cpp.clang_format_fallbackStyle": "WebKit",
      "editor.unicodeHighlight.nonBasicASCII": false,
      "files.autoSave": "afterDelay",
      "grammarly.files.include": [
            "**/*.md"
      ],
      "editor.inlineSuggest.enabled": true,
      "github.copilot.enable": {
            "*": true,
            "yaml": true,
            "plaintext": false,
            "markdown": false
      },
      "yaml.customTags": [
            "!And",
            "!And sequence",
            "!If",
            "!If sequence",
            "!Not",
            "!Not sequence",
            "!Equals",
            "!Equals sequence",
            "!Or",
            "!Or sequence",
            "!FindInMap",
            "!FindInMap sequence",
            "!Base64",
            "!Join",
            "!Join sequence",
            "!Cidr",
            "!Ref",
            "!Sub",
            "!Sub sequence",
            "!GetAtt",
            "!GetAZs",
            "!ImportValue",
            "!ImportValue sequence",
            "!Select",
            "!Select sequence",
            "!Split",
            "!Split sequence"
      ],
      "editor.wordWrap": "on",
      "[python]": {
            "editor.defaultFormatter": "ms-python.autopep8"
      },
      "python.formatting.provider": "none",
      "git.openRepositoryInParentFolders": "never",
      "window.zoomLevel": 1,
      "editor.fontSize": 13,
      "debug.onTaskErrors": "abort",
      "C_Cpp.errorSquiggles": "disabled",
      "cmake.showOptionsMovedNotification": false,
      "editor.formatOnSave": true,
      "autopep8.args": [
            "\"autopep8.args\" = [\"--max-line-length\", \"120\"]"
      ],
      "dart.flutterSdkPath": "/Users/lzwjava/bin/flutter",
      "tabnine.experimentalAutoImports": true,
}
```
{% endraw %}