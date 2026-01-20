from fastapi import APIRouter, HTTPException, status
from backend.models import ChatRequest, ChatResponse, HealthResponse
from backend.services.rag_pipeline import RAGPipeline
from datetime import datetime
import uuid

router = APIRouter(prefix="/api", tags=["chat"])

# Initialize RAG pipeline (singleton)
rag_pipeline = RAGPipeline()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user query and return AI-generated response with similar projects
    
    Args:
        request: ChatRequest with user message
        
    Returns:
        ChatResponse with generated answer and retrieved projects
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process query through RAG pipeline
        result = rag_pipeline.process_query(request.message)
        
        # Calculate confidence based on similarity scores
        if result['similar_projects']:
            avg_similarity = sum(p.similarity_score for p in result['similar_projects']) / len(result['similar_projects'])
            confidence = round(avg_similarity, 2)
        else:
            confidence = 0.0
        
        return ChatResponse(
            response=result['response'],
            similar_projects=result['similar_projects'],
            session_id=session_id,
            confidence=confidence
        )
        
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify all services are operational
    
    Returns:
        HealthResponse with service status
    """
    try:
        health = rag_pipeline.health_check()
        
        # Determine overall status
        vector_db_status = health.get('vector_db', 'unknown')
        azure_status = health.get('llm_service', 'unknown')
        
        overall_status = "healthy" if vector_db_status == "healthy" else "degraded"
        
        return HealthResponse(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat(),
            vector_db_status=vector_db_status,
            azure_status=azure_status
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )

@router.get("/stats")
async def get_stats():
    """
    Get statistics about the vector database
    
    Returns:
        Dictionary with stats
    """
    try:
        count = rag_pipeline.vector_store.get_collection_count()
        return {
            "total_projects": count,
            "collection_name": rag_pipeline.vector_store.collection_name,
            "status": "operational"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )