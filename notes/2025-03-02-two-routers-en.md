---
audio: false
generated: true
lang: en
layout: post
title: Using Two Routers
translated: false
type: note
---

To set up your two TP-Link AX3000 (TL-XDR 3050) routers with your modem in the configuration **Modem → Cable → Router1 → Wireless → Router2**, follow this step-by-step guide. Your modem already has WiFi functionality and an IP address of `192.168.1.1`. We'll configure Router1 as the main router connected to the modem via a cable and Router2 to extend the network wirelessly.

Here’s how to achieve this:

---

### **Step 1: Understand the Setup**

- **Modem**: Provides internet access and has its own WiFi (IP: `192.168.1.1`).
- **Router1**: Will connect to the modem with a cable and act as the primary router for your network.
- **Router2**: Will connect wirelessly to Router1 to extend the network coverage.

You’ve mentioned several modes (Wired AP Bridge, Wireless AP Bridge, DHCP, Broadband Connect). We’ll use **DHCP** for Router1 to get an internet connection from the modem and **Wireless AP Bridge** (or a similar mode like WDS/Repeater) for Router2 to connect wirelessly to Router1.

---

### **Step 2: Set Up Router1**

1. **Connect Router1 to the Modem**:
   - Take an Ethernet cable and plug one end into a **LAN port** on your modem.
   - Plug the other end into the **WAN (Internet) port** on Router1.

2. **Access Router1’s Web Interface**:
   - Connect a computer or smartphone to Router1’s default WiFi network (check the label on the router for the default SSID and password) or use an Ethernet cable.
   - Open a web browser and type `http://tplinkwifi.net` or `192.168.0.1` (the default IP for TP-Link routers).
   - Log in with the default credentials (usually `admin` for both username and password) unless you’ve changed them.

3. **Configure Router1**:
   - **Internet Connection**:
     - Go to **Quick Setup** or the **Internet** settings section.
     - Select **DHCP** mode. This allows Router1 to automatically get an IP address from the modem (likely in the `192.168.1.x` range).
   - **WiFi Settings**:
     - Set a unique **SSID** (network name) and a strong **password** for Router1’s WiFi.
     - Save these details, as Router2 will need them to connect wirelessly.
   - **LAN Settings**:
     - Ensure Router1’s LAN IP is different from the modem’s IP. By default, it’s likely `192.168.0.1`, which is fine since the modem is `192.168.1.1`.
     - Confirm that **DHCP** is enabled on Router1. This allows Router1 to assign IP addresses (e.g., `192.168.0.x`) to devices connected to it, including Router2.
   - Save the settings and reboot Router1 if prompted.

---

### **Step 3: Set Up Router2 as a Wireless Bridge**

1. **Access Router2’s Web Interface**:
   - Connect a computer or smartphone to Router2’s default WiFi network or via Ethernet.
   - Open a web browser and type `http://tplinkwifi.net` or `192.168.0.1`.
   - Log in with the default credentials (or your custom ones).

2. **Configure Router2 in Wireless Bridge Mode**:
   - Look for a mode like **Wireless AP Bridge**, **WDS**, or **Repeater** in the settings (likely under **Operation Mode** or **Wireless** settings).
   - Select **Wireless AP Bridge** (or WDS/Repeater if that’s what’s available).
   - **Connect to Router1’s WiFi**:
     - Scan for available networks and select Router1’s SSID.
     - Enter Router1’s WiFi password.
     - Ensure Router2 uses the same wireless channel as Router1 for compatibility (e.g., if Router1 is on Channel 6, set Router2 to Channel 6).
   - **LAN IP Setting**:
     - Change Router2’s LAN IP to avoid conflicts with Router1. For example, set it to `192.168.0.2` (since Router1 is likely `192.168.0.1`).
     - **Disable DHCP** on Router2. Router1 will handle IP assignments for all devices.
   - Save the settings and reboot Router2. It should now connect wirelessly to Router1.

---

### **Step 4: Test the Setup**

1. **Verify Router2’s Connection**:
   - After rebooting, check Router2’s interface to confirm it’s connected to Router1’s WiFi.
2. **Connect a Device to Router2**:
   - Use a smartphone, laptop, or other device to connect to Router2’s WiFi (it may use the same SSID as Router1, depending on the mode).
   - Check that the device gets an IP address from Router1 (e.g., `192.168.0.x`).
   - Test internet access by browsing a website.

---

### **Final Configuration Summary**

- **Modem**: IP `192.168.1.1`, provides internet and WiFi.
- **Router1**:
  - WAN: Connected to modem via cable, set to **DHCP** (gets IP from modem, e.g., `192.168.1.x`).
  - LAN: IP `192.168.0.1`, **DHCP enabled** to assign IPs to devices.
  - WiFi: Custom SSID and password.
- **Router2**:
  - Mode: **Wireless AP Bridge** (or WDS/Repeater), connected wirelessly to Router1’s WiFi.
  - LAN IP: `192.168.0.2`, **DHCP disabled**.

