#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Dict, List, Optional

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

    def __init__(self, headless: Optional[bool] = True) -> None:
        """
        Initialize a new ShareWood.tv automator

        Args:
            headless: Run browser in headless mode
        """

        # Load environment variables
        self.env = self._load_env()
        
        # Create selenium driver instance
        self.browser = self._init_driver(
            headless, 
            timeout=self.env["BROWSER_TIMEOUT"]
        )
        # ShareWood logging
        self.logging = ShareWoodLogging(
            browser=self.browser, 
            home_url=self.env["SHAREWOOD_URL"],
            login_url=self.env["SHAREWOOD_LOGIN_URL"], 
            logout_url=self.env["SHAREWOOD_LOGOUT_URL"], 
            timeout=self.env["BROWSER_WAIT_TIMEOUT"]
        )
        # ShareWood search
        self.searcher = ShareWoodSearch(
            browser=self.browser, 
            search_url=self.env["SHAREWOOD_TORRENTS_URL"], 
            timeout=self.env["BROWSER_WAIT_TIMEOUT"]
        )
        # ShareWood torrents scraper
        self.scraper = ShareWoodTorrentScraper(browser=self.browser)
    
    def __del__(self) -> None:
        """
        Cleanup ShareWood.tv automator
        """

        # Close browser window
        self.browser.quit()
    
    def _load_env(self) -> Dict[str, str]:
        """
        Load environment variables from .env file
        """

        # Load environment variables from .env file
        load_dotenv()

        # Return environment variables as dictionary
        env_vars = {
            "SHAREWOOD_URL": os.getenv("SHAREWOOD_URL"),
            "SHAREWOOD_LOGIN_URL": os.getenv("SHAREWOOD_LOGIN_URL"),
            "SHAREWOOD_LOGOUT_URL": os.getenv("SHAREWOOD_LOGOUT_URL"),
            "SHAREWOOD_TORRENTS_URL": os.getenv("SHAREWOOD_TORRENTS_URL"),
            "BROWSER_TIMEOUT": int(os.getenv("BROWSER_TIMEOUT", "10")),
            "BROWSER_WAIT_TIMEOUT": int(os.getenv("BROWSER_WAIT_TIMEOUT", "10")),
            "PSEUDO": os.getenv("PSEUDO"),
            "PASSWORD": os.getenv("PASSWORD"),
        }
        
        # Check if all required environment variables are set
        for key, value in env_vars.items():
            if value is None:
                raise ValueError(f"Missing environment variable: {key}")
        return env_vars
    
    def _init_driver(self, headless: bool, timeout: int) -> WebDriver:
        """ 
        Initialize Chrome WebDriver with security optimizations
        Install Chrome WebDriver if not found

        Args:
            headless: Run browser in headless mode
            timeout: Timeout for WebDriverWait
        Returns:
            WebDriver: Chrome WebDriver instance
        Raises:
            Exception: If Chrome WebDriver cannot be installed
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
        # Set default timeout for WebDriver
        driver.implicitly_wait(timeout)
        # Set default page load timeout for WebDriver
        driver.set_page_load_timeout(timeout)
        # Set default script timeout for WebDriver
        driver.set_script_timeout(timeout)
        
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
    
    def search(self, search_criteria: ShareWoodSearchCriteria) -> List[ShareWoodTorrent]:
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
