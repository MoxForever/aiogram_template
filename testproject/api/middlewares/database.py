from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from ...database import DAO, DatabaseConnection


class DatabaseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, db_connection: DatabaseConnection):
        super().__init__(app)
        self.db_connection = db_connection

    async def dispatch(self, request: Request, call_next) -> Response:
        async with DAO(self.db_connection) as dao:
            request.state.dao = dao
            return await call_next(request)
