---
audio: false
generated: true
image: false
lang: en
layout: post
title: 'Black: Python Code Formatter Guide'
translated: false
type: note
---

Black is an opinionated, uncompromising Python code formatter developed by the Python Software Foundation (PSF). It automatically reformats Python code to conform to a consistent style, primarily based on a strict subset of PEP 8, while emphasizing readability, consistency, and minimal diffs in version control. By using Black, developers agree to relinquish control over minor formatting details in exchange for speed, determinism, and reduced debates over style during code reviews. Black ensures that formatted ("blackened") code looks uniform across projects, saving time and mental energy for more critical aspects of development. It supports Python 3.8 and later, with the latest stable release being version 25.1.0 (released on January 29, 2025), which introduces the 2025 stable style with enhancements like normalized Unicode escape casing and improved handling of trailing commas.

Black's philosophy prioritizes:

- **Consistency**: Similar constructs are formatted identically.
- **Generality**: Rules apply broadly without special cases.
- **Readability**: Focuses on easy-to-read code.
- **Diff Minimization**: Reduces changes in Git diffs to speed up reviews.

It's widely used in open-source and professional projects for its reliability and integration capabilities.

## Installation

Black is available on PyPI and can be installed using pip. It's recommended to install it in a virtual environment for project isolation.

- Basic installation:

  ```
  pip install black
  ```

- For additional features like Jupyter Notebook support or colorized diffs:

  ```
  pip install 'black[jupyter,colorama]'
  ```

  (The `d` extra is for blackd, a daemon for editor integrations.)

On Arch Linux, you can install via the package manager: `pacman -S python-black`.

Black can also be installed via conda or other package managers. After installation, verify with `black --version`.

For development or testing, you can clone the GitHub repository and install in editable mode:

```
git clone https://github.com/psf/black.git
cd black
pip install -e .
```

## Usage

Black is primarily a command-line tool. The basic command formats files or directories in place:

```
black {source_file_or_directory}
```

If running Black as a script doesn't work (e.g., due to environment issues), use:

```
python -m black {source_file_or_directory}
```

### Key Command-Line Options

Black offers various flags for customization and control. Here's a summary of the main ones:

- `-h, --help`: Display help and exit.
- `-c, --code <code>`: Format a string of code (e.g., `black --code "print ( 'hello, world' )"` outputs the formatted version).
- `-l, --line-length <int>`: Set line length (default: 88).
- `-t, --target-version <version>`: Specify Python versions for compatibility (e.g., `py38`, can specify multiple like `-t py311 -t py312`).
- `--pyi`: Treat files as typing stubs (`.pyi` style).
- `--ipynb`: Treat files as Jupyter Notebooks.
- `--python-cell-magics <magic>`: Recognize custom Jupyter magics.
- `-x, --skip-source-first-line`: Skip formatting the first line (useful for shebangs).
- `-S, --skip-string-normalization`: Don't normalize strings to double quotes or prefixes.
- `-C, --skip-magic-trailing-comma`: Ignore trailing commas for line breaking.
- `--preview`: Enable experimental style changes for the next release.
- `--unstable`: Enable all preview changes plus unstable features (requires `--preview`).
- `--enable-unstable-feature <feature>`: Enable specific unstable features.
- `--check`: Check if files need reformatting without changing them (exit code 1 if changes needed).
- `--diff`: Show a diff of changes without writing files.
- `--color / --no-color`: Colorize the diff output.
- `--line-ranges <ranges>`: Format specific line ranges (e.g., `--line-ranges=1-10`).
- `--fast / --safe`: Skip (`--fast`) or enforce (`--safe`) AST safety checks (default: safe).
- `--required-version <version>`: Require a specific Black version.
- `--exclude <regex>`: Exclude files/directories via regex.
- `--extend-exclude <regex>`: Add to default exclusions.
- `--force-exclude <regex>`: Exclude even if explicitly passed.
- `--include <regex>`: Include files/directories via regex.
- `-W, --workers <int>`: Set number of parallel workers (default: CPU count).
- `-q, --quiet`: Suppress non-error messages.
- `-v, --verbose`: Show detailed output.
- `--version`: Display Black version.
- `--config <file>`: Load config from a file.

### Examples

- Format a single file: `black example.py`
- Check without formatting: `black --check .`
- Show diff: `black --diff example.py`
- Format stdin: `echo "print('hello')" | black -`
- Format with custom line length: `black -l 79 example.py`
- Format Jupyter Notebook: `black notebook.ipynb`

### Tips and Notes

- Black formats entire files; use `# fmt: off` / `# fmt: on` to skip blocks or `# fmt: skip` for lines.
- For stdin, use `--stdin-filename` to respect exclusions.
- Black is deterministic: same input always yields the same output.
- Use `--preview` to test upcoming styles, but note they may change.

## Configuration

Black can be configured via command-line flags or a `pyproject.toml` file (preferred for projects). Configuration in `pyproject.toml` goes under a `[tool.black]` section.

### Using pyproject.toml

Example:

```
[tool.black]
line-length = 79
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
skip-string-normalization = true
```

