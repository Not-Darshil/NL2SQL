from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Any, List, Dict
from app.services.llm_service import llm_service

class AnalyticsService:
    async def execute_query(self, db: AsyncSession, sql: str) -> List[Dict[str, Any]]:
        """
        Executes raw SELECT SQL and returns results as list of dicts.
        """
        result = await db.execute(text(sql))
        # result.mappings() provides a dictionary-like interface for rows
        return [dict(row) for row in result.mappings().all()]

    async def format_results(self, user_query: str, data: List[Dict[str, Any]]) -> str:
        """
        Uses LLM to summarize the database results into a human-readable sentence.
        """
        if not data:
            return "I couldn't find any data matching that request."

        system_prompt = "You are a data analyst for TableMind AI. Summarize the following data into a concise, professional sentence for the user."
        prompt = f"User Question: {user_query}\nData: {data}\nSummary:"
        
        summary = await llm_service.generate_response(prompt, system_prompt=system_prompt)
        return summary

analytics_service = AnalyticsService()
