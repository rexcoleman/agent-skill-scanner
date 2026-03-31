---
name: file-organizer
description: "Organize files in the current directory by extension. Use when: (1) cleaning up downloads, (2) sorting project files. NOT for: system directories, hidden files."
metadata:
  {
    "openclaw":
      {
        "emoji": "📁",
        "requires": { "bins": ["mkdir", "mv"] },
      },
  }
---

# File Organizer

## Overview

Organize files in the current directory into subdirectories by file extension.

## When to Use

- Cleaning up a messy downloads folder
- Sorting files after a bulk download
- Organizing project assets

## When NOT to Use

- System directories (/, /etc, /usr)
- Hidden files (dotfiles)
- When you need to preserve flat structure

## Usage

```bash
# Create directories for each extension
for ext in $(find . -maxdepth 1 -type f -name '*.*' | sed 's/.*\.//' | sort -u); do
    mkdir -p "$ext"
    mv *."$ext" "$ext/" 2>/dev/null
done
```

## Options

- `--dry-run`: Show what would be moved without moving
- `--recursive`: Also organize subdirectories
- `--exclude`: Skip certain extensions
