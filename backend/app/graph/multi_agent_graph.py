from typing import Literal
from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.llm.langchain_client import llm
from app.tools.inventory_tools import check_low_stock
from app.tools.forecast_tools import naive_forecast

inventory_model = llm.bind_tools([check_low_stock])
forecast_model = llm.bind_tools([naive_forecast])

def supervisor(state: AgentState) -> Literal["inventory_agent", "forecast_agent"]:
    last_msg = state["messages"][-1].content.lower() if state["messages"] else ""
    if any(w in last_msg for w in ["forecast", "predict", "tomorrow", "demand"]):
        return "forecast_agent"
    return "inventory_agent"

def inventory_node(state: AgentState):
    result = inventory_model.invoke(state["messages"])
    if result.tool_calls:
        tool_out = check_low_stock.invoke(result.tool_calls[0]["args"])
        return {"messages": [result, {"role": "tool", "content": str(tool_out)}]}
    return {"messages": [result]}

def forecast_node(state: AgentState):
    result = forecast_model.invoke(state["messages"])
    if result.tool_calls:
        tool_out = naive_forecast.invoke(result.tool_calls[0]["args"])
        return {"messages": [result, {"role": "tool", "content": str(tool_out)}]}
    return {"messages": [result]}

graph = StateGraph(AgentState)
graph.add_node("supervisor", lambda state: state)   # pass-through, routing happens in conditional edge
graph.add_node("inventory_agent", inventory_node)
graph.add_node("forecast_agent", forecast_node)
graph.set_entry_point("supervisor")
graph.add_conditional_edges("supervisor", supervisor, {
    "inventory_agent": "inventory_agent",
    "forecast_agent": "forecast_agent",
})
graph.add_edge("inventory_agent", END)
graph.add_edge("forecast_agent", END)

app_graph = graph.compile()

if __name__ == "__main__":
    for query in ["what's low on stock?", "what will we need tomorrow?"]:
        result = app_graph.invoke({"messages": [("user", query)], "restaurant_id": "abc-123"})
        print(query, "->", result["messages"][-1])