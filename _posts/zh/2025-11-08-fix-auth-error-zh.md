---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复翻译API认证错误
translated: true
type: note
---

### 工作流程与错误原因分析

您的 "Translate Recent Notes" GitHub Actions 工作流程整体结构良好——它能够检出代码库、设置Python环境、安装依赖、对最近N篇文章运行翻译脚本，并将更改提交到`_notes/`目录。但根据您之前分享的日志（在翻译成ar、de、fr等语言时出现401错误），问题出在`scripts/translation/update_lang_notes.py`内部的翻译API调用认证环节。

#### 根本原因

- 错误`"No cookie auth credentials found"`（HTTP 401）是**OpenRouter API**（或与之交互的Python客户端/库，如LiteLLM或非官方SDK）特有的错误。当API请求缺少正确的认证头信息时会出现此问题。
- OpenRouter要求在请求中包含`Authorization: Bearer <your_openrouter_api_key>`。如果API密钥未正确传递，某些客户端会回退到（或误认为需要）基于cookie的会话认证，从而触发此特定错误。
- 在您的工作流程中：
  - 您设置了`OPENROUTER_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}`，这将密钥值传递给了脚本的环境变量。
  - 但脚本可能没有正确读取/使用这个环境变量。常见的不匹配情况包括：
    - 脚本期望使用`OPENAI_API_KEY`（用于OpenRouter等OpenAI兼容端点）。
    - 或者脚本使用的库（如`openai` Python SDK）没有将基础URL设置为`https://openrouter.ai/api/v1`。
    - 密钥`DEEPSEEK_API_KEY`可能实际存储的是您的**OpenRouter API密钥**（路由到DeepSeek/Grok模型），但如果这是直接的DeepSeek密钥，则无法用于OpenRouter。
- 从日志看，脚本正在使用模型`'x-ai/grok-4-fast'`（通过OpenRouter的Grok 4），并且成功处理了front matter/标题，但在按语言翻译内容时失败。
- 这不是GitHub Actions的问题——问题出在Python脚本的API客户端设置上。工作流程继续执行到提交步骤（因此有`git config user.name "github-actions[bot]"`日志），但由于没有翻译内容，只有英文文件被添加。

#### 推荐修复方案

1. **更新工作流程中的环境变量**：
   - 与常见的OpenRouter设置（OpenAI兼容）对齐。将"Translate posts"步骤中的`env`块改为：
{% raw %}

     ```
     env:
       GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
       OPENAI_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}  # 将变量名改为脚本期望的名称
       OPENAI_BASE_URL: https://openrouter.ai/api/v1   # 路由到OpenRouter所必需
     ```

{% endraw %}

- 如果`DEEPSEEK_API_KEY`是您的OpenRouter密钥，很好。如果这是直接的DeepSeek密钥，请在仓库设置中创建一个新密钥`OPENROUTER_API_KEY`，填入您实际的OpenRouter密钥（在[openrouter.ai/keys](https://openrouter.ai/keys)获取）。
- 测试：在运行步骤中添加`echo $OPENAI_API_KEY`（已脱敏）用于日志调试。

2. **修复Python脚本（`update_lang_notes.py`）**：
   - 确保按以下方式初始化OpenAI客户端（假设使用`openai`库）：

     ```python
     import os
     from openai import OpenAI

     client = OpenAI(
         api_key=os.getenv("OPENAI_API_KEY"),
         base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # 如果未设置则默认使用OpenAI
     )

     # 然后使用 client.chat.completions.create(..., model="x-ai/grok-4-fast")
     ```

   - 如果使用LiteLLM（常用于多提供商）：如果`requirements.txt`中没有，请安装它，并调用`completion(model="openrouter/x-ai/grok-4-fast", api_key=os.getenv("OPENAI_API_KEY"), api_base="https://openrouter.ai/api/v1", ...)`。
   - 对于翻译循环：为每种语言添加错误处理（例如，在API调用周围使用`try/except`，记录失败，如果是401则跳过）。
   - 显式处理cookies？可能不需要——坚持使用API密钥。如果脚本有浏览器/Selenium代码，请移除以提高CI可靠性。

3. **工作流程改进**：
   - **输入验证**：添加对N=0或无效`--n`的检查，避免处理空内容。
   - **条件提交**：您的`git diff --cached --quiet || git commit`很好，但更新提交消息以反映所有语言：`-m "Add translated posts (ar, de, es, fr, hi, ja, zh, hant)"`。
   - **缓存**：添加`actions/cache`用于`pip`以加速安装。
   - **调试模式**：添加可选输入`debug: true`和脚本的`--debug`标志用于详细日志记录。
   - **权限**：确保`github-pages`环境具有所需的读写权限。
   - 完整的"Translate posts"步骤更新YAML片段：
{% raw %}

     ```
     - name: Translate posts
       run: |
         python scripts/translation/update_lang_notes.py --n ${{ inputs.n }}
       env:
         GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
         OPENAI_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
         OPENAI_BASE_URL: https://openrouter.ai/api/v1
     ```

{% endraw %}

4. **测试步骤**：
   - **本地测试**：在本地使用导出的环境变量运行`python scripts/translation/update_lang_notes.py --n 1`（例如`export OPENAI_API_KEY=your_key`）。
   - **工作流程测试**：使用`workflow_dispatch`和N=1触发，检查日志中的API调用。
   - **验证密钥**：在仓库设置 > Secrets中，确认`DEEPSEEK_API_KEY`具有有效的OpenRouter密钥（以`sk-or-...`开头）。
   - 如果仍然失败，向脚本添加`--verbose`并检查请求头（例如通过`print(client.api_key)`）。

这应该能解决401错误并使翻译流程正常运行。如果您分享`update_lang_notes.py`的代码片段（例如API客户端初始化部分），我可以更精确地定位问题。

#### 参考资料

- [OpenRouter快速入门（API认证设置）](https://openrouter.ai/docs/quickstart)
- [LiteLLM OpenRouter集成](https://docs.litellm.ai/docs/providers/openrouter)（如果使用）
- [关于类似OpenRouter认证错误的GitHub Issue](https://github.com/mendableai/firecrawl/issues/1352)
- [关于OpenRouter 401错误的Reddit讨论](https://www.reddit.com/r/openrouter/comments/1oqiaol/error_401_no_cookie_auth_credentials_found/)
