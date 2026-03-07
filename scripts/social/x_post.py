import os
import sys
import re
import argparse
from dotenv import load_dotenv
import concurrent.futures
import random

# Add the scripts directory to the path to import openrouter_client
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "llm"))
from openrouter_client import call_openrouter_api_with_messages, MODEL_MAPPING

load_dotenv()

INPUT_DIR = "original"
MAX_THREADS = 10


def create_x_post_prompt():
    return """You are a professional social media content creator. You are creating a short post or a thread of posts for X (formerly Twitter) based on a blog post written in English. Each post should be no more than 140 characters. Be concise and engaging. If the content is long, create a thread."""


def generate_x_posts(text):
    print(f"  Generating X post(s): {text[:50]}...")
    prompt = create_x_post_prompt()
    print(f"  Prompt: {prompt}")

    # Randomly select a model from all available models
    selected_model = random.choice(list(MODEL_MAPPING.keys()))
    print(f"  Using model: {selected_model}")

    try:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
        response = call_openrouter_api_with_messages(messages, model=selected_model)
        if response:
            print("  X post(s) generated successfully.")
            return response.split("\n\n")  # Split into multiple posts
        else:
            print("  X post(s) generation failed.")
            return None
    except Exception as e:
        print(f"  X post(s) generation failed with error: {e}")
        if (
            "This model's maximum context length is" in str(e)
            or "context length" in str(e).lower()
        ):
            print("  Skipping X post(s) generation due to context length error.")
            return None
        return None


def generate_x_post_from_markdown_file(input_file, output_file):
    print(f"  Processing file: {input_file}")
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            content = infile.read()

        # Extract front matter
        front_matter_match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
        content_without_front_matter = (
            content[len(front_matter_match.group(0)) :]
            if front_matter_match
            else content
        )
        print(f"  Content: {content_without_front_matter[:50]}...")

        x_posts = generate_x_posts(content_without_front_matter)
        if x_posts:
            with open(output_file, "w", encoding="utf-8") as outfile:
                for idx, post in enumerate(x_posts):
                    outfile.write(f"{post.strip()}\n")
                    if idx < len(x_posts) - 1:
                        outfile.write("---\n")  # Add separator for thread
            print(f"  Finished processing file: {output_file}")
        else:
            print(f"  X post(s) generation failed for {input_file}")
    except Exception as e:
        print(f"  Error processing file {input_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate X posts from markdown files."
    )
    parser.add_argument(
        "--n", type=int, default=None, help="Maximum number of files to process."
    )
    args = parser.parse_args()
    max_files = args.n

    output_dir = "x"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created directory {output_dir}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        processed_count = 0
        futures = []
        for filename in os.listdir(INPUT_DIR):
            if max_files is not None and processed_count >= max_files:
                print(
                    f"Reached max files limit: {max_files}. Stopping X post generation."
                )
                break
            if filename.endswith(".md"):
                input_file = os.path.join(INPUT_DIR, filename)
                output_filename = filename

                output_file = os.path.join(output_dir, output_filename)
                if not os.path.exists(output_file):
                    print(f"Submitting X post generation job for {filename}...")
                    future = executor.submit(
                        generate_x_post_from_markdown_file, input_file, output_file
                    )
                    futures.append(future)
                    processed_count += 1
                else:
                    print(f"Skipping {filename} because {output_file} already exists.")

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"A thread failed: {e}")


if __name__ == "__main__":
    main()
