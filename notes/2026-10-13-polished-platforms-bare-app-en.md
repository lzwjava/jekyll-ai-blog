---
audio: false
generated: true
image: false
lang: en
layout: post
title: Polished Platforms, Bare App
translated: false
type: note
---

Current state of the repo (branch `main`, clean, up to date with `origin/main`):

**App code — essentially at square one**

- `lib/main.dart` is the only Dart file — a bare "Hello World!" MaterialApp.
- Dependencies `flutter_markdown`, `path_provider`, `yaml` are declared in `pubspec.yaml`, but none are used in code yet.
- The old blog posts (`assets/_posts/*.md`, both EN and ZH) were deleted back in Dec 2024, and no `assets:` section is registered in `pubspec.yaml`.

**Recent work (last few commits) — platform/config polish**

- `bc085e6` — updated web app icons (Icon-192, Icon-512)
- `63159d6` — added iOS development team, updated Xcode scheme
- `90a6159` / `0804f1b` — bumped iOS deployment target to 16.0, added Podfile.lock
- Full multi-platform scaffolding exists: `android/`, `ios/`, `web/`, `macos/`, `linux/`, `windows/`

**Summary:** infrastructure is set up (platforms buildable, iOS signing configured, icons done), but the actual blog feature hasn't been rebuilt yet — no post loading, no markdown rendering, no UI beyond the hello-world screen.

Natural next steps would be: restore the posts (or fetch them from wherever they live now), register them as assets, and build a post list + markdown reader screen. Want me to start on that?
