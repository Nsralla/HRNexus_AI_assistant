"""
Centralized prompts for the HR Nexus AI Assistant.
All prompts are stored here for easy maintenance and updates.
"""

from .intent_classification import INTENT_CLASSIFICATION_PROMPT
from .documentation_query import DOCUMENTATION_QUERY_PROMPT
from .general_conversation import GENERAL_CONVERSATION_SYSTEM_PROMPT
from .data_query import DATA_QUERY_SYSTEM_PROMPT

__all__ = [
    "INTENT_CLASSIFICATION_PROMPT",
    "DOCUMENTATION_QUERY_PROMPT",
    "GENERAL_CONVERSATION_SYSTEM_PROMPT",
    "DATA_QUERY_SYSTEM_PROMPT",
]

