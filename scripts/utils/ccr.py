#!/usr/bin/env python3
"""
Copy the commonly used Claude Code command to the clipboard for easy pasting.

Prefers pyperclip; falls back to platform clipboard tools when available.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from typing import Optional

COMMAND: str = "CLAUDE_CODE_MAX_OUTPUT_TOKENS=100000 ccr code"


def copy_to_clipboard(text: str) -> Optional[str]:
    """Copy text to clipboard using pyperclip if available, else fallback.

    Returns a short string indicating the method on success, or None on failure.
    """
    try:
        import pyperclip  # type: ignore

        pyperclip.copy(text)
        return "pyperclip"
    except Exception:
        # Fall back to common platform tools
        if sys.platform == "darwin" and shutil.which("pbcopy"):
            try:
                proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
                assert proc.stdin is not None
                proc.stdin.write(text.encode("utf-8"))
                proc.stdin.close()
                proc.wait(timeout=2)
                return "pbcopy"
            except Exception:
                pass

        if sys.platform.startswith("linux"):
            if shutil.which("xclip"):
                try:
                    subprocess.run(
                        ["xclip", "-selection", "clipboard"],
                        input=text.encode("utf-8"),
                        check=True,
                    )
                    return "xclip"
                except Exception:
                    pass
            if shutil.which("xsel"):
                try:
                    subprocess.run(
                        ["xsel", "--clipboard", "--input"],
                        input=text.encode("utf-8"),
                        check=True,
                    )
                    return "xsel"
                except Exception:
                    pass

        if sys.platform.startswith("win") and shutil.which("clip"):
            try:
                subprocess.run(["clip"], input=text.encode("utf-16le"), check=True)
                return "clip"
            except Exception:
                pass

    return None


def main() -> None:
    method = copy_to_clipboard(COMMAND)
    if method:
        print(f"Copied to clipboard via {method}. Paste in your terminal.")
        print(f"Command: {COMMAND}")
    else:
        print(COMMAND)
        print(
            "Clipboard unavailable. Printed instead. Install pyperclip: pip install pyperclip",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
