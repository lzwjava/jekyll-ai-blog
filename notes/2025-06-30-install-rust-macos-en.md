---
audio: false
generated: true
lang: en
layout: post
title: Install Rust on macOS with rustup
translated: false
type: note
---

## Installing Rust using rustup

1. **Open Terminal**
    You can find Terminal in **Applications > Utilities** or search for it using Spotlight.

2. **Install rustup and Rust**
    Run the following command to download and run the rustup installation script:

    ```sh
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

    The script will prompt you to proceed. Press `1` for the default installation.

3. **Configure Your Shell**
    After installation, you may need to add Rust to your system `PATH`. The installer will provide a command similar to:

    ```sh
    source $HOME/.cargo/env
    ```

    Add this line to your shell configuration file (e.g., `.zshrc`, `.bashrc`, or `.bash_profile`) to make Rust available in future sessions.

4. **Verify Installation**
    Check that Rust is installed correctly:

    ```sh
    rustc --version
    ```

    You should see the Rust compiler version if the installation was successful.

---

## Using Homebrew to Install Rust

Alternatively, you can use [Homebrew](https://brew.sh/) to install Rust, though `rustup` is generally recommended for easier updates and version management.

1. **Install Homebrew** (if not already installed):

    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. **Install Rust with Homebrew**:

    ```sh
    brew install rust
    ```

3. **Verify Installation**:

    ```sh
    rustc --version
    ```

---

## Compiling Rust Code

1. **Write a Rust Program**
    Create a file named `main.rs` with the following content:

    ```rust
    fn main() {
         println!("Hello, World!");
    }
    ```

2. **Compile the Program**
    In the terminal, navigate to the directory containing your file and run:

    ```sh
    rustc main.rs
    ```

3. **Run the Compiled Program**:

    ```sh
    ./main
    ```

---

This setup should get you started with Rust development on macOS. If you have any issues, feel free to ask!
