---
audio: false
generated: true
image: false
lang: en
layout: post
title: DIY CAN Bus Racing Dashboard
translated: false
type: note
---

Now the picture is much clearer — this is a **CAN bus-based digital dashboard / racing display**, almost certainly built for **sim racing** or a real car's OBD/CAN telemetry.

Reading the board:

**The display (top):**

- **`3`** (big orange number) — current **gear**
- **`70` CLUTCH** — clutch position/pressure %
- **`102` OIL** — oil temp or pressure
- The blue vertical bar — likely an **RPM/shift indicator**

**The compute module:**

- That gray board labeled **"...TICK S3"** is a **LilyGO T-Display-S3** (or similar) — an **ESP32-S3** dev board with a built-in color IPS LCD and USB-C. The "S3" and the form factor are a dead giveaway.

**The breakout below it:**

- The green PCB with **"CAN"** silkscreen and a lit green LED is a **CAN transceiver module** — typically an **SN65HVD230** or **MCP2515 + TCAN/MCP2562** transceiver. The labels **`CTX/CRX`** (CAN TX/RX) and **`3V3 / GND`** confirm it.
- The **"+IN / OUT+ / OUT-"** module on the left with the arrow is a small **buck/boost converter or signal isolator** (power regulation for the 12V automotive rail → 5V/3.3V).
- Yellow wires = the **CAN-H / CAN-L** twisted pair.

**What it actually does:**

The ESP32-S3 reads CAN frames (either from a real car's OBD-II/CAN bus or from sim racing telemetry like iRacing/Assetto Corsa over a CAN gateway), decodes the gear/clutch/oil/RPM signals, and renders them on the LCD as a race dashboard.

This is the **same maker** building the G-force meter from your first image — same prototyping style (perfboard, ESP32-S3, USB-C, orange-on-black UI theme). It's a classic **DIY car/sim dashboard** project.

The typical stack:

```
ESP32-S3 (T-Display-S3)
   │  SPI → built-in ST7789 LCD
   │  GPIO → SN65HVD230 CAN transceiver
   ▼
CAN bus (CAN-H / CAN-L, 500 kbps typical for automotive)
   ▼
Car ECU  /  Sim racing CAN gateway
```

Minimal firmware shape (Arduino-ESP32, using the built-in TWAI/CAN peripheral):

```cpp
#include "driver/twai.h"

void setup() {
  twai_general_config_t g = TWAI_GENERAL_CONFIG_DEFAULT(GPIO_NUM_43, GPIO_NUM_44, TWAI_MODE_NORMAL);
  twai_timing_config_t  t = TWAI_TIMING_CONFIG_500KBITS();
  twai_filter_config_t  f = TWAI_FILTER_CONFIG_ACCEPT_ALL();
  twai_driver_install(&g, &t, &f);
  twai_start();
  // init ST7789 display...
}

void loop() {
  twai_message_t msg;
  if (twai_receive(&msg, pdMS_TO_TICKS(10)) == ESP_OK) {
    switch (msg.identifier) {
      case 0x1F0: gear   = msg.data[0]; break;   // example IDs —
      case 0x1F1: clutch = msg.data[1]; break;   // depend on your DBC
      case 0x1F2: oil    = msg.data[2]; break;
    }
    drawDash(gear, clutch, oil);
  }
}
```

The real work is the **DBC file** — the mapping of CAN arbitration IDs + byte offsets + scaling to physical signals (gear, RPM, oil temp). For sim racing, people often use a PC plugin (SimHub) that pushes telemetry over serial/CAN; for a real car you reverse-engineer the OEM CAN IDs.

Want me to write the full T-Display-S3 dashboard firmware — TWAI receive loop + a clean ST7789 gear/clutch/oil layout matching that orange-on-black aesthetic? It's ~150 lines.
