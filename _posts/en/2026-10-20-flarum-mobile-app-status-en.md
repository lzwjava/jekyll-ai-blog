---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flarum Mobile App Status
translated: false
type: note
---

**Question:** Does Flarum have a mobile app?

**Answer:**

**No official app exists.** Here's the current state:

**PWA (Progressive Web App) — Best Option**

- Flarum supports PWA via an extension, allowing both Android and iOS users to "install" it like an app from the browser.
- You can also use PWABuilder once you have installed the PWA extension to build packages for iOS and Android.
- Android supports push notifications via PWA; iOS support depends on your iOS version.

**Unofficial / Community Apps**

- There is a community-built Flarum iOS app demo using SwiftUI, offering features like login, browsing discussions, replying, tag support, user profiles, and dark mode — but it requires self-compilation and is tied to a specific Flarum install URL.
- Flarum BV (the commercial companion to the Flarum Foundation) has been working on wrapping the PWA extension into an Android and iOS app and offering to publish it to app stores for communities for a small fee.

**Why No Official App?**

- Making an app is a complex process involving a lot of effort — both one-time and long-term maintenance — and the Flarum team currently does not have the necessary resources to tackle such a project.

**Compared to Discourse**, which has the official **DiscourseHub** app on both iOS and Android, this is a notable gap for Flarum.

**Recommendation:** For most users, installing Flarum as a **PWA** is the easiest path to a near-native app experience right now.

**References:**

- [Flarum Community - Push Notifications & App Support](https://discuss.flarum.org/d/31898-edition-422-community-update)
- [Flarum iOS App (Unofficial, SwiftUI)](https://discuss.flarum.org/d/33090-flarum-ios-app-demo-swiftui)
- [Building and Publishing Flarum Apps to iOS and Android](https://discuss.flarum.org/d/34301-building-and-publishing-your-flarum-apps-to-ios-and-android)
