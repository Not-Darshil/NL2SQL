from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class MenuCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class MenuCategoryCreate(MenuCategoryBase):
    pass

class MenuCategory(MenuCategoryBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    is_vegetarian: bool = False
    is_spicy: bool = False
    is_available: bool = True
    image_url: Optional[str] = None
    category_id: UUID

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    is_vegetarian: Optional[bool] = None
    is_spicy: Optional[bool] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None
    category_id: Optional[UUID] = None

class MenuItem(MenuItemBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
