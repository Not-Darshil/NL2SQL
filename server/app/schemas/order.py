from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class OrderItemBase(BaseModel):
    menu_item_id: UUID
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: UUID
    price_at_order: Decimal
    subtotal: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    user_id: UUID
    status: str = "pending"
    total_amount: Decimal
    cancellation_deadline: Optional[datetime] = None

class OrderCreate(BaseModel):
    user_id: UUID
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItem] = []

    model_config = ConfigDict(from_attributes=True)
