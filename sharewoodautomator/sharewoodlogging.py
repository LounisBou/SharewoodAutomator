#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
        print("Accessed ShareWood.tv login page")

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

        print("Successfully logged in to ShareWood.tv")

    def disconnect(self) -> bool:
        """
        Disconnect from ShareWood.tv

        Returns:
            True if logout successful, False otherwise
        """

        # Navigate to logout page
        self.browser.get(self.logout_url)

        # Check if we are on the login page
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("login")
        )

        print("Successfully logged out of ShareWood.tv")

        return True
