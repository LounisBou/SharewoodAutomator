#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .sharewoodselectors import TORRENT_SELECTORS
from .sharewoodtorrent import ShareWoodTorrent


class ShareWoodTorrentScraper:
    """ Scrapes information of torrents from ShareWood.tv """

    def __init__(self, browser, timeout: int) -> None:
        """
        Initializes ShareWoodTorrentScraper

        Args:
            browser: selenium WebDriver instance
            timeout: Timeout for WebDriverWait
        """

        self.browser = browser
        self.timeout = timeout
        self.html = None
        self.soup = None

    def _get_attribut_by_css_selector(self, attribut_name: str) -> str:
        """
        Gets title of a torrent

        Args:
            attribut_name: ShareWoodTorrent attribute name
        Returns:
            str: Title of the torrent
        """

        # Check if soup is None
        if self.soup is None:
            raise ValueError("HTML content not loaded. Please call scrape() first.")

        # Check if css selector exists
        if attribut_name not in TORRENT_SELECTORS:
            raise ValueError(f"Invalid attribute name: {attribut_name}")

        try:
            # Get the title using the CSS selector
            attribut = self.soup.select_one(TORRENT_SELECTORS[attribut_name])
        except Exception as e:
            # Handle any exceptions that occur during selection
            raise ValueError(f"Error while selecting {attribut_name}: {e}") from e

        # Check if the element was found
        if not attribut:
            raise ValueError(f"Element not found for {attribut_name}")

        # Return the text content of the element
        # and strip any leading/trailing whitespace
        # and remove any HTML tags
        return attribut.get_text(strip=True)

    def scrape(self, torrent: ShareWoodTorrent) -> None:
        """
        Scrapes information of torrents from ShareWood.tv

        Args:
            torrent: ShareWoodTorrent to scrape information from
        """

        # Open torrent page
        self.browser.get(torrent.href)

        # Wait for the page to load
        WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, TORRENT_SELECTORS["title"]))
        )

        # Get page HTML content
        self.html = self.browser.page_source

        # Parse HTML content using BeautifulSoup
        self.soup = BeautifulSoup(self.html, "html.parser")

        # Scrape torrent information
        torrent.title = self._get_attribut_by_css_selector("title")
        torrent.description = self._get_attribut_by_css_selector("description")
        torrent.hash = self._get_attribut_by_css_selector("hash")
        torrent.uploader = self._get_attribut_by_css_selector("uploader")
        torrent.uploader_profile = self._get_attribut_by_css_selector("uploader_profile")
        torrent.size = self._get_attribut_by_css_selector("size")
        torrent.age = self._get_attribut_by_css_selector("age")
        torrent.ratio = self._get_attribut_by_css_selector("ratio")
        torrent.tags = self._get_attribut_by_css_selector("tags")
        torrent.resolution = self._get_attribut_by_css_selector("resolution")
        torrent.seeders = self._get_attribut_by_css_selector("seeders")
        torrent.leechers = self._get_attribut_by_css_selector("leechers")
        torrent.discounts = self._get_attribut_by_css_selector("discounts")
        torrent.fastline_credit_url = self._get_attribut_by_css_selector("fastline_credit_url")
        torrent.category = self._get_attribut_by_css_selector("category")
        torrent.subcategory = self._get_attribut_by_css_selector("subcategory")
        torrent.languages = self._get_attribut_by_css_selector("languages")
        torrent.three_d_flag = self._get_attribut_by_css_selector("three_d_flag")
        torrent.completed = self._get_attribut_by_css_selector("completed")
        torrent.nb_comments = self._get_attribut_by_css_selector("nb_comments")
        torrent.download_link = self._get_attribut_by_css_selector("download_link")
