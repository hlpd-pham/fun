"""
RSS Feed Reader
----------------

This script allows users to fetch and display the latest entry from a list of 
RSS feeds provided in a JSON file. Each feed is fetched concurrently, making the 
process faster when dealing with multiple feeds.

Expected JSON Format:
{
    "FeedAuthor1": "https://rss.feed.url/1",
    "FeedAuthor2": "https://rss.feed.url/2",
    ...
}

Usage:
python script_name.py -i path_to_json_file.json

Dependencies:
- aiohttp
- asyncio
- feedparser
"""

import argparse
import aiohttp
import asyncio
import feedparser
import json

async def fetch_feed(session, feed_url, timeout_duration=10):
    """
    Fetch content from the RSS feed URL.

    Args:
    - session: aiohttp ClientSession for making HTTP requests.
    - feed_url (str): URL of the RSS feed.
    - timeout_duration (int, optional): Duration in seconds before timing out the request. Defaults to 10 seconds.

    Returns:
    - str: Raw content of the RSS feed if fetched successfully, None otherwise.
    """
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
    """
    Fetch and parse the latest entry from the RSS feed URL.

    Args:
    - feed_url (str): URL of the RSS feed.
    - timeout_duration (int, optional): Duration in seconds before timing out the request. Defaults to 10 seconds.

    Returns:
    - feedparser.FeedParserDict: Parsed latest entry from the RSS feed.
    """
    async with aiohttp.ClientSession() as session:
        content = await fetch_feed(session, feed_url, timeout_duration)
        if content:
            feed = feedparser.parse(content)
            if feed.entries:
                return feed.entries[0]
    return None

async def parse_rss_feeds(rss_feeds):
    """
    Concurrently fetch and display the latest entries from a list of RSS feeds.

    Args:
    - rss_feeds (dict): Dictionary with feed authors as keys and RSS feed URLs as values.
    """
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
    parser.add_argument('-i', '--input', required=True, help='JSON file containing RSS Feeds and their authors')
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as input_file:
            asyncio.run(parse_rss_feeds(json.load(input_file)))
    except FileNotFoundError:
        print(f"Input file not found: {args.input}")
    except Exception as e:
        print(f"Encountered an error for input: {args.input}. Error: {e}")


if __name__ == "__main__":
    main()
