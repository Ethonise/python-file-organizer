#!/usr/bin/env python3
"""
File Organizer
---------------
Sorts files in a folder into subfolders by type (Images, Documents, Videos, etc).

Usage:
    python organizer.py /path/to/folder
    python organizer.py /path/to/folder --dry-run
    python organizer.py /path/to/folder --recursive
"""

import argparse
import shutil
import logging
from pathlib import Path

# Map of category name -> list of file extensions
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".java", ".cpp", ".sh"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
}

# Reverse lookup: extension -> category, built once at import time
EXTENSION_MAP = {
    ext: category
    for category, extensions in CATEGORIES.items()
    for ext in extensions
}


def get_category(file_path: Path) -> str:
    """Return the category folder name for a given file, or 'Other' if unknown."""
    return EXTENSION_MAP.get(file_path.suffix.lower(), "Other")


def resolve_conflict(destination: Path) -> Path:
    """
    If destination already exists, append a number: file.txt -> file (1).txt
    Prevents overwriting files that happen to share a name.
    """
    if not destination.exists():
        return destination

    stem, suffix, parent = destination.stem, destination.suffix, destination.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(folder: Path, dry_run: bool = False, recursive: bool = False) -> dict:
    """
    Sorts files in `folder` into category subfolders.
    Returns a summary dict of {category: count} for reporting.
    """
    pattern = "**/*" if recursive else "*"
    summary = {}

    for item in folder.glob(pattern):
        # Skip directories and anything already inside a category folder we created
        if item.is_dir() or item.parent.name in CATEGORIES.values() or item.parent.name == "Other":
            continue
        if item.parent.name in CATEGORIES:
            continue

        category = get_category(item)
        target_folder = folder / category
        target_path = resolve_conflict(target_folder / item.name)

        summary[category] = summary.get(category, 0) + 1

        if dry_run:
            logging.info(f"[DRY RUN] Would move: {item.name} -> {category}/")
        else:
            target_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(target_path))
            logging.info(f"Moved: {item.name} -> {category}/")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Sort files in a folder by type.")
    parser.add_argument("folder", type=str, help="Path to the folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--recursive", action="store_true", help="Also organize files in subfolders")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        logging.error(f"Error: '{folder}' is not a valid folder.")
        return

    logging.info(f"{'[DRY RUN] ' if args.dry_run else ''}Organizing: {folder}\n")
    summary = organize_folder(folder, dry_run=args.dry_run, recursive=args.recursive)

    if not summary:
        logging.info("No files to organize — folder is already tidy (or empty).")
        return

    logging.info("\nSummary:")
    for category, count in sorted(summary.items()):
        logging.info(f"  {category}: {count} file(s)")


if __name__ == "__main__":
    main()