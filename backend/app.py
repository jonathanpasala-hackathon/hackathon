from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from controllers.assistant_controller import AssistantController
from tools.data_display_tool import DataDisplayTool
from config.config import Config
import json

app = Flask(__name__)
CORS(app)

# Initialize the assistant controller
assistant = AssistantController()


@app.route('/')
def index():
    """Render the main chat interface"""
    # Get agent information to pass to template
    agents = assistant.get_agent_info()
    return render_template('index.html', agents=agents)


@app.route('/api/process', methods=['POST'])
def process():
    """API endpoint to process user requests"""
    data = request.get_json()
    
    # DEBUG: Print incoming request
    print("\n" + "="*60)
    print("🔍 INCOMING REQUEST")
    print("="*60)
    print(f"Raw JSON: {json.dumps(data, indent=2)}")
    print(f"User Input: {data.get('input', '')}")
    print(f"Session ID: {data.get('session_id', 'default')}")
    print("="*60 + "\n")
    
    user_input = data.get('input', '')
    session_id = data.get('session_id', 'default')
    
    result = assistant.process_request(user_input, session_id)
    
    # Check if there's display data to send
    display_data = DataDisplayTool.get_display_data(session_id)
    if display_data:
        result['display_data'] = display_data
        # Clear after sending so it's only sent once
        DataDisplayTool.clear_display_data(session_id)
    
    # DEBUG: Print outgoing response
    print("\n" + "="*60)
    print("📤 OUTGOING RESPONSE")
    print("="*60)
    print(f"Success: {result.get('success')}")
    print(f"Agent: {result.get('agent')}")
    print(f"Response: {result.get('response')[:100]}..." if len(result.get('response', '')) > 100 else f"Response: {result.get('response')}") # type: ignore
    if 'display_data' in result:
        print(f"Display Data Type: {result['display_data'].get('type')}")
        print(f"Display Data Count: {len(result['display_data'].get('data', []))} items")
    print(f"Full JSON: {json.dumps(result, indent=2)}")
    print("="*60 + "\n")
    
    return jsonify(result)


@app.route('/api/clear', methods=['POST'])
def clear():
    """API endpoint to clear conversation history"""
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    
    assistant.clear_conversation(session_id)
    DataDisplayTool.clear_display_data(session_id)
    
    return jsonify({"status": "cleared"})


@app.route('/api/display-data', methods=['GET'])
def get_display_data():
    """API endpoint to get current display data"""
    session_id = request.args.get('session_id', 'default')
    
    display_data = DataDisplayTool.get_display_data(session_id)
    
    return jsonify(display_data if display_data else {"type": None, "data": []})


@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get information about available agents"""
    return jsonify(assistant.get_agent_info())


if __name__ == '__main__':
    print("=" * 60)
    print("AI Travel Assistant Server Starting...")
    print("=" * 60)
    print(f"Server running on: http://localhost:5000")
    print(f"Debug mode: {Config.DEBUG}")
    print("=" * 60)
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)