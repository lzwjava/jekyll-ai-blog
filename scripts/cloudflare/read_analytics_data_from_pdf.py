#!/usr/bin/env python3
import argparse
import re
import sys
import os
from pypdf import PdfReader


def update_config_yaml(page_views):
    """
    Updates the monthly_page_views in _config.yml
    """
    config_path = os.path.join(os.path.dirname(__file__), "../../_config.yml")
    config_path = os.path.abspath(config_path)

    if not os.path.exists(config_path):
        print(f"Warning: _config.yml not found at {config_path}", file=sys.stderr)
        return

    try:
        with open(config_path, "r") as f:
            content = f.read()

        # Pattern to find monthly_page_views: followed by optional current value
        pattern = r"monthly_page_views:.*"
        replacement = f"monthly_page_views: {page_views}"

        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
        else:
            # If not found, append it
            new_content = content.rstrip() + f"\n\nmonthly_page_views: {page_views}\n"

        with open(config_path, "w") as f:
            f.write(new_content)
        print(f"Updated _config.yml: monthly_page_views = {page_views:,}")
    except Exception as e:
        print(f"Error updating _config.yml: {e}", file=sys.stderr)


def parse_cloudflare_pdf(pdf_path):
    """
    Parses Cloudflare Web Analytics PDF export.
    """
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"Error reading PDF: {e}", file=sys.stderr)
        return None

    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # 1. Extract Site Name
    # Pattern: "Web Analytics for lzwjava.github.io"
    site_match = re.search(r"Web Analytics for\s+([\w\.-]+)", full_text)
    site_name = site_match.group(1) if site_match else "Unknown"
    # Clean up site name if extraction merged it with next word (e.g. "lzwjava.github.ioJan")
    if site_name.endswith("Jan") or site_name.endswith("Feb"):
        site_name = site_name[:-3]
    elif site_name.endswith("Mar") or site_name.endswith("Apr"):
        site_name = site_name[:-3]
    # Add more months if needed, or use a restricted character set
    site_name = re.sub(
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$", "", site_name
    )

    # 2. Extract Date Range
    # Pattern: "Jan 16th 202604:03 (UTC +08:00)Feb 15th 202604:03 (UTC +08:00)"
    # Note: The PDF text extraction often removes spaces between the first date and the second start.
    date_pattern = r"([A-Z][a-z]{2}\s+\d{1,2}(?:st|nd|rd|th)?\s+\d{4})"
    dates = re.findall(date_pattern, full_text)
    date_range = " to ".join(dates[:2]) if len(dates) >= 2 else "Unknown"

    # 3. Extract Total Page Views (High Precision from Hosts section)
    # Pattern: "Hosts\s+lzwjava.github.io\s+17,930"
    hosts_match = re.search(r"Hosts\s+[\w\.-]+\s+([\d,]+)", full_text)
    if hosts_match:
        page_views = int(hosts_match.group(1).replace(",", ""))
    else:
        # Fallback to summary section (Low Precision)
        # Pattern: "Total page views\s+17 .93k" (note the potential space from PDF extraction)
        summary_match = re.search(r"Total page views\s+([\d\s\.]+k)", full_text)
        if summary_match:
            val_str = summary_match.group(1).replace(" ", "").replace("k", "")
            page_views = int(float(val_str) * 1000)
        else:
            page_views = 0

    return {
        "site": site_name,
        "date_range": date_range,
        "page_views": page_views,
        "full_text": full_text,
    }


def main():
    parser = argparse.ArgumentParser(description="Parse Cloudflare Analytics PDF")
    parser.add_argument(
        "--file", help="Path to the Cloudflare Web Analytics PDF export"
    )
    parser.add_argument(
        "--no-update-config",
        action="store_false",
        dest="update_config",
        help="Do not update monthly_page_views in _config.yml",
    )
    parser.set_defaults(update_config=True)
    parser.add_argument(
        "pdf_file",
        nargs="?",
        help="Path to the Cloudflare Web Analytics PDF export (legacy positional argument)",
    )
    args = parser.parse_args()

    pdf_path = args.file or args.pdf_file
    if not pdf_path:
        parser.error(
            "The following arguments are required: --file or a positional pdf_file path"
        )

    data = parse_cloudflare_pdf(pdf_path)
    if not data:
        sys.exit(1)

    print("Cloudflare Web Analytics Report")
    print("==============================")
    print(f"Site:       {data['site']}")
    print(f"Period:     {data['date_range']}")
    print(f"Page Views: {data['page_views']:,}")

    if args.update_config:
        update_config_yaml(data["page_views"])

    print("\nExtracted Text:")
    print("--------------")
    print(data["full_text"])


if __name__ == "__main__":
    main()
