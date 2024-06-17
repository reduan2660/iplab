from fastapi import HTTPException, Cookie
from typing_extensions import Annotated
from datetime import datetime

from app.config import SessionLocal
from app.models import User, Session

async def get_user_from_session(SESSION: Annotated[str, Cookie()] = None):

    if SESSION is None:
        raise HTTPException(status_code=401, detail="Invalid session token")
    
    with SessionLocal() as db:
        session = db.query(Session).filter(Session.id == SESSION).first()
        if session is None:
            raise HTTPException(status_code=401, detail="Invalid session token")
        else:

            # check expiration
            if session.expires < datetime.now().timestamp():
                raise HTTPException(status_code=401, detail="Session token expired")
            else:
                user = db.query(User).filter(User.id == session.user_id).first()
                

                return {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "is_admin": user.is_admin,
                }