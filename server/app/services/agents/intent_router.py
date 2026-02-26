from typing import Dict, Any
from app.services.llm_service import llm_service

class IntentRouterAgent:
    def __init__(self):
        self.system_prompt = """
        You are an Intent Router for a Restaurant Management AI called TableMind AI.
        Your job is to classify the user's input into one of the following intents:

        1. MENU_QUERY: User asking about menu items, prices, ingredients, or dietary options (veg/spicy).
        2. ORDER_ACTION: User wants to create or update an order/cart.
        3. ORDER_CANCEL: User wants to cancel an order.
        4. ANALYTICS_QUERY: User asking for high-level stats, sales, or data that requires SQL (NL2SQL).
        5. RECOMMENDATION: User asking for suggestions based on preferences.
        6. GENERAL_QUERY: Greetings or generic questions not related to the above.

        Respond ONLY with the category name.
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
