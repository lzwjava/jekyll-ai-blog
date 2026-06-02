---
audio: false
generated: true
lang: zh
layout: post
title: iOS双卡手机GFW环境下的流量路由管理
translated: true
type: note
---

iOS 提供了相关 API，允许您在使用双卡功能时管理和区分不同蜂窝数据套餐的网络流量，但也存在一些限制。系统并不原生支持基于中国防火墙（GFW）限制的粒度化控制，无法直接将特定流量路由到特定 SIM 卡。然而，通过结合使用 iOS API、手动配置以及可能的第三方工具，您可以实现一定程度的流量分离，以区别对待澳门 SIM 卡和中国电信 SIM 卡的流量。下面，我将概述相关的 API、配置和注意事项，包括如何应对与 GFW 相关的挑战。

### 用于双卡和流量管理的关键 iOS API 和功能

1. **CoreTelephony 框架**：
    - **目的**：提供对蜂窝相关信息和双卡设备配置的访问。
    - **关键类**：
      - `CTCellularPlanProvisioning`：允许您添加或管理蜂窝套餐（例如 eSIM 或物理 SIM 卡）。
      - `CTTelephonyNetworkInfo`：提供有关可用蜂窝套餐及其属性的信息，例如运营商名称、移动国家代码（MCC）和移动网络代码（MNC）。
      - `CTCellularData`：监控蜂窝数据使用情况和网络状态（例如，蜂窝数据是否启用）。
    - **限制**：CoreTelephony 允许您查询和管理蜂窝套餐，但不提供对特定应用流量路由到特定 SIM 卡的直接控制。您可以检测哪个 SIM 卡是活跃的数据卡，但无法在 API 级别以编程方式将特定流量（例如，针对特定应用或目的地）分配给某个 SIM 卡。

2. **NetworkExtension 框架**：
    - **目的**：支持高级网络配置，例如创建自定义 VPN 或管理网络流量规则。
    - **关键特性**：
      - **NEVPNManager**：允许您配置和管理 VPN 连接，可用于通过特定服务器路由流量以绕过 GFW 限制。
      - **NEPacketTunnelProvider**：用于创建自定义 VPN 隧道，可以配置为通过澳门 SIM 卡路由特定流量以避免 GFW 限制。
    - **GFW 使用场景**：通过在澳门 SIM 卡上设置 VPN（澳门网络独立，不受 GFW 审查影响），您可以通过中国大陆以外的服务器路由流量，以访问被屏蔽的服务，如 Google、WhatsApp 或 YouTube。
    - **限制**：VPN 配置通常在系统级别应用，而不是按 SIM 卡应用。您需要手动切换活跃的数据 SIM 卡或使用自定义 VPN 解决方案来选择性路由流量。

3. **双卡配置（基于设置）**：
    - iOS 在兼容的 iPhone 上支持双卡双待（DSDS）（例如，在澳门或香港等地区购买的 iPhone XS、XR 或更新型号，支持双 nano-SIM 卡或 eSIM）。这允许您：
      - 为蜂窝数据分配默认 SIM 卡（设置 > 蜂窝网络 > 蜂窝数据）。
      - 启用“允许蜂窝数据切换”以根据覆盖范围或可用性自动在 SIM 卡之间切换（设置 > 蜂窝网络 > 蜂窝数据 > 允许蜂窝数据切换）。
      - 标记 SIM 卡（例如，“澳门 SIM 卡”用于无限制访问，“中国电信”用于本地服务）并手动选择哪个 SIM 卡处理特定任务的数据。
    - **手动流量分离**：您可以在设置中手动切换活跃的数据 SIM 卡，将所有蜂窝流量导向澳门 SIM 卡（以绕过 GFW）或中国电信 SIM 卡（用于受 GFW 限制的本地服务）。然而，iOS 不提供 API 来基于应用或目的地在无需用户干预的情况下动态地将流量路由到特定 SIM 卡。

