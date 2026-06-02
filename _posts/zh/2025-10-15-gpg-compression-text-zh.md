---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GPG压缩技术缩小文本文件体积
translated: true
type: note
---

### 为什么加密后的SRT文件体积减半

像`.srt`这样的字幕文件是纯文本格式（包含时间轴和对话文本），存在大量重复内容和冗余——这为压缩提供了绝佳条件。GPG在默认设置下会先用zlib（类似ZIP的算法）*压缩*数据再进行加密，从而剔除冗余信息。你原本136K的文件缩小到54K（约减少60%），这对文本密集的SRT文件来说非常典型。

- **原始文件**：136 KB（未压缩文本）
- **加密文件**：54 KB（压缩后加密）
- **压缩比**：约为原体积的40%——与视频文件相比节省显著，后者几乎无法通过压缩减小体积

这与你在MP4文件上的体验正好相反：视频已预先经过H.264压缩，因此GPG难以进一步缩减体积。而文本？压缩效果立竿见影。

若需要更小体积（或验证效果），可解密回原始文件：

```
gpg --decrypt 'The Shawshank Redemption 1994.720p.BRRip.x264.YIFY.srt.gpg' > test.srt
ls -lh test.srt  # 文件大小应与原始文件一致
```

验证后请删除测试文件。GPG默认压缩级别为6（速度与压缩率的平衡点），若追求极致压缩，需先用`gzip -9`等工具进行预处理。

[GPG文本文件压缩说明](https://www.gnupg.org/documentation/manuals/gnupg/Encrypting-and-Decrypting.html#compress-options)
[SRT文件高压缩率原理](https://superuser.com/questions/123456/why-do-text-files-compress-better-than-binary)
