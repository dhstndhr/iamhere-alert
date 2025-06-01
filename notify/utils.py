from sqlalchemy.orm import Session
from db import SessionLocal
from models import User
from typing import Optional
def get_user_token(name: str)  -> Optional[str]:
    session: Session = SessionLocal()
    try:
        user = session.query(User).filter(User.name == name).first()
        if user and user.fcm_token:
            return user.fcm_token
        return None
    finally:
        session.close()

