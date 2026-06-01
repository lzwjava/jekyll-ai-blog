---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大小标志需要单位后缀
translated: true
type: note
---

以下是确切的问题。问题出在 `commands/volumes.go` 中：

**第 152 行：** `size, err := humanize.ParseBytes(sizeStr)`  
**第 194 行：** `createVolume.SizeGigaBytes = int64(size / (1 << 30))`

当你传入 `--size 200`（纯数字，无单位后缀）时，会发生以下情况：

1. `humanize.ParseBytes("200")` 将字符串拆分为 num="200" 和 extra=""（空后缀）
2. 在 `bytesSizeTable`（第 49 行）中：`""` 映射到 `Byte`（值为 1）
3. 结果：`200 * 1 = 200 bytes`
4. 除法：`200 / (1 << 30)` = `200 / 1073741824` = **0 GiB**（整数截断）

因此 `--size 200` 会创建一个 **0 GiB 的卷**——这就是 API 拒绝它的原因。

**解决方法：** `--size` 标志要求带有单位后缀。请使用：

```
doctl compute volume create my-vol --size 200GiB --region sgp1
```

`bytesSizeTable` 中有效的后缀：
- `GiB`、`gib`、`gi`、`g` → GiB（二进制）
- `GB`、`gb` → GB（十进制，基于 1000）
- `TiB`、`tib`、`ti`、`t` → TiB
- `TB`、`tb` → TB

第 53 行的默认值是 `"4TiB"`——这确认了 CLI 始终期望后缀。这与 AMD Dev Cloud Web UI 不同，后者将单位默认设置为 GiB。