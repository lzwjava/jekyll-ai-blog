---
audio: false
generated: true
image: false
lang: en
layout: post
title: Managing Spotlight Indexing on macOS
translated: false
type: note
---

You have a few options, from gentle to nuclear:

    Option A: Stop the spike now (indexing will resume later)


    sudo mdutil -a -i off


    Turns off indexing on all volumes immediately. The mdworker processes will finish and die. Indexing stays off until you turn it back on with sudo mdutil -a -i on.

    Option B: Add Spotlight exclusions (recommended)

    In System Settings > Siri & Spotlight > Search Privacy, drag in:
    - ~/Projects/ or wherever your node_modules live
    - ~/Library/Caches/
    - ~/Downloads/

    Or from CLI:

    sudo mdutil -E /
    sudo mdutil -i off /Users/lzwjava

    This erases the index and stops indexing your home folder, while keeping system-wide indexing for search.

    Option C: Kill Spotlight permanently (no more search)


    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.metadata.mds.plist


    This unregisters the Spotlight daemon so it never starts again, even after reboot. Cmd+Space search will stop working. You can reverse it with load instead of unload.

    Option D: Just kill the current hogging processes


    sudo pkill mdworker
    sudo pkill mds


    The processes die now but restart within a minute. This is a temporary band-aid.



    My recommendation: Option B — stop indexing your home folder. You keep Spotlight search for apps/system but it won't crawl node_modules, caches, or your massive ~/Projects tree ever again. That 250% CPU spike after every reboot disappears.

    Want me to run it?
