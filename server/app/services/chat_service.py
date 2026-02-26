from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.agents.intent_router import intent_router
from app.services.agents.nl2sql import nl2sql_agent
from app.services.agents.menu_agent import menu_agent
from app.services.agents.order_agent import order_agent
from app.services.agents.cancellation_agent import cancellation_agent
from app.services.agents.recommendation import recommendation_agent
from app.services.analytics_service import analytics_service
from app.models.chat import ChatLog
import uuid

class ChatService:
    async def process_message(
        self, 
        user_id: uuid.UUID, 
        message: str, 
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Main orchestration flow.
        """
        # 1. Identify Intent
        intent = await intent_router.route(message)
        
        response_text = ""
        agent_data = {}

        # 2. Handle Intent
        if intent == "ANALYTICS_QUERY":
            sql = await nl2sql_agent.generate_sql(message)
            if sql:
                data = await analytics_service.execute_query(db, sql)
                response_text = await analytics_service.format_results(message, data)
                agent_data["sql"] = sql
                agent_data["results"] = data
            else:
                response_text = "I'm sorry, I couldn't safely generate a data query for that request."
        
        elif intent == "MENU_QUERY":
            response_text = await menu_agent.handle_query(message, db)
            
        elif intent == "ORDER_ACTION":
            response_text = await order_agent.handle_request(user_id, message, db)

        elif intent == "ORDER_CANCEL":
            response_text = await cancellation_agent.handle_cancellation(user_id, db)

        elif intent == "RECOMMENDATION":
            response_text = await recommendation_agent.recommend(message, db)
            
        else:
            response_text = "I am TableMind AI, your restaurant assistant. How can I help you? You can ask about the menu, place an order, or query sales data."

        # 3. Log to DB
        user_log = ChatLog(user_id=user_id, message=message, sender="user", intent=intent)
        db.add(user_log)
        
        assistant_log = ChatLog(user_id=user_id, message=response_text, sender="assistant", intent=intent)
        db.add(assistant_log)
        
        await db.commit()

        return {
            "intent": intent,
            "response": response_text,
            "data": agent_data
        }

chat_service = ChatService()
