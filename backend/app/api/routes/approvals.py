import logging

from fastapi import APIRouter, HTTPException
from langgraph.types import Command
from app.graph.persistent_graph import get_app_graph

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/approvals/{thread_id}/approve")
def approve(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        result = get_app_graph().invoke(Command(resume="approve"), config=config)
    except Exception as exc:
        logger.exception("Could not resume approval for thread %s", thread_id)
        raise HTTPException(status_code=500, detail=f"Could not resume approval: {exc}") from exc
    return {"status": "approved", "result": str(result["messages"][-1])}

@router.post("/approvals/{thread_id}/reject")
def reject(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        result = get_app_graph().invoke(Command(resume="reject"), config=config)
    except Exception as exc:
        logger.exception("Could not resume rejection for thread %s", thread_id)
        raise HTTPException(status_code=500, detail=f"Could not resume rejection: {exc}") from exc
    return {"status": "rejected", "result": str(result["messages"][-1])}