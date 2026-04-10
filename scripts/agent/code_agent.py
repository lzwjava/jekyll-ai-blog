import os
import sys
import tempfile
import subprocess
import argparse
import pyperclip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ww.llm.openrouter_client import call_openrouter_api


def run_python_code(code):
    # Remove markdown code block if present
    if code.startswith("```python"):
        code = code.split("\n", 1)[1]
    if code.endswith("```"):
        code = code.rsplit("\n", 1)[0]

    # Add test case
    code = code + "\n\n# Test the function\nprint(sum_natural_numbers(5))"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as f:
        f.write(code)
        f.flush()
        try:
            result = subprocess.run(["python3", f.name], capture_output=True, text=True)
            return result.stdout, result.stderr
        except Exception as e:
            return "", str(e)


def solve_and_run(problem, attempted_solutions=None, depth=0):
    if attempted_solutions is None:
        attempted_solutions = []

    print(f"\nDepth: {depth}")
    print(f"Attempting to solve: {problem}")
    print(f"Previous attempts: {len(attempted_solutions)}")

    solution = call_openrouter_api(
        f"You are a Python code generator. Write executable Python code to solve this problem. Only provide the code, no explanations.\n\nProblem: {problem}\nPrevious attempts: {attempted_solutions}"
    )

    print(f"\nGot solution code:\n{solution}\n")
    print("Running code...")

    stdout, stderr = run_python_code(solution)
    print(f"\nExecution output:\n{stdout}")

    if stderr:
        print(f"\nExecution errors:\n{stderr}")
        if len(attempted_solutions) > 5:
            return "Failed to generate working code after multiple attempts"
        return solve_and_run(
            f"Previous solution had errors: {stderr}\nTry again: {problem}",
            attempted_solutions + [solution],
            depth + 1,
        )

    print("\nVerifying solution...")
    verification = call_openrouter_api(
        f"You are a code reviewer. Verify if this code correctly solves the problem. Respond with 'CORRECT' or explain the issues.\n\nProblem: {problem}\nCode:\n{solution}\nOutput:\n{stdout}"
    )

    print(f"Verification result: {verification}")

    if "CORRECT" in verification:
        print("Solution verified as CORRECT!")
        return solution

    print("Solution not verified, trying again...")
    return solve_and_run(problem, attempted_solutions + [solution], depth + 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and run Python code to solve a problem"
    )
    parser.add_argument(
        "question", type=str, nargs="?", help="The coding problem to solve"
    )
    parser.add_argument(
        "--clipboard", "-c", action="store_true", help="Read problem from clipboard"
    )
    args = parser.parse_args()

    if args.clipboard:
        question = pyperclip.paste()
    else:
        question = (
            args.question if args.question else input("Enter your coding problem: ")
        )

    answer = solve_and_run(question)
    print(f"\nQuestion: {question}")
    print(f"\nFinal solution:\n{answer}")

    # Copy solution to clipboard
    pyperclip.copy(answer)
