#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import MagicMock, patch
from sharewoodautomator import ShareWoodLogging

class TestShareWoodLogging:
    """Tests for the ShareWoodLogging class"""
    
    def test_init(self, mock_chrome_driver):
        """Test that logging initializes correctly"""
        # Setup
        login_url = "https://www.sharewood.tv/login"
        logout_url = "https://www.sharewood.tv/logout"
        
        # Execute
        logging = ShareWoodLogging(mock_chrome_driver, login_url, logout_url)
        
        # Verify
        assert logging.browser == mock_chrome_driver
        assert logging.login_url == login_url
    
    def test_connect(self, mock_chrome_driver):
        """Test the connect method"""
        # Setup
        login_url = "https://www.sharewood.tv/login"
        logout_url = "https://www.sharewood.tv/logout"
        
        # Create mocks for WebDriverWait and expected_conditions
        mock_element = MagicMock()
        mock_element.send_keys = MagicMock()
        
        with patch('sharewoodautomator.sharewoodlogging.WebDriverWait') as mock_wait:
            with patch('sharewoodautomator.sharewoodlogging.EC') as mock_ec:
                # Set up mock WebDriverWait to return our mock element
                mock_wait.return_value.until.return_value = mock_element
                
                # Set up mock elements for username, password, and login button
                mock_chrome_driver.find_element = MagicMock()
                mock_chrome_driver.find_element.side_effect = [
                    mock_element,  # password input
                    mock_element,  # login button
                ]
                
                # Initialize logging
                logging = ShareWoodLogging(mock_chrome_driver, login_url, logout_url)
                
                # Create attribute fixing driver reference
                logging.driver = mock_chrome_driver
                
                # Execute
                result = logging.connect("test_user", "test_pass")
                
                # Verify
                assert mock_chrome_driver.get.called_with(login_url)
                
                # Check that WebDriverWait was called with driver and timeout
                mock_wait.assert_called_with(mock_chrome_driver, 10)
                
                # Check that until was called with visibility_of_element_located
                mock_wait.return_value.until.assert_called_with(
                    mock_ec.visibility_of_element_located.return_value
                )
                
                # Check that mock_element.send_keys was called with username
                mock_element.send_keys.assert_called_with("test_user")
                
                # Check that find_element was called for password and login button
                assert mock_chrome_driver.find_element.call_count == 2
    
    def test_disconnect(self, mock_chrome_driver):
        """Test the disconnect method"""
        # Setup
        login_url = "https://www.sharewood.tv/login"
        logout_url = "https://www.sharewood.tv/logout"
        
        with patch('sharewoodautomator.sharewoodlogging.WebDriverWait') as mock_wait:
            with patch('sharewoodautomator.sharewoodlogging.EC') as mock_ec:
                # Initialize logging
                logging = ShareWoodLogging(mock_chrome_driver, login_url, logout_url)
                
                # Execute
                result = logging.disconnect()
                
                # Verify
                assert mock_chrome_driver.get.called_with(logout_url)
                
                # Check that WebDriverWait was called
                mock_wait.assert_called_with(mock_chrome_driver, 10)
                
                # Check that until was called with url_contains
                mock_wait.return_value.until.assert_called_with(
                    mock_ec.url_contains.return_value
                )
                
                # Check result
                assert result is True