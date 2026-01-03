import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # Groq API Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_API_BASE = os.getenv('GROQ_API_BASE', 'https://api.groq.com/openai/v1')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Agent Configuration
    MAX_ITERATIONS = 90
    AGENT_TIMEOUT = 180  # seconds