---

### **Troubleshooting Tips**

- **Router2 Not Connecting Wirelessly**:
  - Double-check Router1’s SSID, password, and channel settings in Router2’s configuration.
  - If **Wireless AP Bridge** isn’t available, try **WDS** or **Repeater** mode. Refer to the TP-Link AX3000 manual for supported modes.
- **No Internet on Router2**:
  - Ensure Router1’s DHCP is working and Router2’s DHCP is off.
  - Verify Router2 is successfully bridging to Router1.
- **Double NAT Concerns**:
  - Since your modem has WiFi and Router1 acts as a router, you might have double NAT (modem and Router1 both assigning IPs). This is usually fine for basic use but could affect some applications (e.g., gaming). If needed, set the modem to **bridge mode** (consult your modem’s manual), though this may disable its WiFi.

With this setup, Router2 will extend your network wirelessly from Router1, and devices connected to either router should access the internet through the modem. Let me know if you need further assistance!

---

If you decide to use a fixed (static) IP address for the first router (Router1) instead of relying on DHCP, you'll need to manually configure its WAN settings to communicate with your modem. Here’s what you should configure for the IP address, DNS, subnet mask, and gateway:

---

### **Assumptions**

- Your modem has an IP address of `192.168.1.1` and uses the subnet `192.168.1.0/24` (subnet mask `255.255.255.0`).
- The modem has a DHCP range (e.g., `192.168.1.2` to `192.168.1.100`) that assigns IP addresses to connected devices.

If your modem uses a different IP or subnet, adjust the values accordingly.

---

### **WAN Settings for Router1**

These settings configure how Router1 connects to the modem:

1. **IP Address**
   - Choose a static IP within the modem’s subnet (`192.168.1.0/24`) but **outside the modem’s DHCP range** to avoid conflicts.
   - Example: If the modem’s DHCP range is `192.168.1.2` to `192.168.1.100`, you can use **`192.168.1.101`**.
   - This ensures Router1 has a unique, fixed address on the modem’s network.

2. **Subnet Mask**
   - Set this to match the modem’s subnet mask, which is typically **`255.255.255.0`**.
   - This defines the network range as `192.168.1.0` to `192.168.1.255`.

3. **Default Gateway**
   - Set this to the modem’s IP address, which is **`192.168.1.1`**.
   - The gateway is the device (your modem) that Router1 uses to access the internet.

4. **DNS Servers**
   - You have two options:
     - Use the modem’s IP: **`192.168.1.1`**. This lets the modem handle DNS requests.
     - Use public DNS servers: **`8.8.8.8`** (Google) and **`8.8.4.4`** (Google secondary). These are reliable and often faster.
   - Recommendation: Start with `192.168.1.1`. If you experience DNS issues, switch to `8.8.8.8` and `8.8.4.4`.

---

### **Example Configuration**

Here’s what your Router1 WAN settings might look like:

- **IP Address**: `192.168.1.101`
- **Subnet Mask**: `255.255.255.0`
- **Default Gateway**: `192.168.1.1`
- **DNS Server**: `192.168.1.1` (or `8.8.8.8` and `8.8.4.4`)

---

### **Additional Notes**

- **Check Modem Settings**: Log into your modem (usually at `192.168.1.1`) to confirm its IP, subnet mask, and DHCP range. Adjust Router1’s static IP if needed.
- **LAN Settings for Router1**: To avoid conflicts, configure Router1’s LAN network on a different subnet, like `192.168.0.1` with a subnet mask of `255.255.255.0`. Enable DHCP on Router1 to assign IPs (e.g., `192.168.0.2` to `192.168.0.254`) to devices connected to it.
- **Testing**: After applying these settings, ensure Router1 can access the internet. If not, double-check the IP (no conflicts), gateway, and DNS values.

This configuration gives Router1 a fixed IP on the modem’s network, ensuring consistent connectivity. Let me know if you need help with additional routers or specific modem details!

---

It sounds like you've set up Router1 with a static WAN IP and configured its LAN with DHCP, but your laptop still can't connect to the network. Let’s troubleshoot this step-by-step to figure out why and how to fix it.

---

### Step 1: Verify Router1’s WAN Connection

Your WAN settings are:

- **IP Address**: `192.168.1.101`
- **Subnet Mask**: `255.255.255.0`
- **Default Gateway**: `192.168.1.1`
- **DNS Server**: `192.168.1.1` (or `8.8.8.8` and `8.8.4.4`)

These settings suggest Router1 is connected to a modem or another router with an IP of `192.168.1.1`. Here’s what to check:

- **Internet Access on Router1**:
  - Log into Router1’s web interface (likely at `192.168.0.1` from your LAN settings below).
  - Go to the **Status** or **WAN** section to see if Router1 shows an active internet connection. If it doesn’t, the problem might be between Router1 and the modem.

