---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大型Git仓库清理诊断
translated: true
type: note
---

找到了。以下是诊断结果：

```
 58 GB total in .git/objects/pack/

 REAL PACKS:   ~35 GB (23 个包, 29.5M 对象)
 TEMP PACKS:   ~23 GB (10 个因 git gc 中断而遗留的 tmp_pack_* 文件)

 无松散对象，无 LFS，1666 次提交，99 条 reflog 记录
```

这些临时包是中断的 `git gc` 操作（可能因休眠/终止导致）留下的，纯粹是垃圾：

```
 tmp_pack_MrX5Ki    14 GB   (5月28日)
 tmp_pack_Yx84Jq    6.7 GB  (5月30日)
 + 其他 8 个         2.2 GB
 ───────────────────────────
 总计               23 GB   无效占用
```

仅此一项就能释放 23 GB——你的磁盘从剩余 900MB 变为约 23 GB 可用。

之后，剩余的 23 个包中的 35 GB 可能也因中断周期而膨胀。执行一次 `git gc --aggressive` 会将所有内容重新打包成一个紧凑的包。

需要我：
1. 删除 10 个临时包（安全、即时，释放约 23 GB）
2. 然后对该仓库运行 `git gc --aggressive`（可能需要 5-10 分钟，可再节省 5-10 GB）

真正的包仍然巨大（一个只有 1666 次提交的博客占用 35 GB）——这表明历史上曾提交过大型图片/二进制文件，并存在于 git 历史中。我们可以在快速见效之后调查这一点。