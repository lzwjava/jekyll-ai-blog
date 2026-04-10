def sample_code():
    """
    A function to demonstrate refactoring by reading content from a file.
    Returns the content of the specified file.
    """
    file_path = "scripts/translation/mistral_client.py"
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    print(sample_code())
