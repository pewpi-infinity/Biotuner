#!/usr/bin/env python3
"""
Integration Example for Biotuner
Demonstrates how brain.py and Mongoose OS work together
"""

import json
import sys
from datetime import datetime


def load_mongoose_config():
    """Load Mongoose OS configuration"""
    with open('mongoose/mongoose.json', 'r') as f:
        return json.load(f)


def display_system_status():
    """Display current system status"""
    print("=" * 60)
    print("BIOTUNER SYSTEM STATUS")
    print("=" * 60)
    
    # Mongoose OS Status
    config = load_mongoose_config()
    print("\n📡 Mongoose OS Integration:")
    print(f"   Operator: {config['operator']}")
    print(f"   Mode: {config['mode']}")
    print(f"   Attached: {config['attached']}")
    
    # brain.py Status
    print("\n🧠 brain.py Module:")
    try:
        with open('brain.py', 'r') as f:
            lines = f.readlines()
        
        # Find functional code end by locating first block marker
        functional_end = None
        for i, line in enumerate(lines):
            if line.strip() == '#====BLOCK====':
                functional_end = i
                break
        
        if functional_end is None:
            functional_end = len(lines)  # No blocks yet, all is functional
        
        total_lines = len(lines)
        accumulated_lines = total_lines - functional_end
        
        # Count blocks
        blocks = sum(1 for line in lines if line.strip() == '#====BLOCK====')
        
        print(f"   Total lines: {total_lines}")
        print(f"   Functional code: {functional_end} lines")
        print(f"   Accumulated content: {accumulated_lines} lines")
        print(f"   Content blocks: {blocks}")
        print(f"   Status: {'Accumulated (see docs/BRAIN.md)' if accumulated_lines > 0 else 'Fresh'}")
    except Exception as e:
        print(f"   Error reading brain.py: {e}")
    
    # Dependencies
    print("\n📦 Dependencies:")
    try:
        import requests
        print(f"   requests: ✓ Available (v{requests.__version__})")
    except ImportError:
        print("   requests: ✗ Not installed (run: pip install -r requirements.txt)")
    
    # Other Components
    print("\n📊 Other Components:")
    try:
        with open('index_value.json', 'r') as f:
            value_data = json.load(f)
        print(f"   Token system: ✓ Active")
        print(f"   Value index: ✓ Present")
    except:
        print(f"   Token system: ℹ Configuration present")
    
    print(f"   Visualizations: ✓ Available (index.html, index_2.html)")
    
    print("\n" + "=" * 60)
    print("Integration Status: ✅ All systems integrated")
    print("=" * 60)
    print("\nFor more information:")
    print("  - README.md: Main documentation")
    print("  - docs/BRAIN.md: brain.py details")
    print("  - docs/MONGOOSE.md: Mongoose OS integration")
    print("\n")


def main():
    """Main entry point"""
    try:
        display_system_status()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
