from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.llm.langchain_client import llm
from app.tools.inventory_tools import check_low_stock

model_with_tools = llm.bind_tools([check_low_stock])

def call_agent(state: AgentState):
    result = model_with_tools.invoke(state["messages"])
    return {"messages": [result]}

def run_tools(state: AgentState):
    last = state["messages"][-1]
    outputs = []
    for call in last.tool_calls:
        if call["name"] == "check_low_stock":
            result = check_low_stock.invoke(call["args"])
            outputs.append({"role": "tool", "content": str(result), "tool_call_id": call["id"]})
    return {"messages": outputs}

def should_continue(state: AgentState):
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else END

graph = StateGraph(AgentState)
graph.add_node("agent", call_agent)
graph.add_node("tools", run_tools)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app_graph = graph.compile()

if __name__ == "__main__":
    result = app_graph.invoke({
        "messages": [("user", "What's low on stock? restaurant_id=abc-123")],
        "restaurant_id": "abc-123",
    })
    print(result["messages"][-1].content)