# Biotuner

A self-evolving AI-powered text processing and content generation system with Mongoose OS integration.

## Overview

Biotuner is an experimental project that combines:
- Dynamic text processing from Project Gutenberg
- Self-modifying code that grows organically
- Mongoose OS API/AI integration for monitoring and intelligence
- Token-based value tracking system
- Visualization capabilities

## Core Components

### brain.py
A self-evolving text processing module that:
- Fetches random texts from Project Gutenberg
- Categorizes sentences into thematic groups (CATS, WATER, TREES, PEOPLE)
- Grows by appending categorized content to itself
- Demonstrates self-modifying code principles

See [docs/BRAIN.md](docs/BRAIN.md) for detailed documentation.

### Mongoose OS Integration
Provides API and AI functionality with:
- Operator attachment and identification
- Passive/Active operating modes
- System monitoring capabilities
- Integration points across all modules

See [docs/MONGOOSE.md](docs/MONGOOSE.md) for detailed documentation.

### Token System
Located in `/token/` directory:
- Token management and tracking
- Value indexing in `index_value.json`
- Settlement data in `/ledger/`
- Pricing information in `c13b0_pricing.json`

### Visualization
- `index.html` - Main visualization interface
- `index_2.html` - Secondary interface
- `visualizer.js` - Visualization logic
- Real-time data display and monitoring

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pewpi-infinity/Biotuner.git
cd Biotuner
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running brain.py
Execute the text processing module:
```bash
python3 brain.py
```

Each execution fetches new content and appends it to the script file.

### Viewing Visualizations
Open `index.html` in a web browser to view the visualization interface.

### Checking Mongoose Status
View the Mongoose OS configuration:
```bash
cat mongoose/mongoose.json
```

## Project Structure

```
Biotuner/
├── brain.py              # Self-evolving text processor
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── mongoose/
│   └── mongoose.json    # Mongoose OS configuration
├── docs/
│   ├── BRAIN.md        # brain.py documentation
│   ├── MONGOOSE.md     # Mongoose OS documentation
│   └── index.html      # Documentation viewer
├── token/
│   └── TOKEN.md        # Token system documentation
├── ledger/
│   └── 20251220.md     # Settlement ledger
├── index.html          # Main visualization
├── index_2.html        # Secondary interface
├── index_value.json    # Value tracking data
├── visualizer.js       # Visualization logic
└── c13b0_pricing.json  # Pricing configuration
```

## Historical Context

This project integrates functionality from multiple phases:
- **Nov 14, 2025**: brain.py first expansion (commit 47208c4)
- **Dec 25, 2025**: Mongoose OS spine attachment (commit ae2afa5)
- **Dec 27, 2025**: Index and chat terminal restoration

## Development Philosophy

Biotuner follows a **non-destructive growth** philosophy:
- All modifications are additions
- Existing functionality remains intact
- Self-modification through appending
- Organic evolution of capabilities

## Configuration

### Mongoose OS
Edit `mongoose/mongoose.json` to configure:
- Operator name
- Operating mode (passive/active)
- Attachment timestamp

### brain.py
Modify constants in brain.py:
- `CATS`: Category definitions
- `RANGE`: Project Gutenberg book ID range
- `URL`: Source URL template

## Contributing

This is an experimental project exploring self-modifying code and AI integration. Contributions should maintain the non-destructive growth philosophy.

## License

See repository license file for details.

## Related Projects

- Project Gutenberg: Source of text content
- Mongoose OS: Inspiration for API/AI integration patterns

---

## 🧱 Historical Research Notes

### 2025-12-23T11:00:23Z
- Repo files: 8
- Code present: 2

### 2025-12-23T19:26:19Z
- Repo files: 10
- Code present: 2
