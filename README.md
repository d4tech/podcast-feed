# podcast-feed

Personal RSS feed for system-design revision audio (generated with ElevenLabs from Obsidian notes).

Feed: https://d4tech.github.io/podcast-feed/feed.xml

Add an episode: copy the MP3 into `episodes/`, add an entry to `episodes.json`, then
`python3 build_feed.py https://d4tech.github.io/podcast-feed <owner_email> && git add -A && git commit -m "Add episode" && git push`.
