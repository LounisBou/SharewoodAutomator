#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field, fields
from typing import Dict, Optional, Set

from sharewoodautomator.sharewoodselectors import SEARCH_CRITERIA_SELECTORS


@dataclass
class ShareWoodSearchCriteria:
    """Search criteria for ShareWood.tv"""

    query: Optional[str] = field(
        default=None,
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["query"],
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["description"],
        }
    )
    uploader: Optional[str] = field(
        default=None,
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["uploader"],
        }
    )
    tags: Optional[str] = field(
        default=None,
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["tags"],
        }
    )
    categories: Optional[Dict[str, bool]] = field(
        default_factory=lambda: {
            "Vidéos": False,
            "Audios": False,
            "Applications": False,
            "Ebooks": False,
            "Jeux-Vidéos": False,
            "Formations": False,
        },
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["categories"]
        }
    )
    subcategories: Optional[Dict[str, bool]] = field(
        default_factory=lambda: {
            "Application Linux": False,
            "Application Mac": False,
            "Application Smartphone/Tablette": False,
            "Application Windows": False,
            "GPS": False,
        },
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["subcategories"]
        }
    )
    languages: Optional[Dict[str, bool]] = field(
        default_factory=lambda: {
            "Français": False,
            "Anglais": False,
            "Québécois": False,
            "Espagnol": False,
            "Japonais": False,
            "Italien": False,
            "Allemand": False,
            "Autre": False,
        },
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["languages"]
        }
    )
    types: Optional[Dict[str, bool]] = field(
        default_factory=lambda: {
            "stream": False,
            "sd": False,
            "freeleech": False,
            "doubleupload": False,
            "internal": False,
            "downloaded": False,
        },
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["types"]
        }
    )
    sorting_values: Optional[Set[str]] = field(
        default_factory=lambda: {'created_at', 'name', 'seeders', 'leechers', 'times_Completed', 'Size'},
    )
    sorting: Optional[str] = field(
        default=None,
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["sorting"],
        }
    )
    direction_values: Optional[Set[str]] = field(
        default_factory=lambda: {"asc", "desc"},
    )
    direction: Optional[str] = field(
        default=None,
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["direction"],
        }
    )
    quantity_values: Optional[Set[int]] = field(
        default_factory=lambda: {25, 50, 100},
    )
    quantity: Optional[int] = field(
        default=None,
        metadata={
            "css_selector": SEARCH_CRITERIA_SELECTORS["quantity"],
        }
    )

    def _get_field_metadata(self, field_name: str) -> Optional[Dict[str, str]]:
        """
        Get the metadata for a specific field

        Args:
            field_name: Name of the field to get metadata for
        Returns:
            Metadata dictionary for the field, or None if not found
        Raises:
            ValueError: If the field name is not found in the dataclass
        """
        metadata = next((field.metadata for field in fields(self) if field.name == field_name), None)

        if metadata is not None:
            return {key: value for key, value in metadata.items() if key != "class"}
        return None

    def _get_field_metadata_attribute(self, field_name: str, attribute: str) -> Optional[str]:
        """
        Get a specific attribute from the metadata of a field

        Args:
            field_name: Name of the field to get metadata for
            attribute: Attribute to retrieve from the metadata
        Returns:
            Value of the specified attribute, or None if not found
        Raises:
            ValueError: If the field name is not found in the dataclass
        """
        metadata = self._get_field_metadata(field_name)

        if metadata is not None and attribute in metadata:
            return metadata[attribute]
        return None

    def get_css_selector(self, field_name: str) -> Optional[str]:
        """
        Get the CSS selector for a specific field

        Args:
            field_name: Name of the field to get the CSS selector for
        Returns:
            CSS selector string, or None if not found
        Raises:
            ValueError: If the field name is not found in the dataclass
        """
        return self._get_field_metadata_attribute(field_name, "css_selector")
