#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CSS selectors for ShareWood.tv scraping.

This module centralizes all CSS selectors used for scraping ShareWood.tv,
making it easier to update them when the website structure changes.
"""

# Page controls selectors
PAGE_CONTROLS_SELECTORS = {
    "home": "#frame > div > div.messages",
    "torrents": "div#result",
    "torrents_search": "form[@action='TorrentController@torrents']",
    "torrent" : "table > div.prez-body",
}

# Login page selectors
LOGIN_SELECTORS = {
    "username_input": "input[name='username']",
    "password_input": "input[name='password']",
    "login_button": "#login-button",
}

# Search criteria selectors
SEARCH_CRITERIA_SELECTORS = {
    "query": "input[name='research']",
    "description": "input[name='description']",
    "uploader": "input[name='uploader']",
    "tags": "input[name='tags']",
    "categories": ".category.category-parent",
    "subcategories": ".subcategory",
    "languages": ".language",
    "types": ".type",
    "specials": {
        "3D": "#stream",
        "hors-regles": "#sd",
        "freeleech": "#freeleech",
        "double-upload": "#double-upload",
        "pack": "#internal",
        "uncompleted": "#downloaded",

    },
    "sorting": ".sort",
    "direction": ".direction",
    "quantity": ".qty",
}

TORRENT_SELECTORS = {
    "title": "#app > div.row > div > div:nth-child(1) > h1",
    "description": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2)",
    "hash": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(13) > td:nth-child(2)",
    "uploader": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(1) > a",
    "uploader_profile": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(1) > a['href']",
    "size": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(5) > td:nth-child(2)",
    "age": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)",
    "ratio": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(6) > td:nth-child(2)",
    "tags": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(9) > td:nth-child(2)",
    "resolution": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(11) > td:nth-child(2)",
    "seeders": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(14) > td:nth-child(2) > span.badge-extra.text-green",
    "leechers": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(15) > td:nth-child(2) > span.badge-extra.text-red",
    "discounts": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span > i",
    "fastline_credit_url": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(2) > a['href']",
    "category": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(7) > td:nth-child(2)",
    "subcategory": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(8) > td:nth-child(2)",
    "languages": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(10) > td:nth-child(2)",
    "three_d_flag": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(12) > td:nth-child(2)",
    "completed": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(16) > td:nth-child(2) > span.badge-extra.text-info",
    "nb_comments": "#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(2)",
    "download_link": "#app > div.torrent.box.container-fluid > div > div > span > a:nth-child(1)",
}
