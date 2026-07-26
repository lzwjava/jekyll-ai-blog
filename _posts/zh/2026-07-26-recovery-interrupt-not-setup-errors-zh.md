---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复中断，非设置错误
translated: true
type: note
---

问题：从setuperr.log确认——“恢复环境”触发是否是实际致命原因，还是其他错误（OneSettings、0x80070490、0x80072EE7）才是真正问题？

回答：那些早期错误都是误导信息，忽略它们即可：

- `0x80070490` (CUnattendManager) 和 `0x80072EE7` (OneSettings初始化失败)——这些只是**Setup尝试联网获取更新/遥测数据，但由于当时WinPE中没有网络连接而失败**。这几乎在每次离线USB安装时都会发生，**不会**阻止Setup继续执行。`0x80072EE7` 具体是DNS/名称解析失败——在WinPE无网络环境下完全正常。
- `0x80070002` (GetWuIdFromRegistry)——文件/注册表项未找到，在全新安装中也是常规情况，非致命错误。

**实际的致命链正是我之前指出的：**

```
CSetupManager::OnFinishLaunchChoiceAction(8149): Result = 0xC19001F4
```

这是唯一一个在后续每个调用中级联传递并强制退出Setup的错误（`CSetupHost::Execute(564): Result = 0xC19001F4`）。它由**用户请求的恢复环境启动**触发——即Setup被告知放弃安装并跳转到恢复模式，而非硬件/介质/网络故障。

因此确认：这是安装过程中发生的中断（很可能是按键触发），而不是损坏的ISO/USB或磁盘问题。**重新执行安装，进度条开始后不要触碰键盘**——从磁盘选择完成后直接让它无干预地运行，直到所有重启进入OOBE。
