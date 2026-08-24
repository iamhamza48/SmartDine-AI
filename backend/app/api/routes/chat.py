import logging

from fastapi import APIRouter
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel

from app.graph.hitl_graph import graph
from app.graph.persistent_graph import get_app_graph, set_app_graph_override

logger = logging.getLogger(__name__)

router = APIRouter()
app_graph = get_app_graph()


class ChatRequest(BaseModel):
    thread_id: str
    message: str
    restaurant_id: str


@router.post("/chat")
def chat(payload: ChatRequest):
    global app_graph

    config = {"configurable": {"thread_id": payload.thread_id}}
    try:
        result = app_graph.invoke(
            {"messages": [("user", payload.message)], "restaurant_id": payload.restaurant_id},
            config=config,
        )
    except Exception as exc:
        logger.warning("Chat graph invocation failed for thread %s; rebuilding graph with in-memory fallback: %s", payload.thread_id, exc)
        app_graph = graph.compile(checkpointer=InMemorySaver())
        set_app_graph_override(app_graph)
        result = app_graph.invoke(
            {"messages": [("user", payload.message)], "restaurant_id": payload.restaurant_id},
            config=config,
        )

    state = app_graph.get_state(config)
    values = state.values

    return {
        "response": result["messages"][-1].content,
        "draft_order": values.get("draft_order"),
        "approval_requested": values.get("approval_requested", False),
    }
