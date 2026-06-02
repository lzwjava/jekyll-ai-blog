---
audio: false
generated: true
image: false
lang: en
layout: post
title: Privacy Tips for Smart Home Notifications
translated: false
type: note
---

Question: Does the Xiaomi doorbell iOS app have a privacy leak risk in notifications, and is it better to use short English names instead of Chinese ones for home names?

Answer:

Yes, your concern is valid in a practical sense.

On iOS, when a smart home device like a Xiaomi doorbell sends a notification (e.g., someone rings the bell or motion is detected), the **notification preview can include the device or home name**. If that notification appears in the lock screen or notification center, and someone takes a screenshot, the **home name may be exposed in the image**.

### Why this can be a privacy issue

* Chinese home names like “花园X城” or full community names can be **highly searchable and identifiable**
* Combined with location context (time, camera event), it may reveal:

  * Where you live
  * The type of residence/community
* Screenshots shared casually (chat, social media, support groups) can unintentionally leak this information

### Using short or neutral names helps

Your idea of using short labels like:

* “GG”
* “Home”
* “HQ”
* “A1”

is actually a **common privacy-hardening practice** in smart home setups.

This reduces:

* Identifiability (harder to trace back to real location)
* Searchability (no direct match with real estate names or Chinese community names)
* Information leakage in screenshots

### Better privacy setup suggestions

If you want to go a step further:

* Rename devices to generic labels (e.g., “Doorbell 1” instead of “Garden Villa Gate”)
* Disable sensitive notification previews on lock screen:

  * iOS Settings → Notifications → Xiaomi app → Show Previews → “When Unlocked” or “Never”
* Avoid embedding real estate/community names in any IoT device naming

### Bottom line

Yes, using short neutral English names is a simple but effective mitigation. It won’t remove all risk (metadata still exists in the system), but it significantly reduces accidental exposure from screenshots or notification previews.
