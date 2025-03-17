#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import patch

import pytest

from sharewoodautomator.sharewoodtorrent import ShareWoodTorrent


class TestShareWoodTorrent:
    """Tests for the ShareWoodTorrent class"""
    
    def test_init(self):
        """Test torrent initializes correctly"""
        # Setup & Execute
        torrent = ShareWoodTorrent(
            url="https://www.sharewood.tv/torrents/123",
            title="Test Torrent",
            description="Test Description",
            hash="abcdef1234567890",
            uploader="test_user",
            size="1.5 GB",
            seeders=10,
            leechers=5
        )
        
        # Verify
        assert torrent.url == "https://www.sharewood.tv/torrents/123"
        assert torrent.title == "Test Torrent"
        assert torrent.description == "Test Description"
        assert torrent.hash == "abcdef1234567890"
        assert torrent.uploader == "test_user"
        assert torrent.size == "1.5 GB"
        assert torrent.seeders == 10
        assert torrent.leechers == 5
        assert torrent.downloaded is False
        assert torrent.downloaded_path is None
    
    def test_repr(self):
        """Test string representation"""
        # Setup
        torrent = ShareWoodTorrent(
            title="Test Torrent",
            description="Test Description",
            uploader="test_user",
            size="1.5 GB",
            age="2 days",
            seeders=10,
            leechers=5,
            completed=100,
            download_link="https://www.sharewood.tv/download/123"
        )
        
        # Execute
        repr_string = repr(torrent)
        
        # Verify
        assert "Test Torrent" in repr_string
        assert "Test Description" in repr_string
        assert "test_user" in repr_string
        assert "1.5 GB" in repr_string
        assert "2 days" in repr_string
        assert "10" in repr_string  # seeders
        assert "5" in repr_string   # leechers
        assert "100" in repr_string  # completed
        assert "https://www.sharewood.tv/download/123" in repr_string
    
    def test_str(self):
        """Test string conversion"""
        # Setup
        torrent = ShareWoodTorrent(title="Test Torrent")
        
        # Execute
        str_string = str(torrent)
        
        # Verify
        assert "Test Torrent" in str_string
    
    @pytest.mark.parametrize("download_path", [
        ".",
        "/tmp/downloads",
        "tests/fixtures"
    ])
    def test_download(self, download_path, ensure_test_dir):
        """Test downloading a torrent file"""
        # Setup
        torrent = ShareWoodTorrent(
            title="Test Torrent",
            download_link="https://www.sharewood.tv/download/123"
        )
        
        # Create the directory if it doesn't exist
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        # Mock urllib.request.urlretrieve
        with patch('sharewoodautomator.sharewoodtorrent.request.urlretrieve') as mock_urlretrieve:
            # Set up mock to return a file path
            mock_urlretrieve.return_value = (f"{download_path}/Test Torrent.torrent", None)
            
            # Execute
            torrent.download(download_path)
            
            # Verify
            mock_urlretrieve.assert_called_once_with(
                "https://www.sharewood.tv/download/123",
                f"{download_path}/Test Torrent.torrent"
            )
            assert torrent.downloaded is True
            assert torrent.downloaded_path == f"{download_path}/Test Torrent.torrent"
    
    def test_download_no_link(self):
        """Test downloading with no download link"""
        # Setup
        torrent = ShareWoodTorrent(title="Test Torrent")
        
        # Execute & Verify
        with pytest.raises(Exception) as excinfo:
            torrent.download()
        
        assert "No download link available" in str(excinfo.value)
    
    def test_download_error(self, ensure_test_dir):
        """Test download error handling"""
        # Setup
        torrent = ShareWoodTorrent(
            title="Test Torrent",
            download_link="https://www.sharewood.tv/download/123"
        )
        
        # Mock urllib.request.urlretrieve to return None
        with patch('sharewoodautomator.sharewoodtorrent.request.urlretrieve') as mock_urlretrieve:
            mock_urlretrieve.return_value = None
            
            # Execute & Verify
            with pytest.raises(Exception) as excinfo:
                torrent.download()
            
            assert "Failed to download torrent file" in str(excinfo.value)
    
    def test_delete(self, ensure_test_dir):
        """Test deleting a downloaded torrent file"""
        # Setup
        test_file = "/tmp/sharewood_downloads/test_torrent.torrent"
        
        # Create an empty test file
        with open(test_file, 'w') as f:
            f.write("test content")
        
        # Create torrent with downloaded=True and path set
        torrent = ShareWoodTorrent(title="Test Torrent")
        torrent.downloaded = True
        torrent.downloaded_path = test_file
        
        # Execute
        torrent.delete()
        
        # Verify
        assert not os.path.exists(test_file)
        assert torrent.downloaded is False
        assert torrent.downloaded_path is None
    
    def test_delete_not_downloaded(self):
        """Test deleting when torrent was not downloaded"""
        # Setup
        torrent = ShareWoodTorrent(title="Test Torrent")
        torrent.downloaded = False
        
        # Execute & Verify
        # Should not raise an exception
        torrent.delete()
    
    def test_delete_file_not_found(self):
        """Test deleting when file does not exist"""
        # Setup
        torrent = ShareWoodTorrent(title="Test Torrent")
        torrent.downloaded = True
        torrent.downloaded_path = "/tmp/non_existent_file.torrent"
        
        # Execute & Verify
        with pytest.raises(Exception) as excinfo:
            torrent.delete()
        
        assert "Downloaded torrent file not found" in str(excinfo.value)
