#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime, timedelta
import json
import argparse


def get_previous_month_dates():
    today = datetime.now().date()
    first_day_current = today.replace(day=1)
    last_day_previous = first_day_current - timedelta(days=1)
    first_day_previous = last_day_previous.replace(day=1)
    return (
        first_day_previous.strftime("%Y-%m-%d"),
        first_day_current.strftime("%Y-%m-%d"),
    )


def get_rum_sites(headers, account_id):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/rum/site_info"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(
            f"Error fetching RUM sites: {response.status_code} {response.text}",
            file=sys.stderr,
        )
        return []
    data = response.json()
    if not data.get("success"):
        print(
            f"API error fetching RUM sites: {json.dumps(data, indent=2)}",
            file=sys.stderr,
        )
        return []
    return data["result"]


def main():
    parser = argparse.ArgumentParser(
        description="Get monthly page views & unique visitors from Cloudflare Web Analytics (RUM)"
    )
    parser.add_argument("--account-id", help="Cloudflare account ID")
    parser.add_argument("--site-tag", help="Specific Web Analytics site tag")
    parser.add_argument("--start-date", help="Start date YYYY-MM-DD")
    parser.add_argument("--end-date", help="End date YYYY-MM-DD")
    args = parser.parse_args()

    token = os.environ.get("CLOUDFLARE_API_KEY")
    if not token:
        print("Error: Set CLOUDFLARE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    account_id = (
        args.account_id
        or os.environ.get("CLOUDFLARE_ACCOUNT_ID")
        or "4c073cd42000b12a4d61bb679c0043d4"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    if not args.start_date:
        start_date, end_date = get_previous_month_dates()
    else:
        start_date = args.start_date
        end_date = args.end_date or (datetime.now().date()).strftime("%Y-%m-%d")

    if args.site_tag:
        sites = [{"site_tag": args.site_tag, "site_name": args.site_tag}]
    else:
        sites = get_rum_sites(headers, account_id)
        if not sites:
            print("No Web Analytics sites found.", file=sys.stderr)
            sys.exit(1)
        print(f"Found {len(sites)} sites: {', '.join([s['site_name'] for s in sites])}")

    total_page_views = 0
    total_visits = 0

    for site in sites:
        site_tag = site["site_tag"]
        site_name = site["site_name"]

        # Query structure for rumHealthCheckEvents1dGroups
        # Fallback to analyticsEngineDatasetBindings if rumHealthCheckEvents1dGroups fails
        query = """
        query {
          viewer {
            accounts(filter: { accountTag: "%s" }) {
              rumHealthCheckEvents1dGroups(
                filter: { siteTag: "%s", date_geq: "%s", date_lt: "%s" }
                limit: 100
              ) {
                sum {
                  pageViews
                  visits
                }
              }
            }
          }
        }
        """ % (account_id, site_tag, start_date, end_date)

        response = requests.post(
            "https://api.cloudflare.com/client/v4/graphql",
            headers=headers,
            json={"query": query},
        )
        if response.status_code != 200:
            print(
                f"Error for site {site_name} ({site_tag}): {response.status_code} {response.text}",
                file=sys.stderr,
            )
            continue

        data = response.json()
        if "errors" in data:
            # Try analyticsEngineDatasets if RUM-specific query fails
            query = """
            query {
              viewer {
                accounts(filter: { accountTag: "%s" }) {
                  analyticsEngineDatasetBindings(filter: { dataset: "%s" }) {
                    analyticsEngineMetrics1dGroups(
                      filter: { dateGEQ: "%s", dateLT: "%s" }
                      limit: 100
                    ) {
                      sum {
                        pageViews
                        uniqueVisitors
                      }
                    }
                  }
                }
              }
            }
            """ % (account_id, site_name, start_date, end_date)
            response = requests.post(
                "https://api.cloudflare.com/client/v4/graphql",
                headers=headers,
                json={"query": query},
            )
            data = response.json()

            if "errors" in data:
                print(
                    f"GraphQL errors for site {site_name} ({site_tag}): {json.dumps(data['errors'], indent=2)}",
                    file=sys.stderr,
                )
                continue

            try:
                metrics = data["data"]["viewer"]["accounts"][0][
                    "analyticsEngineDatasetBindings"
                ][0]["analyticsEngineMetrics1dGroups"]
                site_page_views = sum(group["sum"]["pageViews"] for group in metrics)
                site_visits = sum(group["sum"]["uniqueVisitors"] for group in metrics)
            except (KeyError, IndexError):
                print(
                    f"No data for site {site_name} ({site_tag}) via Analytics Engine",
                    file=sys.stderr,
                )
                continue
        else:
            try:
                account_data = data["data"]["viewer"]["accounts"][0]
                daily_groups = account_data["rumHealthCheckEvents1dGroups"]

                site_page_views = sum(
                    group["sum"]["pageViews"] for group in daily_groups
                )
                site_visits = sum(group["sum"]["visits"] for group in daily_groups)
            except (KeyError, IndexError):
                print(f"No data for site {site_name} ({site_tag})", file=sys.stderr)
                continue

        total_page_views += site_page_views
        total_visits += site_visits

        print(f"Site: {site_name}")
        print(f"  Page views: {site_page_views:,}")
        print(f"  Visits: {site_visits:,}")

    print("\nTotal across sites:")
    print(f"Period: {start_date} to {end_date}")
    print(f"Page views: {total_page_views:,}")
    print(f"Visits (sum daily): {total_visits:,}")


if __name__ == "__main__":
    main()
