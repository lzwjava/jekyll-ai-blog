---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 大疆Mini 3追踪功能限制与应对方案
translated: true
type: note
---

DJI Mini 3（基础款）不具备视觉目标跟随（ActiveTrack）或GPS追踪（Follow Me）等内置功能，无法自动跟拍行驶中的车辆或进行悬空拍摄。这是相比高端DJI无人机的重要功能限制。不过，DJI Mini 3 Pro支持ActiveTrack功能，可通过无人机摄像头对汽车、行人或车辆进行视觉追踪，实现后方、上方等多角度智能跟随，在保持设定距离和高度的同时捕捉动态影像。

关于定制开发的API支持：
- DJI Mobile SDK（支持Android/iOS应用）确实兼容Mini 3系列，支持虚拟摇杆指令（如手动调整位置/速度）和航点任务等基础飞行控制。若整合车辆的实时GPS数据（通过蓝牙、配套应用或外部发射器），可开发定制应用实现车辆路径跟踪。这虽非"即插即用"的视觉追踪，但通过计算偏移量（如后方10-20米/上方50米）能近似实现高空或后方跟拍。
- 但需注意：SDK的ActiveTrack任务API（用于自动视觉跟随）在Mini 3和Mini 3 Pro上均**不受支持**，该功能仅限Mavic Air 2或Air 2S等旧款机型。
- 飞行中可通过SDK相机API实现自动拍摄，支持基于定时器、距离或自定义逻辑的触发机制。

若考虑使用第三方应用（底层调用SDK）：
- 如Dronelink或Litchi等应用可通过手机GPS（或外接设备）为Mini 3启用基础"Follow Me"模式。要实现车辆追踪，需在车辆上配置GPS信标（如通过智能手机热点或专用追踪器向应用传输数据）。已有用户通过此方案在公路或小径实现车辆跟拍，无人机可保持头顶伴随或后方追踪。

重要法律与安全提示：无人机跟拍移动车辆需遵守当地法规（如美国FAA要求保持目视接触，禁止超视距操作）。建议在开阔区域测试以避免障碍物，且Mini 3的轻量化设计会限制高速跟拍时的抗风能力。

### 参考资料
- [DJI Mini 3 Active Track破解教程](https://www.youtube.com/watch?v=UYzSdd3iJwA)
- [Mini 3是否支持汽车等物体的AI追踪](https://www.facebook.com/groups/djimini3ukowners/posts/2726498670890510/)
- [Follow Me模式详解及Mini 3兼容性](https://www.reddit.com/r/dji/comments/13pqbw7/can_someone_explain_follow_me_mode_and_if_its_on/)
- [通过Dronelink实现Mini 3/3 Pro跟随模式](https://www.youtube.com/watch?v=Rhneo8QoXV0)
- [DJI产品SDK兼容性列表](https://support.dji.com/help/content?customId=01700000763&spaceId=17&re=US&lang=en&documentType=&paperDocType=ARTICLE)
- [DJI发布支持Mini 3 Pro与Mini 3的MSDK 5.3.0](https://forum.flylitchi.com/t/dji-has-released-msdk-5-3-0-with-support-for-mini-3-pro-and-mini-3/9512)
- [ActiveTrackOperator类 - DJI移动SDK文档](https://developer.dji.com/api-reference/android-api/Components/Missions/DJIActiveTrackMissionOperator.html)
