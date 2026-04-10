import os
import sys
import argparse
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.llm.openrouter_client import call_openrouter_api
from code_validation_utils import validate_code_quality


def generate_refactor_prompt(file_path):
    """Generate a refactor prompt for the given Python file with proper markdown formatting."""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        prompt = f"""# Refactor Prompt

## Instructions
Refactor the Python code below, focusing on:
- Improving readability
- Enhancing maintainability
- Following Python best practices
- Added if __name__ == "__main__": to ensure that the script can be both imported as a module and run as a standalone script.
- Do not use main() function, use other meaningful function names to let it import from other scripts.
- Used argparse to allow for flexible input of the params.
- Do not need docstring in each function.
- The code is divided into smaller, reusable functions, each with a single responsibility.
- Each function should be below 30 lines for better maintainability.
- Include demo run examples for each function as comments.
- Improved variable names and overall structure for better readability.
- Although not explicitly added, the structure now makes it easier to add error handling where necessary.
- Only output the refactored code without any additional comments or explanations.

## Target File
`{file_path}`

## Code to Refactor
```python
{content}
```

"""
        return prompt
    except FileNotFoundError:
        return f"Error: The file {file_path} was not found."
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"


def refactor_python_code(file_path, model="kimi-k2"):
    """
    Generate a refactor prompt and get AI suggestions for improving Python code.
    The resulting code is written directly back to the original file.
    """
    try:
        print(f"Debug: Reading file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            original_code = file.read()
        print(f"Debug: Read {len(original_code)} bytes from {file_path}")
        print("Debug: Original code preview:\n" + original_code[:1000])

        prompt = generate_refactor_prompt(file_path)
        print(f"Debug: Generated prompt length: {len(prompt)}")
        print("Debug: Prompt preview:\n" + prompt[:1000])
        print(f"Debug: Calling model={model} for refactor")

        response = call_openrouter_api(prompt=prompt, model=model)

        if response is None:
            print("Debug: Model returned None")
            return "Error: Model returned no response"

        print(f"Debug: Received response of length {len(response)}")
        print("Debug: Response preview:\n" + response[:1000])
        print("Debug: Response repr preview:\n" + repr(response)[:1000])
        # write response to a temp file for manual inspection
        try:
            tmp_path = file_path + ".ai_response.tmp"
            with open(tmp_path, "w", encoding="utf-8") as tf:
                tf.write(response)
            print(f"Debug: Wrote model response to {tmp_path}")
        except Exception as e:
            print(f"Debug: Failed to write temp response: {e}")

        # if the model wrapped code in markdown fences, strip them
        cleaned = response
        if cleaned.lstrip().startswith("```"):
            # remove leading ``` and optional language tag and trailing ```
            parts = cleaned.split("```")
            # pick the largest code block (heuristic)
            candidates = [p for p in parts if p.strip()]
            if candidates:
                # assume last candidate is code block content
                cleaned = candidates[-1]
        cleaned = cleaned.strip("\n")

        print("Debug: Cleaned response preview:\n" + cleaned[:1000])
        print("Debug: Cleaned response repr preview:\n" + repr(cleaned)[:1000])

        # write cleaned response to a temp file for manual inspection
        try:
            tmp_path = file_path + ".ai_response.cleaned.tmp"
            with open(tmp_path, "w", encoding="utf-8") as tf:
                tf.write(cleaned)
            print(f"Debug: Wrote cleaned model response to {tmp_path}")
        except Exception as e:
            print(f"Debug: Failed to write cleaned temp response: {e}")

        # show line-by-line preview of cleaned
        try:
            lines = cleaned.splitlines()
            preview_lines = lines[:200]
            print("Debug: First 200 lines of cleaned response:")
            for i, ln in enumerate(preview_lines, start=1):
                print(f"{i:03d}: {ln}")
        except Exception as e:
            print(f"Debug: Failed to split cleaned response into lines: {e}")

        if isinstance(cleaned, str) and cleaned.startswith("Error"):
            print(f"Debug: Model signaled error after cleaning: {cleaned}")
            return cleaned

        # attempt to compile cleaned response to catch syntax errors
        try:
            import py_compile
            import tempfile

            tmpc = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
            tmpc.write(cleaned.encode("utf-8"))
            tmpc.flush()
            tmpc.close()
            try:
                py_compile.compile(tmpc.name, doraise=True)
                compile_ok = True
                print(f"Debug: Cleaned response compiled successfully: {tmpc.name}")
            except py_compile.PyCompileError as ce:
                compile_ok = False
                print(f"Debug: Compilation failed: {ce}")
        except Exception as e:
            print(f"Debug: Failed to attempt compile: {e}")
            compile_ok = False

        is_valid, validation_msg = validate_code_quality(original_code, cleaned)
        print(f"Debug: Validation result: is_valid={is_valid}")
        if not is_valid:
            print(f"Debug: Validation message:\n{validation_msg}")
            return f"Validation failed: {validation_msg}"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response)
        print(f"Debug: Wrote refactored code to {file_path}")
        return f"Successfully refactored {file_path}"

    except Exception as e:
        print("Debug: Exception during refactoring:")
        traceback.print_exc()
        return f"Error during refactoring: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("🐍 Python Code Refactor Agent")
        print("=" * 50)
        print("\n📝 Demo Usage Examples:")
        print("  python scripts/agent/refactor_agent.py my_script.py")
        print(
            "  python scripts/agent/refactor_agent.py my_script.py --model claude-sonnet"
        )
        print(
            "  python scripts/agent/refactor_agent.py utils/helper.py --model deepseek-v3"
        )
        print("\n🤖 Available Models:")
        print("  claude-opus, claude-sonnet, gemini-flash, gemini-pro, kimi-k2,")
        print(
            "  deepseek-v3, deepseek-v3.1, mistral-medium, qwen-coder, gpt-oss, gpt-5"
        )
        print("\n" + "=" * 50)
        print()

    parser = argparse.ArgumentParser(
        description="Get AI suggestions for refactoring Python code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Models:
  claude-opus, claude-sonnet, gemini-flash, gemini-pro, kimi-k2,
  deepseek-v3, deepseek-v3.1, mistral-medium, qwen-coder, gpt-oss, gpt-5

Examples:
  %(prog)s my_script.py
  %(prog)s my_script.py --model claude-sonnet
  %(prog)s utils/helper.py --model deepseek-v3
        """,
    )
    parser.add_argument("file_path", help="Path to the Python file to refactor")
    parser.add_argument(
        "--model",
        default="kimi-k2",
        help="Model to use for refactoring (default: kimi-k2)",
    )
    args = parser.parse_args()

    result = refactor_python_code(args.file_path, args.model)
    print(result)
