#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import fields
from typing import List, Optional

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .sharewoodsearchcriteria import ShareWoodSearchCriteria
from .sharewoodtorrent import ShareWoodTorrent


class ShareWoodSearch():
    """Searches for torrents on ShareWood.tv"""
    
    def __init__(self, browser: WebDriver, search_url: str, ignore_parsing_errors: Optional[bool] = False):
        """
        Initialize a new session with ShareWood.tv
        
        Args:
            browser: Selenium WebDriver instance
            search_url: URL of ShareWood.tv search page
            ignore_parsing_errors: Ignore parsing errors (default: False)
        """
        
        # Instance of Selenium WebDriver
        self.browser = browser
        # URL of ShareWood.tv search page
        self.search_url = search_url
        # Ignore parsing errors
        self.ignore_parsing_errors = ignore_parsing_errors

    def fill_search_form_from_criteria(self, search_criteria: ShareWoodSearchCriteria) -> None:
        """
        Fill search form from search criteria
        
        Args:
            search_criteria: Search criteria for ShareWood.tv
        """
        
        # Navigate to ShareWood.tv
        self.browser.get(self.search_url)

        # Wait for form to load (form with action="TorrentController@torrents")
        search_form = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form[@action='TorrentController@torrents']"))
        )

        # Check if search box is visible
        if search_form.is_displayed():

            # Check if query is provided
            if search_criteria.query:
                # Find search input and enter search query
                search_form.find_element(By.NAME, search_criteria.metadata["name"]).send_keys(search_criteria.query)
            
            # Check if description is provided
            if search_criteria.description:
                # Find description input and enter description
                search_form.find_element(By.NAME, search_criteria.metadata["name"]).send_keys(search_criteria.description)

            # Check if uploader is provided
            if search_criteria.uploader:
                # Find uploader input and enter uploader
                search_form.find_element(By.NAME, search_criteria.metadata["name"]).send_keys(search_criteria.uploader)

            # Check if tags are provided
            if search_criteria.tags:
                # Find tags input and enter tags
                search_form.find_element(By.NAME, search_criteria.metadata["name"]).send_keys(search_criteria.tags)

            # Check if categories are provided
            if search_criteria.categories:
                # Iterate over categories
                for category, checked in search_criteria.categories.items():
                    # Check if category is checked
                    if checked:
                        # Find category checkbox and check it
                        search_form.find_element(By.NAME, category).click()

            # Check if subcategories are provided
            if search_criteria.subcategories:
                # Iterate over subcategories
                for subcategory, checked in search_criteria.subcategories.items():
                    # Check if subcategory is checked
                    if checked:
                        # Find subcategory checkbox and check it
                        search_form.find_element(By.NAME, subcategory).click()

            # Check if languages are provided
            if search_criteria.languages:
                # Iterate over languages
                for language, checked in search_criteria.languages.items():
                    # Check if language is checked
                    if checked:
                        # Find language checkbox and check it
                        search_form.find_element(By.NAME, language).click()

    def apply_filters_from_criteria(self, search_criteria: ShareWoodSearchCriteria) -> str:
        """
        Apply filters from search criteria

        Args:
            search_criteria: Search criteria for ShareWood.tv
        """

        # Wait for form to load (form with action="TorrentController@torrents")
        search_form = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form[@action='TorrentController@torrents']"))
        )

        # Check if sorting is provided
        if search_criteria.sorting:
            # Find sorting select element by name
            sorting_select_input = search_form.find_element(By.NAME, fields(search_criteria.sorting)[0].metadata['name'])
            # Select sorting option by value
            sorting_select_input.select_by_value(search_criteria.sorting)

        # Check if direction is provided
        if search_criteria.direction:
            # Find direction select element by name
            direction_select_input = search_form.find_element(By.NAME, fields(search_criteria.direction)[0].metadata['name'])
            # Select direction option by value
            direction_select_input.select_by_value(search_criteria.direction)

        # Check if quantity is provided
        if search_criteria.quantity:
            # Find quantity select element by name
            quantity_select_input = search_form.find_element(By.NAME, fields(search_criteria.quantity)[0].metadata['name'])
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
        search_results = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )

        # Get HTML of search results (div with id="result")
        result = search_results.get_attribute("innerHTML")

        # Return HTML of search results
        return result
