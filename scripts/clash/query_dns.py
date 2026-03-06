# pip install requests dnspython

import requests
import dns.message
import dns.query
import dns.rdatatype
import argparse


def test_alidns_doh(hostname="example.com", qtype="A"):
    url = "https://dns.alidns.com/dns-query"

    # Build DNS query
    query = dns.message.make_query(hostname, qtype)

    # Send via HTTPS POST (WireFormat)
    r = requests.post(
        url,
        data=query.to_wire(),
        headers={
            "Content-Type": "application/dns-message",
            "Accept": "application/dns-message",
        },
        timeout=5,
    )

    if r.status_code != 200:
        print(f"Failed: HTTP {r.status_code}")
        print(r.text)
        return False

    # Parse response
    response = dns.message.from_wire(r.content)

    print(f"Query: {hostname} {qtype}")
    print("Response:")
    print(response.to_text())

    # Check if we got answers
    if response.answer:
        print("\nAnswers found:")
        for rrset in response.answer:
            for rdata in rrset:
                print(f"  {rrset.name} {rrset.rdclass} {rrset.rdtype} → {rdata}")
        return True
    else:
        print("No answers in response")
        return False


# Test it
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test AliDNS DoH")
    parser.add_argument(
        "hostname",
        nargs="?",
        default="www.google.com",
        help="Hostname to query (default: www.google.com)",
    )
    parser.add_argument("--qtype", "-q", default="A", help="Query type (default: A)")
    args = parser.parse_args()

    success = test_alidns_doh(args.hostname, args.qtype)
    print(f"\nSuccess: {success}")
