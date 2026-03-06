import subprocess
import sys


def install_package(package_name):
    """Install a package globally using npm."""
    try:
        subprocess.run(["sudo", "npm", "install", "-g", package_name], check=True)
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    packages = ["@anthropic-ai/claude-code", "@musistudio/claude-code-router"]

    for package in packages:
        install_package(package)
