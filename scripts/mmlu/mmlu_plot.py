import matplotlib.pyplot as plt
import os

# Sample data (replace with your actual data)
models = [
    "Mistral 7B Instruct v0.2 (llama.cpp)",
    "Mistral 7B Instruct v0.3 (ollama)",
    "DeepSeek V3 (API)",
    "Gemini 1.5 Flash (API)",
    "DeepSeek R1 (API)",
    "Mistral Small Latest (API)",
    "Mistral Large Latest (API)",
    "Mistral Small 2501 (API)",
    "Grok 2 Latest (API)",
]
accuracy = [40.00, 40.00, 78.00, 72.00, 87.14, 65.00, 73.00, 66.00, 72.00]
subject = "college_computer_science"

# Sort models and accuracy by accuracy
sorted_data = sorted(zip(models, accuracy), key=lambda x: x[1])
models, accuracy = zip(*sorted_data)

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(
    models,
    accuracy,
    color=[
        "skyblue",
        "lightcoral",
        "lightgreen",
        "gold",
        "lightcoral",
        "skyblue",
        "lightcoral",
        "lightgreen",
    ],
)
plt.xlabel("Model")
plt.ylabel("Accuracy (%)")
plt.title(f"MMLU Benchmark Accuracy for {subject} (02 Feb 2025)")
plt.ylim(0, 100)  # Set y-axis limit to 0-100 for percentage
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
plt.tight_layout()

# Add accuracy values on top of the bars
for i, val in enumerate(accuracy):
    plt.text(i, val + 1, f"{val:.2f}%", ha="center", va="bottom")

# Save the chart as a JPG file in the current directory
plt.savefig(os.path.join(os.path.dirname(__file__), "mmlu_accuracy_chart.jpg"))
plt.show()
