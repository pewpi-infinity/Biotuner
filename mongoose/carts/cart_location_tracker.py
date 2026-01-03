#!/usr/bin/env python3
"""
Cart Location Tracker Module
Tracks user gestures (tap, slide) and generates movement tokens
"""

import json
import math
from datetime import datetime


def track_tap_event(x, y, force=1.0, user='anonymous'):
    """
    Track a tap event
    
    Args:
        x: X coordinate
        y: Y coordinate
        force: Tap force (0.0 - 1.0)
        user: Username
    
    Returns:
        dict: Tap event record
    """
    event = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'type': 'tap',
        'user': user,
        'coordinates': {'x': x, 'y': y},
        'force': force,
        'token_value': calculate_tap_value(force)
    }
    
    return event


def track_slide_event(start_x, start_y, end_x, end_y, duration=1.0, user='anonymous'):
    """
    Track a slide/swipe event
    
    Args:
        start_x: Starting X coordinate
        start_y: Starting Y coordinate
        end_x: Ending X coordinate
        end_y: Ending Y coordinate
        duration: Slide duration in seconds
        user: Username
    
    Returns:
        dict: Slide event record
    """
    distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
    velocity = distance / max(duration, 0.01)
    
    event = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'type': 'slide',
        'user': user,
        'start': {'x': start_x, 'y': start_y},
        'end': {'x': end_x, 'y': end_y},
        'distance': distance,
        'duration': duration,
        'velocity': velocity,
        'token_value': calculate_slide_value(distance, velocity)
    }
    
    return event


def calculate_tap_value(force):
    """
    Calculate token value from tap force
    
    Args:
        force: Tap force (0.0 - 1.0)
    
    Returns:
        float: Token value in dollars
    """
    # Base value for taps: $1 - $100
    base_value = 1.0
    multiplier = 1 + (force * 99)  # 1x to 100x
    return base_value * multiplier


def calculate_slide_value(distance, velocity):
    """
    Calculate token value from slide characteristics
    
    Args:
        distance: Slide distance in pixels
        velocity: Slide velocity in pixels/second
    
    Returns:
        float: Token value in dollars
    """
    # Base value for slides: $10 - $1000
    base_value = 10.0
    distance_factor = min(distance / 100, 10)  # Up to 10x
    velocity_factor = min(velocity / 100, 10)  # Up to 10x
    multiplier = 1 + distance_factor + velocity_factor
    return base_value * multiplier


def track_location_change(lat, lon, altitude=0, user='anonymous'):
    """
    Track physical location change
    
    Args:
        lat: Latitude
        lon: Longitude
        altitude: Altitude in meters
        user: Username
    
    Returns:
        dict: Location record
    """
    location = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'type': 'location',
        'user': user,
        'coordinates': {
            'latitude': lat,
            'longitude': lon,
            'altitude': altitude
        },
        'token_value': 5.0  # Base value for location tracking
    }
    
    return location


def calculate_movement_token(events):
    """
    Generate a movement token from multiple events
    
    Args:
        events: List of tracked events
    
    Returns:
        dict: Movement token
    """
    if not events:
        return {'error': 'No events provided'}
    
    total_value = sum(e.get('token_value', 0) for e in events)
    
    # Calculate movement patterns
    tap_count = sum(1 for e in events if e.get('type') == 'tap')
    slide_count = sum(1 for e in events if e.get('type') == 'slide')
    location_count = sum(1 for e in events if e.get('type') == 'location')
    
    # Generate hash from events
    event_string = ''.join(str(e.get('timestamp', '')) for e in events)
    token_hash = format(abs(hash(event_string)), '064x')[:64]
    
    token = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'type': 'movement_token',
        'hash': token_hash,
        'event_count': len(events),
        'pattern': {
            'taps': tap_count,
            'slides': slide_count,
            'locations': location_count
        },
        'total_value': total_value,
        'value_formatted': f"${total_value:.2f}",
        'events': events
    }
    
    return token


def analyze_gesture_pattern(events):
    """
    Analyze gesture patterns for insights
    
    Args:
        events: List of gesture events
    
    Returns:
        dict: Pattern analysis
    """
    if not events:
        return {'error': 'No events to analyze'}
    
    analysis = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'event_count': len(events),
        'patterns': {}
    }
    
    # Temporal patterns
    timestamps = [e.get('timestamp', '') for e in events]
    if len(timestamps) > 1:
        analysis['patterns']['temporal'] = {
            'first_event': timestamps[0],
            'last_event': timestamps[-1],
            'span': 'calculated_from_timestamps'
        }
    
    # Spatial patterns
    taps = [e for e in events if e.get('type') == 'tap']
    if taps:
        x_coords = [t['coordinates']['x'] for t in taps]
        y_coords = [t['coordinates']['y'] for t in taps]
        analysis['patterns']['spatial'] = {
            'center_x': sum(x_coords) / len(x_coords),
            'center_y': sum(y_coords) / len(y_coords),
            'spread': max(x_coords) - min(x_coords)
        }
    
    # Velocity patterns
    slides = [e for e in events if e.get('type') == 'slide']
    if slides:
        velocities = [s['velocity'] for s in slides]
        analysis['patterns']['velocity'] = {
            'avg': sum(velocities) / len(velocities),
            'max': max(velocities),
            'min': min(velocities)
        }
    
    return analysis


def main():
    """Main entry point for standalone execution"""
    # Demo tracking
    events = [
        track_tap_event(100, 200, force=0.8, user='demo'),
        track_slide_event(100, 200, 300, 400, duration=0.5, user='demo'),
        track_tap_event(300, 400, force=0.6, user='demo')
    ]
    
    token = calculate_movement_token(events)
    analysis = analyze_gesture_pattern(events)
    
    print("Movement Token:")
    print(json.dumps(token, indent=2))
    print("\nPattern Analysis:")
    print(json.dumps(analysis, indent=2))


if __name__ == '__main__':
    main()
