import argparse
import logging
from clash_utils import switch_clash_proxy_group, setup_logging
from speed import get_top_proxies

# Target groups to switch if they exist
TARGET_GROUPS = [
    "🚀 节点选择",
    "🐟 漏网之鱼",
    "🌍 国外媒体",
    "📺 YouTube",
    "🔍 Google",
    "🤖 OpenAI",
    "📲 电报信息",
    "⌨️ GitHub",
]

# Preferred node filters (avoiding Hong Kong as per plan)
NODE_FILTERS = ["新加坡", "日本", "台湾", "美国", "SG", "JP", "TW", "US"]

def select_best_provider(dry_run=False):
    """
    Selects the best proxy from preferred regions and updates target Clash groups.
    """
    logging.info("Starting automatic proxy selection...")

    # Get the top proxy based on the filters
    top_proxies = get_top_proxies(num_results=1, name_filter=NODE_FILTERS)

    if not top_proxies:
        logging.error("No suitable proxies found matching the filters.")
        print("Error: No suitable proxies found.")
        return

    best_proxy = top_proxies[0]['name']
    latency = top_proxies[0]['latency']

    logging.info(f"Selected best proxy: {best_proxy} (Latency: {latency}ms)")
    print(f"Selected best proxy: {best_proxy} (Latency: {latency}ms)")

    if dry_run:
        logging.info(f"Dry run: Would have switched groups {TARGET_GROUPS} to {best_proxy}")
        print(f"Dry run: Would have switched groups {TARGET_GROUPS} to {best_proxy}")
        return

    # Switch all target groups
    success_count = 0
    for group in TARGET_GROUPS:
        if switch_clash_proxy_group(group, best_proxy):
            success_count += 1

    logging.info(f"Successfully updated {success_count}/{len(TARGET_GROUPS)} groups.")
    print(f"Successfully updated {success_count}/{len(TARGET_GROUPS)} groups.")

def main():
    parser = argparse.ArgumentParser(description="Automatically select the best Clash proxy for main selector groups.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually switching groups.")

    args = parser.parse_args()

    # setup_logging() in clash_utils clears clash.log, which is what we want for a fresh run
    setup_logging()

    select_best_provider(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
