from fastapi import APIRouter
from app.api.v1 import chat, auth

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/v1/chat", tags=["chat"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
