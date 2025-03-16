#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

@dataclass
class ShareWoodSearchCriteria:
    """Search criteria for ShareWood.tv"""

    query: str = field(
        default=None, 
        metadata={
            "id": "search", 
            "name": "research", 
            "placeholder": "Nom / Titre",
        }
    )
    description: str = field(
        default=None, 
        metadata={
            "id": "description", 
            "name": "description", 
            "placeholder": "Acteur, Réalisateur, Langue, ..."
        }
    )
    uploader: str = field(
        default=None, 
        metadata={"placeholder": "Nom de l'uploader"}
    )
    tags: str = field(
        default=None, 
        metadata={"placeholder": "tags",}
    )
    categories: dict = field(
        default={
            "Vidéos": False, 
            "Audios": False, 
            "Applications": False, 
            "Ebooks": False, 
            "Jeux-Vidéos": False, 
            "Formations": False,
        }, 
        metadata={"class": "category category-parent"}
    )
    subcategories: dict = field(
        default={
            "Application Linux": False,
            "Application Mac": False,
            "Application Smartphone/Tablette": False,
            "Application Windows": False,
            "GPS": False,
        }, 
        metadata={"class": "subcategory"}
    )
    languages: dict = field(
        default={
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
    type: dict = field(
        default={
            "stream": False, 
            "sd": False,
            "freeleech": False, 
            "doubleupload": False,
            "internal": False, 
            "downloaded": False,
        },
        metadata={"class": "subcategory"}
    )
    sorting_values: set = field(
        default={'created_at', 'name', 'seeders', 'leechers', 'times_Completed', 'Size'},
        metadata={"id": "sorting", "name": "sorting", "class": "form-control"}
    )
    sorting: str = field(
        default=None, # Default will be "created_at"
        metadata={"id": "sort", "name": "sort", "class": "form-control"}
    )
    direction_values: set = field(
        default={"asc", "desc"},
        metadata={"id": "direction", "name": "direction", "class": "form-control"}
    )
    direction: str = field(
        default=None, # Default will be "desc"
        metadata={"id": "direction", "name": "direction", "class": "form-control"}
    )
    quantity_values: set = field(
        default={25, 50, 100},
        metadata={"id": "qty", "name": "qty", "class": "form-control"}
    )
    quantity: int = field(
        default=None, # Default will be 25
        metadata={"id": "qty", "name": "qty", "class": "form-control"}
    )

