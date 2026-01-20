import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from backend.config import settings
import os

class VectorStore:
    """Service for vector database operations using ChromaDB"""
    
    def __init__(self, collection_name: str = "ai_projects"):
        # Ensure directory exists
        os.makedirs(settings.vector_db_path, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.vector_db_path,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.collection_name = collection_name
        self.collection = None
        
    def create_collection(self):
        """Create or get collection"""
        try:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "AI project case studies for RAG"}
            )
            print(f"✅ Collection '{self.collection_name}' ready")
        except Exception as e:
            print(f"❌ Collection creation failed: {e}")
            raise
    
    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ):
        """
        Add documents with embeddings to vector store
        
        Args:
            documents: Text content
            embeddings: Embedding vectors
            metadatas: Metadata for each document
            ids: Unique IDs for documents
        """
        try:
            if not self.collection:
                self.create_collection()
                
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Added {len(documents)} documents to vector store")
            
        except Exception as e:
            print(f"❌ Adding documents failed: {e}")
            raise
    
    def query(
        self,
        query_embedding: List[float],
        top_k: int = None
    ) -> Dict[str, Any]:
        """
        Query vector store for similar documents
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            
        Returns:
            Dictionary with documents, metadatas, and distances
        """
        try:
            if not self.collection:
                self.create_collection()
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k or settings.retrieval_top_k
            )
            
            return results
            
        except Exception as e:
            print(f"❌ Query failed: {e}")
            raise
    
    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        try:
            if not self.collection:
                self.create_collection()
            return self.collection.count()
        except Exception as e:
            print(f"❌ Count retrieval failed: {e}")
            return 0
    
    def reset_collection(self):
        """Delete and recreate collection (use with caution)"""
        try:
            self.client.delete_collection(name=self.collection_name)
            print(f"✅ Collection '{self.collection_name}' reset")
            self.create_collection()
        except Exception as e:
            print(f"❌ Reset failed: {e}")
            raise