---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Enable WoL on MSI B760M Mortar
translated: false
type: note
---

Question: In this computer with the MSI MAG B760M Mortar WiFi motherboard, how to boot into BIOS/UEFI and enable “Wake-on-LAN” or “PCIe/PCI Wake” under power management settings?

Answer:

For your PC with the **MSI MAG B760M Mortar WiFi** motherboard (MSI B760 series), follow these exact steps to enter the BIOS and enable Wake-on-LAN (WoL). The process is standard for recent MSI gaming motherboards like yours.

### Step 1: Enter the BIOS/UEFI

1. Completely **power off** the computer (full shutdown, not sleep or hibernate).
2. Press the **power button** to start the system.
3. Immediately and **repeatedly tap the Delete (Del) key** right after pressing the power button (start tapping even before the screen lights up).
   - Keep tapping Del quickly until the BIOS setup utility appears (MSI logo or black screen with options).
   - This is the correct key for your motherboard (confirmed across MSI B760 models and official guides).
4. If Del doesn't work after several attempts (rare), also try **F2** repeatedly during the same early boot phase.
5. **Tips**:
   - Use a **wired USB keyboard** connected to a rear USB port (avoid wireless or front-panel ports for initial entry).
   - If Windows Fast Startup is enabled, it can make the boot too fast to catch the key — use the Windows alternative method below first if needed.

**Alternative method from inside Windows** (if you can boot to the OS):

1. Open **Settings** → **System** → **Recovery**.
2. Under **Advanced startup**, click **Restart now**.
3. After reboot: **Troubleshoot** → **Advanced options** → **UEFI Firmware Settings** → **Restart**.
4. This boots directly into BIOS.

### Step 2: Enable Wake-on-LAN in BIOS

Once inside the BIOS (it may start in EZ Mode — press **F7** to switch to Advanced Mode if needed):

1. Use the mouse or arrow keys to select **SETTINGS** (usually on the top/left menu).
2. Go to **Advanced** → **Power Management Setup** (or sometimes directly under **Advanced**).
3. Find **ErP Ready** (or **EuP 2013** / **ERP Ready**) and set it to **Disabled**.
   - This is important — ErP enabled cuts power to PCIe devices (including the network controller) during shutdown, which prevents WoL from working.
4. Go back (or navigate) to **SETTINGS** → **Advanced** → **Wake Up Event Setup** (sometimes called **Wake Event Setup** or similar).
5. Locate **Resume By PCI-E Device**, **Resume By PCI-E/Networking Device**, **Resume By PCIe Device**, or **Power On By PCI-E Device**.
   - Set it to **Enabled**.
   - This is the main Wake-on-LAN / PCIe wake setting (your board uses a PCIe-connected 2.5Gbps Realtek LAN controller, so this covers it).
6. (Optional but recommended) Look for related options like **Wake Up Event By** and set to **BIOS** (instead of OS) for more reliable behavior in some cases.
7. Press **F10** to **Save Changes and Exit**, then confirm **Yes**.
8. The system will restart into Windows.

### Additional Important Steps (After BIOS)

For WoL to fully work after shutdown:

- In Windows: Open **Device Manager** → **Network adapters** → right-click your Ethernet controller (likely Realtek Gaming 2.5GbE Family Controller) → **Properties** → **Power Management** tab:
  - Check **Allow this device to wake the computer**.
  - Check **Only allow a magic packet to wake the computer** (optional, but more secure).
- Also disable **Fast Startup** in Windows (Control Panel → Power Options → Choose what the power buttons do → Change settings that are currently unavailable → uncheck Turn on fast startup).
- Ensure your Ethernet cable is plugged in (WoL typically requires wired LAN, not Wi-Fi on this board).

This configuration matches official MSI WoL guides and user reports for B760-series Mortar boards. Test by shutting down the PC completely and sending a magic packet from another device (using tools like WakeMeOnLan or apps).

References:

- [MSI Official Wake-On-LAN Setup Guide](https://www.msi.com/support/technical_details/MB_Wake_On_LAN)
- [MSI Forum and Reddit threads confirming "Resume By PCI-E Device" and ErP Disabled for B760/B560/MAG Mortar series](https://forum-en.msi.com/index.php?threads/wake-on-lan-mag-b560-mortar.375270/)
- [MSI USA FAQ on Wake on LAN settings](https://us.msi.com/faq/motherboard-503)
