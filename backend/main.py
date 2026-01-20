import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import chat_router
from backend.config import settings, validate_config
import uvicorn

# Validate configuration on startup
try:
    validate_config()
except ValueError as e:
    print(f"⚠️  Configuration Error: {e}")
    print("Please check your .env file and ensure all required credentials are set.")
    exit(1)

# Create FastAPI app
app = FastAPI(
    title="AI Project Requirement Analyzer",
    description="LLM-powered chatbot for analyzing and structuring AI project requirements using RAG",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Project Requirement Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    print("🚀 Starting AI Requirement Analyzer API...")
    print(f"📍 Environment: {settings.environment}")
    print(f"🔗 API will be available at: http://{settings.api_host}:{settings.api_port}")
    print(f"📚 Documentation: http://{settings.api_host}:{settings.api_port}/docs")
    
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development"
    )