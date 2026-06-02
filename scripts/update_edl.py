import requests
import os
import argparse
import sys

BASE_URL = "https://siberguvenlik.gov.tr/api/address/index"
PER_PAGE = 5000
MAX_RECORDS = 100000

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


def fetch_type(ioc_type):
    page = 0
    results = set()

    while True:
        params = {
            "type": ioc_type,
            "page": page,
            "per-page": PER_PAGE
        }

        r = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=60,
            allow_redirects=True
        )

        r.raise_for_status()

        data = r.json()
        models = data.get("models", [])

        if not models:
            break

        for item in models:
            value = (
                item.get("url")
                or item.get("address")
                or item.get("value")
            )

            if value:
                results.add(value.strip())

                if len(results) >= MAX_RECORDS:
                    print(
                        f"{ioc_type.upper()} limiti ({MAX_RECORDS}) ulaşıldı."
                    )
                    return sorted(results)

        page_count = data.get("pageCount", 1)
        page += 1

        if page >= page_count:
            break

    return sorted(results)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        required=True,
        choices=["ip", "domain", "url"]
    )
    parser.add_argument(
        "--output",
        required=True
    )

    args = parser.parse_args()

    try:
        output_dir = os.path.dirname(args.output)

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        results = fetch_type(args.type)

        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
            f.write("\n")

        print(f"Type      : {args.type}")
        print(f"Count     : {len(results)}")
        print(f"Max Limit : {MAX_RECORDS}")
        print(f"Output    : {args.output}")

    except Exception as e:
        print(f"Hata: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
