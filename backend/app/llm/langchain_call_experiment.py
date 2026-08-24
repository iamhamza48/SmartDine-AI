from app.llm.langchain_client import llm

if __name__ == "__main__":
    result = llm.invoke("What needs restocking? Chicken: 12kg (min 15kg).")
    print(result.content)