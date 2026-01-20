import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Groq API
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "llama3-70b-8192")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Application
    environment: str = os.getenv("ENVIRONMENT", "development")
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./data/chroma_db")
    data_file_path: str = os.getenv("DATA_FILE_PATH", "./data/sample_ai_projects.json")
    
    # API
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # RAG Parameters
    retrieval_top_k: int = 3
    max_tokens: int = 1500
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

def validate_config():
    """Validate required configuration"""
    if not settings.groq_api_key:
        raise ValueError("Missing GROQ_API_KEY in .env file")
    print("✅ Configuration validated successfully")

if __name__ == "__main__":
    validate_config()