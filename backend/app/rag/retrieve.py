from sqlalchemy import text
from app.config.db import engine
from app.rag.embed_policies import embed

def retrieve_policy(query: str, k: int = 2) -> list[str]:
    q_vec = embed(query)
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                select content from policy_documents
                order by embedding <=> (:q_vec)::vector
                limit :k
            """),
            {"q_vec": str(q_vec), "k": k}
        ).fetchall()
    return [r[0] for r in rows] 