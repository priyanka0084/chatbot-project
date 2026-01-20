from groq import Groq
from typing import List, Dict
from backend.config import settings

class LLMService:
    """Service for LLM chat completions using Groq"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.llm_model
        
    def generate_response(
        self, 
        system_prompt: str, 
        user_message: str,
        context: str = "",
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate LLM response with RAG context
        
        Args:
            system_prompt: System instructions for the LLM
            user_message: User's query
            context: Retrieved context from vector store
            temperature: Sampling temperature
            max_tokens: Max response length
            
        Returns:
            Generated response text
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            if context:
                messages.append({
                    "role": "system", 
                    "content": f"Relevant past projects:\n\n{context}"
                })
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.temperature,
                max_tokens=max_tokens or settings.max_tokens,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ LLM generation failed: {e}")
            raise
    
    def generate_with_conversation_history(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        context: str = ""
    ) -> str:
        """
        Generate response with conversation history
        
        Args:
            system_prompt: System instructions
            conversation_history: List of {role, content} dicts
            context: Retrieved RAG context
            
        Returns:
            Generated response
        """
        try:
            messages = [{"role": "system", "content": system_prompt}]
            
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Relevant past projects:\n\n{context}"
                })
            
            messages.extend(conversation_history)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ LLM with history failed: {e}")
            raise