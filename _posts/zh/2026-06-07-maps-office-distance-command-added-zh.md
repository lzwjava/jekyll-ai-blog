---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新增地图办公距离命令
translated: true
type: note
---

完成。已添加 `ww maps office` 命令。以下是概要：

修改的文件：
  - ww/maps/maps.py    — 新增 cmd_office()、_haversine_km()，注册到 COMMANDS 和帮助
  - ww/main.py         — 添加到 Maps 帮助部分（按字母顺序）
  - ~/.zsh/completions/_ww — 将 'office' 添加到 maps_cmds（按字母顺序）

用法：
  ww maps office <lat,lng>
  ww maps office "22.838889,114.498969"

显示内容：
  - 反向地理编码得到的 FROM 地址
  - TO：OneLink 办公室（万菱国际中心，天河路 230-232号）
  - 直线距离（haversine）
  - 驾车路线距离 + 时间（Google Directions API）
  - 公交路线距离 + 时间（如有）
  - 路线概览（含高速名称）
  - 逐步导航（前5步 + 后3步）
  - 驾车/直线距离比

运行 `source ~/.zshrc` 或 `autoload -Uz compinit && compinit` 以启用 Tab 补全。