4. **按应用 VPN (NetworkExtension)**：
    - iOS 通过 NetworkExtension 框架中的 `NEAppProxyProvider` 或 `NEAppRule` 类支持按应用 VPN 配置，通常用于企业环境（例如，托管应用配置）。
    - **使用场景**：您可以配置一个按应用 VPN，将特定应用（例如 YouTube、Google）的流量通过使用澳门 SIM 卡数据连接的 VPN 隧道路由，以绕过 GFW 限制，而其他应用则使用中国电信 SIM 卡进行本地服务。
    - **要求**：这需要自定义 VPN 应用或企业移动设备管理（MDM）解决方案，对于独立开发者来说实现起来比较复杂。此外，您需要确保在使用 VPN 时将澳门 SIM 卡设置为活跃的数据 SIM 卡。

5. **URLSession 和自定义网络**：
    - `URLSession` API 允许您使用 `allowsCellularAccess` 或通过绑定到特定网络接口来配置具有特定蜂窝接口的网络请求。
    - **使用场景**：您可以以编程方式禁用某些请求的蜂窝访问（强制使用 Wi-Fi 或其他接口），或使用 VPN 来路由流量。然而，不支持将特定请求绑定到特定 SIM 卡的蜂窝接口；您需要依赖系统的活跃数据 SIM 卡设置。
    - **变通方法**：将 `URLSession` 与配置为使用澳门 SIM 卡数据的 VPN 结合使用，以将流量路由到中国境外的服务器。

### 使用双卡处理 GFW 限制

中国防火墙（GFW）在使用中国大陆运营商（如中国电信）时会屏蔽许多国外网站和服务（例如 Google、YouTube、WhatsApp），因为它们的流量经过中国的审查基础设施。相比之下，澳门 SIM 卡（例如来自 CTM 或 3 Macao）的流量通过澳门独立的网络路由，不受 GFW 审查（除了中国电信澳门，其强制执行 GFW 限制）。以下是您如何利用澳门 SIM 卡和中国电信 SIM 卡的方法：

1. **澳门 SIM 卡用于无限制访问**：
    - 将对被 GFW 屏蔽的应用或服务（例如 Google、YouTube）的默认蜂窝数据套餐设置为澳门 SIM 卡。
    - **配置**：
      - 前往设置 > 蜂窝网络 > 蜂窝数据，选择澳门 SIM 卡。
      - 在中国大陆时，确保为澳门 SIM 卡启用数据漫游，因为它将通过澳门网络路由流量，绕过 GFW。
      - （可选）配置 VPN（例如使用 `NEVPNManager`）以进一步保护流量，尽管澳门 SIM 卡通常不需要 VPN 即可访问被屏蔽的服务。
    - **API 支持**：使用 `CTTelephonyNetworkInfo` 确认澳门 SIM 卡是活跃的数据卡（`dataServiceIdentifier` 属性）并监控其状态。

2. **中国电信 SIM 卡用于本地服务**：
    - 将中国电信 SIM 卡用于需要中国电话号码或针对大陆网络优化的本地应用和服务（例如微信、支付宝）。
    - **配置**：
      - 在访问本地服务时，手动在设置 > 蜂窝网络 > 蜂窝数据中切换到中国电信 SIM 卡。
      - 请注意，此 SIM 卡上的流量将受到 GFW 限制，除非使用 VPN，否则许多国外网站将被屏蔽。
    - **API 支持**：使用 `CTCellularData` 监控蜂窝数据使用情况并确保正确的 SIM 卡处于活跃状态。您也可以使用 `NEVPNManager` 为特定应用配置 VPN，以在中国电信 SIM 卡上绕过 GFW，尽管由于主动屏蔽，VPN 在中国的可靠性不稳定。

