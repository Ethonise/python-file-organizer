# File Organizer Utility

A Python CLI tool designed to automate directory cleanup by sorting files into categorized folders based on their extensions.

### Tech Stack
* Python 3
* Modules: os, shutil, argparse

### Key Features
* Automatic Categorization: Groups files into designated folders (e.g., Code, Documents, Images).
* Safe Execution Mode (--dry-run): Simulates the sorting process in the console before making any actual file operations.
* Summary Report: Displays a concise overview of scanned and moved files.

### Usage
1. Run the organizer in the target folder:
   python organizer.py

2. Run in dry-run mode to inspect changes safely:
   python organizer.py --dry-run
