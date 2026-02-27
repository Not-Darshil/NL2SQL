from typing import Dict, Any
from app.services.llm_service import llm_service

class IntentRouterAgent:
    def __init__(self):
        self.system_prompt = """
        You are an Intent Router for a Restaurant Management AI called TableMind AI.
        Your job is to classify the user's input into one of the following intents:

        1. MENU_QUERY: User asking about menu items, prices, ingredients, dietary options (veg/spicy), or just asking to see/browse the menu.
        2. ORDER_ACTION: User wants to create or update an order, add items to cart, or place an order.
        3. ORDER_CANCEL: User wants to cancel an existing order.
        4. ANALYTICS_QUERY: User asking for high-level stats, sales, revenue, or data that requires database aggregation/SQL.
        5. RECOMMENDATION: User asking for suggestions or what they should eat.
        6. GENERAL_QUERY: Greetings, "who are you", or small talk.

        Respond with ONLY the intent name in uppercase.
        
        Example 1: "Hi there" -> GENERAL_QUERY
        Example 2: "Show me the menu" -> MENU_QUERY
        Example 3: "How much is the burger?" -> MENU_QUERY
        Example 4: "I want to order a pizza" -> ORDER_ACTION
        Example 5: "Total sales today?" -> ANALYTICS_QUERY
        Example 6: "What's good for dinner?" -> RECOMMENDATION
        """

    async def route(self, user_message: str) -> str:
        prompt = f"User message: {user_message}\nIntent:"
        intent = await llm_service.generate_response(prompt, system_prompt=self.system_prompt, temperature=0.0)
        
        # Clean up response case and whitespace
        intent = intent.strip().upper()
        
        valid_intents = [
            "MENU_QUERY", "ORDER_ACTION", "ORDER_CANCEL", 
            "ANALYTICS_QUERY", "RECOMMENDATION", "GENERAL_QUERY"
        ]
        
        for v in valid_intents:
            if v in intent:
                return v
                
        return "GENERAL_QUERY"

intent_router = IntentRouterAgent()
