---
audio: false
generated: true
image: false
lang: en
layout: post
title: Charging Lenovo Laptop in Neta EV
translated: false
type: note
---

### Understanding the Issue with Charging Your Lenovo Laptop in a Neta EV

Based on the details you described, it sounds like you're trying to charge your Lenovo laptop (likely via its Type-C port, using a compatible charger) from your Neta EV car in two different ways:

1. **Via the cigarette lighter port (inside the car)**: This involves plugging an adapter or inverter into the 12V cigarette lighter socket to create a power outlet or USB-C connection. This method isn't working for charging your laptop.

2. **Via the external slow charging port (outside the car)**: This uses the car's charging port with a "charging gun" adapter and cable routed through the window to an internal socket, then connecting your laptop's Type-C charger. This method works fine.

The key difference boils down to **power output limitations, voltage types, and system design** in electric vehicles (EVs) like the Neta models (e.g., Neta V or similar). I'll explain step by step why one fails while the other succeeds, based on typical EV specs and Neta's features.

#### 1. Why the Cigarette Lighter Port Can't Charge Your Laptop

- **Limited Power Output**: The cigarette lighter in most cars, including EVs like Neta, is a 12V DC socket designed for low-power accessories (e.g., phone chargers or small gadgets). In Neta EVs, this is typically rated around 120-180W maximum (based on general 12V automotive standards, as it's fused at 10-15A). However, real-world sustained output is often lower due to heat, wiring, and fuse limits.
  - If you're using an inverter (to convert 12V DC to AC for a standard laptop charger) or a direct USB-C car adapter, efficiency losses can drop usable power to 80-100W or less. Lenovo laptops often require 45-100W+ for proper charging (e.g., 65W for many ThinkPad models), especially if the laptop is in use. If the power dips below this, charging stops or becomes too slow to register.
  - Voltage drops or instability in the 12V system (common in EVs, where it's powered by a DC-DC converter from the high-voltage battery) can also prevent reliable charging.

- **Incompatibility with High-Demand Devices**: Laptops need stable, high-wattage power delivery (PD) via Type-C. Cheap car adapters from the cigarette port often max out at 18-30W PD, which might trickle-charge a phone but not a laptop. Even with an inverter, if it's underrated or the port overheats, it shuts down.

- **EV-Specific Constraints**: In EVs, the 12V system is auxiliary (not directly from the main battery) and prioritized for essentials like lights and infotainment. It's not built for sustained high loads like laptop charging, which could drain the 12V battery or trigger safety cutoffs.

In short, the cigarette port simply doesn't provide enough consistent power for your Lenovo laptop's needs.

#### 2. Why the External Slow Charging Port Method Works

- **This Uses the V2L (Vehicle-to-Load) Feature**: Neta EVs (like the Neta V) support V2L, which turns the car into a mobile power source. You plug a special V2L adapter (often resembling a charging gun) into the external AC charging port, which draws from the high-voltage battery and outputs AC power (e.g., 220V in many regions).
  - Neta's V2L can deliver up to 3,300W (3.3kW), far more than needed for a laptop. This is like plugging into a household wall socket—stable, high-power AC without significant losses.
  - By routing the cable through the window to an internal socket, you're essentially extending a full-power outlet inside the car. Your laptop's Type-C charger (which converts AC to DC) gets the exact power it needs, just like at home.

- **No Power Limitations Here**: V2L bypasses the low-power 12V system and uses the car's onboard inverter/charger directly from the main battery. It's designed for higher loads (e.g., appliances, tools, or even camping gear), so charging a 65-100W laptop is effortless. It also avoids efficiency issues since it's native AC output.

- **Safety and Design Benefits**: V2L includes protections against overload, and since it's external, it doesn't interfere with the car's internal systems. Note: Ensure your Neta model has V2L enabled (most recent ones do), and use the official adapter to avoid risks.

#### Potential Fixes or Alternatives

- For the cigarette port: Try a high-quality inverter rated for at least 150W continuous output, or a dedicated 60W+ PD USB-C car charger. But even then, it might not work reliably in your Neta due to the 12V limits—test with the car running to maintain battery power.
- Stick with V2L for reliable charging, but be mindful of battery drain (it uses the main EV battery, so monitor SOC to avoid stranding yourself).
- If your laptop supports it, a direct USB-C cable from a high-power car USB port (if your Neta has one) might work better than the cigarette lighter.
- General tip: Always check your Neta's user manual for exact specs on ports and V2L usage.

If this doesn't match your exact setup (e.g., specific Neta model or adapter details), provide more info for a tailored explanation!

[Neta V User Manual](https://www.netaauto.co/resource/upload/User%27s%2520Manual%2520of%2520NETA%2520V.pdf)
[NETA V Official Specs](https://www.neta.co.th/en/product/NetaV)
[The Neta V Launched In Malaysia](https://cleantechnica.com/2023/05/15/the-neta-v-launched-in-malaysia-is-now-the-most-affordable-ev-in-the-country/)
[Vehicle to Load (V2L): What It Is & How It Works](https://www.joosup.com/vehicle-to-load/)
[Is it possible to charge a laptop in an ev](https://www.reddit.com/r/electricvehicles/comments/15jp7w1/is_it_possible_to_charge_a_laptop_in_an_ev/)
