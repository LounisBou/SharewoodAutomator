#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import MagicMock, patch

import pytest  # noqa: F401

from sharewoodautomator import ShareWoodAutomator, ShareWoodSearchCriteria


class TestShareWoodAutomator:
    """Tests for the ShareWoodAutomator class"""

    @patch('sharewoodautomator.sharewoodautomator.Chrome')
    @patch('sharewoodautomator.sharewoodautomator.load_dotenv')
    def test_init(self, mock_load_dotenv, mock_chrome, mock_env):
        """Test that automator initializes correctly"""
        # Setup
        mock_chrome.return_value = MagicMock()
        
        with patch.dict(os.environ, mock_env):
            # Execute
            automator = ShareWoodAutomator(headless=True)
            
            # Verify
            assert automator.browser is not None
            assert mock_chrome.called
            assert mock_load_dotenv.called
            assert automator.logging is not None
            assert automator.searcher is not None
            assert automator.scraper is not None
            assert automator.env["SHAREWOOD_URL"] == mock_env["SHAREWOOD_URL"]
    
    @patch('sharewoodautomator.sharewoodautomator.Chrome')
    def test_init_driver_headless(self, mock_chrome, mock_env):
        """Test that driver is initialized with headless mode"""
        # Setup
        mock_browser = MagicMock()
        mock_chrome.return_value = mock_browser
        
        with patch.dict(os.environ, mock_env):
            # Execute
            ShareWoodAutomator(headless=True)
            
            # Verify
            assert mock_chrome.called
            # Check that headless argument was passed to Chrome options
            args = mock_chrome.call_args[1]['options'].arguments
            assert "--headless" in args
    
    @patch('sharewoodautomator.sharewoodautomator.Chrome')
    def test_init_driver_not_headless(self, mock_chrome, mock_env):
        """Test that driver is initialized without headless mode"""
        # Setup
        mock_browser = MagicMock()
        mock_chrome.return_value = mock_browser
        
        with patch.dict(os.environ, mock_env):
            # Execute
            ShareWoodAutomator(headless=False)
            
            # Verify
            assert mock_chrome.called
            # Check that headless argument was not passed to Chrome options
            args = mock_chrome.call_args[1]['options'].arguments
            assert "--headless" not in args
    
    @patch('sharewoodautomator.sharewoodautomator.Chrome')
    def test_connect(self, mock_chrome, mock_env):
        """Test connect method"""
        # Setup
        mock_browser = MagicMock()
        mock_chrome.return_value = mock_browser
        
        with patch.dict(os.environ, mock_env):
            # Create automator with mocked components
            automator = ShareWoodAutomator(headless=True)
            automator.logging = MagicMock()
            
            # Execute
            automator.connect()
            
            # Verify
            automator.logging.connect.assert_called_once_with(
                mock_env["PSEUDO"], mock_env["PASSWORD"]
            )
    
    @patch('sharewoodautomator.sharewoodautomator.Chrome')
    def test_disconnect(self, mock_chrome, mock_env):
        """Test disconnect method"""
        # Setup
        mock_browser = MagicMock()
        mock_chrome.return_value = mock_browser
        
        with patch.dict(os.environ, mock_env):
            # Create automator with mocked components
            automator = ShareWoodAutomator(headless=True)
            automator.logging = MagicMock()
            
            # Execute
            automator.disconnect()
            
            # Verify
            automator.logging.disconnect.assert_called_once()
    
    @patch('sharewoodautomator.sharewoodautomator.Chrome')
    def test_search(self, mock_chrome, mock_env):
        """Test search method"""
        # Setup
        mock_browser = MagicMock()
        mock_chrome.return_value = mock_browser
        
        with patch.dict(os.environ, mock_env):
            # Create automator with mocked components
            automator = ShareWoodAutomator(headless=True)
            automator.searcher = MagicMock()
            
            # Create search criteria
            search_criteria = ShareWoodSearchCriteria(query="test")
            
            # Execute
            automator.search(search_criteria)
            
            # Verify
            automator.searcher.search.assert_called_once_with(search_criteria)
    
    @patch('sharewoodautomator.sharewoodautomator.Chrome')
    def test_download(self, mock_chrome, mock_env):
        """Test download method"""
        # Setup
        mock_browser = MagicMock()
        mock_chrome.return_value = mock_browser
        
        with patch.dict(os.environ, mock_env):
            # Create automator with mocked components
            automator = ShareWoodAutomator(headless=True)
            automator.scraper = MagicMock()
            
            # Mock the ShareWoodTorrent class
            with patch('sharewoodautomator.sharewoodautomator.ShareWoodTorrent') as mock_torrent:
                mock_torrent.download_link = "https://example.com/test.torrent"
                
                # Execute
                automator.download("https://www.sharewood.tv/torrents/123")
                
                # Verify
                automator.scraper.scrape.assert_called_once_with(mock_torrent)
                mock_torrent.download.assert_called_once()
