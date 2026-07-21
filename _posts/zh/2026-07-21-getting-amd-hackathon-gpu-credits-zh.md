---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 获取AMD黑客马拉松GPU积分
translated: true
type: note
---

问题：参加AMD黑客马拉松时，是否需要向AMD员工申请Radeon Cloud积分？

回答：

是的，**很可能需要在开始使用Radeon Cloud GPU之前获取积分**，但不一定必须直接向AMD员工申请。通常有以下几种途径：

1. **黑客马拉松提供的积分**

   对于AMD赞助的黑客马拉松，组织者通常会为参与者提供云访问码/积分。最佳做法是：

   * 加入Luma活动
   * 加入活动的Discord/Slack（如有提供）
   * 向AMD组织者或导师询问：

   > “黑客马拉松参与者是否有GPU积分码或AMD Radeon Cloud访问权限？”

   这是常规方式。

2. **AMD开发者计划积分**

   AMD还有一个官方开发者计划，提供云积分。其当前流程为：

   * 加入AMD AI开发者计划
   * 申请云积分
   * 等待审批

   AMD表示开发者可通过开发者门户申请积分，审批基于使用场景。([AMD][1])

3. **Radeon Cloud账户积分**

   Radeon Cloud页面显示可通过GitHub或ModelScope登录，并在领取积分后启动GPU笔记本。([Radeon Cloud][2])

显示的“10积分/小时”含义如下：

```
GPU使用：
1小时 = 1积分

示例：
100积分 = 10小时GPU运行时间
```

重点是**在确认积分来源之前，不要启动GPU实例**，因为云GPU通常会在运行时消耗积分。

对于黑客马拉松，建议尽早询问：

```
Hi AMD团队，

我参加了AMD黑客马拉松，希望使用Radeon Cloud
进行项目开发。是否有为参与者提供的免费GPU积分？
如果有，能否分享领取流程或代码？

谢谢！
```

同时检查黑客马拉松是否有奖品或参与者福利说明。部分AMD活动会明确提供云积分或GPU访问权限。([AMD][3])

参考资料：

* AMD AI开发者计划云积分 ([AMD][1])
* AMD开发者门户会员福利 ([AMD Developer Portal][4])
* Radeon Cloud登录/积分门户 ([Radeon Cloud][2])

[1]: https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-claim-amd-cloud-credits.html?utm_source=chatgpt.com "如何领取AMD云积分"
[2]: https://radeon-global.anruicloud.com/profile?utm_source=chatgpt.com "Profile - Radeon Cloud"
[3]: https://www.amd.com/en/developer/resources/technical-articles/2026/build-across-the-ai-stack--join-the-amd-x-lablab-ai-hackathon-.html?utm_source=chatgpt.com "跨AI堆栈构建：加入AMD x LabLab.ai黑客马拉松"
[4]: https://developer.amd.com/member-perks/?utm_source=chatgpt.com "会员福利 - AMD开发者门户"