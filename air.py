﻿"""Generate an index file from HTML data that is pulled as a source of truth.

Usage:
    python air.py

Outline:
    TODO: Add Outline

References:
    TODO: Add References
"""

# import sys
import requests
from bs4 import BeautifulSoup


def main():
    """Use the user's credentials to pull HTML data containing their top songs.

    Generate an index file from this data that is pulled as a source of truth.
    This particular example generates a .c file titled current_top_50_songs.c.

    Raises:
        Exception: If the URL containing the list of songs cannot be reached.
    """

    # Headers taken from Chrome's inspect element of favoritemusic.guru.
    headers = {
        'authority': 'favoritemusic.guru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    }

    # Cookies taken from Chrome's inspect element of favoritemusic.guru.
    cookies = {
        'spotifyTopsId': 'fdf56acc-b7d0-4cf2-8753-66bfc9f1d7a0',
    }

    # NOTE: Website could be changed in the future.
    url = 'https://favoritemusic.guru/'

    # Authenticate the user's Spotify credentials to allow the script to work.
    website_response = requests.get(url, headers=headers, cookies=cookies)
    if website_response.status_code != 200:
        sys.exit('Failed to reach ' + url + "! Script aborted.")

    # Strip irrelevant data so that the list of songs can be sent to Spotify.
    extracted_html = BeautifulSoup(website_response.content, 'html.parser')
    list_of_ols = extracted_html.find_all('ol')
    past_month_data = 3     # NOTE: Could utilise other data in the future.
    list_of_songs = list_of_ols[past_month_data].contents
    list_of_songs = [song.text.replace('—', '') for song in list_of_songs]
    list_of_songs = [song.replace('\xa0', '') for song in list_of_songs]


# Only runs if called directly.
if __name__ == '__main__':
    main()