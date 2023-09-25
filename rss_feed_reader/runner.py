#!/opt/homebrew/bin/python3

import argparse
import asyncio
import json
from parse_rss_feed import parse_rss_feeds

def main():
    parser = argparse.ArgumentParser(description='Get first article from each RSS feed')
    parser.add_argument('-i', '--input', required=True, help='JSON file contains RSS Feeds and their authors')
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as input_file:
            asyncio.run(parse_rss_feeds(json.load(input_file)))
    except FileNotFoundError:
        print(f"Input file not found: {args.input}")
    except Exception as e:
        print(f"Encounter error for input: {args.input}, err: {e}")


if __name__ == "__main__":
    main()