3. **流量分离的实用工作流程**：
    - **手动切换**：为简化操作，根据任务在设置中切换活跃的数据 SIM 卡（例如，国际应用用澳门 SIM 卡，本地应用用中国电信 SIM 卡）。这是最直接的方法，但需要用户干预。
    - **中国电信 SIM 卡的 VPN**：如果您需要在使用中国电信 SIM 卡时访问被屏蔽的服务，请使用 `NEVPNManager` 配置 VPN。请注意，由于 GFW 屏蔽，许多 VPN（例如 ExpressVPN、NordVPN）在中国可能不可靠，因此请事先测试像 Astrill 或自定义解决方案这样的提供商。一些 eSIM 提供商（例如 Holafly、ByteSIM）提供内置 VPN，可以激活以绕过限制。
    - **按应用 VPN**：对于高级用途，开发一个使用 `NEAppProxyProvider` 的自定义应用，以在中国电信 SIM 卡活跃时通过 VPN 路由特定应用流量，同时允许其他应用直接使用澳门 SIM 卡。
    - **自动化限制**：iOS 不提供 API 来基于应用或目标 URL 以编程方式切换活跃的数据 SIM 卡。您需要依赖用户发起的 SIM 卡切换或 VPN 来管理流量路由。

### 实现流量分离的步骤

1. **设置双卡**：
    - 确保您的 iPhone 支持双卡（例如，iPhone XS 或更新型号，搭载 iOS 12.1 或更高版本）。
    - 插入澳门 SIM 卡和中国电信 SIM 卡（或为其中之一配置 eSIM）。
    - 前往设置 > 蜂窝网络，标记套餐（例如“澳门”和“中国电信”），并设置默认数据 SIM 卡（例如，澳门用于无限制访问）。

2. **配置蜂窝数据设置**：
    - 禁用“允许蜂窝数据切换”以防止自动 SIM 卡切换，从而手动控制哪个 SIM 卡用于数据（设置 > 蜂窝网络 > 蜂窝数据 > 允许蜂窝数据切换）。
    - 在您的应用中使用 `CTTelephonyNetworkInfo` 以编程方式验证哪个 SIM 卡是活跃的数据卡。

3. **实施用于 GFW 绕过的 VPN**：
    - 对于中国电信 SIM 卡，使用 `NEVPNManager` 或第三方 VPN 应用（例如 Astrill、Holafly 的内置 VPN）配置 VPN 以绕过 GFW 限制。
    - 对于澳门 SIM 卡，可能不需要 VPN，因为其流量经过中国审查基础设施之外的路由。

4. **监控和管理流量**：
    - 使用 `CTCellularData` 监控蜂窝数据使用情况，并确保使用了正确的 SIM 卡。
    - 对于高级路由，探索使用 `NEPacketTunnelProvider` 创建自定义 VPN，以基于应用或目的地选择性路由流量，尽管这需要大量的开发工作。

5. **测试和优化**：
    - 在中国大陆测试两张 SIM 卡的连接性，确保澳门 SIM 卡能按预期绕过 GFW，并且中国电信 SIM 卡能用于本地服务。
    - 验证中国电信 SIM 卡上的 VPN 性能，因为 GFW 会主动屏蔽许多 VPN 协议。

### 限制与挑战

- **无动态 SIM 卡路由的原生 API**：iOS 不提供基于应用、URL 或目的地动态路由流量到特定 SIM 卡的 API。您必须手动切换活跃的数据 SIM 卡或使用 VPN 来管理流量。
- **GFW 对 VPN 的屏蔽**：GFW 主动屏蔽许多 VPN 协议（例如 IPsec、PPTP），即使是基于 SSL 的 VPN 如果被检测到也可能受到速率限制。澳门 SIM 卡通常无需 VPN 即可更可靠地绕过 GFW。
- **中国电信 SIM 卡限制**：中国电信基于 CDMA 的网络可能与某些国外手机存在兼容性问题，尽管其 LTE/5G 网络兼容性更广。此外，其流量受到 GFW 审查，访问被屏蔽服务需要 VPN。
- **实名登记**：澳门和中国电信 SIM 卡都可能需要实名登记（例如，护照详细信息），这可能会使设置复杂化。
- **性能**：在中国大陆使用澳门 SIM 卡漫游可能导致速度较慢，尤其是在农村地区，与本地中国电信 SIM 卡相比。

