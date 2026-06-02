---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hugging Face CLI Login Process Explained
translated: false
type: note
---

Here's how `hf auth login` works, traced through the code:

## Entry Point

You ran `hf auth login`, which hits the CLI command in `src/huggingface_hub/cli/auth.py:61`:

```python
@auth_cli.command("login", ...)
def auth_login(token, add_to_git_credential, force):
    login(token=token, add_to_git_credential=add_to_git_credential, skip_if_logged_in=not force)
```

This calls `login()` in `_login.py:59`. Since you didn't pass `--token`, `token=None`, so it detects you're in a terminal (not notebook) and calls `interpreter_login()`.

## Step 1: Prompt for token (`_login.py:236-272`)

`interpreter_login()` does exactly what you saw:

1. Prints the ASCII HF logo
2. Calls `getpass()` to read the token invisibly ("Enter your token (input will not be visible)")
3. Calls `typer.confirm("Add token as git credential?")` — the `[y/N]` prompt
4. Calls `_login(token, add_to_git_credential)`

## Step 2: Validate token against HF API (`_login.py:370-394`)

`_login()` does 3 things:

```python
def _login(token, add_to_git_credential):
    # 1. Reject org tokens
    if token.startswith("api_org"):
        raise ValueError(...)

    # 2. Call HF API to validate — whoami(token) hits https://huggingface.co/api/whoami-v2
    token_info = whoami(token)
    permission = token_info["auth"]["accessToken"]["role"]  # "read" or "write"
    logger.info(f"Token is valid (permission: {permission}).")

    # 3. Get the token's display name (e.g. "test1")
    token_name = token_info["auth"]["accessToken"]["displayName"]

    # 4. Save token to stored_tokens file
    _save_token(token=token, token_name=token_name)

    # 5. Set as active token (write to token file + optionally git credential)
    _set_active_token(token_name=token_name, add_to_git_credential=add_to_git_credential)
```

## Step 3: Token storage — two files (`_auth.py`)

**stored_tokens** — a multi-token INI file at `~/.cache/huggingface/stored_tokens`:

```python
# _save_token() at _auth.py:207
def _save_token(token, token_name):
    stored_tokens = get_stored_tokens()     # parse existing INI
    stored_tokens[token_name] = token        # add/update entry
    _save_stored_tokens(stored_tokens)       # rewrite INI file
```

The file looks like:
```ini
[test1]
hf_token = hf_xxxx...

[my-other-token]
hf_token = hf_yyyy...
```

Written with `0o600` file permissions via `_write_secret()` (owner-only read/write).

**active token** — a single file at `~/.cache/huggingface/token`:

```python
# _set_active_token() at _login.py:420
def _set_active_token(token_name, add_to_git_credential):
    token = _get_token_by_name(token_name)  # look up from stored_tokens
    _write_secret(Path(HF_TOKEN_PATH), token)  # write raw token to ~/.cache/huggingface/token
```

## Step 4: Git credential (`_login.py:433-439`)

If you said `y` to "Add token as git credential?":

```python
if add_to_git_credential:
    if _is_git_credential_helper_configured():
        set_git_credential(token)
```

This calls `git credential approve` to store the token in your system's git credential manager. On your Mac, that's `osxkeychain` (via `git-credential-manager`). This is what lets `git push` to `huggingface.co` repos authenticate automatically.

## Token resolution priority (`_auth.py:53-67`)

When the library needs a token later (e.g. `hf_hub_download`, `HfApi` calls):

```python
def get_token():
    return _get_token_from_google_colab()    # 1. Colab secrets vault
        or _get_token_from_environment()      # 2. HF_TOKEN env var
        or _get_token_from_file()             # 3. ~/.cache/huggingface/token file
```

Env var (`HF_TOKEN`) beats the file. Colab vault beats both.

## Summary of your output line-by-line

```
To log in, `huggingface_hub` requires a token...    # interpreter_login() prints prompt
Enter your token (input will not be visible):       # getpass()
Add token as git credential? [y/N]: y               # typer.confirm()
Token is valid (permission: write).                 # whoami(token) API call succeeded
The token `test1` has been saved to .../stored_tokens  # _save_token() — INI file
Your token has been saved in your configured git credential helpers (...,osxkeychain).
                                                    # set_git_credential() via git credential approve
Your token has been saved to .../token              # _write_secret() to active token file
Login successful.                                   # _login() returns
The current active token is: `test1`                # prints the displayName from API
```
