#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from .sharewoodtorrent import ShareWoodTorrent


class ShareWoodTorrentScraper:
    """ Scrapes information of torrents from ShareWood.tv """

    def __init__(self, browser):
        """ Initializes ShareWoodTorrentScraper """

        self.browser = browser

    def _get_discounts(self, soup: BeautifulSoup) -> str:
        """ 
        Gets discounts value of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Discounts value
        """

        discounts = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span > i")

        return discounts.text if discounts else None
    
    def _get_fastline_credit_url(self, soup: BeautifulSoup) -> str:
        """ 
        Gets use fastline credit url of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Use fastline credit url
        """

        use_fastline_credit = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(2) > a['href']")

        return use_fastline_credit.text if use_fastline_credit else None
    
    def _get_uploader_profile(self, soup: BeautifulSoup) -> str:
        """ 
        Gets URL of the uploader profile of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: URL of the uploader profile
        """

        uploader_profile = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(2) > a['href']")

        return uploader_profile.text if uploader_profile else None
    
    def _get_age(self, soup: BeautifulSoup) -> str:
        """ 
        Gets age of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Age of the torrent
        """

        age = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)")

        return age.text if age else None
    
    def _get_size(self, soup: BeautifulSoup) -> str:
        """ 
        Gets size of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Size of the torrent
        """

        size = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(5) > td:nth-child(2)")

        return size.text if size else None
    
    def _get_ratio(self, soup: BeautifulSoup) -> str:
        """ 
        Gets estimated ratio of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Estimated ratio of the torrent
        """

        ratio = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(6) > td:nth-child(2)")

        return ratio.text if ratio else None
    
    def _get_category(self, soup: BeautifulSoup) -> str:
        """ 
        Gets category of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Category of the torrent
        """

        category = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(7) > td:nth-child(2)")

        return category.text if category else None
    
    def _get_subcategory(self, soup: BeautifulSoup) -> str:
        """ 
        Gets subcategory of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Subcategory of the torrent
        """

        subcategory = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(8) > td:nth-child(2)")

        return subcategory.text if subcategory else None
    
    def _get_tags(self, soup: BeautifulSoup) -> str:
        """ 
        Gets tags of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Tags of the torrent
        """

        tags = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(9) > td:nth-child(2)")

        return tags.text if tags else None
    
    def _get_languages(self, soup: BeautifulSoup) -> str:
        """ 
        Gets languages of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Languages of the torrent
        """

        languages = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(10) > td:nth-child(2)")

        return languages.text if languages else None
    
    def _get_resolution(self, soup: BeautifulSoup) -> str:
        """ 
        Gets resolution of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Resolution of the torrent
        """

        resolution = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(11) > td:nth-child(2)")

        return resolution.text if resolution else None
    
    def _get_three_d_flag(self, soup: BeautifulSoup) -> str:
        """ 
        Gets 3D flag of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: 3D flag of the torrent
        """

        three_d_flag = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(12) > td:nth-child(2)")

        return three_d_flag.text if three_d_flag else None
    
    def _get_hash(self, soup: BeautifulSoup) -> str:
        """ 
        Gets hash of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Hash of the torrent
        """

        torrent_hash = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(13) > td:nth-child(2)")

        return torrent_hash.text if torrent_hash else None
    
    def _get_seeders(self, soup: BeautifulSoup) -> str:
        """ 
        Gets seeders of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Seeders of the torrent
        """

        seeders = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(14) > td:nth-child(2) > span.badge-extra.text-green")

        return seeders.text if seeders else None
    
    def _get_leechers(self, soup: BeautifulSoup) -> str:
        """
        Gets leechers of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Leechers of the torrent
        """

        leechers = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(15) > td:nth-child(2) > span.badge-extra.text-red")

        return leechers.text if leechers else None
    
    def _get_completed(self, soup: BeautifulSoup) -> str:
        """ 
        Gets completed of a torrent
        
        Args:
            soup: BeautifulSoup instance of the torrent page
        
        Returns:
            str: Completed of the torrent
        """

        completed = soup.select_one("#app > div.row > div > div:nth-child(1) > table > tbody > tr:nth-child(16) > td:nth-child(2) > span.badge-extra.text-info")

        return completed.text if completed else None

    def scrape(self, torrent: ShareWoodTorrent) -> None:
        """ 
        Scrapes information of torrents from ShareWood.tv
        
        Args:
            torrent: ShareWoodTorrent to scrape information from
        """

        # Open torrent page
        self.browser.get(torrent.href)

        # Get page HTML content
        html = self.browser.page_source

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Scrape torrent information
        torrent.discounts = self._get_discounts(soup)
        torrent.fastline_credit_url = self._get_fastline_credit_url(soup)
        torrent.uploader_profile = self._get_uploader_profile(soup)
        torrent.age = self._get_age(soup)
        torrent.size = self._get_size(soup)
        torrent.ratio = self._get_ratio(soup)
        torrent.category = self._get_category(soup)
        torrent.subcategory = self._get_subcategory(soup)
        torrent.tags = self._get_tags(soup)
        torrent.languages = self._get_languages(soup)
        torrent.resolution = self._get_resolution(soup)
        torrent.three_d_flag = self._get_three_d_flag(soup)
        torrent.hash = self._get_hash(soup)
        torrent.seeders = self._get_seeders(soup)
        torrent.leechers = self._get_leechers(soup)
        torrent.completed = self._get_completed(soup)
