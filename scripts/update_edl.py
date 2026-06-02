#!/usr/bin/env python3

import argparse
import requests
import sys

USOM_API = "https://www.usom.gov.tr/api/address/index"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, choices=["ip", "domain", "url"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    results = set()
    page = 1

    try:
        while True:
            r = requests.get(
                USOM_API,
                params={"q": "", "type": args.type, "page": page},
                headers={
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=60
            )
            r.raise_for_status()

            data = r.json()
            models = data.get("models", [])

            if not models:
                break

            for item in models:
                value = item.get("url") or item.get("address")
                if value:
                    results.add(value.strip())

            if page >= int(data.get("pageCount", page)):
                break

            page += 1

        with open(args.output, "w", encoding="utf-8") as f:
            for item in sorted(results):
                f.write(item + "\n")

        print(f"{args.type} feed created: {len(results)} records")

    except Exception as e:
        print(f"Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
