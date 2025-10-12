from strawberry.types import Info
from fastapi import Request

async def get_context(request: Request):
    """
    Fournit db et user_id pour chaque requête GraphQL.
    """
    user_id = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer "):]
        from app.services.auth_service import verify_access_token
        from jose import JWTError
        try:
            user_id = verify_access_token(token)
        except JWTError:
            user_id = None

    from app.db.base import get_db
    async for db in get_db():
        yield {"db": db, "user_id": user_id}
