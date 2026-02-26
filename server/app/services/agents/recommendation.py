from app.services.llm_service import llm_service
from app.services.menu_service import menu_service
from sqlalchemy.ext.asyncio import AsyncSession

class RecommendationAgent:
    def __init__(self):
        self.system_prompt = """
        You are a Recommendation Expert for TableMind AI.
        Based on the user's preferences, provide helpful restaurant suggestions.
        Currently, you should focus on filtering the menu for them.
        """

    async def recommend(self, user_message: str, db: AsyncSession) -> str:
        # For now, let's just use the MenuAgent's logic or a simplified version
        # to find items that match the user's 'vibe'.
        items = await menu_service.get_menu_items(db, search_query=user_message)
        
        if not items:
            return "I don't have enough data to make a perfect recommendation yet, but I'd be happy to show you our most popular items!"

        reply = "Based on what you said, you might really enjoy these:\n"
        for item in items[:3]:
            reply += f"- **{item.name}**: {item.description}\n"
        
        return reply

recommendation_agent = RecommendationAgent()
