from datasets import load_dataset
import requests
import json
from tqdm import tqdm
import argparse
import os
from openai import OpenAI
from dotenv import load_dotenv
import time
import random

load_dotenv()

# Set up argument parsing
parser = argparse.ArgumentParser(
    description="Evaluate MMLU dataset with different backends."
)
parser.add_argument(
    "--type",
    type=str,
    default="ollama",
    choices=["ollama", "llama", "deepseek", "gemini", "mistral", "grok"],
    help="Backend type: ollama, llama, deepseek, gemini, mistral or grok",
)
parser.add_argument("--model", type=str, default="", help="Model name")

args = parser.parse_args()

# Load MMLU dataset
subject = "college_computer_science"  # Choose your subject
dataset = load_dataset("cais/mmlu", subject, split="test")


# Format prompt with one-shot example
def format_mmlu_prompt(example):
    prompt = f"Question: {example['question']}\n"
    prompt += "Choices:\n"
    for i, choice in enumerate(example["choices"]):
        prompt += f"{chr(ord('A') + i)}. {choice}\n"
    prompt += "Give your answer. Just give the choice.\n"
    return prompt


# Initialize DeepSeek client if needed
def initialize_deepseek_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY environment variable not set.")
        exit()
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def call_gemini_api(prompt, retries=3, backoff_factor=1):
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        exit()
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    params = {"key": gemini_api_key}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    print(f"Input to Gemini API: {payload}")

    for attempt in range(retries):
        response = requests.post(url, json=payload, params=params)
        response_json = response.json()
        print(response_json)
        if response.status_code == 200:
            return response_json
        elif response.status_code == 429:
            time.sleep(backoff_factor * (2**attempt))  # Exponential backoff
        else:
            raise Exception(
                f"Gemini API Error: {response.status_code} - {response_json}"
            )
    return None


def call_mistral_api(prompt, model="mistral-small-2501", process_response=True):
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("Error: MISTRAL_API_KEY environment variable not set.")
        return None

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    print(f"Input to Mistral API: {data}")
    print(f"Mistral API URL: {url}")
    print(f"Mistral API Headers: {headers}")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        print(response_json)
        if response_json and response_json["choices"]:
            content = response_json["choices"][0]["message"]["content"]
            if process_response:
                return process_mistral_response(content)
            else:
                return content
        else:
            print(f"Mistral API Error: Invalid response format: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Mistral API Error: {e}")
        stre = f"{e}"
        if "429" in stre:
            # print(f"Response status code: {e.response.status_code}")
            # print(f"Response content: {e.response.text}")
            print("Too many requests, sleeping for 10 seconds and retrying")
            time.sleep(10)
            return call_mistral_api(prompt, model, process_response)

        raise e


import re


def process_ollama_response(response):
    if response.status_code == 200:
        print(f"Output from API: {response.json()}")
        output_text = response.json()["choices"][0]["message"]["content"]
        match = re.search(r"Answer:\s*([A-D])", output_text, re.IGNORECASE)
        if not match:
            match = re.search(r"\*\*Answer\*\*:\s*([A-D])", output_text, re.IGNORECASE)
        if not match:
            match = re.search(
                r"The correct answer is\s*([A-D])", output_text, re.IGNORECASE
            )
        if not match:
            match = re.search(
                r"The correct choice is\s*([A-D])", output_text, re.IGNORECASE
            )
        if not match:
            match = re.search(
                r"The correct choice would be\s*([A-D])", output_text, re.IGNORECASE
            )
        if not match:
            match = re.search(r"The answer is\s*([A-D])", output_text, re.IGNORECASE)
        if not match:
            match = re.search(
                r"The answer appears to be\s*([A-D])", output_text, re.IGNORECASE
            )
        if not match:
            match = re.search(
                r"The correct answer should be\s*([A-D])", output_text, re.IGNORECASE
            )
        if not match:
            match = re.search(
                r"The correct answer would be\s*([A-D])", output_text, re.IGNORECASE
            )
        if match:
            predicted_answer = match.group(1).upper()
        else:
            stripped_output = output_text.strip()
            if len(stripped_output) > 0:
                first_word = stripped_output.split(" ")[0]
                if len(first_word) == 1:
                    predicted_answer = first_word
                else:
                    first_word_comma = stripped_output.split(",")[0]
                    if len(first_word_comma) == 1:
                        predicted_answer = first_word_comma
                    else:
                        first_word_period = stripped_output.split(".")[0]
                        if len(first_word_period) == 1:
                            predicted_answer = first_word_period
                        else:
                            print(
                                f"Could not extract a single character answer from the output: {output_text}, returning random answer"
                            )
                            predicted_answer = random.choice(["A", "B", "C", "D"])
            else:
                predicted_answer = ""

        return predicted_answer
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""


def process_llama_response(response):
    if response.status_code == 200:
        output_text = response.json()["choices"][0]["message"]["content"]
        predicted_answer = (
            output_text.strip()[0] if len(output_text.strip()) > 0 else ""
        )
        print(f"Output from API: {output_text}")
        return predicted_answer
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""


def process_deepseek_response(
    client, prompt, model="deepseek-chat", retries=3, backoff_factor=1
):
    print(f"Input to Deepseek API: {prompt}")
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            if response and response.choices:
                output_text = response.choices[0].message.content.strip()
                predicted_answer = (
                    output_text.strip()[0] if len(output_text.strip()) > 0 else ""
                )
                print(f"Output from API: {output_text}")
                return predicted_answer
            else:
                print("Error: No response from the API.")
                return ""
        except Exception as e:
            if "502" in str(e):
                print(
                    f"Bad gateway error (502) during API call, retrying in {backoff_factor * (2**attempt)} seconds..."
                )
                time.sleep(backoff_factor * (2**attempt))
            else:
                print(f"Error during API call: {e}")
                return ""
    return ""


