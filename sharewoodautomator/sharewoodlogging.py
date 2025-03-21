#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sharewoodautomator.sharewoodselectors import (
    LOGIN_SELECTORS,
    PAGE_CONTROLS_SELECTORS,
)


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

        try:
            self.browser.get(self.login_url)

            # Wait for the page to load
            WebDriverWait(self.browser, self.timeout).until(
                EC.url_contains(self.login_url)
            )
            print("Accessed ShareWood.tv login page")

            # Enter credentials and submit form

            # - Username
            WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, LOGIN_SELECTORS["username_input"]))
            )
            self.browser.find_element(
                by=By.CSS_SELECTOR,
                value=LOGIN_SELECTORS["username_input"]
            ).send_keys(pseudo)

            # - Password
            WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, LOGIN_SELECTORS["password_input"]))
            )
            self.browser.find_element(
                by=By.CSS_SELECTOR,
                value=LOGIN_SELECTORS["password_input"]
            ).send_keys(password)

            # Click on the login button
            WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, LOGIN_SELECTORS["login_button"]))
            )
            self.browser.find_element(
                by=By.CSS_SELECTOR,
                value=LOGIN_SELECTORS["login_button"]
            ).click()

            # Wait for the home page to load completely
            WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#frame > .content > .messages"))
            )

            # Search for cookie button and click it if present
            try:
                # Retrieve the cookie button element (dont wait for it)
                cookie_button = self.browser.find_element(
                    by=By.CSS_SELECTOR,
                    value=PAGE_CONTROLS_SELECTORS["cookie_button"]
                )
                # Click the cookie button
                cookie_button.click()
                print("Cookie button clicked")
            except TimeoutException:
                print("Cookie button not found, continuing...")

            print("Successfully logged in to ShareWood.tv")
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login failed: {e}")
            return False

        return True

    def disconnect(self) -> bool:
        """
        Disconnect from ShareWood.tv

        Returns:
            True if logout successful, False otherwise
        """
        try:
            # Navigate to logout page
            self.browser.get(self.logout_url)

            # Verify successful logout
            WebDriverWait(self.browser, self.timeout).until(
                EC.url_contains(self.login_url)
            )
            print("Successfully logged out of ShareWood.tv")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Logout failed: {e}")
            return False

        return True
