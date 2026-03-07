#!/usr/bin/env python3
"""
Interactive Problem Solving Guide with AI Assistance
===================================================

This tool provides a systematic approach to solving any technical problem
using AI assistants and proven debugging methodologies.

Usage:
    python solve.py
    python solve.py --mode quick  # Skip detailed questioning
    python solve.py --ai claude   # Specify preferred AI
"""

import sys
import json
from pathlib import Path

# Add the llm module to path for importing openrouter_client
sys.path.append(str(Path(__file__).parent.parent / "llm"))

try:
    from openrouter_client import call_openrouter_api

    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Warning: openrouter_client not available. AI assistance disabled.")


class ProblemSolver:
    def __init__(self):
        self.issue_description = ""
        self.issue_type = ""
        self.previous_experience = ""
        self.tried_tools = []
        self.environment = {}
        self.use_ai = True
        self.preferred_ai = "claude-sonnet"

    def ask_diagnostic_questions(self):
        """Ask systematic questions to understand the problem"""
        print("PROBLEM DIAGNOSIS PHASE")
        print("=" * 50)

        # Question 1: What's the exact issue?
        print("\n1. What's the exact issue you're facing?")
        print("   a) Bug in existing code")
        print("   b) New feature implementation")
        print("   c) Performance problem")
        print("   d) Configuration/deployment issue")
        print("   e) Error message you don't understand")
        print("   f) Code review/refactoring")
        print("   g) Learning/teaching something new")

        issue_map = {
            "a": "bug",
            "b": "feature",
            "c": "performance",
            "d": "config",
            "e": "error",
            "f": "refactor",
            "g": "learning",
        }

        while True:
            choice = input("\nSelect option (a-g): ").lower().strip()
            if choice in issue_map:
                self.issue_type = issue_map[choice]
                break
            print("Please select a valid option (a-g)")

        # Detailed description
        print(f"\nDescribe your {self.issue_type} in detail:")
        self.issue_description = input("> ").strip()

        # Question 2: Previous experience
        print("\n2. Have you encountered this type of problem before?")
        self.previous_experience = input(
            "Describe your experience (or 'no' if first time): "
        ).strip()

        # Question 3: Tools tried
        print("\n3. What tools/resources have you already tried? (comma-separated)")
        print("   - Google/Stack Overflow")
        print("   - Official documentation")
        print("   - GitHub issues/search")
        print("   - Debugging tools")
        print("   - AI assistants")
        print("   - Colleagues/forums")

        tools_input = input("Tools tried: ").strip()
        self.tried_tools = [tool.strip() for tool in tools_input.split(",")]

        # Question 4: Environment
        print("\n4. What's your environment? (press Enter to skip)")
        print("   Programming language/framework:")
        lang = input("> ").strip()
        print("   Error messages (if any):")
        error = input("> ").strip()
        print("   Development tools (IDE, etc.):")
        tools = input("> ").strip()

        self.environment = {"language": lang, "error": error, "tools": tools}

        # Question 5: AI preference
        print("\n5. Do you want AI assistance? (y/n)")
        while True:
            ai_choice = input("Use AI: ").lower().strip()
            if ai_choice in ["y", "yes"]:
                self.use_ai = True
                break
            elif ai_choice in ["n", "no"]:
                self.use_ai = False
                break
            print("Please answer 'y' or 'n'")

    def create_solution_plan(self):
        """Create a structured solution plan"""
        print("\nSOLUTION PLANNING PHASE")
        print("=" * 50)

        # Build the problem analysis
        problem_context = f"""
PROBLEM ANALYSIS:
- Issue Type: {self.issue_type}
- Description: {self.issue_description}
- Previous Experience: {self.previous_experience}
- Tools Already Tried: {", ".join(self.tried_tools)}
- Environment: {json.dumps(self.environment, indent=2)}
"""

        print(problem_context)

        # Generate action steps based on issue type
        base_steps = self.get_base_solving_steps()
        specific_steps = self.get_specific_steps()

        print("RECOMMENDED ACTION PLAN:")
        print("-" * 30)

        all_steps = base_steps + specific_steps
        for i, step in enumerate(all_steps, 1):
            print(f"{i:2d}. {step}")

        return all_steps

    def get_base_solving_steps(self):
        """Get fundamental debugging steps"""
        return [
            "Clean slate: Restart IDE/terminal, clear caches",
            "Read error messages carefully - every detail matters",
            "Isolate the problem - create minimal reproducible example",
            "Search systematically: GitHub, Stack Overflow, docs",
            "Document your findings and attempts",
            "Ask for help: colleagues, forums, AI assistants",
            "Test solution thoroughly before implementing",
        ]

    def get_specific_steps(self):
        """Get steps specific to the problem type"""
        step_map = {
            "bug": [
                "Reproduce the bug consistently",
                "Use debugger/print statements to trace execution",
                "Check recent changes (git diff)",
                "Write failing test case",
                "Fix one thing at a time",
            ],
            "feature": [
                "Design the solution architecture",
                "Research best practices and patterns",
                "Start with smallest working version",
                "Add tests for new functionality",
                "Update documentation",
            ],
            "performance": [
                "Profile to identify bottlenecks",
                "Measure before and after optimizations",
                "Check algorithmic complexity",
                "Load test the solution",
                "Monitor resource usage",
            ],
            "config": [
                "Check environment variables and settings",
                "Verify dependencies and versions",
                "Review configuration documentation",
                "Test configuration in isolation",
                "Document working configuration",
            ],
            "error": [
                "Copy exact error message and search it",
                "Check stack trace for line numbers",
                "Search for similar error scenarios",
                "Create minimal failing example",
                "Break complex error into smaller pieces",
            ],
            "refactor": [
                "Identify what needs improvement",
                "Ensure good test coverage first",
                "Make small, safe changes",
                "Balance clean code vs working code",
                "Document reasoning for changes",
            ],
            "learning": [
                "Start with official documentation",
                "Find practical examples to follow",
                "Build simple practice projects",
                "Join communities and ask questions",
                "Teach others to reinforce learning",
            ],
        }

        return step_map.get(self.issue_type, ["Define clear learning objectives"])

    def call_ai_assistant(self, steps):
        """Use AI to get specific guidance"""
        if not AI_AVAILABLE or not self.use_ai:
            return None

        print("\nAI ASSISTANCE PHASE")
        print("=" * 50)

        # Build comprehensive prompt for AI
        prompt = f"""
I need help solving a technical problem. Here's my situation:

**PROBLEM CONTEXT:**
- Issue Type: {self.issue_type}
- Description: {self.issue_description}
- Environment: {json.dumps(self.environment, indent=2)}
- Previous Experience: {self.previous_experience}
- Already Tried: {", ".join(self.tried_tools)}

**MY SOLUTION PLAN:**
{chr(10).join([f"{i}. {step}" for i, step in enumerate(steps, 1)])}

**REQUEST:**
Please provide:
1. 3-5 specific actionable steps for my situation
2. Key things I should watch out for
3. Recommended tools/resources
4. Success criteria to know when I've solved it

Keep advice practical and specific to {self.issue_type} problems.
"""

        try:
            print("Asking AI for guidance...")
            ai_response = call_openrouter_api(
                prompt, model=self.preferred_ai, debug=False
            )
            print("\n" + "=" * 60)
            print("AI GUIDANCE RECEIVED:")
            print("=" * 60)
            print(ai_response)
            print("=" * 60)
            return ai_response
        except Exception as e:
            print(f"AI request failed: {e}")
            return None

    def provide_resources(self):
        """Provide specific resources based on issue type"""
        print("\nRECOMMENDED RESOURCES:")
        print("=" * 50)

        resources = {
            "bug": [
                "Debugging guides: https://stackoverflow.com/questions/how-to-debug",
                "Minimal reproducible example: https://stackoverflow.com/help/minimal-reproducible-example",
                "Git bisect for finding bug-introducing commits",
            ],
            "feature": [
                "Design patterns: https://refactoring.guru/design-patterns",
                "Architecture guides: https://12factor.net/",
                "Testing strategies: https://testing-library.com/",
            ],
            "performance": [
                "Profiling tools: cProfile, Chrome DevTools, Py-Spy",
                "Performance monitoring: New Relic, DataDog",
                "Big O notation: https://www.interviewcake.com/article/python/big-o-notation-time-and-space-complexity",
            ],
            "config": [
                "Configuration management: 12-factor app methodology",
                "Container debugging: docker logs, kubectl logs",
                "Cloud provider debugging guides",
            ],
            "error": [
                "Error message search: Google exact error text",
                "Stack Overflow: https://stackoverflow.com/questions",
                "Error code databases and documentation",
            ],
            "refactor": [
                "Refactoring techniques: https://refactoring.guru/",
                "Test-driven development: https://martinfowler.com/articles/is-tdd-dead/",
                "Code smell detection: https://refactoring.guru/refactoring/smells",
            ],
            "learning": [
                "Documentation: Official docs for your tech stack",
                "Interactive learning: Codecademy, FreeCodeCamp",
                "Communities: Reddit r/learnprogramming, Stack Overflow",
            ],
        }

        specific_resources = resources.get(self.issue_type, resources["learning"])
        for resource in specific_resources:
            print(f"  {resource}")

        print("\nGeneral Problem Solving:")
        print("  Search strategies: exact phrases, error codes, version numbers")
        print("  Documentation: API references, changelogs, migration guides")
        print("  Community: GitHub issues, Discord, Telegram groups")
        print("  Experimentation: try things in isolation, small changes")

    def create_success_checklist(self):
        """Create a success checklist"""
        print("\nSUCCESS CHECKLIST:")
        print("=" * 50)

        checklist = [
            "Problem is clearly defined and understood",
            "Root cause identified (not just symptoms)",
            "Solution is tested and working",
            "No new problems introduced",
            "Code/documentation updated",
            "Solution is maintainable and follows best practices",
            "Lessons learned documented for future reference",
        ]

        for item in checklist:
            print(f"  [ ] {item}")

        print("\nBONUS: Share your solution to help others!")

    def run(self, mode="interactive", ai_model="claude-sonnet"):
        """Main execution method"""
        print("INTERACTIVE PROBLEM SOLVING GUIDE")
        print("=" * 60)
        print("Let's solve your problem systematically with AI assistance!")
        print("=" * 60)

        if mode != "quick":
            self.ask_diagnostic_questions()
        else:
            # Quick mode - basic questions
            print("Quick mode: Basic problem identification")
            self.issue_type = input("Issue type (bug/feature/error/etc.): ").strip()
            self.issue_description = input("Brief description: ").strip()
            self.use_ai = input("Use AI? (y/n): ").strip().lower() in ["y", "yes"]

        self.preferred_ai = ai_model

        # Create and execute solution plan
        steps = self.create_solution_plan()

        # Get AI guidance
        ai_response = self.call_ai_assistant(steps)

        # Provide resources
        self.provide_resources()

        # Success checklist
        self.create_success_checklist()

        print("\nPROBLEM-SOLVING SESSION COMPLETE!")
        print("Remember: Every expert was once a beginner. Keep learning!")

        # Save session summary
        self.save_session_summary(ai_response)

    def save_session_summary(self, ai_response):
        """Save a summary of this problem-solving session"""
        summary = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "issue_type": self.issue_type,
            "description": self.issue_description,
            "steps": self.get_base_solving_steps() + self.get_specific_steps(),
            "ai_guidance": ai_response,
        }

        summary_file = Path(__file__).parent / "problem_solving_sessions.json"
        sessions = []

        if summary_file.exists():
            try:
                sessions = json.loads(summary_file.read_text())
            except:
                sessions = []

        sessions.append(summary)
        summary_file.write_text(json.dumps(sessions, indent=2))
        print(f"\nSession saved to: {summary_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Interactive Problem Solving Guide")
    parser.add_argument(
        "--mode",
        choices=["interactive", "quick"],
        default="interactive",
        help="Questioning mode",
    )
    parser.add_argument(
        "--ai",
        default="claude-sonnet",
        choices=[
            "claude-sonnet",
            "claude-opus",
            "gemini-pro",
            "deepseek-v3.2",
            "mistral-medium",
        ],
        help="Preferred AI model",
    )

    args = parser.parse_args()

    solver = ProblemSolver()
    solver.run(mode=args.mode, ai_model=args.ai)


if __name__ == "__main__":
    main()
