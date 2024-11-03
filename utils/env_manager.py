# utils/env_manager.py

from dotenv import load_dotenv, set_key, unset_key
import os

def load_environment():
    load_dotenv()
    return {
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY', ''),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
        'ADMIN_PASSWORD': os.getenv('ADMIN_PASSWORD', 'admin')
    }

def save_api_key(key_name, key_value):
    if key_value:
        set_key('.env', key_name, key_value)
    else:
        unset_key('.env', key_name)

def get_env_variable(key, default=''):
    return os.getenv(key, default)
