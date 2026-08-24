import logging
from functools import lru_cache

from langgraph.checkpoint.memory import InMemorySaver
from app.config.settings import settings
from app.graph.hitl_graph import graph  # reuse the same StateGraph definition from Phase 7

logger = logging.getLogger(__name__)
_postgres_saver_context = None
_app_graph_override = None


@lru_cache(maxsize=1)
def get_app_graph():
    global _postgres_saver_context

    if _app_graph_override is not None:
        return _app_graph_override

    try:
        from langgraph.checkpoint.postgres import PostgresSaver

        _postgres_saver_context = PostgresSaver.from_conn_string(settings.database_url)
        checkpointer = _postgres_saver_context.__enter__()
        checkpointer.setup()  # idempotent — creates checkpoint tables first run only
        return graph.compile(checkpointer=checkpointer)
    except Exception as exc:
        _postgres_saver_context = None
        logger.warning("Postgres checkpointer unavailable, falling back to in-memory saver: %s", exc)
        return graph.compile(checkpointer=InMemorySaver())


def set_app_graph_override(app_graph):
    global _app_graph_override
    _app_graph_override = app_graph
    get_app_graph.cache_clear()

if __name__ == "__main__":
    from langgraph.types import Command
    app_graph = get_app_graph()
    config = {"configurable": {"thread_id": "demo-persistent-1"}}

    # Run 1: start and hit the interrupt, then this process exits
    result = app_graph.invoke({"messages": [], "restaurant_id": "abc-123"}, config=config)
    print("Run 1 paused. Restart this script and it will resume from Postgres.")

    # Comment the block above and uncomment below to simulate a fresh process resuming:
    # result = app_graph.invoke(Command(resume="approve"), config=config)
    # print("Resumed after restart:", result["messages"][-1])