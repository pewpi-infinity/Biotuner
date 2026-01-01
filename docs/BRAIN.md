# brain.py Documentation

## Overview

`brain.py` is a self-evolving text processing module that pulls content from Project Gutenberg and categorizes it into thematic blocks. The script grows by appending categorized content to itself, creating a living document that expands with each execution.

## Features

- **Dynamic Content Fetching**: Retrieves random texts from Project Gutenberg
- **Category-Based Sorting**: Classifies sentences into predefined categories
- **Self-Appending Growth**: Automatically appends categorized content as comments
- **Text Processing**: Advanced sentence splitting and filtering

## Categories

The module organizes content into four thematic categories:

1. **CATS**: Content related to cats, kittens, and felines
2. **WATER**: Content about water, rivers, lakes, and oceans
3. **TREES**: Content featuring trees, forests, wood, oak, and pine
4. **PEOPLE**: Content about people, men, women, persons, and children

## Dependencies

- `os`: File system operations
- `requests`: HTTP requests to Project Gutenberg
- `random`: Random selection of books
- `re`: Regular expression-based text splitting

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

Run the script to fetch and categorize content:

```bash
python3 brain.py
```

Each execution:
1. Selects a random book from Project Gutenberg (ID range: 1-70000)
2. Downloads the book text
3. Splits text into sentences
4. Categorizes sentences by theme
5. Appends categorized content to the end of brain.py

## Configuration

Key configuration constants:

- `SELF`: The script filename ("brain.py")
- `URL`: Project Gutenberg URL template
- `RANGE`: Book ID range for random selection (1-70000)
- `CATS`: Category definitions with keyword lists

## Functions

### `pull()`
Fetches a random book from Project Gutenberg.

**Returns**: 
- Book text string if successful
- `None` if request fails or book is too short

### `split(t)`
Splits text into sentences using punctuation markers.

**Parameters**:
- `t`: Text string to split

**Returns**: 
- List of sentence strings

### `sort(sent)`
Categorizes sentences into thematic groups.

**Parameters**:
- `sent`: List of sentences

**Returns**: 
- Dictionary with category names as keys and sentence lists as values

### `grow(data)`
Appends categorized content to the script file.

**Parameters**:
- `data`: Dictionary of categorized sentences

**Side Effects**: 
- Appends new content block to brain.py

### `main()`
Main execution flow coordinating all operations.

## Integration with Biotuner

`brain.py` is integrated into the Biotuner ecosystem as a content generation and processing module. It complements the Mongoose OS API functionality by providing dynamic text processing capabilities.

## Historical Context

This module was introduced in commit `47208c41796342c530e70677c7962f297d5bf72d` and represents the first expansion phase of the Biotuner system. It demonstrates the concept of self-modifying code that grows organically through operation.

## Important Notes

### Current State
The `brain.py` file currently contains accumulated content blocks from previous executions. Due to multiline text in the appended blocks, **the file is not currently executable as a Python module**. This is part of its experimental self-evolving design.

### Known Behavior
- The script modifies itself by appending content
- Content is added as Python comments (prefixed with `#`)
- Each execution adds a new `#====BLOCK====` section
- Maximum 50 sentences per category per execution
- 10-second timeout for HTTP requests
- Graceful failure handling for network errors

### Technical Limitation
The `grow()` function writes sentences that may contain newlines, but only prefixes the first line with `#`. This causes continuation lines to be unprefixed, which makes the file non-executable after content accumulation. This is a known characteristic of the historical implementation and represents the experimental nature of self-modifying code.

### To Use Fresh
If you need an executable version:
1. Extract lines 1-52 (the core functions)
2. Save to a new file
3. Run the new file to generate fresh content

The historical version with accumulated content is preserved for documentation and archaeological purposes.
