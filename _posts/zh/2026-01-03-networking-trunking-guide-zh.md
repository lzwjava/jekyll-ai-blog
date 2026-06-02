---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 什么是网络中的中继技术？
translated: true
type: note
---

问题：在 <https://www.youtube.com/watch?v=bQ6D77QeMMg> 这个 YouTube 视频中讲了什么？

回答：

该视频是一个名为 **What is Trunking in Networking?** 的短篇教学解析视频，由 CBT Nuggets 频道于 2024 年 5 月 6 日上传。

视频由讲师 Jeremy 讲解计算机网络中 Trunking 的概念，特别是其与 VLANs (Virtual Local Area Networks) 的关系。以下是完整的口述转录稿（经过自动生成并为提高可读性进行了微调）：

“如果有人问我：‘Jeremy，关于 Trunking 我最应该了解的事情是什么？’ 我会这么回答：Trunking 允许你在设备之间传输多个 VLANs。因此，要真正理解 Trunking，你需要确保对 VLANs 有基础的了解。

VLANs 允许你将网络划分为多个子网络。也就是说，一个 VLAN 等于一个 Subnet。很多人忽略了这种关联感。VLAN 是 Layer 2 的概念——即在 Switching 层级——我们可以用它将网络分割成多个 Broadcast domains（广播域）。每当你这样做时，实际上你就在中间引入了一个 Router 或者一个 Routed network。这就是为什么 VLAN 等于 Subnet 是一个我们可以联系起来的逻辑概念，我们将 Layer 2 概念与 Layer 3 联系在了一起。

现在，如果我们只能在一个设备上划分 VLANs，那将是一个大问题——这会严重限制 Scalability（可扩展性）。所以我们所做的，是在 Switch 之间的所有链路上启用 Trunking（这实际上是一个 Cisco 术语）。

那么，这是否意味着我们的 VLANs 只能在 Cisco switches 之间传输？不，不是的。那是因为 Trunking 是一个行业标准，这就是为什么世界上其他所有人都把 Trunking 称为 ‘Tagging’。实际上我更喜欢这个词，而不是 ‘Trunking’ 这个词。

看，Cisco 是最早进入这个领域的，当时他们推出了 ISL (Inter-Switch Link) Trunking。这是在 Cisco switches 之间运行 VLANs 的能力。但显然，整个行业都会跟进——你有 HP，你有 Force10，你还有所有这些其他的 Switch 厂商：Juniper，以及其他我现在想不起来的厂商，但原因很充分。他们都跟上了，最终行业达成共识：‘我们需要一个行业标准的 802.1Q Trunking 协议。’ 现在它已经 100% 取代了 ISL。

所以现在有了 802.1Q，你就拥有了一种语言。当流量从你的设备移动时——假设我们这里有一个客户端连接到了 Wireless access point。他加入了 Public SSID，对吧？而你已经配置了你的 Wireless access points 对 Public 流量进行打标（Tag）。每当有人加入 Public 网络，假设他们会被打上 VLAN 10 的标签。

一旦流量进入 Switch 并通过链路出去以访问其他设备——如果是 Public 流量，你可能只限制它访问 Internet，对吧？——在那个 Packet 的最前面会得到一个小标签，上面写着：‘这属于 VLAN 10。’ 现在它就在最前面，这意味着所有不理解 VLANs 的设备都将无法处理该 Packet。它们会看着它说：‘啊，这里面有错误的数据。’

所以你所有的 Switches 都必须配置为支持 802.1Q Tagging 或 Trunking 方法，对吧？这就是 Trunk 的作用：允许你将这些带有标签的流量从一个设备传输到另一个设备。

如果你使用的是 Router-on-a-stick 设计——这是一个配置为使用 Subinterfaces（子接口）处理多个 VLANs 的 Router，对吧？——你实际上也会在 Switch 和 Router 之间配置一个 802.1Q Trunk。这在小型甚至很多中型企业中是非常常见的设计，因为 Routers 的连接速度一直在不断变快，对于 Internet 来说，它的工作效果非常好，对吧？

