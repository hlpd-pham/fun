import argparse
import aiohttp
import asyncio
import feedparser
import json
import requests

async def fetch_feed(session, feed_url, timeout_duration=10):
    try:
        async with session.get(feed_url, timeout=timeout_duration) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Error {response.status} while fetching {feed_url}")
    except asyncio.TimeoutError:
        print(f"Timeout occurred for {feed_url}")
    except Exception as e:
        print(f"Error fetching {feed_url}. Error: {e}")
    return None

async def get_latest_entry(feed_url, timeout_duration=10):
    async with aiohttp.ClientSession() as session:
        content = await fetch_feed(session, feed_url, timeout_duration)
        if content:
            feed = feedparser.parse(content)
            if feed.entries:
                return feed.entries[0]
    return None

async def parse_rss_feeds(rss_feeds):
    tasks = [get_latest_entry(feed_url) for feed_url in rss_feeds.values()]

    results = await asyncio.gather(*tasks)

    for feed_author, entry in zip(rss_feeds.keys(), results):
        if entry:
            print(f"Feed Author: {feed_author}")
            print(f"Title: {entry.title}")
            print(f"Link: {entry.link}")
            print(f"Published: {entry.published}")
        else:
            print(f"No entries found for feed: {rss_feeds[feed_author]}")
        print('\n')


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
