---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp Custom Git Bash Path Guide
translated: false
type: note
---

Based on the code, here's the answer:

## Custom Executable Path for Git Bash in Warp (Windows)

### Path Separator: Use `\` (backslash)

From `resolve_executable` in `app/src/util/path.rs:97`:

```rust
if command.contains(path::MAIN_SEPARATOR) {
    let path = Path::new(command);
    return file_exists_and_is_executable(path).then_some(Cow::Borrowed(path));
}
```

On Windows, `path::MAIN_SEPARATOR` is `\`. The code checks if your input contains the OS separator to decide whether to treat it as a direct path vs a PATH lookup. So use:

```
C:\Program Files\Git\usr\bin\bash.exe
```

Forward slashes `/` will NOT be recognized as a path separator and will trigger a PATH lookup instead (which will fail for an absolute path like `C:/Program Files/...`).

### `--login -i` Arguments: Warp Adds Them Automatically

You do NOT need to specify `--login -i` in the custom path field.

From `msys2_arguments_for_session_spawning_command` in `app/src/terminal/local_tty/shell.rs:685-704`:

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

And from `ShellStarter::init` at line 79-94, when Warp detects a Git Bash path (via `is_msys2_path`), it automatically creates an `MSYS2` shell starter with these args.

For non-MSYS2 bash, it uses `arguments_for_session_spawning_command` (line 574-605) which wraps bash with `-c 'exec -a bash <path> --rcfile <(echo <init_script>)'`.

Key: Warp manages the bootstrap arguments itself. The custom path field is just the executable path.

### What Happens When You Type a Custom Path

1. **Settings UI** (`startup_shell.rs:186`): `AvailableShell::try_from(buffer_text.as_str())` is called
2. **Validation** (`local_tty/shell.rs:543`): `resolve_executable` checks the path exists and is executable
3. **Git Bash detection** (`local_tty/shell.rs:80-94`): `canonicalize_git_bash_path` converts `Git\bin\bash.exe` → `Git\usr\bin\bash.exe`, then `is_msys2_path` checks if it's an MSYS2 shell
4. **If MSYS2 detected**: Warp creates `ShellStarter::MSYS2` with `--noprofile --norc` args (not `--login -i`)
5. **If not MSYS2**: Warp creates `ShellStarter::Direct` with the standard bash bootstrap args

### Summary

| Setting | Value |
|---------|-------|
| Custom path | `C:\Program Files\Git\usr\bin\bash.exe` |
| Path separator | `\` (backslash) |
| `--login -i` | Don't add — Warp handles shell args automatically |
| Default shell | Select "Custom" in Settings → Features, paste the path |