所以，当我称之为‘真正的 Trunking 协议’时，我并不是在演戏；我只是想说，当今世界支持的协议有且只有一个：802.1Q。

现在，请注意，我在这张图中加入了一台 Server，因为不仅仅是 Switches 支持 Trunking。你可以对 Server 做 Trunk，这意味着该 Server 可能正在运行 Virtualization（虚拟化）——也就是 VMware、Hyper-V 之类的东西——你可以在同一台设备上创建 Virtual machines 并将它们放在不同的 VLANs 中。

同样的情况：当你看到一台 IP phone 时，IP phone 实际上可以串联（Daisy-chain）一台电脑，你可以运行——我称之为 Mini-trunk。Cisco 可能不会同意我的说法；他们会说：‘不，那是 Voice VLAN。’ 但它就是一个 Mini-trunk。它是一个被限制的 Trunk，只允许 Voice VLAN 作为 Tagged VLAN。

所以当流量进入 Phone 时，Phone 会觉得：‘啊，我理解这个’，因为它能读取 802.1Q tags——因为电话很聪明，这就是它们的设计初衷。Untagged 流量来自电脑。所以这就像是运行到电话的一个非常小的 Trunk。这一切都是通过行业标准的 802.1Q 完成的。

‘假的’ Trunking 协议——你们中有些人可能还记得——实际上叫做 VTP。Cisco 创造了这个协议；不幸的是，他们将其命名为 VLAN Trunking Protocol。这多让人困惑啊？它本应该叫 VLAN Replication Protocol（VLAN 同步协议），因为它的作用是在 Switches 之间同步 VLANs 信息。

所以，看这里——让我清理一下屏幕。我写上 VTP。它是那个假的 Trunking 协议，对吧？当你在这些 Switches 上创建你想要的 VLAN 10, 20 和 30 时——你不需要在这里加一遍、在这里加一遍、再在这里加一遍——VTP 可以直接去同步它。

这就是它名字的来源：通过 Trunk links（干道链路）传播。所以如果你把它配置成了什么样的 Trunk？802.1Q Trunk，对吧？如果它被配置为一个真正的 Trunk，那么这个‘假的’ Trunking 协议 VTP 就可以同步 VLANs，让它们自动出现在下面的 Switches 上。

现在，这并不意味着 Ports（端口）会自动分配给 VLANs——那仍然是你和我的工作，对吧？我们还有活儿要干。我们必须去 Switch 上分配 Ports，但如果我们使用这个名为 VTP 的‘假’ Trunking 协议，我们就不用手动创建 VLANs 了——因为它根本不是一个 Trunking 协议；它是一个在 Trunk links 上运行的同步协议，对吧？

最后一件事：Dynamic Trunking Protocol——就是这个，DTP——是另一个 Cisco 的产物，旨在简化事情，但最终却让事情变得有点复杂，至少对于你和我记忆这些知识来说。

DTP 允许 Switches 自动协商并确定 Trunks，对吧？如果你使用 DTP，Switches 可以识别彼此，这允许它们说：‘嘿，我想成为一个 Trunk。’

这是因为 DTP 有两种主要模式：Auto 和 Desirable，对吧？我写下 Auto 和 Desire。Auto 模式就是坐在那里被动地等待有人尝试成为 Trunk。所以如果你所有的 Switch ports——假设所有这些端口都在 Auto 模式下——它就会说：‘嘿，我可以成为 Trunk。’ 这有点像‘如果你愿意，我就做，但我不会主动推进这件事’。如果你也不想成为 Trunk……”

（转录稿在结尾处略有中断，可能是因为视频结束了。）

总而言之，这段视频教授了 **Trunking**（特别是 802.1Q Tagging）是在交换机和其他设备之间扩展多个 VLANs 的标准方式，并将其与 Cisco 特有的功能如 VTP（VLAN 同步）和 DTP（自动 Trunk 协商）区分开来。

参考资料：

- [YouTube Video: What is Trunking in Networking?](https://www.youtube.com/watch?v=bQ6D77QeMMg)
