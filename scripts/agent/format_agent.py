import sys
import argparse
from pathlib import Path
import os
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.llm.openrouter_client import call_openrouter_api
from scripts.llm.openrouter_client import MODEL_MAPPING


def format_script(script_path):
    """Format a Python or Rust script using standard formatting tools."""
    script_path = Path(script_path)
    if script_path.suffix == ".py":
        try:
            result = subprocess.run(
                ["black", str(script_path)], capture_output=True, text=True
            )
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)
    elif script_path.suffix == ".rs":
        try:
            result = subprocess.run(
                ["rustfmt", str(script_path), "--edition", "2021"],
                capture_output=True,
                text=True,
            )
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)
    else:
        return f"Unsupported file extension for {script_path}"


def ai_format_script(script_path, model):
    """Use OpenRouter API to suggest formatting improvements for the script."""
    script_path = Path(script_path)
    lang = (
        "Python"
        if script_path.suffix == ".py"
        else "Rust"
        if script_path.suffix == ".rs"
        else "Unknown"
    )
    with open(script_path, "r") as f:
        code_content = f.read()
    prompt = f"Please format the following {lang} code for better readability and consistency. Provide only the formatted code without explanations or markdown syntax:\n\n{code_content}"
    response = call_openrouter_api(prompt, model=model)
    # Remove any markdown code block syntax from the response
    response = (
        response.replace("```python", "").replace("```rust", "").replace("```", "")
    )
    # Write the AI-formatted code back to the original script file
    try:
        with open(script_path, "w") as f:
            f.write(response.strip())
        return f"Applied AI formatting to {script_path}"
    except Exception as e:
        return f"Failed to apply AI formatting: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="Format Python or Rust scripts using standard tools and AI."
    )
    parser.add_argument(
        "script",
        type=str,
        help="Path to the script to format (Python .py or Rust .rs).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek-v3.2",
        choices=list(MODEL_MAPPING.keys()),
        help="Model to use for OpenRouter API (e.g., claude-opus, gemini-pro).",
    )
    parser.add_argument(
        "--ai-only",
        action="store_true",
        help="Use only AI formatting instead of standard tools like black or rustfmt.",
    )
    args = parser.parse_args()

    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Script {script_path} does not exist.")
        sys.exit(1)

    # Get the actual model name from the mapping
    selected_model = MODEL_MAPPING[args.model]

    if args.ai_only:
        print("Applying AI-based formatting...")
        ai_result = ai_format_script(script_path, selected_model)
        print("AI Formatting Result:")
        print(ai_result)
    else:
        print("Applying standard formatting tools...")
        format_result = format_script(script_path)
        print("Standard Formatting Output:")
        print(format_result)

        if "error" in format_result.lower():
            print("Standard formatting failed, falling back to AI formatting...")
            ai_result = ai_format_script(script_path, selected_model)
            print("AI Formatting Result:")
            print(ai_result)


if __name__ == "__main__":
    main()
