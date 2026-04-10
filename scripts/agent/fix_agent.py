import sys
import argparse
from pathlib import Path
import os
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.llm.openrouter_client import call_openrouter_api
from scripts.llm.openrouter_client import MODEL_MAPPING


def run_script(script_path):
    """Run a Python or Rust script and capture its output."""
    script_path = Path(script_path)
    if script_path.suffix == ".py":
        try:
            result = subprocess.run(
                ["python3", str(script_path)], capture_output=True, text=True
            )
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)
    elif script_path.suffix == ".rs":
        # For Rust, we need to run cargo build in the directory containing the Rust project
        project_dir = script_path.parent
        try:
            result = subprocess.run(
                ["cargo", "build"], cwd=project_dir, capture_output=True, text=True
            )
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)
    else:
        return f"Unsupported file extension for {script_path}"


def fix_script(script_path, error_message, model):
    """Use OpenRouter API to suggest fixes for the script errors and apply them."""
    script_path = Path(script_path)
    lang = (
        "Python"
        if script_path.suffix == ".py"
        else "Rust"
        if script_path.suffix == ".rs"
        else "Unknown"
    )
    prompt = f"Error in {lang} script {script_path}:\n{error_message}\nPlease provide only the corrected code for the entire script without any explanations, markdown syntax, or additional text."
    response = call_openrouter_api(prompt, model=model)
    # Remove any markdown code block syntax from the response
    response = (
        response.replace("```python", "").replace("```rust", "").replace("```", "")
    )
    # Write the fixed code back to the original script file
    try:
        with open(script_path, "w") as f:
            f.write(response.strip())
        return f"Applied fix to {script_path}"
    except Exception as e:
        return f"Failed to apply fix: {str(e)}"


# Model mapping for user-friendly names


def main():
    parser = argparse.ArgumentParser(description="Run and fix Python or Rust scripts.")
    parser.add_argument(
        "script",
        type=str,
        help="Path to the script to run and fix (Python .py or Rust .rs).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek-v3.2",
        choices=list(MODEL_MAPPING.keys()),
        help="Model to use for OpenRouter API (e.g., claude-opus, gemini-pro).",
    )
    args = parser.parse_args()

    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Script {script_path} does not exist.")
        sys.exit(1)

    # Get the actual model name from the mapping
    selected_model = MODEL_MAPPING[args.model]

    # Run the script initially to capture output
    print("Running script for the first time...")
    output = run_script(script_path)
    print("Initial Script Output:")
    print(output)

    if "error" in output.lower() or "traceback" in output.lower():
        print("Error detected, attempting to fix...")
        fix_result = fix_script(script_path, output, selected_model)
        print("Fix Result:")
        print(fix_result)
        # Re-run the script after applying the fix
        print("Re-running script after fix...")
        output = run_script(script_path)
        print("Updated Script Output:")
        print(output)

    if "error" in output.lower() or "traceback" in output.lower():
        print("Error still present after fix attempt.")
        print("Final Script Output:")
        print(output)


if __name__ == "__main__":
    main()
