#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field, fields
from typing import Dict, Optional, Set


@dataclass
class ShareWoodSearchCriteria:
    """Search criteria for ShareWood.tv"""

    query: Optional[str] = field(
        default=None,
        metadata={
            "id": "search",
            "name": "research",
            "placeholder": "Nom / Titre",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "id": "description",
            "name": "description",
            "placeholder": "Acteur, Réalisateur, Langue, ..."
        }
    )
    uploader: Optional[str] = field(
        default=None,
        metadata={"placeholder": "Nom de l'uploader"}
    )
    tags: Optional[str] = field(
        default=None,
        metadata={"placeholder": "tags"}
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
        metadata={"class": "category category-parent"}
    )
    subcategories: Optional[Dict[str, bool]] = field(
        default_factory=lambda: {
            "Application Linux": False,
            "Application Mac": False,
            "Application Smartphone/Tablette": False,
            "Application Windows": False,
            "GPS": False,
        },
        metadata={"class": "subcategory"}
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
        metadata={"class": "subcategory"}
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
        metadata={"class": "subcategory"}
    )
    sorting_values: Optional[Set[str]] = field(
        default_factory=lambda: {'created_at', 'name', 'seeders', 'leechers', 'times_Completed', 'Size'},
        metadata={"id": "sorting", "name": "sorting", "class": "form-control"}
    )
    sorting: Optional[str] = field(
        default=None,
        metadata={"id": "sort", "name": "sort", "class": "form-control"}
    )
    direction_values: Optional[Set[str]] = field(
        default_factory=lambda: {"asc", "desc"},
        metadata={"id": "direction", "name": "direction", "class": "form-control"}
    )
    direction: Optional[str] = field(
        default=None,
        metadata={"id": "direction", "name": "direction", "class": "form-control"}
    )
    quantity_values: Optional[Set[int]] = field(
        default_factory=lambda: {25, 50, 100},
        metadata={"id": "qty", "name": "qty", "class": "form-control"}
    )
    quantity: Optional[int] = field(
        default=None,
        metadata={"id": "qty", "name": "qty", "class": "form-control"}
    )

    def get_field_metadata(self, field_name: str) -> Optional[Dict[str, str]]:
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

    def get_field_metadata_attribute(self, field_name: str, attribute: str) -> Optional[str]:
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
        metadata = self.get_field_metadata(field_name)

        if metadata is not None and attribute in metadata:
            return metadata[attribute]
        return None
