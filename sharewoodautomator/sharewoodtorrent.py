#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from urllib import request
from dataclasses import dataclass, field

@dataclass
class ShareWoodTorrent:
    """ShareWood.tv torrent"""

    url: str = field(
        init=True,
        default=None,
        metadata={"description": "URL of the torrent page"}
    )
    title: str = field(
        init=True,
        default=None,
        metadata={"description": "Title of the torrent"}
    )
    description: str = field(
        init=True,
        default=None,
        metadata={"description": "Description of the torrent"}
    )
    hash: str = field(
        init=True,
        default=None,
        metadata={"description": "Hash of the torrent"}
    )
    uploader: str = field(
        init=True,
        default=None,
        metadata={"description": "Uploader of the torrent"}
    )
    uploader_profile: str = field(
        init=True,
        default=None,
        metadata={"description": "URL of the uploader profile"}
    )
    size: str = field(
        init=True,
        default=None,
        metadata={"description": "Size of the torrent"}
    )
    age: str = field(
        init=True,
        default=None,
        metadata={"description": "Age of the torrent"}
    )
    ratio: str = field(
        init=True,
        default=None,
        metadata={"description": "Estimated ratio of the torrent"}
    )
    tags: str = field(
        init=True,
        default=None,
        metadata={"description": "Tags of the torrent"}
    )
    resolution: str = field(
        init=True,
        default=None,
        metadata={"description": "Resolution of the torrent"}
    )
    seeders: int = field(
        init=True,
        default=None,
        metadata={"description": "Number of seeders"}
    )
    leechers: int = field(
        init=True,
        default=None,
        metadata={"description": "Number of leechers"}
    )
    discounts: str = field(
        init=True,
        default=None,
        metadata={"description": "Discounts value of the torrent"}
    )
    fastline_credit_url: str = field(
        init=True,
        default=None,
        metadata={"description": "URL of the fastline credit"}
    )
    category: str = field(
        init=True,
        default=None,
        metadata={"description": "Category of the torrent"}
    )
    subcategory: str = field(
        init=True,
        default=None,
        metadata={"description": "Subcategory of the torrent"}
    )
    languages: str = field(
        init=True,
        default=None,
        metadata={"description": "Languages of the torrent"}
    )
    _3d_flag: bool = field(
        init=True,
        default=None,
        metadata={"description": "Flag indicating if torrent is 3D"}
    )
    completed: int = field(
        init=True,
        default=None,
        metadata={"description": "Number of completed downloads"}
    )
    download_link: str = field(
        init=True,
        default=None,
        metadata={"id": "download_link"}
    )
    downloaded: bool = field(
        init=False,
        default=False,
        metadata={"description": "Flag indicating if torrent has been downloaded"}
    )
    downloaded_path: str = field(
        init=False,
        default=None,
        metadata={"description": "Path to downloaded torrent file"}
    )

    def __repr__(self):
        return f"""
            Torrent {getattr(self, 'title', 'N/A')}
            -------------------
            \t Description: {getattr(self, 'description', 'N/A')}
            \t Uploader: {getattr(self, 'uploader', 'N/A')}
            \t Size: {getattr(self, 'size', 'N/A')}
            \t Age: {getattr(self, 'age', 'N/A')}
            \t Seeders: {getattr(self, 'seeders', 'N/A')}
            \t Leechers: {getattr(self, 'leechers', 'N/A')}
            \t Completed: {getattr(self, 'completed', 'N/A')}
            \t Download link: {getattr(self, 'download_link', 'N/A')}
        """
    
    def __str__(self):
        return self.__repr__()

    def download(self, download_path: str = ".") -> None:
        """ 
        Download torrent file
        
        Args:
            download_path: Path to download torrent file

        Raises:
            Exception: If download link is not available
        """

        # Check if download link is available
        if not self.download_link:
            raise Exception("No download link available")

        # Check if download path exists
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Download torrent file to download path
        download_info = request.urlretrieve(self.download_link, f"{download_path}/{self.title}.torrent")
        
        # Check if download was successful
        if download_info:
            self.downloaded = True
            self.downloaded_path = download_info[0]
        else:
            raise Exception("Failed to download torrent file")
        

    def delete(self) -> None:
        """
        Delete downloaded torrent file
        
        Raises:
            Exception: If downloaded torrent file not found
        """

        # Check if torrent has been downloaded
        if self.downloaded:
            # Check if downloaded path exists
            if os.path.exists(self.downloaded_path):
                os.remove(self.downloaded_path)
                self.downloaded = False
                self.downloaded_path = None
            else:
                raise Exception("Downloaded torrent file not found")