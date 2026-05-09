---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tmall Genie Old Model Wi-Fi Limitations
translated: false
type: note
---

Question: Does the old version of Tmall Genie only support 2.4GHz Wi-Fi (not 5GHz), and could that be why it stopped working after simplifying the network?

Answer:

Yes — what you’re remembering is very likely about **Wi-Fi, not Bluetooth**, and there’s an important distinction here.

The smart speaker Tmall Genie (天猫精灵), especially older models, typically supports:

* **2.4GHz Wi-Fi only**
* **Bluetooth (which always operates at 2.4GHz, not 5GHz)**

### Key clarification

There is no “2.4G vs 5G” for Bluetooth.

That “2.4G / 5G” comparison only applies to **Wi-Fi networks**:

* **2.4GHz Wi-Fi** → longer range, better wall penetration, slower speed
* **5GHz Wi-Fi** → faster speed, shorter range, weaker wall penetration

### Why your device stopped working

What likely happened is:

* You “simplified” your network (for example):

  * disabled 2.4GHz Wi-Fi
  * or merged/split SSIDs incorrectly
  * or switched entirely to a 5GHz-only network

But the Tmall Genie **cannot connect to 5GHz Wi-Fi**, so it suddenly becomes unable to go online.

### Why smart speakers still use 2.4GHz

Even though 5GHz is faster, smart home devices prefer 2.4GHz because:

* better signal stability across rooms
* lower power consumption
* compatibility with IoT chips (cheap + stable design choice)

### What you should do

To fix it:

* Ensure your router has **2.4GHz Wi-Fi enabled**
* Connect the Tmall Genie to the **2.4GHz SSID (not 5GHz)**
* Avoid “dual-band merge” setups if the device gets confused during setup

If you want, I can help you check your router setup and tell you exactly how to separate or identify the correct Wi-Fi band.