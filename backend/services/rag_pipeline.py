from typing import List, Dict, Any
from backend.services.embedding_service import EmbeddingService
from backend.services.llm_service import LLMService
from backend.services.vector_store import VectorStore
from backend.utils.prompts import get_system_prompt, format_retrieved_context
from backend.models import SimilarProject

class RAGPipeline:
    """Orchestrates the complete RAG workflow"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()
        self.vector_store = VectorStore()
        self.vector_store.create_collection()
        
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Execute complete RAG pipeline
        
        Args:
            user_query: User's question
            
        Returns:
            Dictionary with response and similar projects
        """
        try:
            # Step 1: Generate query embedding
            query_embedding = self.embedding_service.generate_embedding(user_query)
            
            # Step 2: Retrieve similar projects
            results = self.vector_store.query(query_embedding)
            
            # Step 3: Format context
            context, similar_projects = self._format_results(results)
            
            # Step 4: Generate LLM response
            system_prompt = get_system_prompt()
            response = self.llm_service.generate_response(
                system_prompt=system_prompt,
                user_message=user_query,
                context=context
            )
            
            return {
                "response": response,
                "similar_projects": similar_projects,
                "num_retrieved": len(similar_projects)
            }
            
        except Exception as e:
            print(f"❌ RAG pipeline failed: {e}")
            raise
    
    def _format_results(self, results: Dict[str, Any]) -> tuple[str, List[SimilarProject]]:
        """
        Format retrieval results for LLM context
        
        Args:
            results: ChromaDB query results
            
        Returns:
            Tuple of (formatted_context, similar_projects_list)
        """
        if not results['documents'][0]:
            return "", []
        
        similar_projects = []
        context_parts = []
        
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            # Convert distance to similarity (1 - normalized distance)
            similarity = max(0, 1 - distance)
            
            similar_project = SimilarProject(
                problem_description=metadata.get('problem', ''),
                ai_approach=metadata.get('approach', ''),
                tech_stack=metadata.get('tech_stack', ''),
                outcome=metadata.get('outcome', ''),
                similarity_score=round(similarity, 3)
            )
            similar_projects.append(similar_project)
            
            # Format for LLM context
            context_parts.append(
                f"--- Similar Project {i+1} (Relevance: {similarity:.2%}) ---\n"
                f"Problem: {metadata.get('problem', '')}\n"
                f"AI Approach: {metadata.get('approach', '')}\n"
                f"Tech Stack: {metadata.get('tech_stack', '')}\n"
                f"Outcome: {metadata.get('outcome', '')}\n"
            )
        
        context = "\n".join(context_parts)
        return context, similar_projects
    
    def health_check(self) -> Dict[str, Any]:
        """Check if all components are working"""
        try:
            count = self.vector_store.get_collection_count()
            return {
                "vector_db": "healthy",
                "document_count": count,
                "embedding_service": "healthy",
                "llm_service": "healthy"
            }
        except Exception as e:
            return {
                "vector_db": "unhealthy",
                "error": str(e)
            }
