from flask import Flask, render_template, request, jsonify
from controllers.assistant_controller import AssistantController
from config.config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

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
    
    result = assistant.process_request(user_input)
    
    return jsonify(result)


@app.route('/api/agents', methods=['GET'])
def get_agents():
    """API endpoint to get available agents"""
    return jsonify(assistant.get_agent_info())


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)