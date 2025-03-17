#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import MagicMock, patch

import pytest
from selenium.webdriver import Chrome


@pytest.fixture
def mock_env():
    """Fixture to provide mock environment variables"""
    return {
        "SHAREWOOD_URL": "https://www.sharewood.tv",
        "SHAREWOOD_LOGIN_URL": "https://www.sharewood.tv/login",
        "SHAREWOOD_LOGOUT_URL": "https://www.sharewood.tv/logout",
        "SHAREWOOD_TORRENTS_URL": "https://www.sharewood.tv/torrents",
        "SHAREWOOD_API_URL": "https://www.sharewood.tv/api/",
        "SHAREWOOD_PASSKEY": "mock_passkey",
        "PSEUDO": "mock_username",
        "PASSWORD": "mock_password",
        "DOWNLOAD_PATH": "/tmp/sharewood_downloads"
    }


@pytest.fixture
def mock_chrome_driver():
    """Fixture to provide a mock Chrome WebDriver"""
    mock_driver = MagicMock(spec=Chrome)
    # Set up basic mocked behavior
    mock_driver.title = "ShareWood"
    mock_driver.page_source = "<html><body>Mocked HTML</body></html>"
    mock_driver.current_url = "https://www.sharewood.tv"
    return mock_driver


@pytest.fixture
def mock_load_dotenv():
    """Fixture to mock python-dotenv's load_dotenv function"""
    with patch('dotenv.load_dotenv') as mock:
        yield mock


@pytest.fixture
def ensure_test_dir():
    """Fixture to ensure test directories exist"""
    test_dirs = [
        '/tmp/sharewood_downloads',
        'tests/fixtures'
    ]
    
    for directory in test_dirs:
        os.makedirs(directory, exist_ok=True)
    
    yield
    
    # Clean up test directories
    for directory in test_dirs:
        os.removedirs(directory)
