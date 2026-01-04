"""
Debug utilities for the travel assistant
"""
import json
from datetime import datetime
from typing import Any, Dict
import os


class DebugLogger:
    """Debug logger for tracking requests and responses"""
    
    def __init__(self, enabled: bool = True, log_to_file: bool = False):
        self.enabled = enabled
        self.log_to_file = log_to_file
        self.log_file = "debug_log.txt"
        
        if self.log_to_file and self.enabled:
            # Clear log file on startup
            with open(self.log_file, 'w') as f:
                f.write(f"=== Debug Log Started: {datetime.now()} ===\n\n")
    
    def log_request(self, data: Dict[str, Any], endpoint: str = "/api/process"):
        """Log incoming request"""
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
{'='*70}
🔍 INCOMING REQUEST - {endpoint}
{'='*70}
Timestamp: {timestamp}
User Input: {data.get('input', 'N/A')}
Session ID: {data.get('session_id', 'default')}

Raw JSON:
{json.dumps(data, indent=2)}
{'='*70}
"""
        
        print(message)
        
        if self.log_to_file:
            with open(self.log_file, 'a') as f:
                f.write(message + "\n")
    
    def log_response(self, result: Dict[str, Any], endpoint: str = "/api/process"):
        """Log outgoing response"""
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create summary
        summary = {
            "success": result.get('success'),
            "agent": result.get('agent'),
            "has_display_data": 'display_data' in result,
            "error": result.get('error')
        }
        
        if 'display_data' in result:
            summary['display_type'] = result['display_data'].get('type')
            summary['display_count'] = len(result['display_data'].get('data', []))
        
        # Truncate long responses for console
        response_text = result.get('response', '')
        response_preview = response_text[:200] + "..." if len(response_text) > 200 else response_text
        
        message = f"""
{'='*70}
📤 OUTGOING RESPONSE - {endpoint}
{'='*70}
Timestamp: {timestamp}

Summary:
{json.dumps(summary, indent=2)}

Response Preview:
{response_preview}

Full Response JSON:
{json.dumps(result, indent=2)}
{'='*70}
"""
        
        print(message)
        
        if self.log_to_file:
            with open(self.log_file, 'a') as f:
                f.write(message + "\n")
    
    def log_display_data(self, display_data: Dict[str, Any], session_id: str):
        """Log display data being sent to frontend"""
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data_type = display_data.get('type', 'unknown')
        data_items = display_data.get('data', [])
        
        message = f"""
{'='*70}
🎨 DISPLAY DATA - Session: {session_id}
{'='*70}
Timestamp: {timestamp}
Type: {data_type}
Item Count: {len(data_items)}

Sample Data (first item):
{json.dumps(data_items[0] if data_items else {}, indent=2)}

All Items:
{json.dumps(data_items, indent=2)}
{'='*70}
"""
        
        print(message)
        
        if self.log_to_file:
            with open(self.log_file, 'a') as f:
                f.write(message + "\n")
    
    def log_agent_execution(self, agent_name: str, input_data: str, output: str):
        """Log agent execution details"""
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
{'='*70}
🤖 AGENT EXECUTION - {agent_name}
{'='*70}
Timestamp: {timestamp}

Input:
{input_data[:300]}...

Output:
{output[:300]}...
{'='*70}
"""
        
        print(message)
        
        if self.log_to_file:
            with open(self.log_file, 'a') as f:
                f.write(message + "\n")
    
    def log_error(self, error: Exception, context: str = ""):
        """Log errors"""
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
{'='*70}
❌ ERROR - {context}
{'='*70}
Timestamp: {timestamp}
Error Type: {type(error).__name__}
Error Message: {str(error)}

Stack Trace:
{error.__traceback__ if hasattr(error, '__traceback__') else 'N/A'}
{'='*70}
"""
        
        print(message)
        
        if self.log_to_file:
            with open(self.log_file, 'a') as f:
                f.write(message + "\n")


# Global debug logger instance
debug = DebugLogger(enabled=True, log_to_file=True)


def pretty_print_json(data: Any, title: str = "JSON Data"):
    """Pretty print JSON data"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print('='*60)
    print(json.dumps(data, indent=2))
    print('='*60 + "\n")


def save_json_to_file(data: Any, filename: str = "debug_data.json"):
    """Save JSON data to file for inspection"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"💾 JSON saved to: {filename}")