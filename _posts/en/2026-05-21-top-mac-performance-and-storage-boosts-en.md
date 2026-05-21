---
audio: false
generated: true
image: false
lang: en
layout: post
title: Top Mac Performance and Storage Boosts
translated: false
type: note
---

Here are the **highest-impact things you can do right now**, ranked by ROI:

---

### Biggest Wins

| Action | Saves | How |
|---|---|---|
| **Clear JetBrains cache** | ~7 GB | `rm -rf ~/Library/Caches/JetBrains/` |
| **Homebrew cleanup** | ~3 GB | `brew cleanup --prune=all` |
| **pip cache purge** | ~2.4 GB | `pip cache purge` |
| **Clear WeChat cache** | ~5-10 GB | WeChat Settings > Storage > Clear |
| **Close Vivaldi/Safari tabs** | ~10 GB RAM | Close what you don't need |
| **Quit WeChat when not using** | ~5-19 GB RAM | Just quit the app |
| **Quit idle VSCode projects** | ~15 GB RAM | Close unused windows |
| **Switch input method** (WeType→Apple) | ~3.5 GB RAM | System Settings > Keyboard |

### Additional considerations

- **Spotlight indexing** — the 250% CPU spike is normal after boot. Give it 15 min. You can exclude `node_modules/`, `~/Projects/`, `~/Library/Caches/` in Spotlight Privacy settings to keep it fast long-term.
- **48GB free** — I'd aim for >100GB. Safest cleanup: JetBrains cache + Homebrew + pip alone frees ~12GB.

---

Want me to run any of the cleanups? I can also recommend what to move to your remote RTX 4070 machine (compilation, ML, heavy dev) so this laptop stays lean as a thin client.