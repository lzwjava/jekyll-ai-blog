---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Fixing CocoaPod Ruby Mismatch on macOS
translated: false
type: note
---

I see what's happening: your system Ruby and gems setup is a bit mixed, and so the `pod deintegrate` command can’t find CocoaPods. Let’s walk through it:

---

### Problem

- You’re on macOS (`arm64` likely, M1/M2).
- You updated Ruby (to 3.4.1 via Homebrew).
- Your `pod` executable belongs to the older Ruby (3.3.0 gem path: `/opt/homebrew/lib/ruby/gems/3.3.0/bin/pod`).
- But now Ruby 3.4.1 is active, so it can’t find the `cocoapods` gems in the right location.

That mismatch is why it’s failing.

---

### Solutions

#### 1. Reinstall CocoaPods using the Ruby you’re actually running

```bash
gem install cocoapods
```

Then verify with:

```bash
which pod
pod --version
```

---

#### 2. If you’re using `brew`’s Ruby, it’s best to install CocoaPods via Homebrew too

```bash
brew install cocoapods
```

This avoids Ruby version mismatches entirely.

---

#### 3. If you’re using `rbenv` or `rvm`, ensure you’re in the correct Ruby version environment

For example, with `rbenv`:

```bash
rbenv global 3.4.1
gem install cocoapods
```

---

#### 4. Clean up old pod binary symlinks

Check where the orphaned `pod` command is coming from:

```bash
which pod
```

If it points to `/opt/homebrew/lib/ruby/gems/3.3.0/bin/pod`, remove that or update your `PATH` so it uses the correct one.

---

✅ Recommended (easy & stable): Just run

```bash
brew install cocoapods
```

and then retry:

```bash
pod deintegrate
```

---

Do you want me to help you **fix the PATH so it always picks the right pod** binary, or just the quickest reinstall fix?
