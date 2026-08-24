from langchain_core.tools import tool
from app.rag.retrieve import retrieve_policy

@tool
def check_policy(question: str) -> str:
    """Retrieves the most relevant restaurant policy text for a question."""
    chunks = retrieve_policy(question)
    return "\n---\n".join(chunks) if chunks else "No relevant policy found."