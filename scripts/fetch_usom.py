#!/usr/bin/env python3

import argparse
import requests
import sys
import time

USOM_API = "https://www.usom.gov.tr/api/address/index"


def extract_value(item):
    for key in ["url", "address", "value", "indicator"]:
        if key in item and item[key]:
            return str(item[key]).strip()
    return None


def fetch_usom(indicator_type):
    page = 1
    results = set()

    while True:
        params = {
            "type": indicator_type,
            "page": page
        }

        r = requests.get(USOM_API, params=params, timeout=30)
        r.raise_for_status()

        data = r.json()
        models = data.get("models", [])

        if not models:
            break

        for item in models:
            value = extract_value(item)
            if value:
                results.add(value)

        page_count = data.get("pageCount")

        if page_count and page >= int(page_count):
            break

        page += 1
        time.sleep(0.5)

    return sorted(results)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, choices=["ip", "domain", "url"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        data = fetch_usom(args.type)

        with open(args.output, "w", encoding="utf-8") as f:
            for item in data:
                f.write(item + "\n")

        print(f"{args.type} listesi oluşturuldu: {len(data)} kayıt")

    except Exception as e:
        print(f"Hata: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
