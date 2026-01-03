#!/usr/bin/env python3
"""
Cart Runner Module
Orchestrates all autonomous carts and triggers commits with results
"""

import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    import cart_memory_search
    import cart_signal_generator
    import cart_robotic_builder
    import cart_location_tracker
except ImportError as e:
    print(f"Warning: Could not import cart modules: {e}")
    cart_memory_search = None
    cart_signal_generator = None
    cart_robotic_builder = None
    cart_location_tracker = None


class CartRunner:
    """Orchestrates all autonomous cart operations"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'run_id': self._generate_run_id(),
            'carts': {},
            'summary': {}
        }
        self.activity_log_path = 'mongoose/activity_log.json'
    
    def _generate_run_id(self):
        """Generate unique run ID"""
        return format(abs(hash(datetime.utcnow().isoformat())), '016x')
    
    def run_memory_search(self, query=None):
        """Run memory search cart"""
        if not cart_memory_search:
            return {'error': 'Module not available'}
        
        print("🔍 Running Memory Search Cart...")
        results = cart_memory_search.perform_full_search(query) if query else cart_memory_search.search_brain_memory()
        self.results['carts']['memory_search'] = {
            'status': 'completed',
            'results': results
        }
        return results
    
    def run_signal_generator(self, token_hash='demo0000', token_value=18160000000):
        """Run signal generator cart"""
        if not cart_signal_generator:
            return {'error': 'Module not available'}
        
        print("📡 Running Signal Generator Cart...")
        signal = cart_signal_generator.generate_quantum_tuned_signal(token_hash, token_value)
        self.results['carts']['signal_generator'] = {
            'status': 'completed',
            'results': signal
        }
        return signal
    
    def run_robotic_builder(self, token_hash='demo0000', token_value=18160000000):
        """Run robotic builder cart"""
        if not cart_robotic_builder:
            return {'error': 'Module not available'}
        
        print("🤖 Running Robotic Builder Cart...")
        
        # Get memory content for analysis
        memory_content = ""
        if cart_memory_search:
            memory_results = cart_memory_search.search_brain_memory()
            if 'matches' in memory_results:
                memory_content = '\n'.join([m.get('content', '') for m in memory_results['matches'][:10]])
        
        artifact = cart_robotic_builder.create_build_artifact(token_hash, token_value, memory_content)
        self.results['carts']['robotic_builder'] = {
            'status': 'completed',
            'results': artifact
        }
        return artifact
    
    def run_location_tracker(self, demo_mode=True):
        """Run location tracker cart"""
        if not cart_location_tracker:
            return {'error': 'Module not available'}
        
        print("📍 Running Location Tracker Cart...")
        
        if demo_mode:
            # Generate demo events
            events = [
                cart_location_tracker.track_tap_event(100, 200, force=0.8, user='demo'),
                cart_location_tracker.track_slide_event(100, 200, 300, 400, duration=0.5, user='demo')
            ]
            token = cart_location_tracker.calculate_movement_token(events)
        else:
            token = {'message': 'Location tracking in standby mode'}
        
        self.results['carts']['location_tracker'] = {
            'status': 'completed',
            'results': token
        }
        return token
    
    def run_all_carts(self, query=None, token_hash=None, token_value=None):
        """Run all carts in sequence"""
        print("=" * 60)
        print("🚀 CART RUNNER - Starting All Autonomous Carts")
        print("=" * 60)
        
        # Set defaults
        token_hash = token_hash or 'demo' + '0' * 60
        token_value = token_value or 18160000000
        
        # Run each cart
        self.run_memory_search(query)
        self.run_signal_generator(token_hash, token_value)
        self.run_robotic_builder(token_hash, token_value)
        self.run_location_tracker(demo_mode=True)
        
        # Generate summary
        self.results['summary'] = {
            'total_carts': len(self.results['carts']),
            'completed': sum(1 for c in self.results['carts'].values() if c.get('status') == 'completed'),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        print("\n" + "=" * 60)
        print(f"✅ All Carts Completed: {self.results['summary']['completed']}/{self.results['summary']['total_carts']}")
        print("=" * 60)
        
        return self.results
    
    def save_to_activity_log(self, action_type='cart_run', action_data=None):
        """Save cart run to activity log"""
        try:
            # Load existing log
            if os.path.exists(self.activity_log_path):
                with open(self.activity_log_path, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {
                    'activities': [],
                    'version': '1.0',
                    'created': datetime.utcnow().isoformat() + 'Z'
                }
            
            # Add new activity
            activity = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'action': action_type,
                'run_id': self.results['run_id'],
                'summary': self.results.get('summary', {}),
                'data': action_data or {}
            }
            
            log_data['activities'].append(activity)
            
            # Save back
            with open(self.activity_log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
            
            print(f"\n💾 Activity logged to {self.activity_log_path}")
            return True
        except Exception as e:
            print(f"\n⚠️ Failed to log activity: {e}")
            return False
    
    def generate_commit_message(self):
        """Generate commit message for cart run"""
        summary = self.results.get('summary', {})
        run_id = self.results.get('run_id', 'unknown')
        
        completed = summary.get('completed', 0)
        total = summary.get('total_carts', 0)
        
        # Calculate approximate value from carts
        value = 0
        if 'signal_generator' in self.results['carts']:
            sig_results = self.results['carts']['signal_generator'].get('results', {})
            value = sig_results.get('token_value', 0)
        
        value_str = f"${value/1e9:.2f}B" if value > 1e9 else f"${value:.2f}"
        
        message = f"🧱[CART_RUN]🧱 {completed}/{total} carts completed • Value: {value_str} • Run: {run_id[:8]}"
        
        return message
    
    def get_results_json(self):
        """Get results as JSON string"""
        return json.dumps(self.results, indent=2)


def main():
    """Main entry point for standalone execution"""
    runner = CartRunner()
    
    # Parse command line arguments
    query = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Run all carts
    results = runner.run_all_carts(query=query)
    
    # Save to activity log
    runner.save_to_activity_log('autonomous_cart_run')
    
    # Print results
    print("\n📊 Full Results:")
    print(runner.get_results_json())
    
    # Show commit message
    print(f"\n📝 Suggested Commit Message:")
    print(runner.generate_commit_message())


if __name__ == '__main__':
    main()
