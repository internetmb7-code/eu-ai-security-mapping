#!/usr/bin/env python3
"""
Update the explorer HTML file with fresh data from explorer-data.json.
"""

import json
import re
import sys
from pathlib import Path

def main():
    """Main update function."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # File paths
    data_file = project_root / 'docs' / 'explorer' / 'explorer-data.json'
    html_file = project_root / 'docs' / 'explorer' / 'index.html'

    print(f"Reading data from {data_file}...")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Reading HTML from {html_file}...")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Minify the JSON data for embedding (single line, no extra whitespace)
    data_json = json.dumps(data, separators=(',', ':'), ensure_ascii=False)

    # Find and replace the script data section
    # Pattern: <script id="data" type="application/json">{...}</script>
    pattern = r'<script id="data" type="application/json">.*?</script>'
    replacement = f'<script id="data" type="application/json">{data_json}</script>'

    new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

    if new_html == html_content:
        print("⚠ Warning: No data section found or replaced in HTML!")
        return 1

    print(f"Writing updated HTML to {html_file}...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"✓ Explorer HTML updated successfully")
    print(f"  Data size: {len(data_json):,} bytes")

    return 0

if __name__ == '__main__':
    sys.exit(main())
