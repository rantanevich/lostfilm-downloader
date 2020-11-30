#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path
from typing import NamedTuple

import requests
import feedparser
from dotenv import load_dotenv


BASEDIR = Path(__file__).parent
ENV_FILE = BASEDIR / '.env'
SERIES_FILE = BASEDIR / 'series.json'

RSS_URL = 'http://insearch.site/rssdd.xml'

SEASON_PATTERN = re.compile(r'\(S(\d+)')
EPISODE_PATTERN = re.compile(r'E(\d+)\)')
QUALITY_PATTERN = re.compile(r'\[(1080p|MP4|SD)\]')

load_dotenv(dotenv_path=ENV_FILE)

COOKIES = {
    'uid': os.environ.get('LOSTFILM_UID'),
    'usess': os.environ.get('LOSTFILM_USESS')
}
WATCH_DIR = Path(os.environ.get('WATCH_DIR'))


class Torrent(NamedTuple):
    file: Path
    link: str


def main():
    series = json.loads(SERIES_FILE.read_text())

    torrents = []
    rss = feedparser.parse(RSS_URL)
    # newer series at the RSS feed's top
    for item in rss['entries'][::-1]:
        for name in series:
            season = int(SEASON_PATTERN.findall(item['title'])[0])
            episode = int(EPISODE_PATTERN.findall(item['title'])[0])
            quality = QUALITY_PATTERN.findall(item['title'])[0]

            if (episode != 999 and
                    name in item['title'] and
                    series[name]['quality'] == quality and
                    (series[name]['season'] < season or
                        series[name]['episode'] < episode)):
                series[name]['season'] = season
                series[name]['episode'] = episode
                filename = ''.join(c for c in item['title'] if c.isalnum())
                torrents.append(Torrent(
                    file=WATCH_DIR / f'{filename}.torrent',
                    link=item['link']
                ))

    for torrent in torrents:
        response = requests.get(torrent.link, cookies=COOKIES)
        torrent.file.write_bytes(response.content)

    if torrents:
        CONFIG_FILE.write_text(json.dumps(series, indent=4))


if __name__ == "__main__":
    main()
