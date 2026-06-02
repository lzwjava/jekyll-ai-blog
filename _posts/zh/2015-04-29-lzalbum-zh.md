---
audio: false
generated: false
image: false
lang: zh
layout: post
title: LZ相册
translated: true
type: post
---

这是来自 GitHub 项目 [https://github.com/lzwjava/LZAlbum](https://github.com/lzwjava/LZAlbum) 的 README.md。

---

# LZAlbum

基于 LeanCloud 的 Moments 特性，展示了如何在 LeanCloud 上建模一对一和一对多的关系。

![album](https://cloud.githubusercontent.com/assets/5022872/9563818/dd9588ba-4ec3-11e5-940a-3d1e84b967f0.gif)

# 支持

如果在使用过程中遇到任何问题，请在 [issue](https://github.com/lzwjava/LZAlbum/issues) 中提出，我将在 GitHub 上提供帮助。

# 运行

```
   pod install --no-repo-update --verbose (如果遇到缺少库的错误，请删除 --no-repo-update)
   open LZAlbum.xcworkspace
```

# 致谢

UI 设计大量借鉴了 [MessageDisplayKit](https://github.com/xhzengAIB/MessageDisplayKit)，并且数据存储在 LeanCloud 上。对两者表示感谢。

# 后端

![image](https://cloud.githubusercontent.com/assets/5022872/7449102/2390131e-f260-11e4-8978-cead60e2f272.png)

使用公共账户登录 <https://leancloud.cn，凭证>: <leancloud@163.com>/Public123，然后选择 LCAlbum 应用程序以查看表格结构。
**注意：请勿修改后端数据，只需查看。否则，可能会导致客户端崩溃。**
**注意：上述凭证不是用来登录此应用程序，而是用于 LeanCloud 后端。对于应用程序登录，只需在注册页面注册一个新账户即可。**

# 文档

[相关文档](https://leancloud.cn/docs/ios_os_x_guide.html)

# 许可证

MIT
