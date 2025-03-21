#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, patch

import pytest  # noqa: F401

from sharewoodautomator.sharewoodlogging import ShareWoodLogging


class TestShareWoodLogging:
    """Tests for the ShareWoodLogging class"""

    def test_connect(self, mock_chrome_driver):
        """Test the connect method"""        

        # Create mocks for WebDriverWait and expected_conditions
        mock_element = MagicMock()
        mock_element.send_keys = MagicMock()

        with patch('sharewoodautomator.sharewoodlogging.WebDriverWait') as mock_wait:
            with patch('sharewoodautomator.sharewoodlogging.EC'):
                # Set up mock WebDriverWait to return our mock element
                mock_wait.return_value.until.return_value = mock_element

                # Set up mock elements for username, password, and login button
                mock_chrome_driver.find_element = MagicMock()
                mock_chrome_driver.find_element.side_effect = [
                    mock_element,  # username input
                    mock_element,  # password input
                    mock_element,  # login button
                ]

                # Initialize logging
                logging = ShareWoodLogging(
                    browser=mock_chrome_driver, 
                    home_url="https://www.sharewood.tv",
                    login_url="https://www.sharewood.tv/login",
                    logout_url="https://www.sharewood.tv/logout",
                    timeout=30
                )

                # Execute
                result = logging.connect("test_user", "test_password")

                # Verify
                assert mock_chrome_driver.get.called_with("https://www.sharewood.tv/login")
                assert mock_chrome_driver.title == "ShareWood"
                assert mock_chrome_driver.find_element.called
                assert mock_element.send_keys.called
                assert result is True

    def test_disconnect(self, mock_chrome_driver):
        """Test the disconnect method"""
        # Setup
        login_url = "https://www.sharewood.tv/login"
        logout_url = "https://www.sharewood.tv/logout"

        with patch('sharewoodautomator.sharewoodlogging.WebDriverWait') as mock_wait:
            with patch('sharewoodautomator.sharewoodlogging.EC') as mock_ec:
                # Initialize logging
                logging = ShareWoodLogging(
                    browser=mock_chrome_driver, 
                    home_url="https://www.sharewood.tv",
                    login_url=login_url,
                    logout_url=logout_url,
                    timeout=30
                )

                # Execute
                result = logging.disconnect()

                # Verify
                assert mock_chrome_driver.get.called_with(logout_url)

                # Check that WebDriverWait was called
                mock_wait.assert_called_with(mock_chrome_driver, 30)

                # Check that until was called with url_contains
                mock_wait.return_value.until.assert_called_with(
                    mock_ec.url_contains.return_value
                )

                # Check result
                assert result is True
