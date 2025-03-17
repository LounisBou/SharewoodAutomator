#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command-line interface for ShareWoodAutomator.
Provides functionality to search, scrape, and download torrents from ShareWood.tv.
"""

import argparse
import os
import sys
from typing import Dict, Optional

from . import ShareWoodAutomator, ShareWoodSearchCriteria, __version__


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="sharewoodautomator",
        description="Automate interactions with ShareWood.tv",
        epilog="For more information, visit: https://github.com/LounisBou/sharewoodautomator",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)",
    )

    parser.add_argument(
        "--no-headless",
        action="store_false",
        dest="headless",
        help="Run browser in visible mode",
    )

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    subparsers.required = True

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for torrents")
    search_parser.add_argument(
        "query", help="Search query (e.g., 'Ubuntu 22.04')"
    )
    search_parser.add_argument(
        "--description", help="Description to search for"
    )
    search_parser.add_argument(
        "--uploader", help="Filter results by uploader"
    )
    search_parser.add_argument(
        "--tags", help="Filter results by tags (comma-separated)"
    )
    search_parser.add_argument(
        "--categories",
        help="Filter by categories (comma-separated, e.g., 'Vidéos,Audios')",
    )
    search_parser.add_argument(
        "--subcategories",
        help="Filter by subcategories (comma-separated, e.g., 'Application Linux,Application Mac')",
    )
    search_parser.add_argument(
        "--languages",
        help="Filter by languages (comma-separated, e.g., 'Français,Anglais')",
    )
    search_parser.add_argument(
        "--sorting",
        choices=["created_at", "name", "seeders", "leechers", "times_Completed", "Size"],
        default="created_at",
        help="Sort results by field (default: created_at)",
    )
    search_parser.add_argument(
        "--direction",
        choices=["asc", "desc"],
        default="desc",
        help="Sort direction (default: desc)",
    )
    search_parser.add_argument(
        "--quantity",
        type=int,
        choices=[25, 50, 100],
        default=25,
        help="Number of results to return (default: 25)",
    )

    # Download command
    download_parser = subparsers.add_parser("download", help="Download a torrent")
    download_parser.add_argument(
        "url", help="URL of the torrent to download"
    )
    download_parser.add_argument(
        "--output",
        "-o",
        help="Directory to save the downloaded torrent (default: ./downloads)",
        default="./downloads",
    )

    return parser.parse_args()


def process_comma_separated_list(value: Optional[str], options: Dict[str, bool]) -> Dict[str, bool]:
    """Process comma-separated values into dictionary of boolean flags."""
    if not value:
        return options

    result = {k: False for k in options.keys()}
    for item in value.split(","):
        item = item.strip()
        if item in result:
            result[item] = True

    return result


def main() -> int:
    """Main entry point for the application."""
    args = parse_arguments()

    try:
        # Create automator instance
        automator = ShareWoodAutomator(headless=args.headless)

        # Connect to ShareWood.tv
        automator.connect()

        if args.command == "search":
            # Process category flags
            categories = process_comma_separated_list(
                args.categories, ShareWoodSearchCriteria().categories
            )
            subcategories = process_comma_separated_list(
                args.subcategories, ShareWoodSearchCriteria().subcategories
            )
            languages = process_comma_separated_list(
                args.languages, ShareWoodSearchCriteria().languages
            )

            # Create search criteria
            criteria = ShareWoodSearchCriteria(
                query=args.query,
                description=args.description,
                uploader=args.uploader,
                tags=args.tags,
                categories=categories,
                subcategories=subcategories,
                languages=languages,
                sorting=args.sorting,
                direction=args.direction,
                quantity=args.quantity,
            )

            # Perform search
            results = automator.search(criteria)
            print(f"Found {len(results)} results for '{args.query}'")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.title} - Seeders: {result.seeders}, Size: {result.size}")

        elif args.command == "download":
            # Create output directory if it doesn't exist
            os.makedirs(args.output, exist_ok=True)
            
            # Download torrent
            automator.download(args.url)
            print(f"Downloaded torrent to {args.output}")

    except (ConnectionError, ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        # Always disconnect
        try:
            automator.disconnect()
        except (ConnectionError, ValueError, OSError):
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
