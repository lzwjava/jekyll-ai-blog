---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: China's EV Charging Station Production
translated: false
type: note
---

### EV Charging Stations in China: Overview and Internals

China indeed leads the world in EV charging infrastructure. As of mid-2025, the country has over 10 million public charging points, driven by government mandates, subsidies, and massive domestic manufacturing. This network supports the rapid growth of EVs, with stations everywhere from highways to urban sidewalks. These stations are produced at scale by companies like State Grid, TELD, and Star Charge, using standardized GB/T connectors (similar to Europe's Type 2 but optimized for high-power DC).

#### How Are They Made?
EV charging stations are assembled like modular electronics cabinets, combining off-the-shelf and custom components in factories. The process involves:
- Sourcing power electronics (e.g., semiconductors from suppliers like Infineon).
- Integrating software for smart grid compatibility.
- Testing for safety (e.g., IP65 weatherproofing and UL/IEC certifications).
- Enclosing everything in a rugged metal or composite box for outdoor use.
China's advantage is low-cost, high-volume production—stations can cost as little as $500–$2,000 per unit for AC models, scaling up for DC fast chargers.

#### AC and DC Converters: Yes, and They Handle High Voltages
Most stations support both AC (slower, Level 1/2) and DC (fast, Level 3) charging:
- **AC chargers** take grid AC power (e.g., 220–240V single-phase or 380–480V three-phase) and pass it directly to the EV's onboard converter. No heavy conversion inside the station—just regulation.
- **DC fast chargers** (common in China for highways) have built-in AC-to-DC converters (rectifiers and inverters using IGBTs/MOSFETs). These convert high-voltage AC input to adjustable DC output (400–1,000V, up to 250kW+), bypassing the car's converter for quicker charging (e.g., 80% in 20–30 minutes).
They handle "large volts" via robust power electronics rated for 480V AC input and surges up to 1,500V, with protections against spikes. China's grid supports this with stable three-phase power, and stations often include energy storage (BESS) for peak shaving.

#### What's Inside the Big Box (Charging Cabinet)?
The "big box" is the weatherproof pedestal or wall-mounted enclosure (typically 1–2m tall, steel/aluminum with IP65 rating). It's where the charging gun (cable with GB/T plug) is holstered. Inside, it's packed with electronics, cooling, and controls—think a mini power plant. Key components include:

| Component | Description | Role in Charging |
|-----------|-------------|------------------|
| **Power/Charging Module** | Core AC-DC rectifier, DC-DC converters, and semiconductors (e.g., IGBTs). Takes up ~50% of space/cost. | Converts grid AC to high-voltage DC; adjusts output to EV battery needs (e.g., 200–800V). |
| **Control Unit** | Microprocessor/PLC board with software. | Manages communication (OCPP protocol), monitors battery state, and ramps power safely. |
| **Safety Systems** | GFCI breakers, overcurrent/voltage relays, temperature sensors. | Prevents shocks, overloads, or fires; auto-shuts down on faults. |
| **Cooling System** | Fans, heat sinks, or AC units (2–5kW). | Dissipates heat from high-power operation (up to 47°C ambient). |
| **Metering & Communication** | Energy meters and WiFi/4G modules. | Tracks usage for billing; connects to apps/cloud for remote monitoring. |
| **Cable Management** | Internal reels or ports for the charging gun (5–7m cable). | Stores and deploys the gun; includes strain relief. |
| **User Interface** | LCD screen, RFID/QR payment reader. | Shows status, accepts payments (WeChat/Alipay common in China). |

The cabinet also has wiring terminals for grid connection and EMI shielding to reduce noise. For ultra-fast models (e.g., 200kW+ in cities like Shanghai), it might include a small battery for off-peak storage.

This setup makes China's stations reliable and scalable, powering over 20 million EVs. If you're curious about a specific model or installation, let me know!

[What Are The Main Components Of EV Chargers](https://sinoevse.com/what-are-the-main-components-of-ev-chargers/)
[Key Components of DC Fast Charging Stations](https://www.franklingrid.com/en/this-is-franklin-grid/blog/key-components-of-dc-fast-charging-stations/)
[Electric Vehicle Charging Station Cabinets: Types and Solutions 2025](https://linkwellelectrics.com/electric-vehicle-charging-station-cabinets/)
[Overview of AC/DC Converters for Fast-Charging Stations](https://www.powerelectronicsnews.com/overview-of-ac-dc-converters-for-fast-charging-stations/)
[EV Charging Connector Types: A Complete Guide](https://www.power-sonic.com/ev-charging-connector-types/)
