import subprocess
import argparse

parser = argparse.ArgumentParser(
    description="Install Python packages with --break-system-packages"
)
parser.add_argument("package", help="Package name to install")
args = parser.parse_args()

subprocess.run(
    [
        "/opt/homebrew/bin/python3",
        "-m",
        "pip",
        "install",
        args.package,
        "--break-system-packages",
    ]
)
