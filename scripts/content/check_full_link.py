#!/usr/bin/env python3
import os
import re
import argparse


def find_full_links(directory="original", domain="lzwjava.github.io"):
    """
    Search for full links containing the specified domain in markdown files
    """
    full_link_pattern = rf"https://{re.escape(domain)}[^\s\)]*"
    results = []

    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist")
        return results

    print(f"Searching for full links containing '{domain}' in {directory}...")

    for filename in os.listdir(directory):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            matches = re.finditer(full_link_pattern, content)
            for match in matches:
                # Get line number
                line_num = content[: match.start()].count("\n") + 1

                # Get context (the line containing the match)
                lines = content.split("\n")
                context_line = lines[line_num - 1] if line_num <= len(lines) else ""

                results.append(
                    {
                        "file": filepath,
                        "line": line_num,
                        "url": match.group(),
                        "context": context_line.strip(),
                    }
                )

        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Check for full links in markdown files"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default="original",
        help="Directory to search (default: original)",
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="lzwjava.github.io",
        help="Domain to search for (default: lzwjava.github.io)",
    )
    parser.add_argument(
        "--search", type=str, help="Search for specific text containing the link"
    )

    args = parser.parse_args()

    results = find_full_links(args.dir, args.domain)

    if not results:
        print(f"No full links containing '{args.domain}' found in {args.dir}")
        return

    print(f"\nFound {len(results)} full links:")
    print("=" * 80)

    for result in results:
        print(f"File: {result['file']}")
        print(f"Line: {result['line']}")
        print(f"URL: {result['url']}")
        print(f"Context: {result['context']}")
        print("-" * 80)

        # If searching for specific text, check if it matches
        if args.search and args.search.lower() in result["context"].lower():
            print(f"*** MATCH FOUND for search term: '{args.search}' ***")
            print("-" * 80)


if __name__ == "__main__":
    main()
