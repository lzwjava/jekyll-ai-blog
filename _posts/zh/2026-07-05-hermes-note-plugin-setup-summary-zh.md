---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes笔记插件设置摘要
translated: true
type: note
---

## Note Plugin — 完整设置总结

### 已完成的工作

**1. 安装 Fcitx5**（上一次会话）
- `apt install fcitx5 fcitx5-chinese-addons im-config`
- 通过 `im-config -n fcitx5` 设为默认输入法
- 配置位于 `~/.config/fcitx5/` — 启用 keyboard-us + pinyin 双拼模式

**2. 笔记插件 — 已存在并更新**
- 该插件存在于两个位置：
  - `~/.hermes/plugins/note/` — Hermes 从此读取（用户插件目录）
  - `~/projects/config/hermes/plugins/note/` — 你的配置仓库（数据源）
- 位于 `~/.hermes/plugins/note/` 的当前版本是旧副本（5月23日）
- 将 `__init__.py` 更新至7月版本，包含：
  - 推理标签剥离（`` 等）
  - 从 `~/projects/ww/.env` 加载环境变量
  - 通过 ww 的 `openrouter_client` 生成 LLM 标题
  - 通过 `gitmessageai` 自动 Git 提交与推送
  - 当 ww 未通过 pip 安装时，回退插入 sys.path
- 相应更新了 `plugin.yaml`

**3. 插件已启用**，在 `~/.hermes/config.yaml` 中：
```yaml
plugins:
  enabled:
  - note
```

**4. 依赖安装**（安装到 Hermes 虚拟环境 `~/.hermes/hermes-agent/venv/`）：
- `ww` 包 — 通过 `uv pip install --no-deps -e ~/projects/ww` 安装
- `pyperclip` — 用于剪贴板操作
- `python-dotenv` + `requests` — 已在 Hermes 虚拟环境中

未安装 `ww` 的完整依赖树（torch, cudnn, whisperx, playwright — 2GB+），因为只需要 `ww.note.create_note_from_content` 和 `ww.github.gitmessageai`。

**5. 验证：** 插件在 `hermes plugins list` 中显示为 `enabled`。导入测试成功。

### `/note` 如何工作

在 Hermes CLI 会话中：
```
/note                         # 保存最后一条助手回复
/note 3                       # 保存倒数第三条回复
/note --title "My Title"      # 自定义标题
/note --dir ~/my-notes        # 自定义目录
/note 2 --title "Foo" --dir ~/notes
```

流程：
1. 剥离推理标签（`...`）
2. 提示 LLM（通过 `ww.llm.openrouter_client`）生成一个6个单词的标题
3. 写入 `~/notes/<date>-<slug>-en.md` 并包含 YAML 前置元数据
4. 运行 `gitmessageai` 自动提交并推送

### 涉及的文件

| 文件 | 角色 |
|------|------|
| `~/.hermes/plugins/note/__init__.py` | 插件入口点（已更新） |
| `~/.hermes/plugins/note/plugin.yaml` | 插件元数据（已更新） |
| `~/.hermes/config.yaml` 第642行 | 插件启用列表 |
| `~/projects/ww/ww/note/create_note_from_clipboard.py` | 笔记创建逻辑 |
| `~/projects/ww/ww/note/create_note_utils.py` | 标题生成、前置元数据、文件操作 |
| `~/projects/ww/ww/github/gitmessageai.py` | 自动 Git 推送 |
| `~/projects/ww/.env` | 配置（MODEL, BASE_PATH, OPENROUTER_API_KEY） |
| `~/.config/fcitx5/profile` | Fcitx5 输入法配置 |
| `~/.config/fcitx5/conf/pinyin.conf` | 拼音引擎（双拼模式） |