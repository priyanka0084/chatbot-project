"""
Data ingestion script for loading project cases into vector database
Run this ONCE after setting up the project
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.data_loader import load_project_data, format_project_for_embedding, extract_metadata
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore
from backend.config import settings, validate_config

def ingest_data():
    """Main ingestion function"""
    print("=" * 60)
    print("🚀 AI Project Data Ingestion Script")
    print("=" * 60)
    
    try:
        # Step 1: Validate configuration
        print("\n📋 Step 1: Validating configuration...")
        validate_config()
        
        # Step 2: Load project data
        print("\n📂 Step 2: Loading project data...")
        projects = load_project_data()
        print(f"   Loaded {len(projects)} projects")
        
        # Step 3: Initialize services
        print("\n🔧 Step 3: Initializing services...")
        embedding_service = EmbeddingService()
        vector_store = VectorStore()
        vector_store.create_collection()
        
        # Check if collection already has data
        existing_count = vector_store.get_collection_count()
        if existing_count > 0:
            print(f"\n⚠️  Warning: Collection already contains {existing_count} documents")
            response = input("   Do you want to reset and reload? (yes/no): ")
            if response.lower() == 'yes':
                vector_store.reset_collection()
            else:
                print("   Skipping ingestion.")
                return
        
        # Step 4: Process and embed projects
        print("\n🔄 Step 4: Generating embeddings...")
        documents = []
        embeddings_list = []
        metadatas = []
        ids = []
        
        for i, project in enumerate(projects):
            # Format for embedding
            doc_text = format_project_for_embedding(project)
            documents.append(doc_text)
            
            # Generate ID
            project_id = f"proj_{i+1:03d}"
            ids.append(project_id)
            
            # Extract metadata
            metadata = extract_metadata(project, project_id)
            metadatas.append(metadata)
            
            print(f"   Processing project {i+1}/{len(projects)}...", end='\r')
        
        # Generate embeddings in batch
        print("\n   Generating embeddings (this may take a minute)...")
        embeddings_list = embedding_service.generate_embeddings_batch(documents)
        
        # Step 5: Store in vector database
        print("\n💾 Step 5: Storing in vector database...")
        vector_store.add_documents(
            documents=documents,
            embeddings=embeddings_list,
            metadatas=metadatas,
            ids=ids
        )
        
        # Step 6: Verify
        print("\n✅ Step 6: Verifying...")
        final_count = vector_store.get_collection_count()
        print(f"   Total documents in collection: {final_count}")
        
        print("\n" + "=" * 60)
        print("✅ Data ingestion completed successfully!")
        print("=" * 60)
        print("\n📌 Next steps:")
        print("   1. Start the API: python backend/main.py")
        print("   2. Open frontend: frontend/index.html")
        print("   3. Test the chatbot!")
        
    except Exception as e:
        print(f"\n❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    ingest_data()