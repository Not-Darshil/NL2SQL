from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.menu import MenuItem
from decimal import Decimal

class MenuService:
    async def get_menu_items(
        self, 
        db: AsyncSession, 
        category_id: Optional[str] = None,
        is_vegetarian: Optional[bool] = None,
        is_spicy: Optional[bool] = None,
        max_price: Optional[Decimal] = None,
        search_query: Optional[str] = None
    ) -> List[MenuItem]:
        """
        Fetch menu items with optional filters.
        """
        query = select(MenuItem).where(MenuItem.is_available == True)

        if category_id:
            query = query.where(MenuItem.category_id == category_id)
        if is_vegetarian is not None:
            query = query.where(MenuItem.is_vegetarian == is_vegetarian)
        if is_spicy is not None:
            query = query.where(MenuItem.is_spicy == is_spicy)
        if max_price:
            query = query.where(MenuItem.price <= max_price)
        if search_query:
            query = query.where(MenuItem.name.ilike(f"%{search_query}%"))

        result = await db.execute(query)
        return result.scalars().all()

menu_service = MenuService()
