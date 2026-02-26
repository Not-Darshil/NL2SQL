import json
from typing import Dict, Any, Optional
from app.services.llm_service import llm_service
from app.services.menu_service import menu_service
from sqlalchemy.ext.asyncio import AsyncSession

class MenuAgent:
    def __init__(self):
        self.system_prompt = """
        You are a Menu Expert for TableMind AI. 
        Extract filtering criteria from the user's query about the menu.
        Respond with a JSON object containing:
        - is_vegetarian: boolean or null
        - is_spicy: boolean or null
        - max_price: number or null
        - search_query: string or null

        Example: "Show me some spicy vegetarian food under $15"
        Output: {"is_vegetarian": true, "is_spicy": true, "max_price": 15.0, "search_query": null}
        """

    async def handle_query(self, user_message: str, db: AsyncSession) -> str:
        # 1. Extract filters using LLM
        response = await llm_service.generate_response(user_message, system_prompt=self.system_prompt, temperature=0.0)
        
        try:
            filters = json.loads(response)
        except:
            filters = {}

        # 2. Call MenuService
        items = await menu_service.get_menu_items(
            db=db,
            is_vegetarian=filters.get("is_vegetarian"),
            is_spicy=filters.get("is_spicy"),
            max_price=filters.get("max_price"),
            search_query=filters.get("search_query")
        )

        # 3. Format Response
        if not items:
            return "I couldn't find any items matching those criteria. Would you like to see our full menu?"
        
        reply = "Here are some items I found for you:\n"
        for item in items[:5]: # Cap at 5 for chat
            tags = []
            if item.is_vegetarian: tags.append("Veg")
            if item.is_spicy: tags.append("Spicy")
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            reply += f"- **{item.name}** (${item.price}){tag_str}: {item.description}\n"
            
        return reply

menu_agent = MenuAgent()
