from fastapi import Request

from session_store import get_session

class SessionMiddleware:

    async def __call__(self, request: Request, call_next):

        # Read cookie from the incoming request
        session_id = request.cookies.get("session_id")

        # Default: no authenticated session
        request.state.session = None
        request.state.session_id = None

        if session_id:

            session = get_session(session_id)

            if session:
                request.state.session = session
                request.state.session_id = session_id

        response = await call_next(request)

        return response
