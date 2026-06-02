---
audio: false
generated: true
image: false
lang: en
layout: post
title: China's Intranet and App Distribution
translated: false
type: note
---

Question: On a Google Pixel phone using a v2ray proxy in China, why can some apps like 交警12123 (Traffic Police 12123) only be downloaded from 应用宝 (Tencent MyApp) and not from the Google Play Store?

Answer:

This is a great question that touches on multiple layers — political, regulatory, technical, and business. Let's break it down fully.

---

## 1. Google Play Store Is Blocked in China — Structurally, Not Just Network-Level

Google Play Store has been completely blocked in mainland China since 2012, along with other Google services. This blocking is enforced through the Great Firewall of China as part of the government's internet censorship policies.

The key reasons are:

- **Data sovereignty**: China requires user data to be stored locally and accessible to authorities.
- **Content control**: The government wants oversight of all apps available to Chinese users.
- **Domestic industry protection**: Blocking foreign competitors helps Chinese app stores gain market share.
- **Political tension**: Ongoing disputes between Google and Chinese authorities over censorship compliance.

---

## 2. Why a V2ray Proxy Doesn't Fully Solve the Problem

Even if you use v2ray or any VPN/proxy to bypass the Great Firewall, there are **additional layers** that prevent apps like 交警12123 from appearing on Google Play:

### (A) The Developer Never Submitted the App to Google Play

This is the **primary reason**. Apps like 交警12123 (operated by the Ministry of Public Security of China) are **intentionally distributed only through domestic Chinese app stores**. The developer chose not to publish on Google Play — and there are strong regulatory and practical reasons:

- Chinese law requires app publishers to have a Chinese Business License (营业执照), which requires setting up a Chinese entity. Publishing an Android app in China requires a fundamentally different approach than Google Play Store distribution.
- Google Play does not have a license to distribute apps in China directly.
- Chinese government apps are designed specifically for users inside China, using Chinese infrastructure (servers, authentication, payments, maps, push notifications). Publishing on Google Play would require major rebuilds.

### (B) These Apps Depend on Chinese Infrastructure, Not Google Services

Apps cannot rely on Google Play Services, Maps, or other Google APIs. All aspects of the app must use local alternatives.

Apps like 交警12123 use:
- Chinese government ID verification systems
- Chinese map services (not Google Maps)
- Chinese push notification systems (not Firebase)
- WeChat/Alipay payment integration

None of these work properly via a Google Play distribution model.

### (C) Google Play Account Region Restrictions

Even when you bypass the firewall with v2ray, Google Play checks your **account's country setting** and your **billing region**. Apps with geo-restrictions will simply not appear in search results or will show "Not available in your country" — even with a working proxy.

---

## 3. Why 应用宝 (Tencent MyApp) Has These Apps

Tencent Appstore (应用宝) is a Chinese app distribution platform developed and operated by Tencent. It primarily serves users of Android devices in the Chinese market, where Google Play Store has limited availability due to government restrictions. In 2017, it was approved by the Ministry of Industry and Information Technology as a "trusted" application store.

Tencent MyApp is currently the most popular Chinese app store, with 270 million monthly active users.

Chinese government apps like 交警12123 are distributed through approved domestic platforms because:

- They meet China's regulatory and licensing requirements
- They are vetted and monitored by relevant Chinese authorities
- The distribution infrastructure matches the app's backend systems

---

## 4. Summary: The Real Layers of the Problem

| Layer | Issue |
|---|---|
| **Network/GFW** | v2ray bypasses this ✅ |
| **Google Play license in China** | Google has no license to distribute in China ❌ |
| **Developer choice** | 交警12123 dev never submitted to Google Play ❌ |
| **App technical dependency** | App relies on Chinese backend services, not Google APIs ❌ |
| **Account region** | Google Play filters apps by account country ❌ |

---

## 5. What You Can Do

- **Install 应用宝 (Tencent MyApp)** on your Google Pixel and download the app from there. It works fine on any Android device.
- **Sideload the APK** directly from the official website or a trusted APK mirror — this is legal and common in China.
- You can also try major Chinese stores like **Huawei AppGallery**, **Xiaomi GetApps**, or **Baidu Mobile Assistant** as alternatives to 应用宝.

---

**Bottom line**: V2ray solves the *network censorship* problem but not the *developer distribution decision* problem. 交警12123 was never published on Google Play in the first place — it only exists on Chinese domestic app stores by deliberate choice, and no proxy can make it appear where it was never listed.

References:

- [Google Play Store in China: Everything You Need To Know – AppInChina](https://appinchina.co/blog/google-play-store-in-china-everything-you-need-to-know/)
- [Tencent Appstore – Wikipedia](https://en.wikipedia.org/wiki/Tencent_Appstore)
- [Top 10 Chinese App Stores – DigitalCreative](https://digitalcreative.cn/blog/top-chinese-app-stores)
- [How to Access Google Play Store in China – VPNDada](https://www.vpndada.com/access-google-play-store-china/)
- [Chinese App Store List – 24hChina](https://www.24hchina.com/chinese-app-store-list/)
