---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: DJI Mini 3 Tracking Limitations and Workarounds
translated: false
type: note
---

The DJI Mini 3 (the base model) does not have built-in features like ActiveTrack (visual object following) or Follow Me mode (GPS-based tracking) to automatically chase or hover above a moving car for photos or video. This is a key limitation compared to higher-end DJI drones. However, the DJI Mini 3 Pro does support ActiveTrack, which uses the drone's camera to visually track and follow subjects like cars, people, or vehicles from behind, above, or in other positions—allowing you to capture dynamic shots while the drone maintains a set distance and height.

Regarding APIs for custom development:
- DJI's Mobile SDK (for Android/iOS apps) does support the Mini 3 series, including basic flight control like virtual stick commands (e.g., to manually adjust position/speed) and waypoint missions. You could build a custom app to make the drone follow a car's path if you integrate real-time GPS data from the car (via Bluetooth, a companion app, or external transmitter). This wouldn't be "plug-and-play" visual tracking but could approximate chasing from above or behind by calculating offsets (e.g., 10-20 meters back and 50 meters up).
- However, the SDK's ActiveTrack mission APIs (for automated visual following) are **not supported** on the Mini 3 or Mini 3 Pro—they're limited to older models like Mavic Air 2 or Air 2S.
- For photo capture during flight, you can use the SDK's camera APIs to trigger shots automatically based on timers, distance, or your custom logic.

If you're okay with third-party apps (which leverage the SDK under the hood):
- Apps like Dronelink or Litchi can enable a basic "Follow Me" mode on the Mini 3 by using your phone's GPS (or an external device). To track a car specifically, you'd need to pair it with a GPS beacon on the vehicle (e.g., via a smartphone hotspot or dedicated tracker like a Tile or AirTag alternative that feeds data to the app). This setup has worked for users chasing cars on roads or trails, with the drone staying overhead or trailing behind for footage.

Keep in mind legal/safety notes: Drone following of moving vehicles must comply with local regs (e.g., FAA rules in the US require visual line-of-sight, no beyond-visual-range ops). Test in open areas to avoid obstacles, and the Mini 3's lightweight design limits wind resistance during high-speed chases.

### References
- [DJI Mini 3 Active Track HACK DJI Mini 3 Follow Me](https://www.youtube.com/watch?v=UYzSdd3iJwA)
- [Does the mini 3 have ai tracking to follow objects like cars](https://www.facebook.com/groups/djimini3ukowners/posts/2726498670890510/)
- [Can someone explain follow me mode? And if it's on mini 3?](https://www.reddit.com/r/dji/comments/13pqbw7/can_someone_explain_follow_me_mode_and_if_its_on/)
- [DJI Mini 3 / Mini 3 Pro - Follow Me Mode With Dronelink](https://www.youtube.com/watch?v=Rhneo8QoXV0)
- [DJI Product SDK Compatibility](https://support.dji.com/help/content?customId=01700000763&spaceId=17&re=US&lang=en&documentType=&paperDocType=ARTICLE)
- [DJI has released MSDK 5.3.0 with support for Mini 3 Pro and Mini 3](https://forum.flylitchi.com/t/dji-has-released-msdk-5-3-0-with-support-for-mini-3-pro-and-mini-3/9512)
- [class ActiveTrackOperator - DJI Mobile SDK Documentation](https://developer.dji.com/api-reference/android-api/Components/Missions/DJIActiveTrackMissionOperator.html)
