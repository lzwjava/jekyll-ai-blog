#!/usr/bin/env python3

import tiktoken


def basic_encoding():
    """Basic text encoding and decoding example."""
    # Initialize the tokenizer for GPT-3.5-turbo
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # Sample text
    text = "Hello, how are you doing today?"

    # Encode text to tokens
    tokens = enc.encode(text)
    print("Original text:", text)
    print("Tokens:", tokens)
    print("Number of tokens:", len(tokens))

    # Decode tokens back to text
    decoded_text = enc.decode(tokens)
    print("Decoded text:", decoded_text)
    print()


def different_models():
    """Compare tokenization across different models."""
    models = ["gpt-4", "gpt-3.5-turbo", "text-davinci-003"]
    text = "The quick brown fox jumps over the lazy dog."

    for model in models:
        enc = tiktoken.encoding_for_model(model)
        tokens = enc.encode(text)
        print(f"{model}: {len(tokens)} tokens")
        print("Tokens:", tokens)
    print()


def batch_processing():
    """Process multiple texts at once."""
    enc = tiktoken.encoding_for_model("gpt-4")

    texts = [
        "First message",
        "Second message is longer",
        "Third message is the longest one in this batch",
    ]

    # Encode all texts
    all_tokens = [enc.encode(text) for text in texts]
    total_tokens = sum(len(tokens) for tokens in all_tokens)

    print("Batch processing:")
    for text, tokens in zip(texts, all_tokens):
        print(f"'{text}' -> {len(tokens)} tokens")
    print(f"Total tokens in batch: {total_tokens}")
    print()


def special_tokens():
    """Working with special tokens."""
    enc = tiktoken.encoding_for_model("gpt-4")

    # Some tokenizers have special tokens
    special_tokens = enc.special_tokens_set
    print("Special tokens:", special_tokens)

    # Example with potential special characters
    text_with_special = "Hello <|endoftext|> World"
    tokens = enc.encode(text_with_special, allowed_special="all")
    print("Text with special tokens:", text_with_special)
    print("Tokens:", tokens)
    print("Decoded:", enc.decode(tokens))
    print()


def count_tokens_efficiently():
    """Efficiently count tokens without storing all tokens."""
    enc = tiktoken.encoding_for_model("gpt-4")

    text = """
    This is a longer piece of text that we want to count tokens for.
    It contains multiple sentences and paragraphs.
    We can use the len() function on encoded result.
    Or we can count tokens without storing the list.
    """

    # Method 1: Get tokens and count
    tokens = enc.encode(text)
    count1 = len(tokens)

    # Method 2: Encode and count directly (more memory efficient for very long text)
    count2 = len(enc.encode(text))

    print(f"Token count (method 1): {count1}")
    print(f"Token count (method 2): {count2}")
    print(f"Tokens per word: {count1 / len(text.split()):.2f}")
    print()


if __name__ == "__main__":
    print("TikToken Examples")
    print("=" * 50)

    try:
        basic_encoding()
        different_models()
        batch_processing()
        special_tokens()
        count_tokens_efficiently()

        print("All examples completed successfully!")

    except ImportError:
        print("Error: tiktoken not installed. Install with: pip install tiktoken")
    except Exception as e:
        print(f"Error running examples: {e}")
