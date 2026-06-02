---
audio: false
generated: true
lang: zh
layout: post
title: Meta智能眼镜：功能与API详解
translated: true
type: note
---

我们来详细解析Meta的智能眼镜产品线（包括Ray-Ban和Oakley）、用户规模及其为开发者提供的API支持。

**Meta VR眼镜、Ray-Ban和Oakley智能眼镜分别是什么？**

首先需要厘清术语。"Meta VR Glass"并非Meta官方广泛使用的产品名称，该公司主要的VR/MR产品是**Meta Quest**系列头显设备（如Meta Quest 3）。

当人们提及"Meta眼镜"时，通常指以下采用眼镜形态的产品：

* **Ray-Ban Meta智能眼镜**：这是与EssilorLuxottica（雷朋母公司）合作开发的消费级智能眼镜，外观设计延续经典雷朋太阳镜风格，主要功能包括：
  * 免提拍照录像（配备隐私指示灯）
  * 开放式耳廓扬声器（支持音乐、播客、通话）
  * 集成麦克风阵列（支持通话与语音指令，含唤醒Meta AI的"Hey Meta"）
  * 支持向Facebook和Instagram进行直播
  * 集成Meta AI实现多种功能（信息查询、消息发送、环境描述辅助功能等）
  * 无内置显示屏或AR头显功能（属于"智能眼镜"而非典型AR眼镜）

* **Oakley Meta眼镜（如Oakley Meta HSTN）**：这是与EssilorLuxottica旗下Oakley合作推出的新款"运动AI眼镜"，在保留Ray-Ban Meta核心功能基础上专为运动员优化：
  * 延续Oakley标志性运动美学设计
  * 增强耐用性与防水等级（IPX4）
  * 更长续航表现
  * 更高清摄像系统（3K视频）
  * 集成Meta AI并提供运动定制功能（如高尔夫风速查询）

**用户规模如何？**

截至2025年2月，**Ray-Ban Meta智能眼镜**自2023年9月发布以来累计销量已突破**200万台**。EssilorLuxottica计划在2026年底前将年产能提升至1000万台，印证了市场强劲需求与Meta对该产品的信心。

**Oakley Meta眼镜**作为新产品线于2025年7月开启预售，目前尚未公布具体用户数据，但预期将占据重要市场份额。

**为开发者提供哪些API？**

需明确区分VR/MR头显（如Meta Quest）与智能眼镜（如Ray-Ban Meta和Oakley Meta）的开发者支持差异。

**针对Meta Quest（VR/MR头显）：**

Meta为其Meta Horizon OS（前身为Quest OS）提供完善的开发者平台，包含多种API与SDK以创建沉浸式VR/混合现实体验，重点开发领域包括：

* **OpenXR**：构建高性能XR体验的开放标准，支持跨平台VR/MR应用开发
* **Meta Horizon Worlds**：在Meta社交VR平台内创建场景的配套工具
* **Android应用适配**：使现有Android应用兼容Meta Horizon OS并调用空间特性
* **网页开发**：设计可调用Quest多任务能力的2D网页应用
* **Meta Spatial SDK**：专为混合现实设计，助力2D应用升级空间交互功能
* **透视相机API**：实现虚拟与现实场景无缝融合的混合现实应用
* **交互API**：支持手势追踪、控制器输入、位移控制等功能
* **语音指令与文本转语音API**：为应用集成语音控制与语音输出
* **场景理解API**：获取用户物理环境数据（如场景网格、空间锚点）
* **社交功能API**：集成排行榜、挑战赛、用户通知等能力

**针对Ray-Ban Meta与Oakley Meta智能眼镜：**

目前尚未发布可供第三方开发者直接在该系列眼镜设备上构建定制应用的官方完整SDK或API。

但开发者已通过创新方式实现设备交互：

* **Meta AI集成**：主要交互途径是通过眼镜内置的**Meta AI**。开发者可结合现有大语言模型API与其他AI服务，调用Meta AI能力。例如已有社区项目通过Messenger桥接实现与眼镜的指令传输，再经由ChatGPT或Google Gemini等API处理数据
* **内容分享**：眼镜核心功能是拍摄与分享。开发者可通过**Meta View应用**（眼镜配套应用）提供内容分享通道，类似Instagram、Facebook、WhatsApp的内容流转模式
* **辅助功能**：内置Meta AI提供的环境描述、文本朗读等功能虽不直接开放API，但展现了未来通过更开放工具调用AI助手的可能性

尽管Meta已表明未来智能眼镜（如传闻中的"Orion"项目）将支持更开放开发的长期愿景，但当前Ray-Ban Meta与Oakley Meta智能眼镜的开发者接入仍主要依赖Meta AI集成与内容分享功能的间接调用。在缺乏专用设备端开发SDK的情况下，开发者社区正积极探索非官方集成方案。
