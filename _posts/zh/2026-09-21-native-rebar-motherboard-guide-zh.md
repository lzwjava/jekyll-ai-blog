---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 原生ReBAR主板指南
translated: true
type: note
---

问题：**如果我希望ReBAR能官方正常启用，不希望通过ReBarUEFI解决，那我该买什么主板？**

答案：关键区别在于，ReBarUEFI的问题清单是**需要ReBarUEFI的主板列表**，而不是支持官方ReBAR的主板列表。该问题明确标注了`UEFIPatch: N`的主板，即这些主板的报告者没有使用ReBarUEFI补丁就成功启用了ReBAR。（[GitHub][1]）

如果你的目标是**“装好主板 → 在BIOS中启用Above 4G Decoding + Re-Size BAR → 无需自定义UEFI/ReBarUEFI”**，那么你应该选择**较新的平台**，而不是购买该列表中的老Z170/X99主板。

### ReBarUEFI数据中明确标注无需补丁的主板

| 主板型号                          | 平台       | 测试GPU    | ReBarUEFI补丁 |
| --------------------------------- | ---------- | ---------- | ------------- |
| Gigabyte X470 AORUS GAMING 5 WiFi | X470 / AM4 | Arc A770   | **无需**      |
| Gigabyte B450 AORUS ELITE         | B450 / AM4 | RX 590     | **无需**      |
| Gigabyte B450 AORUS M             | B450 / AM4 | RX 580     | **无需**      |
| Gigabyte B450M Gaming             | B450 / AM4 | RX 6700 XT | **无需**      |
| ASUS PRIME A320M-K                | A320 / AM4 | RX 6600    | **无需**      |
| MSI B450M PRO-VDH MAX             | B450 / AM4 | RX 580     | **无需**      |
| Gigabyte B550I AORUS PRO AX       | B550 / AM4 | RX 5600 XT | **无需**      |

例如，该问题特别指出**X470 AORUS GAMING 5 WiFi**的BIOS在Zen 3下官方支持ReBAR，而Zen 2则需要ReBarUEFI模块。（[GitHub][1]）

所以如果你**今天**要装机，我不会把那篇GitHub问题作为购买主板的指南。它主要记录的是如何让*不受支持/较旧的固件*工作。

### 重要规则

要想**完全不涉及ReBarUEFI**，请购买主板厂商BIOS文档中明确显示以下选项的主板：

```text
Above 4G Decoding       [Enabled]
Re-Size BAR Support     [Enabled]
```

现代AMD AM4/AM5和Intel第10代及以上的主板通常原生支持这些选项。

例如，与其因为ASUS Z170-A有成功的ReBarUEFI报告而购买它，不如选择一块**ReBAR是厂商BIOS中正常功能**的主板。

ReBarUEFI项目本身也将其目的描述为为不支持Resizable BAR的系统添加该功能，因此使用现代原生支持ReBAR的平台就无需该补丁了。（[GitHub][2]）

**如果你特别想为RX 6600/6700 XT或RTX 3060/3090这类显卡组装一台最便宜的主机，请告诉我你计划使用的CPU+GPU。我可以帮你缩小到具体几款便宜且原生BIOS支持ReBAR的主板，而不是依赖ReBarUEFI。**

[1]: https://github.com/xCuri0/ReBarUEFI/issues/11 "List of working motherboards · Issue #11 · xCuri0/ReBarUEFI · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI "GitHub - xCuri0/ReBarUEFI: Resizable BAR for (almost) any UEFI system · GitHub"
