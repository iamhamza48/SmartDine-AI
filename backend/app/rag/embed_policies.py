import glob
from google.genai import types
from app.llm.gemini_client import client
from app.config.db import engine
from sqlalchemy import text

EMBED_MODEL = "gemini-embedding-001"

def embed(text_input: str) -> list[float]:
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=text_input,
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    return response.embeddings[0].values

if __name__ == "__main__":
    with engine.begin() as conn:
        for filepath in glob.glob("data/policies/*.md"):
            content = open(filepath).read()
            vec = embed(content)
            conn.execute(
                text("insert into policy_documents (content, embedding) values (:content, :embedding)"),
                {"content": content, "embedding": str(vec)}
            )
    print("Policies embedded.")