import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_config():
    config = {
        'ANTHROPIC_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'MONGO_URI': os.getenv('MONGO_URI'),
    }
    return config