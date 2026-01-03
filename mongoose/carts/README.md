# Autonomous Cart System

The Biotuner autonomous cart system consists of specialized modules that search, analyze, generate signals, and track user interactions.

## Cart Modules

### 🔍 cart_memory_search.py
Searches through brain.py accumulated content, token hashes, and ledger entries.

**Usage:**
```bash
python3 mongoose/carts/cart_memory_search.py [query]
```

**Features:**
- Search brain.py CATS, WATER, TREES, PEOPLE blocks
- Search token hashes and values
- Search ledger entries
- Pattern matching with context

### 📡 cart_signal_generator.py
Generates Biotuner tricorder signals based on token values and memory patterns.

**Usage:**
```bash
python3 mongoose/carts/cart_signal_generator.py [token_hash] [token_value]
```

**Features:**
- Frequency generation from token values (40 Hz - 40 kHz)
- Quantum-tuned signal parameters
- Harmonic frequency generation
- Signal sweeps and composites

### 🤖 cart_robotic_builder.py
Generates code and build configurations from memory patterns.

**Usage:**
```bash
python3 mongoose/carts/cart_robotic_builder.py
```

**Features:**
- Pattern analysis from memory content
- Code generation based on detected themes
- Build configuration based on token value
- Dockerfile generation

### 📍 cart_location_tracker.py
Tracks user gestures (tap, slide) and generates movement tokens.

**Usage:**
```bash
python3 mongoose/carts/cart_location_tracker.py
```

**Features:**
- Tap event tracking with force
- Slide/swipe tracking with velocity
- Movement token generation
- Gesture pattern analysis

### 🚀 cart_runner.py
Orchestrates all carts and triggers commits with results.

**Usage:**
```bash
python3 mongoose/carts/cart_runner.py [query]
```

**Features:**
- Runs all carts in sequence
- Collects and aggregates outputs
- Logs activities to mongoose/activity_log.json
- Generates commit messages

## Running All Carts

To execute all carts autonomously:

```bash
cd /path/to/Biotuner
python3 mongoose/carts/cart_runner.py
```

With a search query:
```bash
python3 mongoose/carts/cart_runner.py "quantum"
```

## Output

All cart operations are logged to:
- `mongoose/activity_log.json` - Activity tracking
- Console output - Real-time results

## Integration with Mongoose Active Mode

When Mongoose.OS is in active mode, cart operations can trigger automatic GitHub commits through the web interface via `mongoose_active.js`.

## Architecture

```
mongoose/
├── mongoose.json           # Configuration (active/passive mode)
├── activity_log.json      # Activity tracking log
├── mongoose_active.js     # Web UI integration
└── carts/                 # Autonomous cart modules
    ├── cart_memory_search.py
    ├── cart_signal_generator.py
    ├── cart_robotic_builder.py
    ├── cart_location_tracker.py
    └── cart_runner.py
```

## Requirements

- Python 3.7+
- Standard library modules (json, math, random, datetime)

No additional dependencies required for cart operations.
