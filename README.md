# LostFilm.TV Downloader

Downloader checks new series, downloads and places them into torrent's watch directory.

# Requirements

* Python 3.6 or later

# Installation

```sh
git clone
pip install -r requirements.txt
```

# Usage

Script gets sensitive variables from environment. I store them into `.env` within the project's root.

Necessary variables:

| Variable       | Example                          | Description                                                                                 |
|----------------|----------------------------------|---------------------------------------------------------------------------------------------|
| LOSTFILM_UID   | 1234567                          | It locates in "My ID" field of your [account setting](https://www.lostfilm.tv/my_settings)  |
| LOSTFILM_USESS | e134ced312b3511d88943d57ccd70c83 | It can be found in the bottom of popup box when you download series. Click on "usess" label |
| WATCH_DIR      | /data/download/.watch            | Directory for saving torrent files                                                          |

The list of favourite series stores in `series.json`. It also is a tiny database.

Example:
```json
{
    "Mr. Robot": {
        "season": 4,
        "episode": 1,
        "quality": "1080p"
    },
    "Breaking Bad": {
        "season": 3,
        "episode": 6,
        "quality": "MP4"
    },
    "The Queen's Gambit": {
        "season": 1,
        "episode": 1,
        "quality": "SD"
    }
}
```

It can be run as simple Python's scenario:
```sh
python app.py
```

Or set up as a cron job:
```cron
*/30 * * * * ${VENV}/bin/python /opt/lostfilm-downloader/app.py
```
