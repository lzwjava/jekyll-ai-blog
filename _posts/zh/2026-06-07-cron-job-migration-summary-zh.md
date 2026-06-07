---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cron任务迁移摘要
translated: true
type: note
---

综合摘要：

我们的工作内容
───────────

1. 创建了一个 Hermes 定时任务，每 2 分钟执行 `ww appearance smart-auto`
2. 将 `weekly-repo-update` 的调度从“每周日早上9点”改为“每小时”
3. 将两个任务从 Hermes 内部调度器迁移到 macOS 系统 crontab
4. 分析了基于摄像头 smart-auto 的隐私影响

当前系统 crontab
──────────────────────
*/2* ** */opt/homebrew/bin/ww appearance smart-auto
0* ** * /opt/homebrew/bin/ww projects update

`ww appearance smart-auto` 工作原理
─────────────────────────────────────
来源：/Users/lzwjava/projects/ww/ww/display/appearance.py（第96-181行）

步骤1 — 采集：使用 `imagesnap`（首选）或 `ffmpeg` 从摄像头抓取一帧，分辨率 640x480
步骤2 — 转换：用 PIL 打开图像，转换为灰度模式（"L" 模式）
步骤3 — 分析：通过 numpy 计算平均像素亮度（0-255 范围）
步骤4 — 判断：亮度 < 80（阈值）→ 深色模式
                   亮度 >= 80 → 浅色模式
步骤5 — 清理：在 `finally` 块中删除临时 JPEG 文件（始终执行）

隐私分析
───────────────
✓ 100% 本地处理 — 无网络调用、无 API 密钥、无 LLM
✓ 亮度计算后立即删除图像
✓ 无数据离开本机
✓ 采集时摄像头 LED 闪烁（视觉指示）
⚠ 每 2 分钟执行一次较为频繁 — 绿灯会频繁闪烁
⚠ 如果缺少 `imagesnap`/`ffmpeg`，命令会报错失败

`ww projects update` 的作用
──────────────────────────────
拉取 ~/projects/ 下 60 个已配置开源仓库的最新变更

Hermes vs 系统 crontab
─────────────────────

- Hermes 定时任务：内部调度器，存储在 ~/.hermes/，通过 agent 管理
- 系统 crontab：macOS crond，通过 `crontab -l` / `crontab -e` 管理
- 两者相互独立 — Hermes 任务不会出现在系统 crontab 中
- 我们迁移到系统 crontab 以实现透明度和直接 CLI 访问

验证 / 管理
───────────────
查看：   crontab -l
编辑：   crontab -e
删除：   crontab -r（删除所有）