def process_mistral_response(response):
    if response:
        output_text = response.strip()
        predicted_answer = (
            output_text.strip()[0] if len(output_text.strip()) > 0 else ""
        )
        print(f"Output from API: {output_text}")
        return predicted_answer
    else:
        print("Error: No response from Mistral API")
        return ""


def process_gemini_response(prompt):
    json_response = call_gemini_api(prompt)
    if not json_response:
        print("No response from Gemini API after retries.")
        return ""
    if "candidates" not in json_response or not json_response["candidates"]:
        print("No candidates found in the response, retrying...")
        json_response = call_gemini_api(prompt)
        print(json_response)
        if (
            not json_response
            or "candidates" not in json_response
            or not json_response["candidates"]
        ):
            print("No candidates found in the response after retry.")
            return ""

    first_candidate = json_response["candidates"][0]
    if "content" in first_candidate and "parts" in first_candidate["content"]:
        first_part = first_candidate["content"]["parts"][0]
        if "text" in first_part:
            output_text = first_part["text"]
            predicted_answer = (
                output_text.strip()[0] if len(output_text.strip()) > 0 else ""
            )
            print(f"Output from API: {output_text}")
            return predicted_answer
        else:
            print("No text found in the response")
            return ""
    else:
        print("Unexpected response format: content or parts missing")
        return ""


def _call_ollama_api(prompt, model):
    url = "http://localhost:11434/v1/chat/completions"
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model,
        "max_tokens": 400,
    }
    headers = {"Content-Type": "application/json"}
    print(f"Input to API: {data}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return process_ollama_response(response)


def _call_llama_api(prompt):
    url = "http://localhost:8080/v1/chat/completions"
    data = {"messages": [{"role": "user", "content": prompt}]}
    headers = {"Content-Type": "application/json"}
    print(f"Input to API: {data}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return process_llama_response(response)


def _call_grok_api(prompt):
    api_key = os.environ.get("GROK_API_KEY")
    if not api_key:
        print("Error: GROK_API_KEY environment variable not set.")
        return None

    url = "https://api.x.ai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {"model": "grok-2-latest", "messages": [{"role": "user", "content": prompt}]}
    print(f"Input to Grok API: {data}")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        json_response = response.json()
        if "choices" in json_response and json_response["choices"]:
            first_choice = json_response["choices"][0]
            if "message" in first_choice and "content" in first_choice["message"]:
                return process_grok_response(first_choice["message"]["content"])
            else:
                print("Unexpected response format: message or content missing")
                return ""
        else:
            print("No choices found in the response")
            return ""
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        if e.response:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return ""
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return ""


def process_grok_response(response):
    output_text = response.strip()
    predicted_answer = output_text.strip()[0] if len(output_text.strip()) > 0 else ""
    print(f"Output from API: {output_text}")
    return predicted_answer


def _get_predicted_answer(args, prompt, client):
    predicted_answer = ""
    if args.type == "ollama":
        predicted_answer = _call_ollama_api(prompt, args.model)
    elif args.type == "llama":
        predicted_answer = _call_llama_api(prompt)
    elif args.type == "deepseek":
        predicted_answer = process_deepseek_response(client, prompt, args.model)
    elif args.type == "gemini":
        predicted_answer = process_gemini_response(prompt)
    elif args.type == "mistral":
        predicted_answer = call_mistral_api(prompt, args.model)
    elif args.type == "grok":
        predicted_answer = _call_grok_api(prompt)
    else:
        raise ValueError("Invalid backend type")
    return predicted_answer


def evaluate_model(args, dataset):
    correct = 0
    total = 0
    client = None
    if args.type == "deepseek":
        client = initialize_deepseek_client()

    if args.model == "":
        if args.type == "ollama":
            args.model = "mistral:7b"
        elif args.type == "deepseek":
            args.model = "deepseek-chat"
        elif args.type == "mistral":
            args.model = "mistral-small-latest"
        elif args.type == "grok":
            args.model = "grok-2-latest"

    for i, example in tqdm(enumerate(dataset), total=len(dataset), desc="Evaluating"):
        prompt = format_mmlu_prompt(example)
        predicted_answer = _get_predicted_answer(args, prompt, client)

        answer_map = {0: "A", 1: "B", 2: "C", 3: "D"}
        ground_truth_answer = answer_map.get(example["answer"], "")
        is_correct = predicted_answer.upper() == ground_truth_answer
        if is_correct:
            correct += 1
        total += 1

        print(f"Question: {example['question']}")
        print(
            f"Choices: A. {example['choices'][0]}, B. {example['choices'][1]}, C. {example['choices'][2]}, D. {example['choices'][3]}"
        )
        print(
            f"Predicted Answer: {predicted_answer}, Ground Truth: {ground_truth_answer}, Correct: {is_correct}"
        )
        print("-" * 30)

        if (i + 1) % 10 == 0:
            accuracy = correct / total
            print(
                f"Processed {i + 1}/{len(dataset)}. Current Accuracy: {accuracy:.2%} ({correct}/{total})"
            )

    return correct, total


# Evaluation loop
correct, total = evaluate_model(args, dataset)

# Calculate accuracy
accuracy = correct / total
print(f"Subject: {subject}")
print(f"Accuracy: {accuracy:.2%} ({correct}/{total})")
