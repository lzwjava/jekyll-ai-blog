---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 立即安全升级Open WebUI
translated: true
type: note
---

明白了。以下是安全无痛的 Open WebUI 升级方法。

## 如果使用 `pip` 安装（你的情况）

```bash
# 1) （推荐）激活你用于 Open WebUI 的环境
#    例如 conda：
conda activate open-webui
#    或 venv：
# source ~/open-webui-venv/bin/activate

# 2) 升级到最新版本
python3.11 -m pip install -U open-webui

# 3) （可选）如果 pip 缓存导致问题
python3.11 -m pip cache purge
python3.11 -m pip install --no-cache-dir -U open-webui

# 4) 验证安装结果
python3.11 -m pip show open-webui
```

官方文档说明只需执行 `pip install -U open-webui` 即可升级到最新版本。（[Open WebUI][1]）

### 保持数据/设置持久化

运行服务器时，可以指定数据目录以确保升级不影响数据：

```bash
# macOS/Linux
DATA_DIR="$HOME/.open-webui" open-webui serve
# Windows (PowerShell)
$env:DATA_DIR="C:\open-webui\data"; open-webui serve
```

这遵循了官方文档的建议：设置 `DATA_DIR`（或在使用 `uvx … @latest serve` 时设置相同变量），确保聊天记录和配置独立于软件包安装。（[Open WebUI][2]）

> 提示：如果之前未使用 `DATA_DIR`，现在开始使用；Open WebUI 将从此使用该文件夹。

## 如果使用 Docker（供参考）

```bash
# 停止并移除旧容器（数据保存在命名卷中）
docker rm -f open-webui

# 拉取最新镜像
docker pull ghcr.io/open-webui/open-webui:main

# 使用现有卷重新启动
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

这是项目推荐的手动更新流程；你的数据将持久保存在 `open-webui` Docker 卷中。（[Open WebUI][3]）

## 检查最新版本

你可以在升级前后通过 GitHub Releases 确认最新版本标签。（[GitHub][4]）

如果出现错误（例如 Python 版本不匹配），请确保在 pip 方式中使用 Python 3.11，这是项目明确推荐的版本。（[GitHub][5]）

需要我检查你当前环境或解读升级错误输出吗？请粘贴到这里，我会帮你排查。

[1]: https://docs.openwebui.com/getting-started/quick-start/?utm_source=chatgpt.com "️ 快速开始"
[2]: https://docs.openwebui.com/?utm_source=chatgpt.com "Open WebUI：首页"
[3]: https://docs.openwebui.com/getting-started/updating/?utm_source=chatgpt.com "更新 Open WebUI"
[4]: https://github.com/open-webui/open-webui/releases?utm_source=chatgpt.com "版本发布 · open-webui/open-webui"
[5]: https://github.com/open-webui/open-webui?utm_source=chatgpt.com "open-webui/open-webui：用户友好的 AI 界面……"
