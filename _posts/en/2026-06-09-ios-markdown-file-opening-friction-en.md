---
audio: false
generated: true
image: false
lang: en
layout: post
title: iOS Markdown File Opening Friction
translated: false
type: note
---

**Question:** Why is it so hard to open markdown files on iOS despite having hundreds of apps installed, and why did declaring .md file type support matter?

**Answer:**

This is a sandbox + file type declaration problem that exposes iOS's intentional friction against "universal" file opening. Here's what's happening under the hood.

## The iOS File Type Architecture

iOS doesn't have a global file extension → app mapping like Windows/macOS. Instead, apps must *explicitly declare* support for file types in their `Info.plist`. When you tap a `.md` file in WeChat, iOS queries all installed apps asking: "Who claims to handle `public.plain-text` or `com.markdown`?" Only apps that registered these types appear in the share sheet.

Most of your 200-300 apps never registered markdown support — even if they *could* read markdown.

**Example: What Notion's Info.plist does NOT include:**

```xml
<!-- Notion's actual Info.plist (simplified) -->
<key>CFBundleDocumentTypes</key>
<array>
  <!-- Notion declares support for web clips, images, etc -->
  <!-- But NOT .md files explicitly -->
</array>
```

Notion parses markdown *internally* for display, but doesn't declare `public.plain-text` or markdown UTTypes as something it handles when you try to open a file. The app can render markdown, but iOS's sandbox says "you can't receive .md files from outside your sandbox" without explicit declaration.

**Why read.md works:**

```xml
<!-- read.md's Info.plist -->
<key>CFBundleDocumentTypes</key>
<array>
  <dict>
    <key>CFBundleTypeRole</key>
    <string>Editor</string>
    <key>LSItemContentTypes</key>
    <array>
      <string>public.plain-text</string>
      <string>com.markdown</string>  <!-- Explicitly declares markdown -->
      <string>public.text</string>
    </array>
  </dict>
</array>
```

It declares itself as a handler. iOS now knows: "User tapped .md → ask read.md."

## Why DuckDuckGo Browser Doesn't Appear

Browsers are special-cased. They handle `http://` and `https://` schemes, not file types. A `.md` file isn't a URL — it's a document in the sandbox. The share sheet never includes browsers for local files. (This is intentional: Apple wanted to prevent apps from intercepting documents.)

## Why This Design Exists (The Real Reason)

This isn't a bug — it's enforced friction:

1. **Security**: Without explicit declaration, malicious apps can't silently intercept files. An app that secretly handles .md files and tries to exfiltrate your notes can't — it has to declare intent first.

2. **Sandbox model**: iOS enforces one-way communication. Apps can't reach into WeChat's sandbox and read files unless WeChat explicitly hands them over (via share sheet). The receiving app has to have declared "I accept this type."

3. **App discoverability incentive**: Apple wants you to download *specialized* apps instead of relying on generic file handlers. read.md exists because someone saw demand. Notion doesn't need to declare markdown support because users open notes *inside* Notion, not outside.

## What You Actually Need on iOS

For markdown files, your options are:

- **Dedicated markdown readers**: read.md, iA Writer, Ulysses, Markdown Editor (declare .md support)
- **Code editors**: Working Copy (Git), Xcode Playgrounds, Runestone (all declare text/markdown)
- **Text editors that DO declare support**: Some do (check their App Store description)
- **Workaround**: CloudKit sync to Notes.app or iCloud Drive, then open from there (bypasses share sheet friction)

## The Deeper Pattern

This is why iOS feels more "opinionated" than macOS. On macOS, you'd double-click `file.md` and the system checks file associations. On iOS, you hit friction to nudge you toward specialized, curated apps. It's by design — not a limitation, but a philosophy.

If you're building iOS apps and want to handle markdown files, add to your `Info.plist`:

```xml
<key>UTImportedTypeDeclarations</key>
<array>
  <dict>
    <key>UTTypeIdentifier</key>
    <string>com.markdown</string>
    <key>UTTypeConformsTo</key>
    <array><string>public.plain-text</string></array>
    <key>UTTypeTagSpecification</key>
    <dict>
      <key>public.filename-extension</key>
      <array><string>md</string><string>markdown</string></array>
    </dict>
  </dict>
</array>
```

Then declare your app handles it. Now users will see your app in the share sheet.
