#!/usr/bin/env python3
"""
Cart Signal Generator Module
Generates Biotuner tricorder signals based on token values and memory patterns
"""

import json
import math
import random
from datetime import datetime


def generate_frequency_from_value(value):
    """
    Generate frequency from token value
    
    Args:
        value: Token value in dollars
    
    Returns:
        float: Frequency in Hz
    """
    # Map value to frequency range (40 Hz - 40000 Hz)
    # Using logarithmic scaling for better distribution
    if value <= 0:
        return 40.0
    
    log_value = math.log10(max(value, 1))
    frequency = 40 * math.pow(10, log_value / 10)
    
    return min(max(frequency, 40), 40000)


def generate_quantum_tuned_signal(token_hash, value):
    """
    Generate quantum-tuned signal parameters
    
    Args:
        token_hash: Hash of the token
        value: Token value
    
    Returns:
        dict: Signal parameters
    """
    # Extract numeric components from hash
    try:
        hash_int = int(token_hash[:16], 16) if token_hash else random.randint(0, 2**64-1)
    except ValueError:
        # If hash is not valid hex, generate from string
        hash_int = abs(hash(token_hash)) if token_hash else random.randint(0, 2**64-1)
    
    # Base frequency from value
    base_freq = generate_frequency_from_value(value)
    
    # Harmonic frequencies based on hash
    harmonics = []
    for i in range(1, 6):
        harmonic_freq = base_freq * i
        harmonic_amplitude = 1.0 / i
        harmonics.append({
            'frequency': harmonic_freq,
            'amplitude': harmonic_amplitude,
            'phase': (hash_int >> (i * 8)) & 0xFF
        })
    
    # Quantum tuning parameters
    quantum_params = {
        'coherence': (hash_int & 0xFFFF) / 0xFFFF,
        'entanglement_factor': ((hash_int >> 16) & 0xFFFF) / 0xFFFF,
        'resonance_mode': (hash_int >> 32) & 0xFF
    }
    
    signal = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'token_hash': token_hash,
        'token_value': value,
        'base_frequency': base_freq,
        'harmonics': harmonics,
        'quantum_tuning': quantum_params,
        'waveform': 'sine',
        'duration': 1.0  # seconds
    }
    
    return signal


def generate_biotuner_sweep(start_value, end_value, steps=10):
    """
    Generate a sweep of frequencies across value range
    
    Args:
        start_value: Starting token value
        end_value: Ending token value
        steps: Number of steps in sweep
    
    Returns:
        dict: Sweep parameters
    """
    sweep = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'start_value': start_value,
        'end_value': end_value,
        'steps': steps,
        'frequencies': []
    }
    
    if steps <= 1:
        steps = 2
    
    for i in range(steps):
        value = start_value + (end_value - start_value) * i / (steps - 1)
        freq = generate_frequency_from_value(value)
        sweep['frequencies'].append({
            'step': i,
            'value': value,
            'frequency': freq
        })
    
    return sweep


def generate_signal_from_memory_pattern(pattern_text):
    """
    Generate signal based on memory pattern characteristics
    
    Args:
        pattern_text: Text pattern from memory
    
    Returns:
        dict: Signal parameters
    """
    # Analyze pattern characteristics
    char_count = len(pattern_text)
    word_count = len(pattern_text.split())
    vowel_count = sum(1 for c in pattern_text.lower() if c in 'aeiou')
    
    # Generate base frequency from text characteristics
    base_value = char_count * 10 + word_count * 100 + vowel_count * 50
    base_freq = generate_frequency_from_value(base_value)
    
    # Modulation based on text rhythm
    words = pattern_text.split()
    word_lengths = [len(w) for w in words[:10]]  # First 10 words
    
    signal = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'pattern_source': 'memory',
        'base_frequency': base_freq,
        'modulation': {
            'type': 'amplitude',
            'pattern': word_lengths,
            'rate': len(word_lengths) / 10.0  # Hz
        },
        'characteristics': {
            'char_count': char_count,
            'word_count': word_count,
            'vowel_density': vowel_count / max(char_count, 1)
        }
    }
    
    return signal


def generate_composite_signal(signals):
    """
    Combine multiple signals into composite
    
    Args:
        signals: List of signal dictionaries
    
    Returns:
        dict: Composite signal parameters
    """
    if not signals:
        return {'error': 'No signals provided'}
    
    frequencies = [s.get('base_frequency', 440) for s in signals]
    avg_freq = sum(frequencies) / len(frequencies)
    
    composite = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'type': 'composite',
        'component_count': len(signals),
        'average_frequency': avg_freq,
        'frequency_range': [min(frequencies), max(frequencies)],
        'components': signals
    }
    
    return composite


def main():
    """Main entry point for standalone execution"""
    import sys
    
    if len(sys.argv) > 2:
        # Generate signal from value
        token_hash = sys.argv[1]
        value = float(sys.argv[2])
        signal = generate_quantum_tuned_signal(token_hash, value)
    else:
        # Generate demo signal
        signal = generate_quantum_tuned_signal('0' * 64, 18160000000)  # $18.16B
    
    print(json.dumps(signal, indent=2))


if __name__ == '__main__':
    main()
