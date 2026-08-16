---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复隐藏的微信窗口
translated: true
type: note
---

已完成。助手脚本已保存至 `~/.local/bin/fix-wechat.sh`，并且执行成功——它映射了 4 个隐藏的微信窗口并激活了主窗口。

## 总结

| 项目 | 状态 |
|---|---|
| **原因** | 微信自 8 月 13 日起一直在运行，但其窗口被隐藏/取消映射；启动器图标只是生成了无效的第二个实例（单实例应用），因此没有任何窗口显示 |
| **非原因** | 未发生崩溃、段错误、线程挂起或日志损坏——进程树是健康的 |
| **已应用的修复** | 通过 X（`xdotool windowmap`）强制映射隐藏窗口——未杀死应用，您的会话未受影响 |
| **助手** | `~/.local/bin/fix-wechat.sh`——当微信窗口再次丢失时随时运行 |

**如果再次发生**，只需运行：
```bash
fix-wechat.sh
```

**可选清理**（建议执行，因为微信已运行 3 天且存在僵尸子进程）：
```bash
pkill -f '/opt/wechat' ; sleep 2 ; nohup /usr/bin/wechat >/dev/null 2>&1 &
```

请告知微信窗口现在是否已在屏幕上正常显示。