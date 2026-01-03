"""
Personal Assistant - Main Application Entry Point
Run this file from the project root directory
"""
from flask import Flask, render_template, request, jsonify
from controllers.assistant_controller import AssistantController
from config.config import Config

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.config.from_object(Config)

# Initialize controller
assistant = AssistantController()


@app.route('/')
def index():
    """Render the main page"""
    agent_info = assistant.get_agent_info()
    return render_template('index.html', agents=agent_info)


@app.route('/api/process', methods=['POST'])
def process():
    """API endpoint to process user requests"""
    data = request.get_json()
    user_input = data.get('input', '')
    session_id = data.get('session_id', 'default')  # Get session ID from client
    
    result = assistant.process_request(user_input, session_id)
    
    return jsonify(result)


@app.route('/api/clear', methods=['POST'])
def clear():
    """API endpoint to clear conversation history"""
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    
    assistant.clear_conversation(session_id)
    
    return jsonify({"status": "cleared"})


@app.route('/api/agents', methods=['GET'])
def get_agents():
    """API endpoint to get available agents"""
    return jsonify(assistant.get_agent_info())


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    print("=" * 60)
    print("Personal Assistant Server Starting...")
    print("=" * 60)
    print(f"Server running on: http://localhost:5000")
    print(f"Debug mode: {Config.DEBUG}")
    print("=" * 60)
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)