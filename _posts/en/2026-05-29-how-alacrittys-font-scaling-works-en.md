---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Alacritty's Font Scaling Works
translated: false
type: note
---

Now I have the full picture. Here's the answer:

---

**Why your font size resets every time you open Alacritty:**

When you scale the font size with `Cmd+=` / `Cmd+-` at runtime, it only changes `display.font_size` in memory. The code in `event.rs:921-927` shows this clearly:

```rust
fn change_font_size(&mut self, delta: f32) {
    let new_size = self.display.font_size.as_px().round() + delta;
    self.display.font_size = FontSize::from_px(new_size);
    // ... applies to display only, never written to config
}
```

On the next launch, Alacritty reads the config file and applies `config.font.size()` again. Since you have NO config file (`~/.config/alacritty/alacritty.toml` doesn't exist), it uses the hardcoded default: **11.25 pt** (see `font.rs:137`).

The `ResetFontSize` action (Ctrl+Cmd+0 on macOS) confirms this — it resets back to the config value:
```rust
fn reset_font_size(&mut self) {
    self.display.font_size = self.config.font.size().scale(scale_factor);
}
```

**The fix: create a config file with your desired size:**

```bash
mkdir -p ~/.config/alacritty
cat > ~/.config/alacritty/alacritty.toml << 'EOF'
[font]
size = 16.0

[font.normal]
family = "Menlo"
EOF
```

Adjust `size` to whatever you want (16.0 is a good starting point for Retina Macs). The font size is in **points**, and Alacritty applies DPI scaling automatically via `scale_factor`.

**Key insight from the code** (`window_context.rs:277-280`): even on config reload, Alacritty preserves your runtime font size change IF it differs from the old config. But on a fresh launch, there's nothing to preserve — it always reads from config, or falls back to the 11.25 pt default.
