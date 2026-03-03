---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HDLC 正常响应模式详解
translated: true
type: note
---

问题：在 HDLC 中，由主站启动传输过程，从站只有在收到主站的命令帧后才能作为响应向主站传输信息的操作模式称为

A. Normal Response Mode  
B. Asynchronous Response Mode  
C. Asynchronous Balanced Mode  
D. Synchronous Balanced Mode  

您的答案：B  
正确答案：A  

答案：  

正确答案是 **A. Normal Response Mode (NRM)**。

### 解释：

HDLC (High-level Data Link Control) 定义了三种主要的操作模式：

- **Normal Response Mode (NRM)**  
  - 主站 (primary station) 对链路具有完全控制权。  
  - 只有主站才能启动数据传输。  
  - 从站 (secondary station) 未经主站明确轮询或命令，不得传输任何内容。  
  - 在收到命令帧（特别是设置了 poll bit 的帧）后，从站可以响应一个或多个帧。  
  - 如果响应多个帧，最后一帧必须设置 final bit (F-bit)。  
  - 此模式与问题描述**完全匹配**：  
    > “传输过程由主站启动，从站只有收到主站某个命令帧后，才能作为响应向主站传输信息。”

- **Asynchronous Response Mode (ARM)**  
  - 从站可以随时启动传输，无需等待主站许可（asynchronous 表示无需持续轮询）。  
  - 这与问题描述的行为相反。

- **Asynchronous Balanced Mode (ABM)**  
  - 两站平等（balanced 配置）。  
  - 任一站均可随时启动传输。  
  - 常用于点对点全双工链路（例如，modem 连接、X.25 中的 LAPB）。  
  - 明显不符合问题描述。

- **Synchronous Balanced Mode**  
  - 这不是标准的 HDLC 模式名称。

因此，问题给出的描述是 **Normal Response Mode (NRM)** 的教科书定义。

您选择的 B (Asynchronous Response Mode) 是错误的，因为在 ARM 中，从站可以自发发送数据，而无需首先收到主站的命令帧。

参考文献：  

- HDLC 协议标准 (ISO 13239 / ITU-T Recommendation)  
- 大多数计算机网络教科书（例如，Tanenbaum、Kurose & Ross、Forouzan）对 NRM 的描述与问题引用完全一致。