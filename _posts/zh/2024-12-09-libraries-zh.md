---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 使用库时要考虑升级问题
translated: true
type: post
---

我在创业项目 [Fun Live](https://github.com/lzwjava/live-server) 中使用了 CodeIgniter。虽然这个项目已经结束了，但几年后，我想重新启动它来纪念这段经历。然而，在2016年时，我使用的是 CodeIgniter 3，而现在最新版本已经是 CodeIgniter 4。

升级过程变得非常麻烦，因为我的代码与 CodeIgniter 框架紧密耦合。参考升级指南 [https://codeigniter4.github.io/CodeIgniter4/installation/upgrade_4xx.html](https://codeigniter4.github.io/CodeIgniter4/installation/upgrade_4xx.html) 可以看出，更新代码库需要投入大量工作。

这次经历给了我一个重要的教训：在编写代码时，我们应该仔细考虑如何处理未来的更新。明确区分哪些代码是我们可以控制的，哪些是由第三方依赖控制的，这一点至关重要。
