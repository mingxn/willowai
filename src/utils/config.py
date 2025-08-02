# """
# Configuration settings for the plant analysis application.
# """
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "GPT-4o")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    
    # ChromaDB settings
    CHROMADB_HOST = os.getenv("CHROMADB_HOST", "localhost")
    CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", "8000"))
    
    # Image processing settings
    MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", "1024"))
    SUPPORTED_FORMATS = os.getenv("SUPPORTED_FORMATS", "jpg,jpeg,png,webp").split(",")
    
    # Analysis settings
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    ENABLE_DISEASE_DETECTION = os.getenv("ENABLE_DISEASE_DETECTION", "true").lower() == "true"
    ENABLE_GROWTH_ANALYSIS = os.getenv("ENABLE_GROWTH_ANALYSIS", "true").lower() == "true"
    
    # Validation
    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file.")
        return True

# Create global config instance
config = Config()
