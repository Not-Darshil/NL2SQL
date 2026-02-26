from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ChatLogBase(BaseModel):
    user_id: UUID
    message: str
    sender: str
    intent: Optional[str] = None

class ChatLogCreate(ChatLogBase):
    pass

class ChatLog(ChatLogBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
