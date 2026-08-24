from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    restaurant_id: str
    draft_order: dict | None
    approval_requested: bool