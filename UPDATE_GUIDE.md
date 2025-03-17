# ShareWoodAutomator Project Update Guide

This guide will help you implement changes to take advantage of the new configuration files and structure that have been added to your project.

## 1. Update Your Development Environment

First, set up your development environment to use the new configuration:

```bash
# Create and activate a virtual environment (if not already done)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode with extra dependencies
pip install -e ".[dev,docs]"

# Install pre-commit hooks
pre-commit install
```

## 2. Simplify setup.py

Since most configuration has moved to setup.cfg, you can simplify your setup.py file:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

if __name__ == "__main__":
    setup()
```

## 3. Create a Development Requirements File

Create a requirements-dev.txt file for contributors:

```
-e ".[dev,docs]"
```

## 4. Add Type Hints Throughout the Codebase

The py.typed marker indicates your package supports type hints. Add comprehensive type hints to all your functions:

```python
# Before
def search(self, search_criteria):
    ...

# After
from typing import List, Optional
def search(self, search_criteria: ShareWoodSearchCriteria) -> List[ShareWoodTorrent]:
    ...
```

## 5. Create Package Documentation

Set up Sphinx documentation to take advantage of the 'docs' extras:

```bash
mkdir -p docs
cd docs
sphinx-quickstart  # Follow the prompts
```

Edit the created conf.py to use your package version:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import sharewoodautomator
version = sharewoodautomator.__version__
release = version
```

## 6. Create Example Scripts

Create an examples directory with usage examples:

```bash
mkdir -p examples
```

Add example scripts like:

```python
# examples/basic_search.py
#!/usr/bin/env python3
from sharewoodautomator import ShareWoodAutomator, ShareWoodSearchCriteria

# Initialize the automator
automator = ShareWoodAutomator(headless=True)

try:
    # Connect to ShareWood.tv
    automator.connect()

    # Create search criteria
    criteria = ShareWoodSearchCriteria(
        query="Ubuntu 22.04",
        categories={"Applications": True},
        subcategories={"Application Linux": True},
        sorting="seeders",
        direction="desc"
    )

    # Search for torrents
    results = automator.search(criteria)
    
    # Display results
    for result in results:
        print(f"{result.title} - Size: {result.size} - Seeders: {result.seeders}")

finally:
    # Always disconnect properly
    automator.disconnect()
```

## 7. Update CI/CD Pipeline

Update your GitHub Actions workflow to use setup.cfg configuration:

```yaml
# .github/workflows/python-package.yml
name: Python package

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install -e ".[dev]"
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --statistics
    - name: Type check with mypy
      run: |
        mypy sharewoodautomator
    - name: Test with pytest
      run: |
        pytest --cov=sharewoodautomator
```

## 8. Create a tox.ini File for Multi-environment Testing

```ini
[tox]
envlist = py36, py37, py38, py39, py310, py311, lint, type
isolated_build = True

[testenv]
deps = pytest
       pytest-cov
commands = pytest {posargs:tests}

[testenv:lint]
deps = flake8
commands = flake8 sharewoodautomator

[testenv:type]
deps = mypy
commands = mypy sharewoodautomator
```

## 9. Package Configuration Management

Create a configuration module to handle settings properly:

```python
# sharewoodautomator/config.py
import os
from typing import Dict, Optional
from dotenv import load_dotenv


class ShareWoodConfig:
    """Configuration manager for ShareWoodAutomator."""
    
    def __init__(self, env_file: Optional[str] = None) -> None:
        """
        Initialize configuration from environment variables or .env file.
        
        Args:
            env_file: Path to .env file (default: None, will search in current directory)
        """
        # Load environment variables
        load_dotenv(dotenv_path=env_file)
        
        # ShareWood.tv URLs
        self.url = os.getenv("SHAREWOOD_URL", "https://www.sharewood.tv")
        self.login_url = os.getenv("SHAREWOOD_LOGIN_URL", f"{self.url}/login")
        self.logout_url = os.getenv("SHAREWOOD_LOGOUT_URL", f"{self.url}/logout")
        self.torrents_url = os.getenv("SHAREWOOD_TORRENTS_URL", f"{self.url}/torrents")
        self.api_url = os.getenv("SHAREWOOD_API_URL", f"{self.url}/api/")
        
        # Credentials
        self.username = os.getenv("PSEUDO")
        self.password = os.getenv("PASSWORD")
        self.passkey = os.getenv("SHAREWOOD_PASSKEY")
        
        # Download settings
        self.download_path = os.getenv("DOWNLOAD_PATH", "~/Downloads/Sharewood")
        
        # Validate required settings
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate that required configuration is present."""
        missing = []
        
        if not self.username:
            missing.append("PSEUDO")
        if not self.password:
            missing.append("PASSWORD")
            
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
    
    def to_dict(self) -> Dict[str, str]:
        """Convert configuration to dictionary."""
        return {
            "SHAREWOOD_URL": self.url,
            "SHAREWOOD_LOGIN_URL": self.login_url,
            "SHAREWOOD_LOGOUT_URL": self.logout_url,
            "SHAREWOOD_TORRENTS_URL": self.torrents_url,
            "SHAREWOOD_API_URL": self.api_url,
            "SHAREWOOD_PASSKEY": self.passkey or "",
            "PSEUDO": self.username or "",
            "PASSWORD": self.password or "",
            "DOWNLOAD_PATH": self.download_path,
        }
```

## 10. Implement Proper Logging

Replace print statements with Python's logging module:

```python
# sharewoodautomator/sharewoodlogging.py
import logging
from selenium import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up logger
logger = logging.getLogger(__name__)

class ShareWoodLogging:
    """Centralized logging facility for ShareWood.tv"""

    def __init__(self, browser: WebDriver, login_url: str, logout_url: str) -> None:
        """
        Initialize a new logger for ShareWood.tv
        
        Args:
            browser: selenium WebDriver instance
            login_url: URL for ShareWood.tv login page
            logout_url: URL for ShareWood.tv logout page
        """
        self.browser = browser
        self.login_url = login_url
        self.logout_url = logout_url

    def connect(self, pseudo: str, password: str) -> bool:
        """
        Connect to ShareWood.tv
        
        Args:
            pseudo: ShareWood.tv username
            password: ShareWood.tv password
        Returns:
            True if login successful, False otherwise
        """
        self.browser.get(self.login_url)
        assert "ShareWood" in self.browser.title
        logger.info("Accessed ShareWood.tv login page")

        # Enter credentials and submit form
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys(pseudo)
        self.browser.find_element(By.NAME, "password").send_keys(password)
        self.browser.find_element(By.ID, "login-button").click()

        # Verify successful redirect
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("/torrents")
        )

        logger.info("Successfully logged in to ShareWood.tv")
        return True
```

## 11. Setup Version Control Hooks

Update your pre-commit configuration with more checks:

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]
        types: [python]
        files: \.(py)$
        exclude: ^(venv/|\.env/|\.venv/|env/)

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
        args: ["--profile", "black"]

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
        args: [--line-length=100]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-requests]
```

## 12. Prepare for PyPI Distribution

Update your credentials in ~/.pypirc:

```
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = testpypi-token
```

Build and publish your package:

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m build

# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Then upload to PyPI when ready
python -m twine upload dist/*
```

## 13. Create a CHANGELOG.md File

Keep track of your project's history:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-03-17

### Added
- Initial release
- Login management
- Advanced search functionality
- Torrent scraping
- Automated downloads
```

By implementing these changes, you'll significantly improve your package structure and make it more maintainable, professional, and user-friendly.