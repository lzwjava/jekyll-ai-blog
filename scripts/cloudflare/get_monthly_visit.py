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
        first_day_previous.strftime('%Y-%m-%d'),
        first_day_current.strftime('%Y-%m-%d')
    )

def get_zones(headers):
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    if response.status_code != 200:
        print(f'Error fetching zones: {response.status_code} {response.text}', file=sys.stderr)
        return []
    data = response.json()
    if not data.get('success'):
        print(f'API error fetching zones: {json.dumps(data, indent=2)}', file=sys.stderr)
        return []
    return data['result']

def main():
    parser = argparse.ArgumentParser(description='Get monthly page views & unique visitors from Cloudflare Zone HTTP Analytics')
    parser.add_argument('--zone-id', help='Cloudflare zone ID')
    parser.add_argument('--start-date', help='Start date YYYY-MM-DD')
    parser.add_argument('--end-date', help='End date YYYY-MM-DD')
    args = parser.parse_args()

    token = os.environ.get('CLOUDFLARE_API_KEY')
    if not token:
        print('Error: Set CLOUDFLARE_API_KEY environment variable', file=sys.stderr)
        sys.exit(1)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    if not args.start_date:
        start_date, end_date = get_previous_month_dates()
    else:
        start_date = args.start_date
        end_date = args.end_date or (datetime.now().date()).strftime('%Y-%m-%d')

    if args.zone_id:
        zones = [{'id': args.zone_id, 'name': args.zone_id}]
    else:
        zones = get_zones(headers)
        if not zones:
            print('No zones found.', file=sys.stderr)
            sys.exit(1)
        print(f"Found {len(zones)} zones: {', '.join([z['name'] for z in zones])}")

    total_page_views = 0
    total_visits = 0
    total_requests = 0

    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']

        query = '''
        query {
          viewer {
            zones(filter: { zoneTag: "%s" }) {
              httpRequests1dGroups(
                filter: { date_geq: "%s", date_lt: "%s" }
                limit: 100
              ) {
                sum {
                  pageViews
                  visits
                  requests
                }
                dimensions {
                  date
                }
              }
            }
          }
        }
        ''' % (zone_id, start_date, end_date)

        response = requests.post('https://api.cloudflare.com/client/v4/graphql', headers=headers, json={'query': query})
        if response.status_code != 200:
            print(f'Error for zone {zone_name} ({zone_id}): {response.status_code} {response.text}', file=sys.stderr)
            continue

        data = response.json()
        if 'errors' in data:
            print(f'GraphQL errors for zone {zone_name} ({zone_id}): {json.dumps(data["errors"], indent=2)}', file=sys.stderr)
            continue

        try:
            zone_data = data['data']['viewer']['zones'][0]
            daily_groups = zone_data['httpRequests1dGroups']

            zone_page_views = sum(group['sum']['pageViews'] for group in daily_groups)
            zone_visits = sum(group['sum']['visits'] for group in daily_groups)
            zone_requests = sum(group['sum']['requests'] for group in daily_groups)

            total_page_views += zone_page_views
            total_visits += zone_visits
            total_requests += zone_requests

            print(f"Zone: {zone_name}")
            print(f"  Page views: {zone_page_views:,}")
            print(f"  Visits: {zone_visits:,}")
            print(f"  Requests: {zone_requests:,}")
        except (KeyError, IndexError):
            print(f'No data for zone {zone_name} ({zone_id})', file=sys.stderr)
            continue

    print(f"\nTotal across zones:")
    print(f"Period: {start_date} to {end_date}")
    print(f"Page views: {total_page_views:,}")
    print(f"Visits (sum daily): {total_visits:,}")
    print(f"Requests: {total_requests:,}")

if __name__ == '__main__':
    main()
