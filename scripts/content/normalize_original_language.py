#!/usr/bin/env python3
"""Normalize language of files under original/ to English.

This script:
- Finds all markdown files in `original/` ending with `-zh.md` or `-ja.md`.
- Moves those files into a backup directory (default: `backup/original/`).
- For each moved file, looks for the corresponding English post in `_posts/en/`
  by replacing the language suffix with `-en.md` and, if found, copies it to
  `original/` with the `-en.md` suffix.

Usage:
  Dry run (default):
    python scripts/content/normalize_original_language.py

  Apply changes:
    python scripts/content/normalize_original_language.py --apply

Options:
  --apply           Actually perform moves/copies. Without it, prints actions.
  --backup-dir DIR  Where to move zh/ja originals (default: backup/original/).

Notes:
- If an English file already exists in `original/`, the copy step is skipped.
- If no matching `_posts/en/<name>-en.md` is found, the script reports it.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_DIR = ROOT / "original"
POSTS_EN_DIR = ROOT / "_posts" / "en"
DEFAULT_BACKUP_DIR = ROOT / "backup" / "original"


def find_lang_files(base_dir: Path, suffixes: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for suf in suffixes:
        files.extend(sorted(base_dir.glob(f"*-{suf}.md")))
    return files


def to_en_filename(path: Path) -> Path:
    name = path.name
    for lang in ("zh", "ja"):
        if name.endswith(f"-{lang}.md"):
            return path.with_name(name.replace(f"-{lang}.md", "-en.md"))
    return path


def plan_actions(
    files: List[Path], backup_dir: Path
) -> List[Tuple[str, Path, Path | None]]:
    """Return a list of actions to take.

    Each tuple: (action, src, dst)
    - ("move", src, dst) move src -> dst (dst inside backup_dir)
    - ("copy_en", src_en, dst_original_en) copy _posts/en/src_en -> original/dst_original_en
    """
    actions: List[Tuple[str, Path, Path | None]] = []
    for f in files:
        # move the zh/ja original into backup
        dst_in_backup = backup_dir / f.name
        actions.append(("move", f, dst_in_backup))

        # compute expected en names and copy if available
        en_name_in_original = to_en_filename(f)
        en_name_only = en_name_in_original.name
        src_in_posts_en = POSTS_EN_DIR / en_name_only
        dst_in_original_en = ORIGINAL_DIR / en_name_only

        if src_in_posts_en.exists():
            if not dst_in_original_en.exists():
                actions.append(("copy_en", src_in_posts_en, dst_in_original_en))
            else:
                # English already present in original; skip copying
                pass
        else:
            # No source English file found; nothing to copy
            pass

    return actions


def ensure_dir(path: Path, apply: bool) -> None:
    if path.exists():
        return
    if apply:
        path.mkdir(parents=True, exist_ok=True)


def run(actions: List[Tuple[str, Path, Path | None]], apply: bool) -> None:
    move_count = 0
    copy_count = 0
    missing_en: List[Path] = []

    for action, src, dst in actions:
        if action == "move":
            # src: original/*-(zh|ja).md, dst: backup/original/<same name>
            if apply:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not src.exists():
                    print(f"[skip] missing source to move: {src}")
                else:
                    shutil.move(str(src), str(dst))
                    print(f"[move] {src} -> {dst}")
                    move_count += 1
            else:
                print(f"[plan move] {src} -> {dst}")
        elif action == "copy_en":
            # src: _posts/en/<name>-en.md, dst: original/<name>-en.md
            if apply:
                dst_parent = dst.parent if isinstance(dst, Path) else ORIGINAL_DIR
                dst_parent.mkdir(parents=True, exist_ok=True)
                if not src.exists():
                    print(f"[warn] English source not found: {src}")
                    missing_en.append(src)
                elif isinstance(dst, Path) and dst.exists():
                    print(f"[skip] already exists: {dst}")
                else:
                    shutil.copy2(str(src), str(dst))
                    print(f"[copy] {src} -> {dst}")
                    copy_count += 1
            else:
                print(f"[plan copy] {src} -> {dst}")
        else:
            print(f"[unknown action] {action} {src} -> {dst}")

    print(f"\nSummary: moves={move_count}, copies={copy_count}")
    if missing_en:
        print("Missing English sources:")
        for p in missing_en:
            print(f"  - {p}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize original/ language to English by moving zh/ja and copying en."
    )
    parser.add_argument(
        "--apply", action="store_true", help="Apply changes (otherwise dry run)"
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=DEFAULT_BACKUP_DIR,
        help="Backup directory for zh/ja originals",
    )
    args = parser.parse_args()

    if not ORIGINAL_DIR.exists():
        raise SystemExit(f"original/ directory not found at {ORIGINAL_DIR}")
    if not POSTS_EN_DIR.exists():
        raise SystemExit(f"_posts/en/ directory not found at {POSTS_EN_DIR}")

    ensure_dir(args.backup_dir, apply=args.apply)

    targets = find_lang_files(ORIGINAL_DIR, suffixes=("zh", "ja"))
    if not targets:
        print("No zh/ja files found in original/.")
        return

    actions = plan_actions(targets, backup_dir=args.backup_dir)

    # Report any zh/ja files that do not have en sources in _posts/en/
    for f in targets:
        en_name = to_en_filename(f).name
        src_en = POSTS_EN_DIR / en_name
        if not src_en.exists():
            print(
                f"[info] No matching _posts/en/ for {f.name} -> expected {src_en.name}"
            )

    run(actions, apply=args.apply)


if __name__ == "__main__":
    main()
