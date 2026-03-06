#!/usr/bin/env python3
"""
Sync scripts and tests from lzwjava.github.io to pyscripts repository.
This script copies relevant Python files and updates .gitignore accordingly.
"""

import shutil
import subprocess
from pathlib import Path


def main():
    """Main sync function."""
    # Define source and target directories
    source_dir = Path.home() / "projects" / "blog-source"
    target_dir = Path.home() / "projects" / "pyscripts"

    if not source_dir.exists():
        print(f"Source directory does not exist: {source_dir}")
        return

    if not target_dir.exists():
        print(f"Target directory does not exist: {target_dir}")
        return

    # Define patterns for files to sync
    patterns = [
        "scripts/**/*.py",
        "tests/**/*.py",
        "scripts/**/*.sh",
        "requirements*.txt",
        "pyproject.toml",
        "setup.py",
    ]

    # Files and directories to exclude
    exclude_patterns = [
        "__pycache__",
        "*.pyc",
        ".git",
        ".venv",
        "venv",
        "node_modules",
        ".pytest_cache",
    ]

    # Create target directory structure
    (target_dir / "scripts").mkdir(exist_ok=True)
    (target_dir / "tests").mkdir(exist_ok=True)

    md_root = target_dir / "md"
    md_root.mkdir(exist_ok=True)

    # Copy files based on patterns
    for pattern in patterns:
        source_files = source_dir.glob(pattern)
        for source_file in source_files:
            if source_file.is_file():
                # Calculate relative path
                relative_path = source_file.relative_to(source_dir)
                target_file = target_dir / relative_path

                # Create parent directories
                target_file.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                print(f"Copying {source_file} -> {target_file}")
                shutil.copy2(source_file, target_file)

                maybe_create_markdown_mirror(source_file, relative_path, md_root)

    # Update .gitignore
    gitignore_path = target_dir / ".gitignore"
    update_gitignore(gitignore_path, exclude_patterns)

    print("Sync completed successfully!")
    run_git_operations(target_dir)


def update_gitignore(gitignore_path, patterns):
    """Update .gitignore file with exclude patterns."""
    # Read existing .gitignore if it exists
    existing_patterns = set()
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            existing_patterns = {
                line.strip() for line in f if line.strip() and not line.startswith("#")
            }

    # Add new patterns
    new_patterns = set(patterns) - existing_patterns

    if new_patterns:
        with open(gitignore_path, "a") as f:
            if existing_patterns:
                f.write("\n# Added by sync script\n")
            for pattern in sorted(new_patterns):
                f.write(f"{pattern}\n")
        print(f"Updated {gitignore_path} with {len(new_patterns)} new patterns")
    else:
        print("No new patterns to add to .gitignore")


def run_git_operations(repo_dir: Path) -> None:
    """Run git add/commit/push in the target repository if changes exist."""
    try:
        if not has_git_changes(repo_dir):
            print("No git changes detected; skipping commit and push.")
            return

        subprocess.run(["git", "add", "-A"], cwd=repo_dir, check=True)
        subprocess.run(
            ["git", "commit", "-m", "update scripts"], cwd=repo_dir, check=True
        )
        subprocess.run(["git", "push"], cwd=repo_dir, check=True)
        print("Committed and pushed updates to remote.")
    except subprocess.CalledProcessError as err:
        print(f"Git command failed: {err}")


def has_git_changes(repo_dir: Path) -> bool:
    """Check whether the repository has unstaged or uncommitted changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return bool(result.stdout.strip())


def maybe_create_markdown_mirror(
    source_file: Path, relative_path: Path, md_root: Path
) -> None:
    """Create a Markdown mirror of the source file when extension is supported."""
    if source_file.suffix not in {".py", ".sh"}:
        return

    md_target = (md_root / relative_path).with_suffix(".md")
    md_target.parent.mkdir(parents=True, exist_ok=True)

    try:
        original_content = source_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"Skipping Markdown mirror for non-text file: {source_file}")
        return

    fenced_lang = "py"
    frontmatter = (
        "---\n"
        f"title: {source_file.name}\n"
        f"path: {relative_path.as_posix()}\n"
        "---\n\n"
    )

    md_body = f"```{fenced_lang}\n{original_content}\n```\n"
    md_target.write_text(frontmatter + md_body, encoding="utf-8")
    print(f"Created Markdown mirror: {md_target}")


if __name__ == "__main__":
    main()
