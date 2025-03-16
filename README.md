# ShareWoodAutomator

** WARNINGS: This is currently work in progress"

ShareWoodAutomator is a Python library that automates interactions with ShareWood.tv, allowing users to search, scrape, and download torrents programmatically.

## Features

- **Login Management**: Seamless authentication to ShareWood.tv
- **Advanced Search**: Customize search parameters with extensive filtering options
- **Torrent Scraping**: Extract detailed information from torrent pages
- **Automated Downloads**: Download torrent files directly through the application

## Installation

```bash
pip install sharewoodautomator
```

## Requirements

- Python 3.6+
- Selenium
- BeautifulSoup4
- python-dotenv
- Chrome WebDriver

## Configuration

Create a `.env` file in your project root with the following variables:

```
SHAREWOOD_URL=https://www.sharewood.tv
SHAREWOOD_LOGIN=https://www.sharewood.tv/login
SHAREWOOD_LOGOUT=https://www.sharewood.tv/logout
SHAREWOOD_TORRENTS=https://www.sharewood.tv/torrents
PSEUDO=your_username
PASSWORD=your_password
```

## Usage

### Basic Usage

```python
from sharewoodautomator import ShareWoodAutomator, ShareWoodSearchCriteria

# Initialize the automator
automator = ShareWoodAutomator(headless=True)

# Connect to ShareWood.tv
automator.connect()

# Create search criteria
criteria = ShareWoodSearchCriteria(
    query="Ubuntu 22.04",
    categories={"Applications": True},
    subcategories={"Application Linux": True},
    languages={"Français": True, "Anglais": True},
    sorting="seeders",
    direction="desc",
    quantity=25
)

# Search for torrents
results = automator.search(criteria)

# Disconnect from ShareWood.tv
automator.disconnect()
```

### Advanced Search

```python
# Create detailed search criteria
criteria = ShareWoodSearchCriteria(
    query="Python programming",
    description="beginner tutorial",
    uploader="top_uploader",
    tags="education,programming",
    categories={"Formations": True},
    languages={"Anglais": True},
    type={"freeleech": True},
    sorting="seeders",
    direction="desc",
    quantity=50
)

# Search for torrents
results = automator.search(criteria)
```

### Downloading a Torrent

```python
# Download a specific torrent by URL
torrent_url = "https://www.sharewood.tv/torrents/view/12345"
automator.download(torrent_url)

# Or download from search results
results = automator.search(criteria)
# Assuming results contains a list of ShareWoodTorrent objects
for torrent in results:
    # Download torrents with more than 10 seeders
    if torrent.seeders > 10:
        torrent.download(download_path="./downloads")
```

## Class Reference

### ShareWoodAutomator

Main class for interacting with ShareWood.tv.

```python
automator = ShareWoodAutomator(headless=True)
```

- `headless` (bool): Run browser in headless mode.

Methods:
- `connect()`: Connect to ShareWood.tv using credentials from .env file
- `disconnect()`: Disconnect from ShareWood.tv
- `search(search_criteria)`: Search for torrents using the provided criteria
- `download(url)`: Download a torrent from the specified URL

### ShareWoodSearchCriteria

Class for defining search criteria.

```python
criteria = ShareWoodSearchCriteria(
    query="example search",
    description="example description",
    uploader="example_user",
    tags="tag1,tag2",
    categories={"Vidéos": True, "Audios": False},
    subcategories={"Application Linux": True},
    languages={"Français": True, "Anglais": True},
    type={"freeleech": True},
    sorting="seeders",
    direction="desc",
    quantity=25
)
```

### ShareWoodTorrent

Class representing a torrent on ShareWood.tv.

Methods:
- `download(download_path=".")`: Download the torrent file to the specified path
- `delete()`: Delete the downloaded torrent file

## Error Handling

The library includes robust error handling:

```python
try:
    automator.connect()
    results = automator.search(criteria)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    automator.disconnect()
```

## License

[MIT License](LICENSE)

## Disclaimer

This tool is meant for educational purposes only. Please respect the terms of service of ShareWood.tv and copyright laws.