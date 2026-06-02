---
audio: false
generated: true
lang: en
layout: post
title: Install Go via APT on Debian
translated: false
type: note
---

To install Go using `apt` on a Debian-based Linux system (e.g., Ubuntu), follow these steps. Note that `apt` may install an older version of Go (e.g., 1.18 on Ubuntu 22.04), so you should verify if it meets your project's requirements (check the `go.mod` file in `~/Projects/clash-core` for the required Go version).

### Steps to Install Go Using APT

1. **Update the Package Index**
   - Ensure your package lists are up to date:

     ```bash
     sudo apt update
     ```

2. **Install Go**
   - Install the Go package:

     ```bash
     sudo apt install golang-go
     ```

   - This installs the Go compiler, tools, and standard library.

3. **Verify the Installation**
   - Check the installed Go version:

     ```bash
     go version
     ```

   - You should see output like:

     ```
     go version go1.18.1 linux/amd64
     ```

     (The version depends on your distribution's package repository.)

4. **Set Up GOPATH (Optional)**
   - Modern Go versions (1.13+) use modules, so `GOPATH` is optional, but setting it can be useful for some projects.
   - Edit your shell profile (e.g., `~/.bashrc` or `~/.zshrc`):

     ```bash
     nano ~/.bashrc
     ```

   - Add the following:

     ```bash
     export GOPATH=$HOME/go
     export PATH=$PATH:$GOPATH/bin
     ```

   - Save and reload the shell configuration:

     ```bash
     source ~/.bashrc
     ```

5. **Retry the Build**
   - Navigate to your project directory:

     ```bash
     cd ~/Projects/clash-core
     ```

   - Run the `make` command again:

     ```bash
     make
     ```

### Notes

- **Version Check**: If your project requires a newer Go version (e.g., 1.20 or later), the `apt` version might be outdated. Check the required version in `go.mod` or the project’s documentation. If needed, install a newer version manually by downloading the tarball from [https://go.dev/dl/](https://go.dev/dl/) (as described in the previous response).
- **Alternative Repositories**: For a newer version via `apt`, you can add a third-party PPA (e.g., `ppa:longsleep/golang-backports` on Ubuntu). Run:

  ```bash
  sudo add-apt-repository ppa:longsleep/golang-backports
  sudo apt update
  sudo apt install golang-go
  ```

- **Troubleshooting**:
  - If `go` is not found, ensure `/usr/bin/go` exists (`ls /usr/bin/go`). If not, reinstall with `sudo apt install --reinstall golang-go`.
  - If you get dependency errors, run `sudo apt install -f` to fix them.
  - For permission issues, ensure you have `sudo` privileges.

### Sources

- Ubuntu Go installation guide: [https://ubuntu.com/server/docs/programming-go](https://ubuntu.com/server/docs/programming-go)
- General apt usage: [https://help.ubuntu.com/community/AptGet/Howto](https://help.ubuntu.com/community/AptGet/Howto)

If the installed version is too old or you encounter issues, let me know your Linux distribution (e.g., Ubuntu 22.04) and the required Go version, and I’ll guide you further!
