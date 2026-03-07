import os


def list_cn_files(directory):
    filenames = sorted(os.listdir(directory))  # Sort filenames
    cn_files = []

    for filename in filenames:
        if filename.endswith("-en.md"):
            cn_file_path = os.path.join(directory, filename)
            with open(cn_file_path, "r", encoding="utf-8") as file:
                content = file.read()
                if "*This blog post was translated by Mistral*" in content:
                    cn_files.append(filename)
                    print(f"File matches criteria: {filename}")

    return cn_files


# Define the directory containing the markdown posts
base_directory = "/Users/lzwjava/projects/lzwjava.github.io"
posts_directory = os.path.join(base_directory, "_posts")

# List the files
cn_files = list_cn_files(posts_directory)

print(f"Files matching criteria: {cn_files}")
