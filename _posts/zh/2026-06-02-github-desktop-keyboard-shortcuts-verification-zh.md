---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub 桌面版键盘快捷键验证
translated: true
type: note
---

以下是代码的实际内容：

```
验证：GitHub Desktop 键盘快捷键
════════════════════════════════════════════════

来源：app/src/ui/repository.tsx:687-715
        app/src/main-process/menu/build-default-menu.ts

1. Ctrl+Tab — 切换“更改”与“历史记录”
   ─────────────────────────────
   确认。在 repository.tsx 第 699 行：

     if (event.ctrlKey && event.key === 'Tab') {
       this.changeTab()
       event.preventDefault()
     }

   changeTab() 在 RepositorySectionTab.Changes
   和 RepositorySectionTab.History 之间切换。适用于所有平台
   （macOS、Windows、Linux）——它使用 event.ctrlKey，而非
   event.metaKey。

   注意：Shift 键被有意忽略——注释说明：
   “我们在这里不关心 shift 键，只要只有两个标签页，我们就能蒙混过关。”

2. ⌘G / Ctrl+G — 跳转到摘要（提交消息字段）
   ────────────────────────────────────────────────────
   确认。build-default-menu.ts 第 211 行：

     label: 'Go to Summary'
     accelerator: 'CmdOrCtrl+G'

   macOS 上为 ⌘G，Windows/Linux 上为 Ctrl+G。

3. F5 — “刷新所有 Git 数据”
   ──────────────────────────
   错误。代码库中没有任何 F5 快捷键。
   在所有 .ts/.tsx 文件中搜索 'F5' 的结果为零。
   没有专门的刷新快捷键。

4. ⌘1 / Ctrl+1 — 显示“更改”
   ────────────────────────────
   确认。build-default-menu.ts 第 180 行。

5. ⌘2 / Ctrl+2 — 显示“历史记录”
   ────────────────────────────
   确认。build-default-menu.ts 第 186 行。

完整快捷键列表（来自 build-default-menu.ts）：
────────────────────────────────────────────────────

  视图菜单：
    ⌘1 / Ctrl+1        → 显示“更改”
    ⌘2 / Ctrl+2        → 显示“历史记录”
    ⌘T / Ctrl+T        → 显示仓库列表
    ⌘B / Ctrl+B        → 显示分支列表
    ⌘⌥W / Ctrl+Alt+W   → 显示工作树列表
    ⌘G / Ctrl+G        → 跳转到摘要（提交消息）
    Ctrl+H              → 切换暂存更改
    ⌘L / Ctrl+L        → 切换更改过滤器
    ⌘0 / Ctrl+0        → 重置缩放
    ⌘= / Ctrl+=        → 放大
    ⌘- / Ctrl+-        → 缩小
    ⌘9 / Ctrl+9        → 展开活动可调整大小区域
    ⌘8 / Ctrl+8        → 收缩活动可调整大小区域

  仓库菜单：
    ⌘P / Ctrl+P        → 推送
    ⌘⇧P / Ctrl+Shift+P → 拉取
    ⌘⇧T / Ctrl+Shift+T → 获取
    ⌘⇧G / Ctrl+Shift+G → 在 GitHub 上查看
    ⌘⇧F / Ctrl+Shift+F → 在 Finder/资源管理器中显示
    Ctrl+`              → 在 Shell 中打开
    ⌘⌫ / Ctrl+Backspace → 移除仓库

  编辑菜单：
    ⌘F / Ctrl+F        → 查找
    ⌘, / Ctrl+,        → 偏好设置

  全局（不在菜单中）：
    Ctrl+Tab            → 切换“更改”/“历史记录”标签页
    Alt+⌘I / Ctrl+Shift+I → 切换开发者工具
```

因此，关于 `Ctrl+Tab` 的说法是正确的。`⌘G` 的说法也是正确的，但它是“跳转到摘要”（聚焦提交消息），在 UI 中并未标注为“聚焦提交消息字段”——它显示的是“Go to Summary”。关于 `F5` 的说法**完全是编造的**——代码库中没有任何 F5 快捷键。