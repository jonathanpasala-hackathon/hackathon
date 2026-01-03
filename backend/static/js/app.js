// Chat application logic
class ChatApp {
    constructor() {
        this.form = document.getElementById('chat-form');
        this.input = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.messagesContainer = document.getElementById('chat-messages');
        this.status = document.getElementById('status');
        
        // Generate or retrieve session ID
        this.sessionId = this.getOrCreateSessionId();
        
        this.init();
    }
    
    getOrCreateSessionId() {
        // Check if we have a session ID in sessionStorage
        let sessionId = sessionStorage.getItem('chatSessionId');
        if (!sessionId) {
            // Create a new session ID
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('chatSessionId', sessionId);
        }
        return sessionId;
    }
    
    init() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Add clear conversation button functionality if it exists
        const clearBtn = document.getElementById('clear-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearConversation());
        }
    }
    
    async clearConversation() {
        try {
            await fetch('/api/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ session_id: this.sessionId })
            });
            
            // Clear the UI
            this.messagesContainer.innerHTML = `
                <div class="message assistant-message">
                    <strong>Assistant:</strong> Hello! How can I help you today?
                </div>
            `;
            
            this.showStatus('Conversation cleared', 'success');
            setTimeout(() => this.hideStatus(), 2000);
        } catch (error) {
            console.error('Error clearing conversation:', error);
        }
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
            // Send request to API with session ID
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    input: userInput,
                    session_id: this.sessionId
                })
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