from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """Incoming chat message from user"""
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None
    
class SimilarProject(BaseModel):
    """Retrieved similar project from vector store"""
    problem_description: str
    ai_approach: str
    tech_stack: str
    outcome: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)

class ChatResponse(BaseModel):
    """Response sent back to user"""
    response: str
    similar_projects: List[SimilarProject] = []
    session_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    confidence: Optional[float] = None

class ProjectCase(BaseModel):
    """Structure of a project case in dataset"""
    problem_description: str
    ai_approach: str
    tech_stack: str
    outcome: str

class EmbeddingRequest(BaseModel):
    """Request for embedding generation"""
    text: str
    
class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    vector_db_status: str
    azure_status: str