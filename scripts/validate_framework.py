#!/usr/bin/env python3
"""
EU AI Security Mapping Framework - Validation Script

Tests internal consistency, completeness, and logical soundness of the framework.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class FrameworkValidator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.threats = {}
        self.controls = {}
        self.mappings = {}
        self.errors = []
        self.warnings = []
        self.info = []

    def load_data(self):
        """Load JSON data files"""
        print("Loading data files...")

        threats_file = self.base_path / "data" / "threats.json"
        controls_file = self.base_path / "data" / "controls.json"
        mappings_file = self.base_path / "data" / "mappings.json"

        with open(threats_file) as f:
            threats_list = json.load(f)
            self.threats = {t["id"]: t for t in threats_list}

        with open(controls_file) as f:
            controls_list = json.load(f)
            self.controls = {c["id"]: c for c in controls_list}

        with open(mappings_file) as f:
            self.mappings = json.load(f)

        print(f"  Loaded {len(self.threats)} threats")
        print(f"  Loaded {len(self.controls)} controls")
        print(f"  Loaded {len(self.mappings['control_mitigates_threat'])} control-threat mappings")
        print()

    def test_1_1_bidirectional_mapping(self):
        """Test 1.1: Verify bidirectional threat-control relationships"""
        print("Test 1.1: Bidirectional Mapping Audit")
        print("-" * 60)

        # Build threat -> controls mapping from threats.json
        threat_to_controls = {}
        for threat_id, threat in self.threats.items():
            threat_to_controls[threat_id] = set(threat.get("recommended_controls", []))

        # Build control -> threats mapping from controls.json
        control_to_threats = {}
        for control_id, control in self.controls.items():
            control_to_threats[control_id] = set()
            for threat_ref in control.get("threats_addressed", []):
                control_to_threats[control_id].add(threat_ref["threat_id"])

        # Check symmetry: if AGT-X lists CTL-Y, then CTL-Y must list AGT-X
        asymmetries = []
        for threat_id, control_ids in threat_to_controls.items():
            for control_id in control_ids:
                if control_id not in control_to_threats:
                    asymmetries.append(f"  {threat_id} -> {control_id}: Control does not exist")
                elif threat_id not in control_to_threats[control_id]:
                    asymmetries.append(f"  {threat_id} -> {control_id}: Asymmetric (control doesn't list threat)")

        # Check reverse: if CTL-Y lists AGT-X, then AGT-X should list CTL-Y
        for control_id, threat_ids in control_to_threats.items():
            for threat_id in threat_ids:
                if threat_id not in threat_to_controls:
                    asymmetries.append(f"  {control_id} -> {threat_id}: Threat does not exist")
                elif control_id not in threat_to_controls[threat_id]:
                    asymmetries.append(f"  {control_id} -> {threat_id}: Asymmetric (threat doesn't list control)")

        if asymmetries:
            self.errors.extend(asymmetries)
            print(f"FAIL: Found {len(asymmetries)} asymmetries:")
            for asym in asymmetries:
                print(asym)
        else:
            print("PASS: All threat-control relationships are symmetric")

        # Cross-reference with mappings.json
        print("\nCross-referencing with mappings.json...")
        mapping_set = set()
        for mapping in self.mappings["control_mitigates_threat"]:
            mapping_set.add((mapping["control_id"], mapping["threat_id"]))

        # Check if all mappings.json entries are in data files
        for control_id, threat_id in mapping_set:
            if control_id not in control_to_threats.get(control_id, set()):
                if threat_id not in control_to_threats.get(control_id, set()):
                    self.warnings.append(f"  Mapping {control_id} -> {threat_id} in mappings.json but not in controls.json")

        print(f"  Found {len(mapping_set)} mappings in mappings.json")
        print()

    def test_1_3_schema_consistency(self):
        """Test 1.3: Verify primary_surface values match taxonomy"""
        print("Test 1.3: Schema Consistency")
        print("-" * 60)

        # Define canonical surface names from THREAT_MODEL_FRAMEWORK.md
        canonical_surfaces = {
            "input",
            "model",
            "tool-use",
            "output",
            "memory",
            "audit"
        }

        # Check primary_surface values
        surface_inconsistencies = []
        for threat_id, threat in self.threats.items():
            primary_surface = threat.get("primary_surface")
            if primary_surface not in canonical_surfaces:
                surface_inconsistencies.append(f"  {threat_id}: Invalid primary_surface '{primary_surface}'")

        if surface_inconsistencies:
            self.errors.extend(surface_inconsistencies)
            print(f"FAIL: Found {len(surface_inconsistencies)} surface naming inconsistencies:")
            for incon in surface_inconsistencies:
                print(incon)
        else:
            print("PASS: All primary_surface values match canonical taxonomy")

        print()

    def test_2_1_attack_surface_coverage(self):
        """Test 2.1: Attack surface coverage matrix"""
        print("Test 2.1: Attack Surface Coverage Matrix")
        print("-" * 60)

        # Build surface -> threats mapping
        surface_to_threats = defaultdict(list)
        for threat_id, threat in self.threats.items():
            primary_surface = threat.get("primary_surface")
            if primary_surface:
                surface_to_threats[primary_surface].append(threat_id)

        # Display matrix
        print("\n| Surface | Threats | Count |")
        print("|---------|---------|-------|")

        canonical_surfaces = ["input", "model", "tool-use", "output", "memory", "audit"]
        for surface in canonical_surfaces:
            threats = surface_to_threats.get(surface, [])
            threats_str = ", ".join(threats) if threats else "NONE"
            print(f"| {surface:12} | {threats_str:30} | {len(threats):5} |")

            if len(threats) == 0:
                self.errors.append(f"  Surface '{surface}' has no threats")

        # Check for imbalance
        counts = [len(surface_to_threats.get(s, [])) for s in canonical_surfaces]
        max_count = max(counts)
        min_count = min(counts)
        avg_count = sum(counts) / len(counts)

        print(f"\nDistribution: min={min_count}, max={max_count}, avg={avg_count:.1f}")

        if max_count > 2 * avg_count:
            self.warnings.append(f"  Surface imbalance detected: max={max_count}, avg={avg_count:.1f}")
            print(f"WARNING: Unbalanced distribution (max > 2x average)")
        else:
            print("INFO: Distribution is reasonably balanced")

        print()

    def test_2_2_control_coverage(self):
        """Test 2.2: Control coverage matrix"""
        print("Test 2.2: Control Coverage Matrix")
        print("-" * 60)

        # Build control -> threats mapping with relationship type
        control_threat_matrix = defaultdict(lambda: {"primary": [], "secondary": []})
        for control_id, control in self.controls.items():
            for threat_ref in control.get("threats_addressed", []):
                threat_id = threat_ref["threat_id"]
                relationship = threat_ref.get("relationship", "primary")
                control_threat_matrix[control_id][relationship].append(threat_id)

        # Display matrix
        print("\n| Control | Primary Threats | Secondary Threats |")
        print("|---------|-----------------|-------------------|")

        for control_id in sorted(self.controls.keys()):
            primary = ", ".join(control_threat_matrix[control_id]["primary"])
            secondary = ", ".join(control_threat_matrix[control_id]["secondary"])
            print(f"| {control_id:7} | {primary:15} | {secondary:17} |")

        # Check for orphan threats (no control coverage)
        all_covered_threats = set()
        for control_id, relationships in control_threat_matrix.items():
            all_covered_threats.update(relationships["primary"])
            all_covered_threats.update(relationships["secondary"])

        orphan_threats = set(self.threats.keys()) - all_covered_threats
        if orphan_threats:
            self.errors.extend([f"  Orphan threat (no control): {t}" for t in orphan_threats])
            print(f"\nFAIL: Found {len(orphan_threats)} orphan threats")
        else:
            print("\nPASS: All threats have at least one control")

        # Report control_gap_flag entries
        gaps = []
        for threat_id, threat in self.threats.items():
            if "control_gap_flag" in threat and threat["control_gap_flag"]:
                gaps.append(threat_id)

        if gaps:
            self.info.append(f"  {len(gaps)} threats have control_gap_flag: {', '.join(gaps)}")
            print(f"\nINFO: {len(gaps)} of {len(self.threats)} threats have control_gap_flag")

        print()

    def test_2_3_regulatory_coverage(self):
        """Test 2.3: Regulatory requirement coverage"""
        print("Test 2.3: Regulatory Requirement Coverage")
        print("-" * 60)

        # Extract unique regulatory provisions from mappings.json
        regulations = defaultdict(set)
        for mapping in self.mappings.get("threat_addresses_requirement", []):
            regulation = mapping.get("regulation")
            article = mapping.get("article_or_section")
            if regulation and article:
                regulations[regulation].add(article)

        print("\nRegulatory provisions found:")
        for regulation, articles in sorted(regulations.items()):
            print(f"  {regulation}: {len(articles)} articles")

        # This is a simplified check; full validation would require parsing Section 4
        total_provisions = sum(len(articles) for articles in regulations.values())
        print(f"\nTotal regulatory provisions: {total_provisions}")
        print("INFO: Full coverage verification requires parsing main document Section 4")

        print()

    def run_all_tests(self):
        """Run all validation tests"""
        print("=" * 60)
        print("EU AI Security Mapping Framework Validation")
        print("=" * 60)
        print()

        self.load_data()

        self.test_1_1_bidirectional_mapping()
        self.test_1_3_schema_consistency()
        self.test_2_1_attack_surface_coverage()
        self.test_2_2_control_coverage()
        self.test_2_3_regulatory_coverage()

        # Summary
        print("=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Errors:   {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Info:     {len(self.info)}")
        print()

        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(error)
            print()

        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(warning)
            print()

        if self.info:
            print("INFO:")
            for info_msg in self.info:
                print(info_msg)
            print()

        # Exit code
        if self.errors:
            print("RESULT: FAIL")
            return 1
        elif self.warnings:
            print("RESULT: PASS WITH WARNINGS")
            return 0
        else:
            print("RESULT: PASS")
            return 0

def main():
    # Detect base path (script is in scripts/, base is parent)
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent

    validator = FrameworkValidator(base_path)
    exit_code = validator.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
