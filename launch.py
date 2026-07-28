#!/usr/bin/env python3
"""Launch index.html in default browser - works on Windows, macOS, Linux"""

import webbrowser
import sys
from pathlib import Path

script_dir = Path(__file__).parent.resolve()
index_file = script_dir / "index.html"

if not index_file.exists():
    print(f"Error: Could not find index.html at {index_file}")
    sys.exit(1)

webbrowser.open(index_file.as_uri())
print(f"Opened {index_file.name} in your default browser")
