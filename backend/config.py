import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME', 'gpt-3.5-turbo')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    
    @classmethod
    def validate_config(cls):
        """Validate that required environment variables are set"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Set environment variables for crewai
        os.environ['OPENAI_API_KEY'] = cls.OPENAI_API_KEY
        os.environ['OPENAI_MODEL_NAME'] = cls.OPENAI_MODEL_NAME
        
        if cls.SERPER_API_KEY:
            os.environ['SERPER_API_KEY'] = cls.SERPER_API_KEY