Supported options mirror CLI flags (e.g., `line-length`, `skip-string-normalization`). Multi-value options like `target-version` use arrays.

### Precedence

- Command-line flags override config file settings.
- If no `pyproject.toml` is found, Black uses defaults and searches parent directories.
- Use `--config` to specify a custom config file.

### File Discovery and Ignoring

Black automatically discovers Python files in directories, respecting `.gitignore` by default. Use `--include`/`--exclude` to customize. It ignores common directories like `.git`, `.venv`, etc., unless overridden.

For version control, integrate with tools like pre-commit to enforce formatting.

## The Black Code Style

Black enforces a specific style with limited configurability. Key rules:

### Line Length

- Default: 88 characters. May exceed if unbreakable (e.g., long strings).

### Strings

- Prefers double quotes; normalizes prefixes to lowercase (e.g., `r` before `f`).
- Lowers escape sequences (except `\N` names).
- Processes docstrings: fixes indentation, removes extra whitespace/newlines, preserves tabs in text.

### Numeric Literals

- Lowercase syntactic parts (e.g., `0xAB`), uppercase digits.

### Line Breaks and Operators

- Breaks before binary operators.
- Single spaces around most operators; no spaces for unary/power with simple operands.

### Trailing Commas

- Adds to multi-line collections/function args (if Python 3.6+).
- "Magic" trailing comma explodes lists if present.

### Comments

- Two spaces before inline comments; one space before text.
- Preserves special spacing for shebangs, doc comments, etc.

### Indentation

- 4 spaces; matches brackets with dedented closers.

### Empty Lines

- Minimal whitespace: single in functions, double at module level.
- Specific rules for docstrings, classes, and functions.

### Imports

- Splits long imports; compatible with isort's `black` profile.

### Other Rules

- Prefers parentheses over backslashes.
- Normalizes line endings based on file.
- Terse style for `.pyi` files (e.g., no extra lines between methods).
- Collapses empty lines after imports in preview mode.

Black aims to reduce diffs and improve readability, with changes mostly for bug fixes or new syntax support.

## Integrations

Black integrates seamlessly with editors and version control for automated formatting.

### Editors

- **VS Code**: Use the Python extension with Black as formatter. Set `"python.formatting.provider": "black"` in settings.json. For LSP, install python-lsp-server and python-lsp-black.
- **PyCharm/IntelliJ**:
  - Built-in (2023.2+): Settings > Tools > Black, configure path.
  - External Tool: Settings > Tools > External Tools, add Black with `$FilePath$` argument.
  - File Watcher: For auto-format on save.
  - BlackConnect plugin for daemon-based formatting.
- **Vim**: Use official plugin (via vim-plug: `Plug 'psf/black', { 'branch': 'stable' }`). Commands: `:Black` to format. Auto-save: Add autocmd to vimrc. Config vars like `g:black_linelength`.
- **Emacs**: Use reformatter.el or python-black package for on-save formatting.
- **Other**: Supports Sublime Text, JupyterLab, Spyder, etc., via plugins or extensions.

### Version Control

- **Pre-commit Hooks**: Add to `.pre-commit-config.yaml`:

  ```
  repos:
    - repo: https://github.com/psf/black-pre-commit-mirror
      rev: 25.1.0
      hooks:
        - id: black
          language_version: python3.11
  ```

  For Jupyter: Use `id: black-jupyter`.
- **GitHub Actions**: Use actions like `psf/black-action` in workflows for CI checks.
- **Git**: Run Black in pre-commit scripts or husky for enforcement.

## Advanced Topics

- **Preview and Unstable Styles**: Use `--preview` for future changes (e.g., better hug parens). `--unstable` for experimental features.
- **Blackd**: HTTP server for integrations (`blackd --bind-host 127.0.0.1 --bind-port 45484`).
- **Jupyter Support**: Formats notebooks, preserving magics.
- **Typing Stubs**: Special terse formatting for `.pyi` files.
- **Compatibility**: Targets Python 3.8+; use `--target-version` for older code.
- **Alternatives**: Compared to autopep8 (more flexible but less opinionated) or Ruff (faster, includes linting).

For troubleshooting, check the FAQ on the official docs or GitHub issues.

## References

- [Black 25.1.0 Documentation](https://black.readthedocs.io/en/stable/)
- [psf/black GitHub Repository](https://github.com/psf/black)
- [The Black Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
- [Usage and Configuration](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)
- [Editor Integrations](https://black.readthedocs.io/en/stable/integrations/editors.html)
- [Version Control Integration](https://black.readthedocs.io/en/stable/integrations/source_version_control.html)
- [Python Code Formatting Using Black - GeeksforGeeks](https://www.geeksforgeeks.org/python/python-code-formatting-using-black/)
- [How to Auto-Format Your Python Code with Black - freeCodeCamp](https://www.freecodecamp.org/news/auto-format-your-python-code-with-black/)
- [Black - PyPI](https://pypi.org/project/black/)
- [Introduction to Python Black Module - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-to-python-black-module/)
- [Python Auto Formatter: Autopep8 vs. Black - Built In](https://builtin.com/data-science/autopep8-vs-black)
