import os
import logging
from langchain_openai import ChatOpenAI

# Setup logger
logger = logging.getLogger(__name__)


class FormatTool:
    """ 
    Tool for formatting responses from langgraph outputs.
    Formats AI responses into clear, professional, and well-structured formats suitable for HR communications.
    """
    
    def __init__(self):
        """ 
        Initialize the Format tool and the LLM.
        """
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("FORMAT_TOOL"),
            model=os.getenv("FORMAT_MODEL", "google/gemma-3n-e2b-it:free"),
            max_tokens=600,
            temperature=0.3,
        )

    def format_response(self, text: str) -> str:
        """
        Format the given text into a clear, professional, and well-structured response.
        This method formats langgraph outputs for better readability in HR contexts.
        
        Args:
            text: The text to format (typically output from langgraph pipeline)
            
        Returns:
            A well-formatted response with proper structure, bullet points, and sections
        """
        prompt = f"""You are an HR communication specialist that formats AI responses for clarity and professionalism.

Your task:
- Format the following text into a clear, well-structured response
- Use appropriate formatting: bullet points, numbered lists, sections, and paragraphs
- Ensure the tone is professional and suitable for HR communications
- Make the response easy to read and actionable
- Preserve all important information
- Add clear section headers if the content has multiple topics
- Use markdown formatting for better readability

Text to format:
{text}

Formatted response:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return text

