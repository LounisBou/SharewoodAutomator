#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Custom exceptions for the ShareWoodAutomator package."""


class ShareWoodError(Exception):
    """Base exception for all ShareWoodAutomator errors."""
    
    pass


class ShareWoodConnectionError(ShareWoodError):
    """Raised when connection to ShareWood.tv fails."""
    
    pass


class ShareWoodAuthenticationError(ShareWoodError):
    """Raised when authentication to ShareWood.tv fails."""
    
    pass


class ShareWoodSearchError(ShareWoodError):
    """Raised when search on ShareWood.tv fails."""
    
    pass


class ShareWoodParsingError(ShareWoodError):
    """Raised when parsing ShareWood.tv HTML fails."""
    
    pass


class ShareWoodDownloadError(ShareWoodError):
    """Raised when downloading a torrent from ShareWood.tv fails."""
    
    pass


class ShareWoodConfigError(ShareWoodError):
    """Raised when configuration is invalid or missing."""
    
    pass


class ShareWoodTorrentError(ShareWoodError):
    """Raised when torrent operations fail."""
    
    pass
