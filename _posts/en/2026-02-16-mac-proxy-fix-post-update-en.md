---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mac Proxy Fix After Update
translated: false
type: note
---

Question: My MacBook Air M2 is stuck after restart showing "software update complete", but I fixed the initial hang by temporarily disabling Wi-Fi. Now during startup there's no network, the system update/ setup window asks to choose Ethernet or no network. I chose no network and it proceeded to the welcome screen. In the installer log (via Options), I see fetch URL errors, confirming it's a network proxy issue because Clash set system proxies but isn't running yet.

Answer: 

Great news—you’ve already passed the critical stuck point! By choosing "no network" (or offline setup), macOS Tahoe setup skips the parts that require internet (like iCloud sign-in, App Store activation, or final update fetches) and lets you reach the desktop/Welcome screen anyway. This is a standard workaround when network configuration is broken (in your case, leftover Clash system proxy settings preventing connections to Apple's servers).

The fetch URL errors in the installer log are exactly what we expected: during the post-update phase, macOS tries to download small configuration files, fonts, or completion data from domains like mesu.apple.com, gdmf.apple.com, or swcdn.apple.com, but the invalid proxy (127.0.0.1:7890 or similar) causes timeouts or connection refusals.

### Next Steps to Fully Resolve and Restore Normal Networking

1. **Finish the Setup Offline**  
   - Continue through the Welcome / Setup Assistant screens (language, region, Apple ID sign-in can be skipped for now if it asks—choose "Set Up Later").  
   - You should reach the desktop soon.

2. **Once on the Desktop – Immediately Disable All System Proxies**  
   Open **System Settings** > **Network** > select **Wi-Fi** (or your interface) > **Details…** (or Advanced…) > **Proxies** tab:  
   - Uncheck / turn **off** all four options:  
     - Auto Proxy Discovery  
     - Automatic Proxy Configuration  
     - Web Proxy (HTTP)  
     - Secure Web Proxy (HTTPS)  
     - SOCKS Proxy  
   - Click **OK** → **Apply**.  

   This removes the Clash-orphaned proxy settings that are blocking normal internet.

   Alternatively (faster), open **Terminal** right after login and run:  
   ```bash
   networksetup -setwebproxystate "Wi-Fi" off
   networksetup -setsecurewebproxystate "Wi-Fi" off
   networksetup -setsocksfirewallproxystate "Wi-Fi" off
   networksetup -setautoproxystate "Wi-Fi" off
   ```  
   (Replace "Wi-Fi" with your actual service name if different—check with `networksetup -listallnetworkservices`.)

3. **Turn Wi-Fi Back On**  
   - Click the Wi-Fi icon in the menu bar → turn Wi-Fi on → connect to your network.  
   - It should now connect normally without proxy interference.

4. **Let macOS Finish Any Pending Updates**  
   - Go to **System Settings > General > Software Update**.  
   - It will likely find and install any remaining small updates or configuration files that were blocked earlier.  
   - Reboot when prompted.

5. **Prevent Future Issues with Clash**  
   - Open Clash → make sure **"Set as System Proxy"** is **turned off** (or never enable it during macOS updates).  
   - Prefer **TUN mode** (if your Clash version supports it on macOS) — it routes traffic at a lower level without touching system proxy settings.  
   - Consider quitting Clash completely before major macOS updates or restarts.

You’re basically done—the offline setup bypass was the perfect workaround. After clearing the proxies and reconnecting, everything (App Store, iCloud, Safari, etc.) should work normally again. If you still see fetch errors or can’t connect after step 2, run this in Terminal and share the output:  
```bash
scutil --proxy
```  
That will show if any proxy is still active system-wide.

You got through the worst part—nice job troubleshooting!

References:  

- None required for this resolution path (based on standard macOS proxy behavior and common Clash-related update hangs reported across Apple forums and Reddit).