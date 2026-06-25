#!/usr/bin/env python3
"""
Build script for the EU AI Security Mapping Explorer.

Reads source data files (threats.json, controls.json, mappings.json) and
generates the embedded data structure for the HTML explorer.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

def load_json(filepath):
    """Load and parse a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_article(article):
    """
    Extract the base article identifier for grouping.
    E.g., 'Art. 15 (Cybersecurity)' -> 'Art. 15'
          'Art. 6 to 8 (ICT risk management)' -> 'Art. 6 to 8'
          'Art. 5(1)(f)' -> 'Art. 5(1)(f)'
    """
    # Match "Art. X" or "Art. X to Y" or "Art. X(Y)(Z)" pattern
    match = re.match(r'(Art\.\s*\d+(?:\s*to\s*\d+)?(?:\([^)]+\))*)', article)
    if match:
        return match.group(1).strip()
    return article

def get_label_priority(label):
    """
    Return a priority score for labels - prefer ones with descriptions.
    Higher score = better label.
    """
    if '(' in label and ')' in label:
        # Has description in parentheses
        return len(label)  # Longer descriptions are more informative
    return 0  # No description

def build_regulations_structure(mappings, controls_by_id, reg_descriptions):
    """Build the regulations data structure for the explorer."""
    # Use nested defaultdicts with normalized keys
    regulations = defaultdict(lambda: defaultdict(lambda: {'label': '', 'title': '', 'description': '', 'threats': [], 'controls': []}))

    # Track best labels for each normalized article
    best_labels = defaultdict(lambda: defaultdict(str))

    # Populate threats per regulation/article
    for mapping in mappings['threat_addresses_requirement']:
        reg = mapping['regulation']
        article = mapping['article_or_section']
        normalized = normalize_article(article)
        threat_id = mapping['threat_id']
        rationale = mapping['rationale']

        # Update label if this one is better
        if get_label_priority(article) > get_label_priority(best_labels[reg][normalized]):
            best_labels[reg][normalized] = article

        regulations[reg][normalized]['threats'].append({
            'threat_id': threat_id,
            'rationale': rationale
        })

    # Populate controls per regulation/article from control regulatory_basis
    for control_id, control in controls_by_id.items():
        for reg_basis in control.get('regulatory_basis', []):
            reg = reg_basis['regulation']
            article = reg_basis['article_or_section']
            normalized = normalize_article(article)
            relevance = reg_basis['relevance']

            # Update label if this one is better
            if get_label_priority(article) > get_label_priority(best_labels[reg][normalized]):
                best_labels[reg][normalized] = article

            regulations[reg][normalized]['controls'].append({
                'control_id': control_id,
                'relevance': relevance
            })

    # Apply best labels and descriptions
    for reg in regulations:
        for normalized in regulations[reg]:
            best_label = best_labels[reg][normalized]
            if best_label:
                regulations[reg][normalized]['label'] = best_label
            else:
                regulations[reg][normalized]['label'] = normalized

            # Add title and description from regulatory descriptions
            if reg in reg_descriptions and normalized in reg_descriptions[reg]:
                desc_data = reg_descriptions[reg][normalized]
                regulations[reg][normalized]['title'] = desc_data.get('title', '')
                regulations[reg][normalized]['description'] = desc_data.get('description', '')

    # Convert defaultdict to regular dict
    return {reg: dict(articles) for reg, articles in regulations.items()}

def build_explorer_data(threats, controls, mappings, reg_descriptions):
    """Transform source data into explorer format."""

    # Create lookup dictionaries
    controls_by_id = {c['id']: c for c in controls}
    threats_by_id = {t['id']: t for t in threats}

    # Build regulations structure
    regulations = build_regulations_structure(mappings, controls_by_id, reg_descriptions)

    # Build the complete data structure
    data = {
        'regulations': regulations,
        'controls': controls,
        'threats': threats,
        'mappings': {
            'control_mitigates_threat': mappings['control_mitigates_threat'],
            'threat_related_to_threat': mappings['threat_related_to_threat'],
            'threat_addresses_requirement': mappings['threat_addresses_requirement']
        }
    }

    return data

def main():
    """Main build function."""
    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # File paths
    threats_file = project_root / 'data' / 'threats.json'
    controls_file = project_root / 'data' / 'controls.json'
    mappings_file = project_root / 'data' / 'mappings.json'
    reg_descriptions_file = project_root / 'data' / 'regulatory-descriptions.json'
    output_file = project_root / 'docs' / 'explorer' / 'explorer-data.json'

    print(f"Loading source data...")
    threats = load_json(threats_file)
    controls = load_json(controls_file)
    mappings = load_json(mappings_file)
    reg_descriptions = load_json(reg_descriptions_file) if reg_descriptions_file.exists() else {}

    print(f"Building explorer data structure...")
    explorer_data = build_explorer_data(threats, controls, mappings, reg_descriptions)

    # Count total articles
    total_articles = sum(len(arts) for arts in explorer_data['regulations'].values())

    print(f"Writing output to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(explorer_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Explorer data generated successfully")
    print(f"  Regulations: {len(explorer_data['regulations'])} ({', '.join(explorer_data['regulations'].keys())})")
    print(f"  Articles: {total_articles} total")
    print(f"  Controls: {len(explorer_data['controls'])}")
    print(f"  Threats: {len(explorer_data['threats'])}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
