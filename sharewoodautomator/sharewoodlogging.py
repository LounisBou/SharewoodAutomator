#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ShareWoodLogging:
    """Centralized logging facility for ShareWood.tv"""

    def __init__(self, browser: WebDriver, home_url: str, login_url: str, logout_url: str, timeout: int) -> None:
        """
        ShareWood.tv logging manager
        
        Args:
            browser: selenium WebDriver instance
            home_url: URL for ShareWood.tv home page
            login_url: URL for ShareWood.tv login page
            logout_url: URL for ShareWood.tv logout page
            timeout: Timeout for WebDriverWait
        """

        self.browser = browser
        self.home_url = home_url
        self.login_url = login_url
        self.logout_url = logout_url
        self.timeout = timeout

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
        WebDriverWait(self.browser, self.timeout).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        self.browser.find_element(By.NAME, "username").send_keys(pseudo)
        WebDriverWait(self.browser, self.timeout).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        self.browser.find_element(By.NAME, "password").send_keys(password)
        
        # Click on the login button
        WebDriverWait(self.browser, self.timeout).until(
            EC.visibility_of_element_located((By.ID, "login-button"))
        )
        self.browser.find_element(By.ID, "login-button").click()

        # Verify successful redirect to home_url
        WebDriverWait(self.browser, self.timeout).until(
            EC.url_contains(self.home_url)
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
        WebDriverWait(self.browser, self.timeout).until(
            EC.url_contains("login")
        )

        print("Successfully logged out of ShareWood.tv")

        return True
