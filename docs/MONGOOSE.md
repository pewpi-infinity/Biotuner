# Mongoose OS Integration Documentation

## Overview

The Mongoose OS integration provides API and AI functionality within the Biotuner ecosystem. This integration enables passive monitoring and operator attachment capabilities.

## Configuration

The Mongoose OS configuration is stored in `/mongoose/mongoose.json`:

```json
{
  "operator": "Kris Watson",
  "attached": "2025-12-25T08:20:31Z",
  "mode": "passive"
}
```

## Configuration Fields

### `operator`
- **Type**: String
- **Description**: Name of the operator attached to the Mongoose OS instance
- **Example**: "Kris Watson"

### `attached`
- **Type**: ISO 8601 Timestamp
- **Description**: Date and time when the operator was attached
- **Format**: YYYY-MM-DDTHH:MM:SSZ
- **Example**: "2025-12-25T08:20:31Z"

### `mode`
- **Type**: String
- **Description**: Operating mode of the Mongoose OS instance
- **Values**: 
  - `passive`: Monitoring mode without active intervention
  - `active`: Full operational mode with active responses
- **Default**: "passive"

## Operating Modes

### Passive Mode
In passive mode, the Mongoose OS integration:
- Monitors system activities
- Logs events and interactions
- Does not actively intervene in operations
- Collects data for analysis

### Active Mode
In active mode, the Mongoose OS integration:
- Actively responds to events
- Makes decisions based on AI processing
- Intervenes in system operations when needed
- Provides real-time intelligence

## API Integration Points

The Mongoose OS API integrates with various Biotuner components:

### 1. brain.py Integration
- Provides context for text processing
- Monitors content categorization
- Tracks self-modification events

### 2. Token System Integration
- Monitors token operations in `/token/` directory
- Tracks ledger updates in `/ledger/` directory
- Maintains pricing data in `c13b0_pricing.json`

### 3. Visualization Integration
- Supports `visualizer.js` operations
- Provides data for `index.html` displays
- Tracks value data in `index_value.json`

## Usage

### Reading Configuration

```python
import json

with open('mongoose/mongoose.json', 'r') as f:
    config = json.load(f)
    
operator = config['operator']
mode = config['mode']
attached_time = config['attached']
```

### Updating Configuration

```python
import json
from datetime import datetime

config = {
    "operator": "New Operator Name",
    "attached": datetime.utcnow().isoformat() + 'Z',
    "mode": "active"
}

with open('mongoose/mongoose.json', 'w') as f:
    json.dump(config, f, indent=2)
```

## Historical Context

The Mongoose OS integration was introduced in commit `ae2afa5ceb2296be7b3e905be3db8086fc6e92f6` with the message "🧱🧠🧱 attach mongoose spine". This represents the backbone AI/API infrastructure for the Biotuner system.

## Security Considerations

- Configuration file contains operator identification
- Timestamp tracking for audit purposes
- Mode changes should be logged
- Access control recommended for production deployments

## Future Enhancements

Potential areas for enhancement:
- Extended API endpoints
- Additional operating modes
- Event logging integration
- Real-time monitoring dashboard
- Multi-operator support
- Authentication mechanisms

## Troubleshooting

### Configuration Not Loading
- Verify `mongoose/mongoose.json` exists
- Check JSON syntax validity
- Ensure proper file permissions

### Mode Changes Not Effective
- Verify configuration file is being read correctly
- Check for caching issues
- Restart relevant services after mode changes

## Related Documentation

- [brain.py Documentation](BRAIN.md)
- [README.md](../README.md)
- Token System Documentation (see `/token/` directory)
- Ledger Documentation (see `/ledger/` directory)
