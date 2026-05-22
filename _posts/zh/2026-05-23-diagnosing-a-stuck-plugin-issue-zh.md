---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断插件卡住问题
translated: true
type: note
---

现在我已经掌握了完整信息。以下是诊断：

---

## 根本原因：`/note` 卡住

`/note` 插件调用 `create_note_from_content()`，该方法向 OpenRouter 发出**同步 HTTP 请求**且**没有设置超时**。以下是确切的调用链：

```
/note
  → _handle_note()
    → create_note_from_content()
      → _generate_titles()
        → generate_title()
          → _call_llm_or_exit()
            → call_openrouter_api()
              → requests.post(url， headers， json， data)  ← 没有超时
```

### 问题 1：没有 HTTP 超时（卡住的主要原因）

在 `~/projects/ww/ww/llm/openrouter_client.py` 第 53 行：

```python
response = requests.post(url， headers=headers， json=data)
#                          ^^^ 没有超时参数！
```

如果 OpenRouter 响应慢、受到限速或网络中断，该请求会**永久阻塞**。CLI 是单线程的，因此整个界面都会冻结。

### 问题 2：没有用户反馈

插件处理程序在 `process_command()` 中同步运行（cli.py:8210-8211）：

```python
result = resolve_plugin_command_result(
    plugin_handler(user_args)   # 在此阻塞，没有旋转动画，没有进度提示
)
```

没有旋转动画，没有“正在生成标题...”之类的消息，用户只能盯着空白提示符。

### 问题 3：错误日志证据

来自 `agent.log` 于 01:14:43：

```
⚙️  /note [error] LLM call failed. Model: (not set)， max_tokens: 300
```

环境变量 `MODEL` 未被加载。插件第 69 行的 `dotenv` 加载可能正在运行，但 `override=False` 意味着如果 Hermes 已经在进程环境中设置了 `MODEL`，则 `.env` 的值会被跳过。或者 `.env` 加载静默失败。

### 问题 4：`sys.exit(1)` 会杀死 CLI

在 `create_note_utils.py` 第 53-56 行及第 61 行：

```python
if not content or not content.strip():
    print("Content is empty or invalid. Aborting.")
    sys.exit(1)  # 杀死整个 Hermes 进程！
```

如果内容为空或过短，`sys.exit(1)` 会终止整个 CLI，而不仅仅是该命令。

---

## 修复方案

最快的修复——添加超时和加载提示消息。编辑 `~/projects/ww/ww/llm/openrouter_client.py`：

```python
# 第 53 行：添加超时
response = requests.post(url， headers=headers， json=data， timeout=30)
```

并编辑 `~/.hermes/plugins/note/__init__.py` 以添加反馈并优雅地处理错误：

```python
# 在 _handle_note 中，调用 create_note_from_content 之前：
print("正在通过 LLM 生成标题...")

# 使用 try/except 包装，避免 sys.exit 杀死 CLI
try:
    file_path = create_note_from_content(text， custom_title=title， directory=note_dir)
    return f"笔记已保存：{file_path}
```

需要我应用这些修复吗？