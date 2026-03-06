import subprocess
import sys
import argparse


def run_vscode_command(prompt: str = "") -> bool:
    """
    Execute a VS Code command using the 'code' CLI.

    Args:
        command (str): The VS Code command to execute (e.g., 'workbench.action.chat.open').
        prompt (str): Optional prompt or argument for the command.

    Returns:
        bool: True if the command was executed successfully, False otherwise.
    """
    try:
        # Construct the VS Code CLI command
        # Assumes 'code' is in the system PATH
        cmd = ["code", "chat", prompt]

        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Print the command output
        print("Command output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute command: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(
            "VS Code CLI ('code') not found. Ensure VS Code is installed and added to PATH.",
            file=sys.stderr,
        )
        return False


def main():
    parser = argparse.ArgumentParser(description="Run a VS Code command with a prompt.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="",
        help="The prompt or argument for the VS Code command.",
    )
    args = parser.parse_args()

    # Run the command with the provided prompt
    success = run_vscode_command(args.prompt)
    if success:
        print(f"Successfully triggered with prompt: {args.prompt}")
    else:
        print("Failed to trigger")


if __name__ == "__main__":
    main()
