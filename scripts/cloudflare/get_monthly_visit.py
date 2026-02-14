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
    parser = argparse.ArgumentParser(description='Get monthly visits and page views from Cloudflare')
    parser.add_argument('--account-id', help='Cloudflare account ID')
    parser.add_argument('--zone-id', help='Cloudflare zone ID')
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
    zone_id = args.zone_id or os.environ.get('CLOUDFLARE_ZONE_ID')

    if not zone_id:
        print('''
To use:
- Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_ZONE_ID env vars, or pass --account-id and --zone-id

To find your IDs, run this query in GraphQL explorer or curl:
query {
  viewer {
    accounts {
      id
      name
      zones(filter: {status: "active"}) {
        id
        name
      }
    }
  }
}
        ''', file=sys.stderr)
        sys.exit(1)

    if not args.start_date:
        start_date, end_date = get_previous_month_dates()
    else:
        start_date = args.start_date
        end_date = args.end_date or (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')

    query = '''
    query {
      viewer {
        accounts(filter: {accountTag: "%s"}) {
          zones(filter: {zoneTag: "%s"}) {
            name
            httpRequests1dGroups(
              filter: {datetime_geq: "%s", datetime_lt: "%s"},
              limit: 100,
              orderBy: [datetime_ASC]
            ) {
              sum {
                requests
                uniqueVisitors
              }
              dimensions {
                datetime
              }
            }
          }
        }
      }
    }
    ''' % (account_id, zone_id, start_date, end_date)

    response = requests.post('https://api.cloudflare.com/client/v4/graphql', headers=headers, json={'query': query})
    if response.status_code != 200:
        print(f'Error: {response.status_code} {response.text}', file=sys.stderr)
        sys.exit(1)

    data = response.json()
    if 'errors' in data:
        print(f'GraphQL errors: {json.dumps(data["errors"], indent=2)}', file=sys.stderr)
        sys.exit(1)

    try:
        analytics = data['data']['viewer']['accounts'][0]['zones'][0]
        zone_name = analytics['name']
        daily_groups = analytics['httpRequests1dGroups']['groups']
        total_requests = sum(group['sum']['requests'] for group in daily_groups)
        total_unique = sum(group['sum']['uniqueVisitors'] for group in daily_groups)
        print(f"Zone: {zone_name}")
        print(f"Period: {start_date} to {end_date}")
        print(f"Page views (requests): {total_requests:,}")
        print(f"Approx unique visitors: {total_unique:,} (sum of daily uniques)")
    except (KeyError, IndexError) as e:
        print('Error parsing data:', json.dumps(data, indent=2), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
