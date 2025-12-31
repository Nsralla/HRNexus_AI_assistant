"""
Documentation query prompt for RAG-based responses.
"""

DOCUMENTATION_QUERY_PROMPT = """Using the following documentation, answer the user's question.
Be concise but comprehensive. Use markdown formatting for clarity.

Documentation:
{context}

User Question: {user_query}

Provide a helpful, well-formatted answer based on the documentation above."""

