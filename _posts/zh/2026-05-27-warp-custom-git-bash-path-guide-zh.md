---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Warp中自定义Git Bash路径指南
translated: true
type: note
---

根据代码，以下是答案：

## Warp（Windows）中 Git Bash 的自定义可执行路径

### 路径分隔符：使用 `\`（反斜杠）

来自 `app/src/util/path.rs:97` 中的 `resolve_executable`：

```rust
if command.contains(path::MAIN_SEPARATOR) {
    let path = Path::new(command);
    return file_exists_and_is_executable(path).then_some(Cow::Borrowed(path));
}
```

在 Windows 上，`path::MAIN_SEPARATOR` 是 `\`。代码检查你的输入是否包含操作系统分隔符，以决定是将其视为直接路径还是进行 PATH 查找。因此请使用：

```
C:\Program Files\Git\usr\bin\bash.exe
```

正斜杠 `/` **不会**被识别为路径分隔符，而是会触发 PATH 查找（对于像 `C:/Program Files/...` 这样的绝对路径，查找会失败）。

### `--login -i` 参数：Warp 会自动添加

你**不需要**在自定义路径字段中指定 `--login -i`。

来自 `app/src/terminal/local_tty/shell.rs:685-704` 中的 `msys2_arguments_for_session_spawning_command`：

```rust
fn msys2_arguments_for_session_spawning_command(shell_type: ShellType) -> Vec<OsString> {
    match shell_type {
        ShellType::Bash => {
            vec![
                "--noprofile".to_string().into(),
                "--norc".to_string().into(),
            ]
        }
        // ...
    }
}
```

并且来自 `ShellStarter::init`（第 79-94 行），当 Warp 检测到 Git Bash 路径（通过 `is_msys2_path`）时，它会自动创建一个带有这些参数的 `MSYS2` shell 启动器。

对于非 MSYS2 的 bash，它使用 `arguments_for_session_spawning_command`（第 574-605 行），该函数用 `-c 'exec -a bash <path> --rcfile <(echo <init_script>)'` 包装 bash。

关键点：Warp 自行管理引导参数。自定义路径字段仅用于可执行文件的路径。

### 当你输入自定义路径时会发生什么

1. **设置界面**（`startup_shell.rs:186`）：调用 `AvailableShell::try_from(buffer_text.as_str())`
2. **验证**（`local_tty/shell.rs:543`）：`resolve_executable` 检查路径是否存在且可执行
3. **Git Bash 检测**（`local_tty/shell.rs:80-94`）：`canonicalize_git_bash_path` 将 `Git\bin\bash.exe` 转换为 `Git\usr\bin\bash.exe`，然后 `is_msys2_path` 检查它是否为 MSYS2 shell
4. **如果检测到 MSYS2**：Warp 创建带有 `--noprofile --norc` 参数的 `ShellStarter::MSYS2`（而不是 `--login -i`）
5. **如果不是 MSYS2**：Warp 创建带有标准 bash 引导参数的 `ShellStarter::Direct`

### 总结

| 设置项 | 值 |
|--------|-----|
| 自定义路径 | `C:\Program Files\Git\usr\bin\bash.exe` |
| 路径分隔符 | `\`（反斜杠） |
| `--login -i` | 不要添加——Warp 会自动处理 shell 参数 |
| 默认 shell | 在“设置”→“功能”中选择“自定义”，粘贴路径 |