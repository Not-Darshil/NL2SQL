from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
from app.models.order import Order, OrderItem
from app.models.menu import MenuItem
from decimal import Decimal

class OrderService:
    async def get_or_create_cart(self, db: AsyncSession, user_id: uuid.UUID) -> Order:
        """
        Retrieves the active cart for a user or creates a new one.
        """
        query = select(Order).where(
            and_(Order.user_id == user_id, Order.status == "cart")
        )
        result = await db.execute(query)
        cart = result.scalar_one_or_none()

        if not cart:
            cart = Order(user_id=user_id, status="cart", total_amount=Decimal("0.00"))
            db.add(cart)
            await db.flush() # Get the ID
        
        return cart

    async def add_to_cart(
        self, 
        db: AsyncSession, 
        user_id: uuid.UUID, 
        menu_item_id: uuid.UUID, 
        quantity: int = 1
    ) -> Tuple[bool, str]:
        """
        Adds an item to the user's cart and updates total amount.
        """
        cart = await self.get_or_create_cart(db, user_id)
        
        # Get item price
        item_query = select(MenuItem).where(MenuItem.id == menu_item_id)
        item_result = await db.execute(item_query)
        item = item_result.scalar_one_or_none()
        
        if not item:
            return False, "Item not found."

        # Check if item already in cart
        oi_query = select(OrderItem).where(
            and_(OrderItem.order_id == cart.id, OrderItem.menu_item_id == menu_item_id)
        )
        oi_result = await db.execute(oi_query)
        order_item = oi_result.scalar_one_or_none()

        if order_item:
            order_item.quantity += quantity
            order_item.subtotal = order_item.quantity * order_item.price_at_order
        else:
            order_item = OrderItem(
                order_id=cart.id,
                menu_item_id=menu_item_id,
                quantity=quantity,
                price_at_order=item.price,
                subtotal=item.price * quantity
            )
            db.add(order_item)

        # Update cart total
        cart.total_amount += (item.price * quantity)
        await db.commit()
        return True, f"Added {quantity}x {item.name} to cart."

    async def checkout(self, db: AsyncSession, user_id: uuid.UUID) -> Tuple[bool, str]:
        """
        Moves cart to pending and sets cancellation deadline.
        """
        cart = await self.get_or_create_cart(db, user_id)
        
        # Check if cart is empty
        items_query = select(OrderItem).where(OrderItem.order_id == cart.id)
        items_result = await db.execute(items_query)
        if not items_result.scalars().all():
            return False, "Your cart is empty."

        cart.status = "pending"
        cart.cancellation_deadline = datetime.now() + timedelta(minutes=2)
        
        await db.commit()
        return True, "Order placed successfully! You have 2 minutes to cancel if needed."

    async def cancel_order(self, db: AsyncSession, user_id: uuid.UUID) -> Tuple[bool, str]:
        """
        Cancels the latest pending order if within deadline.
        """
        query = select(Order).where(
            and_(Order.user_id == user_id, Order.status == "pending")
        ).order_by(Order.created_at.desc())
        
        result = await db.execute(query)
        order = result.scalar_one_or_none()

        if not order:
            return False, "No pending order found to cancel."

        if order.cancellation_deadline and datetime.now() > order.cancellation_deadline:
            return False, "Cancellation window (2 minutes) has expired."

        order.status = "cancelled"
        await db.commit()
        return True, "Order cancelled successfully."

order_service = OrderService()
