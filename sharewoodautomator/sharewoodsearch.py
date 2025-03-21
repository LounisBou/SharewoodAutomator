#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .sharewoodsearchcriteria import ShareWoodSearchCriteria
from .sharewoodselectors import PAGE_CONTROLS_SELECTORS
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
                # Find search input and enter search query
                search_form.find_element(
                    by=By.NAME,
                    value=search_criteria.get_css_selector("query")
                ).send_keys(search_criteria.query)

            # Check if description is provided
            if search_criteria.description:
                # Find description input and enter description
                search_form.find_element(
                    by=By.CSS_SELECTOR,
                    value=search_criteria.get_css_selector("description")
                ).send_keys(search_criteria.description)

            # Check if uploader is provided
            if search_criteria.uploader:
                # Find uploader input and enter uploader
                search_form.find_element(
                    by=By.CSS_SELECTOR,
                    value=search_criteria.get_css_selector("uploader")
                ).send_keys(search_criteria.uploader)

            # Check if tags are provided
            if search_criteria.tags:
                # Find tags input and enter tags
                search_form.find_element(
                    by=By.CSS_SELECTOR,
                    value=search_criteria.get_css_selector("tags")
                ).send_keys(search_criteria.tags)

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
            sorting_select_input = search_form.find_element(By.CSS_SELECTOR, search_criteria.get_css_selector("sorting"))
            # Select sorting option by value
            sorting_select_input.select_by_value(search_criteria.sorting)

        # Check if direction is provided
        if search_criteria.direction:
            # Find direction select element by name
            direction_select_input = search_form.find_element(By.CSS_SELECTOR, search_criteria.get_css_selector("direction"))
            # Select direction option by value
            direction_select_input.select_by_value(search_criteria.direction)

        # Check if quantity is provided
        if search_criteria.quantity:
            # Find quantity select element by name
            quantity_select_input = search_form.find_element(By.CSS_SELECTOR, search_criteria.get_css_selector("quantity"))
            # Select quantity option by value
            quantity_select_input.select_by_value(search_criteria.quantity)

    def parse_search_result(self, html_search_result: str) -> List[ShareWoodTorrent]:
        """
        Parse search results from ShareWood.tv using BeautifulSoup

        # Find all torrents div with class="row  table-responsive-line"
        # Inside each div, find the following elements:
        # - div with class="col-md-8 col-titre"
        # - - div with class="type-table"
        # - - div with class="titre-table"
        # - - - a with name="torrent" containing title and href to torrent
        # - div with class="col-md-2 col-detail"
        # - - div with class="row"
        # - - - div with class="col-xs-4"
        # - - - - span containing age of torrent
        # - - - div with class="col-xs-4"
        # - - - - span containing size of torrent
        # - - - div with class="col-xs-4"
        # - - - - span containing number of comments
        # - div with class="col-md-2 col-detail"
        # - - div with class="row"
        # - - - div with class="col-xs-4 col-padding"
        # - - - - span containing number of seeders
        # - - - div with class="col-xs-4 col-padding"
        # - - - - span containing number of leechers
        # - - - div with class="col-xs-4 col-padding"
        # - - - - span containing number of downloads

        Args:
            html_search_result: HTML source of search results

        Returns:
            List of parsed search results as ShareWoodTorrent

        Raises:
            Exception: Failed to parse torrent
        """

        # Parse HTML source of search results
        soup = BeautifulSoup(html_search_result, "html.parser")

        # Find all torrents
        torrents = soup.find_all("div", class_="row  table-responsive-line")

        # Initialize list of ShareWoodTorrent
        torrents = []

        # Iterate over a copy of torrents
        for torrent in list(torrents):
            # Append parsed torrent to list of parsed torrents
            parsed_torrent = {
                "url": torrent.find("a", name="torrent")["href"] if torrent.find("a", name="torrent")
                else None,
                "title": torrent.find("a", name="torrent").text if torrent.find("a", name="torrent")
                else None,
                "age": torrent.find("span", class_="age").text if torrent.find("span", class_="age")
                else None,
                "size": torrent.find("span", class_="size").text if torrent.find("span", class_="size")
                else None,
                "comments": torrent.find("span", class_="comments").text if torrent.find("span", class_="comments")
                else None,
                "seeders": torrent.find("span", class_="seeders").text if torrent.find("span", class_="seeders")
                else None,
                "leechers": torrent.find("span", class_="leechers").text if torrent.find("span", class_="leechers")
                else None,
                "downloads": torrent.find("span", class_="downloads").text if torrent.find("span", class_="downloads")
                else None
            }

            # Create ShareWoodTorrent instance
            torrent = ShareWoodTorrent(
                url=parsed_torrent["url"],
                title=parsed_torrent["title"],
                age=parsed_torrent["age"],
                size=parsed_torrent["size"],
                nb_comments=parsed_torrent["comments"],
                seeders=parsed_torrent["seeders"],
                leechers=parsed_torrent["leechers"],
                completed=parsed_torrent["downloads"]
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
