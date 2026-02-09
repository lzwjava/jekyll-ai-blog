---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Enter BIOS on MSI B760M Mortar
translated: false
type: note
---

Question: How to enter BIOS on this computer with the MSI MAG B760M Mortar WiFi motherboard?

Answer: 

To enter the **BIOS/UEFI** setup on your PC built with the **MSI MAG B760M Mortar WiFi** motherboard (an MSI B760 series board), follow these steps:

### Primary Method (During Boot):
1. **Power off** the computer completely (shut down, not just sleep or hibernate).
2. **Press the power button** to turn it on.
3. Immediately and **repeatedly tap the Delete (Del) key** as soon as the system starts powering on (even before any logo appears on screen).  
   - Keep tapping it quickly until the BIOS setup screen loads.  
   - This is the standard key for nearly all modern MSI motherboards, including the B760 series like your MAG B760M Mortar WiFi.
4. If Del doesn't work after a few tries, also try tapping **F2** repeatedly during the same boot window (some MSI boards list both as possibilities, though Del is far more common for desktop boards).

**Tips for success**:
- Use a **wired USB keyboard** plugged directly into a rear motherboard USB port (avoid front-panel ports or wireless keyboards during first boot, as USB initialization can sometimes be delayed).
- If Fast Boot or Ultra Fast Boot is already enabled in BIOS (or if Windows Fast Startup is on), the boot process may be too quick to catch the key press — in that case, use the Windows method below first.
- Watch the screen carefully: many MSI boards briefly display "Press DEL to enter Setup" (or similar) during POST.

### Alternative Method (From Windows, if the PC boots into the OS):
If you can't catch the key during boot:
1. Boot into Windows normally.
2. Go to **Settings** → **System** → **Recovery** (or search for "Advanced startup").
3. Under **Advanced startup**, click **Restart now**.
4. After restart, choose **Troubleshoot** → **Advanced options** → **UEFI Firmware Settings** → **Restart**.
5. The system will reboot directly into the BIOS setup.

Once inside the BIOS:
- Navigate to the **Power Management** (or similar) section.
- Look for options like **Wake-on-LAN**, **Wake on PCIe**, **PCIe Wake Up**, **Power On By PCI-E**, or **ErP Ready** (disable ErP if needed, as it can block wake features).
- Enable the Wake-on-LAN related setting.
- Save changes (usually **F10** → Yes) and exit.

This should work reliably for your specific MSI motherboard.

References:  

- MSI official support page for MAG B760M MORTAR WIFI: [https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/support](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/support)
- Multiple YouTube tutorials and MSI forum posts confirming **Del** key for B760 series and Mortar models.