### 建议

- **主要策略**：将澳门 SIM 卡用作访问被屏蔽服务的默认蜂窝数据套餐，因为它通过澳门未经审查的网络自然绕过 GFW。对于需要中国电话号码或针对大陆网络优化的本地应用（如微信或支付宝），切换到中国电信 SIM 卡。
- **VPN 作为备用**：对于中国电信 SIM 卡，使用可靠的 VPN 提供商（例如 Astrill，或带有内置 VPN 的 eSIM，如 Holafly 或 ByteSIM）来访问被屏蔽的服务。在进入中国之前预安装并测试 VPN，因为在中国下载 VPN 应用可能受到限制。
- **开发工作**：如果您正在构建应用，请使用 `NetworkExtension` 来实现用于选择性流量路由的自定义 VPN，但请注意这很复杂，并且可能需要企业级权限。对于大多数用户来说，手动 SIM 卡切换结合 VPN 就足够了。
- **出行前设置**：在抵达中国之前购买并激活两张 SIM 卡（或 eSIM），因为当地政策可能限制在中国大陆购买 eSIM。例如，像 Nomad 或 Holafly 这样的提供商允许预购和激活带有内置 GFW 绕过功能的 eSIM。

### 代码示例

以下是使用 `CTTelephonyNetworkInfo` 检查活跃蜂窝套餐和使用 `NEVPNManager` 为中国电信 SIM 卡配置 VPN 的基本示例：

```swift
import CoreTelephony
import NetworkExtension

// 检查活跃蜂窝套餐
func checkActiveCellularPlan() {
    let networkInfo = CTTelephonyNetworkInfo()
    if let dataService = networkInfo.serviceCurrentRadioAccessTechnology {
        for (serviceIdentifier, rat) in dataService {
            print("服务: \(serviceIdentifier), 无线电接入技术: \(rat)")
            // 识别哪个 SIM 卡是活跃的（例如，澳门或中国电信）
        }
    }
}

// 为中国电信 SIM 卡配置 VPN
func setupVPN() {
    let vpnManager = NEVPNManager.shared()
    vpnManager.loadFromPreferences { error in
        if let error = error {
            print("加载 VPN 偏好设置失败: \(error)")
            return
        }

        let vpnProtocol = NEVPNProtocolIKEv2()
        vpnProtocol.serverAddress = "vpn.example.com" // 替换为您的 VPN 服务器
        vpnProtocol.remoteIdentifier = "vpn.example.com"
        vpnProtocol.authenticationMethod = .certificate // 根据需要配置

        vpnManager.protocolConfiguration = vpnProtocol
        vpnManager.isEnabled = true

        vpnManager.saveToPreferences { error in
            if let error = error {
                print("保存 VPN 偏好设置失败: \(error)")
            } else {
                print("VPN 配置成功")
            }
        }
    }
}
```

### 结论

虽然 iOS 不提供基于应用或目的地动态路由流量到特定 SIM 卡的原生 API，但您可以通过以下方式实现流量分离：

1. 使用澳门 SIM 卡进行无限制访问，无需 VPN 即可绕过 GFW。
2. 使用中国电信 SIM 卡进行本地服务，并配合 VPN（通过 `NEVPNManager` 或第三方应用配置）以访问被屏蔽的服务。
3. 为不同的任务在设置中手动切换活跃的数据 SIM 卡。
4. （可选）使用 `NetworkExtension` 开发自定义 VPN 解决方案以进行按应用流量路由，尽管这很复杂。

对于最简单的方法，依赖澳门 SIM 卡访问被 GFW 屏蔽的服务，并切换到中国电信 SIM 卡满足本地需求，同时为后者预装可靠的 VPN。由于 GFW 政策和 VPN 可靠性可能迅速变化，请务必在前往中国之前测试配置。

如果您需要关于特定 API 实现的进一步说明或帮助，请告诉我！
