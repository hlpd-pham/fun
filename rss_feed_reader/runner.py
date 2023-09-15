import argparse
import feedparser
import json

def get_latest_entry(feed_url):
    feed = feedparser.parse(feed_url)
    if feed.entries:
        return feed.entries[0]
    return None

def parse_rss_feeds(rss_feeds):
    for feed_author in rss_feeds:
        feed_url = rss_feeds[feed_author]
        entry = get_latest_entry(feed_url)
        if entry:
            print(f"Feed Author: {feed_author}")
            print(f"Title: {entry.title}")
            print(f"Link: {entry.link}")
            print(f"Published: {entry.published}")
        else:
            print(f"No entries found for feed: {feed_url}")
        print('\n')

def main():
    parser = argparse.ArgumentParser(description='Get first article from each RSS feed')
    parser.add_argument('-i', '--input', required=True, help='JSON file contains RSS Feeds and their authors')
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as input_file:
            parse_rss_feeds(json.load(input_file))
    except FileNotFoundError:
        print(f"Input file not found: {args.input}")
    except Exception as e:
        print(f"Encounter error for input: {args.input}, err: {e}")


if __name__ == "__main__":
    main()
