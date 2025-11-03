"""Simple test script to exercise rate limits on API endpoints.

Usage:
    python scripts/test_rate_limit.py --url http://127.0.0.1:8000 \\
        --endpoints /api/superheroes/ /api/heroes/ --requests 50 --concurrency 1

This script will sequentially send requests to each endpoint and report status codes
and response bodies for failures (including 429 responses). It is intended for
local verification; run this while your Django development server is running.

Notes:
- Keep concurrency low for LocMemCache-based testing since each process has its own cache.
- This script does not require extra packages beyond the Python standard library.
"""

import argparse
import sys
import time
from urllib.parse import urljoin

try:
    import requests
except Exception:
    print("The 'requests' package is required. Install with: pip install requests")
    sys.exit(1)


def hit_endpoint(full_url, count, delay=0.1):
    """Hit an endpoint `count` times with a small delay and report results."""
    print(f"\nHitting {full_url} {count} times (delay={delay}s)")
    for i in range(1, count + 1):
        try:
            r = requests.get(full_url, timeout=5)
        except Exception as e:
            print(f"{i:3d}: ERROR connecting to {full_url}: {e}")
            break

        status = r.status_code
        if status == 429:
            # try to parse JSON retry_after
            try:
                payload = r.json()
            except Exception:
                payload = r.text
            print(f"{i:3d}: {status} -> {payload}")
            return True
        elif status >= 400:
            # show body for other errors too
            body = None
            try:
                body = r.json()
            except Exception:
                body = r.text
            print(f"{i:3d}: {status} -> {body}")
        else:
            # success -> show short info
            print(f"{i:3d}: {status}")
        time.sleep(delay)
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", required=True, help="Base URL, e.g. http://127.0.0.1:8000"
    )
    parser.add_argument(
        "--endpoints", nargs="+", required=True, help="List of endpoint paths to test"
    )
    parser.add_argument(
        "--requests", type=int, default=100, help="Number of requests per endpoint"
    )
    parser.add_argument(
        "--delay", type=float, default=0.1, help="Delay between requests (seconds)"
    )
    args = parser.parse_args()

    base = args.url
    for ep in args.endpoints:
        full = urljoin(base, ep)
        hit = hit_endpoint(full, args.requests, delay=args.delay)
        if not hit:
            print(f"Completed {args.requests} requests to {full} without receiving 429")
        else:
            print(f"Rate limit triggered for {full}")


if __name__ == "__main__":
    main()
