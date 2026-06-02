---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configuring OpenWRT as a Wireless Bridge
translated: false
type: note
---

With the help of Grok, I am still trying to work on the following.

---

To address your query, "is it right?" regarding the steps to configure OpenWRT as a wireless bridge, and to provide the correct ways to achieve this, I’ll evaluate the steps you provided and refine them based on best practices for OpenWRT. Your goal is to set up your OpenWRT router (e.g., Xiaomi Mi Router 4C with OpenWRT 24.10.0) as a wireless bridge—connecting wirelessly to an existing Wi-Fi network as a client and sharing that connection via its own Wi-Fi access point (AP) or Ethernet ports, keeping all devices on the same subnet as the main router.

Your provided steps are mostly accurate but miss a critical adjustment to ensure proper bridging and avoid IP conflicts. Below, I’ll first assess your configuration and then present the correct, complete steps to achieve a wireless bridge in OpenWRT using the simple bridge method (client + AP on the same bridge), which aligns with your intent. I’ll also briefly mention an alternative using `relayd` for cases where the simple method fails, though your setup likely supports the simpler approach.

---

### **Evaluation of Your Provided Steps**

Your steps aim to:

1. Connect the OpenWRT router as a client to an existing Wi-Fi network.
2. Set up an AP to broadcast a new Wi-Fi network.
3. Bridge the client and AP interfaces to share the internet.

Here’s a quick review:

- **Step 1: Log In to LuCI** - Correct, accessing the web interface is the starting point.
- **Step 2: Configure the Wireless Client** - Joining the target Wi-Fi and assigning it to the `lan` network is a good start, but the default `lan` configuration in OpenWRT (static IP, typically 192.168.1.1) could conflict with the main router if it uses the same IP. This needs adjustment.
- **Step 3: Configure the Wireless AP** - Setting up an AP and assigning it to `lan` is correct for bridging, but relies on the `lan` interface being properly configured.
- **Step 4: Bridge the Networks** - Assigning both interfaces to `lan` theoretically bridges them, but without disabling the DHCP server or adjusting the IP settings, it may not work seamlessly.
- **Step 5: Test the Setup** - Testing is essential, but success depends on earlier steps being fully correct.

**What’s Missing or Wrong?**

- By default, OpenWRT’s `lan` interface has a static IP (e.g., 192.168.1.1) and runs a DHCP server. If the main router is also 192.168.1.1, this causes an IP conflict. You need to set the `lan` interface to DHCP client mode to obtain an IP from the main router and disable the local DHCP server to let the main router assign IPs to all devices.
- The firewall zone assignment to `lan` is fine for simplicity, but the IP configuration is critical.

With this in mind, your steps are "mostly right" but incomplete without adjusting the `lan` interface settings. Below are the corrected steps.

---

### **Correct Steps to Configure OpenWRT as a Wireless Bridge (Simple Bridge Method)**

This method sets up your OpenWRT router to connect to an existing Wi-Fi network as a client and share that connection via its own AP or Ethernet ports, all on the same subnet as the main router (e.g., 192.168.1.x). Here’s how to do it via the LuCI web interface:

#### **Prerequisites**

- OpenWRT is installed (e.g., version 24.10.0 on Xiaomi Mi Router 4C).
- You have the SSID, password, and encryption type (e.g., WPA2-PSK) of the main Wi-Fi network.
- Access to LuCI at `http://192.168.1.1` (or the current IP) and your admin credentials.

#### **Step 1: Log In to LuCI**

- Open a browser and navigate to `http://192.168.1.1`.
- Log in with your OpenWRT username (default: `root`) and password (set during installation).

#### **Step 2: Configure the Wireless Client**

- **Navigate to Wireless Settings:**
  - Go to **Network > Wireless**.
- **Scan for Networks:**
  - Locate your radio (e.g., `radio0` for 2.4 GHz on the Mi Router 4C).
  - Click **Scan** to list available Wi-Fi networks.
- **Join the Main Wi-Fi Network:**
  - Find the SSID of your main router’s Wi-Fi.
  - Click **Join Network**.
- **Configure Client Settings:**
  - **Wi-Fi Key:** Enter the password for the main Wi-Fi.
  - **Network:** Select or set to `lan` (this adds the client interface to the `br-lan` bridge).
  - **Firewall Zone:** Assign to `lan` (this simplifies traffic rules for bridging).
  - **Interface Name:** LuCI may suggest `wwan`; you can leave it or rename it to `client` for clarity, but ensure it’s tied to `lan`.
- **Save & Apply:**
  - Click **Save & Apply** to connect to the main Wi-Fi.

#### **Step 3: Adjust the LAN Interface to DHCP Client**

- **Go to Interfaces:**
  - Navigate to **Network > Interfaces**.
