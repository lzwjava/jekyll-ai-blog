---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Google Cloud上部署的直播
translated: true
type: note
---

完成。**直播现已在 Google Cloud 上正常运行。** 摘要：

## 部署内容

| 部分 | 变更 |
| --- | --- |
| `srs/srs.conf` | 新的 SRS 6 配置：RTMP 推流接收、HLS（2 秒分片）+ HTTP-FLV、每会话 DVR、hooks → 应用 |
| `docker-compose.yml` | 新增 `srs` 服务（`ossrs/srs:6`，端口 1935+8080，`restart: unless-stopped`，持久化 `./srs-data`） |
| `nginx.conf` | funlive.io vhost 上的 `/live/` 代理 → `<https://funlive.io/live/><key>.m3u8 | .flv`（无混合内容；为 web.funlive.io 播放器配置 CORS；已与仅 VM 的`fun-live-icon` 配置块合并） |
| `LiveDao.php` | `pushUrl` = `rtmp://funlive.io/live/<key>`，HLS/FLV/RTMP 播放 URL 已重新指向（所有 `*.quzhiboapp.com`/已失效的 Aliyun 主机已移除） |
| `LiveHooks.php` | 接收 SRS 6 JSON hook 请求体；拒绝流 key 没有对应 live 记录的推流 |
| `RecordedVideoDao.php` | 修复表名（`recorded_videos`）——原有的 CI3→CI4 迁移 bug |

## 验证过程中发现并修复的问题

1. **CI4 调试工具栏污染了 hook 的 `0` 响应**（开发模式下附加了 28 KB HTML）→ 每次推流都被 SRS 拒绝。已通过返回 `text/plain` 允许响应修复。
2. `recorded_video` → `recorded_videos` 表名。

## 端到端验证（生产环境）

- ffmpeg 推流 → `on_publish ok ... response=0`；未知 key → 拒绝 ✅
- `https://funlive.io/live/<key>.m3u8` 播放列表 + `.ts` 分片 ✅
- `https://funlive.io/live/<key>.flv` 流播放 ✅，CORS + `OPTIONS 204` 预检 ✅
- 停止推流 → `on_unpublish` + `on_dvr` → `recorded_videos` 记录 + FLV 在 `srs-data/` 中 ✅
- 已为 DVR 文件增加 45 天保留 cron（通过容器运行，处理 root 属主的文件）
- 测试流、数据记录和文件已清理；仓库已提交并推送（`6aa3bf3`、`a39d7e0`）

## 现在主播如何开播

在直播配置界面中：在 OBS 里填写 **URL** `rtmp://funlive.io/live` 和 **Stream Key**（每场直播的 key），然后点击开始推流。观众（attended/owner）会自动从 API 获取新的 `https://funlive.io/...` URL——**无需修改前端**。

## 说明

- 我本地的 RTMP 出站被你的 clash 代理阻止，所以推流测试是在 VM 本身上运行的；公网 1935 端口是开放的（`nc` 测试通过）——值得在主播的机器上用 OBS 做一次真实测试。
- Phase 5（回放）：将 `srs-data/` 中的 DVR FLV 转换为 HLS 并上传到 GCS（复用 `GcsStorage`），替换已失效的基于 ssh2 的 `RecordedVideos` 管道。需要时告诉我一声。
