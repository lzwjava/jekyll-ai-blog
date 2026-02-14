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
        first_day_previous.strftime('%Y-%m-%dT00:00:00Z'),
        first_day_current.strftime('%Y-%m-%dT00:00:00Z')
    )

def main():
    parser = argparse.ArgumentParser(description='Get monthly page views & unique visitors from Cloudflare Web Analytics')
    parser.add_argument('--account-id', help='Cloudflare account ID')
    parser.add_argument('--dataset-name', help='Specific Web Analytics dataset name (site domain)')
    parser.add_argument('--start-date', help='Start date YYYY-MM-DDTHH:MM:SSZ')
    parser.add_argument('--end-date', help='End date YYYY-MM-DDTHH:MM:SSZ')
    args = parser.parse_args()

    token = os.environ.get('CLOUDFLARE_API_KEY')
    if not token:
        print('Error: Set CLOUDFLARE_API_KEY environment variable', file=sys.stderr)
        sys.exit(1)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    account_id = args.account_id or os.environ.get('CLOUDFLARE_ACCOUNT_ID') or "4c073cd42000b12a4d61bb679c0043d4"

    if not args.start_date:
        start_date, end_date = get_previous_month_dates()
    else:
        start_date = args.start_date
        end_date = args.end_date or (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')

    # First, get list of datasets if no specific name
    datasets_query = '''
    query {
      viewer {
        accounts(filter: {accountTag: "%s"}) {
          analyticsEngineDatasets {
            name
          }
        }
      }
    }
    ''' % account_id

    response = requests.post('https://api.cloudflare.com/client/v4/graphql', headers=headers, json={'query': datasets_query})
    if response.status_code != 200:
        print(f'Error fetching datasets: {response.status_code} {response.text}', file=sys.stderr)
        sys.exit(1)

    data = response.json()
    if 'errors' in data:
        print(f'GraphQL errors: {json.dumps(data["errors"], indent=2)}', file=sys.stderr)
        sys.exit(1)

    try:
        datasets = data['data']['viewer']['accounts'][0]['analyticsEngineDatasets']
        if not datasets:
            print('No Web Analytics datasets found in account. Enable Web Analytics on your site first.', file=sys.stderr)
            sys.exit(1)

        if args.dataset_name:
            dataset_names = [args.dataset_name]
        else:
            dataset_names = [d['name'] for d in datasets]
            print(f"Found datasets: {', '.join(dataset_names)}")
            if len(dataset_names) > 1:
                print("Using all datasets.", file=sys.stderr)

        total_requests = 0
        total_unique = 0

        for dataset_name in dataset_names:
            query = '''
            query {
              viewer {
                accounts(filter: {accountTag: "%s"}) {
                  analyticsEngineDatasets(filter: {name: "%s"}) {
                    name
                    analyticsEngineMetrics1dGroups(
                      filter: {datetimeGEQ: "%s", datetimeLT: "%s"},
                      limit: 100,
                      orderBy: [datetimeDay_ASC]
                    ) {
                      sum {
                        pageViews
                        uniqueVisitors
                      }
                      dimensions {
                        datetimeDay
                      }
                    }
                  }
                }
              }
            }
            ''' % (account_id, dataset_name, start_date, end_date)

            response = requests.post('https://api.cloudflare.com/client/v4/graphql', headers=headers, json={'query': query})
            if response.status_code != 200:
                print(f'Error for {dataset_name}: {response.status_code} {response.text}', file=sys.stderr)
                continue

            data = response.json()
            if 'errors' in data:
                print(f'GraphQL errors for {dataset_name}: {json.dumps(data["errors"], indent=2)}', file=sys.stderr)
                continue

            try:
                analytics = data['data']['viewer']['accounts'][0]['analyticsEngineDatasets'][0]
                dataset_name_print = analytics['name']
                daily_groups = analytics['analyticsEngineMetrics1dGroups']['groups']
                dataset_requests = sum(group['sum']['pageViews'] for group in daily_groups)
                dataset_unique = sum(group['sum']['uniqueVisitors'] for group in daily_groups)
                total_requests += dataset_requests
                total_unique += dataset_unique
                print(f"Dataset: {dataset_name_print}")
                print(f"  Page views: {dataset_requests:,}")
                print(f"  Approx unique visitors (sum daily): {dataset_unique:,}")
            except (KeyError, IndexError):
                print(f'No data for {dataset_name}', file=sys.stderr)
                continue

        print(f"\nTotal across datasets:")
        print(f"Period: {start_date} to {end_date}")
        print(f"Page views: {total_requests:,}")
        print(f"Approx unique visitors: {total_unique:,} (sum of daily uniques - may overcount)")

    except (KeyError, IndexError) as e:
        print('Error parsing datasets:', json.dumps(data, indent=2), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
