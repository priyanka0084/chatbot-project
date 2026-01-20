from typing import List
from chromadb.utils import embedding_functions

class EmbeddingService:
    """Service for generating embeddings using ChromaDB's built-in models"""
    
    def __init__(self):
        print("✅ Using ChromaDB default embedding function (no download needed)")
        # Use ChromaDB's default sentence transformer (already included)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            text = text.replace("\n", " ").strip()
            # ChromaDB's function returns list of embeddings
            embedding = self.embedding_function([text])[0]
            return embedding
            
        except Exception as e:
            print(f"❌ Embedding generation failed: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            texts = [text.replace("\n", " ").strip() for text in texts]
            print(f"   Generating embeddings for {len(texts)} documents...")
            embeddings = self.embedding_function(texts)
            return embeddings
            
        except Exception as e:
            print(f"❌ Batch embedding generation failed: {e}")
            raise