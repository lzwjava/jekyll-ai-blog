---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缺少启动和安装WIM文件
translated: true
type: note
---

问题：USB 不包含 `boot.wim` 和 `install.wim`——这是什么意思？

答案：

这是一个**非常重要的线索**。

正常的 Windows 11 安装 U 盘必须包含：

```
\sources\boot.wim
\sources\install.wim
```

或者：

```
\sources\boot.wim
\sources\install.swm
\sources\install2.swm
```

`boot.wim` 是必需的，因为它包含 Windows PE（安装环境）。

`install.wim` / `install.swm` 包含实际的 Windows 映像。

如果两者都缺失，你的 U 盘**不是有效的 Windows 安装介质**。

---

根据你在 Mac 上的先前步骤：

* FAT32 格式
* 手动复制 ISO 文件
* 因为 FAT32 有 4GB 限制而拆分 WIM

可能的错误是：

你复制了文件，但忘记了 `sources` 目录的内容，或者拆分 WIM 操作没有正确创建 `.swm` 文件。

---

检查 U 盘结构：

```cmd
dir D:\
```

你应该看到类似这样的内容：

```
boot
efi
sources
support
setup.exe
```

然后：

```cmd
dir D:\sources
```

预期结果：

```
boot.wim
install.swm
install2.swm
...
```

---

## 修复：从 Mac 重新创建 U 盘

挂载 ISO：

```bash
hdiutil attach Win11_25H2_English_x64_v2.iso
```

假设：

ISO 挂载点：

```
/Volumes/CCCOMA_X64FRE_EN-US_DV9
```

U 盘挂载点：

```
/Volumes/WIN11
```

复制除 install.wim 之外的所有内容：

```bash
rsync -avh \
--exclude=sources/install.wim \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/ \
/Volumes/WIN11/
```

安装 wimlib：

```bash
brew install wimlib
```

拆分：

```bash
wimlib-imagex split \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
/Volumes/WIN11/sources/install.swm \
3800
```

之后：

```bash
ls /Volumes/WIN11/sources/
```

应该显示：

```
boot.wim
install.swm
install2.swm
```

---

然后弹出 U 盘：

```bash
diskutil eject /Volumes/WIN11
```

再次从 U 盘启动 Lenovo。

---

你当前的失败错误码：

```
0xC19001F4
```

现在更有意义了。安装程序启动是因为 `boot.wim` 可能以某种方式被加载了，但安装映像/设置阶段出现了问题。

首先验证：

```cmd
dir D:\sources\boot.wim
```

因为如果 `boot.wim` 也缺失，那么 U 盘的创建肯定有问题。
