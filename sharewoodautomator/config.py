#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        
        # Expand user directory in download path
        if self.download_path:
            self.download_path = os.path.expanduser(self.download_path)
        
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
