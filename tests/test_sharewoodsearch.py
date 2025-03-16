#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import MagicMock, patch
from sharewoodautomator import ShareWoodSearch, ShareWoodSearchCriteria

class TestShareWoodSearch:
    """Tests for the ShareWoodSearch class"""
    
    def test_init(self, mock_chrome_driver):
        """Test search initializes correctly"""
        # Setup
        search_url = "https://www.sharewood.tv/torrents"
        
        # Execute
        searcher = ShareWoodSearch(mock_chrome_driver, search_url)
        
        # Verify
        assert searcher.browser == mock_chrome_driver
        assert searcher.search_url == search_url
        assert searcher.ignore_parsing_errors is False
    
    def test_fill_search_form_from_criteria(self, mock_chrome_driver):
        """Test filling search form from criteria"""
        # Setup
        search_url = "https://www.sharewood.tv/torrents"
        
        # Create a mock form element
        mock_form = MagicMock()
        mock_form.is_displayed.return_value = True
        
        # Create mock elements for inputs
        mock_input = MagicMock()
        mock_form.find_element.return_value = mock_input
        
        with patch('sharewoodautomator.sharewoodsearch.WebDriverWait') as mock_wait:
            with patch('sharewoodautomator.sharewoodsearch.EC') as mock_ec:
                # Set up mock WebDriverWait to return our mock form
                mock_wait.return_value.until.return_value = mock_form
                
                # Initialize search
                searcher = ShareWoodSearch(mock_chrome_driver, search_url)
                
                # Create search criteria
                criteria = ShareWoodSearchCriteria(
                    query="test query",
                    description="test description",
                    uploader="test uploader",
                    tags="test,tags",
                    categories={"Vidéos": True, "Audios": False},
                    subcategories={"Application Linux": True},
                    languages={"Français": True, "Anglais": True}
                )
                
                # Execute
                searcher._fill_search_form_from_criteria(criteria)
                
                # Verify
                assert mock_chrome_driver.get.called_with(search_url)
                
                # Check that WebDriverWait was called
                mock_wait.assert_called_with(mock_chrome_driver, 10)
                
                # Check that find_element was called for inputs
                assert mock_form.find_element.called
                
                # Check that send_keys was called for inputs
                assert mock_input.send_keys.called
    
    def test_apply_filters_from_criteria(self, mock_chrome_driver):
        """Test applying filters from criteria"""
        # Setup
        search_url = "https://www.sharewood.tv/torrents"
        
        # Create a mock form element
        mock_form = MagicMock()
        
        # Create mock select inputs
        mock_select = MagicMock()
        mock_form.find_element.return_value = mock_select
        
        with patch('sharewoodautomator.sharewoodsearch.WebDriverWait') as mock_wait:
            with patch('sharewoodautomator.sharewoodsearch.EC') as mock_ec:
                # Set up mock WebDriverWait to return our mock form
                mock_wait.return_value.until.return_value = mock_form
                
                # Initialize search
                searcher = ShareWoodSearch(mock_chrome_driver, search_url)
                
                # Create search criteria with sorting, direction, and quantity
                criteria = ShareWoodSearchCriteria(
                    sorting="seeders",
                    direction="desc",
                    quantity=50
                )
                
                # Execute
                searcher._apply_filters_from_criteria(criteria)
                
                # Verify
                # Check that WebDriverWait was called
                mock_wait.assert_called_with(mock_chrome_driver, 10)
                
                # Check that find_element was called for select inputs
                assert mock_form.find_element.called
    
    def test_parse_search_result(self, mock_chrome_driver):
        """Test parsing search results"""
        # Setup
        search_url = "https://www.sharewood.tv/torrents"
        
        # Create sample HTML with two torrents
        html_result = """
        <div class="row  table-responsive-line">
            <div class="col-md-8 col-titre">
                <div class="type-table"></div>
                <div class="titre-table">
                    <a name="torrent" href="/torrents/123">Test Torrent 1</a>
                </div>
            </div>
            <div class="col-md-2 col-detail">
                <div class="row">
                    <div class="col-xs-4"><span class="age">2 days</span></div>
                    <div class="col-xs-4"><span class="size">1.5 GB</span></div>
                    <div class="col-xs-4"><span class="comments">5</span></div>
                </div>
            </div>
            <div class="col-md-2 col-detail">
                <div class="row">
                    <div class="col-xs-4 col-padding"><span class="seeders">10</span></div>
                    <div class="col-xs-4 col-padding"><span class="leechers">5</span></div>
                    <div class="col-xs-4 col-padding"><span class="downloads">100</span></div>
                </div>
            </div>
        </div>
        <div class="row  table-responsive-line">
            <div class="col-md-8 col-titre">
                <div class="type-table"></div>
                <div class="titre-table">
                    <a name="torrent" href="/torrents/456">Test Torrent 2</a>
                </div>
            </div>
            <div class="col-md-2 col-detail">
                <div class="row">
                    <div class="col-xs-4"><span class="age">1 day</span></div>
                    <div class="col-xs-4"><span class="size">2.3 GB</span></div>
                    <div class="col-xs-4"><span class="comments">2</span></div>
                </div>
            </div>
            <div class="col-md-2 col-detail">
                <div class="row">
                    <div class="col-xs-4 col-padding"><span class="seeders">20</span></div>
                    <div class="col-xs-4 col-padding"><span class="leechers">8</span></div>
                    <div class="col-xs-4 col-padding"><span class="downloads">150</span></div>
                </div>
            </div>
        </div>
        """
        
        # Mock the BeautifulSoup
        with patch('sharewoodautomator.sharewoodsearch.BeautifulSoup') as mock_bs:
            # Create mock BeautifulSoup object
            mock_soup = MagicMock()
            mock_bs.return_value = mock_soup
            
            # Create mock torrents for find_all
            mock_soup.find_all.return_value = []
            
            # Initialize search
            searcher = ShareWoodSearch(mock_chrome_driver, search_url)
            
            # Execute
            results = searcher._parse_search_result(html_result)
            
            # Verify
            assert mock_bs.called
            assert mock_soup.find_all.called
    
    def test_search(self, mock_chrome_driver):
        """Test search method end-to-end"""
        # Setup
        search_url = "https://www.sharewood.tv/torrents"
        
        # Mock the search form and results
        mock_form = MagicMock()
        mock_results = MagicMock()
        mock_results.get_attribute.return_value = "<html>Result</html>"
        
        with patch.object(ShareWoodSearch, '_fill_search_form_from_criteria') as mock_fill:
            with patch.object(ShareWoodSearch, '_apply_filters_from_criteria') as mock_apply:
                with patch('sharewoodautomator.sharewoodsearch.WebDriverWait') as mock_wait:
                    with patch('sharewoodautomator.sharewoodsearch.EC') as mock_ec:
                        # Set up mock WebDriverWait to return our mock results
                        mock_wait.return_value.until.return_value = mock_results
                        
                        # Initialize search
                        searcher = ShareWoodSearch(mock_chrome_driver, search_url)
                        
                        # Create search criteria
                        criteria = ShareWoodSearchCriteria(query="test")
                        
                        # Execute
                        result = searcher.search(criteria)
                        
                        # Verify
                        mock_fill.assert_called_once_with(criteria)
                        mock_apply.assert_called_once_with(criteria)
                        mock_wait.assert_called_with(mock_chrome_driver, 10)
                        assert result == "<html>Result</html>"