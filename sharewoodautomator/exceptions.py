#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Custom exceptions for the ShareWoodAutomator package."""


class ShareWoodError(Exception):
    """Base exception for all ShareWoodAutomator errors."""
    
    def __init__(self, message="An error occurred in ShareWoodAutomator", original_exception=None):
        """
        Initialize the base ShareWood error.

        Args:
            message: Error message describing the issue
            original_exception: The original exception that caused this error
        """
        self.original_exception = original_exception
        if original_exception:
            message = f"{message}: {str(original_exception)}"
        super().__init__(message)


class ShareWoodConnectionError(ShareWoodError):
    """Raised when connection to ShareWood.tv fails."""
    
    def __init__(self, message="Failed to connect to ShareWood.tv", original_exception=None):
        """
        Initialize a connection error.

        Args:
            message: Error message describing the connection issue
            original_exception: The original exception that caused this error
        """
        super().__init__(message, original_exception)


class ShareWoodAuthenticationError(ShareWoodError):
    """Raised when authentication to ShareWood.tv fails."""
    
    def __init__(self, message="Authentication to ShareWood.tv failed", original_exception=None):
        """
        Initialize an authentication error.

        Args:
            message: Error message describing the authentication issue
            original_exception: The original exception that caused this error
        """
        super().__init__(message, original_exception)


class ShareWoodSearchError(ShareWoodError):
    """Raised when search on ShareWood.tv fails."""
    
    def __init__(self, message="Failed to search on ShareWood.tv", original_exception=None):
        """
        Initialize a search error.

        Args:
            message: Error message describing the search issue
            original_exception: The original exception that caused this error
        """
        super().__init__(message, original_exception)


class ShareWoodParsingError(ShareWoodError):
    """Raised when parsing ShareWood.tv HTML fails."""
    
    def __init__(self, message="Failed to parse ShareWood.tv HTML", original_exception=None):
        """
        Initialize a parsing error.

        Args:
            message: Error message describing the parsing issue
            original_exception: The original exception that caused this error
        """
        super().__init__(message, original_exception)


class ShareWoodDownloadError(ShareWoodError):
    """Raised when downloading a torrent from ShareWood.tv fails."""
    
    def __init__(self, message="Failed to download torrent from ShareWood.tv", original_exception=None):
        """
        Initialize a download error.

        Args:
            message: Error message describing the download issue
            original_exception: The original exception that caused this error
        """
        super().__init__(message, original_exception)


class ShareWoodConfigError(ShareWoodError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message="Invalid or missing configuration", original_exception=None):
        """
        Initialize a configuration error.

        Args:
            message: Error message describing the configuration issue
            original_exception: The original exception that caused this error
        """
        super().__init__(message, original_exception)


class ShareWoodTorrentError(ShareWoodError):
    """Raised when torrent operations fail."""
    
    def __init__(self, message="Torrent operation failed", original_exception=None):
        """
        Initialize a torrent operation error.

        Args:
            message: Error message describing the torrent operation issue
            original_exception: The original exception that caused this error
        """
        super().__init__(message, original_exception)
