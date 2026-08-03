---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FluxReel 重命名已全局完成
translated: true
type: note
---

重命名为 **FluxReel** 已完成。 ✅

**变更内容** (提交 `e49cb31`，已推送至 `origin/main`):

| 位置 | 之前 | 之后 |
| --- | --- | --- |
| Python 包 | `ahl/` | `fluxreel/` (git 跟踪重命名，共 20 个文件) |
| CLI 命令 | `ahl` | `fluxreel` (`fluxreel img`, `fluxreel server`, `fluxreel tunnel`…) |
| pip 包 | `ahl 0.2.0` | `fluxreel 0.2.0` (旧条目已卸载) |
| 所有导入 | `from ahl.…` | `from fluxreel.…` |
| 配置路径 | `~/.config/ahl/.env` | `~/.config/fluxreel/.env` |
| pyproject.toml | name/description/script | `fluxreel` + 新描述 |
| fabfile.py | `/root/ahl` 部署目标 | `/root/fluxreel` |
| Web UI | "🌸 AI Video Generator" | "🌸 FluxReel" + title 标签 |
| API 标题 | "Gen Video API" | "FluxReel API" |
| localStorage 键 | `ahl_api_key` | `fluxreel_api_key` |
| 提交文档 | `ahl` 品牌 | **FluxReel** 品牌，命令 `fluxreel` |
| PPT | `ahl_slides.pptx` | `fluxreel_slides.pptx` (从 Marp 重新渲染) |

**已验证工作正常:**

- `python -m fluxreel` 和 `fluxreel` 控制台脚本均可运行
- 所有导入均解析成功（`SdCppProvider` 加载正常）
- 服务器以 FluxReel 身份重启于 `:8000`，健康检查正常，新的 UI 品牌已提供

注意：运行的服务器已在新模块下重启（`-m fluxreel.gen_video.server`），旧 `ahl` pip 条目已卸载——环境已完全切换到 FluxReel。
