#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from dotenv import load_dotenv
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from .sharewoodlogging import ShareWoodLogging
from .sharewoodsearch import ShareWoodSearch
from .sharewoodsearchcriteria import ShareWoodSearchCriteria
from .sharewoodtorrent import ShareWoodTorrent
from .sharewoodtorrentscraper import ShareWoodTorrentScraper


class ShareWoodAutomator:
    """ Automates interactions with ShareWood.tv """

    def __init__(self, headless: bool = True) -> None:
        """
        Initialize a new ShareWood.tv automator

        Args:
            headless: Run browser in headless mode
        """

        # Create selenium driver instance
        self.browser = self._init_driver(headless)
        # Load environment variables
        self.env = self._load_env()
        # ShareWood logging
        self.logging = ShareWoodLogging(self.browser, self.env["SHAREWOOD_LOGIN"], self.env["SHAREWOOD_LOGOUT"])
        # ShareWood search
        self.searcher = ShareWoodSearch(self.browser, self.env["SHAREWOOD_TORRENTS"])
        # ShareWood torrents scraper
        self.scraper = ShareWoodTorrentScraper(self.browser)
    
    def __del__(self) -> None:
        """
        Cleanup ShareWood.tv automator
        """

        # Close browser window
        self.browser.quit()
    
    def _load_env(self) -> dict:
        """
        Load environment variables from .env file
        """

        # Load environment variables from .env file
        load_dotenv()

        # Return environment variables as dictionary
        return {
            "SHAREWOOD_URL": os.getenv("SHAREWOOD_URL"),
            "SHAREWOOD_LOGIN": os.getenv("SHAREWOOD_LOGIN"),
            "SHAREWOOD_LOGOUT": os.getenv("SHAREWOOD_LOGOUT"),
            "SHAREWOOD_TORRENTS": os.getenv("SHAREWOOD_TORRENTS"),
            "PSEUDO": os.getenv("PSEUDO"),
            "PASSWORD": os.getenv("PASSWORD"),
        }
    
    def _init_driver(self, headless: bool) -> WebDriver:
        """ 
        Initialize Chrome WebDriver with security optimizations
        Install Chrome WebDriver if not found

        Args:
            headless: Run browser in headless mode
        """

        # Configure Chrome WebDriver with security optimizations
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless") # Run browser in headless mode
        options.add_argument("--disable-blink-features=AutomationControlled") # Disable automation controlled flag
        options.add_argument("--no-sandbox") # Disable sandbox mode
        options.add_argument("--disable-dev-shm-usage") # Disable dev-shm usage

        # Initialize Chrome WebDriver
        driver = Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(30)
        
        return driver

    def connect(self) -> None:
        """
        Connect to ShareWood.tv
        """

        self.logging.connect(
            self.env["PSEUDO"], self.env["PASSWORD"]
        )

    def disconnect(self) -> None:
        """
        Disconnect from ShareWood.tv
        """
        
        self.logging.disconnect()
    
    def search(self, search_criteria: ShareWoodSearchCriteria) -> list[ShareWoodTorrent]:
        """
        Search for a torrent on ShareWood.tv
        
        Args:
            search_criteria: Search criteria
            
        Returns:
            list[ShareWoodTorrent]: List of torrents found
        """

        return self.searcher.search(search_criteria)

    def download(self, url: str) -> None:
        """
        Download a torrent from ShareWood.tv
        
        Args:
            url: Torrent page URL
        """
        
        # Create ShareWoodTorrent instance
        ShareWoodTorrent(url=url)

        # Scrape torrent information
        self.scraper.scrape(ShareWoodTorrent)

        # Download torrent
        self.browser.get(ShareWoodTorrent.download_link)
