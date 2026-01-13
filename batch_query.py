#!/usr/bin/env python3
"""Make batch query request to uaas.kaixindou.net."""

import json
import requests
from pathlib import Path

# Configuration
URL = "https://uaas.kaixindou.net/service/batchQuery"

HEADERS = {
    "Content-Length": "42",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="143", "Not A(Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://uaas-test.kaixindou.net",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://uaas.kaixindou.net/html/tool.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i"
}

# Default parameters
DEFAULT_PARAMS = {
    "appId": "ikxd",
    "with_oa": "1",
    "type": "3",
    "vals": "1773074531"
}


def make_batch_query(params=None, save_response=True, verbose=False):
    """
    Make a batch query request.

    Args:
        params: Dictionary of query parameters (uses defaults if None)
        save_response: Whether to save the response to a file
        verbose: Print full request details

    Returns:
        Response object
    """
    if params is None:
        params = DEFAULT_PARAMS

    print(f"Making batch query request to {URL}")
    print(f"Parameters: {params}")

    if verbose:
        print("\n--- Request Details ---")
        print(f"URL: {URL}")
        print(f"Method: POST")
        print(f"Headers:")
        for key, val in HEADERS.items():
            print(f"  {key}: {val}")
        print(f"Body: {params}")

    try:
        response = requests.post(
            URL,
            data=params,
            headers=HEADERS,
            timeout=10
        )

        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Size: {len(response.content)} bytes")

        # Try to parse as JSON
        try:
            response_json = response.json()
            print("\n--- Response (JSON) ---")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))

            if save_response:
                output_file = Path(__file__).parent / "batch_query_response.json"
                output_file.write_text(json.dumps(response_json, indent=2, ensure_ascii=False))
                print(f"\nResponse saved to: {output_file}")
        except json.JSONDecodeError:
            print("\n--- Response (Text) ---")
            print(response.text)

            if save_response:
                output_file = Path(__file__).parent / "batch_query_response.txt"
                output_file.write_text(response.text)
                print(f"\nResponse saved to: {output_file}")

        return response

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Make batch query request")
    parser.add_argument("--appId", default="ikxd", help="App ID")
    parser.add_argument("--with_oa", default="1", help="With OA flag")
    parser.add_argument("--type", default="3", help="Type parameter (e.g., 3=user, try 1,2,4)")
    parser.add_argument("--vals", default="1773074531", help="Comma-separated values to query")
    parser.add_argument("--no-save", action="store_true", help="Don't save response to file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    params = {
        "appId": args.appId,
        "with_oa": args.with_oa,
        "type": args.type,
        "vals": args.vals
    }

    print(f"\nNote: API returned '不存在' (does not exist) for value {args.vals}")
    print("Try different values or types if this value doesn't exist in the system.\n")

    make_batch_query(params, save_response=not args.no_save, verbose=args.verbose)


if __name__ == "__main__":
    main()
