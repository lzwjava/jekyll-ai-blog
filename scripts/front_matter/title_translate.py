import os
import boto3
import json


def contains_chinese(text):
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def create_prompt(text, target_language):
    if target_language == "en":
        return f"<s>[INST]Translate the following Chinese text to English, and provide the translation in title case without any Chinese characters or punctuation: {text}[/INST]</s>"
    else:
        return f"<s>[INST]Translate the following English text to Chinese, and provide only the Chinese translation without any English characters or punctuation: {text}[/INST]</s>"


def translate_text(text, target_language):
    session = boto3.Session(region_name="us-east-1")
    bedrock_runtime = session.client("bedrock-runtime")

    prompt = create_prompt(text, target_language)

    body = {
        "prompt": prompt,
        "max_tokens": 4096,
        "top_k": 50,
        "top_p": 0.7,
        "temperature": 0.7,
    }

    response = bedrock_runtime.invoke_model(
        modelId="mistral.mistral-7b-instruct-v0:2",
        body=json.dumps(body),
        contentType="application/json",
    )

    response_body = response["body"].read().decode("utf-8")
    output = json.loads(response_body)

    extracted_text = output["outputs"][0]["text"]
    return extracted_text.title()  # Convert the translated text to title case


def process_files_in_directory(directory):
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for filename in os.listdir(directory):
        if filename.endswith("-en.md"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            title_line_index = next(
                (i for i, line in enumerate(lines) if line.startswith("title:")), None
            )
            if title_line_index is not None:
                title_line = lines[title_line_index]
                title = title_line.replace("title:", "").strip().strip('"')

                if contains_chinese(title):
                    print(f"Translating title in {file_path}")
                    translated_title = translate_text(title, "en")
                    new_title_line = f'title: "{translated_title.strip()}"\n'
                    lines[title_line_index] = new_title_line

                    with open(file_path, "w", encoding="utf-8") as file:
                        file.writelines(lines)
                    print(
                        f"Updated title in {file_path} to '{translated_title.strip()}'"
                    )


# Get the absolute path to the _posts directory
current_directory = os.path.dirname(os.path.abspath(__file__))
posts_directory = os.path.join(current_directory, "../_posts")

process_files_in_directory(posts_directory)
