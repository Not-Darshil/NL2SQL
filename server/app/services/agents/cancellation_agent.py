import uuid
from app.services.order_service import order_service
from sqlalchemy.ext.asyncio import AsyncSession

class CancellationAgent:
    async def handle_cancellation(self, user_id: uuid.UUID, db: AsyncSession) -> str:
        """
        Directly calls OrderService to attempt cancellation.
        """
        success, message = await order_service.cancel_order(db, user_id)
        return message

cancellation_agent = CancellationAgent()
