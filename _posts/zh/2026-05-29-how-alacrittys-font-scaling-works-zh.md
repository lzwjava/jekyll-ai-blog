---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Alacritty 字体缩放的工作原理
translated: true
type: note
---

**为什么每次打开 Alacritty 时字体大小都会重置：**

当你在运行时使用 `Cmd+=` / `Cmd+-` 缩放字体大小时，它只会更改内存中的 `display.font_size`。`event.rs:921-927` 中的代码清晰地显示了这一点：

```rust
fn change_font_size(&mut self, delta: f32) {
    let new_size = self.display.font_size.as_px().round() + delta;
    self.display.font_size = FontSize::from_px(new_size);
    // ... 仅应用于显示，从不写入配置
}
```

下次启动时，Alacritty 会读取配置文件并再次应用 `config.font.size()`。由于你没有配置文件（`~/.config/alacritty/alacritty.toml` 不存在），它会使用硬编码的默认值：**11.25 pt**（参见 `font.rs:137`）。

`ResetFontSize` 操作（macOS 上为 Ctrl+Cmd+0）证实了这一点——它会重置回配置值：
```rust
fn reset_font_size(&mut self) {
    self.display.font_size = self.config.font.size().scale(scale_factor);
}
```

**解决方法：创建一个包含你所需大小的配置文件：**

```bash
mkdir -p ~/.config/alacritty
cat > ~/.config/alacritty/alacritty.toml << 'EOF'
[font]
size = 16.0

[font.normal]
family = "Menlo"
EOF
```

将 `size` 调整为你想要的任何值（16.0 对于 Retina Macs 来说是一个不错的起点）。字体大小以**磅**为单位，Alacritty 会通过 `scale_factor` 自动应用 DPI 缩放。

**代码中的关键点**（`window_context.rs:277-280`）：即使在重新加载配置时，如果运行时字体大小与旧配置不同，Alacritty 会保留你的运行时更改。但如果是全新启动，则没有任何内容需要保留——它始终从配置读取，或者回退到 11.25 pt 的默认值。