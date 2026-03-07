#!/usr/bin/env python3

import re


def calculate_training_duration(log_file):
    """Calculate total training duration from training log"""

    total_time_ms = 0
    iteration_count = 0

    with open(log_file, "r") as f:
        for line in f:
            # Look for iteration lines with time information
            # Format: iter X: loss Y, time Zms, mfu W%
            match = re.search(r"iter (\d+): loss [\d.]+, time ([\d.]+)ms", line)
            if match:
                iteration = int(match.group(1))
                time_ms = float(match.group(2))
                total_time_ms += time_ms
                iteration_count += 1

    # Convert to hours, minutes, seconds
    total_seconds = total_time_ms / 1000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60

    return {
        "total_iterations": iteration_count,
        "total_time_ms": total_time_ms,
        "total_time_seconds": total_seconds,
        "total_time_formatted": f"{hours:02d}:{minutes:02d}:{seconds:05.2f}",
    }


if __name__ == "__main__":
    log_file = "/home/lzw/projects/blog-source/scripts/train/evaluate.txt"
    results = calculate_training_duration(log_file)

    print("Training Analysis:")
    print(f"Total iterations: {results['total_iterations']}")
    print(f"Total time: {results['total_time_ms']:,.2f} ms")
    print(f"Total time: {results['total_time_seconds']:,.2f} seconds")
    print(f"Total duration: {results['total_time_formatted']}")

    # Calculate average time per iteration
    avg_time_ms = results["total_time_ms"] / results["total_iterations"]
    print(f"Average time per iteration: {avg_time_ms:.2f} ms")
