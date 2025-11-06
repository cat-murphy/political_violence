#!/usr/bin/env python3
"""
Test the updated classification script with PROPERTY DESTRUCTION attack type.
"""

import sys
import os
sys.path.append('/workspaces/political_violence')

from classification_script import (
    ATTACK_TYPE_LIST, load_csv_data, create_classification_prompt
)

def main():
    """Test the updated attack type list includes PROPERTY DESTRUCTION."""
    print("Testing updated classification script with PROPERTY DESTRUCTION...")
    
    # Check that PROPERTY DESTRUCTION is in the attack type list
    attack_types = [item["attack_type"] for item in ATTACK_TYPE_LIST]
    print(f"Attack types: {attack_types}")
    
    if "PROPERTY DESTRUCTION" in attack_types:
        print("✓ PROPERTY DESTRUCTION successfully added to attack types")
    else:
        print("✗ PROPERTY DESTRUCTION missing from attack types")
        return
    
    # Check the total number of attack types (should be 7 now)
    if len(attack_types) == 7:
        print("✓ Correct number of attack types (7)")
    else:
        print(f"✗ Expected 7 attack types, got {len(attack_types)}")
        return
    
    # Verify OTHER is still last
    if attack_types[-1] == "OTHER":
        print("✓ OTHER is correctly positioned as last attack type")
    else:
        print(f"✗ OTHER should be last, but got: {attack_types[-1]}")
    
    # Test loading data
    try:
        events = load_csv_data('us_data_filtered.csv')
        print(f"✓ Successfully loaded {len(events)} events")
    except Exception as e:
        print(f"✗ Error loading events: {e}")
        return
    
    print("\n✓ All updates successfully applied!")
    print("✓ Script ready to run with PROPERTY DESTRUCTION attack type")

if __name__ == "__main__":
    main()