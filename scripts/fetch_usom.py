#!/usr/bin/env python3

import argparse
import requests
from urllib.parse import urlparse

USOM_URL_LIST = "https://www.usom.gov.tr/url-list.txt"

def normalize_domain(value):
    value = value.strip()
    if not value:
        return None

    if "://" not in value:
        value = "http://" + value

    parsed = urlparse(value)
    host = parsed.hostname

    if not host:
        return None

    return host.lower()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, choices=["domain", "url"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    r = requests.get(USOM_URL_LIST, timeout=60)
    r.raise_for_status()

    lines = r.text.splitlines()
    results = set()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if args.type == "url":
            results.add(line)
        elif args.type == "domain":
            domain = normalize_domain(line)
            if domain:
                results.add(domain)

    with open(args.output, "w", encoding="utf-8") as f:
        for item in sorted(results):
            f.write(item + "\n")

    print(f"{args.type} feed created: {len(results)} records")

if __name__ == "__main__":
    main()
