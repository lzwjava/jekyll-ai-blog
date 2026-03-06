#!/usr/bin/env python3

import re
import matplotlib.pyplot as plt
import numpy as np
import argparse
from pathlib import Path


def parse_training_log(log_file_path):
    """Parse training log file and extract metrics"""
    step_data = []
    iter_data = []

    with open(log_file_path, "r") as f:
        for line in f:
            line = line.strip()

            # Parse step lines (training and validation loss)
            step_match = re.match(
                r"step (\d+): train loss ([\d.]+), val loss ([\d.]+)", line
            )
            if step_match:
                step_num = int(step_match.group(1))
                train_loss = float(step_match.group(2))
                val_loss = float(step_match.group(3))
                step_data.append(
                    {"step": step_num, "train_loss": train_loss, "val_loss": val_loss}
                )

            # Parse iteration lines (loss, time, mfu)
            iter_match = re.match(
                r"iter (\d+): loss ([\d.]+), time ([\d.]+)ms, mfu ([\d.-]+)%", line
            )
            if iter_match:
                iter_num = int(iter_match.group(1))
                loss = float(iter_match.group(2))
                time_ms = float(iter_match.group(3))
                mfu = float(iter_match.group(4))
                iter_data.append(
                    {"iter": iter_num, "loss": loss, "time_ms": time_ms, "mfu": mfu}
                )

    return step_data, iter_data


def create_visualizations(step_data, iter_data):
    """Create matplotlib visualizations of training metrics"""

    # Set up the plotting style
    plt.style.use("default")
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.rcParams["font.size"] = 10

    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("nanoGPT Training Metrics - RTX 4070", fontsize=16, fontweight="bold")

    # Plot 1: Training and Validation Loss over Steps
    if step_data:
        steps = [d["step"] for d in step_data]
        train_losses = [d["train_loss"] for d in step_data]
        val_losses = [d["val_loss"] for d in step_data]

        axes[0, 0].plot(steps, train_losses, "b-", label="Training Loss", linewidth=2)
        axes[0, 0].plot(steps, val_losses, "r-", label="Validation Loss", linewidth=2)
        axes[0, 0].set_xlabel("Training Step")
        axes[0, 0].set_ylabel("Loss")
        axes[0, 0].set_title("Training vs Validation Loss")
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Iteration Loss over Iterations
    if iter_data:
        iters = [d["iter"] for d in iter_data]
        iter_losses = [d["loss"] for d in iter_data]

        axes[0, 1].plot(iters, iter_losses, "g-", linewidth=1.5)
        axes[0, 1].set_xlabel("Iteration")
        axes[0, 1].set_ylabel("Loss")
        axes[0, 1].set_title("Loss per Iteration")
        axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: Training Time per Iteration
    if iter_data:
        iters = [d["iter"] for d in iter_data]
        times = [d["time_ms"] for d in iter_data]

        axes[1, 0].plot(iters, times, "orange", linewidth=1.5)
        axes[1, 0].set_xlabel("Iteration")
        axes[1, 0].set_ylabel("Time (ms)")
        axes[1, 0].set_title("Training Time per Iteration")
        axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Model FLOP Utilization (MFU)
    if iter_data:
        iters = [d["iter"] for d in iter_data]
        mfus = [d["mfu"] for d in iter_data]

        axes[1, 1].plot(iters, mfus, "purple", linewidth=1.5)
        axes[1, 1].set_xlabel("Iteration")
        axes[1, 1].set_ylabel("MFU (%)")
        axes[1, 1].set_title("Model FLOP Utilization (MFU)")
        axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()

    # Only show plot if not in headless environment
    import os

    if os.environ.get("DISPLAY") is not None and os.environ.get("DISPLAY") != "":
        plt.show()

    return fig


def print_statistics(step_data, iter_data):
    """Print basic statistics about the training"""

    print("=" * 50)
    print("TRAINING STATISTICS")
    print("=" * 50)

    if step_data:
        final_step = step_data[-1]
        print(f"Total Steps Completed: {final_step['step']}")
        print(f"Final Training Loss: {final_step['train_loss']:.4f}")
        print(f"Final Validation Loss: {final_step['val_loss']:.4f}")

        # Calculate loss improvement
        initial_loss = step_data[0]["train_loss"]
        final_loss = final_step["train_loss"]
        improvement = ((initial_loss - final_loss) / initial_loss) * 100
        print(f"Training Loss Improvement: {improvement:.1f}%")

    if iter_data:
        final_iter = iter_data[-1]
        print(f"\nTotal Iterations: {final_iter['iter']}")

        # Calculate average time
        avg_time = np.mean([d["time_ms"] for d in iter_data])
        print(f"Average Time per Iteration: {avg_time:.1f}ms")

        # Calculate average MFU
        valid_mfus = [
            d["mfu"] for d in iter_data if d["mfu"] > -50
        ]  # Filter out invalid values
        if valid_mfus:
            avg_mfu = np.mean(valid_mfus)
            print(f"Average MFU: {avg_mfu:.1f}%")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Parse and visualize nanoGPT training logs"
    )
    parser.add_argument("--file", "-f", type=str, help="Path to training log file")
    args = parser.parse_args()

    # File paths
    if args.file:
        log_file = Path(args.file)
    else:
        log_file = Path(__file__).parent / "train_log_openweb.txt"

    if not log_file.exists():
        print(f"Error: Log file {log_file} not found!")
        return

    print(f"Parsing training log: {log_file}")

    # Parse the log data
    step_data, iter_data = parse_training_log(log_file)

    print(f"Found {len(step_data)} step records and {len(iter_data)} iteration records")

    # Print statistics
    print_statistics(step_data, iter_data)

    # Create visualizations
    fig = create_visualizations(step_data, iter_data)

    # Save the plot
    output_path = Path(__file__).parent / "training_metrics.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"\nVisualization saved to: {output_path}")

    # Also save as PDF for high quality
    pdf_path = Path(__file__).parent / "training_metrics.pdf"
    fig.savefig(pdf_path, bbox_inches="tight")
    print(f"High-quality PDF saved to: {pdf_path}")

    plt.show()


if __name__ == "__main__":
    main()
