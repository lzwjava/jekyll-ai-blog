---
audio: false
generated: true
image: false
lang: zh
layout: post
title: V2RayNG 新增 Hysteria2 支持时间线
translated: true
type: note
---

V2RayNG（来自 https://github.com/2dust/v2rayNG 的 Android 客户端）在 2024 年的某个时候添加了对 **Hysteria 2**（通常缩写为 hy2）的支持，此前在 2024 年 1 月的早期请求中明确表示不支持（因为当时 Xray core 缺少它；issue #2799 被关闭为已完成但当时未添加）。

证据表明支持已在 **2024 年 9 月** 出现：
- 2024 年 9 月下旬的 issue（例如 #3618、#3619）讨论了 **version 1.9.4** 中 Hysteria2 的 bug/功能，例如缺少混淆（salamander）密码的输入字段以及与其他客户端的比较。这确认了 v1.9.4（可能在 2024 年夏/秋发布）已存在完整或部分集成。

初始添加很可能发生在 2024 年 2 月（无支持）和 2024 年中旬之间，可能首先通过基于插件的实现（后来被重构）。

后续发展：
- 到 2024 年底/2025 年初，用户已在 v2rayNG 中积极使用/配置 Hysteria2（issue 如 #4080、#4107 讨论配置导出、hy2 URI 的 pinSHA256 验证）。
- 在 **version 2.0.13**（2026 年 3 月 3 日发布）中，开发者**重构了 Hysteria2**，将其直接与 **Xray core** 集成（而非之前的插件/外部实现），并移除了插件版本。Changelog 条目：“重构Hysteria2 ，使用xray core ，并移除插件版本”（Refactored Hysteria2, using Xray core, and removed the plugin version）。这暗示之前的支持是基于插件的，在此次原生/core 切换之前。
- 围绕 2026 年 1 月 15 日，移除了与 Hysteria 相关的 submodule，与此次重构/清理一致。

注意：早期的 Hysteria2 请求被拒绝，因为上游 Xray-core 最初不支持它（Hysteria2 稳定版约于 2023-2024 年发布）。v2rayNG 使用了独立的集成方法，直到与 Xray 更新对齐。

要获取确切的初始版本/日期，请检查 GitHub 上的旧 release 标签（例如，扫描 v1.9.x 的 changelog 或 2024 年中旬的提交，查找“add hysteria2”或类似内容），但现有证据显示它在 **2024 年中旬之前不支持**，并从 2024 年 9 月起被积极使用。如果您使用的是较新版本（2.0+），Hysteria2 通过 Xray 原生支持。