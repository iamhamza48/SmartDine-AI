from app.llm.langchain_client import llm
from app.tools.inventory_tools import check_low_stock

inventory_llm = llm.bind_tools([check_low_stock])

def run_inventory_agent(user_message: str):
    response = inventory_llm.invoke(user_message)
    if response.tool_calls:
        for call in response.tool_calls:
            if call["name"] == "check_low_stock":
                result = check_low_stock.invoke(call["args"])
                return result
    return response.content

if __name__ == "__main__":
    print(run_inventory_agent("What's running low at restaurant abc-123? restaurant_id=abc-123"))