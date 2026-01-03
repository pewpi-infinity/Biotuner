#!/usr/bin/env python3
"""
Cart Memory Search Module
Searches brain.py accumulated content, tokens, and ledger for patterns
"""

import json
import re
import os
from datetime import datetime


def search_brain_memory(query=None):
    """
    Search brain.py accumulated content for patterns
    
    Args:
        query: Search term or pattern (optional)
    
    Returns:
        dict: Search results with matches
    """
    brain_path = 'brain.py'
    results = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'query': query,
        'matches': [],
        'stats': {}
    }
    
    if not os.path.exists(brain_path):
        results['error'] = 'brain.py not found'
        return results
    
    with open(brain_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Find accumulated blocks
    blocks = []
    current_block = []
    in_block = False
    
    for line in lines:
        if '#====BLOCK====' in line:
            if current_block:
                blocks.append('\n'.join(current_block))
                current_block = []
            in_block = True
            continue
        if in_block and line.startswith('# '):
            current_block.append(line[2:])  # Remove '# ' prefix
    
    if current_block:
        blocks.append('\n'.join(current_block))
    
    results['stats']['total_blocks'] = len(blocks)
    results['stats']['total_lines'] = len(lines)
    
    # Search for query if provided
    if query:
        for i, block in enumerate(blocks):
            if query.lower() in block.lower():
                # Extract context around matches
                lines_in_block = block.split('\n')
                for j, line in enumerate(lines_in_block):
                    if query.lower() in line.lower():
                        results['matches'].append({
                            'block_index': i,
                            'line_index': j,
                            'content': line,
                            'context': lines_in_block[max(0, j-1):min(len(lines_in_block), j+2)]
                        })
    
    # Extract category statistics
    categories = {'CATS': 0, 'WATER': 0, 'TREES': 0, 'PEOPLE': 0}
    for line in lines:
        for cat in categories:
            if f'# {cat}' in line:
                categories[cat] += 1
    
    results['stats']['categories'] = categories
    results['stats']['match_count'] = len(results['matches'])
    
    return results


def search_token_hashes(pattern=None):
    """
    Search token system for specific hashes or values
    
    Args:
        pattern: Hash pattern to search for
    
    Returns:
        dict: Token search results
    """
    results = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'pattern': pattern,
        'tokens': []
    }
    
    # Search in token directory
    token_dir = 'token'
    if os.path.exists(token_dir):
        for filename in os.listdir(token_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(token_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        results['tokens'].append({
                            'file': filename,
                            'data': data
                        })
                except (FileNotFoundError, json.JSONDecodeError, PermissionError):
                    # Skip files that can't be read
                    continue
    
    return results


def search_ledger_entries(date=None):
    """
    Search ledger for specific entries
    
    Args:
        date: Date to search for (YYYYMMDD format)
    
    Returns:
        dict: Ledger search results
    """
    results = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'date_filter': date,
        'entries': []
    }
    
    ledger_dir = 'ledger'
    if os.path.exists(ledger_dir):
        try:
            # Load ledger index
            index_path = os.path.join(ledger_dir, 'index.json')
            if os.path.exists(index_path):
                with open(index_path, 'r') as f:
                    ledger_index = json.load(f)
                    results['entries'] = ledger_index
        except (FileNotFoundError, json.JSONDecodeError) as e:
            results['error'] = f'Failed to read ledger: {e}'
    
    return results


def perform_full_search(query):
    """
    Perform comprehensive search across all systems
    
    Args:
        query: Search term
    
    Returns:
        dict: Combined search results
    """
    return {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'query': query,
        'brain_results': search_brain_memory(query),
        'token_results': search_token_hashes(query),
        'ledger_results': search_ledger_entries()
    }


def main():
    """Main entry point for standalone execution"""
    import sys
    
    query = sys.argv[1] if len(sys.argv) > 1 else None
    results = perform_full_search(query) if query else search_brain_memory()
    
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
