---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 思科交换机争论与批评
translated: true
type: note
---

问题：关于Cisco交换机，有哪些不受欢迎或有争议的观点？

回答：

许多网络工程师喜爱Cisco交换机，但一些不受欢迎的观点仍在论坛、Reddit (r/networking) 和私人Slack频道中反复出现。以下是最常见的一些“热门观点”，它们往往会招致反对或引发“口水战”：

- **Cisco不再是“最好”的企业级交换机，它只是最昂贵的安全选择。**
  Arista、Juniper (QFX/EX) 甚至白盒+ NOS (SONiC, Cumulus, Nvidia Spectrum) 在吞吐量、延迟、缓存和功耗效率方面，往往以相同的价格超越了可比较的Cisco Nexus或Catalyst型号。

- **与现代NOS相比，Cisco IOS/XE客观上已经过时且笨拙。**
  CLI停留在20世纪90年代，配置冗长且不一致，并且存在了十年的bug依然存在。人们认为Junos、Arista EOS甚至Nvidia Cumulus Linux更简洁、更不容易出错。

- **你主要是为Cisco的品牌和支持合同付费，而不是为了卓越的硬件。**
  Broadcom Trident/Tomahawk/Jericho ASIC驱动着几乎所有厂商（Cisco、Arista、Juniper、Dell等）。一旦剥离了软件和品牌，芯片是相同或非常相似的，但Cisco的收费却高出3-5倍。

- **Cisco的“DNA Center”和订阅许可（Smart Licensing/DNA Advantage）是赤裸裸的“抢钱”。**
  许多工程师觉得为了使用以前包含在“right-to-use”许可中的基本功能（OSPF、BGP、VXLAN），他们被锁定在循环付费中。

- **Catalyst 9000系列曾有过令人尴尬的硬件缺陷和静默数据损坏bug。**
  尤其是早期的9300/9500堆栈，存在字段通知问题（随机重启、QoS bug、TCAM耗尽等），花费数年才稳定下来——然而Cisco却将其宣传为“意图驱动网络革命”。

- **Cisco在园区/企业市场竞争中正在输给更便宜、更简单的竞争对手。**
  像Extreme、HPE Aruba、Huawei，甚至Ubiquiti Enterprise或TP-Link Omada等品牌，对于90%的中小型企业和园区部署来说“足够好”，而且成本只是Cisco的一小部分。

- **Cisco认证（CCNA/CCNP/CCIE）在实际的交换工作岗位中已变得在很大程度上无关紧要。**
  考试仍然严重侧重于传统的IOS命令，而大多数现代化公司运行Arista、Juniper或SDN叠加网络。许多招聘经理现在更看重非Cisco设备方面的实践经验。

- **NX-OS模式下的Nexus 9000是一个死胡同产品线。**
  ACI是Cisco唯一推崇的“未来”，但ACI过于复杂，并且在其他地方正在输给VMware NSX、Arista CVP或简单的EVPN/VXLAN。

这些观点在Cisco合作伙伴生态系统和培训公司内部肯定是不受欢迎的，但在过去5-10年部署过多厂商网络的工程师中却越来越普遍。
