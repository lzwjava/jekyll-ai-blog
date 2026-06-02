---
audio: false
generated: true
lang: en
layout: post
title: Managing Dual SIM Traffic Routing on iOS with GFW Considerations
translated: false
type: note
---

iOS provides APIs that allow you to manage and separate network traffic for different cellular data plans when using Dual SIM functionality, but there are limitations, and direct control over routing specific traffic to specific SIMs based on the Great Firewall of China (GFW) restrictions is not natively supported at a granular level. However, with a combination of iOS APIs, manual configuration, and potentially third-party tools, you can achieve some level of separation for handling traffic differently for a Macao SIM and a China Telecom SIM. Below, I’ll outline the relevant APIs, configurations, and considerations, including how to address GFW-related challenges.

### Key iOS APIs and Features for Dual SIM and Traffic Management

1. **CoreTelephony Framework**:
   - **Purpose**: Provides access to cellular-related information and configuration for Dual SIM devices.
   - **Key Classes**:
     - `CTCellularPlanProvisioning`: Allows you to add or manage cellular plans (e.g., eSIM or physical SIM).
     - `CTTelephonyNetworkInfo`: Provides information about available cellular plans and their properties, such as the carrier name, mobile country code (MCC), and mobile network code (MNC).
     - `CTCellularData`: Monitors cellular data usage and network state (e.g., whether cellular data is enabled).
   - **Limitations**: CoreTelephony allows you to query and manage cellular plans but does not provide direct control over routing specific app traffic to a particular SIM. You can detect which SIM is active for data but cannot programmatically assign specific traffic (e.g., for a specific app or destination) to a SIM at the API level.

