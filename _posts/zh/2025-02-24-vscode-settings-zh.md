---
audio: false
generated: true
lang: zh
layout: post
title: VSCode 设置
translated: true
type: note
---

该JSON文件包含各种VS Code设置，用于自定义编辑器的行为和外观。以下是各设置的简要说明：

* `eslint.autoFixOnSave`：保存文件时自动修复ESLint问题
* `java.errors.incompleteClasspath.severity`：配置VS Code处理Java类路径不完整错误的方式，此处设置为忽略
* `files.associations`：为特定文件扩展名关联语言以支持语法高亮
* `emmet.syntaxProfiles`：为特定文件类型定义Emmet缩写语法配置
* `editor.suggestSelection`：决定编辑器中的建议项选择方式
* `vsintellicode.modify.editor.suggestSelection`：使用VS IntelliCode修改编辑器建议选择行为
* `git.ignoreMissingGitWarning`：禁用缺失Git仓库的警告提示
* `python.jediEnabled`：禁用Jedi作为Python补全引擎（推荐使用Pylance）
* `editor.codeActionsOnSave`：指定保存时执行的代码操作，如ESLint修复
* `python.languageServer`：设置Python语言服务器为Pylance
* `editor.renderWhitespace`：控制编辑器中的空白字符渲染方式
* `workbench.editorAssociations`：将文件模式与特定编辑器关联
* `debug.console.fontSize`：设置调试控制台的字体大小
* `terminal.integrated.fontSize`：设置集成终端的字体大小
* `terminal.integrated.shell.osx`：指定macOS系统使用的shell程序
* `explorer.confirmDelete`：禁用文件管理器删除文件时的确认对话框
* `ruby.codeCompletion`：设置Ruby代码补全引擎
* `ruby.intellisense`：配置Ruby智能感知功能
* `C_Cpp.updateChannel`：设置C/C++扩展的更新通道
* `editor.formatOnType`：启用输入时自动格式化
* `[Log]`：针对"Log"类型文件的特定编辑器设置
* `files.exclude`：从文件管理器中排除指定文件和文件夹
* `redhat.telemetry.enabled`：启用或禁用Red Hat遥测功能
* `java.configuration.runtimes`：配置Java运行时环境
* `java.debug.settings.vmArgs`：设置Java调试的虚拟机参数
* `mssql.connections`：存储MSSQL数据库连接信息

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
            "**/.factorypath": true"
      },
      "redhat.telemetry.enabled": true,
      "java.configuration.runtimes": [],
      "java.debug.settings.vmArgs": "-ea",
      "mssql.connections": [
            {
                  "server": "{{输入服务器名称}}",
                  "database": "{{输入数据库名称}}",
                  "user": "{{输入用户名}}",
                  "password": "{{输入密码}}"
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