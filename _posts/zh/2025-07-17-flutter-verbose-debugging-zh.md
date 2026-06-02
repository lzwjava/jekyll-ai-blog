---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Flutter详细模式调试指南
translated: true
type: note
---

明白了 👍 —— Flutter 确实有**详细模式**，该模式会打印*所有*底层操作日志，方便你定位卡顿环节。

---

### ✅ 启用详细日志模式运行 `flutter` 命令

只需添加 `-v`（或 `--verbose`）参数：

- 清理项目：
  ```bash
  flutter clean -v
  ```

- 获取依赖：
  ```bash
  flutter pub get -v
  ```

- 运行应用：
  ```bash
  flutter run -v
  ```

这将向终端输出详细日志（网络请求、文件删除、CocoaPods 命令等）。

---

### 📌 查看详细日志的技巧
- 重点关注**最后几行**输出 → 这里会显示进程卡在哪一步
- 常见卡顿场景：
  - **CocoaPods** 依赖解析（网络缓慢/仓库过期）
  - **Gradle** 同步（Android 构建阶段）
  - 目录权限问题（Flutter 无权限访问某些目录）

---

👉 若 `flutter clean -v` 仍无响应，请将最后约 20 行日志粘贴至此 ⬇️，我将帮你精准定位问题根源。

需要我为你编写一个**带详细日志的快捷清理脚本**吗？这样你只需执行 `./super_clean.sh` 即可替代手动输入多条命令。
