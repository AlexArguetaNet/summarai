from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_api_key():
    return os.getenv("API_KEY")

def get_cors_origins():
    return os.getenv("CORS_ORIGINS")