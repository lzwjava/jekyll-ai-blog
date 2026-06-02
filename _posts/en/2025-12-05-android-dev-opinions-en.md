---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Controversial Android Development Opinions
translated: false
type: note
---

Question: What are some unpopular or controversial opinions about Android development?

Answer:

Here are some genuinely unpopular (or at least heavily debated) opinions that regularly trigger strong reactions in the Android community. These are commonly expressed by experienced developers on Reddit, X/Twitter, Medium, and conferences, even if they’re downvoted or argued against:

- **Kotlin is overhyped and often makes code harder to read**
  Many seniors quietly believe Kotlin’s nullability, extension functions, coroutines, and DSLs have made a lot of codebases look like “write-only” code. They argue Java was more explicit and produced more maintainable large-scale apps.

- **Jetpack Compose is a mistake for anything beyond simple UIs**
  A significant minority thinks Compose’s reactive model creates unpredictable recompositions, terrible debugging stories, and massive APK bloat. They claim XML + ViewBinding + custom Views was faster, more performant, and easier to reason about in complex apps (banks, Uber-scale UIs, etc.).

- **The official Android documentation is mostly useless past the “Hello World” stage**
  Real-world Android development is learned from Stack Overflow, random GitHub repos, and reverse-engineering AOSP or Google’s own apps, not from developer.android.com.

- **Google doesn’t care about third-party developers**
  Every year Google ships features that only their own apps (Gmail, Maps, Photos) can realistically use properly due to hidden APIs, pre-installed privileges, or insane battery-optimization whitelists.

- **RxJava was better than Kotlin Flow/Coroutines for most use cases**
  A surprisingly large number of senior devs miss RxJava’s operator richness, backpressure handling, and testability, and think Flow is a half-baked replacement that only won because Google pushed it.

- **MVVM is a terrible architecture and has ruined Android codebases**
  The forced separation into ViewModel → Repository → UseCase → DataSource chains has created boilerplate hell and indirection nightmares. Many believe clean MVC or MVI (with unidirectional data flow) is superior.

- **Fragment is still the correct way to build complex UIs; single-activity architecture is a fad**
  Multi-activity + Fragment was more modular and memory-efficient than the current “one giant Activity with a NavGraph” religion.

- **Dagger/Hilt is unnecessary complexity**
  For 80–90 % of apps, manual dependency injection or lightweight libraries (Koin, Codgen) are faster and far less painful than the annotation-processing hell of Dagger.

- **Most Android developers can’t write performant code anymore**
  The shift to Kotlin + Compose + coroutines has hidden garbage-collection and threading issues so well that juniors (and many seniors) no longer understand memory, threads, or the view system—until the app starts janking at scale.

- **Firebase is a trap**
  It locks you into Google, kills your backend skills, and becomes insanely expensive once you have real traffic. Self-hosted or other BaaS solutions are better long-term.

- **Writing apps in Flutter or React Native is often a better choice than native Android in 2025**
  Especially for startups and non-Google-play-exclusive apps. The ecosystem fragmentation, Google’s constant API churn, and shrinking advantages of “native” make cross-platform less of a compromise than it was five years ago.

These opinions are genuinely unpopular—you’ll get downvoted to oblivion in most Android subreddits or Slack groups if you say them out loud—but they’re held by a non-trivial number of battle-scarred senior Android engineers.
