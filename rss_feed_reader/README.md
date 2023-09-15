## RSS Feed Reader

### Prerequisite
`pip3 install feedparser requests`

### Sample JSON
```json
{
  "TechCrunch": "https://techcrunch.com/feed/",
  "JasonCohen": "https://longform.asmartbear.com/index.xml",
  "ByteByteGo": "https://blog.bytebytego.com/feed",
  "HackerNews": "https://hnrss.org/frontpage",
  "LeadDev": "https://leaddev.com/content-piece-and-series/rss.xml",
  "PracmaticEngineer": "http://feeds.feedburner.com/ThePragmaticEngineer",
  "BetterDev": "https://betterdev.link/rss.xml"
}
```

### Sample Run
```bash
$ python runner.py -i rss_options.json
Feed Author: TechCrunch
Title: Former WarnerMedia CEO Jason Kilar joins Roblox’s board
Link: https://techcrunch.com/2023/09/15/former-warnermedia-ceo-jason-kilar-joins-robloxs-board/
Published: Fri, 15 Sep 2023 15:20:57 +0000


Feed Author: JasonCohen
Title: Stop saying "fail"
Link: https://longform.asmartbear.com/fail/
Published: Sun, 10 Sep 2023 08:00:00 +0000


Feed Author: ByteByteGo
Title: Why is Kafka so fast? How does it work?
Link: https://blog.bytebytego.com/p/why-is-kafka-so-fast-how-does-it
Published: Thu, 14 Sep 2023 15:30:13 GMT


Feed Author: HackerNews
Title: Repeat after me: building any new homes reduces housing costs for all
Link: https://www.ft.com/content/86836af4-6b52-49e8-a8f0-8aec6181dbc5
Published: Fri, 15 Sep 2023 15:15:41 +0000


Feed Author: LeadDev
Title: Building an onboarding plan for engineering managers
Link: https://leaddev.com/process/building-onboarding-plan-engineering-managers
Published: Thu, 14 Sep 2023 08:35:23 +0000


Feed Author: PracmaticEngineer
Title: How Games Typically Get Built
Link: https://blog.pragmaticengineer.com/how-games-typically-get-built/
Published: Tue, 22 Aug 2023 17:31:57 GMT


Feed Author: BetterDev
Title: Issues #248 Aug 14, 2023
Link: https://betterdev.link/issues/248
Published: Mon, 14 Aug 2023 05:19:00 -0700
```

