#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
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
