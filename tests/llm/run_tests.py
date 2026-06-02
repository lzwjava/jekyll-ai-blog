#!/usr/bin/env python3
"""
Test runner script for LLM clients
Provides convenient ways to run different test suites
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return success status"""
    print(f"\n{'=' * 60}")
    if description:
        print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    try:
        subprocess.run(cmd, check=True, cwd=Path(__file__).parent)
        print(f"✅ {description or 'Command'} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description or 'Command'} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking test dependencies...")

    required_packages = ["pytest", "requests"]
    missing = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} is missing")

    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False

    return True


def check_api_keys():
    """Check which API keys are available"""
    print("\nChecking API keys for integration tests...")

    api_keys = {
        "DEEPSEEK_API_KEY": "DeepSeek",
        "GEMINI_API_KEY": "Gemini",
        "MISTRAL_API_KEY": "Mistral",
        "OPENROUTER_API_KEY": "OpenRouter",
    }

    available = []
    missing = []

    for env_var, service in api_keys.items():
        if os.getenv(env_var):
            available.append(service)
            print(f"✅ {service} API key is set")
        else:
            missing.append(service)
            print(f"⚠️  {service} API key is not set")

    if available:
        print(f"\nIntegration tests will run for: {', '.join(available)}")
    else:
        print("\nNo API keys found - integration tests will be skipped")

    return len(available) > 0


def main():
    parser = argparse.ArgumentParser(description="Run LLM client tests")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument(
        "--integration", action="store_true", help="Run only integration tests"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run tests with coverage report"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--client",
        choices=["deepseek", "gemini", "mistral", "openrouter"],
        help="Run tests for specific client only",
    )
    parser.add_argument(
        "--quick", action="store_true", help="Run quick tests (exclude slow tests)"
    )
    parser.add_argument(
        "--check", action="store_true", help="Check dependencies and API keys only"
    )

    args = parser.parse_args()

    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)

    # Check API keys
    has_api_keys = check_api_keys()

    if args.check:
        print("\n" + "=" * 60)
        print("Dependency and API key check completed")
        sys.exit(0)

    # Build pytest command
    cmd = ["python", "-m", "pytest"]

    # Add path
    if args.client:
        cmd.append(f"test_{args.client}_client.py")
    else:
        cmd.append(".")

    # Add markers
    markers = []
    if args.unit:
        markers.append("unit")
    elif args.integration:
        markers.append("integration")
        if not has_api_keys:
            print("\n⚠️  No API keys found - integration tests will be skipped")

    if args.quick:
        markers.append("not slow")

    if markers:
        cmd.extend(["-m", " and ".join(markers)])

    # Add other options
    if args.verbose:
        cmd.append("-v")
    else:
        cmd.append("-v")  # Always use verbose for better output

    if args.coverage:
        cmd.extend(["--cov=scripts.llm", "--cov-report=html", "--cov-report=term"])

    # Add common options
    cmd.extend(["--tb=short"])

    # Run the tests
    success = run_command(cmd, "Running LLM client tests")

    if args.coverage and success:
        print("\n📊 Coverage report generated in htmlcov/index.html")

    # Summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests completed successfully!")
    else:
        print("💥 Some tests failed")

    print("\nTest run summary:")
    print(
        f"  Test type: {'Unit only' if args.unit else 'Integration only' if args.integration else 'All tests'}"
    )
    print(f"  Client: {args.client if args.client else 'All clients'}")
    print(f"  Coverage: {'Enabled' if args.coverage else 'Disabled'}")
    print(
        f"  API keys: {len([k for k in ['DEEPSEEK_API_KEY', 'GEMINI_API_KEY', 'MISTRAL_API_KEY', 'OPENROUTER_API_KEY'] if os.getenv(k)])} available"
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
