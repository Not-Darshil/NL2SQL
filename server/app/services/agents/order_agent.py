import json
from typing import Dict, Any
import uuid
from app.services.llm_service import llm_service
from app.services.order_service import order_service
from app.services.menu_service import menu_service
from sqlalchemy.ext.asyncio import AsyncSession

class OrderAgent:
    def __init__(self):
        self.system_prompt = """
        You are an Order Assistant for TableMind AI.
        Determine the user's action: "ADD_TO_CART", "CHECKOUT", or "VIEW_CART".
        For "ADD_TO_CART", extract the item name.

        Respond with JSON:
        {"action": "ACTION_NAME", "item_name": "STRING or null"}
        """

    async def handle_request(self, user_id: uuid.UUID, message: str, db: AsyncSession) -> str:
        response = await llm_service.generate_response(message, system_prompt=self.system_prompt, temperature=0.0)
        
        try:
            data = json.loads(response)
        except:
            return "I'm sorry, I couldn't understand your order request."

        action = data.get("action")
        
        if action == "ADD_TO_CART":
            item_name = data.get("item_name")
            if not item_name:
                return "Which item would you like to add to your cart?"
            
            # Find item by name
            items = await menu_service.get_menu_items(db, search_query=item_name)
            if not items:
                return f"I couldn't find '{item_name}' on the menu."
            
            item = items[0] # Take first match
            success, msg = await order_service.add_to_cart(db, user_id, item.id)
            return msg

        elif action == "CHECKOUT":
            success, msg = await order_service.checkout(db, user_id)
            return msg

        elif action == "VIEW_CART":
            cart = await order_service.get_or_create_cart(db, user_id)
            # Fetch items (would be better in OrderService, but doing here for brevity)
            from app.models.order import OrderItem
            from sqlalchemy import select
            query = select(OrderItem).where(OrderItem.order_id == cart.id)
            res = await db.execute(query)
            items = res.scalars().all()
            
            if not items:
                return "Your cart is currently empty."
            
            reply = "Your cart contains:\n"
            for item in items:
                reply += f"- {item.quantity}x Item (ID: {item.menu_item_id[:8]}...)\n"
            reply += f"**Total: ${cart.total_amount}**\nTo place your order, say 'checkout'."
            return reply

        return "How can I help you with your order?"

order_agent = OrderAgent()
