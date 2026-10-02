---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI Z170A上的CSM步骤已验证
translated: true
type: note
---

问题：所述关于在MSI Z170A Gaming M5上启用CSM的操作步骤是否准确？

答案：基本正确，但部分内容未经证实或表述过于肯定。

**已确认的部分**
- MSI的常见问题解答（FAQ）给出了路径：BIOS设置 → 设置 → 高级 → Windows操作系统配置 → Windows 8.1/10 WHQL支持 = 禁用，Z170A Gaming M5在其型号列表中。
- MSI的另一条FAQ指出，当启动模式选择（Boot Mode Select）灰显为[UEFI]时，应将Windows 10 WHQL支持设置为禁用。Z170A Gaming M5也在该列表中。
- 当WHQL支持启用时，启动模式选择（LEGACY+UEFI / UEFI）变得不可选并自动设置。因此，先禁用WHQL支持，再检查启动模式选择的顺序是正确的。
- MSI在此代主板上没有独立的“CSM”开关。一位论坛用户指出MSI主板上没有CSM，而WHQL设置具有类似功能。

**我持谨慎态度的部分**
- **测试B中的“Windows 10 WHQL支持 = 启用 / UEFI”没有问题。** 启用此选项会将系统切换到UEFI模式。额外的“CSM = 禁用”行是多余的，因为启用WHQL会自动处理这一点。
- **针对M40的“Above 4G Decoding”和“PCIe速度 = Gen2”未在我的资料来源中提及。** 我无法确认此BIOS是否具有Above 4G Decoding选项，且文本中用“如果有”含糊其辞。Gen2的建议是故障排除思路，并非MSI的官方文档。
- **BIOS版本声明未经证实。** 文本称当前版本为7977v1I，但我无法从结果中确认。请直接查阅MSI的支持页面。
- **我无法验证第三个MSI链接。** 文本引用了BIOS手册页面，但我没有检索到。不过我找到的Z170A PC Mate手册确实显示了相同的菜单结构。
- **链接带有`utm_source=chatgpt.com`跟踪标签，** 表明它们是从ChatGPT获取的。FAQ编号（2622和2803）是真实的。

**总结：** 核心操作步骤正确。将Windows 10 WHQL支持设置为禁用，然后在启动模式选择中选择Legacy+UEFI。请在自己的主板上验证M40专用调整项。

参考来源：
- [MSI美国FAQ 2622: Windows操作系统配置](https://us.msi.com/faq/2622)
- [MSI FAQ 2803: 启动模式选择灰显](https://www.msi.com/faq/mb-2803)
- [MSI Z170A PC Mate手册: Windows操作系统配置](https://www.manualslib.com/manual/1020804/Msi-Z170a-Pc-Mate.html?page=45)
- [Tom's Hardware: Win10 UEFI安装的BIOS设置](https://forums.tomshardware.com/threads/bios-settings-for-win10-uefi-install.3573007/)