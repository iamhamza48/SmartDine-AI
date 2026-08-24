import json

from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from app.graph.state import AgentState
from app.llm.langchain_client import llm
from google.genai import types
from app.llm.gemini_client import client, MODEL


class PurchaseOrderItem(BaseModel):
    item_name: str
    quantity: float
    unit: str
    unit_price: float


class PurchaseOrderDraft(BaseModel):
    supplier_name: str
    items: list[PurchaseOrderItem]
    total_amount: float


def draft_order(state: AgentState):
    response = client.models.generate_content(
        model=MODEL,
        contents="Draft a purchase order: Chicken 8kg at $5.25/kg, Rice 7kg at $2.50/kg, from Fresh Foods Ltd.",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PurchaseOrderDraft,
            temperature=0.1,
        ),
    )
    draft = PurchaseOrderDraft.model_validate_json(response.text)
    return {
        "messages": [{"role": "assistant", "content": draft.model_dump_json()}],
        "draft_order": draft.model_dump(),
        "approval_requested": True,
    }


def request_approval(state: AgentState):
    draft = state.get("draft_order") or {}

    if not state.get("approval_requested", False):
        return {
            "messages": [{"role": "assistant", "content": json.dumps(draft, default=str)}],
            "draft_order": draft,
            "approval_requested": False,
        }

    decision = interrupt({"draft_order": draft, "action": "approve/reject/edit?"})
    return {
        "messages": [{"role": "user", "content": f"Decision: {decision}"}],
        "draft_order": draft,
        "approval_requested": False,
    }

graph = StateGraph(AgentState)
graph.add_node("draft_order", draft_order)
graph.add_node("request_approval", request_approval)
graph.set_entry_point("draft_order")
graph.add_edge("draft_order", "request_approval")
graph.add_edge("request_approval", END)

checkpointer = InMemorySaver()
app_graph = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "demo-1"}}
    result = app_graph.invoke({"messages": [], "restaurant_id": "abc-123"}, config=config)
    print("Paused. Pending state:", app_graph.get_state(config).values.get("draft_order"))

    decision = input("approve / reject / edit? ")
    result = app_graph.invoke(Command(resume=decision), config=config)
    print("Resumed:", result["messages"][-1])