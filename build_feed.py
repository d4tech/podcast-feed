#!/usr/bin/env python3
"""Build feed.xml (podcast RSS) from episodes.json + the MP3s in episodes/.

episodes.json: [{"file": "episodes/x.mp3", "title": ..., "description": ..., "date": "2026-10-24T12:00:00+05:30"}]
Usage: build_feed.py <base_url> <owner_email>   e.g. https://d4tech.github.io/podcast-feed relay@privaterelay.appleid.com
"""
import json, os, subprocess, sys, email.utils, datetime
from xml.sax.saxutils import escape

base = sys.argv[1].rstrip("/")
owner_email = sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
eps = json.load(open(os.path.join(here, "episodes.json")))

def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    s = int(float(out.strip()))
    return f"{s//3600:02d}:{s%3600//60:02d}:{s%60:02d}"

items = []
for n, e in sorted(enumerate(eps, 1), key=lambda x: x[1]["date"], reverse=True):
    p = os.path.join(here, e["file"])
    d = datetime.datetime.fromisoformat(e["date"])
    url = f"{base}/{e['file'].replace(' ', '%20')}"
    items.append(f"""    <item>
      <title>{escape(e['title'])}</title>
      <description>{escape(e['description'])}</description>
      <enclosure url="{escape(url)}" length="{os.path.getsize(p)}" type="audio/mpeg"/>
      <guid isPermaLink="false">{escape(e['file'])}</guid>
      <pubDate>{email.utils.format_datetime(d)}</pubDate>
      <itunes:duration>{duration(p)}</itunes:duration>
      <itunes:episode>{n}</itunes:episode>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>System Design Revision</title>
    <link>{base}/</link>
    <description>Long-form audio revision for senior and staff system design interviews: requirements, back-of-envelope numbers, deep dives, curveballs and trade-offs, one canonical design per episode.</description>
    <language>en</language>
    <itunes:author>Quorum Notes</itunes:author>
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>episodic</itunes:type>
    <itunes:category text="Technology"/>
    <itunes:category text="Education"/>
    <itunes:owner>
      <itunes:name>Quorum Notes</itunes:name>
      <itunes:email>{escape(owner_email)}</itunes:email>
    </itunes:owner>
    <itunes:image href="{base}/cover.png"/>
{chr(10).join(items)}
  </channel>
</rss>
"""
open(os.path.join(here, "feed.xml"), "w").write(feed)
print(f"feed.xml: {len(items)} episodes → {base}/feed.xml")
