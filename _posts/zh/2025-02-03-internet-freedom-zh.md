---
audio: false
generated: false
image: true
lang: zh
layout: post
title: 追求互联网自由之旅
translated: true
type: post
---

### 目录

1. [中国的 Proxy 解决方案](#proxy-solutions-in-china)
   - 使用澳门 SIM 卡直接访问
   - 推荐高性价比的 proxy server 提供商
   - 为应用配置全局 routing 规则
   - 避免自行搭建 proxy server
   - 通过 proxy 切换 App Store 地区

2. [追求互联网自由之路](#the-journey-to-pursue-internet-freedom)
   - proxy 方法演进的时间线
   - 将对抗 GFW 比作近视康复
   - 当前配置使用多个 proxy servers
   - 基于速度自动选择 proxy
   - 后悔没有早点学习提供商的技术

3. [澳门 SIM 卡](#macau-sim-cards)
   - 中国电信 Easy+ SIM 卡详情
   - 大蓝卡 (Blue Macau SIM card) 预付费套餐
   - 各种日费和流量套餐
   - 需要兼容 4G 的设备
   - 无合约或取消费用

4. [Shadowsocks Proxy 问题](#shadowsocks-proxy-issues)
   - 特定网络下的连接问题
   - 5G 与 4G 的性能差异
   - 运营商策略可能会拦截 proxy 流量
   - Server 位置影响延迟
   - 使用不同 servers 进行排错

5. [跨越身份限制在任何平台注册](#registering-on-any-platform-regardless-of-identity)
   - 使用多个 email 账号进行注册
   - 通过在线服务租用电话号码
   - 通过 proxy 切换 Apple Store 地区
   - 中国 Visa 卡的支付限制
   - 中国身份文件有时会有所帮助


## 中国的 Proxy 解决方案

*2024.12.29*

* 最好的方法是办一张中国澳门的 SIM 卡，在需要时直接使用 cellular data。访问 [https://www.1888.com.mo](https://www.1888.com.mo)。大约 80 元人民币即可获得 10 GB 的 cellular data，提供快速且无痛的体验。

* 中国电信澳门 SIM 卡有两种：红卡和蓝卡。红卡提供日租计划，通常每天花费 2、3 或 5 澳门元。蓝卡提供流量包，例如 98 澳门元 10GB 或 198 澳门元 20GB，没有月租费。

* 如果你需要更多网络流量或经常使用笔记本电脑，可以考虑使用 [Falemon](https://falz.pics)。只需每月 30 元人民币即可访问约 15 个全球 proxy server。

* 在 iOS 上，配合 Shadowsocks 规则使用 Shadowrocket：[https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever)。配置全局 routing 以分离中国流量和海外流量。

* 在 Android 上，使用 V2Ray。在 Fire TV 上，使用 V2Ray 应用。在 Apple TV 上，使用 Shadowrocket 应用。在 Mac 上，使用 ShadowsocksX-NG 或 ClashX 应用。

* 不建议自己搭建 proxy server。像 Shadowsocks、VMess 或 Trojan 这样的协议很容易被封锁，无论使用什么 server。

* 要将 App Store 切换到美国地区，请开启全局 proxy (USA)，它会显示“None”的付款选项，从而允许你自由切换。

* 使用 Visa 卡从 Amazon 购买礼品卡，或使用 Apple 礼品卡门户为你的 App Store 账户充值。

---

## 追求互联网自由之路

*2025.02.03，本文最后更新于 2026 年 1 月。*

#### 历程

2010 年到 2013 年，我使用 Goagent 和 SwitchyOmega 插件来绕过 GFW。

2014 年到 2015 年间，我使用曲径 (Qujing) 进行 proxy，并在 Twitter 上关注了它的作者，他现在住在日本。

2016 年 6 月到 2018 年 7 月，我使用 Digital Ocean 托管自己的 shadowsocks proxy server。

从 2019 年开始，我开始使用 https://zhs.cloud。

2023 年 3 月，我开始在手机中使用澳门 SIM 卡上网，无需 proxy 或 VPN。每月花费约 150 元人民币购买 20GB cellular data，这种方法我用了大约一年。

2024 年，我重新开始使用 Outline Manager 配合自己的 shadowsocks proxy server，并尝试了各种云服务商。

2025 年 2 月，我首选的配置是 Outline Manager 配合阿里云香港 server 进行日常使用，以及一个非香港 server（如新加坡或日本）用于 AI 工具。我保持着与 Shadowrocket 或 Clash 相同的 proxy rules 配置。

2025 年 6 月起，我开始在笔记本电脑上使用 Python 脚本，根据 speed test 结果每 10 分钟自动选择一个 proxy server。该脚本在使用 AI 工具时会优先选择新加坡 server 而非香港 server。更多详情请查看 [Automating Clash Proxy Management](/clash-en)。对于 VPN 云服务商，我仍然使用 https://zhs.cloud。

此外，在 iOS 上，我切回了使用澳门 SIM 卡，每月 20GB 流量花费 150 元人民币。我还三次以每次 20 MOP 的价格额外购买了 5GB 流量，手机流量总计花费约 200 元人民币换取 35GB 数据。

从 2025 年 10 月中旬开始，我停止了澳门 SIM 卡套餐，因为最近几个月我每月使用约 35 GB。使用中国应用会消耗 cellular data，这些应用约占我流量使用的三分之一——主要是微信。

我重新开始使用 iOS Shadowsocks 应用配合来自 https://zhs.cloud 的 proxy servers。并开始学习一些关于 CN2 线路的知识。

从 12 月底开始，由于对 proxy server 的挫败感，我重新开始在手机中使用澳门 SIM 卡。

从 2026 年 1 月开始，我开始使用 [Falemon](https://falz.pics)。一位朋友推荐了它。


#### 与近视康复的区别

一个挑战是对抗 GFW，这是人为的。另一个是应对眼部肌肉功能的原理。

测量 proxy 解决方案的有效性很容易。然而，康复近视需要时间来确定眼球是否在发生变化。

#### 与近视康复的相似之处

相似之处在于，proxy 解决方案和减少 200 度的眼镜通常都很有效。一个是关于访问互联网，另一个是关于改善视力。两者都解决了非常重要的问题。

底层原理是，如果我们了解 GFW 的工作原理并找到绕过它的方法，解决方案应该是直接的。

#### 推理与细微差别

我仍然不完全了解 GFW 的工作原理。当我的 proxy server IP 被封锁时，我现在有更多方法来调查原因。

我可以检查封锁是发生在 cellular network 还是家庭宽带上。如果是 cellular network，我可以检查是在 4G 还是 5G 上。

同样，如果我的近视在半年或一年后没有改善，我需要调查双眼之间是否存在差异。我还需要考虑，在这一年的大部分时间里，我是否在不费力的情况下勉强看清东西。

#### 当前状态

我的 proxy server 目前运行非常好。连接到香港 proxy server 时，手机上的下载速度达到 80 Mbps，上传速度达到 50 Mbps。笔记本电脑上也是如此。

我在笔记本电脑和手机上使用相同的 proxy 配置，它们运行完美。通常，我使用 proxy server 访问中国以外的网站，使用非香港 server 访问 AI 工具。

#### 恢复

如果连接断了，我的恢复方法很简单。我只需要更改阿里云香港 proxy server 的弹性 IP，并将新的 proxy URL 上传到云存储。这意味着我需要运行两个脚本，耗时约 1 分钟，我的笔记本电脑和手机就可以更新 proxy server 地址了。

#### 遗憾

我与 GFW 斗争了太多次，花费了太多时间。我尝试过许多 proxy 协议，明知它们会被 GFW 检测到并被封禁。如果没有可靠的 proxy server，很难在 OpenWrt 路由器上设置 proxy。

我遗憾的一件事是没有早点学习 proxy 提供商的技术，比如 [zhs.cloud](https://zhs.cloud)。我现在了解了他们大部分的秘密。

另一件事是，每当我的 proxy server 被封时，我都没有深入思考。似乎你只需要设置一个新的 proxy server 来获取一个未被封禁的新 IP 地址。但那是浅层思考。

#### 指标

我很遗憾没有早点使用 Speedtest。我很早以前就知道这个工具的名字，但我没有仔细学习如何使用它。

在连接到 5G 或 4G 移动基站或家庭宽带网络时，经常使用 Speedtest 是很有好处的。

对于近视康复也是一样。我买了一个 C 字视力表和一个标准视力表。

没有测量，就没有改进。测量事物有助于学习。经常使用 Speedtest 帮我发现，在 5G 网络上，速度很容易超过 100 Mbps，而在家庭宽带网络上，很难超过 100 Mbps。

#### 现在还为时尚早

GFW 墙会在未来几年倒塌吗？很难说。

当我在康复近视两年后，我告诉朋友我的康复方法需要改进，我需要佩戴比实际度数低 200 度的眼镜，而不是低 150 度。

他说没问题，这很好，不是浪费时间，而且现在还早。是的。这些事情是基础。就像近视一样，人们应该早点发现它。Todd Becker 于 2014 年在 YouTube 上分享了这一发现，视频获得了超过 100 万次观看。现在是 2025 年，世界上有多少人真正知道它？我猜不到 1 万人。


---

## 澳门 SIM 卡

*2023.04.20*

#### 我的澳门 SIM 卡使用经验

在 2023 年周末访问澳门期间，我买了一张中国电信 Easy+ SIM 澳门卡。到达广州后，我发现它仍然可以完美工作，帮助我学习英语和下载许多国外应用。感觉就像还在澳门一样。我强烈推荐它。后来，我尝试了蓝卡，也很不错。以下是两者的简要概述：

#### 中国电信 Easy+ SIM 卡

随时随地轻松使用！

### 关键点
- 无需押金；中国内地、澳门和香港自动激活。
- 无合约或取消费用；购买后即可使用。
- 包含澳门号码；可选配中国内地号码实现双号使用。
- 在线或使用增值卡充值。

### 日费选项
- $2/天：4GB 高速流量，之后降速无限量；5,000 分钟本地通话。
- $3/天：10GB 高速流量，之后降速无限量；5,000 分钟本地通话。
- $5/天：20GB 高速流量，之后降速无限量；5,000 分钟本地通话。

### 其他
- 香港数据使用：$0.1/MB。
- 随时通过发送短信更改套餐。

#### 蓝卡 (Blue Macau SIM Card)

### 关键点
- 无月租；按需付费。
- 本地通话：0.39 MOP/分钟；上网：0.1 MOP/MB；短信：1 MOP/条。
- 可选无有效期数据包：98 MOP 10GB，188 MOP 20GB，288 MOP 40GB。
- 每 180 天充值一次以保持激活状态。

#### 兼容设备

- 需要 4G 全网通或支持中国电信的手机。

欲了解更多信息，请访问 [中国电信澳门](https://www.1888.com.mo/)。

---

你也可以在淘宝上找到这些：

<div align="center"><img src="/assets/images/macao/easy.jpg" width="300px" /><img/></div>

---

## Shadowsocks Proxy 问题

*2025.01.03*

智维：

我和朋友出去烧烤，使用 Shadowsocks 配合新加坡 server 作为 proxy 来绕过 GFW。在室外使用 5G 时，我无法连接，尝试访问 YouTube 时测试超时。但是，当我回到家使用 4G 或我的中国电信家庭网络时，Shadowsocks 运行正常。为什么会发生这种情况？

Mistral：

听起来你在室外使用 5G 时遇到了 Shadowsocks proxy 的连接问题，但在使用 4G 或家庭网络时没有问题。可能有以下几个原因：

1. 网络配置差异：
   - 5G 网络：与 4G 相比，5G 网络可能具有不同的配置或限制。某些运营商可能针对 5G 设置了更严格的防火墙规则或不同的网络 routing，这可能会影响 Shadowsocks proxy 的性能。
   - 4G 网络：4G 网络可能设置较宽松或具有更好的 routing，允许你的 Shadowsocks proxy 正常运行。

2. ISP 限制：
   - 运营商策略：不同运营商对于使用 VPN 或 proxy 可能有不同的策略。你的 5G 运营商可能有更严格的策略来封锁或限制 VPN 流量，包括 Shadowsocks。
   - 家庭网络：你的家庭网络由中国电信提供，可能限制较少，允许 Shadowsocks 无障碍运行。

3. 信号强度与稳定性：
   - 5G 信号：5G 信号的稳定性和强度可能会有所波动，尤其是在户外环境。信号弱或不稳定会导致连接问题，包括超时。
   - 4G 信号：4G 信号可能更稳定一致，为你的 Shadowsocks proxy 提供更好的连接。

4. Proxy Server 位置：
   - 新加坡 Server：位于新加坡的 Shadowsocks server 可能会影响延迟和连通性。与 4G 网络或家庭网络相比，5G 网络到新加坡 server 的延迟可能更高或 routing 不太理想。

5. 设备设置：
   - 配置：确保你的设备设置已正确配置以使用 Shadowsocks。有时，切换网络（从 5G 到 4G 或家庭 Wi-Fi）会导致设置重置或更改。
   - 应用权限：确保 Shadowsocks 应用拥有在不同网络上运行的必要权限。

### 排错步骤：

1. 检查网络设置：
   - 确保 Shadowsocks 设置在 5G 和 4G 网络下均已正确配置。
   - 验证你的 5G 网络上没有可能拦截 proxy 的特定限制或设置。

2. 测试不同 Servers：
   - 尝试连接到不同的 Shadowsocks servers，看问题是否仅针对新加坡 server。
   - 检查到该 server 的延迟和连接稳定性。

3. 联系你的运营商：
   - 如果问题持续存在，请咨询你的 5G 运营商，了解是否存在任何可能影响 Shadowsocks 连接的限制或设置。

4. 更新软件：
   - 确保你的 Shadowsocks 应用和设备软件均为最新版本。有时，更新可以解决连接问题。

5. 使用替代 Proxy：
   - 考虑使用备用的 proxy 服务或 VPN，它们可能与你的 5G 网络有更好的兼容性。

通过系统地检查这些因素，你应该能够找出连接问题的原因并找到合适的解决方案。

-- 

更新：

实际上，我的家庭 Wi-Fi 使用的是中国移动，其地址类似于 120.235.8.xx。

有趣的是，我观察到了不一致的连接模式——虽然我的 proxy server 在 cellular data 和中国电信网络上运行正常，但在使用我的家庭 Wi-Fi 网络时偶尔会无法连接。



---

## 跨越身份限制在任何平台注册

我是一名中国公民，也是一名关注最新技术的软件工程师。看到许多产品禁止中国访问令人沮丧。虽然我还在攻读副学士学位，并希望将来能在海外工作，但我仍会在中国待上几年。在此期间，我想分享一些基于国籍克服互联网障碍的信息。

#### Email

拥有多个 email 账户会更好。Claude 因为 VPN 访问封禁了我的 Gmail，所以我注册了一个新的 Outlook email，结果运行良好。

#### 电话号码

通过 [http://sms-activate.org](http://sms-activate.org)，可以租用电话号码进行注册。但问题是，用这类号码注册的账号可能存在一定风险。

在中国，我个人推荐使用 [https://www.1888.com.mo](https://www.1888.com.mo) 办理一张中国电信澳门卡。我也尝试过 Giffgaff（英国 SIM 卡），最近还订购了一张 PayGo T-Mobile（美国 SIM 卡）。

#### Apple Store 地区

要将 App Store 切换到美国地区，请开启全局 proxy (USA)，它会显示“None”的付款选项，允许你自由切换。

你可以使用 Visa 卡从 Amazon 购买礼品卡，或者使用 Apple 礼品卡门户为你的 App Store 账户充值。

同样的方法也适用于新加坡或其他地区。

#### 支付

拥有一张 Visa 卡很方便。但是，中国发行的 Visa 卡仍然受到一些限制。例如，Anthropic 或 OpenAI 不接受中国发行的 Visa 卡。

#### VPN

你可能想查看 [中国的 Proxy 解决方案](./proxy-en) 和 [搭建你的 Proxy Server](./diy-proxy-en)。

#### 身份

我有中国居民身份证和护照，这在某些情况下会有所帮助。