import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import settings

# LangChain reads these directly from the environment
os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2).lower()
os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=settings.gemini_api_key,
    temperature=0.2,
    max_retries=4,          # built-in retry, still respects free-tier RPM
)