- **IP Conflict**:
  - Ensure no other device on the modem’s network is using `192.168.1.101`. If the modem’s DHCP range includes this IP, it could cause a conflict. Log into the modem (at `192.168.1.1`) and check its DHCP settings or connected devices list. If `192.168.1.101` is within the modem’s DHCP range, either change Router1’s WAN IP to something outside that range (e.g., `192.168.1.200`) or exclude it from the modem’s DHCP pool.

- **Modem Connectivity**:
  - Confirm the Ethernet cable is plugged into the modem’s **LAN port** and Router1’s **WAN port**. If this isn’t set up correctly, Router1 won’t connect to the internet.

---

### Step 2: Check Router1’s LAN and DHCP Settings

Your LAN and DHCP settings are:

- **LAN IP**: `192.168.0.1`
- **Subnet Mask**: `255.255.255.0`
- **DHCP Enabled**: Yes
- **IP Address Range**: `192.168.0.2` to `192.168.0.254`
- **Gateway**: `192.168.0.1`
- **DNS Server**: `192.168.0.1`

These look solid, but let’s ensure they’re working:

- **DHCP Functionality**:
  - With DHCP enabled, your laptop should automatically get an IP address between `192.168.0.2` and `192.168.0.254`, with a gateway of `192.168.0.1`. If it’s not, DHCP might not be functioning properly.

- **DNS Configuration**:
  - Setting the DNS server to `192.168.0.1` means Router1 handles DNS requests for your laptop. Ensure Router1 is configured to forward these requests to an upstream DNS server (like `192.168.1.1` or `8.8.8.8`). This is usually automatic, but double-check in Router1’s settings. Alternatively, you could set the DHCP DNS to `8.8.8.8` and `8.8.4.4` directly to bypass Router1 for DNS.

---

### Step 3: Test Your Laptop’s Connection

Since your laptop isn’t connecting, let’s diagnose it:

- **Connection Type**:
  - Are you using WiFi or Ethernet? If WiFi, ensure you’re connecting to Router1’s SSID (not the modem’s). If Ethernet, confirm the cable is plugged into one of Router1’s LAN ports.

- **Check Laptop’s IP Address**:
  - On your laptop, open a **Command Prompt** (Windows) or **Terminal** (macOS/Linux):
    - Windows: Type `ipconfig` and press Enter.
    - macOS/Linux: Type `ifconfig` or `ip addr` and press Enter.
  - Look for your network adapter’s IP address. It should be something like `192.168.0.x` (where `x` is between 2 and 254), with a subnet mask of `255.255.255.0` and gateway `192.168.0.1`.
  - **If No IP Address**:
    - Your laptop might not be getting an IP from DHCP. Ensure its network settings are set to “Obtain an IP address automatically.” Try renewing the IP:
      - Windows: Run `ipconfig /release` then `ipconfig /renew`.
    - If it still fails, DHCP on Router1 or the connection to it might be the issue.

- **Ping Router1**:
  - From your laptop, run `ping 192.168.0.1`. If you get replies, your laptop is connected to Router1 but might not have internet access. If it times out, the laptop isn’t reaching Router1.

---

### Step 4: Common Issues and Fixes

Here are some likely culprits:

- **Cable Issues**:
  - If using Ethernet, try a different cable or LAN port on Router1. A faulty cable or port could prevent connectivity.

- **WiFi Problems**:
  - If on WiFi, double-check the password and ensure Router1’s WiFi is enabled. Signal interference or a misconfigured SSID could also be the issue.

- **Router1-Modem Link**:
  - If Router1 isn’t getting an internet connection, the modem might require specific settings (e.g., MAC address cloning). Check the modem’s manual or settings for this.

- **Double NAT**:
  - Your setup has the modem (at `192.168.1.1`) and Router1 (at `192.168.0.1`) both acting as routers. This shouldn’t block basic connectivity, but setting the modem to **bridge mode** (if possible) could simplify things.

- **Firewall**:
  - Router1’s firewall might be blocking your laptop. Temporarily disable any custom firewall rules to test.

---

### Step 5: Reset if Needed

If nothing works, reset Router1 and reconfigure:

- **Factory Reset**:
  - Press and hold Router1’s reset button for 10 seconds, then set up the WAN and DHCP settings again as you listed.

- **Try Dynamic WAN**:
  - Instead of a static WAN IP, set Router1’s WAN to **DHCP** to see if it can pull an IP from the modem automatically. If this works, the static IP (`192.168.1.101`) might be the problem.

---

### Final Tips

- **Modem DHCP Range**: Confirm `192.168.1.101` is outside the modem’s DHCP range to avoid conflicts.
- **Firmware**: Check Router1’s web interface for a firmware update.
- **Laptop Drivers**: Ensure your laptop’s network adapter drivers are up to date.

Follow these steps, and you should pinpoint why your laptop isn’t connecting. If you’re still stuck, let me know what you find at each step—I’ll help you narrow it down further!
