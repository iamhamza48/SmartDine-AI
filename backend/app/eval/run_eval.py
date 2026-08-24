import json
from langsmith.evaluation import evaluate
from langsmith import Client
from app.graph.multi_agent_graph import app_graph, supervisor

ls_client = Client()
cases = json.load(open("data/eval/test_cases.json"))

dataset_name = "restaurant-routing-eval"
if not ls_client.has_dataset(dataset_name=dataset_name):
    dataset = ls_client.create_dataset(dataset_name)
    for case in cases:
        ls_client.create_example(
            inputs={"query": case["query"]},
            outputs={"expected_agent": case["expected_agent"]},
            dataset_id=dataset.id,
        )

def predict(inputs: dict) -> dict:
    state = {"messages": [("user", inputs["query"])], "restaurant_id": "abc-123"}
    agent_used = supervisor(state)
    return {"agent_used": agent_used}

def routing_correct(run, example):
    return {"key": "routing_accuracy", "score": run.outputs["agent_used"] == example.outputs["expected_agent"]}

if __name__ == "__main__":
    evaluate(predict, data=dataset_name, evaluators=[routing_correct])