2. **NetworkExtension Framework**:
   - **Purpose**: Enables advanced network configuration, such as creating custom VPNs or managing network traffic rules.
   - **Key Features**:
     - **NEVPNManager**: Allows you to configure and manage VPN connections, which can be used to route traffic through a specific server to bypass GFW restrictions.
     - **NEPacketTunnelProvider**: For creating custom VPN tunnels, which can be configured to route specific traffic through a Macao SIM to avoid GFW restrictions.
   - **Use Case for GFW**: By setting up a VPN on the Macao SIM (which is not subject to GFW censorship, as Macao’s networks are independent), you can route traffic through a server outside mainland China to access blocked services like Google, WhatsApp, or YouTube.[](https://prepaid-data-sim-card.fandom.com/wiki/Macau)
   - **Limitations**: VPN configurations are typically applied at the system level, not per-SIM. You would need to manually switch the active data SIM or use a custom VPN solution to selectively route traffic.

3. **Dual SIM Configuration (Settings-Based)**:
   - iOS supports Dual SIM Dual Standby (DSDS) on compatible iPhones (e.g., iPhone XS, XR, or later purchased in regions like Macao or Hong Kong, which support Dual SIM with two nano-SIMs or eSIM). This allows you to:[](https://support.apple.com/en-us/109317)[](https://support.apple.com/en-us/108898)
     - Assign a default SIM for cellular data (Settings > Cellular > Cellular Data).
     - Enable “Allow Cellular Data Switching” to automatically switch between SIMs based on coverage or availability (Settings > Cellular > Cellular Data > Allow Cellular Data Switching).[](https://support.apple.com/en-us/108898)
     - Label SIMs (e.g., “Macao SIM” for unrestricted access, “China Telecom” for local services) and manually select which SIM handles data for specific tasks.
   - **Manual Traffic Separation**: You can manually switch the active data SIM in Settings to direct all cellular traffic through either the Macao SIM (to bypass GFW) or the China Telecom SIM (for local services subject to GFW). However, iOS does not provide an API to dynamically route traffic to a specific SIM based on app or destination without user intervention.

4. **Per-App VPN (NetworkExtension)**:
   - iOS supports per-app VPN configurations through the `NEAppProxyProvider` or `NEAppRule` classes in the NetworkExtension framework, typically used in enterprise settings (e.g., Managed App Configurations).
   - **Use Case**: You could configure a per-app VPN to route traffic from specific apps (e.g., YouTube, Google) through a VPN tunnel using the Macao SIM’s data connection to bypass GFW restrictions, while other apps use the China Telecom SIM for local services.
   - **Requirements**: This requires a custom VPN app or an enterprise Mobile Device Management (MDM) solution, which is complex to implement for individual developers. Additionally, you’d need to ensure the Macao SIM is set as the active data SIM when the VPN is in use.

5. **URLSession and Custom Networking**:
   - The `URLSession` API allows you to configure network requests with specific cellular interfaces using `allowsCellularAccess` or by binding to a specific network interface.
   - **Use Case**: You can programmatically disable cellular access for certain requests (forcing Wi-Fi or another interface) or use a VPN to route traffic. However, binding specific requests to a particular SIM’s cellular interface is not directly supported; you’d need to rely on the system’s active data SIM setting.
   - **Workaround**: Combine `URLSession` with a VPN configured to use the Macao SIM’s data to route traffic to servers outside China.

### Handling GFW Restrictions with Dual SIMs

The Great Firewall of China (GFW) blocks access to many foreign websites and services (e.g., Google, YouTube, WhatsApp) when using mainland Chinese carriers like China Telecom, as their traffic is routed through China’s censored infrastructure. In contrast, a Macao SIM (e.g., from CTM or Three Macao) routes traffic through Macao’s independent networks, which are not subject to GFW censorship (except for China Telecom Macao, which enforces GFW restrictions). Here’s how you can leverage this with a Macao SIM and a China Telecom SIM:[](https://www.getnomad.app/blog/do-esims-work-in-china)[](https://prepaid-data-sim-card.fandom.com/wiki/China)[](https://prepaid-data-sim-card.fandom.com/wiki/Macau)

1. **Macao SIM for Unrestricted Access**:
   - Use the Macao SIM as the default cellular data plan for apps or services blocked by the GFW (e.g., Google, YouTube).
   - **Configuration**:
     - Go to Settings > Cellular > Cellular Data and select the Macao SIM.
     - Ensure data roaming is enabled for the Macao SIM when in mainland China, as it will route traffic through Macao’s network, bypassing GFW.[](https://www.flyertalk.com/forum/china/2113715-sim-card-bypass-great-firewall.html)[](https://www.reddit.com/r/shanghai/comments/10c9fqc/can_phone_data_roaming_from_overseas_bypass_the/)
     - Optionally, configure a VPN (e.g., using `NEVPNManager`) to further secure traffic, though a Macao SIM typically doesn’t require a VPN to access blocked services.
   - **API Support**: Use `CTTelephonyNetworkInfo` to confirm the Macao SIM is active for data (`dataServiceIdentifier` property) and monitor its state.

2. **China Telecom SIM for Local Services**:
   - Use the China Telecom SIM for local apps and services (e.g., WeChat, Alipay) that require a Chinese phone number or are optimized for mainland networks.
   - **Configuration**:
     - Manually switch to the China Telecom SIM in Settings > Cellular > Cellular Data when accessing local services.
     - Be aware that traffic on this SIM will be subject to GFW restrictions, blocking access to many foreign sites unless a VPN is used.
   - **API Support**: Use `CTCellularData` to monitor cellular data usage and ensure the correct SIM is active. You can also use `NEVPNManager` to configure a VPN for specific apps to bypass GFW on the China Telecom SIM, though VPN reliability in China is inconsistent due to active blocking.[](https://www.flyertalk.com/forum/china/2113715-sim-card-bypass-great-firewall.html)

3. **Practical Workflow for Traffic Separation**:
   - **Manual Switching**: For simplicity, switch the active data SIM in Settings based on the task (e.g., Macao SIM for international apps, China Telecom SIM for local apps). This is the most straightforward approach but requires user intervention.
   - **VPN for China Telecom SIM**: If you need to access blocked services while using the China Telecom SIM, configure a VPN using `NEVPNManager`. Note that many VPNs (e.g., ExpressVPN, NordVPN) may be unreliable in China due to GFW blocking, so test providers like Astrill or custom solutions beforehand. Some eSIM providers (e.g., Holafly, ByteSIM) offer built-in VPNs that can be activated to bypass restrictions.[](https://www.flyertalk.com/forum/china/2113715-sim-card-bypass-great-firewall.html)[](https://www.reddit.com/r/chinalife/comments/1ebjcxi/can_you_use_esims_to_get_around_the_firewall/)[](https://esim.holafly.com/internet/mobile-internet-china/)
   - **Per-App VPN**: For advanced use, develop a custom app using `NEAppProxyProvider` to route specific app traffic through a VPN when the China Telecom SIM is active, while allowing other apps to use the Macao SIM directly.
   - **Automation Limitations**: iOS does not provide an API to programmatically switch the active data SIM based on app or destination URL. You’d need to rely on user-initiated SIM switching or a VPN to manage traffic routing.

### Steps to Implement Traffic Separation

1. **Set Up Dual SIM**:
   - Ensure your iPhone supports Dual SIM (e.g., iPhone XS or later with iOS 12.1 or later).[](https://support.apple.com/en-us/109317)
   - Insert the Macao SIM and China Telecom SIM (or configure an eSIM for one of them).
   - Go to Settings > Cellular, label the plans (e.g., “Macao” and “China Telecom”), and set the default data SIM (e.g., Macao for unrestricted access).[](https://support.apple.com/en-us/108898)

2. **Configure Cellular Data Settings**:
   - Disable “Allow Cellular Data Switching” to prevent automatic SIM switching, giving you manual control over which SIM is used for data (Settings > Cellular > Cellular Data > Allow Cellular Data Switching).[](https://support.apple.com/en-us/108898)
   - Use `CTTelephonyNetworkInfo` to programmatically verify which SIM is active for data in your app.

3. **Implement VPN for GFW Bypass**:
   - For the China Telecom SIM, configure a VPN using `NEVPNManager` or a third-party VPN app (e.g., Astrill, Holafly’s built-in VPN) to bypass GFW restrictions.
   - For the Macao SIM, a VPN may not be necessary, as its traffic is routed outside China’s censored infrastructure.[](https://prepaid-data-sim-card.fandom.com/wiki/Macau)[](https://www.reddit.com/r/shanghai/comments/10c9fqc/can_phone_data_roaming_from_overseas_bypass_the/)

4. **Monitor and Manage Traffic**:
   - Use `CTCellularData` to monitor cellular data usage and ensure the correct SIM is being used.
   - For advanced routing, explore `NEPacketTunnelProvider` to create a custom VPN that selectively routes traffic based on app or destination, though this requires significant development effort.

5. **Test and Optimize**:
   - Test connectivity in mainland China with both SIMs to ensure the Macao SIM bypasses GFW as expected and the China Telecom SIM works for local services.
   - Verify VPN performance on the China Telecom SIM, as GFW actively blocks many VPN protocols.[](https://www.flyertalk.com/forum/china/2113715-sim-card-bypass-great-firewall.html)

### Limitations and Challenges

- **No Native API for Dynamic SIM Routing**: iOS does not provide an API to dynamically route traffic to a specific SIM based on app, URL, or destination. You must manually switch the active data SIM or use a VPN to manage traffic.
- **GFW VPN Blocking**: The GFW actively blocks many VPN protocols (e.g., IPsec, PPTP), and even SSL-based VPNs may be rate-limited if detected. A Macao SIM is often more reliable for bypassing GFW without a VPN.[](https://www.flyertalk.com/forum/china/2113715-sim-card-bypass-great-firewall.html)
- **China Telecom SIM Restrictions**: China Telecom’s CDMA-based network may have compatibility issues with some foreign phones, though its LTE/5G network is more widely compatible. Additionally, its traffic is subject to GFW censorship, requiring a VPN for blocked services.[](https://esim.holafly.com/sim-card/china-sim-card/)[](https://yesim.app/blog/mobile-internet-and-sim-card-in-china/)
- **Real-Name Registration**: Both Macao and China Telecom SIMs may require real-name registration (e.g., passport details), which can complicate setup.[](https://prepaid-data-sim-card.fandom.com/wiki/Macau)[](https://prepaid-data-sim-card.fandom.com/wiki/China)
- **Performance**: Roaming on a Macao SIM in mainland China may result in slower speeds compared to a local China Telecom SIM, especially in rural areas.[](https://www.flyertalk.com/forum/china/2113715-sim-card-bypass-great-firewall.html)

### Recommendations

- **Primary Strategy**: Use the Macao SIM as the default cellular data plan for accessing blocked services, as it naturally bypasses GFW by routing traffic through Macao’s uncensored networks. Switch to the China Telecom SIM for local apps like WeChat or Alipay that require a Chinese number or are optimized for mainland networks.[](https://prepaid-data-sim-card.fandom.com/wiki/Macau)[](https://www.reddit.com/r/shanghai/comments/10c9fqc/can_phone_data_roaming_from_overseas_bypass_the/)
- **VPN as Backup**: For the China Telecom SIM, use a reliable VPN provider (e.g., Astrill, or eSIMs with built-in VPNs like Holafly or ByteSIM) to access blocked services. Pre-install and test the VPN before entering China, as downloading VPN apps in China may be restricted.[](https://esim.holafly.com/internet/mobile-internet-china/)[](https://bytesim.com/blogs/esim/mobile-internet-china)[](https://prepaid-data-sim-card.fandom.com/wiki/China)
- **Development Effort**: If you’re building an app, use `NetworkExtension` to implement a custom VPN for selective traffic routing, but note that this is complex and may require enterprise-level permissions. For most users, manual SIM switching combined with a VPN is sufficient.
- **Pre-Travel Setup**: Purchase and activate both SIMs (or eSIMs) before arriving in China, as local policies may restrict purchasing eSIMs in mainland China. For example, providers like Nomad or Holafly allow pre-purchase and activation of eSIMs with built-in GFW bypass.[](https://www.getnomad.app/blog/do-esims-work-in-china)[](https://www.getnomad.app/blog/do-esims-work-in-china)[](https://esim.holafly.com/internet/mobile-internet-china/)

### Example Code Snippet

Below is a basic example of using `CTTelephonyNetworkInfo` to check the active cellular plan and `NEVPNManager` to configure a VPN for the China Telecom SIM:

```swift
import CoreTelephony
import NetworkExtension

// Check active cellular plan
func checkActiveCellularPlan() {
    let networkInfo = CTTelephonyNetworkInfo()
    if let dataService = networkInfo.serviceCurrentRadioAccessTechnology {
        for (serviceIdentifier, rat) in dataService {
            print("Service: \(serviceIdentifier), Radio Access Technology: \(rat)")
            // Identify which SIM is active (e.g., Macao or China Telecom)
        }
    }
}

// Configure VPN for China Telecom SIM
func setupVPN() {
    let vpnManager = NEVPNManager.shared()
    vpnManager.loadFromPreferences { error in
        if let error = error {
            print("Failed to load VPN preferences: \(error)")
            return
        }

        let vpnProtocol = NEVPNProtocolIKEv2()
        vpnProtocol.serverAddress = "vpn.example.com" // Replace with your VPN server
        vpnProtocol.remoteIdentifier = "vpn.example.com"
        vpnProtocol.authenticationMethod = .certificate // Configure as needed

        vpnManager.protocolConfiguration = vpnProtocol
        vpnManager.isEnabled = true

        vpnManager.saveToPreferences { error in
            if let error = error {
                print("Failed to save VPN preferences: \(error)")
            } else {
                print("VPN configured successfully")
            }
        }
    }
}
```

### Conclusion

While iOS does not offer a native API to dynamically route traffic to specific SIMs based on app or destination, you can achieve traffic separation by:

1. Using the Macao SIM for unrestricted access to bypass GFW without a VPN.
2. Using the China Telecom SIM for local services, paired with a VPN (configured via `NEVPNManager` or a third-party app) to access blocked services.
3. Manually switching the active data SIM in Settings for different tasks.
4. Optionally, developing a custom VPN solution with `NetworkExtension` for per-app traffic routing, though this is complex.

For the simplest approach, rely on the Macao SIM for GFW-blocked services and switch to the China Telecom SIM for local needs, pre-installing a reliable VPN for the latter. Always test configurations before traveling to China, as GFW policies and VPN reliability can change rapidly.[](https://www.flyertalk.com/forum/china/2113715-sim-card-bypass-great-firewall.html)[](https://prepaid-data-sim-card.fandom.com/wiki/China)

If you need further clarification or assistance with specific API implementations, let me know!
