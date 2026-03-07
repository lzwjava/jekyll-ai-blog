import os
import sys
import re


def get_package(file_path):
    """
    Extract the package name from a .java file.

    Args:
        file_path (str): Path to the .java file.

    Returns:
        str: The package name, or None if not found.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r"^\s*package\s+([\w.]+);", line)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return None


def get_specific_imports(file_path):
    """
    Extract specific class imports from a .java file, excluding wildcard imports.

    Args:
        file_path (str): Path to the .java file.

    Returns:
        list: List of fully qualified imported class names.
    """
    imports = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r"^\s*import\s+([\w.]+);", line)
                if match:
                    imp = match.group(1)
                    # Exclude wildcard imports (e.g., import java.util.*;)
                    if not imp.endswith(".*"):
                        imports.append(imp)
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return imports


def get_package_group(full_class_name, level):
    """
    Get the package group based on the first 'level' parts of the package name.

    Args:
        full_class_name (str): Fully qualified class name (e.g., "org.springframework.boot.App").
        level (int): Number of package levels to include (e.g., 1 for "org", 2 for "org.springframework").

    Returns:
        str: The package group (e.g., "org" or "org.springframework").
    """
    package = ".".join(
        full_class_name.split(".")[:-1]
    )  # Extract package, excluding class name
    parts = package.split(".")
    if len(parts) <= level:
        return package  # Use full package if it has fewer or equal parts than level
    else:
        return ".".join(parts[:level])  # Use first 'level' parts


if __name__ == "__main__":
    # Check for command-line arguments: root_directory and level
    if len(sys.argv) != 3:
        print("Usage: python script.py <root_directory> <level>")
        sys.exit(1)

    root_dir = sys.argv[1]
    try:
        level = int(sys.argv[2])
        if level < 1:
            raise ValueError
    except ValueError:
        print("Error: level must be a positive integer")
        sys.exit(1)

    all_classes = set()

    # First pass: Collect all fully qualified class names in the project
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                package = get_package(file_path)
                if package:
                    class_name = file.replace(".java", "")
                    full_class_name = f"{package}.{class_name}"
                    all_classes.add(full_class_name)

    # Store dependencies between package groups
    group_dependencies = set()

    # Second pass: Analyze dependencies based on package groups
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                package = get_package(file_path)
                if package:
                    class_name = file.replace(".java", "")
                    full_class_name = f"{package}.{class_name}"
                    importer_group = get_package_group(full_class_name, level)
                    imports = get_specific_imports(file_path)
                    for imp in imports:
                        # Only include dependencies on classes within the project
                        # Exclude self-dependencies
                        if imp in all_classes and imp != full_class_name:
                            imported_group = get_package_group(imp, level)
                            if imported_group != importer_group:
                                group_dependencies.add((importer_group, imported_group))

    # Output the dependency graph in DOT format
    print("digraph G {")
    for from_group, to_group in sorted(group_dependencies):
        print(f'  "{from_group}" -> "{to_group}";')
    print("}")