- **Edit the LAN Interface:**
  - Click **Edit** next to the `lan` interface.
- **Set Protocol to DHCP Client:**
  - In the **Protocol** dropdown, select **DHCP client**.
  - This allows the `br-lan` bridge (which now includes the wireless client) to obtain an IP address from the main router’s DHCP server (e.g., 192.168.1.x).
- **Disable DHCP Server:**
  - Since `lan` is now a DHCP client, the local DHCP server is automatically disabled. Verify this under **Advanced Settings** or **DHCP and DNS**—ensure "Ignore interface" is checked if the option appears.
- **Save & Apply:**
  - Click **Save & Apply**. The router will now request an IP from the main router.

#### **Step 4: Configure the Wireless Access Point**

- **Add a New Wireless Network:**
  - Go back to **Network > Wireless**.
  - Click **Add** under the same radio (e.g., `radio0`) to create a new wireless interface.
- **Set Up the AP:**
  - **ESSID:** Choose a name for your Wi-Fi (e.g., `OpenWRT_AP`).
  - **Mode:** Set to **Access Point (AP)**.
  - **Network:** Assign to `lan` (this bridges it with the client interface and Ethernet ports).
- **Configure Security:**
  - Go to the **Wireless Security** tab.
  - **Encryption:** Select **WPA2-PSK** (recommended).
  - **Key:** Set a strong password for your AP.
- **Save & Apply:**
  - Click **Save & Apply**. Your router will now broadcast its own Wi-Fi.

#### **Step 5: Verify the Bridge**

- **Check Interfaces:**
  - Go to **Network > Interfaces**.
  - Ensure the `lan` interface lists both the wireless client (e.g., `wlan0`) and AP (e.g., `wlan0-1`) under the `br-lan` bridge.
- **Check IP Assignment:**
  - Go to **Status > Overview**.
  - Note the IP address assigned to the `lan` interface by the main router (e.g., `192.168.1.100`).

#### **Step 6: Test the Setup**

- **Test Wi-Fi:**
  - Connect a device to the `OpenWRT_AP` Wi-Fi.
  - Verify it receives an IP from the main router (e.g., `192.168.1.x`) and has internet access.
- **Test Ethernet (if applicable):**
  - Plug a device into one of the router’s LAN ports.
  - Confirm it gets an IP from the main router and connects to the internet.
- **Access LuCI:**
  - Use the new IP address (e.g., `http://192.168.1.100`) to access the OpenWRT interface.

---

### **Why This Works**

- Assigning both the client and AP interfaces to the `lan` network adds them to the `br-lan` bridge, allowing layer 2 traffic to flow between them and the main router.
- Setting `lan` to DHCP client ensures the OpenWRT router gets a unique IP from the main router, avoiding conflicts (e.g., with `192.168.1.1`), and disables the local DHCP server so the main router manages all IP assignments.
- Devices connected to the AP or Ethernet ports appear on the same subnet as the main network (e.g., `192.168.1.x`), fulfilling the wireless bridge requirement.

---

### **Alternative Method: Using relayd (Pseudo-Bridge)**

If the simple bridge method fails (e.g., due to wireless driver limitations), you can use the `relayd` package for a pseudo-bridge. This creates a routed setup where the OpenWRT router’s clients are on a different subnet, but it’s more reliable on some hardware. Here’s a brief overview:

1. **Install relayd:**
   - Go to **System > Software**, search for `relayd`, and install it.
2. **Configure Wireless Client:**
   - Join the main Wi-Fi, but assign it to a new interface (e.g., `wwan`) set to DHCP client.
3. **Configure LAN:**
   - Set `lan` to a static IP (e.g., `192.168.2.1`) with its own DHCP server.
4. **Set Up relayd:**
   - Configure `relayd` via SSH or LuCI (under **Network > Hostnames**) to relay between `wwan` and `lan`.
5. **Configure AP:**
   - Set the AP on the `lan` network.
6. **Test:**
   - Devices on `OpenWRT_AP` will be on `192.168.2.x`, with internet relayed from the main router.

**Note:** This isn’t a true bridge (different subnets), so use it only if the simple method doesn’t work. For your Xiaomi Mi Router 4C with OpenWRT 24.10.0, the simple bridge should suffice.

---

### **Conclusion**

Your original steps are **mostly correct** but incomplete without setting the `lan` interface to DHCP client mode to avoid IP conflicts and ensure proper bridging. The corrected steps above provide a reliable way to configure OpenWRT as a wireless bridge. If you follow them, your router will connect to the main Wi-Fi and share that connection seamlessly via its AP or Ethernet ports, all on the same subnet. Test the setup, and if issues arise (rare with modern OpenWRT), consider the `relayd` alternative.
