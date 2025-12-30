from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any
import queue
import threading
from typing import Dict, List
class StreamingCallbackHandler(BaseCallbackHandler):
    """
    Custom callback handler for streaming LLM tokens.
    Collects tokens in a queue that can be consumed by Streamlit or other interfaces.
    """
    
    def __init__(self):
        self.token_queue = queue.Queue()
        self.tokens = []
        self.is_streaming = True
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Called when LLM starts generating"""
        pass
    
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Called when LLM generates a new token"""
        if self.is_streaming:
            self.tokens.append(token)
            self.token_queue.put(token)
    
    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """Called when LLM finishes generating"""
        self.token_queue.put(None)  # Signal end of stream
    
    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Called when LLM encounters an error"""
        self.token_queue.put(None)  # Signal end of stream
    
    def get_tokens(self):
        """Get all collected tokens"""
        return ''.join(self.tokens)
    
    def reset(self):
        """Reset the handler for new generation"""
        self.tokens = []
        self.is_streaming = True
        # Clear the queue
        while not self.token_queue.empty():
            try:
                self.token_queue.get_nowait()
            except queue.Empty:
                break