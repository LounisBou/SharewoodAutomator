#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sharewoodautomator import ShareWoodAutomator, ShareWoodSearchCriteria

# Main entry point
if __name__ == "__main__":
    # Create ShareWood.tv automator instance
    automator = ShareWoodAutomator(headless=False)

    # Perform search on ShareWood.tv
    automator.search(
        ShareWoodSearchCriteria(
            query="The Shawshank Redemption",
            sorting="date",
            order="desc",
        )
    )
    
    # Close ShareWood.tv automator instance
    del automator