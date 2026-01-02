// Chat application logic
class ChatApp {
    constructor() {
        this.form = document.getElementById('chat-form');
        this.input = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.messagesContainer = document.getElementById('chat-messages');
        this.status = document.getElementById('status');
        
        this.init();
    }
    
    init() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const userInput = this.input.value.trim();
        if (!userInput) return;
        
        // Display user message
        this.addMessage(userInput, 'user');
        
        // Clear input
        this.input.value = '';
        
        // Disable send button
        this.sendBtn.disabled = true;
        
        // Show loading status
        this.showStatus('Processing your request...', 'loading');
        
        try {
            // Send request to API
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ input: userInput })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
            // Display assistant response
            if (data.success) {
                this.addMessage(data.response, 'assistant', data.agent);
                this.showStatus('Request completed successfully', 'success');
            } else {
                this.addMessage(`Error: ${data.error || 'Unknown error occurred'}`, 'assistant');
                this.showStatus('An error occurred', 'error');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('Sorry, there was an error processing your request.', 'assistant');
            this.showStatus('Connection error', 'error');
        } finally {
            // Re-enable send button
            this.sendBtn.disabled = false;
            
            // Hide status after 3 seconds
            setTimeout(() => this.hideStatus(), 3000);
        }
    }
    
    addMessage(text, sender, agent = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const label = sender === 'user' ? 'You' : 'Assistant';
        const agentInfo = agent ? ` (${agent.replace('_', ' ')})` : '';
        
        messageDiv.innerHTML = `
            <strong>${label}${agentInfo}:</strong>
            ${this.escapeHtml(text)}
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    showStatus(message, type) {
        this.status.textContent = message;
        this.status.className = `status show ${type}`;
    }
    
    hideStatus() {
        this.status.className = 'status';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});