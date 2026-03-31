import argparse
import sys
import requests

API_URL = "http://127.0.0.1:5000/api/build"
ALLOWED_PLATFORMS = {"android", "ios", "windows", "mac", "linux"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="SWAB CLI - Trigger headless builds"
    )

    parser.add_argument("--app-name", required=True)
    parser.add_argument("--app-description", required=True)
    parser.add_argument("--app-version", required=True)
    parser.add_argument("--build-number", required=True)
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--web-url", required=True)

    parser.add_argument(
        "--platforms",
        nargs="+",
        required=True,
        help="Target platforms (android ios windows mac linux)"
    )

    return parser.parse_args()


def validate_platforms(platforms):
    invalid = [p for p in platforms if p not in ALLOWED_PLATFORMS]
    if invalid:
        print(f"Error: Unsupported platform(s): {', '.join(invalid)}")
        sys.exit(1)


def main():
    args = parse_args()
    validate_platforms(args.platforms)

    payload = {
        "app_name": args.app_name,
        "app_description": args.app_description,
        "app_version": args.app_version,
        "build_number": args.build_number,
        "package_name": args.package_name,
        "web_url": args.web_url,
        "platforms": args.platforms,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"Failed to connect to backend: {e}")
        sys.exit(1)

    if response.status_code != 200:
        print("Build request failed:")
        print(response.text)
        sys.exit(1)

    data = response.json()
    print("Build started successfully")
    print(f"Build ID: {data.get('build_id')}")


if __name__ == "__main__":
    main()
