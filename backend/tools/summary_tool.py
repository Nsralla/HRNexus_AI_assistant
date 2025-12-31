import os
import logging
from langchain_openai import ChatOpenAI

# Setup logger
logger = logging.getLogger(__name__)


class SummaryTool:
    """ 
    Tool for creating summaries from langgraph outputs.
    Provides methods for summarizing HR-related AI responses.
    """
    
    def __init__(self):
        """ 
        Initialize the Summary tool and the LLM.
        """
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("SUMMARY_TOOL"),
            model=os.getenv("SUMMARY_MODEL", "google/gemma-3n-e2b-it:free"),
            max_tokens=1000,
            temperature=0.3,
        )

    def create_summary(self, text: str) -> str:
        """
        Create a concise summary of the given text.
        This method is called by CrewAI agents to summarize langgraph outputs.
        
        Args:
            text: The text to summarize (typically output from langgraph pipeline)
            
        Returns:
            A concise summary preserving key information
        """
        prompt = f"""You are an HR assistant that creates concise summaries of AI-generated responses.

Your task:
- Summarize the following text while preserving all key information
- Keep the summary concise but comprehensive (aim for 50-200 words)
- Maintain the same language as the input text
- Focus on actionable insights and important details
- Ensure the summary is professional and suitable for HR communications

Text to summarize:
{text}

Summary:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            logger.error(f"Error creating summary: {e}")
            return text
