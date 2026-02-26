from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.api.api import api_router

app = FastAPI(title="TableMind AI API", version="1.0.0")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to TableMind AI API"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Try to execute a simple query to check the database connection
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
