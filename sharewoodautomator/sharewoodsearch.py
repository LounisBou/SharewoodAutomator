#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional

from bs4 import BeautifulSoup, Tag
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .sharewoodsearchcriteria import ShareWoodSearchCriteria
from .sharewoodselectors import PAGE_CONTROLS_SELECTORS, TORRENT_RESULTS_SELECTORS
from .sharewoodtorrent import ShareWoodTorrent


class ShareWoodSearch():
    """Searches for torrents on ShareWood.tv"""

    def __init__(self, browser: WebDriver, search_url: str, timeout: int, ignore_parsing_errors: Optional[bool] = False) -> None:
        """
        Initialize a new session with ShareWood.tv

        Args:
            browser: Selenium WebDriver instance
            search_url: URL of ShareWood.tv search page
            timeout: Timeout for WebDriverWait
            ignore_parsing_errors: Ignore parsing errors (default: False)
        """

        # Instance of Selenium WebDriver
        self.browser = browser
        # URL of ShareWood.tv search page
        self.search_url = search_url
        # Ignore parsing errors
        self.ignore_parsing_errors = ignore_parsing_errors
        # Timeout for WebDriverWait
        self.timeout = timeout

    def fill_search_form_from_criteria(self, search_criteria: ShareWoodSearchCriteria) -> None:
        """
        Fill search form from search criteria

        Args:
            search_criteria: Search criteria for ShareWood.tv
        """

        # Navigate to ShareWood.tv torrent page
        self.browser.get(self.search_url)
        print(f"Navigating to ShareWood.tv torrent page : {self.search_url}")

        # Wait for page to load
        WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PAGE_CONTROLS_SELECTORS["torrents"]))
        )
        print(" - Torrent page is loaded")

        # Wait for form to load
        search_form = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PAGE_CONTROLS_SELECTORS["torrents_search"]))
        )

        # Check if search box is visible
        if search_form.is_displayed():

            print(" - Search form is loaded and displayed")

            # Check if query is provided
            if search_criteria.query:
                try:
                    # Find search input and enter search query
                    search_form.find_element(
                        by=By.CSS_SELECTOR,
                        value=search_criteria.get_css_selector("query")
                    ).send_keys(search_criteria.query)
                except NoSuchElementException as e:
                    raise ValueError("Search input not found") from e

            # Check if description is provided
            if search_criteria.description:
                try:
                    # Find description input and enter description
                    search_form.find_element(
                        by=By.CSS_SELECTOR,
                        value=search_criteria.get_css_selector("description")
                    ).send_keys(search_criteria.description)
                except NoSuchElementException as e:
                    raise ValueError("Description input not found") from e

            # Check if uploader is provided
            if search_criteria.uploader:
                try:
                    # Find uploader input and enter uploader
                    search_form.find_element(
                        by=By.CSS_SELECTOR,
                        value=search_criteria.get_css_selector("uploader")
                    ).send_keys(search_criteria.uploader)
                except NoSuchElementException as e:
                    raise ValueError("Uploader input not found") from e

            # Check if tags are provided
            if search_criteria.tags:
                try:
                    # Find tags input and enter tags
                    search_form.find_element(
                        by=By.CSS_SELECTOR,
                        value=search_criteria.get_css_selector("tags")
                    ).send_keys(search_criteria.tags)
                except NoSuchElementException as e:
                    raise ValueError("Tags input not found") from e

        else:
            raise ValueError("Search form is not loaded or not displayed")

    def apply_filters_from_criteria(self, search_criteria: ShareWoodSearchCriteria) -> str:
        """
        Apply filters from search criteria

        Args:
            search_criteria: Search criteria for ShareWood.tv
        """

        # Wait for form to load
        search_form = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PAGE_CONTROLS_SELECTORS["torrents_search"]))
        )

        # Check if sorting is provided
        if search_criteria.sorting:
            # Find sorting select element by name
            sorting_select_input = search_form.find_element(
                by=By.CSS_SELECTOR,
                value=search_criteria.get_css_selector("sorting")
            )
            # Select sorting option by value
            sorting_select_input.select_by_value(search_criteria.sorting)

        # Check if direction is provided
        if search_criteria.direction:
            # Find direction select element by name
            direction_select_input = search_form.find_element(
                by=By.CSS_SELECTOR,
                value=search_criteria.get_css_selector("direction")
            )
            # Select direction option by value
            direction_select_input.select_by_value(search_criteria.direction)

        # Check if quantity is provided
        if search_criteria.quantity:
            # Find quantity select element by name
            quantity_select_input = search_form.find_element(
                by=By.CSS_SELECTOR,
                value=search_criteria.get_css_selector("quantity")
            )
            # Select quantity option by value
            quantity_select_input.select_by_value(search_criteria.quantity)

    def parse_search_result(self, html_search_result: str) -> List[ShareWoodTorrent]:
        """
        Parse search results from ShareWood.tv using BeautifulSoup

        Args:
            html_search_result: HTML source of search results

        Returns:
            List of parsed search results as ShareWoodTorrent

        Raises:
            Exception: Failed to parse torrent
        """

        # Parse HTML source of search results
        soup: BeautifulSoup = BeautifulSoup(html_search_result, "html.parser")

        # Find all torrents
        torrent_elements: List[Tag] = soup.find_all("div", class_="row  table-responsive-line")

        # Initialize list of ShareWoodTorrent
        torrents: List[ShareWoodTorrent] = []

        # Iterate over a copy of torrents
        for torrent_element in list(torrent_elements):
            # Append parsed torrent to list of parsed torrents
            parsed_torrent_element = {
                "url": torrent_element.select_one(TORRENT_RESULTS_SELECTORS["url"]),
                "title": torrent_element.select_one(TORRENT_RESULTS_SELECTORS["title"]),
                "age": torrent_element.select_one(TORRENT_RESULTS_SELECTORS["age"]),
                "size": torrent_element.select_one(TORRENT_RESULTS_SELECTORS["size"]),
                "comments": torrent_element.select_one(TORRENT_RESULTS_SELECTORS["comments"]),
                "seeders": torrent_element.select_one(TORRENT_RESULTS_SELECTORS["seeders"]),
                "leechers": torrent_element.select_one(TORRENT_RESULTS_SELECTORS["leechers"]),
                "downloads": torrent_element.select_one(TORRENT_RESULTS_SELECTORS["downloads"])
            }

            # Create ShareWoodTorrent instance
            torrent = ShareWoodTorrent(
                url=parsed_torrent_element["url"].get("href") if parsed_torrent_element["url"] else None,
                title=parsed_torrent_element["title"].get_text(strip=True) if parsed_torrent_element["title"] else None,
                age=parsed_torrent_element["age"].get_text(strip=True) if parsed_torrent_element["age"] else None,
                size=parsed_torrent_element["size"] .get_text(strip=True) if parsed_torrent_element["size"] else None,
                nb_comments=parsed_torrent_element["comments"].get_text(strip=True) if parsed_torrent_element["comments"] else None,
                leechers=parsed_torrent_element["leechers"].get_text(strip=True) if parsed_torrent_element["leechers"] else None,
                completed=parsed_torrent_element["downloads"].get_text(strip=True) if parsed_torrent_element["downloads"] else None,
            )

            # Check if torrent parsed successfully
            if torrent.url is None and self.ignore_parsing_errors is False:
                raise ValueError("Failed to parse torrent")

            # Append torrent to list of torrents
            torrents.append(torrent)

        # Return list of ShareWoodTorrent
        return torrents

    def search(self, search_criteria: ShareWoodSearchCriteria) -> List[ShareWoodTorrent]:
        """
        Search for torrents on ShareWood.tv"

        Args:
            search_criteria: Search criteria for ShareWood.tv"

        Returns:
            List of parsed search results as dictionaries containing:
            - title: Title of torrent
            - href: Href to torrent
            - age: Age of torrent
            - size: Size of torrent
            - comments: Number of comments
            - seeders: Number of seeders
            - leechers: Number of leechers
            - downloads: Number of downloads
        """

        # Fill search form from search criteria
        self.fill_search_form_from_criteria(search_criteria)

        # Apply filters from search criteria
        self.apply_filters_from_criteria(search_criteria)

        # No need to submit form, search results are loaded dynamically
        # Wait for search results to load (div with id="result")
        search_results = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PAGE_CONTROLS_SELECTORS["torrents"]))
        )

        # Get HTML of search results (div with id="result")
        result = search_results.get_attribute("innerHTML")

        # Return HTML of search results
        return result
