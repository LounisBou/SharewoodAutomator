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
