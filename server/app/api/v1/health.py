from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict, Any
import time

from app.core.database import get_db
from app.services.llm_service import llm_service

router = APIRouter()

@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Checks the health of the system, including database and LLM connections.
    """
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {}
    }

    # Check Database
    try:
        start_time = time.time()
        await db.execute(text("SELECT 1"))
        db_latency = (time.time() - start_time) * 1000
        health_status["services"]["database"] = {
            "status": "healthy",
            "latency_ms": round(db_latency, 2)
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    # Check LLM (Ollama)
    llm_health = await llm_service.check_health()
    health_status["services"]["llm"] = llm_health
    if llm_health["status"] != "healthy":
        health_status["status"] = "degraded"

    return health_status

@router.get("/llm")
async def check_llm():
    """ Specifically check LLM health """
    return await llm_service.check_health()

@router.get("/db")
async def check_db(db: AsyncSession = Depends(get_db)):
    """ Specifically check Database health """
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "message": "Database connection established"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@router.get("/test-llm")
async def test_llm_connection():
    """
    Performs a live test by sending a simple prompt to Ollama.
    """
    test_prompt = "Hi, what color is the sky? Answer in one word."
    try:
        start_time = time.time()
        response = await llm_service.generate_response(test_prompt, temperature=0.0)
        latency = (time.time() - start_time) * 1000
        
        if "Error" in response or not response:
            return {
                "status": "unhealthy",
                "error": response or "Empty response from LLM",
                "prompt": test_prompt
            }
            
        return {
            "status": "healthy",
            "prompt": test_prompt,
            "response": response.strip(),
            "latency_ms": round(latency, 2)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
