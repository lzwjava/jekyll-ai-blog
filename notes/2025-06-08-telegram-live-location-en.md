---
audio: false
generated: true
lang: en
layout: post
title: Live Location in Telegram
translated: false
type: note
---

You're observing a common pattern with Telegram's live location updates, and based on the `edit_date` timestamps, it certainly looks like live location updates can be received very frequently, potentially even every second or at very short intervals.

Here's why and what the pattern indicates:

**Pattern Observation:**

Looking at your provided JSON, specifically the `edited_message` objects with the `location` field and increasing `edit_date`:

* **`update_id`: 263947386** - `edit_date`: 1749371583
* **`update_id`: 263947388** - `edit_date`: 1749371587 (4 seconds after the previous one)
* **`update_id`: 263947389** - `edit_date`: 1749371591 (4 seconds after the previous one)
* **`update_id`: 263947390** - `edit_date`: 1749371595 (4 seconds after the previous one)
* **`update_id`: 263947391** - `edit_date`: 1749371602 (7 seconds after the previous one)
* **`update_id`: 263947392** - `edit_date`: 1749371614 (12 seconds after the previous one)
* **`update_id`: 263947393** - `edit_date`: 1749371624 (10 seconds after the previous one)
* **`update_id`: 263947394** - `edit_date`: 1749371628 (4 seconds after the previous one)

And there's also a `message` object:

* **`update_id`: 263947387** - `date`: 1749371586 (This is a new message, not an edited live location)

**Does it mean live location messages will be received every 1 second?**

**Not necessarily exactly every 1 second, but very frequently, often with sub-5-second intervals, especially when there's movement or a need for higher accuracy updates.**

Here's why:

1. **Live Location Nature:** Live location is designed to provide near real-time updates of a user's position. For this to be "live," the updates must be frequent.
2. **`edited_message`:** Unlike regular messages, live location updates are sent as `edited_message` updates to a single, existing message. This means the original message containing the live location is constantly being updated with new coordinates.
3. **`edit_date` field:** The `edit_date` timestamp in the `edited_message` object clearly shows that these updates are happening very close to each other.
4. **Factors Influencing Frequency:**
    * **Movement:** If the user is moving, the updates will typically be more frequent to reflect the changing position accurately.
    * **`live_period`:** The `live_period` field (e.g., 28800 seconds, which is 8 hours) indicates how long the live location sharing will last. Within this period, updates will occur as needed.
    * **Horizontal Accuracy:** Changes in `horizontal_accuracy` might also trigger updates, as the device refines its location estimate.
    * **Network Conditions:** While Telegram tries to send updates promptly, network latency could introduce slight variations in the exact timing of when you receive them.
    * **Telegram's Internal Logic:** Telegram has its own internal algorithms to determine the optimal frequency of sending updates based on the user's activity, device battery, and network conditions. It's not a fixed "every 1 second" rule but rather an adaptive one.

**In summary:**

The pattern you see with rapidly changing `edit_date` for the `edited_message` containing `location` strongly suggests that Telegram sends live location updates very frequently. While it might not be precisely every 1 second, intervals of a few seconds (e.g., 1-5 seconds, or slightly longer if the user is stationary) are typical for live location. The occasional longer gap could be due to network conditions, the user being stationary, or Telegram's internal optimization.
