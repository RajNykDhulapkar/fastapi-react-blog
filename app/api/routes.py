from fastapi import APIRouter

from app.api.endpoints import auth_endpoints, user_endpoints, post_endpoints
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(auth_endpoints.router,
                          prefix="/auth", tags=[settings.api_tags.AUTH])
api_router.include_router(user_endpoints.router,
                          prefix="/user", tags=[settings.api_tags.USER])
api_router.include_router(post_endpoints.router,
                          prefix="/post", tags=[settings.api_tags.POST])
