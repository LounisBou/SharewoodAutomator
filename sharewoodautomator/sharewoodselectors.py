#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CSS selectors for ShareWood.tv scraping.

This module centralizes all CSS selectors used for scraping ShareWood.tv,
making it easier to update them when the website structure changes.
"""

# Login page selectors
LOGIN_SELECTORS = {
    "username_input": "input[name='username']",
    "password_input": "input[name='password']",
    "login_button": "#login-button",
}

# Search page selectors
SEARCH_SELECTORS = {
    "search_form": "//form[@action='TorrentController@torrents']",
    "search_results": "#result",
    "torrent_rows": "div.row.table-responsive-line",
    "torrent_link": "a[name='torrent']",
    "torrent_title": "a[name='torrent']",
    "torrent_age": "span.age",
    "torrent_size": "span.size",
    "torrent_comments": "span.comments",
    "torrent_seeders": "span.seeders",
    "torrent_leechers": "span.leechers",
    "torrent_downloads": "span.downloads",
}

# Torrent page selectors
TORRENT_SELECTORS = {
    "discounts": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span > i",
    "fastline_credit_url": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(2) > a",
    "uploader_profile": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(2) > a",
    "age": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)",
    "size": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(5) > td:nth-child(2)",
    "ratio": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(6) > td:nth-child(2)",
    "category": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(7) > td:nth-child(2)",
    "subcategory": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(8) > td:nth-child(2)",
    "tags": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(9) > td:nth-child(2)",
    "languages": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(10) > td:nth-child(2)",
    "resolution": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(11) > td:nth-child(2)",
    "three_d_flag": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(12) > td:nth-child(2)",
    "hash": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(13) > td:nth-child(2)",
    "seeders": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(14) > td:nth-child(2) > span.badge-extra.text-green",
    "leechers": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(15) > td:nth-child(2) > span.badge-extra.text-red",
    "completed": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(16) > td:nth-child(2) > span.badge-extra.text-info",
}
