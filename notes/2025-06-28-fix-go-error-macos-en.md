---
audio: false
generated: true
lang: en
layout: post
title: Fixing Go Command Not Found on macOS
translated: false
type: note
---

The error message `/bin/sh: go: command not found` indicates that the Go programming language is not installed on your macOS system, or it's not properly configured in your PATH. The `make` command is trying to run a Go build process, which requires the Go compiler (`go`). Below are the steps to install Go on macOS and resolve this issue.

### Steps to Install Go on macOS

There are two primary ways to install Go on macOS: using the official Go installer or using Homebrew. I'll cover both methods, but Homebrew is often simpler for macOS users. Choose one method based on your preference.

#### Prerequisites

- Ensure your macOS version is 10.10 or later for compatibility with recent Go versions.[](https://tecadmin.net/install-go-on-macos/)
- You need administrator access to install Go and modify system files.
- A terminal application (found in Applications > Utilities > Terminal).

#### Method 1: Install Go Using Homebrew (Recommended)

Homebrew is a popular package manager for macOS that simplifies software installation.

1. **Install Homebrew (if not already installed)**:
   - Open Terminal and run:

     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

   - Follow the on-screen instructions to complete the installation.[](https://www.digitalocean.com/community/tutorials/how-to-install-go-and-set-up-a-local-programming-environment-on-macos)

2. **Install Go**:
   - Run the following command to install the latest version of Go:

     ```bash
     brew install go
     ```

   - This installs Go to `/usr/local/Cellar/go` (or a similar path) and adds the Go binary to `/usr/local/bin`.[](https://www.feliciano.tech/blog/how-to-install-go-on-linux-macos/)[](https://formulae.brew.sh/formula/go)

3. **Verify Installation**:
   - Check the installed Go version by running:

     ```bash
     go version
     ```

   - You should see output like `go version go1.23.x darwin/amd64`, confirming Go is installed.[](https://tecadmin.net/install-go-on-macos/)

4. **Set Up Environment Variables** (if needed):
   - Homebrew typically adds Go to your PATH automatically, but if `go` commands don't work, add the Go binary path to your shell profile:
     - Open or create the appropriate shell configuration file (e.g., `~/.zshrc` for Zsh, which is default on macOS since Catalina, or `~/.bash_profile` for Bash):

       ```bash
       nano ~/.zshrc
       ```

     - Add the following lines:

       ```bash
       export PATH=$PATH:/usr/local/go/bin
       ```

     - Save the file (Ctrl+X, then Y, then Enter in nano) and apply the changes:

       ```bash
       source ~/.zshrc
       ```

     - If you want to use a custom workspace, set `GOPATH` (optional, as Go modules often eliminate the need for this):

       ```bash
       export GOPATH=$HOME/go
       export PATH=$PATH:$GOPATH/bin
       ```

     - Source the file again:

       ```bash
       source ~/.zshrc
       ```

5. **Test Go Installation**:
   - Run `go version` again to ensure the command is recognized.
   - Optionally, create a simple Go program to confirm everything works:

     ```bash
     mkdir -p ~/go/src/hello
     nano ~/go/src/hello/main.go
     ```

     - Add the following code:

       ```go
       package main
       import "fmt"
       func main() {
           fmt.Println("Hello, World!")
       }
       ```

     - Save and exit (Ctrl+X, Y, Enter), then compile and run:

       ```bash
       cd ~/go/src/hello
       go run main.go
       ```

     - You should see `Hello, World!` as output.[](https://www.digitalocean.com/community/tutorials/how-to-install-go-and-set-up-a-local-programming-environment-on-macos)

#### Method 2: Install Go Using the Official Installer

If you prefer not to use Homebrew, you can install Go using the official macOS package.

1. **Download the Go Installer**:
   - Visit the official Go download page: <https://go.dev/dl/>
   - Download the macOS package (`.pkg`) for your system architecture (e.g., `go1.23.x.darwin-amd64.pkg` for Intel Macs or `go1.23.x.darwin-arm64.pkg` for Apple Silicon).[](https://medium.com/%40priyamjpatel/installing-go-on-a-mac-machine-bca6746fff0b)[](https://golangdocs.com/install-go-mac-os)

2. **Run the Installer**:
   - Double-click the downloaded `.pkg` file in Finder.
   - Follow the on-screen instructions to install Go. It will be installed to `/usr/local/go` by default.
   - You may need to enter your administrator password.[](https://www.scaler.com/topics/golang/install-golang/)[](https://golangdocs.com/install-go-mac-os)

3. **Set Up Environment Variables**:
   - Open Terminal and edit your shell configuration file (e.g., `~/.zshrc` or `~/.bash_profile`):

     ```bash
     nano ~/.zshrc
     ```

   - Add the following lines:

     ```bash
     export GOROOT=/usr/local/go
     export GOPATH=$HOME/go
     export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
     ```

   - Save and apply the changes:

     ```bash
     source ~/.zshrc
     ```

   - Note: `GOROOT` is optional unless you're developing Go itself or need a non-standard installation path. Modern Go versions often don't require `GOROOT` to be set.[](https://stackoverflow.com/questions/12843063/install-go-with-brew-and-running-the-gotour)[](https://tecadmin.net/install-go-on-macos/)

4. **Verify Installation**:
   - Run:

     ```bash
     go version
     ```

   - You should see the installed Go version (e.g., `go version go1.23.x darwin/amd64`).[](https://golangdocs.com/install-go-mac-os)

5. **Test Go Installation**:
   - Follow the same steps as in Method 1, Step 5 to create and run a "Hello, World!" program.

#### Troubleshooting the Original Issue

After installing Go, navigate back to your `clash-core` directory and retry the `make` command:

```bash
cd /path/to/clash-core
make
```

If you encounter issues:

- **Proxy Settings**: Your terminal output shows `HTTP_PROXY` and `HTTPS_PROXY` set to `http://127.0.0.1:7890`. Ensure your proxy is active and not interfering with Go's network access (e.g., downloading dependencies). You can temporarily disable the proxy to test:

  ```bash
  unset HTTP_PROXY HTTPS_PROXY
  make
  ```

- **Permissions**: If you get permission errors, ensure you have write access to the project directory and Go workspace (`$GOPATH` or `$HOME/go`).
- **Go Modules**: The `clash-core` project likely uses Go modules. Ensure you're in the correct directory containing `go.mod`, and run `go mod tidy` to fetch dependencies before `make`:

  ```bash
  go mod tidy
  make
  ```

- **Architecture Mismatch**: The `make` command is building for `linux-amd64` (`GOOS=linux GOARCH=amd64`). If you intend to run the binary on macOS, you may need to modify the Makefile or build command to target `darwin-amd64` (for Intel Macs) or `darwin-arm64` (for Apple Silicon). Check the Makefile for the `linux-amd64` target and adjust it, or run:

  ```bash
  GOARCH=amd64 GOOS=darwin CGO_ENABLED=0 go build -trimpath -ldflags '-X "github.com/Dreamacro/clash/constant.Version=1.18" -X "github.com/Dreamacro/clash/constant.BuildTime=Sat Jun 28 12:24:27 UTC 2025" -w -s -buildid=' -o bin/clash-darwin-amd64
  ```

  Replace `amd64` with `arm64` if you're on Apple Silicon.

#### Additional Notes

- **Uninstalling Previous Go Versions**: If Go was previously installed, remove it to avoid conflicts:

  ```bash
  sudo rm -rf /usr/local/go
  sudo rm -f /etc/paths.d/go
  ```

  Then reinstall using one of the methods above.[](https://hostman.com/tutorials/how-to-install-go-on-macos/)[](https://go.dev/doc/install)
- **Go Workspace**: If you set `GOPATH`, create the directory:

  ```bash
  mkdir -p $HOME/go/{bin,src,pkg}
  ```

  However, with Go modules (used by most modern projects like `clash-core`), `GOPATH` is less critical.[](https://www.geeksforgeeks.org/how-to-install-golang-on-macos/)
- **Xcode Command Line Tools**: Some Go projects require C dependencies (e.g., `CGO_ENABLED=1`). Install Xcode Command Line Tools if needed:

  ```bash
  xcode-select --install
  ```

  [](https://www.digitalocean.com/community/tutorials/how-to-install-go-and-set-up-a-local-programming-environment-on-macos)
- **Multiple Go Versions**: If you need multiple Go versions, consider using a version manager like `gvm` (install via Homebrew or script).[](https://jimkang.medium.com/install-go-on-mac-with-homebrew-5fa421fc55f5)

#### Verification

Once Go is installed and the `make` command succeeds, the `clash-core` binary should appear in the `bin/` directory (e.g., `bin/clash-linux-amd64` or `bin/clash-darwin-amd64`). Verify it works by running:

```bash
./bin/clash-darwin-amd64 --version
```

If you need further assistance or run into specific errors, let me know the exact error message or context, and I can provide more targeted help!
