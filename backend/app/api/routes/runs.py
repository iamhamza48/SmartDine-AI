import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.graph.persistent_graph import get_app_graph

router = APIRouter()
app_graph = get_app_graph()

@router.get("/runs/{thread_id}/stream")
def stream_run(thread_id: str, message: str, restaurant_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    def event_gen():
        for chunk in app_graph.stream(
            {"messages": [("user", message)], "restaurant_id": restaurant_id},
            config=config,
            stream_mode="updates",
        ):
            yield f"data: {json.dumps(chunk, default=str)}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")