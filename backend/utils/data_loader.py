import json
from typing import List, Dict, Any
from backend.models import ProjectCase
from backend.config import settings

def load_project_data(file_path: str = None) -> List[ProjectCase]:
    """
    Load project cases from JSON file
    
    Args:
        file_path: Path to JSON file (default from settings)
        
    Returns:
        List of ProjectCase objects
    """
    try:
        path = file_path or settings.data_file_path
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        projects = [ProjectCase(**item) for item in data]
        print(f"✅ Loaded {len(projects)} project cases from {path}")
        return projects
        
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        raise
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        raise

def format_project_for_embedding(project: ProjectCase) -> str:
    """
    Format project case into a single text for embedding
    
    Args:
        project: ProjectCase object
        
    Returns:
        Formatted string
    """
    return f"""Problem: {project.problem_description}
AI Approach: {project.ai_approach}
Tech Stack: {project.tech_stack}
Outcome: {project.outcome}"""

def extract_metadata(project: ProjectCase, project_id: str) -> Dict[str, Any]:
    """
    Extract metadata for vector store
    
    Args:
        project: ProjectCase object
        project_id: Unique identifier
        
    Returns:
        Metadata dictionary
    """
    return {
        "project_id": project_id,
        "problem": project.problem_description,
        "approach": project.ai_approach,
        "tech_stack": project.tech_stack,
        "outcome": project.outcome
    }