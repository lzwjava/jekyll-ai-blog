import os
import sys
import argparse
import pyperclip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ww.llm.openrouter_client import call_openrouter_api


def solve_complex(problem, attempted_solutions=None, depth=0):
    if attempted_solutions is None:
        attempted_solutions = []

    print(f"\nDepth: {depth}")
    print(f"Attempting to solve: {problem}")
    print(f"Previous attempts: {len(attempted_solutions)}")

    solution = call_openrouter_api(
        f"You are a problem solver. Solve this problem or say 'WRONG' if your solution might be incorrect.\n\nProblem: {problem}\nPrevious attempts: {attempted_solutions}\nProvide a solution."
    )

    print(f"Got solution: {solution}")

    if "WRONG" in solution:
        print("Solution marked as WRONG, trying again...")
        if len(attempted_solutions) > 5:
            print("Too many attempts, giving up")
            return "Failed to find solution after multiple attempts"

        return solve_complex(
            f"Previous solution was wrong. Try a different approach for: {problem}",
            attempted_solutions + [solution],
            depth + 1,
        )

    return solution


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a problem recursively")
    parser.add_argument("question", type=str, nargs="?", help="The question to solve")
    parser.add_argument(
        "--clipboard", "-c", action="store_true", help="Read question from clipboard"
    )
    args = parser.parse_args()

    if args.clipboard:
        question = pyperclip.paste()
    else:
        question = args.question if args.question else input("Enter your question: ")

    answer = solve_complex(question)
    print(f"\nQuestion: {question}")
    print(f"Answer: {answer}")

    # Copy answer to clipboard
    pyperclip.copy(answer)
